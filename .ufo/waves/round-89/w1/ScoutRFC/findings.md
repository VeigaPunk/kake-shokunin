# ScoutRFC — round 89 registry-row evidence (lane-internal, not outside admission)

Lane `/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE). Base `76225160d0dff8d2042fbcd037bd08b0971d5e07`. Freeze `08ab46a1`. Dispatch `2e700b9a`. Re-measured HEAD at the time of the run: `acc69ba5`.

## 1. Live fetches (plain unauthenticated GET, no cookie, no Authorization, no token)

Command: `curl -sS --http1.1 -L -o <file> -w "... status=%{http_code} bytes=%{size_download} url=%{url_effective}\n" https://www.rfc-editor.org/rfc/rfc9111.txt` (and `rfc9110.txt`). Each URL was fetched once.

| URL | HTTP | bytes | sha256 | UTC access (file completion, mtime) | final URL |
|---|---|---|---|---|---|
| https://www.rfc-editor.org/rfc/rfc9111.txt | 200 | 84477 | aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e | 2026-11-04T21:13:39Z | same (no redirect) |
| https://www.rfc-editor.org/rfc/rfc9110.txt | 200 | 502941 | 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a | 2026-11-04T21:13:41Z | same (no redirect) |

Retained bodies: `receipts/rfc9111.txt`, `receipts/rfc9110.txt` (byte-identical to the sha256 above; both also match the lane's retained copies in round-80..88 waves). Honest limit: response headers were not retained (the `-w` line captured status, size and URL only). Scratch copies were deleted.

## 2. Located sentences (line numbers are in the retained plain text)

**RFC 9111 §4.1 (heading line 526, "Calculating Cache Keys with the Vary Header Field").** Nominated-field sentence, lines 530–532 (the sentence spans 528–534), 24 words:
> the cache MUST NOT use that stored response without revalidation unless all the presented request header fields nominated by that Vary field value match

Wildcard sentence, lines 556–557, 17 words: "A stored response with a Vary header field value containing a member "*" always fails to match."

Note: RFC 9111 §2 (lines 251–262) also uses the term "cache key" informally; §4.1 is the normative Vary-keying section.

**RFC 9110 §5.6.1.2 (heading line 1693, "Recipient Requirements").** Empty-element sentence, lines 1695–1697, 13 words:
> A recipient MUST parse and ignore a reasonable number of empty list elements

**RFC 9110 §12.5.5 `Vary` production:** heading line 5668; the stated production is at **line 5675**, exactly:
`     Vary = #( "*" / field-name )`
Collected ABNF (Appendix A, sender-expanded form) at lines 9823–9824: `Vary = [ ( "*" / field-name ) *( OWS "," OWS ( "*" / field-name ) ) ]`.
Supporting: `field-name = token` at line 1466 (§5.1); `token = 1*tchar` at line 1733 (§5.6.2).

## 3. Registry (`corpus/SOURCES.md`)

- **Highest existing S id at base `76225160`: S463** (201 rows, S001–S463; `awk NF!=13` malformed count 0). **At HEAD `acc69ba5`: S465** (S464 and S465 added by commit `fcb615c6`).
- **Both URLs already appear at base.** `https://www.rfc-editor.org/rfc/rfc9111.txt` is cited by S456 (base line 203). `https://www.rfc-editor.org/rfc/rfc9110.txt` is cited by S028, S033, S453, S454, S455. The RFC 9111 HTTP-caching URL `https://httpwg.org/specs/rfc9111.html` is cited by S461, S462, S463.
- **Shape: 11 columns = NF 13 when split on `|`** (leading and trailing empty cells). Header (line 7): `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`. Separator line 8. All 202 pipe rows at base have 11 cells.
- **Template row (real, base line 210, S463), cell by cell:**
  `| S463 | RFC 9111 - HTTP Caching, Calculating Cache Keys with the Vary Header Field - https://httpwg.org/specs/rfc9111.html#caching.negotiated.responses | spec | A | <scope> | <anchor> | <teaches> | mined | 2026-11-04 | 180d | corpus/knowledge/vary-matching.md |`
  Enums: `kind` in {spec,docs,paper,code,tool,dataset,talk,book,community,own-work}; `tier` in {A,B,C}; `status` in {queued,mined,rejected}; `recheck` = `NNd` or ISO date or symbolic; `used-by` = comma list of existing repo-relative paths or `—`.
- **Census at base:** `scripts/sources-census.sh validate --root <base-archive> --file <SOURCES>` → exit 0, 25 `W04` lines, 0 `E*` lines. Simulated insertion of one new row (used-by `corpus/knowledge/vary-matching.md`, which exists at base) on a full `git archive` of base → exit 0, **26 `W04`** (base+1). Receipts: `receipts/basefull.out`, `receipts/simfull.out`. At HEAD `acc69ba5` the lane's `controls/census-final-tip.txt` reads 27 `W04` (S464 and S465), per the lane's own receipt.

## 4. Round-88 `## Gate` (`corpus/lessons/round-88.md`, heading line 14; next `## ` heading line 48)

Decisions parsed by the C1 counter's item B logic (`**admit**`/`**reject**` in the Decision cell):
- **admit: 2** — row line 33 (RFC 9111 §4.1 match rule), row line 34 (RFC 9110 §12.5.5 `Vary` grammar).
- **reject: 2** — row line 35 (the "counter-pass shows §4.1" proposition), row line 36 (empty-`Vary` refusal as an RFC requirement).

Parsed identically at base and at the worktree (`admits=2 rejects=2`). The round-89 lesson at HEAD states `gate-sample: admits=2 rejects=2` and `r88-gate-summary-correction: admits=2 rejects=2`; item B agrees. Item B's `round-89 lesson missing` at base is expected (the lesson is not in base).

## 5. Measured defects (new, not in the six routed items unless noted)

**D-1 (C2 counter — shortcut guard bypass, met=true for a shortcut). Severity: blocks the C2 claim.**
Candidate `receipts/esc_candidate6.py` loads the round's own reference by scanning `.ufo/waves/round-89` at run time with `pathlib` and `exec`s it, mapping the reference's `Invalid` to `invalid_input` exit 1. Scored with the current `c89_key.py` (`guard`, `score_candidate`, seed 89089, in a scratch `work` dir):
`guard note: None` → `frozen=16/16 props=200/200 refuse=9/9` → met would be **true**.
The v1 guard (`FORBIDDEN` incl. `'.ufo/waves'` and `'round-89'`, plus the `open(` check) refuses this same source (`'.ufo/waves'` and `'round-89'` both occur in it). The v2 amendment (`46a43e94`) removed `.ufo/waves`, `round-89`, `frozen`, `oracle`, and the v2 `open(` check only catches a literal `open(` on a line that also mentions `.ufo`. So the freeze-v2 relaxation admits this bypass. The contract's rule "must not read any file under `.ufo/waves/`" is therefore not enforced. The freeze's disclosed limit ("a candidate that imports the reference under another name is not detected") understates this: the candidate reads the reference from disk by path.

**D-2 (C2 counter — contract-required rule with no killing property).** Mutant `uri-not-escaped` (`key = esc(uri) +` → `key = uri +`) scores **frozen 16/16, props 200/200, refuse 9/9 → met=true**. Contract §4 mandates `%`→`%25` and the four separators escaped in the URI. The property population has no URI-with-separator or URI-with-`%` class (`uri_change` only appends `/x`), and no frozen case has one. Demonstrated collision with the mutant: `{"uri":"x","request_headers":{"a":"v"},"vary":"a"}` and `{"uri":"x\x1fa\x1ev","request_headers":{},"vary":""}` both key to `x\x1fa\x1ev`; the reference keeps them distinct (`x\x1fa\x1ev` vs `x%1Fa%1Ev`).
Other mutants: `percent-not-escaped` → 15/16, 200/200 (killed only by a frozen case); `no-uri-value-trim` → 14/16, 180/200 (killed). `names-not-escaped` (`esc(name)`→`name`) survives but is **equivalent**: `tok()` restricts names to tchar, which excludes `%` and the four control separators, so no behaviour changes on accepted input.

**D-3 (C1 counter — item E is not revision-pinned; the base control has drifted).** `item_e` reads `git log` over the repo's full history from HEAD, not the `--revision` argument. At base `76225160`, `c89_defect_queue.py --revision 76225160 ...` now prints `items=6 open=5 closed=1 met=false`, exit 1, with `E-freeze-before-dispatch: []`. The committed control `controls/base-c1.txt` reads `open=6 closed=0` (its E line: "no commit adds .ufo/waves/round-89/c89_key.py"). The predicate text "the same counter at the base prints open=6" is no longer reproduced; exit 1 still holds. Receipt: `receipts/rerun-base-c1.txt`.

**D-4 (C1 counter — item E misses post-dispatch amendment; R88-E repeat).** At HEAD `acc69ba5`, `item_e` returns `[]`. But `2e700b9a` (dispatch, 18:13:04-03:00) precedes `46a43e94` (freeze v2, 18:16:18-03:00), and v2 amended `.ufo/waves/round-89/c89_key.py` and `controls/base-c2.txt` after dispatch. Item E checks only the first-add ancestry and committer time of `c89_key.py`. The lane's own `w1/ExecDefects.md` already flags this; my measurement confirms it.

**D-5 (C1 at HEAD: item A open, 3 lines).** `c89_defect_queue.py --revision HEAD` (acc69ba5): `open=1 closed=5 met=false`, exit 1. Open: `SCORECARD.md:5469`, `SCORECARD.md:5488` and `corpus/lessons/round-88.md:265` keep `22/22` without an `[r89-correction` tag. Items B, C, D, E (as in D-3/D-4), F pass at HEAD. Receipt: `receipts/rerun-head-c1.txt`.

**D-6 (round-88 lesson factually wrong at its own commit; not among R88-A..F).** `corpus/lessons/round-88.md` lines 37–40 state "the lane registry still ends at **S462** (`grep -c 'S463' corpus/SOURCES.md` → 0)" and lines 191–196 say the S463 row is "not yet observed". Base `76225160` has S463 at line 210 (`grep -c 'S463'` on the base blob → 1), and commit `55d67f15` (round-88 integration, before the lesson commit `edcb2980`) adds S463. The lesson's registry-delta claim is contradicted by committed bytes.

**D-7 (instrument scope, disclosed for L1).** The selftest for C2 (`c89_key.py --selftest`, 43/43) reproduces the committed `controls/c2-selftest.txt` byte-for-byte (`diff` identical, exit 0). I ran it without a `TMPDIR` override (inherited TMPDIR; disclosed, not a counter defect).

## 6. Commands and exits (all read-only against the lane; scratch deleted)

- `curl ... rfc9111.txt` / `rfc9110.txt` → 200 each (above).
- `bash scripts/sources-census.sh validate --root <archive> --file <SOURCES>` → base 0; base+S464 row 0 (26 W04); 3 E11 when used-by files were absent from a partial archive (disclosed: my first partial-tree attempt was wrong, not a lane defect).
- `python3 -B .ufo/waves/round-89/c89_key.py --root . --revision 76225160… --candidate scripts/cache_key.py --work <scratch>` → exit 1, `frozen=0/16 props=0/200 refuse=0/9 controls=5/5 met=false (candidate absent)`. Receipt `receipts/rerun-base-c2.txt` (matches committed `base-c2.txt`).
- `python3 -B .ufo/waves/round-89/c89_defect_queue.py --root . --revision {76225160…|HEAD} --work <scratch>` → exit 1 both (base open=5 — D-3; HEAD open=1 — D-5).
- `python3 -B .ufo/waves/round-89/c89_key.py --selftest` → exit 0, `selftest: 43/43 passed`.
- Mutant and candidate runs: `c89_key._ref_source()` with `str.replace` mutants, scored by `score_candidate` (listed above).

## 7. Tooling and channel record

No tools installed. Used `curl 8.23.0` (already on host), `git` (read-only), `python3`, `awk`, `sha256sum`. Pacman was not touched.

## 8. Writes and disclosures

- Writes: `w1/ScoutRFC/findings.md`, `w1/ScoutRFC.md`, `w1/ScoutRFC/receipts/*` (RFC bodies, census outputs, selftest, reruns, the candidate). Scratch dir `/fast/scratch/hyaku/kake-r89/ScoutRFC/` created and deleted before yield (`ls` confirms absent).
- One 1-line file was written to `/tmp/s463row.txt` by a `awk ... > /tmp/...` line, and removed (`ls` confirms absent). This violates the "no /tmp" rule for one file; disclosed.
- No commit, push, git mutation, fleet-repo write, sibling write, or task delegation.
- The lane's HEAD advanced during my run (`46a43e94` → `08ce630d` → `acc69ba5`, and L1 added S464/S465). Live-tree simulations were therefore taken from `git archive` snapshots, not the live worktree.
