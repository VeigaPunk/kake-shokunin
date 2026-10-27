# SentinelResolver

Seat: SentinelResolver (security review of the symlink/path handling the C2 fix must add to `scripts/id_resolver.py`).
Scope: read-only. The lane tool was **copied out** of the lane into scratch and never executed in place; no lane file, lane
git index, jj state or sibling lane was touched. No build, no counter, no after-state scoring by this seat.
Tool snapshot: `fd6303ce…:scripts/id_resolver.py` = `HEAD:scripts/id_resolver.py` = blob
`c1c47a41573a271e9dd9fbafbc28a482d4979e4a`; worktree `sha256 = 2c1b4970a652023a883a414620c07cf393f7c4b28b87053564a45302428e663a`
= the copied tool, so "base" below = the round-59 base-revision tool.
Scratch (deleted before this report was written; drivers + receipts in `.ufo/waves/round-59/w1/SentinelResolver.files/`):
`/fast/scratch/hyaku/kake-r59/SentinelResolver/`. Fixture repos: `git -C "$D" init -q`; every
`git -C "$D" rev-parse --show-toplevel` asserted equal to the fixture dir before its first commit; commits used
`-c user.name=selftest -c user.email=selftest@local -c commit.gpgsign=false`. No pacman, no `uv tool install`, no PATH
change, no host service touched — **no tool was installed or upgraded by this seat**.
Rows below are the **current tool's** behaviour on gate-shaped fixtures; ids are my own labels (`S100` = registered,
`S2xx`/`S1x00` = deliberately unregistered), not counter-drawn ids.

---

## VECTORS:

### A. The three counter-pinned routes, and the base's failure on each

| # | Fixture | Base behaviour | Required behaviour |
|---|---|---|---|
| A1 | **K10** worktree: `corpus/knowledge/linked -> ../../notes_store` (in-lane dir), `notes_store/hidden.md` cites `S200` | **exit 0 green**, `ids_cited=1 ids_resolved=1 dangling=0` — the citation reachable only through the symlink is **dropped**, so a real dangling id is reported green | the in-lane symlinked knowledge dir **is** traversed; `S200` is counted (exit 1, `DANGLING S200`) |
| A2 | **K11** revision: `corpus/knowledge/linked.md -> ../notes.md` (cites `S300`), `corpus/knowledge/odd.md -> F400-target.md` (dangling) | **exit 0 green**, `ids_cited=1` — `git show <rev>:<path>` on a mode-120000 blob returns the **link target string**, so `../notes.md` is parsed as a body and `S300` is **missed** | the committed symlink resolves **inside the tree** and the target's real body is read; the target string is never a body; the dangling link contributes no body and no fabricated id |
| A3 | **K12** worktree: `corpus/SOURCES.md -> <outside>/SOURCES.md` holding the registry rows | **exit 0 green**, `ids_cited=2 ids_resolved=2 dangling=0` — `lane_registry()` has **no** containment check, so a foreign registry is read and its ids trusted as resolved | the registry that is not inside the lane is **refused**: exit **2** (unevaluable), never a green/1 summary |

### B. Path-escape and target-parsing vectors (same fix surface; the counter pins none of these)

| # | Fixture | Base behaviour | Required behaviour |
|---|---|---|---|
| B1 | revision: knowledge symlink whose **target string is itself an id** (`evil.md -> S999.md`, target absent) | **exit 1** `DANGLING S999 cited-by=corpus/knowledge/evil.md` — a **fabricated citation** for a file that does not exist | no body, no citation, no `DANGLING` line for a link target string |
| B2 | revision: knowledge symlink whose **target string is a sentence** (`note.md -> "Cites S100 and S1800."`) | **exit 1** `DANGLING S1800` — the *link target text* was parsed as Markdown | a link target string is never read as a body |
| B3 | revision: **registry** is a committed symlink whose target string is a **forged registry table** | **exit 0 green**, `ids_cited=2 ids_resolved=2 dangling=0` — the lane registry holds **no rows at all**; the forged table came from the link target string. A whole registry can be forged this way | the registry is read from the tree; a link target string is never parsed as a registry |
| B4 | revision: registry is a committed symlink resolving **in-tree** (`corpus/SOURCES.md -> knowledge/reg.md`) | **exit 1**, `ids_cited=1 ids_resolved=0 dangling=1` — the target string `knowledge/reg.md` was parsed as the registry, so *every* citation dangles (false red) | the in-tree target is resolved and read as the registry |
| B5/B6 | worktree: registry symlinked to a **sibling lane's** registry, or to an **absolute** path outside the lane | **exit 0 green** in both — ids resolved from **another lane's / a foreign** registry | exit 2: the lane registry must resolve inside the lane |
| B7/B8 | worktree: `corpus/knowledge` or `corpus/` **itself** is a symlink (out of lane) | **exit 2** `no knowledge file: corpus/knowledge absent` — refused, but the message says "absent" for a dir that exists, and the `corpus/` case never reaches a registry check | refuse consistently and accurately (the candidate artifact reports `registry outside the lane`, the better error) |
| B9/B10/B11 | worktree: knowledge symlink -> file outside the lane (absolute, `../../`), or -> **another lane's** knowledge dir | **exit 0** each; the outside ids are correctly **not** counted — `inside()` (realpath containment) holds today | unchanged: the containment check must keep holding **after** the fix starts following symlinked dirs |
| B12 | worktree: knowledge symlink -> the lane's **own registry** (`corpus/knowledge/reg.md -> ../SOURCES.md`) | **exit 1** `DANGLING S100 cited-by=corpus/knowledge/ok.md` — the registry's own row ids become "citations" of the registry file | the registry is not a knowledge file; it must not be read as one |
| B13 | revision: two-hop in-tree chain (`hop2.md -> hop1.md -> real.md`, `real.md` cites `S1700`) | **exit 0 green** at revision, `ids_cited=1` — the chain is unresolved, so `S1700` is missed (the same tree in worktree mode does give `DANGLING S1700`) | at a revision, chains resolve inside the tree (bounded); `S1700` is cited |
| B14 | revision: **committed cycle** `a.md -> b.md -> a.md` | no crash today (each blob is read as text) | the resolver detects the cycle (visited set / hop limit); it does not loop |

### C. Denial-of-service / hang vectors

| # | Fixture | Base behaviour | Required behaviour |
|---|---|---|---|
| C1 | worktree: symlink **cycle** in the tree (`corpus/knowledge/a -> ../dirB -> ../dirA`, plus `self -> ..`) | **exit 0** today, but only because `os.walk()` does **not** follow symlinked dirs. A naive `followlinks=True` fix loops: my probe visited **5001 dirs in 0.09 s without terminating** | the fix that follows in-lane symlinked dirs **must** carry a visited-realpath set / depth bound; a cycle terminates with a bounded file set |
| C2/C3 | worktree: **FIFO** named pipe inside `corpus/knowledge` (`pipe.md`), and a symlink to an in-lane FIFO (the realpath containment check **passes**, then the open blocks) | **TIMEOUT — the tool hangs forever**, in the base *and* in the current candidate artifact | only regular files are read (`S_ISREG` on the opened fd); a FIFO/device is skipped, never opened |
| C4 | worktree: symlink -> `/dev/zero` | **exit 0** — the containment check rejects it (realpath outside the lane); the check is the only thing between the tool and an unbounded device read | keep the containment check **and** require a regular file |
| C5 | worktree: symlinked knowledge dir holding **400 files** | not reached today (symlinked dirs are not followed) | bounded work: a symlinked dir must not multiply the corpus without bound |

### D. TOCTOU between the containment check and the open (check-then-use)

| # | Fixture | Base behaviour | Required behaviour |
|---|---|---|---|
| D1 | `corpus/knowledge/race.md` is a symlink a concurrent writer **swaps** between an in-lane and an out-of-lane target while the tool walks 200 knowledge files (the inverse swap — the check rejects the target the open then reads — admits an out-of-lane read the other way round) | the base's `inside(full)` → `open(full)` are two separate steps. Racing the **real base tool**: **26 of 120 runs** reported the out-of-lane id `S1400` as a citation of the lane (14 of 120 in an earlier identical run — the rate is timing-dependent, the leak is not). Isolated replica of the exact pattern: **550 of 4000 iterations** read out-of-lane content through the swap | the containment decision must be made on the **object actually opened**: open the fd first, then resolve `/proc/self/fd/<fd>` and test containment. Measured on the same race: **0 of 4000** out-of-lane reads with open-then-resolve vs 550 with check-then-open. The current candidate artifact still leaks: **18 of 60** runs |

### E. Trust-boundary vectors outside the lane's own tree (lower severity, same code path)

| # | Fixture | Base behaviour | Required behaviour |
|---|---|---|---|
| E1/E2 | a **sibling lane's** registry is a symlink out of the fleet (worktree), or its **HEAD** registry is a *committed* symlink to a forged table | **exit 1** `DANGLING S2000 owners=alpha-shokunin` in both — ownership is attributed from a link target string that is not a registry | a sibling's registry is trusted only when it is a real registry file |
| E3 | fleet entry `beta-shokunin` is a **symlink to the lane itself** | the lane is correctly excluded from siblings by the realpath compare, but the alias lane's registry is read as a sibling | unchanged; note the fleet can present aliases of one lane |
| E4 | `--root` is a **symlink** to a repository toplevel (`alias -> fleet/kake-shokunin`) | the tool measures the pointed-to lane; a K14-style check `realpath(root) == toplevel` **accepts** it (measured: `realpath(--root)` == `rev-parse --show-toplevel` → True) | the root check must compare the **realpath of the root the caller named** with the toplevel and refuse a root that is not literally that toplevel |
| E5 | worktree: knowledge file reached through two in-lane symlink hops (`hop2 -> hop1 -> ../../../outside/leak.md`) | **exit 0**, outside id not counted — correct today | unchanged; a hop chain must not defeat the containment check |

---

## MUST-HAVES FOR THE FIX:

Ordered by severity. **[M]** = must hold for the C2 claim to be honest; **[S]** = should hold (same code path, cheap).

1. **[M] The registry must resolve inside the lane, or the run is unevaluable (exit 2).** `lane_registry()` applies no
   containment check at all (B5/B6 give **exit 0 green** off a foreign registry). Apply the same realpath-containment
   rule as the knowledge walk and refuse with **status 2** — the counter's K12 expects exit 2, and exit 2 is the tool's
   reserved code for "the evidence needed to evaluate was not obtained". Do **not** over-refuse: an in-lane registry
   symlink (B4) must keep working, or the fix trades a false green for a false red.
2. **[M] A link target string is never content.** At a revision a mode-120000 blob is a *path*, not a body and not a
   registry. This closes the fabricated-citation class (B1, B2) **and** the forged-registry false green (B3) — one bug:
   `git show <rev>:<symlink>` yields the target string and the current code feeds it to the markdown and registry parsers.
   Resolve the target **inside the tree** (`git cat-file` the target's blob oid, or dispatch on the `ls-tree` mode) and
   read *that* oid.
3. **[M] Every resolved symlink target must be proven to stay inside the tree.** At a revision, reject a target that is
   absolute, normalizes above the tree root, is absent from the tree, or points at anything other than a regular file. At
   worktree time, keep the realpath containment check for **every** file and **every** traversed directory — including the
   newly-followed symlinked directories (B9/B10/B11/E5 must keep holding afterwards).
4. **[M] A committed symlink chain must resolve with a bound, and a cycle must terminate.** Depth limit or visited set on
   the resolution (B13, B14), searching the `ls-tree` entry map (mode + oid), never the working tree.
5. **[M] Following in-lane symlinked directories (K10) requires cycle protection.** A naive `os.walk(followlinks=True)`
   loops forever on a cycle (measured: 5001 dirs in 0.09 s, no termination). The fix must carry a visited-realpath set
   (my candidate traversal with that set terminates and yields a bounded file set) or an equivalent bound.
6. **[M] Only regular files are read.** `os.path.isfile()` follows symlinks and is true for a FIFO's *path*, and `open()`
   on a FIFO blocks forever: the base **hangs** (TIMEOUT) on a FIFO inside `corpus/knowledge`, and the current candidate
   artifact hangs too (C2/C3). Test `S_ISREG` on the opened fd (`os.fstat`) and skip anything else. A gate that hangs is a
   DoS on the round, not a measurement.
7. **[M] The containment decision must be taken on the object actually opened (TOCTOU).** `inside(path)` → `open(path)`
   is a check-then-use race; racing the real base tool leaked an out-of-lane id in **26 of 120 runs** (14 of 120 earlier).
   Open the fd first, then resolve `/proc/self/fd/<fd>` and test containment against the lane root: the same race then
   leaks **0 of 4000** (measured). The current candidate artifact still leaks (**18 of 60** runs). This is the one
   must-have that is a real exploitation path, not a robustness gap: whoever can write into the lane tree (or a sibling
   checked out into it) can choose which file's content is measured.
8. **[M] A dangling symlink must not destroy the run.** One broken link inside `corpus/knowledge` currently makes the whole
   measurement exit 2 (`cannot read corpus/knowledge/odd.md: No such file or directory`) — exactly the shape of K11's
   `odd.md -> F11-target.md`, whose required behaviour is "a dangling link contributes no body and no fabricated id",
   **not** "the run dies". Skip unresolvable links and keep measuring.
9. **[S] The registry is not a knowledge file.** A knowledge symlink pointing at `corpus/SOURCES.md` currently makes the
   registry's own row ids count as citations of the registry (B12). Exclude the registry from the knowledge set.
10. **[S] Sibling registries are trusted only as registries.** A sibling registry that is a symlink (worktree) or a
    committed symlink (HEAD) currently yields ownership from a link target string (E1/E2). Apply the same
    "target string is not content" rule there, or at minimum refuse a symlinked sibling registry.
11. **[S] Root and top-level paths.** The `--root` check must compare the realpath of the root the caller named with the
    repository toplevel, so a symlinked root pointing at another lane's toplevel is refused rather than silently measuring
    that lane (E4). The same treatment must cover `corpus/` and `corpus/knowledge` themselves (B7/B8): refused today, but
    with a misleading message and, for `corpus/`, no registry check at all.
12. **[S] Traversal must stay bounded.** A symlinked directory holding an arbitrary number of files, or a chain of
    symlinked directories, must not multiply the corpus without bound (C5). A file-count or depth cap is cheap.

### Explicitly NOT required (to keep the fix from over-reaching)

- **Refusing every symlinked registry.** An in-lane registry symlink (B4) must keep working; the counter pins only the
  out-of-lane case, and over-refusal turns a false green into a false red on a legitimate tree.
- **Following symlinked directories at a revision.** Git stores a symlinked directory as one mode-120000 blob; the files
  under its target are **not** in the tree (measured: `ids_cited=1`, the target's citation is invisible). Revision-mode
  directory-symlink parity is a *semantics* question for the wave, not a security one; out of this seat's scope.
- **Rejecting a knowledge symlink to another knowledge file in the same lane.** The base attributes the citation to **both**
  paths (`cited-by=…/alias.md,…/real.md`); duplicated citing paths are a presentation question (the id is counted once),
  not a trust-boundary break.

### Observations on the in-flight candidate artifact (not a verdict on the fix)

`.ufo/waves/round-59/w1/ExecResolverFix2.files/id_resolver.py` moved while this seat worked (mtimes 22:46, 22:54, 22:57,
23:00). Against the **23:00** snapshot (copied to scratch; the docstring was made raw in the scratch copy only):

- The docstring at line 2 contains `\xNN`, a **SyntaxError** in a non-raw docstring (`unicodeescape … truncated \xXX
  escape`): the artifact as committed **does not compile**. The 22:57 snapshot had the same defect and raised `NameError:
  name '_nul_paths' is not defined` on the revision path; the 23:00 snapshot raised `NameError: name 'ATX_HEADING_RE' is
  not defined` on every worktree run. In-flight breakage, not security findings — but the artifact is not executable.
- Where it did run, it already refuses an out-of-lane registry (`registry outside the lane: corpus/SOURCES.md` → exit 2 on
  B5/B6) and an out-of-lane `corpus/` (B8), satisfying must-have 1 for the worktree side.
- It **still hangs on a FIFO** (C2/C3: TIMEOUT) and **still leaks the out-of-lane id under the TOCTOU race** (18 of 60):
  must-haves 6 and 7 are not met by that snapshot.

---

## VERDICT:

The base tool has **four** false-green / false-red symlink paths and **two** denial-of-service paths, and the three
counter-pinned routes (K10/K11/K12) are only the visible part of it: an out-of-lane registry symlink yields a green
summary off another file's registry, a committed link target string is parsed as a *body* (fabricating a dangling id)
**and** as a *registry* (forging a whole green registry, B3), a committed symlink chain is never resolved so real
citations are missed, a single dangling link kills the whole measurement, a FIFO inside `corpus/knowledge` **hangs the tool
forever**, and a symlink swap between the containment check and the open leaks an out-of-lane file into the citation set
in **26 of 120 raced runs** of the real base tool. The fix must add, at minimum: registry containment with an exit-2
refusal (K12), mode-aware tree reads so a link target string is never content (K11), in-lane symlinked-directory traversal
with cycle protection (K10), a resolved-target containment proof for every link, a regular-file-only read rule, a bounded
link resolution, dangling links skipped rather than fatal, and a containment decision taken on the **opened fd** rather
than on a path resolved earlier — the last is the only measured exploitation path, and it goes from 550/4000 leaking reads
to 0/4000 with open-then-resolve.
VERDICT: the C2 fix needs seven symlink/path must-haves beyond the three counter-pinned routes — registry containment
(exit 2), link-target-string-is-never-content, resolved-target containment, bounded/cycle-safe link resolution,
cycle-safe directory following, regular-files-only reads, and fd-level containment (TOCTOU) — and the FIFO hang plus the
26/120 TOCTOU leak are the two highest-severity items, both still present in the in-flight candidate artifact.
