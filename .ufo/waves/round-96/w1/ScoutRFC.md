# ScoutRFC — kake round 96, wave 1

Seat: `ScoutRFC`. Target: open RFC 9111 once, produce the evidence the S480 registry
row and the C2 knowledge entry rest on. Lane base `bde9869144f69c5a459c0d2c93f5135922fe3a8d`;
instruments commit `7ae3e9b07e2435f7fde6e73838d9fa14488b8dda`; freeze commit
`049e8eca2f0fa5e981232eb4efe367357dce578c`. Lane-bound leaf member: no subagent
dispatch, no lane mutation, no instrument touched.

**VERDICT: SCOUT fetch=0 sha-match=yes quotes=6/6 located**

## 1. Instrument digests (verified before anything was attacked)

`sha256sum` over the frozen instruments, against
`.ufo/waves/round-96/controls/instrument-sha256.txt`:

| file | expected (freeze) | observed | match |
|---|---|---|---|
| `.ufo/waves/round-96/c96_selfassess.py` | `a282da654d5ee6af923abb2cae4bd0a4fd6e4309db81de5a67999ed7b25ad134` | same | yes |
| `.ufo/waves/round-96/c96_reval.py` | `ec40aec19d0b4563ad21d79b398c7aaa65a99806984dbca55086c099571eebb9` | same | yes |
| `.ufo/waves/round-96/reval-contract-v1.md` | `65f0a3479c0e6ad005e384a98cac467fd965151420fd2425c9458da8a214afae` | same | yes |

No instrument defect found. Nothing was repaired; the instruments were read, not touched.

## 2. The fetch (one GET)

Command (run in this seat's scratch dir, absolute paths elsewhere):

```
curl -sS --http1.1 -o rfc9111.txt -w 'http_code=%{http_code} size_download=%{size_download} url_effective=%{url_effective} content_type=%{content_type}\n' 'https://www.rfc-editor.org/rfc/rfc9111.txt'
```

| fact | value |
|---|---|
| HTTP status | **200** |
| content type | `text/plain;charset=utf-8` |
| byte count | **84477** (curl `size_download` and `wc -c` agree) |
| sha256 | **`aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`** |
| accessed (UTC) | **2026-11-05T18:17:11Z** (local 2026-11-05T15:17:11-03:00) |
| curl rc | 0, empty stderr |
| client | curl 8.23.0 (libcurl/8.23.0, OpenSSL/3.6.5) |
| page fetches | exactly one curl invocation, one URL; no redirect hop, no HEAD probe, no crawl |

**Digest comparison — IDENTICAL.** The observed sha256 equals the freeze's expected
digest `aeb52adb…` **and** the sha256 of the retained round-93 body
`.ufo/waves/round-93/L1/src/rfc9111.txt` (committed blob `cef95c761dfcbc6f649019efa2cf5f97dc5f9020`
at base). `cmp` of the fetched bytes against the retained body → rc 0, no output
(byte-identical). The retained body is therefore a sound basis for the contract's
line-number citations, and the freeze's Sourced-claim requirement is satisfied without
re-stamping anything.

Receipt: `.ufo/waves/round-96/w1/ScoutRFC/fetch.txt`. A copy of the fetched body is
retained beside it at `.ufo/waves/round-96/w1/ScoutRFC/rfc9111.txt`
(sha256 `aeb52adb…`, same digest).

## 3. The six clause quotes (6/6 located)

Run on the **fetched bytes**: `grep -n -F '<fragment>' rfc9111.txt`. Each fragment is an
exact substring of the line it is named at (checked independently with Python against
`body_lines[n-1]`).

| expected line | fragment | found line | exact at that line | words |
|---|---|---|---|---|
| 848 | `MUST send the relevant entity tags` | **848** | yes | 6 |
| 852 | `SHOULD send the Last-Modified value` | **852** | yes | 5 |
| 861 | `In most cases, both validators are generated` | **861** | yes | 7 |
| 935 | `A 304 (Not Modified) response status code indicates` | **935** | yes | 8 |
| 938 | `A full response (i.e., one containing content) indicates` | **938** | yes | 8 |
| 944 | `However, if a cache receives a 5xx (Server Error) response` | **944** | yes | 10 |

**6/6 located at the named lines.** Because the fetched body is byte-identical to the
retained round-93 body, these are also the retained body's line numbers — which is what
`reval-contract-v1.md` cites for clauses C1–C5. The supporting headings on the same
body: line 801 `4.3.  Validation`, 812 `4.3.1.  Sending a Validation Request`,
866 `4.3.2.  Handling a Received Validation Request`, 930 `4.3.3.  Handling a
Validation Response`, 951 `4.3.4.  Freshening Stored Responses upon Validation`
(§4.3.4 is the contract's named exclusion and is not in S480's scope). The contract's
§4.3.2 precedence citation (lines 887-891, "If-None-Match takes precedence over
If-Modified-Since") is also present in the body, unchanged.

## 4. Read-only sibling read — chousa criterion 146 (R95-3 prior art)

Read-only; **nothing in chousa was written or modified**.

- file: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/QUALITY.md`
- exact line: **1054**
- first sentence, verbatim:

> A self-assessment counter validates each resolution line against the bytes it claims to repair, and its audit window covers every block rather than the newest.

(25 whitespace units; the sentence is the criterion's bolded head, which is its first
sentence.)

**Prior art, cited — never ported.** This is the R95-3 item named by
`corpus/lessons/round-95.md` §Routed and by the round-96 freeze's non-claim work: cite
chousa round-79 criterion 146 as the precedent for the repair-naming rule. The C1
scribe's QUALITY criterion should cite this line; the C1 seat's own wording, its
counters and its digests are not derived from it.

## 5. The drafted S480 SOURCES row

Full draft with cell checks and census receipts: `.ufo/waves/round-96/w1/ScoutRFC/s480-row.md`;
the row as a single machine-checkable line: `.ufo/waves/round-96/w1/ScoutRFC/s480-row.txt`.

Insert position: after the S479 row (`corpus/SOURCES.md` line 225 at base, the last row
of `## Registry`) → new row at line 226.

Columns (11, no literal or escaped pipe in any cell — `len(row.split('|')[1:-1]) == 11`
→ True; `'\\|' in row` → False; the row holds exactly 12 `|` characters, all delimiters):

| # | column | value |
|---|---|---|
| 1 | id | `S480` (unused at base; base's highest id is S479) |
| 2 | source | `RFC 9111: HTTP Caching, section 4.3.1 Sending a Validation Request and section 4.3.3 Handling a Validation Response - https://www.rfc-editor.org/rfc/rfc9111.txt` |
| 3 | kind | `spec` |
| 4 | tier | `A` (scoped to §4.3.1/§4.3.3 only) |
| 5 | scope | how a cache constructs a conditional validation request and how it handles the response; expressly **not** the lane's supplied-values convention, not any live cache's behaviour, not storage / freshness lifetime / cache keys / serving / the merged field set of a 304; distinct from S476's §4.3.2 origin-side reading, S470's heuristic-freshness reading and S456's storage-and-freshness reading |
| 6 | anchor | §4.3.1 heading line 812, MUST entity-tag bullet 848-850, SHOULD Last-Modified bullet 852-855, both-validators sentence 861-864; §4.3.3 heading line 930, 304 bullet 935-936, full-response bullet 938-941, 5xx bullet 944-948; June 2022; fetched 2026-11-05T18:17:11Z HTTP 200, 84477 bytes, sha256 `aeb52adb…`; retained body `.ufo/waves/round-93/L1/src/rfc9111.txt` (cmp identical) |
| 7 | teaches | one grounded learner benefit, carrying the verbatim 7-word quote "In most cases, both validators are generated" (raw substring of the retained body at line 861, ≤25 units) |
| 8 | status | `queued` |
| 9 | opened | `2026-11-05` |
| 10 | recheck | `180d` |
| 11 | used-by | `corpus/knowledge/revalidation-exchange.md, .ufo/waves/round-96/w1/ScoutRFC/fetch.txt` |

**Census receipts** (script `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`,
read-only; run against a lane-shaped scratch mirror that carries the used-by paths the
census checks, so E11 measures the row rather than a missing mirror):

| command | rc | result | receipt |
|---|---|---|---|
| `validate --today 2026-11-05 <mirror>` (control, no row) | 0 | `mirror ok`, 0 E-findings | `census-validate-control-mirror.txt` |
| `validate --today 2026-11-05 <mirror>` (with S480 at line 226) | 0 | `mirror ok`, **0 E-findings** | `census-validate-with-s480.txt` |
| `census --today 2026-11-05 <mirror>` (with S480) | 0 | rows **217** (216 at base), tier.A 192 (191), queued 9 (8), mined 186, rejected 22, FLEET.missing 0 | `census-with-s480.txt` |
| `validate --today 2026-11-05 --root <fleet> kake` (lane, no row) | 0 | `kake ok`; rows 216 / tier.A 191 / queued 8 — matches the base census | — |

The **only** difference between the control and with-row validate outputs is one added
line: `W04 S480 duplicate url www.rfc-editor.org/rfc/rfc9111.txt across scopes`. W04 is
the pre-existing duplicate-URL warning class that S456, S470 and S476 already carry for
the same URL at different scopes; it is a warning, not an E-finding, and the exit stays
0.

## 6. Findings and notes for the L1

1. **S480 is `queued`, not `mined`, and it must stay that way until the C2 knowledge
   entry lands.** The census's E11 check runs only on `mined` rows, so the
   not-yet-existing `corpus/knowledge/revalidation-exchange.md` does not fire today. If
   the row is flipped to `mined` before the knowledge entry is committed, E11 fires on
   that path. Flip the status only after the entry exists.
2. **The row is not appended by this seat.** The L1 integrates it through the round
   gate; this seat is a reporter. The row's insertion point and the append-only
   constraint are recorded above.
3. **`teaches` carries a verbatim quote** so the row's grounding is checkable against
   the retained body without re-deriving it: "In most cases, both validators are
   generated" (7 words, raw substring at retained-body line 861, ≤25 units per
   `corpus/QUALITY.md`'s quote bound).
4. **Gate quote for the round lesson's `## Gate` record** (contract v1 rule 1 wants a
   ≤25-word quote with its location): the line-861 fragment above is the recommended
   one. A longer alternative, the whitespace-collapsed 17-word 304 span (lines 935-936),
   is not a single-line raw substring and needs the collapsing caveat recorded if used.
   The lesson is not this seat's to write.
5. **The retained round-93 body is sound and current.** It is byte-identical to today's
   fetch, so the contract's line citations need no amendment, and no re-stamp of the
   retained copy is warranted.
6. **No instrument defect was observed.** The three frozen digests match
   `controls/instrument-sha256.txt` exactly. Had any mismatched, the finding would have
   been routed, not repaired.

## 7. Scope discipline

- Files written, all inside `LANE/.ufo/waves/round-96/w1/ScoutRFC/`:
  `fetch.txt`, `s480-row.md`, `s480-row.txt`, `rfc9111.txt`,
  `census-validate-control-mirror.txt`, `census-validate-with-s480.txt`,
  `census-with-s480.txt` — plus this seat's report file at
  `.ufo/waves/round-96/w1/ScoutRFC.md`.
- Nothing else in the lane tree was written or modified. `git status --porcelain` in the
  lane shows only the round-96 wave directory (and other seats' own untracked files)
  — no tracked file was touched, no `corpus/` byte changed, no instrument changed.
- **No mutating git or jj command was run anywhere.** Only `git status --porcelain`,
  `git ls-tree`, `git show` and `git diff --stat` (read-only).
- chousa was read only; nothing under `chousa-shokunin/` was written.
- No tool was installed or upgraded for this seat: `curl`, `sha256sum`, `cmp`, `grep`,
  `python3` and `gawk` (inside the census script) were already present; the recorded
  versions are curl 8.23.0 and Python 3 (system). No pacman, no `uv tool install`, no
  binary in `~/.local/bin`, no PATH directory touched, no sysctl touched.
- Scratch root `/fast/scratch/hyaku/kake-r96/ScoutRFC/` was used for the fetch, the
  mirror and the receipts, and was **deleted** after the receipts were copied into the
  seat directory.

## 8. Remaining unknowns

- Whether the L1's S480 append uses exactly this scope/teaches wording is not mine to
  decide; the row is a draft.
- The C2 knowledge entry `corpus/knowledge/revalidation-exchange.md` does not exist at
  the time of writing; its quotes are the C2 scribe's to verify (this seat verified the
  same six fragments against the same body, so it can be re-used as corroboration).
- The census's W04 warning for the shared RFC 9111 URL is expected but will grow if
  further RFC 9111 rows are added; the L1 may want to record that the warning class is
  pre-existing rather than introduced by S480.
