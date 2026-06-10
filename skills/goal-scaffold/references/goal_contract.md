# Goal Contract Reference

## Good Goal Shape

A strong `/goal` is a compact operating contract:

```text
/goal <desired end state>, verified by <specific evidence>, while preserving
<constraints>. Use <allowed inputs/tools/boundaries>. Between iterations,
<how to choose the next action and what to record>. If blocked, <when to stop
and what to report>.
```

Use goals for tasks with a clear finish line and uncertain path: performance
optimization, flaky test investigation, migrations, bug hunts, benchmark-driven
tuning, research reproduction, multi-step refactors, or any effort that needs a
final evidence-backed artifact.

Use a normal prompt for one-off edits.

## Planning File Roles

- Plan: durable contract and full feature spec.
- TODO: bounded living checklist for progress and completion gates.
- History: unbounded journal and audit trail.
- Goal template: short copy/paste launch prompt.
- Adversarial prompt: independent validation contract.
- Subagent report: validation output written after implementation.

## Adversarial PASS Standard

PASS means the implementation satisfies the original intent and its evidence is
defensible. It is not enough to hit a number if the implementation changed the
problem, filtered hard cases, weakened tests, skipped relevant baselines, or
claimed more than the evidence supports.

FAIL should include:

- failed or missing gates;
- commands not run;
- unverifiable claims;
- reward-hacking risks;
- code organization or maintainability issues;
- missing docs/tests;
- exact next steps that would make the claim pass.
