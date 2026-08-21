#!/usr/bin/env python3
"""Build a curated, deterministic repository review bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import Literal, TypedDict, cast


ZIP_LIMIT_BYTES = 25 * 1024 * 1024
ROOT_FIELDS = {
    "version",
    "repo_root",
    "bundle_dir",
    "title",
    "request",
    "context",
    "review_questions",
    "files",
}
FILE_FIELDS = {"kind", "source", "destination", "reason"}
SENSITIVE_PARTS = {
    ".aws",
    ".azure",
    ".docker",
    ".git",
    ".gnupg",
    ".ssh",
    "private",
    "secrets",
}
SENSITIVE_NAMES = (
    re.compile(r"(^|/)\.env($|[._/-])", re.IGNORECASE),
    re.compile(r"(^|/)(id_rsa|id_dsa|id_ecdsa|id_ed25519)(\.pub)?$", re.IGNORECASE),
    re.compile(r"\.(pem|p12|pfx|key)$", re.IGNORECASE),
    re.compile(
        r"(^|/)[^/]*(secret|token|credential|credentials|service[-_]?account|private[-_]?key|apikey|api[-_]?key)[^/]*$",
        re.IGNORECASE,
    ),
)
SECRET_VALUES = (
    re.compile(r"-----BEGIN (?:RSA |DSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"),
    re.compile(
        r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*(?:[\"'][A-Za-z0-9_./+=-]{12,}[\"']|[A-Za-z0-9_+=/-]{20,})"
    ),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{20,}"),
    re.compile(r"\b(?:sk|rk|pk|org|proj)-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bnpm_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    re.compile(r"\b(?:A3T|AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    re.compile(r"\bya29\.[0-9A-Za-z_-]{20,}\b"),
)

FileKind = Literal["context", "evidence", "source", "log"]


class FileSpec(TypedDict):
    kind: FileKind
    source: str
    destination: str
    reason: str


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    args = parser.parse_args()

    raw = json.loads(args.spec.read_text())
    assert isinstance(raw, dict), "spec must be a JSON object"
    assert set(raw) == ROOT_FIELDS, f"spec fields must be {sorted(ROOT_FIELDS)}"
    assert type(raw["version"]) is int and raw["version"] == 1, "unknown spec version"

    for field in (
        "repo_root",
        "bundle_dir",
        "title",
        "request",
        "context",
        "review_questions",
    ):
        assert isinstance(raw[field], str) and raw[field].strip(), (
            f"{field} must be a non-empty string"
        )
    assert isinstance(raw["files"], list) and raw["files"], (
        "files must be a non-empty list"
    )

    repo = Path(cast(str, raw["repo_root"]))
    assert repo.is_absolute() and repo.is_dir(), (
        "repo_root must be an existing absolute directory"
    )
    repo = repo.resolve()
    git_root = Path(_git(repo, "rev-parse", "--show-toplevel")).resolve()
    assert git_root == repo, "repo_root must be the git worktree root"

    bundle_rel = _relative_path(cast(str, raw["bundle_dir"]), "bundle_dir")
    assert bundle_rel.parent.name == "reviews", (
        "bundle_dir must be inside a reviews directory"
    )
    assert re.fullmatch(r"\d{8}_[a-z0-9_]+_review_bundle", bundle_rel.name), (
        "invalid bundle name"
    )
    _require_safe_path(bundle_rel)
    _require_no_symlink_parts(repo, bundle_rel, "bundle_dir")
    bundle = repo / bundle_rel
    assert bundle.resolve().is_relative_to(repo), "bundle_dir leaves repo_root"

    archive = bundle.with_suffix(".zip")
    checksum = Path(f"{archive}.sha256")
    temp_archive = archive.parent / f".{archive.name}.tmp"
    for path in (bundle, archive, checksum, temp_archive):
        if path.exists():
            raise SystemExit(f"refusing to overwrite existing output: {path}")

    title = cast(str, raw["title"])
    request = cast(str, raw["request"])
    context = cast(str, raw["context"])
    questions = cast(str, raw["review_questions"])
    for label, text in (
        ("title", title),
        ("request", request),
        ("context", context),
        ("review_questions", questions),
    ):
        _require_safe_text(label, text)

    selected: list[tuple[FileSpec, Path, Path]] = []
    sources: set[str] = set()
    destinations: set[str] = set()
    for index, value in enumerate(cast(list[object], raw["files"])):
        assert isinstance(value, dict), f"files[{index}] must be an object"
        item = cast(dict[str, object], value)
        assert set(item) == FILE_FIELDS, (
            f"files[{index}] fields must be {sorted(FILE_FIELDS)}"
        )
        for field in FILE_FIELDS:
            field_value = item[field]
            assert isinstance(field_value, str) and field_value.strip(), (
                f"files[{index}].{field} is required"
            )

        kind = cast(str, item["kind"])
        source_value = cast(str, item["source"])
        destination_value = cast(str, item["destination"])
        reason = cast(str, item["reason"])
        category = _category_dir(kind)
        source_rel = _relative_path(source_value, f"files[{index}].source")
        destination_rel = _relative_path(
            destination_value, f"files[{index}].destination"
        )
        source = repo / source_rel
        destination = bundle / category / destination_rel
        _require_safe_path(source_rel)
        _require_safe_path(Path(category) / destination_rel)
        _require_regular_repo_file(repo, source_rel, source)
        _require_safe_bytes(source_rel.as_posix(), source.read_bytes())
        _require_safe_text(f"files[{index}].reason", reason)

        source_key = source_rel.as_posix().casefold()
        destination_key = destination.relative_to(bundle).as_posix().casefold()
        assert source_key not in sources, f"duplicate source: {source_rel}"
        assert destination_key not in destinations, (
            f"duplicate destination: {destination.relative_to(bundle)}"
        )
        sources.add(source_key)
        destinations.add(destination_key)
        file_spec: FileSpec = {
            "kind": cast(FileKind, kind),
            "source": source_value,
            "destination": destination_value,
            "reason": reason,
        }
        selected.append((file_spec, source, destination))

    status = _git(repo, "status", "--short", "--untracked-files=all")
    branch = _git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    head = _git(repo, "rev-parse", "HEAD")
    changed_paths = len(status.splitlines()) if status else 0
    repository_context = (
        f"# Repository Context\n\n"
        f"- Repository: `{repo.name}`\n"
        f"- Branch: `{branch}`\n"
        f"- Revision: `{head}`\n"
        f"- Working tree: {'dirty' if status else 'clean'} ({changed_paths} changed paths)\n\n"
        f"{context.rstrip()}\n"
    )
    _require_safe_text("repository metadata", repository_context)

    bundle.mkdir(parents=True)
    generated = {
        Path("README.md"): _readme(title, selected),
        Path("REQUEST.txt"): request,
        Path("briefing/context.md"): repository_context,
        Path(
            "briefing/reviewer_questions.md"
        ): f"# Reviewer Questions\n\n{questions.rstrip()}\n",
    }
    for relative, text in generated.items():
        path = bundle / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode())

    for _, source, destination in selected:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)

    manifest_files: list[dict[str, object]] = []
    generated_reasons = {
        "README.md": "Start-here guide for the reviewer.",
        "REQUEST.txt": "Original user request preserved verbatim.",
        "briefing/context.md": "Curated repository and task context.",
        "briefing/reviewer_questions.md": "Concrete questions for the reviewer.",
    }
    for relative in sorted(generated):
        path = bundle / relative
        manifest_files.append(
            _manifest_entry(
                "generated",
                None,
                relative,
                generated_reasons[relative.as_posix()],
                path,
            )
        )
    for file_spec, _, destination in selected:
        relative = destination.relative_to(bundle)
        manifest_files.append(
            _manifest_entry(
                file_spec["kind"],
                file_spec["source"],
                relative,
                file_spec["reason"],
                destination,
            )
        )

    manifest = {
        "schema_version": 1,
        "title": title,
        "bundle": bundle.name,
        "repository": {
            "name": repo.name,
            "branch": branch,
            "head": head,
            "dirty": bool(status),
            "changed_paths": changed_paths,
        },
        "zip_limit_bytes": ZIP_LIMIT_BYTES,
        "files": sorted(manifest_files, key=lambda item: cast(str, item["path"])),
    }
    (bundle / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )

    with zipfile.ZipFile(
        temp_archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as output:
        for path in sorted(item for item in bundle.rglob("*") if item.is_file()):
            relative = path.relative_to(bundle.parent).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            output.writestr(info, path.read_bytes(), compresslevel=9)

    if temp_archive.stat().st_size > ZIP_LIMIT_BYTES:
        largest = sorted(
            (
                (path.stat().st_size, path.relative_to(bundle))
                for path in bundle.rglob("*")
                if path.is_file()
            ),
            reverse=True,
        )[:5]
        temp_archive.unlink()
        details = ", ".join(f"{path} ({size} bytes)" for size, path in largest)
        raise SystemExit(f"archive exceeds 25 MiB; largest files: {details}")

    temp_archive.rename(archive)
    checksum.write_text(f"{_sha256(archive)}  {archive.name}\n")
    print(f"bundle_dir={bundle}")
    print(f"archive={archive}")
    print(f"checksum={checksum}")
    print(f"selected_files={len(selected)}")
    print(f"bundle_files={len(manifest_files) + 1}")
    print(f"archive_bytes={archive.stat().st_size}")


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _relative_path(value: str, label: str) -> Path:
    assert "\\" not in value and ":" not in value, f"invalid {label}"
    assert all(ord(character) >= 32 for character in value), f"invalid {label}"
    path = Path(value)
    assert not path.is_absolute(), f"{label} must be relative"
    assert path.parts and all(part not in {"", ".", ".."} for part in path.parts), (
        f"invalid {label}"
    )
    return path


def _category_dir(kind: str) -> str:
    match kind:
        case "context":
            return "context"
        case "evidence":
            return "evidence"
        case "source":
            return "source"
        case "log":
            return "logs"
        case _:
            raise AssertionError(f"unknown file kind: {kind}")


def _require_safe_path(path: Path) -> None:
    normalized = path.as_posix()
    parts = [part.lower() for part in path.parts]
    if any(part in SENSITIVE_PARTS for part in parts) or any(
        parts[index : index + 2] == [".config", "gcloud"]
        for index in range(len(parts) - 1)
    ):
        raise SystemExit(f"refusing sensitive path: {normalized}")
    if any(pattern.search(normalized) for pattern in SENSITIVE_NAMES):
        raise SystemExit(f"refusing sensitive filename: {normalized}")


def _require_regular_repo_file(repo: Path, relative: Path, path: Path) -> None:
    _require_no_symlink_parts(repo, relative, "source")
    assert path.is_file(), f"source is not a regular file: {relative}"
    assert path.resolve().is_relative_to(repo), f"source leaves repo_root: {relative}"


def _require_no_symlink_parts(repo: Path, relative: Path, label: str) -> None:
    current = repo
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            raise SystemExit(f"refusing symlink in {label}: {relative}")


def _require_safe_text(label: str, text: str) -> None:
    _require_safe_bytes(label, text.encode())


def _require_safe_bytes(label: str, data: bytes) -> None:
    text = data.decode("utf-8", errors="ignore")
    if any(pattern.search(text) for pattern in SECRET_VALUES):
        raise SystemExit(f"refusing secret-like content: {label}")


def _readme(title: str, selected: list[tuple[FileSpec, Path, Path]]) -> str:
    categories = sorted(
        {_category_dir(file_spec["kind"]) for file_spec, _, _ in selected}
    )
    directories = "\n".join(f"- `{category}/`" for category in categories)
    return f"""# {title}

This is a curated package for an external second opinion. It is not a complete
copy of the repository.

## Start Here

1. `REQUEST.txt` — original request, preserved verbatim.
2. `briefing/context.md` — current state, relevant background, and boundaries.
3. `briefing/reviewer_questions.md` — concrete questions to answer.
4. `MANIFEST.json` — provenance, reasons, sizes, and hashes for bundled files.

## Supporting Files

{directories}

The manifest indexes every payload file except itself. `path` values are
bundle-relative. Non-null `source` values are repository-relative. Copied
Markdown keeps its original relative links; use the manifest when a link does
not resolve inside this curated layout.
"""


def _manifest_entry(
    kind: str,
    source: str | None,
    relative: Path,
    reason: str,
    path: Path,
) -> dict[str, object]:
    return {
        "kind": kind,
        "source": source,
        "path": relative.as_posix(),
        "reason": reason,
        "size": path.stat().st_size,
        "sha256": _sha256(path),
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


if __name__ == "__main__":
    main()
