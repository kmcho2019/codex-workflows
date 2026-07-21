from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from typing import Any


SCRIPT = Path(__file__).parents[1] / "scripts" / "build_review_bundle.py"


class BuildReviewBundleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self._git("init", "--quiet")
        self._git("config", "user.name", "Test User")
        self._git("config", "user.email", "test@example.com")
        self._git("config", "commit.gpgSign", "false")

        files = {
            "docs/guidance.md": "# Guidance\n\nKeep the implementation small.\n",
            "results/current.csv": "name,value\nalpha,1\n",
            "src/app.py": "def answer() -> int:\n    return 42\n",
            "logs/run.log": "validation passed\n",
        }
        for relative, text in files.items():
            path = self.repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        self._git("add", ".")
        self._git("commit", "--quiet", "-m", "Add fixtures")

        self.spec_path = self.root / "spec.json"
        self.spec: dict[str, Any] = {
            "version": 1,
            "repo_root": str(self.repo),
            "bundle_dir": "docs/topic/reviews/20260721_topic_review_bundle",
            "title": "Topic Review Bundle",
            "request": "Review this exact request.\nDo not alter it.",
            "context": "The implementation is ready for a second opinion.",
            "review_questions": "- Is the design coherent?\n- What evidence is missing?",
            "files": [
                {
                    "kind": "context",
                    "source": "docs/guidance.md",
                    "destination": "repository/guidance.md",
                    "reason": "Defines the repository's implementation expectations.",
                },
                {
                    "kind": "evidence",
                    "source": "results/current.csv",
                    "destination": "results/current.csv",
                    "reason": "Contains the current measured result.",
                },
                {
                    "kind": "source",
                    "source": "src/app.py",
                    "destination": "implementation/app.py",
                    "reason": "Implements the behavior under review.",
                },
                {
                    "kind": "log",
                    "source": "logs/run.log",
                    "destination": "validation/run.log",
                    "reason": "Records the focused validation result.",
                },
            ],
        }

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_builds_curated_reproducible_bundle(self) -> None:
        first = self._run()
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertIn("selected_files=4", first.stdout)
        self.assertIn("bundle_files=9", first.stdout)

        bundle = self.repo / self.spec["bundle_dir"]
        archive = bundle.with_suffix(".zip")
        checksum = Path(f"{archive}.sha256")
        self.assertEqual((bundle / "REQUEST.txt").read_text(), self.spec["request"])
        self.assertTrue((bundle / "context/repository/guidance.md").is_file())
        self.assertTrue((bundle / "evidence/results/current.csv").is_file())
        self.assertTrue((bundle / "source/implementation/app.py").is_file())
        self.assertTrue((bundle / "logs/validation/run.log").is_file())

        manifest = json.loads((bundle / "MANIFEST.json").read_text())
        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(len(manifest["files"]), 8)
        selected = next(
            item for item in manifest["files"] if item["source"] == "src/app.py"
        )
        self.assertEqual(selected["kind"], "source")
        self.assertEqual(selected["path"], "source/implementation/app.py")
        self.assertEqual(selected["sha256"], self._sha256(self.repo / "src/app.py"))
        self.assertNotIn(str(self.repo), (bundle / "MANIFEST.json").read_text())

        expected_checksum = checksum.read_text().split()[0]
        self.assertEqual(expected_checksum, self._sha256(archive))
        with zipfile.ZipFile(archive) as zipped:
            names = zipped.namelist()
            self.assertEqual(names, sorted(names))
            self.assertTrue(all(name.startswith(f"{bundle.name}/") for name in names))
            self.assertIn(f"{bundle.name}/MANIFEST.json", names)

        first_archive = archive.read_bytes()
        shutil.rmtree(bundle)
        archive.unlink()
        checksum.unlink()
        second = self._run()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first_archive, archive.read_bytes())

    def test_rejects_invalid_specs(self) -> None:
        cases: list[tuple[str, dict[str, Any], str]] = []

        unknown_field = copy.deepcopy(self.spec)
        unknown_field["extra"] = True
        cases.append(("unknown field", unknown_field, "spec fields must be"))

        unknown_version = copy.deepcopy(self.spec)
        unknown_version["version"] = 2
        cases.append(("unknown version", unknown_version, "unknown spec version"))

        unknown_kind = copy.deepcopy(self.spec)
        unknown_kind["files"][0]["kind"] = "document"
        cases.append(("unknown kind", unknown_kind, "unknown file kind"))

        source_traversal = copy.deepcopy(self.spec)
        source_traversal["files"][0]["source"] = "../outside.md"
        cases.append(("source traversal", source_traversal, "invalid files[0].source"))

        destination_traversal = copy.deepcopy(self.spec)
        destination_traversal["files"][0]["destination"] = "../outside.md"
        cases.append(
            (
                "destination traversal",
                destination_traversal,
                "invalid files[0].destination",
            )
        )

        portable_traversal = copy.deepcopy(self.spec)
        portable_traversal["files"][0]["destination"] = "..\\outside.md"
        cases.append(
            ("portable traversal", portable_traversal, "invalid files[0].destination")
        )

        duplicate_source = copy.deepcopy(self.spec)
        duplicate_source["files"][1]["source"] = "docs/guidance.md"
        cases.append(("duplicate source", duplicate_source, "duplicate source"))

        duplicate_destination = copy.deepcopy(self.spec)
        duplicate_destination["files"][1]["kind"] = "context"
        duplicate_destination["files"][1]["destination"] = "repository/guidance.md"
        cases.append(
            ("duplicate destination", duplicate_destination, "duplicate destination")
        )

        missing_source = copy.deepcopy(self.spec)
        missing_source["files"][0]["source"] = "docs/missing.md"
        cases.append(("missing source", missing_source, "source is not a regular file"))

        invalid_bundle_name = copy.deepcopy(self.spec)
        invalid_bundle_name["bundle_dir"] = "docs/topic/reviews/topic_bundle"
        cases.append(
            ("invalid bundle name", invalid_bundle_name, "invalid bundle name")
        )

        for name, spec, message in cases:
            with self.subTest(name=name):
                result = self._run(spec)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stderr)

    def test_rejects_sensitive_files_and_symlinks(self) -> None:
        sensitive_name = self.repo / ".env"
        sensitive_name.write_text("SAFE_PLACEHOLDER=true\n")
        named_spec = copy.deepcopy(self.spec)
        named_spec["files"][0]["source"] = ".env"
        self.assertFailure(named_spec, "refusing sensitive filename")

        secret_value = self.repo / "results/credential.txt"
        secret_value.write_text('api_key = "abcdefghijklmnopqrstuvwx"\n')
        content_spec = copy.deepcopy(self.spec)
        content_spec["files"][0]["source"] = "results/credential.txt"
        self.assertFailure(content_spec, "refusing sensitive filename")

        secret_value.rename(self.repo / "results/value.txt")
        content_spec["files"][0]["source"] = "results/value.txt"
        self.assertFailure(content_spec, "refusing secret-like content")

        link = self.repo / "docs/link.md"
        link.symlink_to(self.repo / "docs/guidance.md")
        link_spec = copy.deepcopy(self.spec)
        link_spec["files"][0]["source"] = "docs/link.md"
        self.assertFailure(link_spec, "refusing symlink")

        outside = self.root / "outside"
        outside.mkdir()
        reviews_link = self.repo / "docs/linked/reviews"
        reviews_link.parent.mkdir(parents=True)
        reviews_link.symlink_to(outside, target_is_directory=True)
        output_spec = copy.deepcopy(self.spec)
        output_spec["bundle_dir"] = "docs/linked/reviews/20260721_topic_review_bundle"
        self.assertFailure(output_spec, "refusing symlink in bundle_dir")

    def test_refuses_existing_output(self) -> None:
        result = self._run()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFailure(self.spec, "refusing to overwrite existing output")

    def test_rejects_archive_larger_than_25_mib(self) -> None:
        large = self.repo / "results/large.bin"
        large.write_bytes(os.urandom(26 * 1024 * 1024))
        spec = copy.deepcopy(self.spec)
        spec["files"] = [
            {
                "kind": "evidence",
                "source": "results/large.bin",
                "destination": "data/large.bin",
                "reason": "Exercises the archive size limit.",
            }
        ]
        result = self._run(spec)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("archive exceeds 25 MiB", result.stderr)
        bundle = self.repo / spec["bundle_dir"]
        self.assertTrue(bundle.is_dir())
        self.assertFalse(bundle.with_suffix(".zip").exists())
        self.assertFalse(Path(f"{bundle.with_suffix('.zip')}.sha256").exists())

    def assertFailure(self, spec: dict[str, Any], message: str) -> None:
        result = self._run(spec)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stderr)

    def _run(
        self, spec: dict[str, Any] | None = None
    ) -> subprocess.CompletedProcess[str]:
        self.spec_path.write_text(json.dumps(spec or self.spec))
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--spec", str(self.spec_path)],
            capture_output=True,
            text=True,
        )

    def _git(self, *args: str) -> None:
        subprocess.run(["git", "-C", str(self.repo), *args], check=True)

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    unittest.main()
