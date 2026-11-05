# Round-92 mutation test — C2 instrument and C2 counter (seat MutHeuristic)

VERDICT: C2's frozen counter does not establish conformance to contract v1 — 13 of 24
single-clause tool mutants survive it, and 9 hand-built subjects that violate named
contract clauses read `met=true`. The counter's own sandbox, forgery battery and
population digests are sound (4 of 16 counter mutants are killed by a frozen subject or
hand case), but its anti-table conjunct, its pins-blob digest and its self-integrity have
no witness, and its reference accepts `max-age="600"` where the contract and the shipped
tool refuse it.

Axes walked (Godspeed): (a) tool-mutant kill rate against the frozen counter,
(b) counter-mutant detection (defect discovery), (c) receipt reproducibility from
committed bytes. Every move below improved (b) or (c) and harmed none: no frozen file was
edited, every mutant lived in scratch, and every verdict is a counter run on a committed
revision.

## Method (exact)

Lane `LANE=/home/vgpnk/Projects/shokunin/kake-shokunin`, freeze
`a5640ca02c20f94a0fa03af41b977b46ae99808e`, shipped subject
`scripts/heuristic_freshness.py` sha256
`7bfe82da8e1a1d541930ef1b4ee64cfe9b3fa5b8169680795bcc8626d2f37f5c` (unchanged at
report time), frozen counter `.ufo/waves/round-92/c92_heuristic.py` sha256
`8f356c8d4a8dea5de80f97f61ba6e8147b0e60b9e356cf651df28b0db1405f3f`.

```
S=/fast/scratch/hyaku/kake-r92/MutHeuristic
git clone -q --shared LANE $S/clone
git -C $S/clone checkout -q --detach a5640ca02c20f94a0fa03af41b977b46ae99808e
git -C $S/clone update-ref refs/heads/master $(git -C LANE rev-parse refs/heads/master)
# assert: git -C $S/clone rev-parse --show-toplevel == $S/clone
# each mutant: write it over scripts/heuristic_freshness.py in the clone, then
git -C $S/clone -c user.name=mut-fixture -c user.email=mut@fixture.invalid \
    commit -qm "fixture <mutant>"
python3 -B LANE/.ufo/waves/round-92/c92_heuristic.py --root $S/clone \
    --revision <mutant commit> --work $S/work/<id>
```

The counter reads the candidate from `--revision`, so a mutant is scored only once it is a
commit in a scratch clone; LANE was never staged, committed or checked out. A verdict is
`killed` iff the counter exits non-zero or prints `met=false`.

Baselines: `T00-shipped` (the shipped tool as committed in scratch) reads
`hand=28/28 generated=120/120 forgeries_refused=5/5 anti_table=ok population=ok met=true`
exit 0 — so the scoring path itself is live.

## Part 1 — 24 tool mutants of `scripts/heuristic_freshness.py`

11 killed, 13 survived. Full table with per-mutant sha256, commit, exit code, verdict,
detector and the exact one-clause diff: `tool-mutants.txt`.

| id | clause mutated | verdict | detector |
|---|---|---|---|
| T01-drop-204 | 11 set: 204 removed | killed | generated population (status 204, no usable Last-Modified) |
| T02-drop-404 | 11 set: 404 removed | killed | hand case `gate/404-heuristically-cacheable` |
| T03-add-500 | 11 set: 500 added | killed | hand case `gate/500-not-cacheable` |
| T04-cap-86401 | 12 cap 86400→86401 | killed | hand case `heuristic/cap-86400` |
| T05-fraction-9 | 12 fraction 10→9 | killed | hand case `heuristic/ten-percent` |
| T06-boundary-lt | 12/13 `Last-Modified <= Date`→`<` | killed | hand case `heuristic/equal-timestamps` |
| T07-private-any | 9 `private` honoured when not shared | killed | hand case `store/private-not-shared` |
| T09-expires-negated | 10 `Expires - Date` sign reversed | killed | hand case `explicit/expires-minus-date` |
| T10-smaxage-any | 10 `s-maxage` honoured when not shared | killed | hand case `explicit/s-maxage-ignored-private` |
| T11-public-inverted | 11 `public` gate polarity inverted | killed | hand case `gate/500-not-cacheable` |
| T24-dup-name | 1 duplicate header name accepted | killed | hand case `refuse/duplicate-header-name` |
| T08-vary-contains | 9 Vary member equality→substring | **survived** | — |
| T12-quoted-delta-accepted | 4 quoted delta-seconds accepted | **survived** | — |
| T13-nul-accepted | 2 NUL in a header value accepted | **survived** | — |
| T14-shared-type | 3 non-bool `shared` accepted | **survived** | — |
| T15-now-negative | 3 negative `now` accepted | **survived** | — |
| T16-status-bounds | 3 status 0..999 accepted | **survived** | — |
| T17-bool-is-int | 3 `true` accepted as `status`/`now` | **survived** | — |
| T18-extra-top-key | Input: extra top-level key accepted | **survived** | — |
| T19-extra-stored-key | Input: extra `stored` key accepted | **survived** | — |
| T20-value-no-trim | 2 header value not trimmed | **survived** | — |
| T21-strip-all | 2 trim widened beyond SP/HTAB | **survived** | — |
| T22-signed-date | 5 signed `Date` accepted | **survived** | — |
| T23-early-notstorable | 8 `not-storable` decided before validation | **survived** | — |

### Surviving tool mutants = missing case classes (named clauses)

1. **clause 9 — Vary member equality.** A member must equal `*`; `Accept-*` is not a star
   member. No case carries a non-star member containing `*`.
2. **clause 4 — delta-seconds bareness.** Contract: "a quoted or signed form is a
   refusal." No case sends `max-age="600"`; see D1 for the deeper consequence.
3. **clause 2 — CR/LF/NUL.** The refusal set is tested nowhere; NUL is the unexercised byte.
4. **clause 3 — `shared` type.** Non-bool `shared` is never sent.
5. **clause 3 — `now` bound.** No case sends a negative `now` (all 28 hand cases use
   `now=1000000`; the generator draws 0..2e9).
6. **clause 3 — status bounds.** No case sends a status outside 100..599 (the generator's
   list is inside the range).
7. **clause 3 — bool is not an int.** No case sends `true` as `status` or `now`.
8. **Input — extra top-level key.** "Any other top-level key is refused" is untested.
9. **Input — extra `stored` key.** Same, one level down.
10. **clause 2 — trimming.** No value in the population carries leading/trailing SP or
    HTAB, so neither "trim nothing" nor "trim everything" is observable.
11. **clause 5 — decimal integer.** `+5`/`-5` as `Date` is untested (`1e6` is the only
    non-integer case).
12. **clause 8 — no decision before validation.** A `not-storable` response with a
    malformed `Expires`/`Last-Modified` is untested, so returning early is invisible.

## Part 2 — 16 counter mutants of `.ufo/waves/round-92/c92_heuristic.py`

4 killed, 12 survived. Full table with diffs and witness revisions: `counter-mutants.txt`.

| id | mutation | verdict | refusing subject / witness |
|---|---|---|---|
| CM06-dup-header | reference: duplicate-name refusal disabled | killed | hand case `refuse/duplicate-header-name` (exit 2, reference drift) |
| CM07-drop-204 | reference: 204 removed from the set | killed | generated population (`generated=115/120`, exit 1) |
| CM08-cap | reference: cap 86400→86401 | killed | hand case `heuristic/cap-86400` (exit 2, reference drift) |
| CM16-no-sandbox | subject launched without the sandbox | killed | `neg-oracle-import.py` + `neg-pin-reader.py` admitted, `forgeries_refused=3/5`, exit 1 |
| CM01-extra-top-key | reference: extra top-level key accepted | survived | `N14-extra-top-key`: mutant met=true, pristine met=true |
| CM02-shared-type | reference: non-bool `shared` accepted | survived | `N6-shared-truthy`: mutant met=true, pristine met=true |
| CM03-now-bound | reference: negative `now` accepted | survived | `N7-now-negative`: mutant met=true, pristine met=true |
| CM04-status-bounds | reference: status 0..999 accepted | survived | `N8-status-bounds`: mutant met=true, pristine met=true |
| CM05-nul | reference: NUL accepted | survived | `N11-nul-accepted`: mutant met=true, pristine met=true |
| CM11-anti-table | met: `not hits` dropped | **survived (defect)** | `N2-stem`: mutant met=true with `anti_table=hit`; pristine met=false |
| CM12-pins-digest | met: `PINS_SHA` blob check dropped | **survived (defect)** | `W-pins-comment`: mutant met=true; pristine met=false (`population=drift`) |
| CM13-met-true | met forced true | **survived (defect)** | `N4-cap43200`: mutant met=true with `hand=25/28`; pristine met=false |
| CM14-dead-keys-out | `KEYS_OUT` emptied | survived (no effect) | constant never read |
| CM09-sandbox-open | sandbox `open` denial removed | survived (invisible) | forgeries still 5/5 refused |
| CM10-sandbox-import | sandbox import allowlist denial removed | survived (invisible) | forgeries still 5/5 refused |
| CM15-sandbox-proc | sandbox process-creation denial removed | survived (invisible) | no forgery creates a process |

## Defects found in the frozen counter (findings, not edits)

- **D1 — reference/contract drift, unobserved.** Contract clause 4: a quoted delta-seconds
  argument is a refusal. The counter's `parse_cc` strips the quotes *before* the digit
  check, so `reference({"Cache-Control": 'max-age="600"'})` returns
  `{"decision": "explicit", "lifetime": 600}` while the shipped tool refuses it
  (`exit 1`, `invalid_input: max-age argument is not a bare non-negative decimal
  integer`). No hand case and no generated case contains a quoted argument, so the drift
  never reaches the exit-2 self-check — the counter's docstring claim that "an
  oracle/contract drift exits 2 rather than passing silently" is false for this class.
- **D2 — nine contract-violating subjects read `met=true`.** Subjects N6–N14 (committed in
  scratch, listed above) violate clauses 2, 3 (×3), 4, 5, 8, 9 and the Input shape; the
  pristine counter scores all nine `met=true`, exit 0. `met=true` therefore means
  "conforms to 28 hand cases + 120 generated cases + 5 forgeries", not "conforms to
  contract v1".
- **D3 — the anti-table conjunct has no frozen subject.** The five frozen forgeries are
  never passed through the anti-table (only `a.candidate` is), and none embeds a hand-case
  digest or a forgery stem. A subject that behaves correctly but carries the comment
  `# neg-status-table` (`N2-stem`) or a 16-hex hand-case digest (`N3-digest`) is refused by
  the pristine counter (`anti_table=hit`) and admitted by CM11. The counter's docstring
  claim that "the anti-table conjunct is exercised by a frozen subject rather than being an
  unfalsified assertion" is falsified: the only witnesses are the ones this seat built.
- **D4 — `KEYS_OUT` is dead.** Defined at line 47 and never read; output-key exactness
  comes from `got == expected`. CM14 changes it with no observable effect.
- **D5 — the C2 counter does not pin its own blob.** C1's counter carries a `self`
  conjunct (`frozen/c1-self.sha256`); C2's has none, so CM13 (`met = True`) is
  indistinguishable from the frozen counter by any downstream check.
- **D6 — the three sandbox guards are mutually redundant for this population.** Removing
  the `open` denial alone (CM09) still refuses all five forgeries because the import
  allowlist blocks the counter module's own `argparse`/`shutil`/`subprocess` imports;
  removing the import denial alone (CM10) still refuses them because the `open` denial
  blocks the counter-blob and pins reads; the process guard (CM15) is touched by no
  forgery. Only removing the sandbox wholesale (CM16) admits two forgeries. The frozen
  population cannot attribute a refusal to a particular guard.
- **D7 — `PINS_SHA` is load-bearing but unwitnessed.** A revision whose pins file gains a
  trailing comment reads `population=drift` under the pristine counter and `population=ok`
  under CM12. No frozen control exercises it.
- **D8 — hand-case coverage of the cacheable set is 2/12.** Only 404 and 500 are hand
  cases; T01 (drop 204) and CM07 are caught by the generated population only, and the
  generated status list is fixed, so a wrong set entry for 206/300/301/308/405/410/414/501
  would be caught only if the generator happens to draw that status without an explicit
  expiration.

## C1 counter probe (the heading's "C1 counter")

The C1 counter was not mutated at scale because its frozen `self` conjunct pins its own
blob: `sha256 .ufo/waves/round-92/c92_defects.py` =
`9ba796212cf8b0cca9251e0208962609fc2b9a224b0f25610aa2c7f346f13195` =
`frozen/c1-self.sha256`. Probe run at the freeze revision:

```
python3 -B LANE/.ufo/waves/round-92/c92_defects.py --root LANE \
  --revision a5640ca02c20f94a0fa03af41b977b46ae99808e --work <scratch>
C1v92 revision=a5640ca0… items=3 open=3 closed=0 battery=hit differential=fail self=ok met=false
exit=1
```

`self=ok` at the freeze and `self=hit` at `e143faff` (where the pin file does not exist)
show the pin is live. Two honest limits: (i) the pin is an internal consistency check —
a mutant that also rewrites `frozen/c1-self.sha256` in the same revision reads `self=ok`;
(ii) item A's execution binding could not be mutation-tested here because the carrier
artifacts (`integration/mutation-tip.*`) did not exist during this seat's run, so every
item-A predicate path returns "mutation receipt absent" at the freeze revision.

## Limits

- The `met=true`/`met=false` verdicts are the frozen counter's own output; no verdict here
  is an admission, and none changes the round's claim predicate.
- Tool-mutant scoring used one clone and one commit chain; the shipped tool's sha256 was
  re-checked at report time and is unchanged.
- Subject variants N2–N14 are this seat's construction from the contract text, not the
  lane's; they were committed only in scratch, so the witness revisions are not citable
  after scratch removal. `subjects.txt` carries the base subject (`bootstrap_subject.py`,
  scored `met=true` by the frozen counter) plus each witness's exact one-clause diff and
  its pristine reading — that is the reproducible form.
- No network, no installs, no lane writes outside `.ufo/waves/round-92/w1/MutHeuristic/`.
