# CriticJunkC2v2

Second attack on C2 after the version-2 fixes. Attack surface: `.ufo/waves/round-56/c56_quote_truth.py` at the tip
(`7ad7db51dfcf`; the wave's attack revision `a450e43e696d` is its parent), contract §Counter versions, `w1/CritCheatC2.md`.

Method. One disposable clone at the tip: `D=$(mktemp -d)/clone`, `git clone -q --no-checkout <lane>`, `git checkout -q 7ad7db51dfcf`,
toplevel asserted equal to `$D`; every variant is one commit `git -C $D -c user.name=selftest -c user.email=selftest@local commit`
on top of the tip, so no lane path, lane index or jj state was touched. Counters run as
`python3 -B <counter> --root $D --revision <rev> --json`. v2 = the tip blob; v1 = `git show 2d308e808bfd:.ufo/waves/round-56/c56_quote_truth.py`
(the frozen v1). `diff` of `run_checks` v1 vs v2 is 40 changed lines (6 removed, 34 added), all inside C1, C2, C3 and C5;
**C4, C6, C7 and C8 are byte-identical**. The tip commit adds only W2 dispatch files (`git diff --name-only a450e43 7ad7db5`
over the counter, `sources/`, `corpus/knowledge`, `corpus/SOURCES.md`, `corpus/lessons/round-56.md` is empty), so the tip and
`a450e43e696d` carry the same evidence.
Control: tip tree = 8/8 exit 0 under v2, 7/8 under v1 (v1's S367 title clause, as `w1/CriticC2Contract.md` WR-1 says).
The variant revisions below exist only in `$D`; they are not reachable from the lane.

## JUNK TREE RESULT:

| variant | rev | construction | v1 | v2 |
|---|---|---|---|---|
| control | `7ad7db51dfcf` | the real build | 7/8 | **8/8** exit 0 |
| **V0j** | `b761c17804fd` | faithful replay of W1's cheat A: 3 synthetic bodies (1,107 B each), 3 placeholder entries (210 B), 3 rewritten Gate lines, junk scope/teaches cells, receipts self-signed over the junk bodies, mirror inherited and the census receipt inherited rather than retyped (C7 passes either way, per w1) | **8/8** exit 0 | **7/8** exit 1 |
| **V1** | `f976f89beea7` | the same junk for S419/S420 only; S367's body, entry, Gate line, receipt and row, and the whole registry, inherited untouched | 7/8 | **8/8** exit 0 |
| V1j | `dff216e567d9` | V1 + junk `scope`/`teaches` cells on S419/S420 | 7/8 | **8/8** |
| **V2_min** | `39cc76b3d7f4` | 2 synthetic bodies + `receipts.json`; **entries, rows, Gate lines, validate block, mirror all inherited real** | 7/8 | **8/8** exit 0 |
| P_comment | `de97869d6e69` | the full junk tree (V0) with every quoted span inside `<!-- nav: … -->` inside the window | 8/8 | 7/8 (sha only) |
| P_staged_alias | `26577c33c15e` | V1 + `corpus/knowledge/yahoo-japan-soft404-recrawl.md` (staged candidate, other filename) | 7/8 | **8/8** |

**Does W1's junk tree still reach 8/8? No — 7/8, and the sole failing note is the held-body pin.** V0j is that tree rebuilt
from `w1/CritCheatC2.md`'s file list and construction (the original clone is gone):
`S367: held-row retained body sha256 f126bc3d… != pinned 0188de9d…` — C5 only, every other condition passes. Quote truth is
still not support: the same construction reaches 8/8 the moment the one pinned file is inherited (V1), and 3 authored files
suffice (V2_min).

Per condition, V1 and V2_min (identical results): C1 pass (`entries: 3`), C2 pass, C3 pass (`rows: 158, base_rows: 156`),
C4 pass, C5 pass, C6 pass (`receipts: 6`), C7 pass, C8 pass (`registry_rows: 158`); exit 0, `met: true`.

**Minimal junk tree (V2_min) — 3 edits, 0 authored spans.** Files: `sources/S419.html` (1,220 B), `sources/S420.html` (1,107 B),
`sources/receipts.json` (two `sha256`/`bytes` fields recomputed). Zero knowledge-entry lines, zero registry lines, zero Gate
lines, zero validate lines authored. The synthetic page is *generated from the entry's own double-quoted spans*: extract
`"…"` from `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` (15 spans) and `…-nonexistent-url-recrawl.md` (12 spans),
emit each once between `<h2>` and `個別リンクURL`, add `value="<row url>"` and ~1,100 B of filler. No page is read; the
body is derived from the claim it is supposed to support, so C5's substring test is circular by construction. It passes
C5's title, anchor, URL-field, 1,000-byte floor, content-window, 25-unit, 40-character and page-uniqueness checks because
all of those are properties the builder sets.

**Cheapest entry-based tree (V1) — 8 edits, 6 arbitrary spans.** `sources/S419.html`, `sources/S420.html` (1,107 B each),
the two entries (210 B each: 3 header lines, one `# junk` heading, three quoted spans, `[S419]`), the two `validate/`
entry copies, `receipts.json`, and two Gate lines in `corpus/lessons/round-56.md`. Arbitrary spans: `ゔゔゔゔゔゔ`,
`ぴぴぴぴぴぴぴ`, `ぺゃぺゃぺゃぺゃ` (S419) and `ゞゞゞゞゞゞ`, `ぼゃぼゃぼゃぼゃ`, `ぢぢぢぢぢぢぢ` (S420) — 6 to 8 units each, no meaning,
each the only occurrence in its body, each absent from the other five retained bodies; the Gate lines reuse span 1. The
entries assert nothing (`c56_quote_truth.py` never reads a claim), and the junk `scope`/`teaches` cells of V1j ("JUNK scope
cell authored by the seat…") pass the ≥20-character test at `:301`.

## WHAT VERSION 2 ADDED:

Each rule below is measured twice: on the full-junk base (V0/V0j, identical for these variants; v1 prints 8/8, so a v2
failure proves the rule is new) and on the V1 base (where v2 prints 8/8, so the variant's note is isolated). The `v2` column
is the full-junk run, where the S367 sha note is always present as a baseline — 7/8 there means sha + this rule, 6/8 means
sha + a whole condition; the V1-base rerun of each variant prints 7/8, with the quoted note (the `otherbody` variant also
drops one unique span, inside the same condition).

| v2 rule (line) | variant | v1 | v2 | note produced |
|---|---|---|---|---|
| held-body sha pin `:95`, `:346` | V0j `b761c178` | **8/8** | 7/8 | `S367: held-row retained body sha256 … != pinned …` |
| 40-character ceiling `:90` | `34212c8c` (13-unit, 42-char span) | 8/8 | 7/8 | `S419: entry line 9 quotes 42 characters, character ceiling 40` |
| one-token 12+ char substring `:415` | `28afffb6` (`"zzzzzzzzzzzz"`) | 8/8 | 7/8 | `… quotes 'zzzzzzzzzzzz'… which is not a raw substring` |
| Gate quote `count != 1` even inside the block `:401` | `60a95794` (gate span twice in the window) | 8/8 | 7/8 | `a Gate quote occurs more than once in its own body` |
| page-uniqueness against **every** retained body `:356-370` | `ac3042f3` (gate span also in S387) | 8/8 | 7/8 | `… also in another retained body` |
| `verified-at` must carry the round date `:271` | `b6b0bc26` | 8/8 | 6/8 (C2 ×3 + sha) | `verified-at: line does not carry the round date` |
| `recheck` must open NNd/ISO/on-release | `472a1e7e` | 8/8 | 6/8 | `recheck: line does not open with NNd, an ISO date or on-release` |
| staged candidate name absent `:91` | `ec1c7a92` | 8/8 | 6/8 | `staged candidate name … survives` |
| kind/tier enums, `scope`/`teaches` ≥ 20 chars `:301` | `12b2e401`, `784b971b` | 8/8 | 6/8 | `kind 'junk' … outside the census enums` / `scope or teaches cell is shorter than 20 characters` |
| (v1 rule, unchanged) held row cells vs base | `06da6b3d` | 6/8 | 5/8 | `S367: a cell other than used-by differs from the base row` |

Every rule above is real: on the V1 base each variant drops 8/8 → 7/8 with exactly the quoted note. But the additions are
narrow. **Nothing was added to C6, C7 or C8** (byte-identical code): a receipt is still self-signed over whatever body ships
(V2_min's receipts hash the synthetic pages), the census receipt is still typed, and C8 still takes the *oldest*
`--diff-filter=A` add (`:555`), i.e. the inherited contract commit. Two additions are evadable by name or by unit:
the staged rule hardcodes two filenames (`P_staged_alias` passes 8/8 with a third name), and because CJK punctuation costs
0 units, the 40-character ceiling still permits 28 of 40 characters to be punctuation around 12 semantic characters.

**The pin is a tool constant, not pinned evidence.** `HELD_BODY_SHA256` lives in the executed file, and `contract.json` pins
no counter blob: `claims.C2` carries only the predicate, the command string, the base control and the kill rule. A one-line
edit to a copy of the counter
(`… "S367": "<V0j junk sha>"`) makes V0j print **8/8 exit 0** and the real tip print 7/8; `diff` is 11 lines. The counter
reads all evidence at `--revision` but executes the file at the lane's working-copy path, so the sha pin protects the held
body only while the tool is unmodified and unverified. This is not hypothetical: during this seat's run the lane working
copy carried uncommitted edits to `.ufo/waves/round-56/c56_selftally.py` (C1) and the three knowledge entries, not made by
this seat; a counter invoked by its documented path executes whatever is in the working tree, not the measured revision's blob.

## WHAT THE COUNTER CANNOT SEE:

- **Support and relevance.** C5 is substring truth. V1's six spans are meaningless kana inside entries that assert nothing;
  V2_min's page is generated from the entry's own quotes. No condition relates a span to the row's `scope`/`teaches` cell,
  to the entry's prose, or to the page's subject. `junk description cell`-class strings pass `:301` (V1j).
- **Body provenance.** C6's sha256 is self-signed: a 1,107-byte synthetic document passes exactly as the 8,051-byte page does.
  No fetch, no response headers, no cross-check of body bytes against the row URL beyond string equality of two typed fields
  (`:446`). V2_min ships two fabricated pages with a receipt that hashes them.
- **Rendering.** `content_window` is a byte-offset pair (`:165`). `P_comment` puts all spans inside `<!-- nav: … -->` in the
  window and still passes; script/style/attribute placement follows from the same test (not run this wave).
- **Title and heading identity.** For the new rows both sides are authored by the same seat: the row's title and `§` anchor
  are typed cells, and the body must merely contain them. V2_min types them into its synthetic `<h2>`. Only S367 has an
  external anchor (the sha).
- **C7.** Still a receipt check. `sources-census.sh` does not read `sources/` at all — `grep -n 'sources/\|receipts\|sha256'
  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh` returns nothing — so an *honest* census receipt coexists with
  fabricated bodies (V2_min inherits the real one).
- **C8.** Unchanged and inherited: the mirror and its pin come from the contract commit; the append-ordering question
  (`w1/CritCheatC2.md` variant C) is still answered by the oldest add.
- **The staged-name rule.** Two hardcoded paths; any other filename passes (`P_staged_alias`, 8/8).
- **Novelty and count.** No condition reads the entries' prose, so "three arbitrary spans" is not distinguishable from three
  fragments of one sentence, nor a real page's sentence from a fabricated one.
- **The counter's own integrity.** See the pin-move experiment above; nothing in C1..C8 compares the executed counter to a
  pinned blob.

Impacted axes: C2 predicate integrity (8/8 reachable with 3 authored files and no page read), C5 quote truth (substring, not
support), C6/C7 provenance (self-signed / typed), and the counter's own provenance (unpinned tool). Axes not touched:
calibration (C1), the registry row count (158 verified at every variant), the mirror bytes.

Smallest safe corrections: (1) pin all three retained bodies' sha256 in `contract.json` before data, as S367's is now, and
require each body to be added by a commit that precedes the entry that quotes it — closes V2_min and V1 in one rule;
(2) pin the counter blob itself (sha256 in `contract.json`, verified by the runner, or run it from `git show <rev>:…`) so
the pin constant cannot be moved; (3) strip `<!-- -->`, `<script>`, `<style>` and attribute values before the C5 window test;
(4) derive the staged names from `assimilation/staged-ids`/the renumber map instead of two literals; (5) have C7 run
`sources-census.sh --file` on the measured tree, and add a body-level arm to the census, since it currently never opens
`sources/`.

VERDICT: W1's junk tree no longer reaches 8/8 (7/8, sole note the S367 sha pin), but the pin protects one file only — a 3-file tree (two synthetic bodies generated from the entries' own quotes plus a self-signed receipts file) reaches 8/8 with zero authored prose, and every v2 addition except the pin is a name-, unit- or substring-shaped check that the counter itself cannot see support, provenance or rendering through.
