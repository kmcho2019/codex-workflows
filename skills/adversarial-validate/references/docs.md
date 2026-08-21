# Documentation Mode

Use docs mode to test accuracy, task completion, and comprehension. Apply
ASD-STE100-inspired plain technical language. Do not claim formal ASD-STE100
compliance.

## Primary Proof

- Verify commands, names, defaults, data flow, and diagrams against the current
  source and configuration.
- Give a novice one concrete task to complete using only the documented path.
- Check that the document has one clear home and does not duplicate a more
  authoritative source.

## Role Passes

**Novice task performer:** Follow the document literally. Record the first
missing prerequisite, undefined term, ambiguous step, or dead end.

**Source examiner:** Trace each technical claim and diagram edge to code,
configuration, a test, or a cited source.

**Documentation maintainer:** Check placement, duplication, update burden, and
whether new prose or diagrams replace a real gap.

## Plain-Language Checks

- Use one term for one concept. Define it before first use.
- Prefer short sentences with one main instruction or claim.
- Name the actor and action. Avoid vague words such as "it", "this", or
  "usually" when their meaning is not local and exact.
- Put prerequisites before actions and actions before expected results.
- Remove repeated summaries, decorative sections, and examples that do not
  resolve a likely question.
- Integrate needed explanations near first use. Do not add a separate FAQ when
  a local sentence fixes the gap.
- Keep a text path when a diagram is optional or may not render.

Do not expand the document merely to answer every possible beginner question.
Fix only gaps exposed by the contract and role passes.
