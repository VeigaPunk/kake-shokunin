# KakeR27.CliPaths — root-relative traversal, symlink and non-regular inputs (falsification)

Candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835`. Target under attack: the C2 gate CLI
`scripts/citing_set.py` (blob `3a361a002f66ce16b475e0e08eb2949db67f6651900d2c4b2699d5ef37ffc228`, read
from `git cat-file -p ac46a74…:scripts/citing_set.py`) and its runner `scripts/citing_set_selftest.py`
(`3c167895c7f3a4acf531886816bffcbf189d299d6137ca12096265855dd62a1c`). Working-tree hashes before and
after the run are byte-identical to the candidate blobs; tracked tree clean
(`git status --porcelain -uno` empty), HEAD still `ac46a74…`. No source/docs/registry edits, no
commits, no installs, no network. Read-only seat: only this report plus owned scratch under
`/fast/scratch/hyaku/kake-r27/CliPaths/` (TMPDIR set there; no /tmp, no /dev/shm). Every probe target is
my own harmless scratch file inside or outside the fixture root — no host or private-file target.
Axis judged: **operability** (does the CLI fail safely and consistently on hostile path shapes?).
Method: every expectation below was written into the harness (`build_probes*.py`, `evidence.py`) as a
`declared` block *before* the probe ran; the runner compares exit + verdict + finding-id multiset + reason
against it. Four probes matched my declaration for reasons that were **my** error, not the candidate's
(see Uncertainties). Command shape: `python3 -B scripts/citing_set.py --root <root> [--revision <rev>] --population <p> --ledger <l> --json`.

## Findings (author-side, severity ordered)

**F1 — HIGH (operability): a non-regular population/ledger document hangs the gate forever.**
Declared: exit 2, `input_invalid`, no hang. Observed: no exit at all. W15 `population.json` is a FIFO
and W17 `ledger.json` is a FIFO → no exit after 8 s (nor after 15 s in the first batch); the process
stays alive and blocked. `/proc` forensics: state `S (sleeping)`, `wchan=wait_for_partner`,
`syscall=257 0xffffffffffffff9c … 0x80000` → `openat(2)` with `O_CLOEXEC` and no `O_NONBLOCK`, i.e. a
blocking open on the FIFO. `WorkingTreeSource.read_document` (scripts/citing_set.py:207-219) opens the
document path blind; the corpus side *does* guard (`entry.is_file(follow_symlinks=False)` else
`not_a_regular_file`, scripts/citing_set.py:262-267), so the same class of input is refused in the
corpus and accepted-then-blocking in the documents. A CLI consumer pointing `--population`/`--ledger`
at a FIFO or other blocking special file therefore never terminates and emits no JSON. Not reachable
through the frozen C2 measurement (`.ufo/waves/round-27/c2_count.py:24-25` materialises regular files and
runs the gate in working-tree mode), so the frozen 16/16 number is unaffected; it is a live CLI defect
and an internal asymmetry with the corpus guard.

**F2 — MEDIUM: working-tree mode and Git mode disagree about a corpus path that is not a directory.**
Declared: the two modes must not disagree. Observed, same tree shape, two verdicts. W23 working tree,
`corpus/knowledge` is a regular file → exit 2, `could-not-evaluate`, `input_invalid/not_a_directory`
(stdout sha `fe9da122e7a2…`). G04 git mode, `corpus/knowledge` is a regular blob → exit 1, `failed`,
findings `ledger_pair_not_cited` + `unadjudicated_citing_pair`, `corpusFiles=1` (stdout sha
`8c86a79f62e1…`) — the blob is read *as a corpus document* although it is not under `corpus/knowledge/`.
`GitSource.corpus_files` (scripts/citing_set.py:290-315) has no counterpart to the working tree's
`not_a_directory` check (scripts/citing_set.py:238-241). The two documented input modes are meant to be two
views of one repository; here the same repository yields different verdicts, and one of them silently
evaluates an out-of-scope file.

**F3 — MEDIUM: a symlinked input document is readable in working-tree mode and unreadable in Git mode.**
W07/W33b working tree, `population.json` is a symlink to a file *inside* the root → exit 0, `clean`
(`is_inside` uses `realpath`, so an in-root link stays inside). G05 git mode, the same layout stored as a
symlink blob → exit 2, `input_invalid/document_not_json`: `git show rev:path` returns the *link target
text*, not the target's content, so the document can never be read in Git mode. The symlink policy is
asymmetric in itself: corpus symlinks are rejected in both modes (W08/W09/W29/W31 vs G02/G03, all
`symlink_rejected`), documents are followed in working mode and rejected in Git mode.

**F4 — LOW: symlinked parent of the corpus — safe in working mode, differently classed in Git mode.**
W32b working tree, `corpus` → symlink to an outside tree → exit 2, `input_invalid/path_escapes_root`
(scope document): the out-of-root file's content is **not** read; the gate refuses before opening. G13 the
analogous tree (`corpus` is a symlink blob) → exit 1, `failed`, `corpusFiles=0`. Different verdict class
for the same logical layout; the working-mode answer is the safe one.

**F5 — LOW: an empty or missing corpus scope is green.** W22 (root with no `corpus/knowledge` and an
empty ledger) → exit 0, `clean`, `corpusFiles=0`, `citingPairs=0` — by exit code indistinguishable from
a fully adjudicated corpus. W21 (corpus missing, non-empty ledger) → exit 1, `failed`,
`ledger_pair_not_cited`. No out-of-root file is read, so this is not a path escape; it is a scope-shape
fail-open of the family the r26→r27 correction set out to close, and the shape a mistyped `--root` gives.

## Confinement that held (author-side; each met its declared expectation)
Traversal refused before any filesystem access: W02/W03/W05 `..` → `path_escapes_root`; W04 absolute →
`absolute_path_not_allowed`; W24 traversal *through* an in-root symlinked directory pointing outside →
`path_escapes_root`; W28 symlink chain ending outside → `path_escapes_root`. W25 proves the refusal
precedes the open: the traversal target was an out-of-root FIFO and the run returned in 0.027 s (no
block). Corpus symlinks refused regardless of target: W08/W29 (directory, in- or out-of-root),
W09/W10/W11/W31 (file: in-root, broken, out-of-root, inside a subdirectory) → `symlink_rejected`. Corpus
non-regular refused: W12 FIFO, W13 socket → `not_a_regular_file`. Ledger `file` fields are never resolved
on the filesystem: W27 names an out-of-root FIFO in the ledger → exit 1 in 0.026 s, no open, no hang.
Git pathspec is not over-broad: G07, with `corpus/knowledge-extra.md` in the revision → `corpusFiles=1`,
the sibling file is not enumerated. Git mode never consults the working tree: G12, working tree holding
a FIFO and a dangling `population.json` symlink → git-mode run `clean`, `corpusFiles=1`.

## Coverage gap in the frozen suite (author-side)
The 29 frozen fixtures are 118 files, all mode `100644` — no symlink and no special file can be
represented — and `citing_set_selftest.py` never passes `--revision` (the word appears only in a
docstring). F1-F4 are therefore unreachable by the frozen fixture suite, and the documented Git mode has
zero fixture coverage: the frozen C2 measurement exercises only working-tree mode over regular files.

## Uncertainties / my own errors (not candidate defects)
W14 and W27 mismatches were mis-declared expectations of mine (I omitted the
`S002 → corpus/knowledge/sub/doc2.md` adjudication, and mis-modelled the ledger case); re-declared
correctly in W30 → exit 0, `clean`, `corpusFiles=2`. W32 (first attempt) was a badly built fixture: the
symlink target had no `knowledge/` subdir, so it measured only the missing-corpus path (that observation
is F5's evidence, not an escape); corrected in W32b. Git-mode probes used scratch repositories of my own
construction; the candidate's own repository is never run in `--revision` mode by any frozen artifact.
I could not create a character device unprivileged, so a device node as a document is untested (the FIFO
covers the same blocking-open class). No install was needed; no tool version changed.

## Verdict (falsification only)
Root-relative confinement is sound: every out-of-root target I could construct was refused with
`input_invalid` *before* any open, and no host or private file was read or printed. Against that,
three live operability defects stand — the non-regular-document hang (F1), the working-tree/Git mode
disagreement on corpus shape (F2) and on symlinked documents (F3) — plus an empty-scope green (F5).
None changes the frozen C2 number (working-tree mode over regular files), but the gate cannot be claimed
to "fail safely and consistently" on hostile path shapes, and the frozen suite cannot detect any of these.
