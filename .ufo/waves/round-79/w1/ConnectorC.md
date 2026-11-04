# ConnectorC — cross-lane overlap scan (round 79, w1)

**Verdict:** no sibling lane holds either surface. `X-Robots-Tag` header ground is exclusively kake's and every sibling hit is recorded response *data*, never an instrument; no lane in the fleet has a receipt-rewrite disclosure gate (the `fromBlob`/`toBlob` event model exists only in kake). One real defect found: kake's own coverage map and PROVINCE both attribute the `X-Robots-Tag` channel to `scripts/header_audit.py`, which parses no robots directive — C2 must **rewrite** those two exclusion sentences, not merely append a row. Two reusable patterns named below (kama's ledger-introduction cutoff; kumitate's fail-closed receipt checks).

Scan ran read-only over all 21 sibling lanes; no writes outside this file, no scratch tree created, no git mutation. Commands were `grep -r`, `ls`, `sed -n`, `git cat-file -e`, `git ls-tree`; nothing was executed from another lane.

## (a) `X-Robots-Tag` ground per lane

| path:line | lane | what it holds | verdict |
|---|---|---|---|
| `kake-shokunin/corpus/SOURCES.md:196` (S449) | kake | S449 names the header spec but the entry scopes it out | `overlap` — kake already owns it; S452 is free (kake registry ends S450 `:197`, S451 `:198`; `grep -n S452 corpus/SOURCES.md` → no row) |
| `kake-shokunin/corpus/knowledge/meta-robots-directives.md:123` | kake | "No `X-Robots-Tag` response headers" — S449 entry's own exclusion | `overlap` — the exclusion C2 lifts; ScribeKnowledge must re-read this line |
| `kake-shokunin/corpus/README.md:558-559` | kake | "Ground it does not hold: `X-Robots-Tag` response headers (the `response_snapshot.py` / `header_audit.py` instruments own that channel)" | `overlap` **and a defect** — see "Coverage-map correction" below |
| `kake-shokunin/PROVINCE.md:580-581` | kake | same sentence, "**What it refuses.**" | `overlap` **and a defect** — same |
| `kake-shokunin/PROVINCE.md:419` | kake | S367 held row: `X-Robots-Tag: NOFOLLOW` quoted as vendor sentence | `overlap` — prior knowledge mention, no instrument; C2 is the first instrument |
| `tabi-shokunin/corpus/adjacency-screen.tsv:35` | tabi | screens kake `PROVINCE.md:412` (meta-robots/`X-Robots-Tag` publisher declaration): "no — tabi's committed robots discipline is robots.txt-only … there is no tabi side to cite" | `none` (already split-cleared) — tabi screened this surface in round 33 and declared no claim |
| `tabi-shokunin/.ufo/waves/round-33/w2/CritScreenCrawlerSplit.md:106` | tabi | same verdict, prose form | `none` |
| `chousa-shokunin/.ufo/waves/round-29/falsify/CriticHeadOmission/S006.response.json:24` (and `S007:36`, `sweep.json:439,543`, `DiffToolB/*.network.json`) | chousa | recorded `["x-robots-tag","nofollow"]` field-lines inside round-29 head-omission falsification receipts | `none` — response data, no instrument. **Reusable input lead** (below) |
| `kumitate-shokunin/.ufo/waves/round-68/build/K68ScoutS211/captures/transports-2025-11-25.md:42` | kumitate | `x-robots-tag: noindex` in a transport capture transcript | `none` — data |
| `kotoba-shokunin/.ufo/waves/round-63/w1/ExecSourceProbe.md:28,109` | kotoba | `x-robots-tag: noindex` in a source-probe note | `none` — data |
| `souji-shokunin/.../scan-receipts.json:489` | souji | a grep receipt quoting kake's own PROVINCE text | `none` — transcription of kake, not a claim |

Only `kake-shokunin/PROVINCE.md` and `kake-shokunin/corpus/README.md` mention the header among all 21 lanes' PROVINCE/coverage files (`grep -ln -i 'x-robots-tag' */PROVINCE.md` → kake only; same for `*/corpus/README.md`). No sibling lane needs a citation or a deferral for C2.

**Reusable input lead (not an amendment):** chousa's twelve round-29 `CriticHeadOmission` receipts carry real recorded `x-robots-tag` field-lines (`S006.response.json:24` = `nofollow`, `S007.response.json:36`, plus `sweep.json:439,543`). C2's frozen real-run is pinned to the 12 round-61 `capture/*/response.json` surfaces, so this is a stated-limit note for a later round, not something to fold in now.

## (b) Receipt-rewrite / disclosure-ledger gates

| path:line | lane | predicate shape | verdict |
|---|---|---|---|
| `kake-shokunin/.ufo/waves/round-58/receipt-rewrites.json:1` (`schema: kake-r58-receipt-rewrites-v1`), events carry `path, commit, status, fromBlob, toBlob, kind, note` | kake | per-event blob pair vs a disclosure ledger | `overlap` (kake's own; C1) — `fromBlob`/`toBlob` occurs **255 times in kake and zero times in any sibling lane** (`grep -rln fromBlob */scripts/ */tools/` → no sibling) |
| `kake-shokunin/.ufo/waves/round-79/c79_receipt_ledger.py:18` | kake | `met <=> undisclosed==0 AND phantom==0 AND malformed==0 AND wrong_kind==0 AND unpointed==0 AND symlinks==0 AND round_rewritten==0` | `overlap` (the claim's own counter) |
| `kama-shokunin/tools/append-only-audit.py:22-26` + `kama-shokunin/registry/append-only-disclosures.tsv` | kama | `a ledger read from <to> may only disclose commits that precede its own introduction (the first commit adding the ledger path): a deletion made once the ledger existed is restored by append, never disclosed` | **`reusable`** — the ledger-introduction cutoff. See below |
| `kama-shokunin/corpus/knowledge/append-only-accepted-history.md:1-30` | kama | documents `disclosed` / `undisclosed` / `bad_declarations` outcome split (`events=223 restored=87 disclosed=5 unrestored=53 ungraded=78`) | `reusable` — the vocabulary pattern only; different subject (graded source lines, not committed receipts) |
| `kumitate-shokunin/scripts/report-receipt-diff.mjs:4,11,18` | kumitate | `kumitate-report-receipt-diff-v4`; findings `RECEIPT_MISSING` (does not exist at rev / escapes with `..` / is a directory / **is a symlink**), `RECEIPT_EMPTY`, `TALLY_UNRECEIPTED`; exit 2 fail-closed | **`reusable`** — two exact patterns, see below. Not an overlap: it binds *report ↔ receipt*, never receipt blob → blob |
| `kumitate-shokunin/scripts/receipt-attest.mjs:10-32` | kumitate | nonce ledger scans the whole directory, any extension; `REPLAY`/`TAMPERED` verdicts | `none` — anti-forgery, not disclosure |
| `kumitate-shokunin/scripts/routed-ledger.mjs:1-14` | kumitate | every routed item needs a ledger row, bound by a located quote | `none` — defect routing, different subject |
| `kumitate-shokunin/corpus/QUALITY.md:700-721` (Q35) | kumitate | `grep`-style row rewrite counter: `Q35 rewritten=<n> removed=<m>` over committed `SOURCES.md` at two revisions | `none` — registry rows, not measurement receipts |
| `kake-shokunin/scripts/ledger_latest_check.py:1`, `scripts/receipt_replay.py:1` | kake | latest ledger figures vs committed receipts; round-23 receipt replay | `overlap` — kake-internal, neither watches receipt rewrites |

**Exact reusable pattern 1 — the ledger-introduction cutoff** (`kama/tools/append-only-audit.py:22-26`). kama refuses to let a ledger bless damage that happened *after* the ledger existed, because "a ledger that accepts new rows would bless any later damage". C1's frozen predicate has the weaker analogue `round_rewritten == 0` (`.ufo/waves/round-79/contract.md`, predicate), which guards only round 79 via `--round`. kama's rule is chronological, not per-round: a round-79 correction entry could then not silently absorb a future round-80 rewrite. This is **report-only** — the predicate is frozen and only the L1 may amend terms; noting it because a critic falsifying "does C1 build a gate that can bless its own successors?" will land on exactly this.

**Exact reusable pattern 2 — two fail-closed receipt checks** (`kumitate/scripts/report-receipt-diff.mjs:11,18`). (i) "a symlinked receipt is not a receipt" — kake's c79 already carries `symlinks == 0`; the two lanes independently converged on the same rejection, which is corroboration for the conjunct, not an overlap. (ii) `RECEIPT_MISSING` treats escape-with-`..`, directory, and symlink as one class — the same shape SentinelC must audit for manifest path handling in C2.

No sibling lane's QUALITY.md carries a criterion about rewriting a *committed measurement receipt*; the closest are append-only-prose rules (`tameshi/QUALITY.md:265-276`, `mori:123-128`, `tsukuroi:60`, `souji:13`), all about source/corpus text, not receipts.

## (c) Frozen case matrix with the oracle outside the tool root

| path | lane | shape | verdict |
|---|---|---|---|
| `kake-shokunin/.ufo/waves/round-78/cases/g01_absent_tag/{manifest.json,page.html,expect.json}` | kake | **r78 keeps the oracle inside each case dir** (`expect.json` beside the manifest) | `none` — the r78 precedent is the *opposite* of the r79 shape; do not describe r79 as "the r78 pattern" |
| `kake-shokunin/.ufo/waves/round-79/cases/c01/manifest.json` vs `.ufo/waves/round-79/expect/expect.json` | kake | oracle hoisted out of the case dirs; counter copies each manifest to `--work` so the tool sees opaque input | `overlap` (the claim's own) — **first occurrence in the fleet**: `ls -d *-shokunin/.ufo/waves/round-*/expect` returns only kake r79 |
| `kake-shokunin/.ufo/waves/round-78/c78_meta_robots_matrix.py:1-30` | kake | `--cases --consts`, per-case `expect.json` read by the counter, tool blob via `git show <rev>:scripts/meta_robots_audit.py` | `reusable` — the blob-from-revision extraction and `FROZEN_CASE_IDS` (never a directory count) carry to c79 unchanged |
| `kake-shokunin/.ufo/waves/round-41/oracle`, `mado-shokunin/.ufo/waves/round-21/oracle`, `round-22/oracle`, `kengaku-shokunin/.ufo/waves/round-53/labels` | kake/mado/kengaku | wave-scoped oracle/label dirs, but no counter takes a `--cases` + separate-oracle pair | `none` — `grep` for counters taking both `--cases` and `--truth/--labels/--expected` returns nothing fleet-wide |
| `mado-shokunin/.ufo/waves/round-78/fixtures/` | mado | one fixture file, no cases/oracle split | `none` |

## (d) Tools that already parse HTTP header fields for robots directives

| path | lane | finding | verdict |
|---|---|---|---|
| `kake-shokunin/scripts/header_audit.py:1-30,329-335,424-433` | kake | audits **transport/security** headers only — `content_type_present`, `hsts_present`, `xcto_nosniff_value`, `csp_present`, `singleton_fields`, `field_name_syntax`. `grep -n -i 'robots' scripts/header_audit.py scripts/response_snapshot.py` → **zero hits** | `none` for robots grammar; **`reusable`** manifest shape — `{"version":1,"checks":[{id,source,url,https,expect,headers}]}` (r61 C2, `header_audit.py:34-44`) |
| `kake-shokunin/scripts/response_snapshot.py:1-20` | kake | GET-only capture; records "every header field-line in wire order as `{name,value}` (duplicates preserved)"; creates files exclusively, never overwrites | `reusable` — it is the carrier C2 consumes, and its no-overwrite discipline is what makes the round-61 captures trustworthy input |
| `kake-shokunin/scripts/meta_robots_audit.py` | kake | the r78 meta-carrier audit; page-level only (README:550, PROVINCE:571-576) | `overlap` — same *shape* of declaration audit, different carrier; C2 must cite it as the sibling instrument, not re-derive vocabulary |
| `kake-shokunin/scripts/robots_audit.py`, `robots_audit_selftest.py` | kake | robots.txt audit (r37/r38) | `none` — different file |
| all other lanes | — | `grep -rln --include='*.py' -i 'x-robots-tag'` fleet-wide → only kake wave-scratch files (r56 spec builder, r79 retain/case/const files) | `none` |

The only prior kake code that touches `X-Robots-Tag` at all is `kake-shokunin/.ufo/waves/round-56/make_spec_w1.py:212`, and that is a seat-assignment sentence, not parsing.

## Coverage-map correction (must be a rewrite, not an append)

`kake-shokunin/corpus/README.md:558-559` and `kake-shokunin/PROVINCE.md:580-581` both read:

> Ground it does not hold: `X-Robots-Tag` response headers (the `response_snapshot.py` / `header_audit.py` instruments own that channel)

Both instruments exist (`git cat-file -e HEAD:scripts/response_snapshot.py`, `HEAD:scripts/header_audit.py` → present; `header_audit.py` is 48,986 bytes, last touched 2026-10-27). But `header_audit.py` holds no robots directive grammar (`grep -n -i robots` → 0 hits) and `response_snapshot.py` is a capture, not an audit. So the parenthetical is false in the direction that matters: the header *channel* is recorded, but the *robots declaration grammar on headers* is held by nothing. Once C2 lands, the exclusion sentence is directly contradicted by a committed tool, and a reader following it would be wrong twice over (wrong that the ground is refused; wrong about which instrument owns it).

ScribeKnowledge's row addition at `corpus/README.md:550` (the r78 row) is not enough: rows 558-559 and `PROVINCE.md:580-581` need an explicit correction naming `scripts/x_robots_tag_audit.py` and narrowing the refusal to what still holds (live serving, crawler behaviour, per-bot effective resolution, cross-carrier conflicts, redirect-hop inheritance). Reported, not edited — these are other seats' files and the contract reserves edits to them.

## Declared splits that should be updated

| path:line | declared split | action |
|---|---|---|
| `kake-shokunin/PROVINCE.md:38-48` | `## Adjacent` — `tabi` owns client-side crawler discipline; `kake` owns publisher-side placement | no change needed: a header declaration audit is publisher-side by construction and tabi's own screen (`tabi/.../adjacency-screen.tsv:35`) already declares no tabi side to cite |
| `kake-shokunin/PROVINCE.md:302-310` | surface `robots-txt-publisher-audit-vs-client-obedience` | no change: header carrier sits inside the same publisher half |
| `kake-shokunin/PROVINCE.md:323` | "Client-side crawler discipline stays with tabi; kake keeps…" | no change |
| `tabi-shokunin/corpus/adjacency-screen.tsv:35` | tabi's screen of kake `:412` | no change by kake — tabi owns that file and its verdict already reads `none` |

There is no `kake-shokunin/corpus/adjacency.tsv`; kake's adjacency lives only in `PROVINCE.md:38-48` plus the tabi-side screen. Nothing in the declared splits is invalidated by C2 — the only stale text is the two exclusion sentences above.

## Boundaries kept

Read-only scan of `/home/vgpnk/Projects/shokunin/*-shokunin`. No file in any sibling lane was created, modified or deleted; no `git`/`jj` mutation; no subagent. No scratch tree was needed, so nothing to remove. No tool was installed or upgraded this seat.
