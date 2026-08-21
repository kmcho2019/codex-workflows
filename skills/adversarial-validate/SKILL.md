---
name: adversarial-validate
description: "Test code, docs, claims, or visuals against an explicit acceptance contract using primary evidence and task-based adversarial passes. Use for adversarial validation, completion proof, anti-bloat review, novice comprehension tests, evidence checks, or visual accuracy checks. Do not use for ordinary code review or open-ended rewriting."
---

# Adversarial Validate

Validate one artifact kind at a time:

- code: Read [references/code.md](references/code.md).
- docs: Read [references/docs.md](references/docs.md).
- claim: Read [references/claim.md](references/claim.md).
- visual: Read [references/visual.md](references/visual.md).

If a request contains more than one kind, validate each kind separately. Do
not create a mixed mode.

## Contract

Derive a short acceptance contract from the user's request, applicable
AGENTS.md or GUIDELINES.md, and named plans or specifications. State:

- the outcome to prove;
- the exact artifact and revision;
- the allowed scope;
- the primary evidence and commands;
- what must not regress.

Resolve facts from the repository. Ask the user only when a missing decision
would materially change the contract.

For a dirty git checkout, identify the revision as `HEAD` plus the changed
paths. For a non-versioned artifact, record its path and observation time.

## Workflow

1. Freeze the contract before reviewing.
2. Inspect primary evidence. Do not trust an implementer summary as proof.
3. Run the direct task or command that best tests the outcome.
   If it would mutate outside the allowed scope, run the closest read-only
   proof and name the untested runtime risk.
4. Run distinct role passes from the selected mode reference. Do not ask
   several reviewers the same broad question.
5. Verify every finding against the artifact and adjacent source.
6. Reject speculative risks and fixes that add more complexity than they
   remove.
7. If fixes are requested, apply only accepted in-scope findings. Rerun the
   affected proof and this validation.

Use role-play yourself by default. Use a subagent only when the user requested
delegation and an independent pass adds useful evidence. Read
[references/external-reviewers.md](references/external-reviewers.md) only when
the user requests an external model or a multimodal second opinion.

Stop after two correction cycles that do not converge. Report the contract or
scope decision that prevents progress instead of adding more patches.

## Findings

A finding must include:

- the failed contract item;
- exact evidence;
- user or maintainer impact;
- the smallest sufficient correction.

Do not report a preference as a finding unless it violates an explicit local
rule or creates a concrete cost.

End each mode report with exactly one verdict:

- PASS: All contract items have reproducible evidence.
- FAIL: At least one contract item has a correctable gap.
- BLOCKED: Required evidence cannot be obtained within the allowed scope.

Keep the final report short. List evidence first, then accepted findings,
residual risk, and the verdict.
