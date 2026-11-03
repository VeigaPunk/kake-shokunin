# MutC2 — round-72 C2 counter mutation test

**Verdict: mutants=8 killed=6 survived=2.** Both survivors are one class: the `PHRASE` constant is not
pinned by any of the four legs (any substring/superstring of the dated-absence phrase keeps all four exits
correct). No other clause mutation survives.

Frozen input: `.ufo/waves/round-72/c72_tmp_v2.py` at freeze commit `a19d38ea`.
sha256 `af2f0c9c6b7ba04facdf63397b1e2e66ca20dd464984745354409d91fcf6e6ca`, identical to
`git show a19d38ea:.ufo/waves/round-72/c72_tmp_v2.py | sha256sum` before and after every run (the frozen
file was never edited; each mutant is a separate copy). Scratch `/fast/scratch/hyaku/kake-r72/MutC2`
deleted before yield.

## Frozen-bytes baseline (all four legs, before any mutant)

| leg | command | observed | required |
|---|---|---|---|
| selftest | `python3 -B c72.py --selftest` | `C2v2 selftest 11/11`, exit 0 | exit 0 |
| J3 control | `python3 -B c72.py --lane <j3clone> --revision 1c21a39a…` | exit 1, `findings=[(27, 0, 1, 0)]` | exit 1 |
| base (red-before) | `python3 -B c72.py --lane <lane> --revision cc6b4e0b…` | exit 1, `command_findings=2 prose_findings=5` | exit 1 |
| tip | `python3 -B c72.py --lane <lane> --revision 3c68645a…` | exit 0, `findings=[]` | exit 0 |

J3 fixture built by copying `controls/j3-control.sh` logic (no `rm` from the script): `git clone --shared`
of the lane, `checkout -q 3c68645a`, line 27 replaced verbatim with
`cp state/probe-latest.json /tmp/kake-r12/live/probe-latest.backup.json (historical record, not an executable instruction)`,
committed `-c user.name=kake-scratch -c user.email=kake@scratch.local` →
`J3_CONTROL_COMMIT=1c21a39a9356ba55fe0bcab4817030df8a341e21` (toplevel asserted = clone dir).
Fixture validity: round-71 counter on it → `C2 revision=1c21a39a… met=True`, exit 0 (accepted, as the
control requires).

## Mutants (each a single hunk, verified `diff -u | grep -c '^@@'` = 1)

| mutant | single change | selftest | J3 | base | tip | verdict |
|---|---|---|---|---|---|---|
| M-a | `brace = len(brace_spans)` → `brace = 0` | 10/11 exit 1 | 1 | 1 | 0 | killed by selftest (`brace_default_is_finding`) |
| M-b | `command += 1` → `command += 0` | 8/11 exit 1 | **0** | 1 | 0 | killed by selftest + J3 |
| M-c | `imperative = …` → `imperative = False` | 10/11 exit 1 | **0** | 1 | 0 | killed by selftest + J3 |
| M-d | `in_cmd_span = any(…)` → `in_cmd_span = False` | 9/11 exit 1 | 1 | 1 | 0 | killed by selftest |
| M-e | `guard_ok = all(…)` → `guard_ok = True` | 10/11 exit 1 | 1 | 1 | 0 | killed by selftest (`guard_added_token_needs_phrase`) |
| M-f | `PHRASE = "not an executable instruction"` → `PHRASE = "historical record"` | 11/11 exit 0 | 1 | 1 | 0 | **SURVIVED** |
| M-g | `if in_cmd_span or imperative:` → `… and not annotated:` | 9/11 exit 1 | **0** | 1 | 0 | killed by selftest + J3 |
| M-h | `PHRASE = "not an executable instruction"` → `PHRASE = "not an executable"` | 11/11 exit 0 | 1 | 1 | 0 | **SURVIVED** (same class as M-f) |

Failing selftest cases (exact):
- M-a: `brace_default_is_finding`
- M-b: `j3_phrase_only_on_command_is_command_finding`, `imperative_line_token_is_command_finding`,
  `v1_accepted_j3_rejected_here`
- M-c: `imperative_line_token_is_command_finding`
- M-d: `j3_phrase_only_on_command_is_command_finding`, `v1_accepted_j3_rejected_here`
- M-e: `guard_added_token_needs_phrase`
- M-g: `j3_phrase_only_on_command_is_command_finding`, `v1_accepted_j3_rejected_here`

Kill-power per leg: selftest 6/8, J3 3/8 (all also selftest-killed), base 0/8, tip 0/8. The base leg is red
only for prose/command reasons (`prose=5`, `command=2`; no brace token at `cc6b4e0b`), and the tip is green
under every detection-clause mutant, so neither leg can kill a clause mutation; the selftest is the only
killing leg except for the phrase constant.

## Survivor M-f — `PHRASE = "historical record"`

Why it survives: `PHRASE` feeds both `annotated = PHRASE in line` and the added-line guard. Every
dated-absence annotation at the tip contains the substring `historical record`, so the tip stays green;
the J3 line is an imperative command line, so its annotation is irrelevant and J3 stays red; base lines
carry no annotation, so base stays red. The two selftest fixtures that exercise annotation
(`prose_annotated_ok`, `guard_annotated_addition_ok`) use lines containing **both** substrings, so they
cannot distinguish the full absence phrase from the substring.

Counterexample (function-level, frozen vs M-f):

```
line_findings("see /tmp/kake-rX/ (historical record only)")
    frozen -> (0, 0, 1)   M-f -> (0, 0, 0)
guard on added line "new /tmp/kake-rX note (historical record)"
    frozen -> guard_ok=False   M-f -> guard_ok=True
```

M-f therefore tolerates a prose token on a line annotated only `historical record`, and lets an added
token line through the guard with that annotation — the contract's predicate says prose is tolerated only
when the line carries `not an executable instruction`. This is a coverage finding about the frozen
selftest (no case whose annotation text holds only one candidate phrase), not a change to the contract.

## Survivor M-h — `PHRASE = "not an executable"` (truncation, same class)

Same mechanism: the truncated phrase is a substring of every real annotation, so tip stays green and the
other legs are unaffected. Counterexample:

```
line_findings("see /tmp/kake-rX/ (not an executable command, ignore)")
    frozen -> (0, 0, 1)   M-h -> (0, 0, 0)
guard on added line "new /tmp/kake-rX note (not an executable)"
    frozen -> guard_ok=False   M-h -> guard_ok=True
```

## Evidence commands (all exit codes as printed)

```
git -C <lane> show a19d38ea:.ufo/waves/round-72/c72_tmp_v2.py > $S/c72.py ; sha256sum  # af2f0c9c…
python3 -B $S/c72.py --selftest                                    # 11/11, exit 0
python3 -B $S/c72.py --lane $S/j3clone --revision 1c21a39a…        # exit 1
python3 -B $S/c72.py --lane <lane> --revision cc6b4e0b…            # exit 1
python3 -B $S/c72.py --lane <lane> --revision 3c68645a…            # exit 0
python3 -B <lane>/.ufo/waves/round-71/c71_tmp.py --lane $S/j3clone --revision 1c21a39a…  # exit 0, met=True
# per mutant m in mut_M{a..h}.py: the same four runs; table above
diff -u $S/c72.py $S/mut_M*.py                                     # 1 hunk each
sha256sum $S/c72.py                                                # af2f0c9c… (unchanged)
```

Restoration: the frozen copy was never modified (before/after hash equal, and equal to the lane's committed
bytes at `a19d38ea`); every mutant is a distinct file. Scratch `/fast/scratch/hyaku/kake-r72/MutC2`
removed before yield (including the J3 clone).

No tool installs or upgrades were needed or performed (pacman untouched; no uv/npx/binary installs).
