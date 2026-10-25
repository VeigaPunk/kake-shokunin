# ReviewWorktreeRead — C2 R4 worktree-read attack

Axes: operability, freshness. Seat writes only this file. Lane HEAD at write time: `1c846ed2d67b1692ea966be064f0fc04542763c6`.

## Verdict

A dirty worktree cannot move the C2 score through R4. Editing the retained text, the receipt, `corpus/SOURCES.md`, the lesson, or the knowledge entry — staged or unstaged — does not enter the score. The round-48 defect (open the worktree path, ignore the named revision) is not in this counter.

A dirty worktree can still move the *invoked* score by editing `c49_quote_truth.py` itself. The frozen command runs that worktree path. That residual is not live at this revision: the worktree script blob equals the pinned blob. It is not an R4 read.

## Grep

`rg -n -e 'open\(' -e 'os\.path\.join\(root'` on `.ufo/waves/round-49/c49_quote_truth.py` printed one line:

```
212:        with open(args["json"], "w", encoding="utf-8") as handle:
```

`os.path.join(root` : no hits. `import os` / `os.path` : no hits. An AST walk of that file found one `open` call, same line, mode `"w"`.

Same grep on `.ufo/waves/round-48/c48_quote_truth.py`:

```
205:                path = os.path.join(root, os.path.dirname(RECEIPTS), receipt["textPath"])
207:                    with open(path, "rb") as fh:
248:            with open(args.json, "w", encoding="utf-8") as fh:
```

The path open is line 207, built on line 205. That is the round-48 R4 read named in `corpus/lessons/round-48-verifier-spotcheck.md` routed defect 2.

## What C2 R4 reads

`c49_quote_truth.py:76-83` `git_show` runs `git -C <root> show <revision>:<rel>` and returns stdout bytes. R4 (`c49_quote_truth.py:172-182`) sets `rel` to `.ufo/waves/round-49/sources/<textPath>` from the receipt blob, then hashes and substring-checks that blob. `textPath` is not joined to `root` and is not passed to `open`.

At `1c846ed2d67b1692ea966be064f0fc04542763c6:.ufo/waves/round-49/sources/receipts.json` the pins are `S273.txt` / `ab4a685d7432b69e659f6d3717aeeffc66b9277e69ad54de601f72cc30d4347b` and `S274.txt` / `e3be028952b74702f7f06fb540e91b481ac1a026bdbe87ff035a3b566b0fcda4`. `git show` of those two paths piped to `sha256sum` matched both pins, so the show output is the raw blob.

R1–R3 inputs (`corpus/SOURCES.md`, `corpus/lessons/round-49.md`, `corpus/knowledge/crawl-budget-consequences.md`, the receipt file) use the same `git_show`. None of them is opened from the worktree.

The line-212 `open` runs only when `--json` is set, and only after `run()` has already built the score (`c49_quote_truth.py:205-213`). The frozen counting command does not pass `--json`, so that call does not run. It writes a sidecar. It does not read retained text. A bad `--json` path can still change the process exit to 2 via the broad `except Exception` — a caller footgun, not an R4 worktree read.

## c48 comparison

`c48_quote_truth.py:205-208` opens `<root>/.ufo/waves/round-48/sources/<textPath>` and hashes those bytes. `--revision` is not used for that read. A dirty or staged retained file changes the sha256 and the substring check. That is the defect this round's lesson claims to close (`corpus/lessons/round-49.md` Mistakes, class "quote counter reads worktree bytes").

## Probe (not the lane)

Throwaway repo under `/tmp`, then deleted. Committed `retained.txt` as `committed-bytes`, then overwrote and staged `dirty-worktree-bytes`.

- `git show <rev>:retained.txt` sha256 `20682c5f1e9ae3779884f0e82a1af21818a94346c866b3868757f4cf70c4549e` — dirty bytes absent. Same result from the c49 `subprocess` pattern.
- `open(path, "rb")` on the worktree file sha256 `5ebf27f0a3686357f1891dc233141f1a8acf118a83be3a62322c1b39e4840240` — dirty bytes present. The index (`git show :retained.txt`) matched the dirty hash, not the commit.

So a staged dirty file moves a c48-style score and does not move a c49-style `git show <rev>:` score. `alias.show` in the lane is unset. No tracked `.gitattributes`.

## Lane equality is not the proof

`git status --porcelain` on the counter, `sources/`, `corpus/SOURCES.md`, the lesson, and the knowledge entry was empty. Worktree `git hash-object` matched `git rev-parse 1c846ed2d67b1692ea966be064f0fc04542763c6:<path>` for the counter (`0808c865234a4a2bc95905622871807c5c77ee1d`), both retained texts, the receipt, SOURCES, the lesson, and the knowledge entry. That only says the tree is clean now.

Fail-closed check: `git cat-file -e 090ce8f1cfbae2dfb8bfa65dedd2c72861c48166:.ufo/waves/round-49/sources/S273.txt` failed, while the worktree file `.ufo/waves/round-49/sources/S273.txt` exists. A worktree open would see that file at the base revision. `git_show` returns `None`, and R4 records `retained text absent at revision` (`c49_quote_truth.py:175-176`).

## Residual — invocation, not R4

The frozen command is `python3 -B` on the worktree path `.ufo/waves/round-49/c49_quote_truth.py`, not `git show <revision>:` of that script. A dirty copy of the counter can print any score. C1 check 8 (`c49_order.py:167-175`) reads the *committed* counter blob and rejects the substring `os.path.join(root`. It does not execute the worktree file. A dirty script that opens a worktree path would move C2 while C1 still passes, until that edit is committed. A committed `open(f"{root}/...")` would also miss that substring; that mutation is the other seat's item, not applied here.

Not claimed: this seat did not re-run the frozen C2 command (owned by ExecRerunC2) and did not dirty the lane tree.

Report: .ufo/waves/round-49/w1/ReviewWorktreeRead.md
