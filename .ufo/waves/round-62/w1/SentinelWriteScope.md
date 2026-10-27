# SentinelWriteScope — round-62 counter/plan write-scope review

Item: ensure the frozen C1 counter reads only committed Git blobs and that neither the counter
nor the round plan writes upstream, external or unintended lane paths.

Binding: advisory only. Frozen claim, `c62_calibration.py`, criteria and score untouched; no lane
file was written by this seat except this report. All probes ran in
`/fast/scratch/hyaku/kake-r62/SentinelWriteScope/` (fixtures `fx`, `fx2`, created from committed
lane blobs, deleted before yield). Lane untouched: `git -C <lane> status --porcelain` stayed at the
single `?? .ufo/waves/round-62/` entry before and after every probe, and `HEAD` stayed `c341a7a4`.

Counter under review: `.ufo/waves/round-62/contract.md` + `.ufo/waves/round-62/w1-spec.json` +
`c62_calibration.py`. Frozen hash verified:

```
$ sha256sum .ufo/waves/round-62/c62_calibration.py
ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d
```
(matches the pinned hash in the contract)

## Verdict

| # | Severity | Finding | Write or read? |
|---|---|---|---|
| W1 | **HIGH (evidence integrity)** | Empty `--revision` makes `git show :<path>` read the **index**, not a commit → `met=true` exit 0 with **zero commits** | read (unintended source of truth) |
| W2 | MEDIUM | No repo-identity assertion: `GIT_DIR` (or a foreign `--root`) silently redirects all five blob reads to another repository | read |
| W3 | LOW | `--revision=<value beginning with `--output=`>` is passed through as a git option and makes `git show` write files | **write** |
| W4 | INFO | Mutable revisions (`HEAD`, branch names) accepted; "measured committed revision" is not enforced | read |
| W5 | INFO | Counter never reads the retained `S432.html`: quote provenance is marker-presence only | read (missing) |
| W6 | INFO | Round-62 base-control output is prose-only; no stored control artifact (round-61 has `controls/c1-c58-base-control.txt`) | evidence |

Verified-clean results are in the last section; W1 is the one that matters for scoring integrity.

---

## W1 — HIGH: `--revision=` (or `--revision ""`) reads the index and false-greens the claim

Exploit path (no commit required, no lane mutation):

1. Stage lane content that satisfies the predicate (i.e. the planned after-state) — this is the
   normal pre-commit state of the integrator's working tree.
2. Run the frozen counter with an empty revision:
   `python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision=`
3. Because `blob()` builds `f"{rev}:{path}"`, an empty `rev` yields `":<path>"`, which git resolves
   as the **index** blob (stage 0), not a commit.

Evidence (fixture `fx`: `HEAD` = committed base copy, green content staged only):

```
$ git -C fx log --oneline -1
37b5744 base copy without round-62 lesson
$ git -C fx status --porcelain=v1
M  corpus/QUALITY.md
M  corpus/knowledge/response-header-expectations.md
M  corpus/lessons/round-61-verifier-spotcheck.md
A  corpus/lessons/round-62.md

$ python3 -B fx/c62.py --root fx --revision=
revision= disagreements=0 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
EXIT=0

$ python3 -B fx/c62.py --root fx --revision=HEAD
revision=HEAD disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
EXIT=1
```

The accidental form is equally reachable, and is the realistic trigger (unset shell variable):

```
$ python3 -B fx/c62.py --root fx --revision ""
revision= disagreements=0 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
EXIT=0
```

Impact: the contract's central invariant — "the counter re-derives all states from committed blobs"
(contract C1) — does not hold for a caller-controlled revision. A wave can be scored `met=true,
exit 0` while nothing is committed, so the after-state can be reported from uncommitted bytes that
later change. The only tell is the empty `revision=` field, which nothing rejects.

Smallest remediation (both lines verified to reject the bad inputs, one-line cost):

```python
RE_SHA = re.compile(r"[0-9a-f]{40}")
def resolve(root: str, rev: str) -> str | None:           # reject "", refs, options, index revs
    if not RE_SHA.fullmatch(rev):
        return None
    p = subprocess.run(["git", "-C", root, "rev-parse", "--verify", "--quiet",
                        "--end-of-options", f"{rev}^{{commit}}"], stdout=subprocess.PIPE)
    return p.stdout.decode().strip() or None
```
then build the object argument from the returned 40-hex sha (and return 2 when `None`).

Verification of the guard itself:

```
chk(:corpus/QUALITY.md^{commit})=1     # index rev rejected
chk(--output=/x^{commit})=1            # option-shaped rev rejected
chk(HEAD^{commit})=0                   # real rev accepted
```

## W2 — MEDIUM: reads are not bound to the lane repository

`blob()` runs `git -C root show ...` with the inherited environment and never asserts the
repository. `GIT_DIR` overrides `-C` discovery, so the five "committed blob" reads can come from
any repository on the host while the command line still says `--root <lane>`:

```
$ GIT_DIR=/fast/scratch/hyaku/kake-r62/SentinelWriteScope/fx2/.git \
    python3 -B fx/c62.py --root /fast/scratch/hyaku/kake-r62/SentinelWriteScope/fx --revision HEAD
revision=HEAD disagreements=0 unresolved=0 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 met=true
EXIT=0
$ env -u GIT_DIR python3 -B fx/c62.py --root .../fx --revision HEAD
revision=HEAD disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
EXIT=1
```

Related, weaker: `--root` is unvalidated, so a seat can measure a sibling checkout of the lane.
Currently benign — the fleet root `/home/vgpnk/Projects/shokunin` is a git repo but does not track
`kake-shokunin` (`git ls-tree HEAD kake-shokunin` → empty), so the accidental invocation from the
fleet root fails closed:

```
$ python3 -B kake-shokunin/.ufo/waves/round-62/c62_calibration.py --root . --revision c341a7a4...
could-not-evaluate: missing verifier spot-check
EXIT=2
```

Impact: after-state evidence can be taken from a different repo with no detection; exit 2 vs exit 1
does distinguish the fleet-root mistake, so this is integrity, not a false green on its own.

Smallest remediation: assert identity before measuring —
`git -C root rev-parse --show-toplevel` must equal the expected lane root (verified:
`git -C fx rev-parse --show-toplevel` → `/fast/scratch/hyaku/kake-r62/SentinelWriteScope/fx`), and
run the measurement with `env` scrubbed of `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`,
`GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES` (or reject when they are set).

## W3 — LOW: option-shaped `--revision` turns a read into a write

`argparse` rejects the space form (`--revision --output=/x` → "expected one argument"), but the
`=` form is accepted verbatim and the resulting argv element starts with `--`, so `git show` parses
it as the `--output=<file>` option. The appended `:corpus/...` suffix means the written path is
`<value> + ":corpus/lessons/<name>"`:

```
$ mkdir -p "$S/leak:corpus/lessons"
$ python3 -B fx/c62.py --root fx --revision=--output=$S/leak
could-not-evaluate: missing verifier spot-check
EXIT=2
$ ls -la "$S/leak:corpus/lessons/"
-rw-r--r-- 1 vgpnk vgpnk 2953 round-61-verifier-spotcheck.md
-rw-r--r-- 1 vgpnk vgpnk 2953 round-62.md
```

Impact: a caller-supplied revision can create files whose name is `<chosen-prefix>:corpus/...`
(only in a parent directory the caller already created; other paths fail with git exit 128 and are
silently converted to `could-not-evaluate`). No existing normal-named file can be clobbered, and
git rejects main-level options after the subcommand, which bounds the escalation:

```
$ git -C fx show --git-dir=<other>/.git
fatal: unrecognized argument: --git-dir=<other>/.git
$ git -C fx show --work-tree=/home/vgpnk/Projects/shokunin
fatal: unrecognized argument: --work-tree=/home/vgpnk/Projects/shokunin
```

Smallest remediation: the W1 `rev-parse --verify --end-of-options` gate rejects this input before
git runs (verified above). Note `git show` itself does not accept `--end-of-options`
(`fatal: option '--output=...' must come before non-option arguments`), so the gate must be a
pre-invocation validation, not an extra argv element.

## W4 — INFO: revision is not pinned to a commit id

`--revision HEAD` / a branch name is accepted, so a floating ref can be measured. W1's 40-hex gate
also closes this. The recorded base-control uses the full sha `c341a7a4…`, so the intent is already
40-hex; only enforcement is missing.

## W5 — INFO: the correction's provenance is never checked against the source

`PATHS` has five entries (`spot`, `knowledge`, `quality`, `lesson`, `sources`); the retained source
`.ufo/waves/round-61/sources/S432.html` is not among them, and `git show` for each of the five paths
is the counter's entire read set. So `substantive_quote_correction` asserts that the exact `QUOTE`
string plus the literals `S432 §3.6` and `Round-62 correction` appear in the knowledge blob — not
that the sentence exists in the source. A fabricated-but-matching quote string would pass. This is
a predicate-strength gap (other seats own it); it is reported here because it is also a read-scope
gap: the one committed blob that could ground the quote is never opened.

## W6 — INFO: no stored base-control artifact for round 62

`.ufo/waves/round-62/` contains only `c62_calibration.py`, `contract.md`, `w1*`; there is no
`controls/` output comparable to round-61's `controls/c1-c58-base-control.txt`. The base-control
values live only in contract prose. I reproduced them independently (below), but a committed
control file would make the "before" unreconstructable-by-accident.

---

## Verified clean (what the review did confirm)

1. **Counter writes nothing.** Full syscall trace of the real base run in the lane:

```
$ strace -f -qq -e trace=openat,open,creat,unlink,unlinkat,rename,renameat,renameat2,mkdir,mkdirat,truncate,ftruncate \
    -o trace-base.log python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision c341a7a4...
revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false
EXIT=1
```
   Write-mode opens in the trace: only `openat(AT_FDCWD, "/dev/null", O_RDWR)` ×5 (git's stderr
   suppression). Zero write/create/unlink/rename/mkdir on any lane path (`grep -c 'kake-shokunin'`
   over those lines → `0`), zero `.git/*.lock`, zero `/tmp` opens (`grep -c '/tmp/' → 0`).
   Wave-dir inventory (`find … -printf '%p\t%s\t%T@'`, sorted) and `git status --porcelain` were
   byte- and mtime-identical before/after (the only diff rows were two sibling seat reports that
   appeared in `w1/` during the run, which is expected and not attributable to the counter).

2. **Reads are committed blobs, default environment.** Reads under the lane are
   `.git/HEAD`, `.git/packed-refs`, `.git/objects/info/alternates` (ENOENT), and the pack
   index/`.pack` — i.e. git's object store; no worktree `corpus/...` file is opened. No
   `objects/info/alternates` file exists (`cat .git/objects/info/alternates` → absent) and the lane
   worktree equals base for the whole read set:

```
$ git -C <lane> diff --stat c341a7a4... -- corpus/lessons/round-61-verifier-spotcheck.md \
    corpus/knowledge/response-header-expectations.md corpus/QUALITY.md corpus/SOURCES.md
(no output)
```

3. **Base control reproduced from committed bytes** (independent of the counter):
   `git show c341a7a4…:corpus/lessons/round-61-verifier-spotcheck.md | grep S432 | grep -c Disagree`
   → `1`; `Round-62 correction` → `0`; `substantive located quote` → `0`; `| S432 |` → `1`. Matches
   the contract's recorded `unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1
   met=false exit 1`.

4. **Plan write grants are inside lane/scratch.** All 64 `w1-spec.json` items confine output to the
   seat's own `w1/<Name>.md` (`reportDir: .ufo/waves/round-62/w1`), and every item whose wording
   touches corpus files says "Do not edit files" / "no lane changes" / "report only" (checked the
   11 items containing edit/append/write verbs, e.g. `ScribeS432QuoteFix`, `ScribeLOG`,
   `ExecutorNoHarmSnapshot`). Scratch is `/fast/scratch/hyaku/kake-r62/<seat>/`; no `..`, absolute
   escape or `/tmp` grant appears in the plan (`grep -RnoE
   '(/home/[A-Za-z0-9._/-]+|/tmp/[A-Za-z0-9._/-]+|/fast/[A-Za-z0-9._/-]+|~/[A-Za-z0-9._/-]+|\.\./)'
   contract.md w1-spec.json` → only the lane/contract, census and scratch paths), and no `w1/*.md`
   report shows a lane git mutation
   (`grep -rlnE 'git -C … (commit|add|checkout|reset|rm|stash)'` → no hits).

5. **No symlink/path-escape in the write surface.** `.ufo/waves/round-62` and `w1/` are real
   directories (`find .ufo/waves/round-62 -type l` → empty), registry names are 64 unique, and
   this report's path was absent before writing (no seat-report collision).

6. **Host bounds held.** No writes to `/home/vgpnk/.local/bin` or `/home/vgpnk/.config/git`
   (`find … -mmin -120` → empty), no tracked lane file modified (`git status` = only
   `?? .ufo/waves/round-62/`, `HEAD` = `c341a7a4`), no pacman invocation, no installs. The required
   guard text is present in the dispatched wave context (`grep -c 'Never use pacman'
   w1-dispatch.json` → `1`, shared by all 64 tasks). No stray counter processes remained
   (`pgrep -af c62_calibration` → empty).

## Residual risk after the proposed W1/W2 fixes

Low. Remaining exposure is (a) a compromised lane `.git/config`/global `~/.config/git/config`
(`core.fsmonitor`, `core.pager`) influencing git, and (b) W5: provenance of the quote is still not
verified against the retained source blob. Neither is a write-scope hole.
