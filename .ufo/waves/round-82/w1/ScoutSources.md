# ScoutSources — round 82 wave w1

**Seat:** scout, leaf (no subagent dispatch). **Write scope:** this report plus
`.ufo/waves/round-82/w1/ScoutSources/` only — no production file, `corpus/SOURCES.md` untouched by this
seat, nothing staged or committed.

## Verdict

One GET of `https://www.rfc-editor.org/rfc/rfc9110.txt` at 2026-11-04T12:51:57Z returned HTTP/2 200, final
URL identical, 502,941 bytes, sha256 `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` —
**byte-identical** to `corpus/lessons/round-81-gate/rfc9110.txt` (`cmp -s` exit 0) and to
`corpus/lessons/round-81.md` §Gate. §8.8.3 sits at `:3570`, its strong-validator statement imports §8.8.1
`:3403-3405`, and a 24-word raw-substring quote verifies at `:3572-3574`. S455 has since landed at
`corpus/SOURCES.md:202` as a congruent variant; the registry validates `ok` at `W04=22`.

## 1. Fetch receipt

Exactly **one** GET: no body, no credentials, no cookie jar (`-c`/`-b` absent — the answer carried
`set-cookie: __cf_bm=…`, neither retained nor resent). User agent `kake-shokunin/round-82 w1 ScoutSources
(…; contact: lane operator)`.

```
$ curl -sSL --max-time 90 -A 'kake-shokunin/round-82 w1 ScoutSources (…)' \
       -o rfc9110.txt -D rfc9110.headers \
       -w 'http_status=%{http_code}\nfinal_url=%{url_effective}\nbytes=%{size_download}\n' \
       https://www.rfc-editor.org/rfc/rfc9110.txt
http_status=200
final_url=https://www.rfc-editor.org/rfc/rfc9110.txt
bytes=502941
exit=0
```

| field | value |
|---|---|
| requested = final URL | `https://www.rfc-editor.org/rfc/rfc9110.txt` (no redirect) |
| HTTP status | `HTTP/2 200` |
| fetched-at (UTC) | `2026-11-04T12:51:57Z` — the server `date:` header, equal to the local `date -u` printed right after the command; no pre-request timestamp was captured, so the instant rests on those two clocks |
| byte count | 502,941 |
| sha256 / headers sha256 | `21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a` / `606d5ce783832f67b35fed0dc34504fa0f01de11914f1607983665d0ed489d45` |
| `etag` / `last-modified` | `W/"7c9fc097e78bd883e559172c885e074c"` (weak) / absent |

```
$ sha256sum <new body>; sha256sum corpus/lessons/round-81-gate/rfc9110.txt    (both exit 0)
21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a  <new body>
21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a  <round-81 retained>
$ cmp -s <new body> <round-81 retained> && echo identical   →  identical   exit=0
```

§Gate carries the same digest and the same 502,941 bytes (its `200 139493` stdout is the `--compressed`
transfer size, not the body size). **The body is byte-identical.** Four fetches now share one digest:
S453's row (10:44:53Z), the round-81 sources seat (11:46:19Z), the round-81 gate (11:46:55Z) and this one
(12:51:57Z).

## 2. §8.8.3 location, spans, and the strong-validator reading

Headings: `8.8.1.  Weak versus Strong` `:3393`, `8.8.2.  Last-Modified` `:3480`, **`8.8.3.  ETag`
`:3570`**, `8.8.3.1.  Generation` `:3619`, `8.8.3.2.  Comparison` `:3643`, `8.8.3.3.  Example…` `:3672`;
§8.8.3 ends at `:3724` and `9.  Methods` begins at `:3726`. Definitional spans: `:3572-3580` (`ETag` field
+ entity-tag definition), `:3582-3588` (ABNF), `:3590-3593` (RFC 2616 note), `:3595-3599` (tag vs
modification date), `:3601-3605` (examples), `:3607-3612` (strong is the default; a tag failing any §8.8.1
strong characteristic MUST be marked weak), `:3614-3617` (trailer placement).

**On a strong validator and a change in the representation data, §8.8.3 restates nothing — it imports.**
`:3609-3611` cites "all of the characteristics of a strong validator (Section 8.8.1)", so the substantive
sentence is §8.8.1 `:3403-3405`: a strong validator is representation metadata that changes value whenever
a change occurs to the representation data that would be observable in the content of a 200 (OK) response
to GET. §8.8.3 adds the operational half: strong by default (`:3607-3608`), a non-conforming tag MUST be
marked `W/` (`:3608-3612`), strong comparison needs **both** tags non-weak (`:3648-3649`). The weak half
is §8.8.1 `:3438-3444` — a weak validator "might not change for every change to the representation data",
so equal weak tags do not establish equal bytes. `:3446-3450` (SHOULD change a weak tag) is cache
invalidation, outside this row's scope.

Quotes, all classes machine-checked (`receipts/quote_check.py` → `receipts/quote_check.txt`, `python3 -B`,
exit 0; `raw` = exact substring). Fenced blocks reproduce the source's own line breaks and 3-space
continuation margin.

**Primary — 24 words, `raw=True`, `:3572-3574`** (the substring starts mid-line, so line 1 carries
no leading margin):
```text
The "ETag" field in a response provides the current entity tag for
   the selected representation, as determined at the conclusion of
   handling the request.
```

**Strong-validator fragment — 16 words, `raw=True`, `:3403-3404`:**
```text
representation metadata that changes value
   whenever a change occurs to the representation data that would be
```

Its first line alone is raw at `:3403` (9 words): `A "strong validator" is representation metadata that
changes value`. **The whole definitional sentence has no raw span**: `:3403-3405` is 31 words (over the
cap) and **collapsed-only** — with single spaces the script reports `raw=False`, the wrap inserting `\n
` between "value" and "whenever". Collapsed span: "A "strong validator" is representation metadata that
changes value whenever a change occurs to the representation data that would be observable in the content
of a 200 (OK) response to GET."

**Weak-validator definition — 17 words, `raw=True`, `:3438-3439`:**
```text
a "weak validator" is representation metadata that might
   not change for every change to the representation data.
```

Field observation for C2's method (not a claim about any other surface): this origin answers with a
**weak** ETag, and the round-81 sources seat recorded the same `W/"7c9fc097…e074c"` at 11:46:19Z with the
same body digest. A weak tag constant across two captures is consistent with identical bytes and, per
`:3438-3439`, also with changed bytes — an ETag-equality test cannot carry body-identity evidence here;
the sha256 of the retained body can.

## 3. S455 — proposed registry row

Proposed insertion point at proposal time: **after line 201** of `corpus/SOURCES.md` (last registry row
`S454`; 202 blank; 203 opened `## Paths`). Eleven cells, no literal `|` inside a cell (NF=13 verified).
This seat writes no registry byte.

```
| S455 | RFC 9110: HTTP Semantics, §8.8.1 Weak versus Strong and §8.8.3 ETag — https://www.rfc-editor.org/rfc/rfc9110.txt | spec | A | What a strong validator guarantees about a change in representation data (it changes value whenever a change to that data would be observable in a 200 (OK) response to GET) and what a weak validator does not guarantee (it might not change for every such change, so equal weak tags do not imply equal bytes); not cache freshness, not conditional-request evaluation or when a weak validator may be used as a precondition, not the ETag trailer placement, not any lane's capture, digest or drift property | §8.8.1 strong-validator definition lines 3403-3405 and weak-validator definition lines 3438-3444, §8.8.3 ETag lines 3570-3617 (grammar 3582-3588, strong-default rule 3607-3612), §8.8.3.2 comparison lines 3643-3653, of the retained plain text; June 2022; HTTP 200 at 2026-11-04T12:51:57Z, final URL identical, 502,941 bytes, retained text sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a | A strong validator changes value whenever a change to the representation data would be observable in a 200 (OK) response to GET, so an unchanged strong tag rules out such a change; a weak validator might not change for every such change, so an equal weak tag carries no such guarantee | mined | 2026-11-04 | 365d | corpus/knowledge/capture-drift-validators.md, corpus/lessons/round-82.md |
```

Cell checks (`python3 -B`, 13 fields / 11 cells, `ALL=True`): id `S455` matches `S[0-9]{3,}`; kind `spec`;
tier `A`; status `mined`; `opened` a past ISO date; `recheck` `NNd`; anchor names both sections, the line
numbers and the 64-hex digest; `used-by` names exactly the two artifacts this round adds —
`corpus/knowledge/capture-drift-validators.md` (ScribeKnowledge target) and `corpus/lessons/round-82.md`
(ScribeLesson target). Neither existed at the census run below, so `E11` read "missing used-by".

Shape test against the **fleet** census (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`,
read-only, unmodified):

```
$ sources-census.sh validate --root <lane> --file <lane>/corpus/SOURCES.md --today 2026-11-04
ok  …/corpus/SOURCES.md                     exit=0   W04=21
$ sources-census.sh validate --root <lane> --file <scratch>/SOURCES-S455-inserted.md --today 2026-11-04
E11=256  W04=22                             exit=1
$ sources-census.sh validate --root <lane> --file <lane>/corpus/SOURCES.md --today 2026-11-04   # later, S455 landed
ok  …/corpus/SOURCES.md                     exit=0   W04=22
```

Differential: **+1 `W04`** (S455 shares `www.rfc-editor.org/rfc/rfc9110.txt`, the 22nd such warning), no
`E01`–`E10`, no `E12`, no `E04`. The 256 `E11` lines are the `--file`-mode defect (below), not a finding
about this row — they start at `S001` and cover every row's `used-by`.

**Landed variant, cell-diffed** (`corpus/SOURCES.md:202`, ScribeKnowledge's write, not this seat's): `id`,
`source`, `kind`, `tier`, `status`, `opened`, `recheck` identical; `scope`, `anchor`, `teaches`, `used-by`
differ. Congruent on every fact verified here — strong definition `3403-3405`, weak `3438-3439`, `§8.8.3`
`3570-3617`, the `W/` rule `3607-3612`, strong comparison `3648-3649`, digest `21c1cdce…47232a`. Its
anchor cites the round-81 retained copy as byte source; §1's fetch re-derives that digest at 12:51:57Z and
§1's `cmp -s` shows the copies are the same bytes, so the landed line numbers hold for both.

**Overlap with the four existing RFC 9110 `.txt` rows.** `S028` (URI schemes, empty host), `S033` (media
types, same chapter 8 but a different field), `S453` (dates/field values, adjacent only), `S454` (404/410
statuses) — none reads §8.8. All four share the URL, hence the extra `W04`; `E04` (duplicate URL **and**
scope) cannot fire because every scope cell differs.

**Sharpest overlap is `S010`, a `.html` row** (`corpus/SOURCES.md:18`, §8.8.1 + §8.8.3, teaching "a strong
validator can change for metadata reasons without representation-data changes"). S455 is the same sections
in the other format, so distinctness is narrow: S010 states the metadata-direction implication, S455 the
representation-data-direction guarantee and the weak-validator non-guarantee, quoting a different sentence
with plain-text line numbers — what `corpus/QUALITY.md:212-214` requires ("Formats of one document (RFC
9110 html/txt) may share text but need distinct quotes"). If a later census treats section overlap as
fatal, **S455 is the row to withdraw**; S010 stays untouched, as round-81 recorded for S454 against S088.

## 4. Search log line

Round 82 bounded question (2026-11-04): what does RFC 9110 say about a strong validator's relation to a
change in the representation data, and what a weak validator does not guarantee, for a capture-to-capture
drift gate that compares retained bodies? Opened the RFC Editor plain text exactly once
(`https://www.rfc-editor.org/rfc/rfc9110.txt`, HTTP 200, 502,941 bytes, sha256 `21c1cdce…47232a`) and
searched §8.8.1 and §8.8.3 at verified line numbers. Identified 2 candidate sections in 1 primary
document, screened 2, included 1 registry row (S455, whose anchor carries both sections), excluded 0
registry candidates; S010 (HTML, same sections), S028, S033, S453, S454 and S433 were read as overlap, not
as candidates. Stop: both definitions and the strong-default rule have direct primary text at
machine-verified lines; freshness, conditional-request evaluation and capture mechanics belong to other
rows or to the lane, so no further source was opened.

## 5. Commands, limits, cleanup

| command | exit |
|---|---|
| `curl -sSL --max-time 90 … -o rfc9110.txt -D rfc9110.headers -w …` (one GET) | 0 (200, 502,941 B) |
| `sha256sum` new body and round-81 retained body; `cmp -s` the two | 0, 0, 0 (digests equal, identical) |
| `python3 -B receipts/quote_check.py`; report-quote re-check | 0, 0 (`raw=True` for all three blocks) |
| `sources-census.sh validate --root <lane> --file <lane>/corpus/SOURCES.md` | 0 (`ok`, W04=21) |
| `sources-census.sh validate --root <lane> --file <scratch>/SOURCES-S455-inserted.md` | 1 (E11=256, W04=22) |
| `sources-census.sh validate --root <lane> --file <lane>/corpus/SOURCES.md` (S455 landed) | 0 (`ok`, W04=22) |

Limits: one document, one GET, nothing re-run to "confirm" a digest. No tool installed or upgraded (none
needed). No network beyond the one declared URL. This reading decides the strong/weak validator statement
only — not freshness semantics, not conditional-request rules, not any lane property; the contract's C2
predicate is untouched.

**Routed, not repaired** (all outside this seat's write scope):

1. `sources-census.sh --file` resolves `used-by` from the **registry file's own location**, not
   `--root`: the canonical file exits 0 under `--root /tmp`, while the same bytes copied outside
   the lane exit 1 with 256 `E11` starting at `S001`. `--root` must still *name* a directory
   (`/nonexistent` → exit 2), so it is validated then unused. Round-81 §Gate recorded 252. Fleet
   file, read-only to this seat; receipts `tA.out`–`tD.out`.
2. `rfc-editor.org` answers `rfc9110.txt` with a **weak** ETag and no `Last-Modified`, so
   body-identity on this surface must rest on the digest (see §2).
3. `corpus/SOURCES.md` moved under this seat's feet (ScribeKnowledge inserted `:202` while the
   report was being written). Not a conflict — the row is congruent and the cell diff is recorded
   above; this seat wrote none of it.

Scratch `/fast/scratch/hyaku/kake-r82/ScoutSources/` was created with `mkdir -p`, passed explicitly, and
is removed before yield; receipts were copied into `.ufo/waves/round-82/w1/ScoutSources/receipts/` first.
