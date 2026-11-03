# ScoutPointers — round 73, wave w1 (kake, attempt 1)

Status: **read-only reconnaissance report**.
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`
Base revision: `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc`
Assigned report path: `.ufo/waves/round-73/w1/ScoutPointers.md`
Tooling authorization: Operator directive 2026-10-19. No tools installed or upgraded (pacman paused host-wide; no `uv`, `npx`, or binary downloads required).
Seat scope: Leaf member. No subagent dispatch. No peer messaging. No git/jj mutations in lane checkout. All base bytes read via `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show <base>:<path>` or `git cat-file`. Scratch directory `/fast/scratch/hyaku/kake-r73/ScoutPointers/` cleaned before exit.

---

## 1. Inventory of Round-72 Receipt Pointers in LOG.md and SCORECARD.md

### 1.1 Scope of Extraction at Base `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc`

- **LOG.md scope**: The section starting at line 2498 (`## Round 72 — 2026-11-03 ...`) extending to the end of the file at line 2507 (no subsequent line starting with `## ` exists; `wc -l` confirms 2507 lines total).
- **SCORECARD.md scope**: Every line whose first table cell is `72` (lines 4818 and 4819).
- **Token filter**: Every pointer token beginning with `controls/`, `sources/`, or `w1/`.

### 1.2 Extracted Tokens and Existence Checks

Each occurrence was tested for existence at base revision `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc` under `.ufo/waves/round-72/` via:
`git -C /home/vgpnk/Projects/shokunin/kake-shokunin cat-file -e c1f3d8d4ed9470ecbaaf3353952a374b079e68cc:.ufo/waves/round-72/<token>`

| File | Line | Token | Target path under `.ufo/waves/round-72/` | Exit | Status |
|---|---|---|---|---|---|
| `LOG.md` | 2500 | `controls/c1-base.txt` | `.ufo/waves/round-72/controls/c1-base.txt` | 0 | LIVE |
| `LOG.md` | 2500 | `controls/c2-base-red.txt` | `.ufo/waves/round-72/controls/c2-base-red.txt` | 0 | LIVE |
| `LOG.md` | 2500 | `controls/c2-selftest.txt` | `.ufo/waves/round-72/controls/c2-selftest.txt` | 0 | LIVE |
| `LOG.md` | 2500 | `controls/c2-j3-control.txt` | `.ufo/waves/round-72/controls/c2-j3-control.txt` | 0 | LIVE |
| `LOG.md` | 2501 | `controls/c56-tip-linux.txt` | `.ufo/waves/round-72/controls/c56-tip-linux.txt` | 0 | LIVE |
| `LOG.md` | 2504 | `controls/j3-control.sh` | `.ufo/waves/round-72/controls/j3-control.sh` | 0 | LIVE |
| `LOG.md` | 2504 | `controls/c2-j3-control-r3.txt` | `.ufo/waves/round-72/controls/c2-j3-control-r3.txt` | 0 | LIVE |
| `LOG.md` | 2505 | `controls/c1-base.txt` | `.ufo/waves/round-72/controls/c1-base.txt` | 0 | LIVE |
| `LOG.md` | 2505 | `controls/c1-tip.txt` | `.ufo/waves/round-72/controls/c1-tip.txt` | 128 | **DEAD** |
| `LOG.md` | 2505 | `controls/c2-base-red.txt` | `.ufo/waves/round-72/controls/c2-base-red.txt` | 0 | LIVE |
| `LOG.md` | 2505 | `controls/c2-j3-control-r3.txt` | `.ufo/waves/round-72/controls/c2-j3-control-r3.txt` | 0 | LIVE |
| `LOG.md` | 2505 | `controls/c2-tip.txt` | `.ufo/waves/round-72/controls/c2-tip.txt` | 128 | **DEAD** |
| `SCORECARD.md` | 4818 | `controls/c1-base.txt` | `.ufo/waves/round-72/controls/c1-base.txt` | 0 | LIVE |
| `SCORECARD.md` | 4818 | `controls/c1-tip.txt` | `.ufo/waves/round-72/controls/c1-tip.txt` | 128 | **DEAD** |
| `SCORECARD.md` | 4819 | `controls/c2-tip.txt` | `.ufo/waves/round-72/controls/c2-tip.txt` | 128 | **DEAD** |
| `SCORECARD.md` | 4819 | `controls/c2-j3-control-r3.txt` | `.ufo/waves/round-72/controls/c2-j3-control-r3.txt` | 0 | LIVE |

### 1.3 Distinct Token Summary

Across the 16 extracted token occurrences, there are 9 unique tokens:
1. `controls/c1-base.txt`: **LIVE** (3 occurrences: `LOG.md:2500`, `LOG.md:2505`, `SCORECARD.md:4818`)
2. `controls/c1-tip.txt`: **DEAD** (2 occurrences: `LOG.md:2505`, `SCORECARD.md:4818`)
3. `controls/c2-base-red.txt`: **LIVE** (2 occurrences: `LOG.md:2500`, `LOG.md:2505`)
4. `controls/c2-j3-control.txt`: **LIVE** (1 occurrence: `LOG.md:2500`)
5. `controls/c2-j3-control-r3.txt`: **LIVE** (3 occurrences: `LOG.md:2504`, `LOG.md:2505`, `SCORECARD.md:4819`)
6. `controls/c2-selftest.txt`: **LIVE** (1 occurrence: `LOG.md:2500`)
7. `controls/c2-tip.txt`: **DEAD** (2 occurrences: `LOG.md:2505`, `SCORECARD.md:4819`)
8. `controls/c56-tip-linux.txt`: **LIVE** (1 occurrence: `LOG.md:2501`)
9. `controls/j3-control.sh`: **LIVE** (1 occurrence: `LOG.md:2504`)

Tokens starting with `sources/` or `w1/`: 0 occurrences found in the surveyed sections.

---

## 2. Nearest Real Replacements for Dead Tokens

The committed files under `.ufo/waves/round-72/` at base `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc` were inspected via `git ls-tree -r --name-only c1f3d8d4ed9470ecbaaf3353952a374b079e68cc .ufo/waves/round-72/`.

### 2.1 Dead Token: `controls/c1-tip.txt`
- **Cited in**:
  - `LOG.md:2505`: `C1 base agreement=24 mismatches=4 (controls/c1-base.txt) → landed-tip see controls/c1-tip.txt (agreement 25 required).`
  - `SCORECARD.md:4818`: `agreement 25 required at the landed tip (controls/c1-tip.txt; see the round report for the measured value at the final commit)`
- **Target queried**: `.ufo/waves/round-72/controls/c1-tip.txt`
- **Result**: Exit code 128 (`fatal: path '.ufo/waves/round-72/controls/c1-tip.txt' does not exist in 'c1f3d8d4ed9470ecbaaf3353952a374b079e68cc'`)
- **Nearest real replacement by name**:
  - Primary candidate: `.ufo/waves/round-72/controls/c1-tip-final.txt`
    - Exact command: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin cat-file -e c1f3d8d4ed9470ecbaaf3353952a374b079e68cc:.ufo/waves/round-72/controls/c1-tip-final.txt` → exit 0.
    - Content validation: `git show c1f3d8d4ed9470ecbaaf3353952a374b079e68cc:.ufo/waves/round-72/controls/c1-tip-final.txt` confirms line:
      `C1 gate-status members=28 evaluated=28 mismatches=3 structural=0 agreement=25 scores_held=3/3 met=True` with `exit=0`.
      This directly substantiates the claim of `agreement=25` at the landed tip.
  - Secondary/wave candidate: `.ufo/waves/round-72/w1/c1-relabel-tip.txt` (exit 0).

### 2.2 Dead Token: `controls/c2-tip.txt`
- **Cited in**:
  - `LOG.md:2505`: `tip exit 0 (controls/c2-tip.txt)`
  - `SCORECARD.md:4819`: `c72_tmp_v2.py selftest 11/11; J3 control c72_exit=1; base red exit 1; tip exit 0 (controls/c2-tip.txt)`
- **Target queried**: `.ufo/waves/round-72/controls/c2-tip.txt`
- **Result**: Exit code 128 (`fatal: path '.ufo/waves/round-72/controls/c2-tip.txt' does not exist in 'c1f3d8d4ed9470ecbaaf3353952a374b079e68cc'`)
- **Nearest real replacement by name**:
  - Primary candidate: `.ufo/waves/round-72/controls/c2-tip-final.txt`
    - Exact command: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin cat-file -e c1f3d8d4ed9470ecbaaf3353952a374b079e68cc:.ufo/waves/round-72/controls/c2-tip-final.txt` → exit 0.
    - Content validation: `git show c1f3d8d4ed9470ecbaaf3353952a374b079e68cc:.ufo/waves/round-72/controls/c2-tip-final.txt` confirms line:
      `C2v2 revision=5013c0ee87bda5fee03024488b4e293c4ca7ff16 brace_findings=0 command_findings=0 prose_findings=0 findings=[] removed=8 added=8 guard=ok met=True` with `exit=0`.
      This directly substantiates the claim of `tip exit 0`.

---

## 3. Grammar Analysis of `c70_pointer_audit.py` (Base Revision)

Source file: `.ufo/waves/round-70/c70_pointer_audit.py` committed at base `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc`.

### 3.1 Quoted Definitions: Token Classes and Parsing Regex

Lines 56–62 of `.ufo/waves/round-70/c70_pointer_audit.py`:
```python
56:CLASSES = (
57:    ('repo', re.compile(
58:        r'(?:^|[`(>|\s])((?:\.ufo|corpus|scripts|handoffs|considerthese)/'
59:        r'[A-Za-z0-9_./-]+\.[A-Za-z0-9]{1,16})(?![A-Za-z0-9])')),
60:    ('home', re.compile(r'(?:^|[`(>|\s])(~/[A-Za-z0-9_./+-]+)')),
61:    ('tmp', re.compile(r'(?:^|[`(>|\s])(/tmp/[A-Za-z0-9_.+-]+)')),
62:)
```

### 3.2 Quoted Definitions: File Input Scope (SCORECARD.md Only)

Lines 73–83 of `.ufo/waves/round-70/c70_pointer_audit.py`:
```python
73:def read_scorecard(root, revision):
74:    probe = git(root, ['rev-parse', '--git-dir'])
75:    if probe.returncode != 0:
76:        raise OSError('not a git repository: %s' % root)
77:    check = git(root, ['rev-parse', '--verify', '--quiet', revision + '^{commit}'])
78:    if check.returncode != 0:
79:        raise OSError('revision does not resolve: %s' % revision)
80:    show = git(root, ['show', revision + ':SCORECARD.md'])
81:    if show.returncode != 0:
82:        raise OSError('SCORECARD.md is not readable at revision %s' % revision)
83:    return show.stdout.decode('utf-8', 'replace')
```

### 3.3 Quoted Definitions: Repo-Root-Relative Resolution

Lines 108–119 of `.ufo/waves/round-70/c70_pointer_audit.py`:
```python
108:def is_dangling(root, revision, token, cls):
109:    if cls == 'repo':
110:        probe = git(root, ['cat-file', '-e', revision + ':' + token])
111:        if probe.returncode == 0:
112:            return False
113:        normalized = os.path.normpath(token)
114:        if normalized == token:
115:            return True
116:        probe = git(root, ['cat-file', '-e', revision + ':' + normalized])
117:        return probe.returncode != 0
118:    path = os.path.expanduser(token) if cls == 'home' else token
119:    return not os.path.exists(path)
```

### 3.4 Why Wave-Relative Tokens (`controls/c1-tip.txt`) Escape `c70_pointer_audit.py`

1. **Prefix Mismatch**: The `repo` class regex in lines 57–59 explicitly matches only tokens whose leading directory is one of `(?:\.ufo|corpus|scripts|handoffs|considerthese)/`. Tokens starting with `controls/`, `sources/`, or `w1/` are rejected by the regex and are never admitted into the `found` dictionary.
2. **Input Scope Blind Spot**: The counter reads only `SCORECARD.md` via `read_scorecard` (lines 73–83). All citations inside `LOG.md` are unread.
3. **Root-Relative Resolution**: Even if `controls/c1-tip.txt` were extracted by an expanded regex, `is_dangling` (line 110) tests `revision + ':' + token`, resolving against the repository root (`c1f3d8d4:controls/c1-tip.txt`). It does not prepend `.ufo/waves/round-72/`.

Consequently, wave-relative receipt tokens such as `controls/c1-tip.txt` and `controls/c2-tip.txt` are **strictly outside the grammar and scope** of `c70_pointer_audit.py`. Running `c70_pointer_audit.py` at base produces `unannotated=0 met=true` (exit 0) despite these dead self-assessment pointers.

---

## 4. Exercised Evidence Table

`$L` = `/home/vgpnk/Projects/shokunin/kake-shokunin`
`$B` = `c1f3d8d4ed9470ecbaaf3353952a374b079e68cc`

| # | Exact command | Exit | Key output line |
|---|---|---|---|
| E1 | `git -C "$L" show "$B:LOG.md" \| wc -l` | 0 | `2507` |
| E2 | `git -C "$L" show "$B:LOG.md" \| sed -n '2498,2507p' \| nl -ba -v 2498` | 0 | `2498 ## Round 72 — 2026-11-03 ...` through `2507 - **Not done this round.** ...` |
| E3 | `git -C "$L" show "$B:SCORECARD.md" \| grep -n "^\| *72 *\|"` | 0 | `4818:\| 72 \| calibration ...` and `4819:\| 72 \| operability ...` |
| E4 | `git -C "$L" cat-file -e "$B:.ufo/waves/round-72/controls/c1-base.txt"` | 0 | (no output; exit 0 confirms existence) |
| E5 | `git -C "$L" cat-file -e "$B:.ufo/waves/round-72/controls/c2-base-red.txt"` | 0 | (no output; exit 0 confirms existence) |
| E6 | `git -C "$L" cat-file -e "$B:.ufo/waves/round-72/controls/c2-selftest.txt"` | 0 | (no output; exit 0 confirms existence) |
| E7 | `git -C "$L" cat-file -e "$B:.ufo/waves/round-72/controls/c2-j3-control.txt"` | 0 | (no output; exit 0 confirms existence) |
| E8 | `git -C "$L" cat-file -e "$B:.ufo/waves/round-72/controls/c56-tip-linux.txt"` | 0 | (no output; exit 0 confirms existence) |
| E9 | `git -C "$L" cat-file -e "$B:.ufo/waves/round-72/controls/j3-control.sh"` | 0 | (no output; exit 0 confirms existence) |
| E10 | `git -C "$L" cat-file -e "$B:.ufo/waves/round-72/controls/c2-j3-control-r3.txt"` | 0 | (no output; exit 0 confirms existence) |
| E11 | `git -C "$L" cat-file -e "$B:.ufo/waves/round-72/controls/c1-tip.txt"` | 128 | `fatal: path '.ufo/waves/round-72/controls/c1-tip.txt' does not exist in 'c1f3d8d4ed9470ecbaaf3353952a374b079e68cc'` |
| E12 | `git -C "$L" cat-file -e "$B:.ufo/waves/round-72/controls/c2-tip.txt"` | 128 | `fatal: path '.ufo/waves/round-72/controls/c2-tip.txt' does not exist in 'c1f3d8d4ed9470ecbaaf3353952a374b079e68cc'` |
| E13 | `git -C "$L" cat-file -e "$B:.ufo/waves/round-72/controls/c1-tip-final.txt"` | 0 | (no output; exit 0 confirms existence) |
| E14 | `git -C "$L" cat-file -e "$B:.ufo/waves/round-72/controls/c2-tip-final.txt"` | 0 | (no output; exit 0 confirms existence) |
| E15 | `git -C "$L" show "$B:.ufo/waves/round-72/controls/c1-tip-final.txt" \| tail -n 2` | 0 | `C1 gate-status members=28 evaluated=28 mismatches=3 structural=0 agreement=25 scores_held=3/3 met=True` |
| E16 | `git -C "$L" show "$B:.ufo/waves/round-72/controls/c2-tip-final.txt" \| tail -n 2` | 0 | `C2v2 revision=5013c0ee87bda5fee03024488b4e293c4ca7ff16 brace_findings=0 command_findings=0 prose_findings=0 findings=[] removed=8 added=8 guard=ok met=True` |
| E17 | `python3 -B "$L/.ufo/waves/round-70/c70_pointer_audit.py" --root "$L" --revision "$B"` | 0 | `pointers=359 dangling=17 annotated=17 unannotated=0 met=true` |
