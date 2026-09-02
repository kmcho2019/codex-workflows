---
name: publication-figures
description: "Create or refine publication-quality figures in matplotlib or TikZ for papers, technical reports, and professional presentations. Use for learning curves, scaling laws, comparisons, Pareto fronts, matrices, method diagrams, or any chart that must be polished, accessible, and reproducible."
---

A figure in a paper is an argument, not a screenshot of an array. It makes one
claim, and a reader who skips the prose should still get that claim right.
Default matplotlib output does not clear that bar: it is sized for a screen,
titled where a caption belongs, colored from a cycle that collapses in
greyscale, and rasterized where the document wants vector.

Everything below is what separates a figure that survives review from one that
gets remade the week before the deadline.

## Non-negotiables

1. **Build at the final printed size.** A figure drawn 8 inches wide and shrunk
   to a 3.25-inch column has 3pt tick labels. Pick the width from the document
   (`COLUMN`, `TEXT`, `WIDE` in the style module), then include it with
   `width=\linewidth`, which scales by 1.0 once the size is right (see *Where
   the figure goes*). Never build big and rescale to fit. A `WIDE` figure only
   gets a 6.75-inch `\linewidth` inside a `figure*` — in a plain `figure` in a
   two-column paper it silently scales to about a half.
2. **Vector out.** Write PDF for `\includegraphics` and SVG alongside it for
   preview. A rasterized *plot* — axes, lines, text — is a defect: it blurs
   under the zoom every reviewer uses. PNG is correct only for genuinely
   raster content: a photograph, a sample image grid, an attention map at
   pixel resolution.
3. **Every number comes from recorded evidence.** Read metrics from the
   project's run outputs. Never plot a remembered, rounded, or plausible
   number, and never leave synthetic demo data in a script that ships.
4. **The caption is the title.** No `ax.set_title` on a paper figure — a title
   duplicates the caption and steals vertical space. Panel letters (**a**,
   **b**) are how you name parts of a multi-panel figure.
5. **Show the uncertainty, or say there is none.** One seed is an anecdote.
   Plot the interval across seeds and state the seed count in the caption; if
   you only have one run, say "single seed" rather than implying more.
6. **Label the axes with units.** "Loss" is a label; "step" without knowing
   whether it counts optimizer steps or tokens is not.
7. **Colorblind-safe, greyscale-safe.** Use the module's palette. Never `jet`,
   `rainbow`, or `hsv` — they invent structure that is not in the data.
8. **Sans-serif text, and the same face in every figure.** `use_style()`
   defaults to a Helvetica-metric sans, which is what Nature and Science
   require in figures and what survives the 5-8pt sizes tick labels print at.
   Figure text is its own register — it does not have to match the body font,
   but it must match across your figures, diagrams included. Pass
   `use_style(family="serif")` only for a figure carrying heavy math that
   should read as part of a serif-set page.

## Set up once per project

Vendor the style module next to the figure scripts so a figure stays
reproducible after this session ends. Copy this skill's bundled
`assets/figure_style.py` to `figs/figure_style.py`. Resolve the asset path
relative to this `SKILL.md`; do not depend on a separate source checkout.

Vendor it next to whichever destination the script lives in — a report's script
under an output directory needs its own copy there, or the import fails.

Then find an interpreter that has matplotlib, in this order — do not install
into the project's environment without asking:

```sh
python -c "import matplotlib"                      # the project env already has it
uv run --with matplotlib --with numpy python figs/loss_curve.py
```

## Optional SciencePlots style

If the project already uses
[SciencePlots](https://github.com/garrettj403/SciencePlots), or the user wants
a venue-specific matplotlib style, it is a good alternative to the bundled
style. Import `scienceplots` before selecting a style such as `science`,
`ieee`, or `nature`. Use `no-latex` when a LaTeX installation is unavailable.
Do not install it or add it to the project without the user's approval.

Choose one style source: SciencePlots or `use_style()`. Do not stack them,
because both change the same matplotlib settings. The sizing, evidence,
accessibility, uncertainty, caption, and vector-export rules in this skill
still apply. SciencePlots is described in
[Garrett (2021)](https://doi.org/10.5281/zenodo.4106649).

## Where the figure goes, and how to link it

Keep the figure in the project so its source, data, and output remain together.

| The figure is for | Write it to | Link or include it as |
| --- | --- | --- |
| A paper (`.tex`) | `figs/` beside the `.tex` | `\includegraphics{figs/loss_curve.pdf}` from the LaTeX source |
| A report, summary, or chat answer | The requested output directory, or `artifacts/` when the project has no convention | An absolute Markdown file link in the final response |

Keep the generating script beside its output, in whichever of the two
destinations you chose (`figs/loss_curve.py` → `figs/loss_curve.pdf`,
`figs/loss_curve.svg`). A figure whose script is gone
cannot be corrected when a reviewer asks for one more seed.

Build the figure at the column width, **and** still write `width=\linewidth`:

```latex
\begin{figure}[t]          % figure* for a WIDE figure in a two-column paper
  \centering
  \includegraphics[width=\linewidth]{figs/loss_curve.pdf}
  \caption{Validation loss over training, mean of 5 seeds with 95\% intervals.}
  \label{fig:loss}
\end{figure}
```

The two together are the point. Sized correctly, `width=\linewidth` scales by
1.0 and changes nothing — but it still fits if the venue's column turns out
narrower than you assumed. What it cannot do is rescue a figure built at the
wrong size: a 15-inch canvas dropped into a 5.5-inch column is scaled to 0.35,
and 11pt tick labels land at 4pt. That is the most common reason a real paper's
figures are unreadable, and `width=\linewidth` is what hides it until print.

## Write the caption with the figure

Every reference below tells you to "state it in the caption". This is what that
means, and the caption is written *with* the figure, not after the draft.

Captions in current papers run a median of about 28 words, and half are three
sentences or more. The dominant shape is a **short bold phrase naming the
claim, then the detail a reader needs to trust it**:

```latex
\caption{\textbf{LPO reaches the reward plateau in a third of the compute.}
Held-out reward against training compute for LPO and two baselines; mean of 5
seeds, bands are 95\% intervals. The dotted line is the pretrained model.}
```

- **Lead with the finding, not the setup.** "Training curves for LPO and
  baselines" names the axes, which the axes already do. The caption's first
  clause should be the thing you want remembered.
- **The figure must stand alone.** A reader who skips your Section 4 should
  still get the claim right. That is the whole job.
- **Put the method facts here**, because nowhere else in the figure has room:
  seed count, what the band or bar means, any smoothing, any normalization,
  which points were fitted and which excluded, and whether a frontier line is
  measured or a guide.
- **Say what is not shown** when it matters — a single seed, a truncated axis,
  a run cut short.
- **Do not restate the axis labels** in prose, and do not repeat the caption as
  an axes title. The title is the caption's job.

A one-panel figure earns roughly 25-40 words; a multi-panel figure earns more,
and each panel needs its own clause.

## Multi-panel figures

Roughly a quarter of figures in current ML papers are multi-panel — `(a)`/`(b)`
subpanels, or a `Left:`/`Right:` pair. Panels are a composition choice that cuts
across every figure type below, and they go wrong in consistent ways.

- **Label every panel** `(a)`, `(b)`, … at the top-left (`panel_labels()`).
  Prose refers to "Fig. 2b"; without letters the only way to name a panel is by
  position, which breaks the moment one moves.
- **Share the axis when panels share a quantity** (`sharey=True`), and let the
  shared axis carry one label on the panel that shows the ticks. Two panels of
  the same metric on silently different ranges is the multi-panel version of a
  truncated bar axis — the reader compares heights that are not comparable.
- **One legend for the figure**, not one per panel. Put it under the panels or
  outside the last one.
- **Panels read in argument order**: left to right, top to bottom. Panel (a)
  should be the one the text discusses first.
- **If the panels do not support one claim, they are separate figures.** A
  2×3 grid of unrelated plots is a contact sheet, and its caption will read as
  a list rather than a sentence.

Build them with `figure_grid(nrows, ncols, width=TEXT, sharey=True)`, which
sizes the whole grid to the final printed width.

## Read exactly one reference

Pick by the question the figure answers, not by the shape you have in mind.

| The figure answers | Read |
| --- | --- |
| How does a metric move over training, and is the gap bigger than seed noise? | [references/curves.md](references/curves.md) |
| How does performance change with scale, and what does the trend predict? | [references/scaling.md](references/scaling.md) |
| Which method wins across benchmarks, or which ablated component mattered? | [references/comparison.md](references/comparison.md) |
| What is traded off against what — reward vs KL, quality vs cost or latency? | [references/pareto.md](references/pareto.md) |
| What does this 2D grid, confusion matrix, or sweep look like? | [references/matrix.md](references/matrix.md) |
| What is the method, architecture, or pipeline? | [references/diagram.md](references/diagram.md) |

Every reference's template writes to `figs/`, which is the paper destination.
For a report or a chat answer, put both the script and its `save()` stem under
the requested output directory, or `artifacts/` when none is specified.

Do not read references for figures you are not making.

Anything genuinely outside those six — a photograph, a qualitative sample
grid, a map — still obeys the non-negotiables above and the style module.

## Before you hand it over

- **Read the audit line `save()` prints.** It checks the printed width, the
  Type 42 font embedding, stray axes titles, missing axis labels, text below
  the 5pt floor, text that overlaps other text, and text running off the
  canvas. `clean` is the bar; anything else is a defect to fix, not a warning
  to note and move past.
- One audit finding is not yours to fix: if it reports no publication font on
  the machine, say so when you hand the figure over rather than installing
  fonts, which is a change to the environment you should ask about first.
- A label placed at a reference line or a data point is the usual source of an
  overlap — it lands on a tick label at some data ranges and not others. Move
  it, or give it `backgroundcolor="white"` so it masks what it covers.
- Open the PDF and read it at printed size. If a tick label is unreadable on
  screen at 100%, it is unreadable on paper.
- Every axis labelled, with units. No stray `ax.set_title`.
- The claim in the caption is visible in the figure without the prose.
- Uncertainty shown, with n stated.
- No unexplained series, no legend entry for something that was cut.
- The script reruns from scratch and reproduces the same file.
