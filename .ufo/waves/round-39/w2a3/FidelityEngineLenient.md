# Fidelity: CtlEngineLenient (shape: lenient crawler reading, ~14 skipped sentences)

VERDICT: faithful shortcut. Materialized byte-for-byte; genuinely skips the advertised work on 3/3 constructed disagreements; keeps only surface lastmod syntax (no calendar/TZD) — consistent with the named shape, not a hidden strict validator.

## Materialization (mis-materialization check)
- `sha256sum .ufo/waves/round-39/a3-controls/w1a3/CtlEngineLenient.py` → `56652e5de6c76be1142d7c385f5baa0b98036c8a3e51c0eb8902cd803b77f0c0` — byte-equal to the fenced ```python block in `.ufo/waves/round-39/w1a3/CtlEngineLenient.md` and to the sha the seat claimed (verified by extraction + difflib, zero diff).
- `/fast/scratch/hyaku/kake-r39a3w1/CtlEngineLenient/control.py` exists (4282 B); no `l1-materialized.diff` there — this control is a fresh write, not a dead-w1 tweak, so no changed-line count applies. dead-w1/ contains 12 other bases only.

## Shape check
- Grep: no `requests|socket|urlopen|urllib.request|subprocess|exec(|eval(|lxml|gzip` — pure stdlib, offline. Import list: json, re, sys, ElementTree, pathlib, urllib.parse (line 1).
- Zero occurrences of `loc_not_absolute|loc_out_of_scope|loc_too_long|changefreq_invalid|priority_invalid|too_large|too_many_entries` in source — the control cannot emit them, honest saturation: every sealed case requiring one must fail.
- Skipped work enumerated: sentences 19, 20, 22, 23, 24 (both clauses), 25, 26, 27, 28→kept only as loose surface regex `ISO` (line 3), 29, 30, 31, 32 — 14 counting s24's two clauses separately; 13 counting whole sentences. `usable` (lines 20, 27–28) parses locs then is never consumed: dead scope machinery, shape as advertised.
- Kept: encoding (6–7), well-formedness + doctype (8–9), root (10), entries + unexpected + no_entries (11–13), loc presence (15), field repeats (16), unexpected children (17), manifest/check/verdict plumbing (3–5, 33–34).

## Constructed disagreements (correct tool must fail; control returns clean)
Sandbox `/fast/scratch/hyaku/kake-r39a3w2/FidelityEngineLenient/` (control.py copied, same sha). Command: `timeout 60s prlimit --as=4000000000 /usr/bin/python3 -B control.py --manifest t/<n>.json` (sitemapUrl `https://example.test/maps/sitemap.xml`):
- t1scope (s27): sitemapindex loc `https://other.test/x.xml` → `{"verdict":"clean",...findings:[]}` exit 0. Correct: `loc_out_of_scope`@1, failed-policy/1.
- t2vals (s29,31,32): `<lastmod>2026-02-30` + `<changefreq>sometimes` + `<priority>2` → clean/0. Correct: `lastmod_invalid` (Feb 30 never exists — freshness axis), `changefreq_invalid`, `priority_invalid`, all @1.
- t3many (s20): 50,001 valid url entries (2,450,118 B) → clean/0. Correct: `too_many_entries`@null, failed-policy/1.
3/3 disagree as required; exit codes observed 0/0/0.

## Seat's own fixtures cross-check (report [.ufo/waves/round-39/w1a3/CtlEngineLenient.md] [INFERENCE] 0/1/0/2)
valid→clean/0 ✓; malformed→`xml_malformed`@null, failed-policy/1 ✓; lenient→clean/0 ✓; invalid→`input_invalid`/2 ✓. All match.

## Operability edges
`control.py` (no args) → exit 64, no output; `--badflag` → 64; unreadable manifest → `input_invalid`/2; t/ file count 13 before and after all runs — writes nothing but stdout JSON (s1–2).

## Per attacked statement
- "L1 materializes the exact bytes" — holds (sha256 triple-match).
- "lenient crawler reading (14)" shape — holds: keeps structure/manifest/verdict, skips all value/scope/limit work; count 14 iff s24's clauses counted separately, else 13 (cosmetic).
- Seat [INFERENCE] fixture exits 0/1/0/2 — holds (all four reproduced).
- "loses operability, not a defect to repair" — holds: verified as control property, not a bug.

No installs (python3 3.14.8, timeout, prlimit preexisting). Key-blindness respected: no sealed paths, no counter run, no receipt fields beyond allowed read. Residual risk: none found; the shortcut is honest — it fails only where the shape says it must.
