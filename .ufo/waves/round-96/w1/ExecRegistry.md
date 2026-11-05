
## Round-96 ExecRegistry report (scoped findings)

Files changed (all inside w1/ExecRegistry/ only):
- .ufo/waves/round-96/w1/ExecRegistry/registry-rows.md (two draft rows as append-only diff vs SKILL.md line 218; no existing line modified)
- .ufo/waves/round-96/w1/ExecRegistry/resolution-receipts.txt (sha256 + cat-file + test -e + --help receipts)
- .ufo/waves/round-96/w1/ExecRegistry.md (this report)

Behavior: mirror-c95 8-column rows for c96_selfassess.py (battery=23/23, ng_pred_admits=3/3, c1caa585) and c96_reval.py (hand 37, generated 120, forgeries 6/6, mutants 14/14, d9c8f96e).

Exact retained evidence (observed rc):
- sha256sum of c96_selfassess.py a282da65… and c96_reval.py ec40aec1… match controls/instrument-sha256.txt; c1-surfaces.json c1caa585…, c2-population.sha256 d9c8f96e…, pos-good-reval.py 47c65725…, mutants-reval.json 517f7b16…, reval-contract-v1.md 65f0a347…, freeze.md d3eee8ee… (sha256sum pipeline rc=0; one expected sha256sum miss on scripts/reval_exchange.py in that pipeline — see receipts, absent vs HEAD, present in worktree only because uncommitted on this host; not named as a row path).
- git rev-parse --show-toplevel rc=0 prints lane root; git rev-parse HEAD rc=0 prints 049e8eca2f0fa5e981232eb4efe367357dce578c (freeze tip). git cat-file -e HEAD:<path> rc=0 for SKILL.md, both counters, freeze.md, reval-contract-v1.md, c1-surfaces.json, c2-population.sha256, pos-good-reval.py, mutants-reval.json and all six neg-*.py forgeries (15/15 OK); HEAD:scripts/reval_exchange.py ABSENT (expected per base-c2 control candidate=absent met=false; C2 author not yet landed at freeze tip).
- test -e rc=0 for all 8 row paths plus scripts/reval_exchange.py in worktree 9/9.
- python3 -B .ufo/waves/round-96/c96_selfassess.py --help rc=0; python3 -B .ufo/waves/round-96/c96_reval.py --help rc=0 (both flag sets parse, incl --selftest/--verdict-only).
- Row shape check: both drafted rows have exactly 9 pipe chars = 8 columns (asserted in the writer script rc=0); context line is byte-identical to SKILL.md line 218 (asserted in writer script rc=0).

Risks/blockers:
- scripts/reval_exchange.py not committed at freeze tip (ABSENT HEAD); the C2 row verdict map therefore cannot be replayed as met=true until the author lands the candidate. Not this seat's repair (frozen round; target untouched).
- No man page for gate registry shape beyond the c95 rows; draft mirrors them exactly.
- No tool installed (none needed). Scratch tree /fast/scratch/hyaku/kake-r96/ExecRegistry deleted before yield; receipts copied into w1/ExecRegistry first.

Verdict: EXEC-REGISTRY rows=2 resolved=8/8 (8 distinct round-96 paths named in the two rows, each cat-file OK at freeze tip; commands parse per --help rc=0).
