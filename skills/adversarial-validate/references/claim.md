# Claim Mode

Use claim mode to test a factual, performance, completion, or paper-fidelity
claim.

## Primary Proof

- Split the claim into atomic statements.
- Record the exact revision, configuration, dataset, environment, and command
  needed for each statement.
- Prefer raw results and reproducible commands over summaries and copied
  tables.
- Compare like with like. Separate current results, best historical results,
  baselines, and external reference results.

Classify each statement as:

- verified: Primary evidence proves it.
- contradicted: Primary evidence disproves it.
- unverified: The required evidence is absent or cannot be reproduced.

For paper reproduction, classify each method element as:

- exact: The implementation follows the stated method.
- adapted: The implementation intentionally changes the method.
- divergent: The implementation conflicts with the method or its assumptions.
- missing: The implementation does not contain the element.

## Role Passes

**Reproducer:** Run or reconstruct the shortest proof without using the
implementer's conclusion.

**Skeptic:** Search for mismatched revisions, datasets, metrics, hidden
selection, and claims based on best-ever rather than current reproducible
results.

**Scope examiner:** Check whether the evidence proves the full claim or only a
narrower statement.

State uncertainty directly. Do not convert absent evidence into a negative
claim.
