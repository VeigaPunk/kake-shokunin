# ExecLandedCheck

Ticket: round-58 w1 report hygiene. Lane read-only; writes: this file and `w1/ExecLandedCheck.files/` only. Tool versions: `scripts/landed_check.py` at lane tip `cc8da16` (blob of the file at HEAD, unmodified), `scripts/id_resolver.py` at lane tip, `.ufo/waves/round-58/c58_resolver_cases.py` (version 1, in flux). No tools installed.

## LANDED CHECK:

Tool: `landed_check.py` — flags `--report`, `--repo`, `--branch`, `--selftest` (`--help`, exit 0). Reads hash-shaped tokens (7–40 hex, boundary-guarded) out of the report, resolves each with `git rev-parse --verify --quiet <tok>^{commit}`, and asks `git merge-base --is-ancestor <oid> <branch>`. Exit 0 = every cited commit is an ancestor; 1 = at least one is not; 2 = unevaluable (unresolvable branch/repo, or nothing resolvable); 64 = usage.

Self-integrity: `--selftest` → `selftest 14/14`, exit 0 (TMPDIR inside my scratch).

Target run — round-57 report `…/shokunin/.ufo/reports/round-57/kake.md` (84 lines) against lane `kake-shokunin`:

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/landed_check.py \
  --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-57/kake.md \
  --repo /home/vgpnk/Projects/shokunin/kake-shokunin --branch HEAD
```

Result: **`cited=9 landed=9 missing=0 unknown=0`, exit 0** — every cited hash is an ancestor of the lane tip. All nine printed as ANCESTOR: `28fa0b23e699303725aba2727094531f5e44494d`, `32754df75774dd38e8a96fcda375fc93adf97f1e`, `20217f23eca15862febe14545523832e21584106`, `b9a5d012f7fd`, `f7c98ff26928`, `cddef5b4fd36`, `4b8c73050470`, `51921b971246`, `31b61a4ddfca`. Twelve-character abbreviations resolve; the report's "final lane tip `20217f23…`" line is an ancestor of the current tip `cc8da16` (detached HEAD; `refs/heads/master` is also `cc8da16`). No suppressed digests, no UNKNOWN. Receipt: `.files/landed-check-round57.txt`.

Semantics I measured on a throwaway fixture repo (init under my scratch, toplevel asserted, commits only with `-c user.name=selftest -c user.email=selftest@local`; receipt `.files/landed-check-probe.txt`):
- **Invented hashes pass.** A report citing one real commit plus `deadbeef…` (40 hex) prints `cited=2 landed=1 missing=0 unknown=1`, **exit 0**. UNKNOWN is not a failure unless nothing landed.
- **Non-commit objects are skipped.** A blob oid on the same line is neither cited nor counted (the blob was cited on the line and `cited` stayed 2).
- **Bare 64-hex digests are skipped by length, label or not**: a digest-only report yields `cited=0`, **exit 2**.
- **Detached HEAD vs `master`:** a commit made on the detached lane is `NOT-ANCESTOR … missing=1`, **exit 1** with `--branch master`, and `ANCESTOR`, exit 0 with `--branch HEAD`. The lane is currently detached at `cc8da16`, so `master` will not advance with round-58 work.
- An **ambiguous 7-char abbreviation** resolves in neither direction → UNKNOWN (not a failure); a bare unlabelled 40-hex sha1 digest would be counted as an unknown citation (label it `sha256`/`digest` on the line, or the 64-hex values in `sources/receipts.json` — field name already `sha256` — are skipped anyway).

## RESOLVER BASE:

Assigned command, run verbatim (no `--fleet`, so the fleet defaults to the lane's parent, `/home/vgpnk/Projects/shokunin`):

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision 044048597d62f3199494b63b36e90dd57825e350
```

Output: **`ids_cited=106 ids_resolved=106 dangling=0 owned_elsewhere=0 unowned=0`, exit 0.** Receipt: `.files/resolver-base.txt`.

Cross-check with the contract's C2 counter at the same base revision (`c58_resolver_cases.py --revision 0440485… --work <scratch>`): **`C2 resolver-cases 7/12 met=False`, exit 1** — K1–K5 FAIL, each printing `exit=0 ids_cited=… dangling=0` (the same green summary shape as the assigned run); P1–P7 PASS, P7 = `exit=0 ids_cited=106 ids_resolved=106 dangling=0`. First line is byte-identical to the committed `controls/base-c2-resolver-cases.txt`; the rest is identical after normalising the scratch path in the P5 line (my extra `EXIT=1` line is the harness echo). Receipt: `.files/c2-counter-base.txt`.

Reading for the L1: the base resolver line **is the false green C2 targets** — green (`106/106`, exit 0) at a revision whose fenced-registry and git-quoted-path cases print the identical green summary. It must not be quoted as C2 before-evidence or as a before-number for a green claim; the before-receipt is `7/12`. The green line is also fleet-insensitive at base (nothing dangles, so sibling ownership never engages; the counter's P7 deliberately passes an empty fleet dir and still sees 106/106/0). `106` is exactly the contract's P7 floor: after this round's two new rows are cited by the two entries the after run should exceed it, so an after run still printing 106 meets the floor but means the entries are not citing.

## COMMANDS FOR L1:

One line, absolute paths, run from any cwd (report path follows the round-57 convention `…/.ufo/reports/round-<N>/kake.md`; `…/round-58/` exists, `kake.md` does not yet):

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/landed_check.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-58/kake.md --repo /home/vgpnk/Projects/shokunin/kake-shokunin --branch HEAD; echo "EXIT=$?"
```

How to read it: `NOT-ANCESTOR <tok>` = a cited commit is not in the lane tip's ancestry (fix the hash or the claim); `UNKNOWN <tok>` = the hash is not a lane commit (relabel it as fleet-root/other-repo or drop it — it does not by itself fail the run); `EXIT=1` = at least one NOT-ANCESTOR; `EXIT=2` = nothing resolvable, or the report/repo/branch is missing — a report with no resolvable hash citations cannot certify landing. Run it after the last lane commit, and again if any hash in the report is edited. **Use `--branch HEAD`, not `master`**: the lane is detached at `cc8da16`, so `master` stays behind and new commits would print NOT-ANCESTOR (measured above).

Scratch `/fast/scratch/hyaku/kake-r58/ExecLandedCheck` (fixtures, C2 work dirs) deleted before this report; the four receipts above are the retained evidence. Checks not run: the C1 and C3 counters, `--fleet` cross-lane ownership beyond P7, and the round-58 report check itself (no report exists yet).

VERDICT: round-57 report lands clean (9/9 cited hashes are lane ancestors, exit 0); the assigned base resolver line reads green (106/106, exit 0) but the C2 counter scores that same revision 7/12 — quote 7/12 as the before, run the round-58 check with `--branch HEAD`.
