# Round 76 — Amendment 3 (terms-only, recorded before any after-state)

Motivation: `w1/ReviewerC1.md` executed counterexamples against the frozen v1 counter and found four
fidelity gaps (correction rows unchecked; correction closure by fragment; single-letter assignment tokens
dropped; a commit-existence exception the frozen text does not grant) and three population gaps (duplicate
rows from overlapping heading levels; `*.ready*` admitted as a receipt; whitespace normalization hiding a
historical-line rewrite). This amendment decides each point in terms and binds the delivered counter. No
target, exit code or finding-id vocabulary changes.

## B1 — revision citations vs digests
A 7–40 character lowercase hex token is a **revision citation**: it is satisfied by resolving as a commit
object at the measured revision (`git cat-file -e <token>^{commit}`); ancestry is not required for a
citation. A 64-character lowercase hex token is a **digest** and must be contiguous in a receipt. A 41–63
character lowercase hex token is treated as a digest. This supersedes the v1 counter's unannounced
exception and makes it contractual.

## B2 — section identity and no duplicate rows
A SCORECARD section is a heading of **exactly level two** whose title matches `^Round[ -]?<N>\b`; a
QUALITY section is a level-two heading matching `^Round[- ]?<N>\b`; a lesson's rows are drawn from
level-two `## Mistakes`, `## Gate`, `## Claims` and `## Corrections`. A physical row is counted **once**
even when two accepted sections overlap; duplicate findings from one physical row are a counter defect.
A table row indented by 0–3 leading spaces is a table row (the `CORPUS.md` census parser precedent);
4 or more spaces is code and is not scanned.

## B3 — correction rows are checked too
A correction row's claim-bearing spans are subject to the same rules as any claim row. A correction closes
a defective span only when it (a) names that span, (b) quotes a **whole receipt line** — exact equality
with a receipt line after trimming leading and trailing whitespace — and (c) carries no fabricated
claim-bearing span of its own (a fabricated span on a correction line is `T1`). A quote that is only a
fragment of a receipt line cannot close a defect.

**B3-bis (naming vs claiming).** On a validated correction row, a claim-bearing span that is not a whole
receipt line is exempt only when the identical span is a `T1`/`T2` finding at the `--base` revision — that
is what "names the defective span" means mechanically. Any other claim-bearing span on the row is a claim
and must itself be a whole receipt line (or a receipt-contiguous span), else `T1`.

## B4 — append-only compares exact text
`append_only` compares each base row's exact text (no whitespace collapsing) with the rows at the measured
revision. A whitespace-only rewrite of a base row is `A1`, like a deletion: kill rule (3) forbids rewriting
a historical line.

## B5 — ready artifacts are never receipts
Any file whose name matches `*.ready*` (the wave handoff family, including `probe.ready.txt`) is never a
receipt, in addition to `*-results.json`, `*-dispatch.json`, `*-spec.json` and `swarm-registry.json`.

## B6 — the re-measured before-state
Under B1–B5 the same population at `a0491fcd` yields **`findings=7`**: the v1's eight included one
duplicate physical row (`SCORECARD.md:4904`, counted under two overlapping headings) and counted two
revision citations (`6c10b433`, `ca1a2982` at `corpus/lessons/round-75.md:102`) as spans. The seven are:
`SCORECARD.md:4892` ×2, `4893` ×2, `4904` ×1, `corpus/QUALITY.md:1499` ×1, `corpus/lessons/round-75.md:82`
×1. The re-measured receipt is `controls/base-c1-quote-truth-v2.txt`; the v1 receipt stays committed as
history. The C1 target is unchanged: `findings=0 append_only=true met=true`, exit 0, over the same
population, closed by whole-line correction rows.
