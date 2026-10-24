# ScoutCorpusStale — round 38 freshness of the lane's robots statements

Axes: freshness (primary), operability. Read-only lane; head `2dab7f31`, claim base `af43a50f`. Sealed key and both sealed trees not accessed; round-38 counters not run; no network, no installs.

## Measured base behavior (the three readings; tool `944d2f51f396…`)

Clone at `af43a50f`; probes in `/fast/scratch/hyaku/kake-r38w1/ScoutCorpusStale/probe/`; each run `python3 -B scripts/robots_audit.py --manifest <probe>`:

| probe | exit | observed | rule that changes it |
|---|---|---|---|
| `note: NaN` (unused member) | 0 | `clean`, evaluated 1 | (h) → one `input_invalid`, nothing evaluated |
| `robotsStatus: NaN` | 2 | `check_invalid` c1, evaluated 0 | (h) → `input_invalid` null, nothing evaluated |
| 5000-digit unused integer | 2 | `input_invalid` null | (h) → changes nothing |
| 5000-digit `robotsStatus` | 2 | `input_invalid` null | (h) → `check_invalid` that check, others evaluated |
| URL leading space / U+0001 / `"` | 0 | `clean`, evaluated 1 | (i) → `check_invalid` |
| `/robots%2Etxt`, `Disallow: /`, expect allow | 1 | `blocked` | (k) → `clean` (normalized path) |
| `/robots.txt?x=1`, expect allow | 1 | `blocked` | none: (k) keeps it rules-decided |
| `/robots.txt`, expect allow | 0 | `clean` | none |
| base selftest | 0 | `137/137`, `cases: 137` (3.3 s) | harm instrument holds |

Mechanism in base bytes: `json.loads` accepts `NaN` and raises `ValueError` above 4300 integer digits (verified: 4300 ok, 4301 `Exceeds the limit`), which `load_manifest` turns into `input_invalid`; `urlsplit` strips leading space/control and accepts the rest; the implicit allow compares `IMPLICIT_ALLOWED_PATH` to the raw path.

## Sentences needing an append-only correction (digests at `2dab7f31`)

1. `corpus/knowledge/robots-txt-rules.md:57` (`77d6f56c…`) — implicit allow limited to "when the file decides access (status 2xx)", citing (a) and (e). Silent on the path compared; (k) decides it on the normalized path: `/robots%2Etxt` and `/%72obots.txt` allowed; `/robots.txt?x=1`, `/ROBOTS.TXT`, `/robots%2Ftxt` rules-decided; `/robots.txt?` allowed; explicit `Disallow: /robots.txt` does not override. **Append only** (incomplete, not false; same reading as `w1/ScribeKnowledgeEntry.md:9`).
2. `robots-txt-rules.md:67` — "with an absolute http(s) URL" is the whole URL rule. (i) adds a character check judged as written: ASCII outside the RFC 3986 set (space, U+0000–001F, U+007F, `"` `<` `>` `\` `^` `` ` `` `{` `|` `}`) anywhere → `check_invalid`; non-ASCII kept; `%` without two hex digits allowed. **Append**, cite S029/S089 RFC 3986 §2 and SCORECARD C2 (i).
3. `robots-txt-rules.md:71` — "malformed manifest/check input is a failure to evaluate" cites only (f)/(g). (h) adds `NaN`/`Infinity`/`-Infinity` anywhere → one `input_invalid`; integers of any length are JSON; out-of-range status → `check_invalid`; unused long numbers change nothing; `1e400` stays a float. **Append**, cite S034 RFC 8259 §6 and C2 (h).
4. `robots-txt-rules.md:1-2` — `source:`/`verified-at:` list S011/S095/S096 only; the (h)/(i) readings need S034 and RFC 3986 §2 (re-opened this round). **Append a "Round-38 source recheck" tail** (pattern `corpus/knowledge/crawl-scope-per-host.md:47-57`), not a header rewrite (`corpus/QUALITY.md:31-39`).
5. `robots-txt-rules.md:11` and `:83` — both call the "Round 37 — declared claims" C1 contract "the contract". After the build it is round 37 as amended by C2 (h)/(i)/(k). **Append one pointer** covering both; keep :83's evidence boundary.
6. `SKILL.md:1083-1086` — registry says "round-37 C1" and "The contract is SCORECARD 'Round 37 — declared claims'". **Append** a note naming the round-38 amendments as the current contract for (h)/(i)/(k) and the v3 counter (`sealed_count_v3.py`, `met: passed >= 20 of 20`).
7. `SKILL.md:1092` — proof cell pins the round-37 counter (`key 424aa248`, `>= 25 of 28`) as the gate's "frozen proof" and says it "does not separate the contract from the stock Python parser; the selftest does". Defects: no `not admitted` status, no v3 counter; and the parenthetical is inaccurate — stock `urllib.robotparser` scored 20/28, met false (`verification/control-CtlC1NaiveReader.json`, passed 20), while the 28/28 control was stdlib-plus-six-patches (`SCORECARD.md:198` tail). **Append correction**; the r37 counter stays round 37's rule of record. "137 fixtures" is accurate now, but changes when the selftest lands.
8. `PROVINCE.md:297-305` — cites "Round-37 C1 contract" only; no `not admitted`, no (h)/(i)/(k). **Append** the round-38 step (ScribeProvinceStep draft); leave :297-305 byte-identical.
9. `corpus/README.md:362-368` — "Coverage — round 37" presents the r37 contract as current; no `not admitted`, no (h)/(i)/(k). **Append** a round-38 coverage block (same draft).
10. `corpus/lessons/round-37-verifier-spotcheck.md:149-151` — item 6 lists "robots `NaN`/malformed URLs" as open; these are exactly (h)/(i). **Append a status note** (claimed by C2, open until measurement).
11. `round-37-verifier-spotcheck.md:141-143` — item 2 asks for a counter redesign; C2 v3 is it. **Append a status note**; do not rewrite.

## Sentences that do NOT exist (do not hunt for them)

- No target sentence states the raw-path implicit allow, `NaN` acceptance or `urlsplit` stripping. `grep -nE 'NaN|Infinity|urlsplit'` over the five targets: only `SKILL.md:776-777` (source_recheck's own JSON policy, a different tool) and the lesson's open-item line above.
- The raw-path statement is code only: `scripts/robots_audit.py` docstring lines 47-49 at `af43a50f` ("compared on the raw path-to-match, before normalization"), plus round-37 wave reports. ExecRobotsTool replaces it; no prose correction is owed.
- No target sentence claims round-37 admission outright: `round-37-verifier-spotcheck.md:75` says "Not admitted" and `SCORECARD.md:198` carries "**not admitted** (round-37 closure …)". The exposure is framing (items 6–9), not an explicit admission claim.

## Harm-instrument compatibility (checked, not the claim)

`python3 -B scripts/robots_audit_selftest.py` at `af43a50f` → exit 0, 137/137. The 45 URL literals contain no excluded ASCII character; no `NaN`/`Infinity` fixture; the only implicit-allow fixtures are `e11` (mixed-case `/Robots.txt`, blocked) and `e12` (raw `/robots.txt` with `Disallow: /`, clean), both still correct under (k). (h)/(i)/(k) do not break the 137.

## Not verified

The (h) 64 MiB-of-digits / 20 s bound; the C2 build and v3 counter (no key; not my seat); when the L1 appends these corrections. This seat edited no prose; drafts belong to the scribes.
