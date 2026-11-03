# ExecJ3Variants — round-72 C2 counter on five SKILL.md line-27 variants

**Verdict: `variants_matching_expectation=5 of 5`.** `c72_tmp_v2.py` rejects the three
command-bearing line-27 variants (V1, V2, V5) and accepts the two prose variants (V3, V4);
the frozen `c71_tmp.py` accepts all five. Base `3c68645a` and lane HEAD `a19d38ea` are green
under both counters. One evidence-backed boundary is recorded at the end: c72's command test is
a finite first-word list, so `env cp …` / `xargs …` command lines are accepted.

All work ran in scratch clones under `/fast/scratch/hyaku/kake-r72/ExecJ3Variants`; the lane
was never mutated (only this report was written into it).

## Table

| Variant | form (line 27 payload) | c71 exit | c72 exit | expected c72 | matches |
|---|---|---|---|---|---|
| V1 | imperative line, first word `cp` | 0 | 1 | 1 | yes |
| V2 | imperative line, first word `python3` | 0 | 1 | 1 | yes |
| V3 | prose, first word `Roster` | 0 | 0 | 0 | yes |
| V4 | prose, first word `the`, `cp` mid-sentence | 0 | 0 | 0 | yes |
| V5 | table row, backticked span `cp a /tmp/…` | 0 | 1 | 1 | yes |

Exact payloads (whole line 27 replaced, base `/tmp/` token asserted present first):

```
V1: cp state/probe-latest.json /tmp/kake-r12/live/x.json (historical record, not an executable instruction)
V2: python3 -B scripts/x.py --out /tmp/kake-r12/out.json (not an executable instruction)
V3: Roster note: the snapshot was under /tmp/kake-r12/live/ (historical record, not an executable instruction)
V4: the snapshot was under /tmp/kake-r12/live/ and cp is not used here (historical record, not an executable instruction)
V5: | x | `cp a /tmp/kake-r12/b` (historical record, not an executable instruction) |
```

Variant commits (detached checkout of `3c68645a` + one-line commit, `kake-scratch
<kake@scratch.local>`):

```
V1 db51f7eb60d7b24e081a22e3a7cbfccbcdefd93e
V2 d594c84fe83fdf40e3dcf5a84826411f7f2beb88
V3 c2d72de74610af1fbcb438693f40f5a9ac8d4ba8
V4 79f7a3a03e640b0328347654427b82020403daf1
V5 7c464c1d2adbf4d8482e772f66ff1b8abeb9e5aa
```

Each clone's diff vs base is exactly one file, one insertion, one deletion
(`git -C $S/vN diff --numstat 3c68645a HEAD` → `1  1  SKILL.md` for all five); each clone's
`git rev-parse --show-toplevel` was asserted equal to the clone dir (realpath) before the first
commit.

## Counter evidence (commands, exact findings lines, exit codes)

Command shape, run once per variant with `N` and `<hash>`:

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-72/c72_tmp_v2.py \
  --lane /fast/scratch/hyaku/kake-r72/ExecJ3Variants/VN --revision <hash>
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-71/c71_tmp.py \
  --lane /fast/scratch/hyaku/kake-r72/ExecJ3Variants/VN --revision <hash>
```

c72 findings lines (`findings` tuple = `(line, brace, command, prose)`):

```
V1 exit 1: C2v2 revision=db51f7eb… brace_findings=0 command_findings=1 prose_findings=0 findings=[(27, 0, 1, 0)] removed=7 added=7 guard=ok met=False
V2 exit 1: C2v2 revision=d594c84f… brace_findings=0 command_findings=1 prose_findings=0 findings=[(27, 0, 1, 0)] removed=7 added=7 guard=ok met=False
V3 exit 0: C2v2 revision=c2d72de7… brace_findings=0 command_findings=0 prose_findings=0 findings=[] removed=7 added=7 guard=ok met=True
V4 exit 0: C2v2 revision=79f7a3a0… brace_findings=0 command_findings=0 prose_findings=0 findings=[] removed=7 added=7 guard=ok met=True
V5 exit 1: C2v2 revision=7c464c1d… brace_findings=0 command_findings=1 prose_findings=0 findings=[(27, 0, 1, 0)] removed=7 added=7 guard=ok met=False
```

c71 lines (all five exits 0; phrase annotation alone keeps `unannotated_tokens=0`):

```
V1..V5: C2 revision=<hash> tokens_total=7 unannotated_tokens=0 unannotated_lines=[] removed=7 added=7 guard=ok met=True
```

So the c71→c72 delta on these five is exactly the command-form class: c71 exit 0 / c72 exit 1
on V1, V2, V5; identical 0/0 on the prose V3, V4. No variant changed the guard leg
(`guard=ok` in every run), so no rejection here is an annotation-loss artifact.

### Base and lane HEAD

```
python3 -B …/round-72/c72_tmp_v2.py --lane /home/vgpnk/Projects/shokunin/kake-shokunin --revision 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1
  exit 0: C2v2 revision=3c68645a… brace_findings=0 command_findings=0 prose_findings=0 findings=[] removed=7 added=7 guard=ok met=True
python3 -B …/round-71/c71_tmp.py --lane … --revision 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1
  exit 0: C2 revision=3c68645a… tokens_total=8 unannotated_tokens=0 unannotated_lines=[] removed=7 added=7 guard=ok met=True
python3 -B …/round-72/c72_tmp_v2.py --lane … --revision HEAD   # lane HEAD = a19d38ea
  exit 0: C2v2 revision=HEAD brace_findings=0 command_findings=0 prose_findings=0 findings=[] removed=7 added=7 guard=ok met=True
python3 -B …/round-71/c71_tmp.py --lane … --revision HEAD
  exit 0: C2 revision=HEAD tokens_total=8 unannotated_tokens=0 unannotated_lines=[] removed=7 added=7 guard=ok met=True
```

(`tokens_total=8` at base/HEAD vs `7` in the variants is the replaced line losing one of its two
tokens; not a behavioral delta.)

### Able-to-fail checks (read-only on the same clones)

```
c72 --selftest  → exit 0, "C2v2 selftest 11/11"
c72 --lane $S/V3 --revision cc6b4e0b8c35e72dfb02c6184b847f68c1262153 → exit 1
  C2v2 revision=cc6b4e0b… brace_findings=0 command_findings=2 prose_findings=5
  findings=[(27, 0, 0, 1), (95, 0, 0, 1), (227, 0, 0, 1), (356, 0, 0, 1), (359, 0, 0, 1), (463, 0, 1, 0), (464, 0, 1, 0)]
  removed=0 added=0 guard=ok met=False
c71 --lane $S/V3 --revision cc6b4e0b… → exit 1
  tokens_total=7 unannotated_tokens=7 unannotated_lines=[27, 95, 227, 356, 359, 463, 464] met=False
```

## Counterexample / boundary (outside the five expectations)

c72's `command` branch keys on a finite first-word set (`node python python3 cp mv git curl npx
uv bash sh diff cat ls grep mktemp test`) in a backticked span or as the line's first word.
Two extra probe clones exercised executable lines that evade it because the first word is not in
the set — both accepted, `findings=[]`, `met=True`, c72 exit 0:

```
P1 62a93c1f…: env cp state/probe-latest.json /tmp/kake-r12/live/x.json (historical record, not an executable instruction)
P2 3dfe5b5b…: xargs -I{} cp {} /tmp/kake-r12/live/ (historical record, not an executable instruction)
```

These are labeled probes, not variants: they do not change `variants_matching_expectation=5 of 5`.
Recorded because the operability claim is about the J3 command-form class, and this is its
observable boundary — an `env`/`xargs`-prefixed copy still passes, as would any interpreter or
wrapper word absent from the list.

## Conformance

- Lane read-only: no edit/commit/checkout/reset in `/home/vgpnk/Projects/shokunin/kake-shokunin`;
  only this report file was created there. All clones lived in the seat scratch tree.
- Counters were run unmodified; no frozen file was edited.
- No tools installed or upgraded; nothing to record under the operator tooling directive.
- Scratch tree `/fast/scratch/hyaku/kake-r72/ExecJ3Variants` deleted before yield (all clones and
  `results.json`).
