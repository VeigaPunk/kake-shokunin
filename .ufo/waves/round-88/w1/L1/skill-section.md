## Round 88 — conservative Vary matching and the r87 defect queue

`corpus/knowledge/vary-matching.md` (S463, RFC9111 §4.1) supplies the match
decision table, the conservative asymmetry and the runnable checklist.
`corpus/knowledge/gate-agreement-metadata.md` carries the provenance trio the
r84-86 ledger JSON cannot open with (round-87 routed defect R1); the ledger
bytes and the round-87 frozen instrument are unchanged.

| Name | Kind | Entry command | Verdict map | Selftest | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| vary_match | probe | `printf '%s' '<payload>' \| python3 -B scripts/vary_match.py` with stdin JSON `{vary,stored,presented}` | 0 clean/decided (stdout `match` or `mismatch`); 1 failed/invalid_input on stderr; a decision is not a cache-key, storage, revalidation or serving permission | `TMPDIR=$(mktemp -d) python3 -B scripts/vary_match.py --selftest` | `.ufo/waves/round-88/vary-cases.json` (20 frozen cases) and the seeded 200-input differential population inside `.ufo/waves/round-88/c88_vary.py` | stdin/stdout/stderr only; selftest runs isolated in-memory fixtures | kake |
| c88 defect queue | gate | `python3 -B .ufo/waves/round-88/c88_defect_queue.py --root . --revision <rev> --work <explicit-scratch>` | 0 clean/met; 1 failed/not-met; other nonzero could-not-evaluate | `python3 -B .ufo/waves/round-88/c88_defect_queue.py --selftest` | `.ufo/waves/round-88/frozen/{base-gate-agreement-ledger.json,base-cache-current-age.md,base-cache_current_age.py}` frozen at base f4479c14 | reads the committed revision; writes/deletes one tool file under the explicit work dir | kake |
| c88 vary capability | gate | `python3 -B .ufo/waves/round-88/c88_vary.py --root . --revision <rev> --work <explicit-scratch>` | 0 clean/met; 1 failed/not-met | `python3 -B .ufo/waves/round-88/c88_vary.py --selftest` | `.ufo/waves/round-88/vary-cases.json` plus the counter's seeded generator and reference | reads the committed candidate; writes/deletes one tool file under the explicit work dir | kake |

`scripts/cache_current_age.py` keeps its round-87 row; round 88 changes only its
`invalid_input` message so it names the offending JSON type (`float`,
`boolean`, ...). Arithmetic, exits and the 61-fixture selftest are unchanged and
re-run in `.ufo/waves/round-88/controls/`. The counter enforces that item
behaviorally (exit, message, six-term arithmetic, selftest), not by prose.
