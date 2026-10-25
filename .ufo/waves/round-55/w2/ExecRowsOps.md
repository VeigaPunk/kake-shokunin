# ExecRowsOps
ATTACKS: the three coverage-map rows added at revision a7a548e102b71bd16b0a6ddafa469393a2c98b69 in `corpus/README.md` §Coverage map — README:59 `knowledge/receipt-integrity.md` (S133), README:60 `knowledge/redirect-rewrite-rules.md` (S050, S135), README:65 `knowledge/vault-properties.md` (S019). Claim C1, calibration axis.

All bytes read with `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show a7a548e102b71bd16b0a6ddafa469393a2c98b69:<path>`; no worktree read was used as evidence. `git -C … rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin/kake-shokunin`.

## PER-ROW

Row extraction: `git show R:corpus/README.md | grep -n "knowledge/"` → rows at 59, 60, 65; each row has 3 cells, coverage cell 34 / 43 / 32 whitespace tokens, no `|` (`python3` split over `/tmp/readme.md` → `59 cells: 3 cov_tokens: 34 has_pipe: False` / `60 … 43 … False` / `65 … 32 … False`).

| file | statement (split from the coverage cell) | class | evidence (file line + quote <= 25 units) | command → observed |
|---|---|---|---|---|
| receipt-integrity.md | Three receipt defect classes (counter-error, tool-absent, stale planted) | SUPPORTED | L12 "## Three defect classes, each reachable in the round-44 instrument"; L20/L27/L34 name the three | `git show R:.ufo/waves/round-44/w2/ReviewCounterContract.md \| grep -cE '^\*\*\([abc]\) '` → `3` |
| receipt-integrity.md | v2 binding rule's exit gate | SUPPORTED | L56 "**exit gate** — counter exit in `{0, 1}`; anything else is class `counter_error`" | `git show R:.ufo/waves/round-45/c45_audit.py \| grep -n 'exit_code not in'` → L76 `if exit_code not in (0, 1):` |
| receipt-integrity.md | note gate | SUPPORTED | L57 "**note gate** — `receipt["note"] != "tool absent"`; else class `tool_absent`" | same file grep → L80 `if receipt.get("note") == "tool absent":` |
| receipt-integrity.md | counter-sha gate | SUPPORTED | L58 "**counter binding** — `receipt["counterSha256"] == sha256(invoked counter)`; else `stale_receipt`" | same grep → L82 `if receipt.get("counterSha256") != counter_sha:` |
| receipt-integrity.md | mtime-window gate | SUPPORTED | L59 "**run window** — receipt `st_mtime_ns` inside `[started_ns − 1 s, finish_ns + 1 s]`" | same grep → L15 `MTIME_EPS_NS = 1_000_000_000`; L91-94 `in_window = lower_ns <= receipt_mtime_ns <= upper_ns` |
| receipt-integrity.md | seed gate | SUPPORTED | L61 "**seed recorded** — a receipt without a `seed` is `stale_receipt`" | same grep → L87 `if "seed" not in receipt or receipt["seed"] is None:` |
| receipt-integrity.md | plus a toolSha256 control binding | SUPPORTED | L94 "the toolSha256 binding closes the receipt→control leg" | same grep → L85-86 `receipt.get("toolSha256") not in (None, expected_tool_sha)` |
| receipt-integrity.md | do-nothing reachability | SUPPORTED | L74 "## Do-nothing reachability"; L78 "Under v1 each reaches the declared after-state" | quote only (no count asserted) |
| receipt-integrity.md | 27-control count | SUPPORTED | L110-111 "27 controls in the round-44 claim cohort — `ls … \| wc -l` → `27`" | `git ls-tree -r --name-only R .ufo/waves/round-44/verification/claim/after-final/tools/ \| wc -l` → `27` |
| receipt-integrity.md | fixture counts | SUPPORTED | L112-113 "4 invalid/stale fixture classes plus 1 honest control" | `git ls-tree --name-only R .ufo/waves/round-45/fixtures/` → 5 dirs `counter-error honest stale-backdate stale-planted tool-absent` (= 4 invalid/stale + 1 honest) |
| receipt-integrity.md | two named residual limits | SUPPORTED | L91-92 "Two limits stay open after the wave-2 repairs, and both are named rather than closed" | quote only |
| redirect-rewrite-rules.md | Render and Cloudflare Pages redirect/rewrite rule semantics | SUPPORTED | L9-11 "Two static-host rule systems the lane's redirect/rewrite audit … models" | quote only |
| redirect-rewrite-rules.md | resource precedence | SUPPORTED | L18-20 "If a resource exists at the path, serve it — no rule is applied"; L40-42 Cloudflare's opposite | quote only |
| redirect-rewrite-rules.md | first-match order | SUPPORTED | L21-22 "Apply the first matching rule (starting from the top of the list)"; L38-39 "the top-most redirect is applied" | quote only |
| redirect-rewrite-rules.md | dashboard versus `_redirects` placement | SUPPORTED | L15 "Rules are dashboard-defined per site."; L35 "Rules live in a plain-text `_redirects` file in the static asset directory." | quote only |
| redirect-rewrite-rules.md | Cloudflare's status codes 301, 302, 303, 307, 308 with 302 default | SUPPORTED | L43-44 "Status codes 301, 302, 303, 307, 308 are supported; 302 is the default" | `git show R:corpus/knowledge/redirect-rewrite-rules.md \| grep -o "30[12378]" \| sort -u` → `301 302 303 307 308` (5 codes, 302 default on L43) |
| redirect-rewrite-rules.md | splat and placeholder expansion | SUPPORTED | L28-31 "A terminal `*` matches any string from that position"; L44-45 "Splats … and `:placeholders` work as in Render" | quote only |
| redirect-rewrite-rules.md | manifest fields declaring which precedence an offline audit applies | SUPPORTED | L49-51 "the manifest field `resourcePrecedence` (true = Render, false = Cloudflare Pages) and `defaultStatus`" | `git show R:scripts/redirect_audit.py \| grep -n 'resourcePrecedence\|defaultStatus'` → L174-175, L218, L225-228 (both read and validated) |
| redirect-rewrite-rules.md | No live serving claim | SUPPORTED | L53-56 "Nothing here is a live serving claim" | quote only |
| vault-properties.md | Static GET exposes the client-rendered PROPERTIES literal, so rot-checking needs no rendered DOM | SUPPORTED | L7-10 "a static GET sees the full `const PROPERTIES = [...]` source, so **rot-checking needs NO rendered DOM**" | quote only |
| vault-properties.md | 13 entries | SUPPORTED | L23 "`properties[]`, 13 entries"; L93 HOLD c1 "13 records" | `node -e 'eval(literal)'` over `git show R:.ufo/waves/round-23/live/vault-index-kimi/page.html` → `entries: 13` (file 10,059 B) |
| vault-properties.md | 3 null URLs | SUPPORTED | L29 "13 entries, 3 `url:null`"; L93 HOLD c1 "3 null URLs" | same node parse → `null_urls: 3`, `nonnull: 10`; null names `ds4cc| kimi mirror ; snapshot|.kimi.pro ; burnerchrome| — .com TBD` |
| vault-properties.md | seed-tag byte normalization | SUPPORTED | L72-76 "post-publish byte-digest checks MUST normalize the seed tag" | quote only |
| vault-properties.md | round-23 HOLD/STALE corrections where URLs marked live are not 200 | SUPPORTED | L95 c3 STALE "four of the nine URLs marked live … are non-200"; L97 c5 STALE plazir27runson now 404 | `git show R:.ufo/waves/round-23/receipts/vault-properties.json \| python3 -c …` → `c1 HOLD`, `c3 STALE`, `c5 STALE`, `c6 HOLD`, `c7 HOLD`, `c8 HOLD` (c3/c5 carry the non-200 content) |

ID CHECKS (row id set vs file `source:` header vs `corpus/SOURCES.md` at R):
- receipt-integrity.md: row `(S133)`; header L1 names S133 only → equal. `git show R:corpus/SOURCES.md | grep -nE '^\| *S(019|050|133|135) '` → S133 at line 141.
- redirect-rewrite-rules.md: row `(S050, S135)`; header L3-L4 names S050 and S135 → equal. SOURCES → S050 line 58, S135 line 143.
- vault-properties.md: row `(S019)`; header L1 names S019 → equal. SOURCES → S019 line 27.
- Duplicate check: `grep -cE '^\|.*`knowledge/<file>.md`.*\|'` over README → 1 each.

Nuances recorded, none classified as OVERREACH/UNSUPPORTED/STALE:
1. vault-properties row's "HOLD/STALE" is the section's marker vocabulary; the non-200-live-marked correction is STALE-only (c3, c5) — no HOLD item carries it. Existential reading holds, so SUPPORTED.
2. redirect row's "redirect/rewrite" for Cloudflare rests on the entry's own framing (L9-11); the Cloudflare section documents redirect rules and asset-shadowing, not a CF rewrite status.
3. receipt row: the entry's quoted driver sha `f3c3171b658abccd…0a076` is "at landing" (matches `run-manifest.json` driver_sha256 in all four `verification/matrix/runs/after/*`); current committed `c45_audit.py` hashes to `9b824d958d1494471f45ad84d6ae38ce600518311b1fb95af51b1098aac8a400` (`git show … | sha256sum`), so the file-level sha is landing-scoped, not present-bytes. The row's gate list still holds of current bytes (all six clauses present, greps above).
4. vault row cites S019, whose SOURCES scope is "Local provenance-field and lesson-heading census only; no verification of historical platform claims"; the entry's own header says "Metadata authority only: S019 … not present-day property state". Id equality passes; the id does not ground the PROPERTIES content (the retained literal does).

## COUNTS RE-DERIVED

- defect-class count 3: `git show R:.ufo/waves/round-44/w2/ReviewCounterContract.md | grep -cE '^\*\*\([abc]\) '` → `3`.
- 27 controls: `git ls-tree -r --name-only R .ufo/waves/round-44/verification/claim/after-final/tools/ | wc -l` → `27` (revision tree; the entry's own command was `ls` over the worktree).
- fixtures: `git ls-tree --name-only R .ufo/waves/round-45/fixtures/ | wc -l` → `5`; names = 4 invalid/stale + `honest`.
- vault entries/null: node parse of the retained literal at `R:.ufo/waves/round-23/live/vault-index-kimi/page.html` (10,059 B) → `entries: 13`, `null_urls: 3`, `nonnull: 10`, status `{"live":10,"queue":3}`.
- vault receipt agreement: `…/round-23/receipts/vault-properties.json` c1 observation → `COUNTS|entries=13|null_urls=3|live_urls=10|literal_bytes=2118`.
- Cloudflare status codes: 5 distinct (`301 302 303 307 308`), default 302 stated on L43.
- row shape: 3 cells, no `|` in coverage cell, 32-43 tokens each — all >= 5.
- `python3 -B .ufo/waves/round-55/c55_readme_index.py` (the C1 counter): unrun — out of this seat's assignment (owned by the counter seat).

## PROPOSED REPLACEMENTS

none needed — no statement in any of the three coverage cells was OVERREACH, UNSUPPORTED or STALE.

## UNRUN

- live re-observation of any vault property URL (no network GET by this seat; the counts come from committed retained bytes and the round-23 receipt).
- twin-literal parse of `ufo-fsd.kimi.page` (only the veigapunk retained body was parsed; the receipt records `literal_objects=13` on both twins).
- `c55_readme_index.py` run and any C1 predicate evaluation (not this seat's surface).
- `c45_matrix.py --stage after` re-run (driver bytes changed after landing; gate presence verified by grep, not by execution).

VERDICT: all 20 atomic statements in the three rows are SUPPORTED by committed bytes; every count re-derives (3 classes, 27 controls, 5 fixture dirs, 13 entries, 3 null URLs, 5 status codes) and all four cited ids match header and SOURCES rows — no replacement needed.
