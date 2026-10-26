# ReviewerResolverCode

Code review of `scripts/id_resolver.py` as frozen at `4b8c73050470ada9e6583f3b12d659d1bed6a17f`
(read with `git show 4b8c730…:scripts/id_resolver.py`; byte-identical to the current worktree copy,
`diff -q` clean) against the contract docstring of `.ufo/waves/round-57/c57_idresolver_gate.py`
(lines 14–40, "CLI contract the gate exercises") and the gate's own reference implementation
(`registry_rows`/`read_lane`/`read_siblings`/`compare`, gate lines 128–200, used as arbiter for G3–G5).
Line numbers below are the tool's. Probes ran on a copy of the pinned blob, fixtures under `mktemp -d`.

FINDINGS:

F1 — MEDIUM — `knowledge_bodies` revision mode drops every non-ASCII / git-quoted knowledge path,
silently, and reports green. Lines 141–145: `git ls-tree -r --name-only` (no `-z`,
`core.quotePath` defaults true) returns `"corpus/knowledge/\344\270\255\346\226\207.md"`; the trailing
`"` fails `rel.endswith(".md")`, the file is never read, its ids never counted. The gate's reference
shares the bug, so G3/G5 cannot catch it.
Input (ran): lane at a revision with `corpus/knowledge/ok.md` = `Cites S001.` and
`corpus/knowledge/中文.md` = `Cites S900.` →
`--revision <rev>`: `ids_cited=1 ids_resolved=1 dangling=0`, exit 0 (dangling S900 hidden);
same tree without `--revision`: `DANGLING S900 cited-by=corpus/knowledge/中文.md`, exit 1.
`git ls-tree` output confirmed quoted. Fix: `git ls-tree -r -z --name-only` and split on NUL
(or `-c core.quotePath=false`), keeping the same prefix/`.md` filter.

F2 — MEDIUM — an unreadable `--fleet` directory raises and exits 1, which means "dangling > 0".
Lines 176–181 (`os.listdir(fleet)` unguarded; `evaluate` has no try, `main` at 712 only guards
`status == 2`).
Input (ran, uid 1000): `--fleet <dir mode 000>` → stderr `PermissionError: [Errno 13] …
'…/fleet'`, empty stdout, **exit 1**. Contract: "exit … 2 unevaluable"; a wrapper reads the 1 as
dangling. Fix: wrap the listing (and the per-sibling calls) and return `_err(f"fleet unreadable: {…}")`.

F3 — MEDIUM — an unreadable knowledge subdirectory is skipped silently and the run stays green.
Line 159: `os.walk(base)` without `onerror`; `open()` errors are caught per file (166–170) but a
directory that cannot be listed is not reported at all, contradicting "every
`corpus/knowledge/**/*.md` file".
Input (ran): `corpus/knowledge/sub` mode 000 containing `b.md` = `S777`, `a.md` = `S001`, registry
holds only S001 → `ids_cited=1 ids_resolved=1 dangling=0`, exit 0. Fix: pass `onerror` that
collects/raises, surfaced as status 2 ("cannot read corpus/knowledge/sub").

F4 — MEDIUM — the rendered `DANGLING` line is unparseable by the frozen counter when a citing path
contains a space, and silently wrong when it contains a comma. Lines 248–249 join raw
repo-relative paths with `,`; the gate's `DANGLE = r"^DANGLING (S\d{3,}) cited-by=(\S+) …$"` is a
single non-space token split on `,` (gate lines 67, 100–104).
Input (ran): knowledge file `corpus/knowledge/a b,c.md` → stdout
`DANGLING S777 cited-by=corpus/knowledge/a b,c.md owners=- url-match=-`; `gate.parse` returns
`unexpected line before the summary: …`. With only a comma (`a,b.md`) `gate.parse` accepts but
yields the two phantom paths `corpus/knowledge/a` and `b.md`. Same failure in `--revision` mode
(`corpus/knowledge/my note.md`). No such path exists in the lane today (54 knowledge blobs, zero
with space or non-ASCII name), so this is latent. Fix: treat a path containing `,` or whitespace as
unevaluable (exit 2 with a message) rather than emit a line the counter must reject; the line
format itself is frozen on the gate side.

F5 — MEDIUM (latent; no live divergence today) — sibling repo detection uses
`git rev-parse --show-toplevel` (line 194) instead of the contract's "when the directory has a
`.git`", so a `.git`-less sibling that sits inside *any* enclosing repo is read through that
enclosing repo's `HEAD:corpus/SOURCES.md`. The real fleet root `/home/vgpnk/Projects/shokunin` is
itself a git repo (`rev-parse --show-toplevel` → itself).
Input (ran): fleet dir `git init`-ed with a committed `corpus/SOURCES.md` holding S777; sibling
`gamma-shokunin` a plain dir with its own registry holding only S002; lane cites S777 → tool:
`owners=gamma-shokunin`; gate reference: `owners=[]` (unowned). Live today: all 21 siblings have
`.git` and `git cat-file -e HEAD:corpus/SOURCES.md` succeeds for each (checked), and the fleet root
has no `corpus/SOURCES.md` at HEAD (`cat-file -e` → 128), so no current mismatch. Fix: guard on
`os.path.exists(os.path.join(path, ".git"))` as the gate does, or on
`realpath(show-toplevel) == realpath(path)`.

F6 — LOW — a sibling that *is* a repo but whose `HEAD:corpus/SOURCES.md` is unavailable falls back
to the working-tree file (lines 196–202), contrary to "a sibling's registry is
`git show HEAD:corpus/SOURCES.md` when it is a git repo, else the file".
Input (ran): sibling `git init`-ed with no commits and an uncommitted `corpus/SOURCES.md` holding
S777 → tool `owners=gamma-shokunin`; gate reference `owners=[]`. Fix: in the repo branch, a failed
`git show` means "owns nothing" (return `{}`), never the worktree file.

F7 — LOW — url-match deviates from "occurs verbatim": line 98 takes URLs only from the second cell
and strips `.,;:` from each. The contract says the *row* carries an http(s) URL occurring verbatim
in a citing file; the gate reference scans the whole row line with no stripping.
Inputs (ran): (a) row `| S101 | see https://a.example/101, and more |` + body quoting
`https://a.example/101` → tool `url-match=alpha-shokunin`, reference `url-match=-` (strip makes a
non-verbatim prefix match); (b) row `| S101 | text | docs | A | s | https://a.example/101 |` (URL in
the anchor cell) + same body → tool `url-match=-`, reference `url-match=alpha-shokunin`.
Live consequence: URL sets differ from the reference on 13 of 21 sibling registries (trailing `;`
after URLs in kake S001/S002 and others). Not gate-visible: G4/G5 compare with `with_urls=False`
and G3 fixtures place short unpunctuated URLs in the source cell. Fix: `URL_RE.findall("".join(row
cells))` with no `rstrip`.

F8 — LOW — registry heading recognition is stricter than the reference: line 42
`REGISTRY_HEADING_RE = r"^##\s+Registry\s*$"` (case-sensitive, exact). The reference opens on any
`## ` heading whose lowercased text starts with `## registry`.
Input (ran): registry with `## registry` (lowercase) holding S001, knowledge citing S001 → tool
`DANGLING S001 … unowned=1`, exit 1; reference `summary=(1,1,0,0,0)`. Also `## Registry notes`
re-opens the section for the reference only. Fix: `re.match(r"^##\s+registry\b", line, re.I)`.

F9 — LOW — `parse_registry` requires a closing pipe in the first cell (line 39, `ROW_RE`), the
reference does not.
Input (ran): registry body `## Registry` / `| S001` (no second pipe), knowledge cites S001 → tool
`DANGLING S001 …`, exit 1; reference resolves it. Fix: detect rows with `^ {0,3}\|` and take the
first `|`-separated cell, as the reference does.

F10 — LOW — a mistyped `--fleet` (absent path, or a regular file) yields `owners=-` for every id
and exit 1 instead of a diagnostic (lines 177–179 return `[]`).
Input (ran): `--fleet /nonexistent` and `--fleet <regular file>` → `DANGLING S777 … owners=-`,
exit 1, empty stderr. The contract does not demand 2 here, but "unowned" is then asserted on
missing evidence. Fix: when `--fleet` was given explicitly and is not a readable directory,
return `_err`.

TIMING (host load avg 14.9/28.0/33.2, 32 cores; 3 runs, min):

- `python3 -B scripts/id_resolver.py --root <lane> --fleet /home/vgpnk/Projects/shokunin`:
  35 / 36 / 38 ms, exit 0, `ids_cited=106 ids_resolved=106 dangling=0` (0 dangling ⇒ no sibling
  git calls; the 21 registries incl. kotodama's 804 rows are not opened on a green run).
- same with `--revision 3994101…` (5 dangling, 21 sibling registries parsed, 21 `git show` calls):
  112 / 116 / 124 ms, exit 1, RED_IDS S367 S372 S373 S390 S409 → `owners=kotodama-shokunin`;
  with `--revision 4b8c730…`: 129 ms, exit 0.
- `--selftest`: 114 ms, `selftest: 33/33`, exit 0.
- synthetic scaling (400 dangling ids, 1 sibling with 800 rows, ~13 MB across 40 knowledge files,
  url-match substring scan at line 235): 163 ms — linear in dangling × citing-paths, no blow-up.
- peak child RSS ≈ 29.9 MB (interpreter baseline 29.4 MB).
No timeout risk against the gate's 300 s per-call limit; `_spawn` (line 62) itself has no timeout,
so a stalled filesystem would burn the gate's limit and surface as `Unevaluable` (timeout) instead.

NO-DEFECT CHECKS (all confirmed by running unless noted):

- Differential parse over the real fleet: `parse_registry` returns exactly the reference's id set
  for all 21 sibling registries at HEAD (804-row kotodama included; zero tool-only, zero
  ref-only ids).
- End-to-end parity with the gate reference on real revisions: at `3994101…`
  (exit 1, 99 cited / 5 dangling / 5 owned) and at `4b8c730…` (exit 0, 106/106),
  `gate.parse` accepted every line and `gate.compare(dang, summ, ref, False) == ""`.
- Determinism: byte-identical output at the red revision under `PYTHONHASHSEED=0`, `=12345`,
  `LC_ALL=C`, `LC_ALL=C.UTF-8`; ids, citing paths, owners and url-match all sorted (lines 112, 223,
  231–236); summary identity `cited = resolved + dangling`, `owned + unowned = dangling` holds.
- Output shape: `DANGLE`/`SUMMARY` regexes match for ASCII space-free paths; `-` used for empty
  sets; DANGLING lines precede the single summary line.
- Exit codes: 0 clean, 1 dangling, 2 for unresolved revision, registry absent at the revision,
  registry file unreadable (mode 000, ran), empty knowledge tree, non-directory `--root`;
  64 for no `--root`, missing option value, unknown option; `--help` → 0.
- `git show` robustness: `_text` decodes with `errors="replace"` (binaries and non-UTF-8 blobs do
  not raise); a NUL-filled `blob.md` at a revision was read and its `S777` reported (exit 1).
- `--revision` accepts a branch name (`master`), `HEAD`, a full sha and a 7-char short sha; a
  nonexistent branch exits 2 with a diagnostic on stderr and empty stdout.
- Sibling reading: a symlinked sibling pointing at an external repo is followed and named
  (`owners=linked-shokunin`), a symlink to the lane itself is excluded by realpath (selftest case
  "lane excluded from owners by realpath"), and a `git clone` of the lane in the fleet counts as an
  owner (`owners=clone-shokunin`) — same as the reference, consistent with "realpath differs".
- Selftest hermeticity (strace `-f -e trace=openat,connect`): 0 `connect()` calls (no network);
  every write-mode open resolves under `$TMPDIR` (the relative `.git/...` opens are inside the
  `mkdtemp` fixture repos); with `PATH=/nonexistent` (git absent) it reports 22/33, exit 1, and
  leaves **zero** directories — `_tmpdir`'s `finally` runs on failure; no `~/.gitconfig` writes
  (identity inline via `-c`, lines 311–312); fixtures use absolute paths, no `chdir`.
- `--selftest` ignores a stray `--root` and still prints exactly one `selftest: 33/33` line
  (G2's shape).

VERDICT: C2 resolver is deterministic, fast and gate-equal on today's lane and fleet (0 defects in
the measured path), but F1 (non-ASCII knowledge paths silently dropped in `--revision` mode ⇒ false
green), F2/F3 (permission errors exit 1 or pass silently instead of 2) and F4 (unparseable DANGLING
line for spaced paths) are real contract deviations a hostile replay can construct; F5–F10 are
latent divergences from the gate's reference on inputs the lane does not have.
