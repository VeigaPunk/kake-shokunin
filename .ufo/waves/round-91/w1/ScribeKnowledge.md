# Seat report — ScribeKnowledge (round 91, wave 1)

VERDICT: registry and knowledge changes land append-only and the census is clean (exit 0) — the
entry is written against `.ufo/waves/round-91/c2-contract.md` because `scripts/stored_reuse.py` was
present but **not yet a LANE commit** when I wrote it; this seat claims no `met` and scores no claim.

## 1. Source re-opened before quoting

Retained body: `.ufo/waves/round-91/L1/src/rfc9111.txt`, 84 477 bytes, sha256
`aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` — re-hashed by this seat, equal to
the digest in the item and in `freeze.md`.

```
$ sha256sum .ufo/waves/round-91/L1/src/rfc9111.txt
aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e  .ufo/waves/round-91/L1/src/rfc9111.txt
```

Sections located by plain-text line number: §5.2.1 heading 1111 (directive bodies 1113–1201), §4.2.1
heading 652 (lifetime rules 654–684), §4.2.4 heading 784 (stale rules 786–799); §1.2.2 delta-seconds
214–217 was read too because clause 4's bare-integer rule rests on it.

**20 quotes filed, 20 verified.** Each is a raw substring of the stated line and ≤14 words. The check
is mechanical, not by eye (`quote-check2.txt`, exit 0):

```
$ python3 - <<'EOF'
rfc = open(".ufo/waves/round-91/L1/src/rfc9111.txt").read().split("\n")
md  = open("corpus/knowledge/stored-response-reuse.md").read()
for n, q in QS:            # the 20 (line, quote) pairs filed in the entry
    assert q in rfc[n-1] and q in md and len(q.split()) <= 25
EOF
quotes=20 violations=0 []
```

Two-space sentence gaps are preserved verbatim (e.g. line 1113 `…directives.  They are advisory;`), so
each span is a byte-exact substring rather than a re-spaced rendering. One first-draft quote (line
1201, `504 (Gateway Timeout) status code.`) was broken across a markdown line wrap and failed the
check (`in_entry=False`); it was rewrapped onto one line and the check re-run clean. Recorded because a
wrapped quote is exactly the failure the round-55 ≤25-unit criterion is meant to catch.

## 2. `corpus/knowledge/stored-response-reuse.md` (new, 289 lines, sha256 `401108a3…6024f06`)

Opens with the lane's provenance trio plus `ground:`/`scope:`, matching `cache-current-age.md` and
`vary-matching.md`:

- `source:` S469 with the retained path, size and digest; names S461/S462/S463/S467 as distinct scopes.
- `verified-at:` what this seat actually did — located the quotes, read the contract, ran the tool for
  the checklist examples, ran its `--selftest`, ran the counter at HEAD, and did not score or commit.
- `recheck:` 180d with a concrete re-fetch instruction (URL, digest, three headings) and no ephemeral
  path.

Body covers what the item asked for:

1. **What it decides** — the seven-member vocabulary, `current_age = max(0, Age) + max(0, now − Date)`,
   and the first-match lifetime order (`s-maxage` shared → `max-age` → `Expires − Date` → `null`).
2. **What it refuses to decide** — no storage key / no Vary match (r88/r89 hold those), no revalidation
   exchange (§4.3), no heuristic freshness (§4.2.2; the answer is `heuristic-undecided`), no
   stale-serving permission without a client `max-stale`, no Date parsing, no clock, no network, no
   store, no live property claim.
3. **Decision table** — clauses 10–21 as one first-match table a publisher engineer can read, with the
   lifetime/age reporting per row, plus the two readings most often got wrong (request `max-age` is a
   client constraint, not the response lifetime; `must-revalidate` bites only when stale).
4. **Error patterns** — the five named shapes with the exact stderr text and exit code, each measured:
   `invalid_input: quoted delta-seconds argument: max-age`; `invalid_input: duplicate Cache-Control
   directive: max-age`; `invalid_input: duplicate header name: CACHE-CONTROL`; `invalid_input: stored
   response has no Date header`; `invalid_input: control character in header value: X-N`.
5. **Runnable checklist** — `python3 -B scripts/stored_reuse.py` with a literal input and its exact
   output, the serve-stale example, a refusal example, `--selftest`, the counter command with its
   expected `met=true` line, and the boundary reminder.
6. **Located quotes** — three tables (one per section) plus the §1.2.2 block, each with line numbers and
   word counts, followed by what each span grounds and what it does not.
7. **Adapter conventions and limits** — Date/Expires as integers, the chosen storable-status list, the
   duplicate refusals, `only-if-cached` reported as a decision not a 504, unclamped negative lifetime,
   and the statement that 45 + 120 cases are contract conformance, not RFC conformance.

### Measured receipts behind the checklist

```
$ printf '%s' '{"stored":{"status":200,"headers":{"Cache-Control":"max-age=60","Date":"1000000"}},"request":{"method":"GET"},"now":1000030}' \
  | python3 -B scripts/stored_reuse.py
{"decision": "reuse", "freshness_lifetime": 60, "current_age": 30}          exit=0   (ex1.txt)

$ printf '%s' '…{"Age":"-1"}…' | python3 -B scripts/stored_reuse.py
invalid_input: age must be nonnegative                                       exit=1   (ex2.txt)

$ TMPDIR=<scratch> python3 -B scripts/stored_reuse.py --selftest
selftest 45/45                                                              exit=0   (selftest.txt)
```

The nine additional probes (serve-stale, not-storable, heuristic-undecided, only-if-cached-miss, the
five refusal shapes, plus the contract probes below) are in `patterns.txt`, `patterns2.txt` and
`contract-probes.txt`. Candidate digest measured by this seat:
`5004657dbf2ae43399631f79e5d5955a8aa698b53f6127e22e2cc654ba9ad299`, equal to the digest
`ExecReuseTool` measured and to the counter's `candidate_sha256` in
`.ufo/waves/round-91/w1/ExecReuseTool/counter-final.txt`.

## 3. `corpus/SOURCES.md` — one appended row, S469

`S469` was free (the highest id at base is S468; `grep -c S469 corpus/SOURCES.md` was 0 before the
append). Eleven columns, inside `## Registry`, before `## Paths` — no existing row touched, no cell
rewritten:

```
| S469 | RFC 9111: HTTP Caching, section 5.2.1 Request Directives, section 4.2.1 Calculating Freshness
Lifetime and section 4.2.4 Serving Stale Responses — https://www.rfc-editor.org/rfc/rfc9111.txt |
spec | A | <scope: which directives constrain reuse, the first-match lifetime order, when stale is
forbidden or permitted; distinct from S461/S462/S463/S467> | <anchor: headings 1111/652/784, body
ranges 1113-1201/654-684/786-799, §1.2.2 214-217; retained path, 84477 bytes, sha256 aeb52adb…; opened
2026-11-04> | <teaches: advisory request directives; bare non-negative delta-seconds; first-match
lifetime; must-revalidate forbids stale, client max-stale permits it> | mined | 2026-11-04 | 180d |
corpus/knowledge/stored-response-reuse.md |
```

tier A / kind spec / status mined / recheck 180d, `used-by` naming the new entry only.

### Census

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
kake	W04	S469 duplicate url www.rfc-editor.org/rfc/rfc9111.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
exit=0
```

- **exit 0**, last line `kake ok /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`.
- No E codes (`grep -cE '\|E[0-9]{2}'` → 0).
- **W04 29 → 30.** The new warning is S469: it shares `https://www.rfc-editor.org/rfc/rfc9111.txt` with
  S467 (same URL, different section scope). The other 29 are unchanged — S461/S462/S463 use the
  `httpwg.org` host, so the new row does not add a second duplicate there. Before/after full outputs:
  `census-before.txt`, `census-after.txt`, counts in `census-counts.txt`.
- Rows `205 → 206` (the census's row counter is not printed in `validate` mode; counted with
  `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`).
- Re-run after all five files were in place (`census-final.txt`): identical output, **exit 0**, last
  line `kake ok …/corpus/SOURCES.md`, 30 × W04, 0 × E.

## 4. `corpus/README.md` and `PROVINCE.md`

- **Coverage-map row appended** after the r90 row (map table line 135):
  `| Stored-response reuse decision (may a stored copy be handed to this request; first-match freshness
  order; when a stale copy is served or refused) | r91 | knowledge/stored-response-reuse.md +
  scripts/stored_reuse.py | S469 |`. It satisfies the round-55 criterion (entry cell names
  `knowledge/<path>`, description shares "stored-response"/"reuse" with the file's head).
- **Frontier line appended** as `## Round-91 frontier step — the reuse decision`: the reuse decision
  moves from open ground to held bounded ground for supplied integer seconds only; storage key/Vary
  (r88/r89), age arithmetic (r87) and construction (r89/r90) stay with their rounds; open on this axis
  are §4.3, §4.2.2, stale serving without a client directive, field-specific normalisation and every
  live observation.
- **`PROVINCE.md` gains `## Round 91 — stored-response reuse decision only`** (25 lines, appended after
  the round-90 section): the seven decisions, the two arithmetic rules, the refusal contract, the
  frozen counter, and the boundary — no storage key, no revalidation exchange, no heuristic freshness,
  no live property claim, no publish or property repair.

## 5. `SKILL.md` — two registry rows in the existing 8-column shape

Appended as `## Round 91 — stored-response reuse decision` with header
`| Name | Kind | Entry command | Verdict map | Selftest | Pinned values | Write scope | Owner |`:

| Name | Kind | what the row pins |
|---|---|---|
| `stored_reuse` | probe | entry `printf … \| python3 -B scripts/stored_reuse.py`; verdicts 0 decided / 1 `invalid_input:` with empty stdout; selftest `selftest 45/45`; pinned `c2-contract.md` sha256 `faa91e09…` + candidate sha256 `5004657d…`; writes nothing |
| `c91 reuse capability` | gate | entry `c91_reuse.py --root . --revision <rev> --work <scratch> [--seed N] [--generated N]`; verdicts 0 met / 1 not met (failures, admitted forgery, `anti_table=hit`, `population=drift` named in the JSON line) / 2 unresolved revision or reference drift; selftest `selftest 45/45 hand cases, 120 generated, 7 decisions`; pinned `frozen/c2-population.sha256` sha256 `033b6103…` (five forgery subjects); `--work` scratch only |

The section closes with the two limits I want a later reader to carry: the gate scores the contract,
not the RFC, and `anti_table` is a substring screen (below).

## 6. Findings on the round's own instruments (reported, not edited)

**F1 — the tool was not committed when I started (state, not a defect).** `scripts/stored_reuse.py`
exists in the working tree (`5004657d…`) but no LANE commit contains it. The frozen counter at HEAD
therefore reads:

```
$ python3 -B .ufo/waves/round-91/c91_reuse.py --root . --revision HEAD --work <scratch> --seed 91091
C2v91 revision=f4fff130a52ae6de49af5de7d568d2ee320ebfb0 candidate=absent hand=0/45 generated=0/120 forgeries_refused=0/5 anti_table=n/a population=n/a seed=91091 met=false
{"reason": "candidate absent"}
exit=1
```

(`counter-at-head.txt`.) The entry is written against the contract and says so in `verified-at:`. The
`met=true` line belongs to the C2 seat (`w1/ExecReuseTool/counter-final.txt`, measured on its clone
commit `945aaca5…`); L1's re-run at the landing revision is what counts, and nothing in my files
asserts a score.

**F2 — the published `met` receipt pins a seed, so its generated population is precomputable.** The
counter's `--seed` defaults to `random.SystemRandom().randrange(...)`, but the C2 receipt used
`--seed 91091` and prints it. A candidate written after that receipt can answer the 120 generated
cases for that seed without implementing the contract; `anti_table` would not catch it, because the
screen covers hand-case input digests only. Recommendation for the landing run: use the default random
seed (or an unpublished one) so the `met=true` receipt is not a reproducible target. This is a property
of the evidence, not of the frozen predicate — no edit requested.

**F3 — `anti_table` is tuned to the sorted-form digest.** `c91_reuse.py` screens the candidate source
for `sha256(json.dumps(inp, sort_keys=True))[:16]`, and `frozen/make-neg-hash-table.py` builds the
frozen table forgery with exactly that normalisation. A table keyed on the raw stdin payload would
evade `anti_table`; the defence that actually holds is the seeded generated population (F2's caveat
applies). Worth stating in the registry row's neighbourhood — done, in the section's closing paragraph.

**F4 — the contract's input model cannot express two `Cache-Control` header lines.** A JSON object has
unique keys, and clause 1 refuses two names that differ only in case, so the RFC's duplicate-value
question (line 679: first occurrence *or* treat as stale) is exercised only *within* one comma list.
That is the same class as round-90 routed defect R90-5 (duplicate JSON members) and is not fixed by
contract v1.

**F5 — a repeated identical directive is accepted, and the contract does not say what it means.**
Measured: `Cache-Control: max-age=60, max-age=60` → `{"decision": "reuse", "freshness_lifetime": 60,
"current_age": 30}`, exit 0 (`contract-probes.txt`). Clause 4 refuses only "the same directive name
twice **with different arguments**", so this is contract-consistent; but "first occurrence wins" is
then an unstated assumption that happens to be invisible here (both arguments are equal). A future
contract revision should say which occurrence is read when arguments agree in value but differ in
spelling (`max-age=060`).

**F6 — clause 20 converts `heuristic-undecided` to `only-if-cached-miss`.** Measured: no lifetime
header + request `only-if-cached` → `{"decision": "only-if-cached-miss", "freshness_lifetime": null,
"current_age": 10}`, exit 0. Clause 20 excludes only `reuse` and `not-storable` from conversion, so this
is the contract's own reading; no hand case pins it and only the generated population reaches it.
`ExecReuseTool` reported the same care-point independently — agreement, not a new defect.

**F7 — the coverage map has no r87 or r88 row although both entries are held.** The map's preamble
says it holds "one row per `PROVINCE.md` §Frontier ground that a held entry can be dated to";
`knowledge/cache-current-age.md` (r87) and `knowledge/vary-matching.md` (r88) appear only in their
narrative sections (README lines 689–716), not in the table (lines 102–135, which jumps r83 → r89).
Pre-existing at base, outside this item's append-only scope: reported, not repaired.

**F8 — census sequencing constraint for scribes.** `E11` treats a `used-by` path missing on disk as an
error (exit 1), so the knowledge entry must exist *before* `validate` runs; an entry written after the
row would fail the census. Recorded because the natural order (row first, entry second) fails.

**F9 — cosmetic.** `c91_reuse.py` `score_subject` binds `i` in both `enumerate` loops and never uses it
(its own `idx`/`enumerate` counters do the work). No predicate impact; already reported by
`ExecReuseTool`, confirmed by reading lines 404–425.

**F10 — the frozen control runner and both pre-freeze control receipts were rewritten in the working
tree after the freeze.** Observed at the end of my seat, not my edit and not re-run by me
(`controls-drift.txt`, whole diff retained):

| file | state |
|---|---|
| `.ufo/waves/round-91/controls/run_controls.sh` | working tree sha256 `35703c8a…15495b`; committed at freeze `f4fff130` as `37d42f26…369970d`; mtime `2026-11-04 20:37:35 -0300`, i.e. after the freeze commit |
| `.ufo/waves/round-91/controls/ctl-c1.txt` | modified, mtime `20:37:41` |
| `.ufo/waves/round-91/controls/ctl-c2.txt` | modified, mtime `20:38:55`; its forgery lines now name fixture revision `c8526fd1f8bb34b865473064199b49c60298a70c` where the committed receipt names `eabbedb4f1695af612b03bb769995e89b99c0e5a` |

The diff changes the `reading()` helper from `grep … | tail -1` to `head -1 …` (a real fragility: a
later `met=` line in the same output file would be read as the verdict), adds exit-code checks, and
names the scratch directory with `$$`. Whether that is an authorized repair by L1 or a seat overstepping
is not mine to decide — but `freeze.md` §"Controls executed before this freeze" cites
`ctl-c1.txt`/`ctl-c2.txt` as evidence gathered *before* the freeze, and those files now hold a later
run. If the repaired bytes land, the freeze needs an explicit post-freeze amendment naming old and new
digests, or the pre-freeze control claim loses its standing.

**F11 — `freeze.md` pins round-90's runner digest but not its own runner's.** The freeze names
`sha256 00e339b8…` for `.ufo/waves/round-90/controls/run_controls.sh` (the C1 item-C script under test)
but records no digest for `.ufo/waves/round-91/controls/run_controls.sh`, the script that produced the
pre-freeze controls. That omission is exactly why F10 is undetectable from the freeze document alone: a
reader cannot tell whether the runner that produced `ctl-c1.txt`/`ctl-c2.txt` is the one on disk. The
freeze should pin every script it invokes, as it already pins its counters and the population file.

## 7. Files touched (all inside LANE, all additive)

| Path | Change | Evidence |
|---|---|---|
| `corpus/knowledge/stored-response-reuse.md` | new, 289 lines, sha256 `401108a34b362185fa2af7a4a24b9f953307954dd54d9b37fdd5df4606024f06` | §2 above |
| `corpus/SOURCES.md` | +1 line (S469), 0 deleted | `git diff --numstat` → `1 0` |
| `corpus/README.md` | +19 lines (map row + Frontier section), 0 deleted | `git diff --numstat` → `19 0` |
| `PROVINCE.md` | +25 lines (`## Round 91`), 0 deleted | `git diff --numstat` → `25 0` |
| `SKILL.md` | +26 lines (two registry rows + limits), 0 deleted | `git diff --numstat` → `26 0` |
| `.ufo/waves/round-91/w1/ScribeKnowledge.md` | this report | — |
| `.ufo/waves/round-91/w1/ScribeKnowledge/` | 14 receipts (see below) | — |

Nothing outside LANE was written; no frozen file, no `MANIFEST.json`, no `.ufo/state`, no `.scratch`, no
sibling lane, no fleet-root tracked file. No `git add/commit/stash/checkout/reset`, no `jj`. No
subagent. No tool install (python3 stdlib and coreutils sufficed; pacman untouched per the host-wide
pause). No network fetch — the retained body at the frozen digest was used, as the item directs.

Receipts in `.ufo/waves/round-91/w1/ScribeKnowledge/`: `ex1.txt`, `ex2.txt`, `patterns.txt`,
`patterns2.txt`, `contract-probes.txt`, `selftest.txt`, `counter-at-head.txt`, `counter-selftest.txt`,
`quote-check2.txt`, `census-before.txt`, `census-after.txt`, `census-counts.txt`, `census-final.txt`,
`controls-drift.txt` (F10/F11 evidence).

## 8. Honest limits

- This seat verified the entry's quotes, ran the probe for the checklist examples, and ran the counter
  at HEAD. It did **not** score C2, did not run the counter at a carrier (no commit contains the tool
  yet), and does not claim the tool is correct — that is `ReviewReuse`/`MutReuse`/`CriticClaims` and
  L1's landing run.
- The entry's decision table is a restatement of contract v1, checked against the contract text and
  against nine measured runs; it is not an independent reading of RFC 9111 and carries no RFC
  conformance claim.
- The census's W04 warnings are advisory and do not affect the exit code; the 30th is explained above.
- The scratch directory `/fast/scratch/hyaku/kake-r91/ScribeKnowledge` was deleted after the receipts
  were copied; nothing citable lives under `/tmp` or `/fast/scratch`.
