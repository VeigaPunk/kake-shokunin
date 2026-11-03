# CriticClaims — round 73 w1, adversarial review of the frozen contract (attempt 1)

Seat: CriticClaims (leaf; no subagents; no peer messaging). Lane untouched except this report file.
Scratch: `/fast/scratch/hyaku/kake-r73/CriticClaims/` (clone at base; deleted before yield — trap verified below).
Environment: git 2.56.0, Python 3.14.8, node v24.21.0 (all preexisting; **no tool installs performed** — the 2026-10-19 tooling authorization was not needed).

## Freeze topology (measured)

```
git -C /home/vgpnk/Projects/shokunin/kake-shokunin log --oneline -6        # rc=0
  4c7c53bc round-73: freeze claim contract, base controls, attack corpus, wave-1 plan
  c1f3d8d4 round-72 verifier spot-check (integrator, hyaku): non-author admit/reject
git -C ... log -1 --format='parent=%P subject=%s' 4c7c53bc                 # rc=0
  parent=c1f3d8d4ed9470ecbaaf3353952a374b079e68cc subject=round-73: freeze claim contract, ...
```

The **freeze commit is `4c7c53bc`**, a child of base `c1f3d8d4`. `git ls-tree -r --name-only 4c7c53bc -- .ufo/waves/round-73` (rc=0) contains: `attack-corpus.txt`, `contract.md`, `controls/{c0-gate-status-base-c66,c1-pointer-base-c70,c2-c72-base,c3-sweep-base}.txt`, `sources/{bash-param.html,bash-param.txt,receipts.txt}`, `w1-plan.json`, `w1-spec.json`. Working tree vs freeze bytes: `cmp` on contract.md, attack-corpus.txt, all 4 controls, sources/receipts.txt → **7/7 IDENTICAL**. No post-freeze mutation of the frozen artifacts.

## C1 — calibration

**(1) Base receipt and rerun.** `controls/c1-pointer-base-c70.txt` first/last lines:
`+++ python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root . --revision c1f3d8d4... --work /fast/scratch/hyaku/kake-r73/main/c70w` / `pointers=359 dangling=17 annotated=17 unannotated=0 met=true` / `c70_exit=0`.
Rerun at base in my clone: `python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root <clone> --revision c1f3d8d4 --work $S/c70w` → identical summary, **exit 0**. Receipt confirmed.

**(2) The two tokens are dead at base.**
```
git cat-file -e c1f3d8d4:.ufo/waves/round-72/controls/c1-tip.txt   # exit 128, "fatal: path ... does not exist"
git cat-file -e c1f3d8d4:.ufo/waves/round-72/controls/c2-tip.txt   # exit 128, same
git ls-tree --name-only c1f3d8d4 -- .ufo/waves/round-72/controls/  # rc=0, 13 files, neither c1-tip.txt nor c2-tip.txt
```
Both non-zero as the contract expects. ✓

**(3) Is "c70 is blind to them" true for the reason given?** The blindness is real, but the contract's reason ("c70 parses only repo-rooted SCORECARD pointers") is imprecise. The actual mechanism (base `c70_pointer_audit.py` lines 46–52):
```python
CLASSES = (
    ('repo', re.compile(r'(?:^|[`(>|\s])((?:\.ufo|corpus|scripts|handoffs|considerthese)/[A-Za-z0-9_./-]+\.[A-Za-z0-9]{1,16})(?![A-Za-z0-9])')),
    ('home', ...), ('tmp', ...))
```
- `controls/c1-tip.txt` matches **no class**: the repo class whitelists only the prefixes `.ufo|corpus|scripts|handoffs|considerthese`, so the token is never extracted at all — it is not "resolved and found alive", it is invisible. The same holds for `sources/…` and `w1/…` tokens.
- c70 reads **only SCORECARD.md** (`read_scorecard` → `git show <rev>:SCORECARD.md`); it never reads LOG.md. So "only repo-rooted" is wrong twice over: c70 also parses `~/` and `/tmp/` classes, and repo-rooted-ness is not the discriminator — the prefix whitelist is.
- **Does not void C1**: the new counter has its own grammar; the before values re-derive (next item).

**(4) Before values re-derived independently.** From committed bytes at base: LOG.md `## Round 72` section = lines 2498–2507 of 2507; SCORECARD first-cell-72 rows = 2 (lines 4818–4819 of 4829). In-scope tokens (`(controls|sources|w1)/…`) found: 9 unique (7 × `controls/…` alive under `.ufo/waves/round-72/`, exit 0; plus the two dead). Exactly `controls/c1-tip.txt` and `controls/c2-tip.txt` are dead, and **each is named in both the LOG section and the SCORECARD rows** (LOG line 2466: "…tip `unannotated=0 append_only=true met=true` exit 0 (`controls/c1-tip.txt`)"; LOG line 2505 and SCORECARD rows 4818/4819 name both). Expected before `dead=2 unannotated=2 met=False exit 1` re-derives. ✓

**(5) Is `dead ≥ 2` sound, and would a token-dropping tail defeat it?** Two answers:
- *Against a tail that drops the dead tokens from LOG/SCORECARD*: sound, **provided** the delivered counter implements the append-only conjunct over **both** files ("every base line of LOG.md and of SCORECARD.md survives as a line-prefix"). Dropping a token requires rewriting or deleting a base line → prefix violation → red. The spec mandates this and a selftest fixture ("a base line edited (append_only false)"). Note c70's own `append_only` covers SCORECARD only — the new counter must not inherit that limitation.
- *The deeper function of `dead ≥ 2`*: it is the **anti-blindness pin**. A counter whose token regex is broken (the exact c70 failure mode) would report `dead=0 unannotated=0 met=True` — a false green. `dead ≥ 2` forces the counter to prove it still sees the two known dead tokens. This makes finding **F-A** below the most serious defect in the freeze.

**(6) Do-nothing control adequacy.** Base control = the counter itself at base (expected red: dead=2 unannotated=2 → exit 1). The bare-errata fixture (names the token, no resolving path → stays unannotated → red) is mandated in the spec selftest. Adequate against false-green for the stated mechanism. Note the annotation semantics are **existence-only**: a correction naming any resolving path under `.ufo/waves/round-72/` passes, even an unrelated one — consistent with the claim sentence's promise ("resolve or carry a … correction"), so by design, but worth stating.

**(7) Hazard demonstrated (F-C).** An appended correction that names an unresolving `.ufo/…`-spelled path creates a *new* dangling repo pointer that c70 **does** see (prefix `.ufo/` is whitelisted), and c70's annotation cells come only from the round-70 calibration section — so the harm check "c70 exit 0 at tip" goes red:
```
scratch commit: append to SCORECARD.md
  | errata (demo): superseded `controls/c1-tip.txt` — corrected target `.ufo/waves/round-72/controls/c1-tip.txt` |
python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root <clone> --revision HEAD --work $S/c70w2
  → pointers=360 dangling=18 annotated=17 unannotated=1 met=false   # exit 1
```
Safe spellings for real tails: name only `controls/…`/`sources/…`/`w1/…` (invisible to c70) or `.ufo/…` paths that resolve at the tip. (The ConnOverlap seat is assigned this same trap; this is independent measured evidence.)

## C2 — operability

**(1) Before value.** Receipt `controls/c2-c72-base.txt`: `C2v2 revision=c1f3d8d4… brace_findings=0 command_findings=0 prose_findings=0 findings=[] removed=8 added=8 guard=ok met=True`, `c72_exit=0`. Rerun at base: identical line, **exit 0**. ✓

**(2) Do-nothing control: measured, target reached.** I imported the frozen c72's `line_findings` (importlib from the committed file, no edit) and ran it over the corpus third column:
```
c72_accepts=9 of A=11; legit_clean=4/4
```
- Accepted (holes real): corpus lines 1–2 (**H1**: `${TMPDIR:-/tmp}` — `TOKEN_RE` needs literal `/tmp/`, `BRACE_TOKEN_RE` needs `${TMPDIR:-/tmp/` with the slash *inside* the braces; both escape) and lines 3–9 (**H2**: `rsync`, `rm`, env-prefix `TMPDIR=… python3`, `sudo` prefix, `cd … &&`, isolated `` `cp` `` span, `sudo cp` — first word outside the 17-word list, phrase-only annotation, pass).
- Rejected: line 10 (`` `cp state/… /tmp/…` `` — span first word `cp` is in the list → command finding) and line 11 (bare imperative `cp …` → command finding). Both are corpus lines whose `expected` is `finding`, so no conflict.
- **k = 9 ≥ 1 → the do-nothing control reaches its target; the claim is NOT void.** The void condition is explicit in the contract ("if c72 already rejects every attack line the claim is void") and is not triggered.

**(3) H4 diagnosis sentence is false against the frozen c72 (F-D).** Probes through the frozen `line_findings`:
```
see /tmp/kake-r12/live/ (historical record)                        -> (0, 0, 1)   # prose finding → rejected
see /tmp/kake-r12/live/ (not an executable)                        -> (0, 0, 1)   # rejected
cp x /tmp/kake-r12/y (historical record)                           -> (0, 1, 0)   # command finding → rejected
see /tmp/kake-r12/live/ (historical record, not an executable instruction) -> (0, 0, 0)  # full phrase → accepted
```
The contract sentence "(H4) the `PHRASE` constant is not pinned: a truncated phrase (`not an executable`, `historical record`) passes" is **not true** of the frozen c72 v2: every truncated variant I probed is a finding. The w1-spec's H4 requirement ("the annotation test uses the full phrase …, and the selftest asserts that a truncated annotation does not count") is the correct, stronger form and contradicts the contract's motivating sentence. Also: the frozen corpus contains **no truncated-phrase line**, and the corpus header comment says "holes H1-H3 of the contract" while the contract lists H1–H4 (H3 is a file-mode hole, not a line shape — the comment is off). **No predicate impact** (the predicate never requires H4 to be a live hole), but the round must not report "truncated phrases passed c72" as measured history.

**(4) H3 (symlink) — real, demonstrated, and covered only at spec level (F5-residual).** First-hand demonstration in my scratch clone:
```
leg 1: SKILL.md committed as mode 120000 symlink → .ufo/h3-target.md (which carries "see the artifacts under /tmp/kake-r99/ now")
  python3 -B .ufo/waves/round-72/c72_tmp_v2.py --lane <clone> --revision HEAD
  → C2v2 ... brace_findings=0 command_findings=0 prose_findings=0 findings=[] removed=1396 added=1 guard=ok met=True   # exit 0
leg 2: same content as a regular file
  → ... prose_findings=1 findings=[(1, 0, 0, 1)] guard=fail met=False   # exit 1
```
`git show <rev>:SKILL.md` on a mode-120000 blob returns the link text, so c72 audits one path string instead of 1396 real lines. The hole is real. The frozen **corpus cannot represent it** (a line list has no file mode) and the frozen **predicate's** corpus conjunct never exercises it; coverage rests entirely on the w1-spec's requirement ("a mode 120000 (symlink) SKILL.md is a finding, not an evaluation error") plus the predicate's `--selftest` gate. The integrator must verify the delivered c73 selftest actually contains the mode-120000 case and the truncation case before committing the counter.

**(5) Corpus provenance sentence is stale (F-E).** Contract C2 says the corpus is "written by the executor seat `ExecC2Counter` into `w1/` and promoted by the integrator before the counting command runs", while the Counter delivery section says it is "committed in this freeze". Measured: the corpus **is committed at `4c7c53bc`** (freeze), no `w1/attack-corpus.txt` exists, and the spec's ExecC2Counter item says "Verify every class against the frozen attack corpus" — verify, not write. Hazard only: anyone regenerating/re-promoting a corpus would change the frozen corpus, which the freeze itself declares voiding for C2. The frozen bytes are authoritative (working tree verified identical).

**(6) Registry row placement.** SKILL.md at base = 1396 lines; `grep -n` shows the last line (1396) is the gate-registry table row (`| gate-status-counter-v2-hostportable | …`). The appended c73 row lands at 1397, satisfying "beyond line 935"; "exactly one row naming `c73_tmp_v3.py`" is re-derivable at the tip via `git diff <base> <tip> -- SKILL.md`.

**(7) Sourced claim verified.** `sha256sum .ufo/waves/round-73/sources/bash-param.html` → `6b0800fd35c7f9fa8bb66d0eae1cd2e8bae7ded09ad6e89460dda2775a13c8e3` — matches the contract's `6b0800fd…a13c8e3` and `sources/receipts.txt` (url, `http=200 bytes=30764`, 2026-11-03T22:33:40Z). ✓

## C3 — freshness

**(1) Base repro.** `node scripts/freshness-sweep.mjs --offline` in the base clone → **exit 2**, stderr first line `freshness-sweep: Error: paths sidecar binding invalid: corpus/SOURCES.md:140` at `loadPathSidecar (scripts/freshness-sweep.mjs:388)`. Matches the control receipt byte-for-byte in substance. ✓

**(2) Exact sidecar-entry conditions** (read from `loadPathSidecar`, lines ~361–397 of the base file):
- Schema gate: `schema === 'kake-paths-sidecar-v1'`, `entries` array.
- Per entry: `file` is `'SKILL.md'` or matches `/^corpus\/.+\.md$/` with no `.`/`..`/empty parts; `line` safe integer ≥ 1; `token` string with `canonHome(token) === token` (canonical `~` spelling); `lineSha256` 64-hex; `kind` ∈ {`absent`, `restored`}; `date` YYYY-MM-DD that parses and round-trips; `note` string containing the date.
- Binding (throws `paths sidecar binding invalid: <file>:<line>` iff): the line is undefined, **or** `sha256(line) !== lineSha256`, **or** the token is not among the line's `PATH_RE` matches normalized through `canonHome`, **or** (`kind==='absent'` and the note-prose fails `ABSENT_RE` (`/absent|gone|vanished|emptied|no longer|dangling|no such file|never published|missing/i`, line 133) or lacks the phrase `historical record, not an executable instruction`), **or** (`kind==='restored'` and the note-prose matches `ABSENT_RE`). Duplicate key `file:line:token` throws.
- The sweep reads corpus files from the **working tree** (`fs.readFileSync`), not committed bytes — the tip measurement is against the tip worktree, consistent with the predicate's "at the tip".

**(3) The single mismatching entry.** Sidecar at base: 174 entries, 9 binding `corpus/SOURCES.md`, exactly one at line 140: token `~/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md`, pinned `lineSha256=b3315f41…a8a47`, kind `absent`, date `2026-10-31`, note contains "absent on this host" + the full phrase + the date. Actual base line-140 sha256 (file split on `\n`, sha256 of the line's UTF-8 bytes — the sweep's own method): `4e4081310d6ad17268d8120a29b0400c0edbe6fcee0c035af7c9341acc732e15` ≠ pinned value. The line carries the token in its `/home/vgpnk/…` spelling (canonHome maps it to the pinned `~/…` form). ✓

**(4) Re-pin sufficiency — demonstrated.** In my scratch clone I patched **only** that one entry's `lineSha256` to the computed value and re-ran the sweep:
```
patched entries: 1
node scripts/freshness-sweep.mjs --offline   → exit 1, Error lines on stderr: 0
  VERDICT: DRIFT — §paths: 1 unannotated miss · 1 NOT in pins.pathsMissSet (exit 1, partial: offline)
```
So re-pinning **only** `lineSha256` keeps every other check green (token presence on the new line, kind/date/note/phrase all re-evaluated and passed) — the annotation's meaning is preserved. The predicate's "exits 0 **or 1**" clause is therefore necessary, not slack: the expected after value is **exit 1 with named drift** (one §paths miss not in `pins.pathsMissSet`), not a clean exit 0. The round must not promise a clean sweep. Sidecar restored to base bytes afterwards (`git status --porcelain` empty).

**(5) Cause attribution re-derived.** `git merge-base --is-ancestor 84dcc841 c1f3d8d4` → rc=0; subject "round-71: lesson, LOG, SCORECARD, S132 used-by, wave evidence"; its SOURCES.md diff hunk is `@@ -137,7 +137,7 @@` modifying the S132 row (line 140) — the used-by cell edit the contract names. ✓

**(6) Selftest runnable.** `KAKE_SELFTEST_DIR=$S/kst HOME=$S/home node scripts/freshness-sweep.mjs --selftest` → **exit 0**, `selftest: 36/36 passed`. The predicate's selftest conjunct is exercisable as written. ✓

## Harm checks — re-derivation status

| Harm | Receipt | Re-derived | Result |
|---|---|---|---|
| c66 agreement ≥ 25 | `controls/c0-gate-status-base-c66.txt` | rerun at base, `--work $S/c66w`, jobs 6 | exit 0; `C1 gate-status members=28 evaluated=28 mismatches=3 structural=0 agreement=25 scores_held=3/3 met=True` — exact match ✓ |
| c70 exit 0 at tip | `controls/c1-pointer-base-c70.txt` | rerun at base | exit 0, identical summary ✓ |
| c72 exit 0 at tip | `controls/c2-c72-base.txt` | rerun at base | exit 0, identical line ✓ |
| sweep exit 2 control | `controls/c3-sweep-base.txt` | rerun at base | exit 2, same Error line ✓ |
| Scores unchanged | — | after-state only (`git diff base tip -- SCORECARD.md`); not run — no tip exists | re-derivable |
| Census | — | `bash <scratch copy> sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` | exit 0, final line `ok /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`, W04 duplicate-URL warnings pre-existing; SOURCES row count at base = 177 ✓ |

Note: the census script lives at the **fleet root** (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, 35466 bytes, verified present); the contract's relative command resolves from the fleet root. Not a dangling reference.

## The freeze itself — reference audit (item 5)

Every path the contract references, with status:
- **Committed at freeze `4c7c53bc`**: contract.md, attack-corpus.txt, the 4 base controls, sources/ trio (bash-param.html sha verified above), w1-plan.json, w1-spec.json.
- **Exist at base `c1f3d8d4`**: `.ufo/waves/round-66/c66_gate_status_hostportable.py`, `.ufo/waves/round-70/c70_pointer_audit.py`, `.ufo/waves/round-72/c72_tmp_v2.py`, `scripts/freshness-sweep.mjs`, LOG.md, SCORECARD.md, SKILL.md, `corpus/SOURCES.md`, `corpus/knowledge/freshness-sidecar.json`, `corpus/lessons/round-72-verifier-spotcheck.md` (`cat-file -e` exit 0).
- **Declared wave delivery** (Counter delivery section): `c73_wave_pointers.py`, `c73_tmp_v3.py` — absent at freeze, as declared. ✓
- **Declared future**: `corpus/lessons/round-73.md` ("after landing").
- **Round-produced receipts** named in Before→after: `controls/c2-c72-corpus.txt`, `controls/c2-c73-corpus.txt` — absent at freeze; declared by context (the sentences naming them describe the round producing them), though not listed in the Counter delivery section (pedantic note only).
- **Expected-absent by design**: `.ufo/waves/round-72/controls/c1-tip.txt`, `c2-tip.txt` — the C1 defect itself; measured exit 128/128.

**No dangling reference found.**

## Findings register

| # | Severity | Sentence attacked | Reproduction (command → exit → key line) | Voids the claim it touches? |
|---|---|---|---|---|
| **F-A** | **HIGH — must be adjudicated before the C1 counter lands** | w1-spec.json ExecPointerCounter item: "Selftest fixtures …: **no dead pointer (met)**; … **a dead pointer with a correct tail (met)**" | Textual contradiction with the frozen predicate `dead ≥ 2`: a fixture with dead=0 or dead=1 must yield `met=False` exit 1. If the executor builds the selftest to the spec labels, the delivered counter asserts `met=True` where the frozen predicate says False — which the freeze itself declares voiding ("A delivered counter that changes a frozen predicate … voids the claim it touches"). `dead ≥ 2` is the anti-blindness pin (a broken token regex would otherwise false-green exactly as c70 did); the spec labels would bless that failure mode. Smallest safe correction: the counter's selftest asserts `met=False` for the dead=0 and dead=1 fixtures; integrator checks this before committing the counter | Would void C1 **if implemented as labeled**; trivially fixable now |
| **F-B** | LOW | C1 claim sentence: "resolve or carry a **dated** correction" | The annotation rule (contract and spec) requires only the token name + a resolving path — no date check anywhere. An undated one-line correction satisfies the frozen predicate | No measurement impact; claim/predicate mismatch the judge should fix by wording (the "dated" qualifier is unenforced) |
| **F-C** | HAZARD (demonstrated) | interacts with harm "c70 exit 0 at tip" and C1's kill rule | Scratch commit appending a correction naming `.ufo/waves/round-72/controls/c1-tip.txt` (unresolving) → c70 at that commit: `pointers=360 dangling=18 annotated=17 unannotated=1 met=false`, exit 1 | No; execution constraint on tail spelling (see C1 §7) |
| **F-D** | LOW-MED (wording) | "(H4) … a truncated phrase (`not an executable`, `historical record`) passes" + corpus header "holes H1-H3 of the contract" | Probes through frozen `line_findings`: both truncations → `(0,0,1)` prose findings (rejected); no corpus line carries a truncation; header names H1–H3 while the contract lists H1–H4 | No predicate impact; the spec's H4 requirement (selftest asserts truncation does not count) is correct and stronger; the round must not report the contract's H4 sentence as measured history |
| **F-E** | LOW wording / HIGH if acted on | C2: corpus "written by the executor seat `ExecC2Counter` into `w1/` and promoted by the integrator" | Corpus is committed at freeze `4c7c53bc` (ls-tree rc=0); no `w1/attack-corpus.txt`; spec tells the executor to *verify* against the frozen corpus | No; hazard only — regenerating/re-promoting the corpus would be a frozen-corpus change, which voids C2 per the freeze's own rule |
| **F-F** | LOW | Spec: "annotated iff an appended tail line (any line after the base line count of **its file**) …" | Both dead tokens occur in **both** LOG and SCORECARD (measured); whether a tail in LOG alone annotates the SCORECARD occurrence is unspecified | No; the spec already demands the executor state the exact rule — the integrator should check the stated rule covers both files |

## Verdict

The freeze is **sound in its measurements**: every base receipt re-derives exactly (c66, c70, c72, sweep, census), both dead tokens are dead at base for the disclosed reason (with the mechanism stated more precisely than the contract's phrasing), the C2 do-nothing control reaches its target with margin (**c72 accepts 9 of 11 attack lines; k=9 ≥ 1 — the claim is not void**), the C3 re-pin is demonstrated sufficient (exit 2 → exit 1, zero Error lines, exactly one field changed), and no contract reference dangles. The defects are concentrated in the **delivered-counter interface**: F-A (spec selftest labels contradicting `dead ≥ 2`) is the one finding that can silently void C1 if the executor follows the spec literally, and it must be adjudicated before the integrator commits `c73_wave_pointers.py`. F-B/F-D/F-E are wording defects that should be corrected in the round's narrative, not in the frozen bytes.

Scratch tree `/fast/scratch/hyaku/kake-r73/CriticClaims/` deleted before yield (verified below).
