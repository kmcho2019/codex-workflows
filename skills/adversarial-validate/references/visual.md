# Visual Mode

Use visual mode for rendered documentation, diagrams, charts, screenshots, or
interfaces. Inspect the rendered artifact, not only its source.

## Primary Proof

- Render or open the artifact with its supported tool.
- Inspect the target sizes, pages, states, or viewports named in the contract.
- For a diagram, trace nodes, edges, labels, and direction against the actual
  implementation or data flow.
- For a chart, verify axes, units, legends, scales, samples, and source data.
- For an interface, perform the named user task and inspect the states it
  reaches.

## Role Passes

**First-time user:** Identify the first unclear entry point, label, sequence,
or action.

**Visual examiner:** Check clipping, overlap, illegible text, weak hierarchy,
broken rendering, color-only meaning, and misleading emphasis.

**Source examiner:** Check that the visual does not invent, omit, or reverse
important structure from the source of truth.

A polished visual fails when it is inaccurate. An accurate visual fails when
the intended reader cannot use it for the named task.

Use the built-in image inspection path first. Read
[external-reviewers.md](external-reviewers.md) before sending any visual to an
external model.
