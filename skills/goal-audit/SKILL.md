---
name: goal-audit
description: "Audit an active goal or research branch against its plan, todo, git history, results, and reproducible evidence. Use for current status, remaining work, trajectory, stalled-progress, completion, or next-priority questions. Do not use to create a goal scaffold or implement unspecified fixes."
---

# Goal Audit

Perform a read-only audit unless the user also asks for implementation.

## Establish The Contract

Find the active goal from the user's request, goal_template.md, plans, todo
files, handoffs, or linked specifications. Resolve the current goal from links,
revision history, and repository state before asking the user.

Record:

- target outcome and acceptance gates;
- target branch or revision;
- goal start or baseline revision;
- allowed repositories, data, and tools;
- stated constraints and stop conditions.

When documents disagree, use the newest explicitly adopted contract. Report
the conflict when no source establishes precedence.

## Gather Evidence

Inspect evidence in this order:

1. Goal contract and living todo.
2. Current git status, branch, diff, and history since the baseline.
3. Tests, benchmarks, reports, and generated artifacts.
4. Implementation and user-facing documentation.
5. Handoffs and journals for context, not proof.

Use primary evidence. A commit count, long journal, or completed checkbox does
not prove an outcome.

Run the narrowest read-only command that resolves an important uncertainty.
Do not rerun expensive benchmarks when existing current evidence is sufficient.

## Requirement Ledger

List every contract item once and classify it as:

- proven: Current reproducible evidence satisfies the item.
- partial: Some required behavior or evidence is missing.
- missing: No implementation or valid evidence satisfies the item.
- blocked: A named unavailable dependency prevents proof or completion.
- superseded: A newer adopted contract replaced the item.

Do not add an unknown state. Missing evidence is missing or blocked. Record the
evidence path, command, result, and revision for each proven item. For a dirty
git checkout, use `HEAD` plus the changed paths. For non-versioned evidence,
record its source and observation time.

## Quantitative Claims

Separate these values:

- baseline;
- target;
- current reproducible result;
- best historical result;
- external reference result.

Include the configuration, dataset, metric definition, and runtime basis.
Never compare values from incompatible conditions without labeling the
difference.

## Trajectory

Return exactly one status:

- COMPLETE: Every active item is proven.
- ON_TRACK: Evidence is improving and the next gap has a defensible path.
- AT_RISK: Work is active, but evidence is flat, scope is drifting, or the same
  failed approach is repeating.
- BLOCKED: A named dependency prevents meaningful progress within scope.

Distinguish activity from progress. Identify stale claims, repeated loops,
unfinished delegated work, and infrastructure work that has not improved a
goal-facing result.

## Report

Report, in order:

1. One trajectory label and the evidence revision.
2. Compact requirement ledger.
3. Metric table when the goal is quantitative.
4. Evidence for the trajectory label.
5. One immediate next action with the highest goal-facing value.
6. The next milestone only when it helps explain that action.

Do not create a new plan during the audit. Recommend retrenchment or a new goal
only when the evidence shows the current contract is exhausted or incoherent.
