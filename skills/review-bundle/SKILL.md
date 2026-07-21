---
name: review-bundle
description: "Create a curated, shareable review bundle from a request and relevant repository files. Use when the user wants a senior or colleague's second opinion, an external brainstorming package, a review context bundle, or a ZIP containing selected docs, code, results, and logs without sharing the entire repository."
---

# Review Bundle

Prepare a small, self-contained package that lets a reviewer understand the
request quickly and inspect deeper evidence when useful.

## Workflow

1. Preserve the user's request verbatim. Do not replace it with a summary.
2. Read repository guidance and inspect the named files, current git state,
   canonical docs, implementation entry points, tests, results, and logs.
3. Choose the nearest relevant `reviews/` directory. Use a bundle name of
   `<YYYYMMDD>_<slug>_review_bundle`. Ask for a destination only when the
   relevant context root is ambiguous.
4. Curate the smallest sufficient file set:
   - prefer sources of truth over summaries of summaries;
   - include implementation, tests, and configuration that explain behavior;
   - include compact result tables and logs that support important claims;
   - follow references or imports only when they materially help the review;
   - omit caches, model weights, complete experiment trees, duplicate derived
     output, and unrelated repository files.
5. Write a concise context briefing and concrete reviewer questions. State
   important omissions and unresolved uncertainty in the briefing.
6. Build the bundle with `scripts/build_review_bundle.py`.
7. Inspect `README.md`, `MANIFEST.json`, and the archive listing. Verify the
   checksum before reporting the result.

Do not include full Codex session transcripts. Include a repository log or a
short transcript excerpt only when it is directly relevant and already lives
inside the repository. Do not upload or send the bundle.

## File Categories

Classify every selected file with exactly one kind:

- `context`: repository guidance, architecture, glossary, or background.
- `evidence`: plans, reports, tables, figures, datasets, or result artifacts.
- `source`: implementation, tests, configuration, schemas, or commands.
- `log`: compact execution or validation logs.

Give every file a short, reviewer-facing inclusion reason. Use portable,
repo-relative source paths and clear destinations within its category.

## Build Spec

Create a temporary JSON spec with exactly this shape:

```json
{
  "version": 1,
  "repo_root": "/absolute/path/to/repository",
  "bundle_dir": "docs/topic/reviews/20260721_topic_review_bundle",
  "title": "Topic Review Bundle",
  "request": "The user's exact request, including original newlines.",
  "context": "Concise Markdown briefing with current state and boundaries.",
  "review_questions": "Markdown list of concrete questions for the reviewer.",
  "files": [
    {
      "kind": "evidence",
      "source": "docs/topic/results.md",
      "destination": "current/results.md",
      "reason": "Canonical summary of the current results."
    }
  ]
}
```

All fields are required. `bundle_dir` and every `source` must be
repo-relative. `destination` is relative to the selected category directory.
List individual files; do not pass directories or globs.

Run the installed skill with:

```bash
uv run --no-project python \
  ~/.codex/skills/review-bundle/scripts/build_review_bundle.py \
  --spec /tmp/review-bundle-spec.json
```

When working from this source repository, use
`skills/review-bundle/scripts/build_review_bundle.py` instead. Keep
`--no-project`; the standard-library helper must not create a `.venv`,
`uv.lock`, or other provenance noise in the repository being packaged.

## Safety Contract

The packager refuses existing outputs, unknown fields or kinds, duplicate
files, path traversal, symlinks, files outside the repository, sensitive
filenames, secret-like content, and ZIPs larger than 25 MiB. It has no bypass
flags. If it fails, clean or narrow the selection and run it again; never
weaken the checks for convenience.

The output contains the bundle directory, a sibling `.zip`, and a sibling
`.zip.sha256`. Report all three paths, file count, archive size, notable
omissions, and any limits the reviewer should know.
