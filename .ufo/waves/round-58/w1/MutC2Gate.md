# MutC2Gate

Mutation test of the frozen round-58 C2 counter `.ufo/waves/round-58/c58_resolver_cases.py` (sha256 `60c814aa…`, byte-identical at lane working tree and contract commit `fff3eea6`) by mutating the tool it scores: `scripts/id_resolver.py` at base `044048597d62f3199494b63b36e90dd57825e350` (lane working-tree copy is byte-identical to base; sha256 `25982446d2e647830269cfff0b4bebf7bf263dde57c4321d87eeb42f06461bee`).

Method: shared clone of the lane checked out at base under `/fast/scratch/hyaku/kake-r58/MutC2Gate/lane` (`rev-parse --show-toplevel` asserted before every commit); each mutant = one anchor string asserted to occur exactly once in the source, mutated, committed with `user.name=selftest <selftest@local>`, then the gate run `--root <clone> --revision <mutant sha> --work <scratch>`; pristine bytes rewritten back after each run and sha256-verified. 18 gate runs (pristine + 16 mutants + restored control), full stdout per run in `MutC2Gate.files/mutants.jsonl`, machine summary `MutC2Gate.files/summary.json`, harness `MutC2Gate.files/mutate.py`.

Baseline: pristine tool scores **7/12 met=False** — fails are exactly K1, K2, K3 (D1 fence-blind registry) and K4, K5 (F1 git-quoted paths); P1–P7 pass. Matches the round facts "base 7/12": the two disclosed false-green defects are open at base, the gate's base run is the red control. Kill criterion: mutant is KILLED when its tally changes from 7/12; a mutant still scoring exactly 7/12 SURVIVED.

## MUTANTS:

| id | mutation point (single) | tally | verdict | newly failing gate cases | mutant sha256 / commit |
| --- | --- | --- | --- | --- | --- |
| M01 | `ID_RE` `\d{3,}`→`\d{4,}` | 1/12 | KILLED | P1 P2 P3 P4 P6 P7 | `be56f130…` / `1172a8c2cf0b` |
| M02 | `ROW_RE` `^ {0,3}`→`^ {0,4}` | 5/12 | KILLED | P3 P6 | `a7795ac2…` / `85f40a54ada4` |
| M03 | `REGISTRY_HEADING_RE` `^##\s+`→`^#+\s+` (loosened) | 7/12 | SURVIVED | none | `b502e883…` / `6d9eeff9e92b` |
| M04 | `SECTION_END_RE` → never-match `(?!)` | 6/12 | KILLED | P6 only | `5c244fd2…` / `fc3a5fa3ac02` |
| M05 | sibling owner `sorted(...)` removed | 7/12 | SURVIVED (equivalent) | none | `04e8cb20…` / `37ebddf95210` |
| M06 | `--fleet` not-a-directory check removed | 5/12 | KILLED | P5 P6 | `d47f58d2…` / `7db143a2823e` |
| M07 | dangling exit `1`→`0` | 4/12 | KILLED | P3 P4 P6 | `67a56df8…` / `a121caf83be7` |
| M08 | url-match computation removed (`matched` always `[]`) | 6/12 | KILLED | P6 only | `b322ff1b…` / `e808c369cd33` |
| M09 | selftest tally printed `{passed + 1}/{total}` | 6/12 | KILLED | P6 only | `ac86f622…` / `9fa85a846a62` |
| M10 | `ID_CELL_RE` `\d{3,}`→`\d{4,}` | 2/12 | KILLED | P1 P2 P4 P6 P7 | `0a9c8a6a…` / `25437cdd49f2` |
| M11 | `URL_RE` scheme `https?`→`zzttps` (url-match never fires) | 6/12 | KILLED | P6 only | `5804a5dd…` / `08f7e08f8737` |
| M12 | `parse_cited` per-id path `sorted()` removed | 6/12 | KILLED | P6 only | `310893f4…` / `ae359f4a4a9f` |
| M13 | usage-error exit `64`→`65` | 6/12 | KILLED | P6 only | `a9090ccc…` / `7f082fdabad9` |
| M14 | dangling-id `sorted()` removed | 6/12 | KILLED | P6 only | `c8cb1656…` / `7817040ad339` |
| M15 | `--fleet` default `os.path.dirname(root)`→`root` | 7/12 | SURVIVED | none | `c019c1ac…` / `44e652e30ac9` |
| M16 | sibling suffix `"-shokunin"`→`"-shokuninX"` | 5/12 | KILLED | P4 P6 | `da15a6aa…` / `fdd8e0c37b7f` |

Score: 13 KILLED / 16. Gate-fixture cases (K*, P1–P5, P7) independently kill 6 mutants (M01, M02, M06, M07, M10, M16); the other 7 kills (M04, M08, M09, M11, M12, M13, M14) come solely through P6, i.e. the tool's own 49-case selftest, not from the counter's own fixtures. K1–K5 fail in every run including pristine, so they distinguish no mutant.

Restoration evidence: after every mutant the pristine bytes were rewritten and `sha256(scripts/id_resolver.py) == 25982446…` re-asserted (harness hard-fails otherwise; all 16 restored ok); final RESTORED-control gate run at base scores 7/12 with the identical K1–K5 fail set as PRISTINE-base. No lane file, lane git state, or sibling was touched; all commits happened in the seat clone only.

## SURVIVORS:

- **M03 — registry-heading level loosened (`^##\s+Registry\s*$` → `^#+\s+Registry\s*$`).** No gate case pins the heading level: every fixture (and selftest) uses exactly `## Registry`, and the only cases that exercise heading strictness (K1 fenced heading; trailing-text variant in the selftest) are either already red at base (K1) or live in the selftest and did not fail under the loosened pattern. A tool accepting `### Registry` (or `# Registry`) as the Registry section scores the same 7/12.
- **M05 — sibling owner sort removed.** Equivalent mutant: `sibling_dirs()` already returns `sorted(os.listdir(fleet))` and the owner set is built by iterating that ordered list, so owner order is invariantly alphabetical with or without the `sorted()` call. Neither the 12 gate cases nor the selftest can observe a difference; this is a tool redundancy finding, not a gate gap.
- **M15 — `--fleet` default changed from parent-of-root to root itself.** Every gate case and every selftest case passes `--fleet` explicitly (or a revision/fleet pair); the default-resolution branch is dead code to the entire counter, so the gate cannot see it.

## PROPOSED CASES:

1. **Heading-level strictness (kills M03):** registry file whose section header is `### Registry` (h3, same row table beneath) with the entry citing that row's id; expectation: the h3 heading does NOT open the Registry section, so the id is unregistered → exit 1, `^DANGLING S… ` and `ids_resolved=0`. (Mirrors the existing "4 spaces is code" boundary case, one level up.)
2. **`--fleet` default resolution (kills M15):** one fixture run without `--fleet`, lane directory placed directly under the work/fleet dir so the default (parent of `--root`) is the fleet holding a committed `alpha-shokunin` registry; expectation: `^DANGLING S… .*owners=alpha-shokunin ` exactly as P4. Current gate never omits the flag.
3. Optional, hardening only: a gate-owned url-match assertion (e.g. require `url-match=alpha-shokunin` in a P4-variant) would remove the P6-only dependence of M08/M11; today url-match breakage is caught only transitively via the tool's selftest inside P6.

VERDICT: gate is live but thin — 13/16 single-point tool mutants killed, 6 by its own fixtures and 7 only via the borrowed selftest in P6; M03/M15 expose real case gaps (heading level, --fleet default) and M05 is an equivalent mutant of a redundant sort.
