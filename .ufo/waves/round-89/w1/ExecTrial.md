# ExecTrial — round 89 C2 real-data trial

Seat: ExecTrial (leaf; no subagent dispatch). Scope: run the C2 cache-key
capability on recorded response headers from the round-23 / round-61 / round-81
capture trees, end to end. No production edits, no commits, no network GET.

## 1. Inputs and provenance

Recorded `vary` values come from `response.json` captures in the LANE tree
(`.ufo/waves/round-61/capture/*/response.json`, `.ufo/waves/round-81/capture/*/response.json`).
Each capture's full file sha256 is in `outputs/provenance.json` and inside
`outputs/results-reference.json` (`captures`).

Round-23 was checked first and **cannot** supply a recorded `vary`: its 12
`live/*/fetch.json` files carry only `bytes, contentType, error, fetchedAt, finalUrl,
method, redirects, sha256, status, truncated, url` — no response headers. The
header-bearing trees are round-61 (12 captures) and round-81 (3 captures).

A repo-wide scan of every `response.json` / `fetch.json` under `.ufo/waves/`
found `Vary` values only of `Accept-Encoding` or `Origin`. **No capture carries a
`*` wildcard.**

Recorded-vary construction: RFC 9110 §5.3 combination of duplicate header lines.
Several captures carry `Vary` as two lines (`Accept-Encoding`; `Origin`). The
driver joins them with `", "` to get one `vary` string. The contract does not
specify this step (see §5, defect D1).

Real surfaces used (status 200 unless noted):

| case | capture | url | recorded vary | recorded vary lines |
|---|---|---|---|---|
| R1 | round-81/capture/ds4cc-primary | https://ds4cc.com/ | `Accept-Encoding` | 1 |
| R2, R2b, R3 | round-61/capture/burnerchrome-kimi, vault-index-kimi | https://burnerchrome.kimi.page/, https://veigapunk.kimi.page/ | `Accept-Encoding, Origin` | 2 |
| R4 | round-61/capture/charter-ghp | https://veigapunk.github.io/charter-ufo-fsd/ | `Accept-Encoding` | 1 |
| R5 | round-61/capture/ufo-fsd-kimi-pro | https://ufo-fsd.kimi.pro/ | *(none)* | 0 |
| R6 | round-81/capture/ds4cc-sitemap | https://ds4cc.com/sitemap.xml | `Accept-Encoding` | 1 |

Excluded surfaces: `round-61` `charter-kimi`, `lucario-kimi`, `plazir15-kimi`,
`plazir27-kimi` return **HTTP 404** (identical body sha256
`93ddca9a021664d5…`). Their recorded `Vary` is `Accept-Encoding, Origin` but
they are error pages, so they are not used as surfaces.

Request header maps are **constructed**, not recorded: each map contains only
fields the recorded response nominates (`Accept-Encoding: gzip, deflate, br`,
`Origin: https://requester.test`). Request values are my plausible choices;
the recorded responses do not say what a request carried.

## 2. Driver and candidates

- Driver: `driver/trial.py` (copy of `/fast/scratch/hyaku/kake-r89/ExecTrial/driver/trial.py`).
  It builds each input from the capture file, runs `python3 -B <candidate>` with
  the JSON on stdin in a fresh subprocess (cwd = scratch output dir), and records
  exit, stdout, stderr and the participating fields parsed from the key.
- Primary candidate: the frozen reference `REFERENCE` string extracted by `ast`
  from `.ufo/waves/round-89/c89_key.py` into `driver/reference_c89_key.py`
  (2554 bytes, sha256 `3c514c7d982749ab66c66ce495c21c1a954bde031acdc02bb1a56b623adf2962`).
  The ExecKey candidate is not final; I used the reference as the task allowed.
- Cross-check: L1's draft `.ufo/waves/round-89/w1/L1/cache_key.py` (sha256
  `864e5f127ce36030e5f6e40b8c6d7e1a8a7fec4be1d8bb6d22fcb22156d155ef`, read-only copy
  run from scratch). It is not a lane candidate; I ran it only as a second opinion.
- Driver check: the frozen 16-case file `frozen/c2-cases.json` run through the same
  stdin path against the reference gives **16/16** (expected key or expected
  refusal substring).

Commands (scratch paths; all exit as shown):

```
python3 -B trial.py reference_c89_key.py out-reference <LANE>/.ufo/waves   -> exit 0 (all runs; refusals reported per case)
python3 -B trial.py l1_draft_cache_key.py out-l1draft <LANE>/.ufo/waves    -> exit 0
frozen-case passthrough via stdin driver                                    -> 16/16, exit 0
```

Note: an earlier command I ran, `reference_c89_key.py --selftest`, is a misuse
and not evidence. That reference has no `--selftest` mode; it read stdin, got no
JSON and exited 1 (`invalid_input: not JSON`). I make no claim from it.

## 3. Results (reference; L1 draft matches on every key and exit)

Stored under `outputs/`; every case has `inputs/<id>.json`,
`outputs/<id>.reference.stdout`, `outputs/<id>.reference.stderr`.
Control bytes are shown as `\x1f` (US), `\x1e` (RS), `\x1c` (GS).

| id | kind | exit | key (escaped) | participating fields |
|---|---|---|---|---|
| R1-ds4cc-primary-ae | real | 0 | `https://ds4cc.com/\x1faccept-encoding\x1egzip, deflate, br` | accept-encoding present |
| R2-burnerchrome-ae-origin-present | real | 0 | `https://burnerchrome.kimi.page/\x1faccept-encoding\x1egzip, deflate, br\x1forigin\x1ehttps://requester.test` | accept-encoding present; origin present |
| R2b-burnerchrome-origin-present-empty | real | 0 | `https://burnerchrome.kimi.page/\x1faccept-encoding\x1egzip, deflate, br\x1forigin\x1e` | accept-encoding present; origin present-empty |
| R3-vault-index-ae-origin-absent | real | 0 | `https://veigapunk.kimi.page/\x1faccept-encoding\x1egzip, deflate, br\x1forigin\x1e\x1c` | accept-encoding present; origin absent (GS) |
| R4-charter-ghp-lowercase-names | real | 0 | `https://veigapunk.github.io/charter-ufo-fsd/\x1faccept-encoding\x1ebr` | accept-encoding present (request name lowercase, matched) |
| R5-ufo-fsd-kimi-pro-no-vary | real | 0 | `https://ufo-fsd.kimi.pro/` | none (no vary) |
| R6-ds4cc-sitemap-ae | real | 0 | `https://ds4cc.com/sitemap.xml\x1faccept-encoding\x1egzip` | accept-encoding present |
| X1-synthetic-wildcard-on-ds4cc | synthetic | 1 | — | `invalid_input: vary wildcard nominates no field` |
| X2-synthetic-trailing-comma-on-burnerchrome | synthetic | 1 | — | `invalid_input: vary member is not a token` |
| X3-synthetic-duplicate-header-case-on-burnerchrome | synthetic | 1 | — | `invalid_input: duplicate header name` |
| X4-synthetic-crlf-in-origin-value | synthetic | 1 | — | `invalid_input: header value contains CR or LF` |
| X5-synthetic-vary-duplicate-member-case | synthetic | 1 | — | `invalid_input: duplicate vary member` |

Checks visible in the table: R2 vs R2b differ (present `https://…` vs present-empty),
and R2b vs R3 differ (present-empty vs absent GS). The ordering in the key is by
lowercased name (`accept-encoding` before `origin`), and the request-side casing
(`accept-encoding` in R4) matches the recorded `Vary` casing `Accept-Encoding`
through the lowercase rule.

## 4. Refusal coverage — what the real data gives

- **Real-data refusals: 0 of 6.** No recorded surface's `vary` triggers any
  contract refusal; every real surface returns exit 0.
- The `*` refusal the seat spec asked for does not exist in the real data. X1
  is therefore **synthetic**: the recorded surface URL with `vary` replaced by
  `*`. Its exit 1 shows the candidate refuses the wildcard; it does not show that
  any server sent one.
- X2–X5 are also synthetic. They exercise the refusal list (trailing comma,
  duplicate header case, CR/LF in a value, duplicate vary member case) on real
  surface URLs and real recorded vary strings.

## 5. What the trial establishes, and what it does not

Establishes:
- The reference and the L1 draft both build the declared key form on six real
  recorded-vary inputs, and both refuse five constructed invalid inputs with
  exit 1 and the contract's refusal class. The two differ only in refusal wording
  (`invalid_input:` prefix and reason text), not in exit or key.
- Absent vs present-empty vs present are distinct keys on real vary data (R2b,
  R3 above).
- A surface with no recorded `Vary` gets a key of `ESC(uri)` alone (R5).

Does not establish:
- **Anything about what a server, CDN or browser stores or serves.** A key
  computed from a recorded `vary` is evidence about key construction only. The
  contract says so (§Scope), and this trial does not overturn it.
- Anything about the request headers a real client sent. They are constructed
  to match the recorded nomination, not observed.
- Anything about duplicate-header combination rules a real server or cache
  applies. The driver's `", "` join is my adapter choice.
- Any real-data refusal (none exists in this corpus; see §4).
- The ExecKey candidate, which is not final.

## 6. Defects and gaps found

- **D1 (contract gap).** The contract takes `vary` as one string but does not say
  how duplicate `Vary` header lines are combined. Seven of the twelve round-61
  captures arrive that way: three at status 200 (burnerchrome-kimi, ds4cc-kimi,
  vault-index-kimi) and four at status 404 (charter-kimi, lucario-kimi, plazir15-kimi,
  plazir27-kimi). The round-81 captures each carry one line.
  Choosing `", "` (RFC 9110 §5.3) is an adapter decision the contract must
  declare or pin.
- **D2 (case-set gap).** The frozen 16 cases and the property population do not
  include a Vary wildcard example drawn from recorded data; that is unsurprising
  (no capture has one), but it means refusal evidence from real data is zero.
- **D3 (round-23 data gap).** `round-23/live/*/fetch.json` carries no response
  headers, so round-23 cannot provide `vary`. The scout scoping that named it as
  a header source was wrong for header data; round-61 and round-81 are the only
  header-bearing trees.
- **D4 (captured 404s).** Four round-61 captures return 404 with a `Vary` header
  and identical body sha. They are usable as header evidence but not as surfaces.
  Any future C2 real-data trial must filter on status.
- **D5 (ExecKey not final).** The ExecKey candidate was not final when I ran.
  This trial used the frozen reference and the L1 draft only.

## 7. Tools

No tools were installed or upgraded. Only the Python 3 interpreter on the host
was used (`python3 -B`). No network GET was made. No pacman, no `uv tool`
installs.

## 8. Checks for L1 to run

- Re-run the driver against the final `scripts/cache_key.py`:
  `python3 -B driver/trial.py <final>/scripts/cache_key.py <out> <LANE>/.ufo/waves`
  and diff `outputs/results-*.json` key and exit fields.
- Decide D1 (declare the `Vary` line-combination rule in the contract, or pin
  it in the driver), before any real-data row goes into SCORECARD.

## 9. Scratch and receipts

- Scratch root `/fast/scratch/hyaku/kake-r89/ExecTrial/` was used for the driver,
  the reference copy, the L1 draft copy and outputs. Those outputs are copied to
  this directory (`outputs/`), and the scratch directory is removed before yield.
- Receipts copied here: `driver/trial.py`, `driver/reference_c89_key.py`,
  `outputs/results-reference.json`, `outputs/results-l1draft.json`,
  `outputs/provenance.json`, and the per-case `inputs/` and `outputs/` files.
- Source captures are cited by path and sha256 in `outputs/provenance.json`:
  `.ufo/waves/round-81/capture/ds4cc-primary/response.json`, `.../ds4cc-sitemap/response.json`,
  `.ufo/waves/round-61/capture/burnerchrome-kimi/response.json`,
  `.../vault-index-kimi/response.json`, `.../charter-ghp/response.json`,
  `.../ufo-fsd-kimi-pro/response.json`.
