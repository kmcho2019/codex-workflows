# External Reviewers

External review is optional. It transmits the selected prompt and artifacts to
another service. Use it only when the user explicitly requests or approves the
exact reviewer and file scope.

## Selection

- For a code diff, prefer the installed autoreview skill. It already supports
  structured Codex, Claude, and Pi reviews with repository isolation.
- Use direct Claude or Pi review for non-code artifacts only when a curated
  bundle is more useful than the local role passes.
- Treat Agy visual review as experimental until a harmless fixture proves the
  installed version's image input and isolation behavior.

## Isolation

1. Check that the requested CLI exists and inspect its current help.
2. Create a neutral temporary directory.
3. Copy only the selected artifacts and a short contract into it.
4. Exclude secrets, credentials, private logs, personal data, and broad
   repository context.
5. Disable writes, project instructions, plugins, skills, MCP servers, and
   session persistence where the CLI supports those controls.
6. Require structured findings with evidence and one verdict.
7. Delete or retain the temporary bundle according to the user's request.

Do not invent flags. Use the installed CLI help as the source of truth.

## Reviewer Tasks

Give each reviewer one role and one task. Examples include novice task
completion, source accuracy, change minimization, or visual legibility. Do not
run a panel of identical generic reviews.

Treat all output as advisory. Verify each finding locally before reporting or
fixing it. Stop after one external pass unless new evidence justifies a second
pass.
