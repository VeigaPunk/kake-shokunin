VERDICT: C1 is met on the committed bytes, but its frozen counter also admits a forgery. C2 is met by its frozen counter, but that counter also admits three forged gates, and the gate itself is falsified as a conformance gate: a 20-line stdlib stub escapes the sandbox and is admitted, and it admits 7/7 held-out non-conforming mutants.

Seat: CriticClaims (critic, wave 1, round 90). Lane `/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE), master `79e1aac24654e01dc0559eb3beb8abbe61ec73a8`.
I ran the counters exactly as frozen. Their sha256 match the freeze: `c90_gate.py` 703b0058…, `c90_defects.py` 462224f6…, pins a57f8985…. The bytes are the same at 4ee62b18, 7f6c68f1, e50c9566 and master.
- Receipts: `.ufo/waves/round-90/w1/CriticClaims/` (`receipts/`, `probes/`, `forged-gates/`, `SHA256SUMS`).
- Fixtures: one shared clone under `/fast/scratch/hyaku/kake-r90/CriticClaims/fx.2ZsC`. I checked that `rev-parse --show-toplevel` equalled the fixture before committing. Identity was `fixture <fixture@scratch.invalid>`. The scratch directory is deleted.
- I made no writes in LANE outside my two paths, and ran no mutating git command in LANE.
- Tools: none installed or upgraded. No network.

## (a) Causal separability: holds for the counters, not for the claim text

| Run | Line 1 | exit | Receipt |
|---|---|---|---|
| C1 counter at C2 carrier 7f6c68f1 | `open=3 closed=0 met=false` | 1 | `receipts/c1-lane-at-7f6c68f1.txt` |
| C2 counter at C1 carrier e50c9566, seed 90 | `positives=4/4 negatives_refused=57/57 … met=true` | 0 | `receipts/c2-lane-at-e50c9566.txt` |
| C1 counter at master 79e1aac2 | `open=0 closed=3 met=true` | 0 | `receipts/c1-lane-at-master.txt` |

- Neither counter reads the other's files or receipts. I checked this by reading both sources: `c90_gate.py` extracts only the gate, the frozen population, `c89_key.py` and the pins file.
- **Defect A1 (claim and carrier):** the frozen C2 claim includes a conjunct the counter never measures. It reads "Sourced: the CR/LF every-header refusal clause is grounded on a RFC 9110 §5.5 row opened this round". That row, S466, does not exist at the C2 carrier: `git show 7f6c68f1:corpus/SOURCES.md | grep -c '^| S466 |'` → 0, while at e50c9566 it is 1.
  - The C2 knowledge entry `corpus/knowledge/cache-key-conformance-gate.md` is also absent at 7f6c68f1 and present at e50c9566.
  - So C2-as-worded is only true at the C1 carrier. The "C1 carrier" e50c9566 bundles C2 material: S466, S468 and the gate entry.
  - The freeze's Separability paragraph ("C2 reads only `scripts/`…") is true of the counter, not of the claim.
  - Smallest correction: state C2's sourcing conjunct as a separate unmeasured note, or measure C2 sourcing at e50c9566, and say that the carrier is shared.

## (b) Cheap shortcuts and forgeries reach both targets

### C2: three forged gates score met=true with the frozen counter

Each forged gate was committed on top of 7f6c68f1 in the fixture as `scripts/cache_key_conformance.py` (commits in `receipts/fixture-commits.txt`). Command for each: `python3 -B .ufo/waves/round-90/c90_gate.py --root <fx> --revision fx-<N> --work <scratch> --seed 90`.

| Forged gate | Size | Line 1 | exit | Receipt |
|---|---|---|---|---|
| F1: md5 allowlist of the 4 positives, after stripping the counter's nonce suffix `\n# nonce <16hex>\n` | 7 lines | `gate=present positives=4/4 negatives_refused=57/57 false_admits=0 errors=0 anti_table=ok population=ok seed=90 met=true` | 0 | `receipts/c2-fx-F1.txt`, `forged-gates/F1-gate.py` |
| F1b: no hashes in its source; it walks up from `--candidate` to the pins file the counter extracts beside the subjects and admits pins ending `cache_key.py` or containing `/M33` or `/M36` | 14 lines | same, `met=true` | 0 | `receipts/c2-fx-F1b.txt` |
| F2: the real gate with `reference()` replaced by the shipped `scripts/cache_key.py@209027f4`, embedded as a string and exec'd (an oracle-wrapping differential gate) | 440 lines | same, `met=true` | 0 | `receipts/c2-fx-F2.txt` |

- **F1 and F1b are forgeries**, and they are cheaper than the freeze's own forgery controls. The freeze's "hash-table gate" control (`run_controls.sh` lines 107–120) hashes the nonce'd bytes, so it could never match. That control was a strawman.
  - The nonce is a fixed-format suffix that can be stripped.
  - `anti_table` checks only `sha256[:12]` and full file stems. md5 and indirect lookup through the pins file both pass it.
- **F2 is not a separate forgery, and that is the point.** The real gate admits `cache_key.py` on every scored case, so its `reference()` equals the shipped candidate on every input the gate sends. A gate that only wraps the candidate under test is therefore indistinguishable to this counter.
  - The counter cannot tell an independent gate from a tautological one.
  - Common-mode evidence: the shipped candidate and the gate's `reference()` both accept `{"request_headers":{"a":"1","a":"2"}}` with last-wins (`'u\x1fa\x1e2'`). The contract says header names that are "equal case-insensitively are refused".
  - Both parse with `json.loads`, so the gate cannot see this case (`receipts/heldout-witnesses.txt`, DUP-EXACT-JSON-KEY).
  - This is a contract-reading gap that no seat has routed. It is not a proven bug.
- **Counter weakness, not exploited by the round:** the population pins are read from the *measured revision* (`extract(root, rev, [... PINS_FILE])`). The counter never checks the pins file against the freeze digest `a57f8985…`, so a carrier could swap a subject and its pin together.
  - The pins are byte-identical at 4ee62b18, 7f6c68f1, e50c9566 and master, so the real carrier did not do this.
- **Conclusion on C2's evidence:** the counter's `met=true` is reachable with a 7-line table gate, so it does not show that the lane has a behavioural gate. Only reading the gate source shows that, and the real gate is behavioural (hand cases, generated cases, sandbox). But that gate fails the stronger tests below.

### C2: the real gate, attacked directly (`scripts/cache_key_conformance.py`, blob identical at 7f6c68f1 and master)

**Defect A2: sandbox escape.**
- `probes/p2_forkexec.py` is a 20-line stdlib stub. It calls `_posixsubprocess.fork_exec` directly, which skips the Python-level `subprocess.Popen` audit event. Through that it runs the sibling `cache_key.py` in an unsandboxed child.
- Command: `python3 -B scripts/cache_key_conformance.py --candidate probes/p2_forkexec.py --seed 90 --work <scratch>`.
- Result: `clauses=6/6 hand=70/70 generated=120/120 sandbox=ok seed=90 met=true`, exit 0 (`receipts/sandbox-escape.txt`).
- This delegating stub belongs to the same class as the frozen negatives `ctl-oracle-import` and `neg-oracle-path-import`. The gate admits it.
- It falsifies the gate docstring ("spawn no process") and the entry's Sandbox row (`cache-key-conformance-gate.md:35`, "no process"; `:46`, delegation is "refused by sandbox").
- Partial disclosure exists at `:60-61` ("native code already loaded by the stdlib is not confined … not a security boundary"). That line does not name this cheap, pure-stdlib delegation path.
- Control: `probes/p1_readline.py`, which reads the oracle through `readline.read_history_file`, is caught: `sandbox=violation met=false`, exit 1. The hook covers that path.
- Smallest correction: add `_posixsubprocess`, `subprocess`, `multiprocessing`, `_ctypes` and `ctypes` to a denied-import set in `SANDBOX`, and add `p2_forkexec` as a frozen negative. Real confinement would be OS-level (e.g. bwrap or unshare), which is routable.

**Defect A3: held-out non-conforming candidates are admitted, 7/7 mutants on 3 seeds (21/21 runs exit 0).**
- Each probe is a one-line mutation of the shipped `cache_key.py`. `receipts/heldout-witnesses.txt` shows each mutant differing from both the gate's own `reference()` and the shipped candidate on one input.
- Scores: `receipts/heldout-gate.txt`, all `clauses=6/6 hand=70/70 generated=120/120 sandbox=ok met=true`, exit=0, seeds 90, 7 and 12345.

| Mutant | Contract clause violated | Why the gate misses it |
|---|---|---|
| H1 truncates to the first 4 Vary members | 1 Members | generator draws ≤4 members; hand cases ≤3 |
| H2 refuses `\|` and `^` in names | 2 Names / RFC 9110 tchar | name pool lacks these tchars |
| H3 percent-encodes non-ASCII in the URI | 4 Escaping (only `%` and the separators) | no non-ASCII URI case |
| H4 trims DEL from values | 3 Values (SP/HTAB only) | value alphabet lacks U+007F |
| H5 refuses values longer than 64 chars | 3 Values | values ≤5 chars |
| H6 strips spaces from header names, so `" a"` is accepted | Refusals (name not a token) | no OWS-padded name case |
| H7 refuses more than 6 headers | Input | ≤4 headers generated |

- These are boundary and coverage gaps (case-count and alphabet limits), not a design flaw. They do show that "refuses the non-conforming population" is a score on a train set: the population was visible while the gate was written.
- The lesson's Mistake 5 (a hand case dropped because all four positives disagreed) shows the gate was fitted against the frozen positives, which is disclosed.
- Smallest correction: widen the generator (0–8 members and headers, the full tchar set, non-ASCII URI and values, DEL, long values) plus boundary hand cases. Add held-out mutants generated at scoring time from the seed to the C2 counter.

### C1: one forgery fixture closes all three items

- Fixture commit `31b09129` (branch fx-c1 from freeze 4ee62b18; diff in `receipts/c1-forgery-fixture.patch`).
- Command: `python3 -B .ufo/waves/round-90/c90_defects.py --root <fx> --revision fx-c1 --work <scratch>` → `C1v90 revision=31b09129… items=3 open=0 closed=3 met=true`, exit 0 (`receipts/c1-fx-forgery.txt`).

What the fixture contains:
- **D1:** the real relocation (bytes from master). This item is honest.
- **D2 forgery:** a correction for "`open=5 closed=1` at f62e7954" that cites `.ufo/waves/round-89/controls/base-c1.txt` at the round-89 **base** 76225160 (`open=6 closed=0`).
  - It is not a measurement of f62e7954. It is a different revision, and its number contradicts the statement it claims to correct.
  - The counter accepts any 40-hex revision whose committed receipt and c89 re-run agree, so an old receipt is enough and no new file is needed.
  - The freeze's own positive control also cites 93475f7e, not f62e7954.
  - Smallest correction: require the hex revision to be `f62e7954a9ed…` (the statement being corrected), or the round-89 measured tip, and nothing else.
- **D3 forgery:** a new row S499 whose scope is S463's scope with "not" changed to "Not". It still reads "…; Not cache-key construction, storage…", which is exactly the defect.
  - Its teaches cell is `supersedes S463 — scope kept`. The Gate quote is the 3-word `"the cache key"`.
  - The scope check is a case-sensitive substring test, and any 3-word RFC phrase passes the quote check.
  - Smallest correction: test the scope case-insensitively for "not … construction", and require the Gate quote to come from S467's anchored lines (§2, 251–262).
- The real carrier e50c9566 does the honest thing (correction at f62e7954 itself; S467 scope "grounds cache-key construction ingredients"), so **C1 holds on the committed bytes**. Its counter could not have told the honest carrier from this fixture.

## (c) Axis labels

- **C1 "calibration"** fits only part of the claim. D89-2 (a ledger number reconciled to a receipt) is calibration. D89-1 (scratch file at the lane root) is operability/discipline, and D89-3 (a registry scope cell) is corpus quality.
  - The calibration-specific route from the spot-check ("turn the instrument-calibration lesson into a grounded `QUALITY.md` criterion", `round-89-verifier-spotcheck.md:169-171`) is not in any measured commit: `git diff --stat 209027f4 master -- corpus/QUALITY.md` is empty.
  - The round-90 lesson §Routed does not carry it either. `corpus/QUALITY.md` shows as uncommitted-modified in LANE's working tree during my review, so L1 may be adding it now. It is unmeasured.
- **C2 "operability, capability acquisition"** is right. This is a new verification tool, not freshness. The round-89 freshness dispute is resolved correctly.

## (d) Is C1 thin, and is the lane more capable?

- **C1 is bookkeeping-only.** By numstat it is LOG +5, SCORECARD +7, SOURCES +3, the lesson, a 28-line file moved, and one receipt re-run. It closes the three routed items honestly, but it adds no capability.
  - D3 is only partly closed in substance. `corpus/knowledge/cache-key-construction.md:1` still says `source: S463 … (already a registry row; this entry adds none for §4.1)`, and S463 `used-by` still lists that entry.
  - A reader of the construction entry is still sent to a row whose scope says "not cache-key construction". S467's `used-by` lists the entry, but the entry does not cite S467.
- **The lane is measurably more capable, but less so than claimed.**
  - Real gains:
    - The gate refuses the 7 ExecControls stubs that the round-89 instrument falsely admitted.
    - The M37 equivalence claim is falsified with a grounded `%`-tchar case.
    - Three RFC rows are added with retained bodies.
  - Limits found here: a sandbox escape (A2), 7 boundary misses (A3), and a counter that admits forgeries (F1, F1b, F2).
  - At master, `SKILL.md` has 0 mentions of `cache_key_conformance` (`git show master:SKILL.md | grep -c cache_key_conformance` → 0), so the gate is not yet registered in committed bytes. SKILL.md is uncommitted-modified in the working tree.

## (e) Harm

- `git -C LANE diff --numstat 209027f4..master`: 30 files, and every row has 0 deletions (`awk '$2!=0'` prints nothing).
- `--diff-filter=D`: 0 deleted files.
- SCORECARD.md, LOG.md and corpus/SOURCES.md are pure appends, so the base bytes are a prefix (the C1 D2/D3 conjuncts confirm this at e50c9566 and master). S463 is byte-identical.
- I found no filed byte rewritten and no owned axis made worse by the committed changes.
- Overclaim risk: the gate's docstring and entry claim "no process" and refusal of delegation, which A2 falsifies. Entry `:35` and `:46` would spread a false guarantee if admitted unamended.

## Honest limits

- I scored held-out mutants and the escape probes against the gate directly, not through the C2 counter, because the counter's population is frozen.
- Contract readings for H3 (non-ASCII URI percent-encoding is non-conforming because only `%` and the separators are escaped) and for DUP-EXACT-JSON-KEY are my reading of `c2-contract.md`. They are stated, not adjudicated.
- C2 counter runs used seed 90 only. The held-out gate runs used seeds 90, 7 and 12345.
- I did not re-run the freeze's own control script.
