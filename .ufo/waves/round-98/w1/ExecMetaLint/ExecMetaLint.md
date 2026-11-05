# ExecMetaLint — R98-D1 knowledge meta-text gate

Seat: ExecMetaLint (executor, leaf). Lane tip read: `git -C LANE rev-parse master` = `7838981e4e40280176085e8aa1f6827eb7133a69`.
Report path note: the spec names `w1/ExecMetaLint.md`; the hard bound confines writes to `w1/ExecMetaLint/`, so the report lives here.

## Deliverables (all in this directory)

| file | content |
|---|---|
| `knowledge_metatext_lint.py` | stdlib gate; reads `git show <rev>:<path>` for `corpus/knowledge/*.md` (or `--dir`); `--selftest`; exit 0 clean / 1 gate finding / 2 setup |
| `selftest.txt` | `selftest 13/13`, rc 0 |
| `at-master.txt` | master scan, rc 1, `gate_findings=1 review_hits=146` |
| `fixture-fixed.txt` | scratch-clone fixture with line 130 removed, rc 0, `gate_findings=0 review_hits=145` |
| `dir-leak.txt` | `--dir` over a copy of master's `revalidation-exchange.md`, rc 1 |
| `bad-rev.txt` | `--revision no-such-rev`, rc 2 |

## Design: two tiers, nothing suppressed silently

- **GATE** (fails exit 1): text only a drafting or integration handoff produces.
  `drafted-by` (`Drafted by`), `word-count-receipt`, `receipt-file` (`quotes-verified.txt`), `body-word-count` (`body is N words`), `l1-integrates` (`the L1 integrates`), `heading-unbalanced-backtick` (heading with an odd backtick count, i.e. a truncated tail), `unclosed-fence`.
- **REVIEW** (printed as `review:`, never fails the gate): provenance voice the corpus's own `verified-at:`/`source:` convention uses. `this-seat`, `seat-id` (known role prefix + CapitalisedName), `seat-scratch-path` (`.ufo/waves/round-N/w1/`), `l1-integrates-future` (`L1 integrates`, not `the L1 integrates`).
- Fenced code (``` and ~~~, with CommonMark closer rules) is exempt in both tiers.

Why two tiers: the first draft put `this seat` and `w1/` citations into the gate. Master then gave 148 hits, about 20 entries whose `verified-at:` lines legitimately say "this seat re-opened…" and cite receipts. Those are provenance, not handoff copy, so they moved to REVIEW with the judgement recorded below.

## Verdicts (command, observed rc)

- `python3 -B knowledge_metatext_lint.py --selftest` → rc 0, `selftest 13/13`. Fixtures: P1 the line-130 shape, P2–P6 gate positives, R1–R2 review positives, N1–N5 negatives (quoted meta-text inside a backtick fence, a tilde fence, near-miss prose such as "Execution", "Critical", "Scoutable", a longer-closer fence, and "seat belt").
- `--root LANE --revision master` → rc 1. Gate: exactly one finding, `corpus/knowledge/revalidation-exchange.md:130`, rules `drafted-by,word-count-receipt,receipt-file,body-word-count,l1-integrates,heading-unbalanced-backtick`. This is the expected finding.
- Fixture: `git clone --shared` into `fx`; `git rev-parse --show-toplevel` equalled the fixture dir; one commit deleting line 130 (`fixture: remove leaked meta-text line 130`, identity via `-c`, 1 deletion). `--revision HEAD` → rc 0, `gate_findings=0`. The lane tip was not touched (`master` still `7838981e`).
- `--dir` over the master copy → rc 1 (`gate_findings=1`). `--revision no-such-rev` → rc 2. `--dir` nonexistent → rc 2.

## Review tier at master (146 hits; judged by class, not line by line)

| rule | hits | judgement |
|---|---|---|
| this-seat | 25 lines / 13 files | provenance first-person ("this seat re-opened the RFC body"), in `verified-at:` lines and prose. Not handoff copy. **False positive for the gate**, kept visible. |
| seat-scratch-path | 54 | receipt citations `.ufo/waves/round-N/w1/...`, the corpus's sanctioned evidence form. **False positive for the gate.** |
| seat-id | 120 | mostly provenance ("wave-1 seat `ScoutX`"). Four hits are systemd `ExecStart=` tokens (`keeper-timer-inert.md`, `ops-automation.md`, `free-read-verbs.md`), a **pattern false positive**. |
| l1-integrates-future | 1 | `referrer-policy-effective.md:19` "After L1 integrates the candidate, the planned command is:". A planned-step note addressed to the lead inside an entry. **Borderline; a real-or-not call for the L1.** Not gated because the planned command is verification content. |

Note: the `ReviewCapA` / `ReviewCapB` review-seat rule of C1 does not apply here. This is a judgement list for the L1.

The one gate-tier hit on master (line 130) is a **real** finding. It is a seat's drafting tail, a malformed duplicate heading, and an unbalanced backtick. This seat did not edit `corpus/knowledge/` (the removal belongs to the L1 under R98-D1).

## Known limits

1. The gate is a closed list. A handoff paraphrased outside the listed phrases ("for the integrator", "L1 will fold this in") passes. The heading rule catches only an odd backtick count, so a clean-backtick heading with handoff prose also passes.
2. The REVIEW tier is noisy by design (146 hits at master). A human reads it; the gate does not.
3. The gate is not yet wired into any runner or the SKILL.md registry. That wiring is the L1's to do; this seat wrote no fleet-root or registry file.
4. The fixture proof is a single-line deletion. It shows the gate's exit flips with the defect, not that every class is caught.

## Tooling

No tools installed or upgraded. Python 3 stdlib only; `git` read-only plus fixture clone. No sysctl, pacman, PATH or fleet-root writes.

## Hand-off checks for the main agent

- Re-run `python3 -B .ufo/waves/round-98/w1/ExecMetaLint/knowledge_metatext_lint.py --selftest` (expect `selftest 13/13`, rc 0) and `--root . --revision <integrated tip>` (expect rc 0 once line 130 is removed).
- Decide the L1 call on `referrer-policy-effective.md:19` (review tier).
- Wire the gate into the lane's gate list if it is to run on every integration.

EXEC-METALINT selftest=13/13 master_findings=1 fixed_exit=0
