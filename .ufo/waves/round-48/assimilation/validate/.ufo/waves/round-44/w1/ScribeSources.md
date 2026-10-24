# ScribeSources — round 44 report

- **Axis:** freshness.
- **Behavior:** Re-opened SOURCES.md rows S129/S130 and all cited source files on 2026-10-23. The S129 CtlDoNothing.md §Verdict quote and the companion ReviewFreeze.md §Verdict quote are in their sections' first prose paragraphs. The S130 self-assessment quote is in the first section-prose paragraph, correcting the old paragraph-2 locator. The Gate admits both methods and records the locator corrections. It records S131/S132 as append-only superseding row text, with corrected anchors and `teaches` cells opening `supersedes S129 — ` / `supersedes S130 — `.
- **Accessed sources:** `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md` rows 137–138; `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-43.md` locator erratum; `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/CtlDoNothing.md` §Verdict; `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-33/w1/ReviewFreeze.md` §Verdict and §1; `/home/vgpnk/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md` §Checking self-assessment statements at writing.

## Quote counts

The three Gate quotes, in order, and their verbatim text:

1. “The do-nothing shortcut never reaches predicate_pass=true” — `wc -w`: 6.
2. “every pinned sha256 verifies over the committed blob” — `wc -w`: 8.
3. “records a calibration error present when the statement was written” — `wc -w`: 10.

Commands and decisive outputs:

```text
mkdir -p /fast/scratch/hyaku/kake-r44/ScribeSources
(no output)
test -d /fast/scratch/hyaku/kake-r44/ScribeSources
(no output)


printf '%s\n' 'The do-nothing shortcut never reaches predicate_pass=true' | wc -w; printf '%s\n' 'every pinned sha256 verifies over the committed blob' | wc -w; printf '%s\n' 'records a calibration error present when the statement was written' | wc -w
6
8
10
```

## Touched surfaces and gates

- Wrote `corpus/lessons/round-44.md` with the Gate, exact corrected S131/S132 anchor and `teaches` cells, and the requested `## Mistakes` heading.
- Wrote `.ufo/waves/round-44/w1/ScribeSources.md` (this report).
- Created `/fast/scratch/hyaku/kake-r44/ScribeSources`; no temporary files were placed there.
- Left `corpus/SOURCES.md`, its S129/S130 rows, and all other lessons unchanged. The S131/S132 correction text is recorded in the requested lesson; no registry mutation was in this seat's allowed write scope.
- **Checks:** The three `wc -w` counts were run. `test -d /fast/scratch/hyaku/kake-r44/ScribeSources` was also issued; the tool reported no output and did not render an exit status. No build, test, or lint was run.
- **Installs:** none.
- **Out-of-scope:** no source registry edit, product-code change, or unrelated lesson edit.
- **Blocker:** none.

## Artifacts

- `corpus/lessons/round-44.md`
- `.ufo/waves/round-44/w1/ScribeSources.md`
