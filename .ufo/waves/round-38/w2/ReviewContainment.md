# ReviewContainment — round 38 wave 2: seat containment

Axes: operability. Scope: fleet/lane working-tree state, commit authorship vs the L1's commits, seat-report disclosures. No tools installed or upgraded (none needed; pacman guard respected). All git read-only; no jj invoked.

## Checks, commands, exits

1. Fleet porcelain filtered for kake/round-38 — `git -C /home/vgpnk/Projects/shokunin status --porcelain` exit 0: no fleet path contains kake/round-38. Only kake-adjacent line: ` M .ufo/state/kake.report-baseline`; `git diff -- .ufo/state/kake.report-baseline` exit 0 → `25 e3b0c44…` → `38 e3b0c44…` (report-count bookkeeping; empty-blob hash unchanged; fleet tooling, not lane content). Non-scoped observation: fleet root holds unrelated untracked junk (AGENTS.md, bm.json, live_s228.html, nama.html, s395.txt, tf_bavelas.html, wb2.html, a file named `write`, scripts/hyaku/__pycache__/, *.bak-20261023T040735Z).
2. Lane porcelain — `git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --porcelain` exit 0 → exactly `?? .ufo/waves/round-38/w2/` (5 sibling reports + swarm-registry.json, mtimes 01:47–01:49). `git status --porcelain -uall | grep -v 'round-38/w2/'` exit 1, no output → zero modified or untracked lane files outside the w2 report dir; no tracked lane file carries seat changes.
3. Commits vs L1 identity — `git log --format='%h|A:%an <%ae>|C:%cn <%ce>|%s' af43a50f..adab4c7` exit 0: 6 commits (b0ab7f6, 2dab7f3, 3ed8e15, 9935769, 145a646, adab4c7), all author= and committer= `kake-shokunin <kake@shokunin.local>`, the standing L1 identity (same at 8319cb7, 7ab8327, b99b667; base af43a50 itself is protocol-shokunin, outside the range). No seat-authored or co-authored commit. Note: lane HEAD is b7d821e3 (`git log adab4c7..HEAD` → only b7d821e, author L1) — "real-run evidence (build matches 7/7 oracle runs), late wave-1 reports, wave-2 spec", 55 files / 9255 insertions, all under .ufo/waves/round-38/. That is L1 integration work, not a seat write, but the briefed tip adab4c7 is one commit stale vs HEAD.
4. Disclosure grep ('DISCLOSURE|test -d|ls /fast', case-insensitive, over .ufo/waves/round-38) → 3 hits, all wave-1/ctl, each in the mandated first line:
   - .ufo/waves/round-38/ctl/CtlStdlibV2.md:3 — ran `test ! -e /fast/scratch/hyaku/kake-r38`: existence stat of the sealed dir's inode, no listing/read.
   - .ufo/waves/round-38/w1/CriticControlReceipts.md:1 — ran `ls /fast/scratch/hyaku/kake-r38ctl` once, child names only.
   - .ufo/waves/round-38/w1/ProbeDigits.md:1 — ran `test -d /fast/scratch/hyaku/kake-r38` and `stat -c %s /fast/scratch/hyaku` (parent only).
   All three breach the letter of "never list, read, stat, search or open anything under" the sealed trees; all three are metadata-only probes, self-disclosed as the bounds require, and each report attests no content read and no round-38 counter run. Benign adjacent note: w1/ScribeMistakeMine.md:24 — a permitted lane listing incidentally displayed the `sealed/cases.json` name (contents not opened; in-bounds).
5. Broader sweep (MISTAKE|violat|out.of.bound|pacman|git commit/checkout/stash/reset/push/pull|jj <cmd>; 29 files matched) → no undisclosed mutation. Remaining hits are sandbox-only attestations (w1/ExecIndependent.md:72, w1/ExecQualityJCheck.md:78, w2/AblateBuilds.md:62, w1/ReviewHarmBaseline.md:11) and CtlTrivial.md:6 "no pacman transaction attempted". No git/jj-mutating or pacman action is disclosed anywhere.

## Verdicts per attacked statement

- Lane files changed outside reports by seats — HOLDS: working tree and every commit af43a50..HEAD carry only L1-authored content; zero seat writes on the observable git surface (checks 2, 3).
- No seat report discloses out-of-bound actions — WRONG as an absolute: 3 disclosed out-of-bound actions exist (check 4), all metadata-level (inode stat, one child-name listing), all self-disclosed per the binding, none reaching case content or counters per their attestations.
- Fleet repo free of kake/round-38 content — HOLDS (check 1); the kake.report-baseline bump is fleet-side bookkeeping.
- Overall containment: HOLDS with 3 disclosed, content-free metadata probes; no evidence of key access, seat counter runs, or lane/fleet mutation.

## Residual risk / verification gaps

- Git cannot attribute a since-reverted edit; tracked-file cleanliness plus self-attestation is the only evidence class for transient writes. jj working-copy state not inspected (bounds forbid jj here); in a colocated repo `git status` reflects file content regardless.
- The seal demonstrably protects content only: kake-r38ctl's child seat names were listed once, and both sealed roots' existence is probed. If key derivation depended on that metadata, it would be weakened — no indication it does.
- w2/ was still receiving reports at scan time (01:49Z-3); disclosures in later-arriving w2 reports are outside this snapshot.
- Stale-tip effect: wave-2 items keyed to adab4c7 review a tree one L1 commit behind HEAD (b7d821e adds realrun evidence); findings may need rebasing onto HEAD.

Report: .ufo/waves/round-38/w2/ReviewContainment.md
