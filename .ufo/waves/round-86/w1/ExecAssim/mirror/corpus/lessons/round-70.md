# Round 70 — lessons (kake, attempt 1)

Base `e5f6fd9e4c243d092160bc74e8bea24256087173` (lane master at round open). Frozen contract
`.ufo/waves/round-70/contract.md` (commit `908b20b00f7479a61596e93e05104d1cd0054349`), Amendment 0
(seat shape, `d76ae92656bc24bc935d28201267a5d8b293de5a`) and Amendment 1 (term refinements after the
W1 attacks, before any after-state; `.ufo/waves/round-70/amendment-1-note.md`). Two claims: C1
calibration (2 → 2, HOLD), C2 freshness (10 → 10, HOLD). Wave shape: W1, one v1 wave of 14 seats
(4 attack seats ≈ 28.6 %), dispatched through the inline spawn handoff; no residual wave.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| M1 — reference-drift: the scorecard's own evidence pointers name scratch paths and host-tree paths that no round ever annotated | `SCORECARD.md` move-log rows 10–18 at base `e5f6fd9e` (9 distinct `/tmp/kake-rNN` tokens in 11 occurrences, 8 dangling on this host; `~/DIRMAP.md`, lowercase `~/projects`, `~/Projects/plazir-15-site`); base run `controls/c1-base-v2.txt` (dangling=17) | none — the corpus append-only rules never covered `SCORECARD.md`, and `scripts/freshness-sweep.mjs` scans SKILL.md and corpus files, never SCORECARD (ReviewerPredicates verified the scan population at lines 5 and 399–401) | the C1 counter `.ufo/waves/round-70/c70_pointer_audit.py` (v2), the `## Pointer calibration (round 70)` section of `SCORECARD.md` (17 exact-token rows), and the round-70 QUALITY criterion |
| M2 — planning overstatement frozen into the contract: a motivating-evidence count and a collision premise written from occurrence greps, not from the frozen extractor | `.ufo/waves/round-70/contract.md` §C1 ("12 tokens") and §C2 ("staged id S352 collides with the lane registry's S352"); measured: 9 distinct tokens (11 occurrences), and S352 occurs 0 times in the lane registry at base (`w1/ScoutAdoption/lane-ids.txt`, `w1/ExecMirror/collisions` — the 8 real collisions are S312, S329, S367, S372, S373, S374, S390, S409, none adopted) | none — the contract was written before the extractor ran; the §10 contract's own rule (decide by the committed extractor outputs, never arithmetic) was applied only as a citation, not as a pre-write check | Amendment 1 records both corrections; the adopted id S438 stands on the next-unused rule (first gap after the maximum S437), and the calibration rows cover what the counter enumerates, not the prose count |
| M3 — counter v1 defects caught by the wave's own attack seats before any after-state | `w1/SentinelAdoption.md` §2 (os.path.lexists vs test -e on a broken symlink; a `/tmp` literal at v1 `:188`; a home token escaping `$HOME` used as an existence oracle; a fenced code-block row credited as an annotation) and `w1/MutC1Counter.md` F7 (same fence finding) | the round-69 QUALITY criterion caught the `/tmp` literal (the sentinel ran its literal scan); the lexists, home-escape and fence findings had no standing criterion — caught by the sentinel and mutation seats | counter v2 (Amendment 1 list); selftest extended 5/5 → 8/8; the v1 base receipt is kept as history |

## Corrections

None: no recorded integer count is relabelled this round (C1 is pointer-existence calibration, not
count re-derivation; the round-69 correction rows stand unchanged).

## Gate

Candidates considered this round, with decisions:

- **Admit — the BigQuery origin-membership entry** (`corpus/knowledge/crux-bigquery-origin-membership.md`;
  registry id S438, the lane's next unused id — the staged id S352 is unused in the lane registry,
  the measured collision set of the staged file is eight other ids, none adopted; renumber map
  `S352 → S438`). PROVINCE scope: field performance / CrUX eligibility is this lane's Frontier
  ground (`PROVINCE.md` §Frontier, first entry `corpus/knowledge/field-performance-cwv.md`); the
  entry adds a publisher-side knowledge row, claims no gate, no measured property and no capability
  row, so the area stays in Frontier. QUALITY bar: the cited id resolves in this lane's own
  `corpus/SOURCES.md` at the measured revision; the locator names the section that carries the
  quote — § CrUX on BigQuery → Materialized table schema → origin_summary (the staged anchor
  "Data structures" does not occur in the retained body; corrected, pinned by the doc's printed
  "Last updated 2026-10-13 UTC"); every blockquoted span is a raw substring of the retained body at
  ≤25 words ("a list of all origins included in the dataset", 8 words, raw grep 1; "it is updated
  monthly with the latest list of origins in the dataset", 13 words, raw grep 1); the mandated
  C2(c) quote ("The origin_summary table contains a list of all origins in the CrUX dataset",
  13 words) is **collapsed-only** in the retained body (raw grep 0; present once after tag-strip +
  whitespace collapse), derived independently three times (ScoutSources, CriticAdoption,
  ScribeEntries) with the method stated — recorded here because the round-55 raw-quote discipline
  binds the entry's own blockquotes, which use the raw spans above, while the contract's C2(c)
  locator check accepts the collapsed class with the method stated. The free-tier and
  account/SQL facts are stated in the lane's prose; their full sentences are collapsed-only in the
  retained body (link-wrapped "free tier", anchor-split "Google Cloud account") and are not
  blockquoted. Normalized row: `status` mined, `opened` 2026-11-03, `recheck` cell `180d`,
  `used-by` corpus/knowledge/crux-bigquery-origin-membership.md, 13 awk fields, no literal or
  escaped pipe in any cell. Stripped recheck prose, recorded verbatim from the staged S352 row
  (cadence prefix stripped; the `\|` is the staged cell's markdown escape of the pipe; the command
  as run uses a bare pipe): `curl -fsSL 'https://developer.chrome.com/docs/crux/bigquery' | grep -F -c 'The origin_summary table contains a list of all origins in the CrUX dataset'` -> 1 (ran 2026-10-24). This round's re-derivation on the retained body: the same literal grep against the raw HTML prints 0 (exit 1) and prints 1 against the whitespace-collapsed flat text (recipe
  `.ufo/waves/round-63/quote-class/extract_text.py` at e5f6fd9e, flat sha256 `8cc3fa21…9cff`) — the staged "1" was a collapsed-text count, not a raw-substring count.
- **Reject — `crux-keyless-check.md`** (staged S303, the CrUX Vis docs row, and S304, the
  own-work unregistered-caller POST probe). Reason: its probe rows are campaign-session own-work
  observations that are not lane-held registry rows (neither S303 nor S304 is in this lane's
  `corpus/SOURCES.md` at the measured revision) and would have to be re-run as fresh probes this
  round before anything in them could be admitted — and a keyless POST to the CrUX API conflicts
  with the held entry's own policy sentence ("kake holds no key; by lane policy it makes no API
  call without an operator-provisioned one", `field-performance-cwv.md`); its Vis/eligibility
  surface overlaps the held r28 entry thematically (the lane holds no Vis source row — the
  overlap is the eligibility topic, not a held Vis statement; CriticAdoption §3 corrected the
  contract's overclaimed half). Flip: a round that re-runs both probes fresh (receipt plus
  response body) and shows a publisher-side keyless surface not derivable from the held S038/S039
  ground — or re-words the entry as a procedure claiming no eligibility ground — with its recheck
  re-bound to a string the entry body actually quotes.
- **Admit — the C1 counter v2 and the calibration section** (base red `unannotated=17` exit 1 →
  tip green; selftest 8/8; append-only conjunct against base).
- **Admit — the round-70 QUALITY criterion** (M1's uncaught class).
- **Admit — S438 row** (the adoption's one new registry row; census exit 0 before and after).
- **Reject — appending any of the eight colliding staged rows** (S312, S329, S367, S372, S373,
  S374, S390, S409): each is already adopted in the lane registry (byte-identical source cells
  for the checked pair); appending would duplicate ids (census E03). Recorded as the reason the
  whole-file guard run exits 1 while the single-row adoption path is collision-free
  (ExecMirror finding 2).
- **Reject — assimilation of the register slice**: no row of the absent-defect-register slice is
  appended; the kake r58 L0 question on adopting quarantine rows stays open and unrouted-around.

Discernment spot-check: seats in this wave are the lane's own (`LEARNING.md`: a subagent the lane
dispatched is still the lane). A lane-side sample of this round's gate decisions: 4 admits, 3
rejects, with the reasons above. The non-author spot-check is owed to the hyaku closure and is not
claimed here.

## Sourced claims

- **C2 rests on S438** (Chrome for Developers: CrUX on BigQuery,
  https://developer.chrome.com/docs/crux/bigquery, opened 2026-11-03, one GET, HTTP 200, 110,697
  bytes, sha256 `dd17ea8cb30ec89af9eb6cbb16fcb0de3d04eb33143a3aa8ac19c9da6d5db420`). Located quotes
  and classes are in the Gate block above. Source: `.ufo/waves/round-70/w1/ScoutSources/sources/S438-crux-bigquery.html`
  with `receipt.json` (url, final url, status, bytes, sha256, access date, command; the receipt's
  sha256 and byte count re-derive from the retained file — SentinelAdoption §3 re-derived both).
- **C1 rests on committed lane bytes** (SCORECARD.md at base and tip) and the round-69 spot-check's
  routed item 2 context; no new external source is needed for it.

## Frontier

- `corpus/SOURCES.md`: registry 175 → 176 (S438 appended inside `## Registry`, after S437; census
  exit 0 at base and at tip, 16 W04 warnings unchanged). No status/recheck/used-by cell of an
  existing row changed.
- `corpus/knowledge/`: one adopted entry on Frontier ground the coverage map did not hold (the
  key-free origin-membership route); `corpus/README.md` coverage map gains a row for it.
- No PROVINCE.md edit: the entry stays Frontier knowledge (no gate), so the area does not move to
  Core.

## Measurements (counting commands; receipts under `.ufo/waves/round-70/controls/`)

- C1: `python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root <lane> --revision <rev> --base <base>`.
  Base `e5f6fd9e`: `pointers=348 dangling=17 annotated=0 unannotated=17 met=false`, exit 1
  (`controls/c1-base-v2.txt`; the v1 counter's base receipt `w1/ExecC1Counter/base-run.txt`
  recorded unannotated=19 before Amendment 1's two false-positive fixes — kept as history).
- C2: at base, `test -f corpus/knowledge/crux-bigquery-origin-membership.md` fails and
  `grep -c '^| S438 ' corpus/SOURCES.md` = 0; at the tip both hold, the row parses NF=13, and
  `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` exits 0.

After-state values are in the report (measured at the round tip).

## Known residuals (named, not closed)

- The round-69 L0 question (lowercase `~/projects` corpus citations; `--offline` red on this host)
  stays open: C1 annotates SCORECARD cells only and touches no pin, corpus file or lesson line the
  sweep scans.
- SKILL.md `/tmp` procedure cites (spot-check routed item 2, lines ~95, ~356, ~359): outside both
  claims' file sets this round (RevengerTmp verdict: next round, under the round-69 QUALITY
  criterion, with the sidecar re-pin census).
- Counter residuals named by the attack seats, frozen as-is this round: a fully self-consistent
  fabricated retained body would pass C2(c) (the non-author closure may re-fetch); the census has
  no escaped-pipe awareness (a crafted one-cell-short row with `\|` renders shifted columns in GFM
  while the census exits 0 — SentinelAdoption A2; fleet script, operator-owned); the lane's
  corpus-contract gate does not screen knowledge files for HTML/script payloads (SentinelAdoption
  A5 — lane-ownable repair routed to a later round).
- `/tmp/kake-r16` exists on this host (a sweep-selftest fixture directory created 2026-11-03T18:50Z,
  before this round's dispatch): it resolves, so it is not in the dangling set; its status flips
  with selftest runs, so measurement order matters (RevengerTmp divergence 2).
- MutC1Counter F7 (fenced annotation credited) is fixed in counter v2's locus rule; the v1
  artifact's receipts are history.
