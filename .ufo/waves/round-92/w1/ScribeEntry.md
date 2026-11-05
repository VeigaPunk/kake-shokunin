# Seat report — ScribeEntry (round 92, wave 1)

VERDICT: the C2 knowledge entry lands with 32 mechanically verified located quotes and a validated S470 registry row draft — C2 is neither scored nor falsified by this seat; the instrument landed in the working tree mid-run and reproduces the entry's described behaviour on all seven worked examples.

## 1. The source, opened by this seat (not a retained copy)

```
$ curl -sS -o rfc9111.txt -w 'status=%{http_code} bytes=%{size_download} url=%{url_effective}\n' \
    https://www.rfc-editor.org/rfc/rfc9111.txt
status=200 bytes=84477 url=https://www.rfc-editor.org/rfc/rfc9111.txt
exit=0

$ sha256sum rfc9111.txt
aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e  rfc9111.txt
$ wc -c rfc9111.txt
84477 rfc9111.txt
UTC access date: 2026-11-05T00:30:25Z (local 2026-11-04T21:30:25-03)
```

This is a **live GET**, unlike round 91's row (which rested on a retained body — the K91-7 provenance gap). The fetched body is byte-identical to the lane's retained `.ufo/waves/round-92/L1/src/rfc9111.txt` (same sha256, same 84477 bytes), so every line number below is the same line number in the fetched body. Receipt: `w1/ScribeEntry/receipt.txt`.

**No other URL was fetched.** The RFC 9110 §15.1 quotes were read from the lane's retained `.ufo/waves/round-89/L1/src/rfc9110.txt` (502941 bytes, sha256 `21c1cdce…72332a`), re-hashed by this seat; the item authorised only the rfc9111.txt URL.

## 2. §4.2.2 located, and the four required quotes

Heading at plain-text line **686**; the section body runs 688-717.

| Required quote | Lines | Bytes (raw substring) |
|---|---|---|
| permission to assign a heuristic expiration time | 688-693 | `a cache MAY assign a heuristic expiration time when an explicit time` (689) |
| prohibition when an explicit expiration time is present | 695-696 | `A cache MUST NOT use heuristics to determine freshness when an` (695) |
| restriction to heuristically cacheable status codes or explicitly cacheable responses | 697-701 | `responses without explicit freshness whose status codes are defined` (698) … `explicitly cacheable (e.g., with a public response directive).` (701) |
| the fraction of the interval since Last-Modified, and the 10 % figure | 706-709 | `that is no more than some fraction of the interval since that time.` (708) … `A typical setting of this fraction might be 10%.` (709) |

**32 quotes filed, 32 verified, 0 violations.** Each is checked mechanically (not by eye) to be a raw substring of its stated line AND of the whole fetched body AND of the landed entry, and each is 3-25 words:

```
rfc9111_quotes=29 violations=0 []
rfc9110_quotes=3  violations=0 []
total_quotes=32 violations=0 []
```

The check and its full output: `w1/ScribeEntry/quotes.txt`.

## 3. `corpus/knowledge/heuristic-freshness.md` (new, 480 lines, 28848 bytes)

House form: `source:` / `verified-at:` / `recheck:` trio first, then `ground:` and `scope:` — matching `stored-response-reuse.md` and `cache-key-construction.md`. Body covers what the item asked for:

1. **The decision table**, contract clauses 9-13, first match wins, with `lifetime` and `heuristic` per row, and the three readings most easily got backwards (clause 10 outranks everything; clause 11 is an `and` so `public` opens the gate alone; clause 13 is a decline, not a failure).
2. **The two lane conventions marked as conventions**, with the source sentences that make them conventions: the 10 % fraction (the RFC says "encouraged", line 707, and "typical", line 709) and the 86400-second cap (the RFC names no cap and no interval; lines 692-693 say it "does not provide specific algorithms" and imposes only "worst-case constraints" in general terms). Neither is presented as spec text.
3. **The composition with `scripts/stored_reuse.py`** — a table of the two tools' questions, vocabularies, outputs and inputs, plus two cautions a reader must carry: the r91 `heuristic-undecided` is *broader* than the r92 one (r91 fires whenever no explicit lifetime exists; r92 subdivides that into `heuristic` / `not-heuristically-cacheable` / `heuristic-undecided`), and the two storability rules are not the same rule (a response r91 calls `not-storable` may still get a r92 `heuristic` verdict — measured, `w1/ScribeEntry/composition.txt`). Stated explicitly that neither tool calls the other and that no code path exists (`grep -rn "heuristic_freshness" scripts/` → no hits).
4. **A "What this does not claim" paragraph** — no live cache, no storage, no revalidation, no browser behaviour, each with what it would take instead.
5. **Adapter conventions** the source does not require: epoch-second dates with `Date` required; the twelve codes read from RFC 9110 §15.1; the interval measured to `Date` (so `now` is validated but unread by any decision clause); the `not-storable` gate narrowed to three conditions rather than §3's full list; `Vary: *` read as a storability bar; qualified `private` treated like unqualified.
6. **A runnable checklist** — the seven worked examples with their exact measured output and exit status, the tool's `--selftest`, and the frozen counter's command with its expected `met=true` line and its `candidate=absent` reading before the tool is committed.

## 4. The instrument, measured after it landed

`scripts/heuristic_freshness.py` appeared in the lane **working tree** at 21:40 local, while this seat was writing the entry (sha256 `7bfe82da…d2f37f5c` at that moment). `git log --oneline -1 -- scripts/heuristic_freshness.py` printed nothing — no LANE commit contained it when this seat measured it. This seat did not write it and did not modify it.

All seven checklist examples reproduce the described behaviour, and the eight refusal shapes carry the exact stderr strings now quoted in the entry:

```
{"decision": "heuristic", "heuristic": true, "lifetime": 1000}          exit=0
{"decision": "heuristic", "heuristic": true, "lifetime": 86400}          exit=0
{"decision": "explicit", "heuristic": false, "lifetime": 600}           exit=0
{"decision": "not-heuristically-cacheable", "heuristic": false, "lifetime": null}  exit=0
{"decision": "heuristic", "heuristic": true, "lifetime": 1000}          exit=0   (500 + public)
{"decision": "heuristic-undecided", "heuristic": false, "lifetime": null} exit=0
invalid_input: Date is absent                                             exit=1   (stdout empty)
selftest 54/54                                                            exit=0
```

Transcripts: `w1/ScribeEntry/instrument-probes.txt`, `w1/ScribeEntry/refusal-probes.txt`.

## 5. `corpus/SOURCES.md` — the row is **drafted, not appended**

`corpus/SOURCES.md` was **not edited** by this seat (the L1 appends it). `git diff --numstat -- corpus/SOURCES.md` is empty. The draft is one line at `w1/ScribeEntry/sources-row.md`:

- id **S470** — next unused after S469 (highest id in the registry); `grep -cE '^\| S470' corpus/SOURCES.md` → 0 before the draft. No existing row covers RFC 9111 §4.2.2: the only `4.2.2` hits in the registry are S028, which is **RFC 9110**'s URI-scheme section — a different document, section and topic.
- kind `spec`, tier `A`, status `mined`, recheck `180d`, opened `2026-11-04`, used-by `corpus/knowledge/heuristic-freshness.md`.
- anchor: §4.2.2 heading line 686, permission 688-693, prohibition 695-696, restriction 697-701, fraction/10 % 706-709, June 2022, fetched 2026-11-05T00:30:25Z HTTP 200 84477 bytes sha256 `aeb52adb…5302cf3e`, retained `.ufo/waves/round-92/L1/src/rfc9111.txt`.
- `teaches`: one grounded cell — the four rules, in the source's own words, including that 10 % is *typical*, not required.

**The drafted row was validated without touching the lane.** It was inserted into a scratch copy of the registry and validated against a scratch mirror whose `corpus/knowledge`, `corpus/lessons`, `SKILL.md`, `SCORECARD.md`, `PROVINCE.md` and `scripts/` are symlinks to the real lane, so the `used-by` existence check (E11) resolves against the real tree:

```
$ scripts/sources-census.sh validate --file <scratch-mirror>/corpus/SOURCES.md \
    --root /home/vgpnk/Projects/shokunin --today 2026-11-04
file	W04	S470 duplicate url www.rfc-editor.org/rfc/rfc9111.txt across scopes
file	ok	<scratch-mirror>/corpus/SOURCES.md
exit=0 (no E codes)
```

Baseline (lane as it stands): `kake ok …/corpus/SOURCES.md`, exit 0, 29 × W04. With the draft: exit 0, no E codes, one **additional advisory** W04 (the same URL is already carried by S467 and S469 on different sections; W04 does not change the exit code). Row count 206 → 207 with the append. Receipt: `w1/ScribeEntry/census-draft.txt`.

## 6. Findings (reported, not edited)

**F1 — the contract's `now` is required but read by no decision clause.** The C2 contract's input section makes `now` a mandatory key and clause 3 validates it (`now` an int ≥ 0), but clauses 9-13 never use it: the heuristic lifetime is `Date − Last-Modified`, and `now` does not enter the `explicit`, `not-storable`, `not-heuristically-cacheable` or `heuristic-undecided` verdicts either. Measured on the landed instrument: `now` = 0, 1000000 and 999999999 give byte-identical output, while omitting it is a refusal (`invalid_input: now is not a non-negative int`, exit 1). So the contract makes a caller supply a value it then ignores — defensible as a stable input shape, but a reader of the contract alone would reasonably expect `now` to matter. **Routing question for the L1: is the clause-3 requirement of `now` intended, and if so should the contract say explicitly that the decision is `now`-invariant?** The entry states the invariance as an adapter convention, not as a defect, because it is observable and consistent.

**F2 — the contract's clause 9 is stricter than RFC 9111 §3 on qualified `private`.** Clause 9 refuses `not-storable` whenever the stored Cache-Control carries `private` and the cache is shared. RFC 9111 §5.2.2.7 (lines 1327-1338) distinguishes the unqualified form ("a shared cache MUST NOT store the response") from the qualified form (`private="Set-Cookie"`), where only the listed fields are limited to one user; and §3's own rule (lines 297-299) admits a private directive that "allows a shared cache to store a modified response". Measured on the landed instrument: `Cache-Control: private="Set-Cookie"` on a shared cache → `not-storable`. **This is a lane convention that is stricter than the RFC, not a misreading of §4.2.2** — §4.2.2 does not speak to `private` at all. The entry names it as an adapter convention so it is not mistaken for spec text. No change requested to the frozen contract.

**F3 — the counter's `--seed` default is 92 and is printed in the `met` line.** `c92_heuristic.py` takes `--seed` (default 92) and prints `seed=92` in its verdict line, so the 120-case generated population is precomputable by anyone who reads the frozen counter — the same class of weakness round 91's scribe filed as F2 for `c91_reuse.py` (K91-6's cousin). `anti_table` screens the candidate source for the hand-case input digests and the forgery stems only, so a candidate that memorises the seed-92 population's expected outputs is not caught by that conjunct. This is a property of the *evidence*, not of the frozen predicate, and the counter is frozen — reported for the round's routed list, not repaired here.

**F4 — the counter's anti-table screen is a substring screen over the candidate source.** `anti_table` looks for `sha256(json.dumps(inp, sort_keys=True))[:16]` and the forgery stems. A candidate that hard-codes a lookup table keyed on something other than the sorted-form digest (for instance the raw stdin bytes) evades it; the defence that actually holds is the generated population, subject to F3. Same observation round 91 filed (its F3). Reported, not repaired.

**F5 — the tool's `--selftest` population (54) is not the counter's population (28 hand + 120 generated).** Both numbers are "the fixtures", and a reader could compare them as if they measured the same thing. The entry says explicitly that the two are different populations and the numbers are not comparable.

**F6 — the counter's reference self-check is a real defence, and it is worth stating.** `c92_heuristic.py` runs its own `reference()` against all 28 hand cases *before* it scores any candidate and exits 2 with the drifting case named if they disagree, so a contract drift cannot pass silently. This is a stronger shape than round 91's `c91_reuse.py`. Recorded as an observation, not a defect.

**F7 — the lane's knowledge-entry count and the registry count move with this round.** `corpus/knowledge/*.md` 79 → 80 with this entry; `corpus/SOURCES.md` 206 → 207 with the L1's append of S470. Both counts are the L1's to state in `SCORECARD.md`; this seat states them here so the numbers are not lost.

## 7. Files touched (all inside LANE, all additive)

| Path | Change |
|---|---|
| `corpus/knowledge/heuristic-freshness.md` | new, 480 lines, 28848 bytes |
| `.ufo/waves/round-92/w1/ScribeEntry/quotes.txt` | new — the 32 quotes, their lines, and the mechanical check |
| `.ufo/waves/round-92/w1/ScribeEntry/receipt.txt` | new — the GET record, digests, section location, file list, limits |
| `.ufo/waves/round-92/w1/ScribeEntry/sources-row.md` | new — the S470 row draft and the L1's append constraints |
| `.ufo/waves/round-92/w1/ScribeEntry/refprobe.txt` | new — the frozen counter's reference exercised over its 28 hand cases |
| `.ufo/waves/round-92/w1/ScribeEntry/composition.txt` | new — r91 vs r92 measured side by side |
| `.ufo/waves/round-92/w1/ScribeEntry/census-draft.txt` | new — baseline and with-draft census |
| `.ufo/waves/round-92/w1/ScribeEntry/instrument-probes.txt` | new — the seven worked examples |
| `.ufo/waves/round-92/w1/ScribeEntry/refusal-probes.txt` | new — the eight refusal shapes |
| `.ufo/waves/round-92/w1/ScribeEntry.md` | this report |

**Not touched:** `corpus/SOURCES.md` (L1 appends), `corpus/README.md`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, every frozen file (`.ufo/waves/round-92/c92_defects.py`, `c92_heuristic.py`, `c2-contract.md`, `frozen/`, `controls/`), `scripts/heuristic_freshness.py` (the executor seat's), the fleet root, `MANIFEST.json`, `.ufo/state`, `.scratch`, the fleet templates and scripts, any sibling lane, `/home/vgpnk/Projects/shokuknow`.

**No git mutation of any kind in LANE** — no `git add`, `commit`, `stash`, `checkout`, `switch`, `reset`, `pull`, `push`, and no `jj` command. No fixture repo was needed (the census check was done on scratch copies and symlinks, not on a clone).

## 8. Honest limits

- **This seat scored nothing.** It did not run the frozen counter `c92_heuristic.py` against a carrier, did not claim or deny `met`, and did not write the instrument. The L1's landing run is what decides C2.
- **The entry's decision table is a restatement of contract v1**, checked against the contract text and against the counter's own reference implementation and the landed instrument's observed behaviour — it is not an independent reading of RFC 9111 and carries no RFC conformance claim.
- **The 120 generated cases are the reference's own outputs**; agreement there is not independent evidence. The entry says so.
- **The RFC 9110 §15.1 quotes were read from a retained body, not re-fetched**, because the item authorised only the rfc9111.txt URL. The entry and the receipt both say so.
- **The instrument measurements are working-tree observations.** No LANE commit contained `scripts/heuristic_freshness.py` when this seat measured it; the L1's commit may carry different bytes.
- **One advisory W04 is expected** when the S470 row lands (same URL, different section scope, as with S467 and S469). It does not change the census exit code.
- **Tooling:** no tool was installed or upgraded — python3's standard library and coreutils sufficed. `pacman` was untouched per the host-wide pause.
- **Scratch:** `/fast/scratch/hyaku/kake-r92/ScribeEntry/` was created by this seat, holds the fetched body and the probe outputs, and was deleted after the receipts were copied into this wave directory. A `/tmp` or `/fast/scratch` path is never citable evidence; cite `w1/ScribeEntry/`.
