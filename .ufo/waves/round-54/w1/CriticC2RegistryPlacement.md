# CriticC2RegistryPlacement — can a fake c53 registry row outside the `Owned freshness gate registry` table pass C2?

**Answer: yes — twice over.** The registry check is *section-scoped*, not
*table-scoped*, and the window is keyed to the *first* occurrence of the
heading, so a fake row can sit (a) inside the section but outside the table,
or (b) outside the section entirely under a shadow copy of the heading. Both
pass `registry=present` and, with the manifest branch satisfied, full C2 exit 0.

## Instrument under attack

`.ufo/waves/round-54/c54_ops_debt.py`, committed bytes at `8e408e0`
(registry-scan logic byte-identical to the freeze commit `acae1dc`):

```
TABLE_HEADING = "### Owned freshness gate registry"
inside = False
for line in skill.splitlines():
    if line.strip() == TABLE_HEADING:   # start at FIRST heading, whitespace-tolerant
        inside = True; continue
    if inside and line.startswith("## "):
        break                            # terminates ONLY on "## " (level-2 + space)
    if inside and "c53_gate_truth.py" in line:
        registry_line = line             # FIRST line mentioning the name wins…
        registry_present = all(token in line for token in REQUIRED)  # …and decides
        break
```

REQUIRED = `("c53_gate_truth.py", "gate", "--revision", "0=", "--selftest", "exec-quality-gate", "read-only")` — all substring checks on that one line.

## Scope / termination conditions (observed)

- Window = lines after the **first** line that `strip()`-equals
  `### Owned freshness gate registry`, through the first subsequent line
  starting with `## ` (exactly two hashes + space) — or EOF.
- `###`/`####`/`#` headings, `##nospace`, blank lines, prose, HTML comments,
  and non-table `|` lines are all *inside* the window — no table membership
  test anywhere. The scan never looks at the markdown table structure.
- First line containing `c53_gate_truth.py` terminates the scan and alone
  decides `registry_present` — first-match-wins, single-line judge.
- Heading match is `line.strip() ==` so leading whitespace still counts, and
  a *duplicate* heading earlier in the file hijacks the window (the real
  section is never reached).
- Token check: `"gate" in line` is vacuous (substring of `c53_gate_truth.py`);
  `0=` matches `0=all`; tokens may live anywhere on the line, including
  inside `<!-- -->`.

## Counterexamples (sandbox `/tmp/kake-critic-c2`, `git clone --no-hardlinks` of the lane; lane checkout and jj/git index untouched)

Counters run: `frozen` = byte-exact committed counter from `8e408e0`;
`fixre` = same + the lane's own pending `MANIFEST_RE` backtick fix (the only
working-tree diff), needed because the committed regex never matches the
backticked names in `settlement.md` — so frozen exits 1 with
`manifest=incomplete` on every revision, while `registry=present/absent` is
the operative signal for this finding.

| Mutant (new commit on `8e408e0`) | Fake row location | Frozen | fixre |
|---|---|---|---|
| M2 `15b9ef0` | row under a **shadow `###` heading** inserted at line 12, outside the real section (real table never reached) | `registry=present`, exit 1* | `registry=present`, **exit 0** |
| M1 `58116bb` | **prose line inside the section** between heading and `| Name |` header — outside the table | `registry=present`, exit 1* | `registry=present`, **exit 0** |
| M3 `2a5855c` | `|` row at **EOF**, far outside the section | `registry=absent` | `registry=absent` |
| M4 `b32139e` | compliant real row (`read-only` added) + EOF fake | `registry=present` (real row) | `registry=present`, exit 0 |
| M5 `5da6e24` | bare `c53_gate_truth.py` **name mention** (no tokens) before the table + compliant real row | `registry=absent` | `registry=absent` — **false negative**: first match wins, compliant row never evaluated |

\* frozen exits 1 only because `MANIFEST_RE` cannot parse the backticked
manifest rows (`\| \`Name.md\` |`); that is a separate defect for
ReviewerC2Manifest. `registry=present` is printed under the frozen bytes.

Concrete passing fake (M2): `### Owned freshness gate registry` + blank +
`| c53-gate-truth | gate | `…c53_gate_truth.py --revision <commit>` | `0=all pass` | `… --selftest` | exec-quality-gate | read-only | kake |` placed *before* `## Property map` — outside the real section, yet captured.

## Related exposure observed during the run

- Landed real row at `8e408e0` (SKILL.md:213) lacks the literal token
  `read-only` → `registry=absent` at the landing commit even with the fixed
  regex; the lane's uncommitted working-tree edit adds "is read-only".
  P2.1 is not satisfied by committed bytes as of this wave (for the reviewer seat).
- Token-judge weakness: any prose/comment line carrying the seven substrings
  passes; an HTML comment `<!-- c53_gate_truth.py gate --revision 0= --selftest exec-quality-gate read-only -->` inside the window would also pass (same mechanism as M1; not separately committed).

## Smallest safe correction

1. Treat the row as a **table row**: after `TABLE_HEADING`, require the
   candidate line to match `^\s*\|.*\|\s*$` and require its **name cell**
   (`split("|")[1].strip()`) to equal `c53-gate-truth` — not a substring
   anywhere in the line.
2. Evaluate **all** candidate rows in the window; do not stop at the first
   name mention (fixes both the false-positive takeover and the M5 false
   negative). Fail if no name-matched row exists or if the matched row lacks
   a required cell value.
3. Terminate the window on **any** heading (`^#{1,6} `) and on the first
   non-table line after the table starts — a `### ` sibling section should
   close the table, and the row must live between the separator line and the
   table's last `|` line.
4. Anchor the heading once: verify `TABLE_HEADING` occurs exactly once
   (`skill.count(TABLE_HEADING) == 1`), so a shadow heading can't hijack the
   window.

Impact: C2's `registry row present` condition currently certifies placement
it does not check; the claim's own wording ("the SKILL.md gate-registry
**table** has a row") is stronger than the instrument. Fixable defect —
tighten the scanner before the counter is trusted as C2 evidence.

No installs. Lane tree, shared checkout, and lane jj/Git index untouched;
all mutations confined to `/tmp/kake-critic-c2` (disposable clone) and
`/tmp/c54_ops_debt_*.py` (byte-extract + disclosed regex variant).
