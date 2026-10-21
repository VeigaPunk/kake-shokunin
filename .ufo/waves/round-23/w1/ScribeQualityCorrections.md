# ScribeQualityCorrections — round 23 (w1)

Author-side scribe. Not an independent admission. Lane read-only: this file is the only write. observedAt: 2026-10-21. Lane HEAD observed: `4e7dd1d` (`round-23: correct routed round-22 defects ...`), which already carries a correction register in `corpus/QUALITY.md` and the misroot move. Scratch: `/tmp/kake-r23-ScribeQualityCorrections-Y0Ty` (probe outputs only; counter-probe temp clones removed by its own `TemporaryDirectory`).

## Verdict

- Note 1 (inverted `counter-probe.py` predicate): verified defect, already corrected in `corpus/QUALITY.md` lines 117–133 by `4e7dd1d`. The committed text is accurate. Holds.
- Note 2 (lane-root `err.txt`/`out.txt`): verified moved byte-identically to `.ufo/waves/round-22/residual/misroot/`. The lesson's own sentence still says "fleet root" (lesson line 34) and needs an append-only tail. Open, P3.
- Note 3 (`/tmp/kake-r22a2/*_c0fd6d5.py` runners): verified; `.ufo/waves/round-22/postfix/REPRODUCE.md` (`4e7dd1d`) recreates both runners from Git and reproduces the receipts exactly. Digest labels verified. Holds.
- One additional freshness defect not named in notes 1–3: `postfix/defect-probe-after.json:123` names a mutable lane working-tree path whose bytes changed in round 23. Result still reproduces; receipt identity is not pinned. P2, open.

## Findings

### F1 — P2 — after-side receipt names a mutable working-tree validator (same class as note 3)

- Impacted claim: `postfix/defect-probe-after.json` "met 8/8" is attributed to a path that no longer holds the validator it was produced from.
- Exact command: `grep -n '"validator"' .ufo/waves/round-22/postfix/defect-probe-after.json`
- Exact output: `123:  "validator": "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py"`
- Exact command: `sha256sum scripts/canonical_audit.py` (lane worktree)
- Exact output: `d8acf75062ab61006a5fdf786d04deb0d54d0d15f19e11be09a80b57aa74ecac  scripts/canonical_audit.py`
- `git log -2 -- scripts/canonical_audit.py` → `4d95d2e round-23: evaluate body-only SVG/MathML ...` then `b539cc1 round-22: recovery fixes ...`. The round-22 pin is `git show b539cc1:scripts/canonical_audit.py | sha256sum` = `5de32200ea409349659180ab93d02d273c113008596d93834da94ef1c04a1c15` (matches `frozen/expected.json` pin recorded in the lesson).
- Re-run (read-only, temp files): `python3 .ufo/waves/round-22/postfix/defect-probe.py --validator <b539cc1 blob>` → `validator=b539cc1 exit=0 met 8 passed True`; same with HEAD blob (`d8acf750…`) → `validator=HEAD exit=0 met 8 passed True`.
- Smallest fix: append a correction pinning the receipt's validator to `git show b539cc1:scripts/canonical_audit.py` (sha256 `5de32200…`). [INFERENCE] the after receipt was produced from the b539cc1 blob because lane HEAD was b539cc1 at that time; the receipt does not record a digest, so this rests on the frozen pin.

### F2 — P3 — lesson line 34 misplaces the misroot files

- Impacted claim: lesson "Step-1 conformance" row (`corpus/lessons/round-22-verifier-spotcheck.md:34-36`).
- Exact command: `git --no-optional-locks show HEAD:corpus/lessons/round-22-verifier-spotcheck.md | sed -n '34,36p'`
- Exact output: `No step-1 conformance defect found. Misroot: fleet root `err.txt`/`out.txt` are` / `absent now (`ls` → no such file); `git show d5a0369:out.txt` is the`
- Observed: `git ls-tree --name-only d5a0369 | grep -E '^(err|out)\.txt$'` → `err.txt`, `out.txt` (lane repo root). `ls /home/vgpnk/Projects/shokunin/{err,out}.txt` → `No such file or directory` (fleet root absent now). `git ls-tree --name-only HEAD` shows neither at root.
- Smallest fix: append the tail correction in the draft below (corrects location wording; does not edit line 34).

### F3 — P3 — `/tmp` pointers in residual reports are outside note 3's named receipts

- Impacted claim: note 3 covers `postfix/{counter,defect}-probe-before.json` only. Residual reports at HEAD still cite tmpfs runners as evidence-shaped pointers: `grep -c '/tmp/kake-r22' HEAD -- .ufo/waves/round-22/residual` → `CritAdmission.md:3`, `ResRevCounter.md:2`, `ResRevNetPath.md:2`, `ResRevManifestFd.md:2`, `CritScope.md:1`, `ResRevCliUsage.md:1`, `ResRevSources.md:1`. `CritAdmission.md` itself states "`/tmp/kake-r22a2/` before-files no longer exist".
- Smallest fix: extend the register line to say receipts and residual reports; a tmpfs path is a pointer only. Optional for L1.

### F4 — P3 — the committed `QUALITY.md` register uses shorthand for the receipt path

- Impacted claim: `corpus/QUALITY.md` criterion writes `postfix/counter-probe.py`; the register line (commit `4e7dd1d`) does not name the full path.
- Smallest fix: the draft below names `.ufo/waves/round-22/postfix/counter-probe.py` explicitly. Optional.

## Draft correction text (append-only; for L1 to append — NOT written to the lane)

Intended destination: tail of `corpus/lessons/round-22-verifier-spotcheck.md` (after line 171). Original lines stay byte-identical.

````markdown

## Correction register — round 23 (routed notes 1–3)

Grounding: routed notes 1–3 above. Dated 2026-10-21; observed at lane HEAD `4e7dd1d`. Original lines are kept for history.

- **[r23-correction 2026-10-21, note 1]** Confirmed. `corpus/QUALITY.md` "Derived counts and resolver neighbours — round 22 recovery", first criterion, the sentence "Fails if `postfix/counter-probe.py` against the counter exits 0." inverts the predicate. `.ufo/waves/round-22/postfix/counter-probe.py` ends `return 0 if result["passed"] else 1`, and `passed` is true only when CE1, CE2 and CE3 are each rejected. Correct reading: the criterion fails when `python3 .ufo/waves/round-22/postfix/counter-probe.py --lane . --measure <counter>` exits nonzero. Receipts agree: `counter-probe-before.json` `passed:false`; `counter-probe-after.json` `passed:true`. The defect-probe sentence ("exits 1") is correct as written. The register is `corpus/QUALITY.md` §"Correction register — round 23" (commit `4e7dd1d`).
- **[r23-correction 2026-10-21, note 2]** The misroot copies were tracked at the lane repository root by `d5a0369` (`git ls-tree --name-only d5a0369` lists `err.txt` and `out.txt`), not at the fleet root. Blobs: `err.txt` `34e8da93a2cc93d0e6e128701c2bbeca77f0494c`; `out.txt` `edf522361b33050d32da3de6e5ea9be165a216da`. Commit `4e7dd1d` moved them unchanged (`rename ... (100%)`) to `.ufo/waves/round-22/residual/misroot/err.txt` and `.ufo/waves/round-22/residual/misroot/out.txt`. Line 34's sentence "Misroot: fleet root `err.txt`/`out.txt` are absent now" should be read as: lane-root copies (tracked by `d5a0369`) were moved by `4e7dd1d`; both are absent from the lane root (`git ls-tree --name-only HEAD`) and from the fleet root (`ls` → no such file). The `git show d5a0369:out.txt` command is a lane-repository path and stands.
- **[r23-correction 2026-10-21, note 3]** `postfix/counter-probe-before.json` (`/tmp/kake-r22a2/measure_c0fd6d5.py`) and `postfix/defect-probe-before.json` (`/tmp/kake-r22a2/canonical_audit_c0fd6d5.py`) name tmpfs runners that no longer exist; the path is a pointer, not evidence. Recreate from Git with `.ufo/waves/round-22/postfix/REPRODUCE.md` (commit `4e7dd1d`): `git show c0fd6d5:scripts/canonical_audit.py > "$T/canonical_audit_c0fd6d5.py"` and `git show c0fd6d5:.ufo/waves/round-22/measure.py > "$T/measure_c0fd6d5.py"`, then `python3 .ufo/waves/round-22/postfix/defect-probe.py --validator "$T/canonical_audit_c0fd6d5.py"` and `python3 .ufo/waves/round-22/postfix/counter-probe.py --lane . --measure "$T/measure_c0fd6d5.py"`. Observed 2026-10-21: defect-probe exit 1, `met 2 passed False`; counter-probe exit 1, CE1 exit 0 accepted 32 rejected false, CE2 exit 0 accepted 0 rejected false, CE3 exit 0 accepted 32 rejected false. Digests: validator `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7` (the `c0fd6d5` blob and its `frozen/expected.json` line 74 pin); measure `329f45b67b3610c5ac132ef53f3428ad8dc9c2dd065ec0a96834a08b71ab9c49`.
- **[r23-correction 2026-10-21, note 3 extension]** `postfix/defect-probe-after.json` line 123 names the mutable lane path `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py`, whose bytes are now `d8acf75062ab61006a5fdf786d04deb0d54d0d15f19e11be09a80b57aa74ecac` (commit `4d95d2e`). The round-22 validator is `git show b539cc1:scripts/canonical_audit.py` (sha256 `5de32200ea409349659180ab93d02d273c113008596d93834da94ef1c04a1c15`). Observed 2026-10-21: `met 8 passed True` with both the b539cc1 blob and HEAD. Residual reports that cite `/tmp/kake-r22a2*` are pointers only, not evidence.
````

## Checked and held

- `git show --stat --format='%h %an %cI%n%s' 4e7dd1d`: `corpus/QUALITY.md` +18/-0 (`git diff --numstat b5d599e 4e7dd1d -- corpus/QUALITY.md` → `18 0`); `REPRODUCE.md` +17; misroot `err.txt`/`out.txt` 100% renames.
- `counter-probe.py` source: `return 0 if result["passed"] else 1`; `passed = ce1_ok and ce2_ok and ce3_ok`. Exit 0 = all counter-examples rejected. Note 1 wording confirmed.
- `defect-probe.py` line 114: `return 0 if ok else 1`. Receipts: before `met 2 passed false`; after `met 8 passed true`. "exits 1" is correct as written in `QUALITY.md`.
- Misroot blobs: `git rev-parse d5a0369:err.txt` = `4e7dd1d:.ufo/waves/round-22/residual/misroot/err.txt` = `34e8da93…`; `out.txt` = `edf52236…`. `out.txt` content `{"findings":[],"pagesChecked":0,"verdict":"could-not-evaluate"}` matches lesson line 36.
- `REPRODUCE.md` recipe run verbatim: defect-probe `exit=1 met 2 passed False`; counter-probe `exit=1` with CE1 `(0,32,False)`, CE2 `(0,0,False)`, CE3 `(0,32,False)` as `(exit, accepted, rejected)`. Matches both before receipts.
- Digest labels: `git show c0fd6d5:scripts/canonical_audit.py | sha256sum` = `35433e50…`; `c0fd6d5` `frozen/expected.json` line 74 pins `35433e50…`; `c0fd6d5:.ufo/waves/round-22/measure.py` sha256 `329f45b6…`; `git show b539cc1:scripts/canonical_audit.py` = `5de32200…`. The `REPRODUCE.md` label "round-22 frozen pin before re-pin" is correct.
- `git show c0fd6d5:...` paths exist: `scripts/canonical_audit.py`, `.ufo/waves/round-22/measure.py`, `matrix.py`, `cases.json`. `BASE 7c61c8c...` used by counter-probe is present.
- After receipt `counter-probe-after.json:29` measure path = worktree `.ufo/waves/round-22/measure.py`, sha256 `fa916ada…` = the round-22 pin (`lesson` line 67 digest). Held.
- No `err.txt`/`out.txt` at lane root or fleet root (observed). No other lane file cites them except the lesson and the `residual/misroot` move.
- `measure.py` blob: `HEAD:.ufo/waves/round-22/measure.py` = `b539cc1:…` = `d2d75a82…` (git blob id, unchanged across round 23).

## Limits

- Lane read-only: nothing appended to `corpus/*`; the draft is for L1 to append. No commit, push, or git mutation was run (`git --no-optional-locks` read-only verbs, plus `git clone` inside the probe's own temp dir).
- Note-level freshness only: checks are local (git, receipts, probe scripts, filesystem). No web or live surface is in scope for notes 1–3; none was contacted.
- F1's "produced from b539cc1" is an inference from lane HEAD history; the receipt records no digest.
- The after-side re-runs used the current HEAD and b539cc1 validators, not the exact bytes the receipt observed at 03:15 (not recorded).
- Tools installed/updated: none. No pacman or host changes.
