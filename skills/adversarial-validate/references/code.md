# Code Mode

Use code mode to test whether an implementation meets its contract without
unnecessary state or structure. Use autoreview instead when the request is
only an ordinary diff review.

## Primary Proof

- Inspect the target diff and the owning code path.
- Run the narrowest tests, type checks, benchmarks, or reproductions that prove
  the requested behavior.
- Compare the implementation with the named plan, API, schema, or paper when
  one defines the contract.
- Measure changed files and non-test code only as scope signals. A line count is
  not a quality verdict.

## Role Passes

**Contract examiner:** Trace every required behavior from input to observable
output. Find missing cases and behavior that exists only in comments or tests.

**Change minimizer:** Challenge each new argument, state, abstraction, helper,
override, fallback, and compatibility branch. Require a current caller or
supported contract that needs it.

**Maintainer:** Follow the main path without prior context. Check names,
ownership boundaries, exhaustive typed states, and whether tests explain the
contract.

## Anti-Bloat Checks

- Prefer one explicit state model. Use discriminated states and exhaustive
  handling when values have multiple forms.
- Required values must not become optional for convenience.
- A fallback must serve a supported failure mode. Do not preserve speculative
  compatibility.
- Required loaded data should fail at its boundary instead of spreading
  defaults or recovery branches.
- Keep an abstraction only when it removes real duplication or state.
- Reject one-use wrappers, indirection, configuration, and extension points
  without a current need.
- Do not delete compatibility or validation that an explicit contract still
  requires.

A simpler alternative is useful only when it preserves the accepted behavior
and its proof.
