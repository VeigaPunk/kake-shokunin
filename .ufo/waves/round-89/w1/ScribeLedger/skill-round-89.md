# DRAFT — SKILL.md registry: new `## Round 89` section (ScribeLedger, wave 1)

Landing note for L1: the three rows landed in commit `28532540` sit inside the round-88 table
(`SKILL.md:1597` onward), which alters a filed table and gives round 89 no heading of its own. Move
the three rows out of that table into the section below; the round-88 table then returns to its base
bytes. The `cache_key` row's Selftest cell also needs the correction below: the tool has no selftest,
and `--selftest` is not a recognised argument (the candidate reads stdin; `--selftest` with stdin
`/dev/null` prints `invalid_input: input is not valid JSON` and exits 1).

## Round 89 — cache-key construction and the routed round-88 defects

`corpus/knowledge/cache-key-construction.md` (S464, S465) supplies the key-form table and the runnable
checklist. The offline reader `scripts/cache_key.py` builds the stored-response key from a supplied
URI, request header map and `Vary` value; it decides construction only, not storage, reuse,
revalidation, freshness or serving. Both counters are instruments whose `met` is not conformance (see
the round-89 lesson §Wave review).

| Name | Kind | Entry command | Verdict map | Selftest | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| cache_key | probe | `printf '%s' '<payload>' \| python3 -B scripts/cache_key.py` with stdin JSON `{uri,request_headers,vary}` | 0 clean (stdout `{"key": ...}`); 1 failed/invalid_input on stderr; a key is construction only, not a storage, revalidation, reuse or freshness decision | none in the tool (`--selftest` is not a recognised argument); the instrument that scores it is `c89_key.py` below | `.ufo/waves/round-89/c2-contract.md` (declared key form); `.ufo/waves/round-89/frozen/c2-cases.json` (16 frozen cases) | stdin/stdout/stderr only; writes nothing | kake |
| c89 defect queue | gate | `python3 -B .ufo/waves/round-89/c89_defect_queue.py --root . --revision <rev> --work <explicit-scratch>` | 0 clean/met; 1 failed/not-met (open items named in the JSON line); a 0 is not verified repair while the counter's items B, C, E and F carry the defects routed as RC-1, RC-2, RC-8, RC-9 and RC-10 | `python3 -B .ufo/waves/round-89/c89_defect_queue.py --selftest` (12/12) | `.ufo/waves/round-89/controls/base-c1.txt` (freeze-time receipt; the base revision now reads `open=5`, RC-1) | `--work` scratch only; reads the committed revision | kake |
| c89 key capability | gate | `python3 -B .ufo/waves/round-89/c89_key.py --root . --revision <rev> --candidate scripts/cache_key.py --work <explicit-scratch>` | 0 met (the instrument admits non-conforming candidates; R89-2); 1 not met | `python3 -B .ufo/waves/round-89/c89_key.py --selftest` (43/43; tests the counter's own reference against the contract's examples, not `scripts/cache_key.py`) | seed 89089; `.ufo/waves/round-89/frozen/c2-cases.json` (16); `.ufo/waves/round-89/controls/ctl-*.py` (five committed stubs) | `--work` scratch only; reads the committed candidate | kake |

`scripts/cache_current_age.py` and `scripts/vary_match.py` keep their round-87 and round-88 rows; round
89 changes neither tool.
