CONFORMANT
Axes: operability, freshness. Scoped result: no pre-freeze round-43 seat artifact found in the inspected committed history; no round admission judgment.
Freeze b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee: committer 2026-10-23T16:44:33-03:00 (=19:44:33Z). Author time 15:44:18-03:00 is NOT the freeze boundary.
Paths: W=.ufo/waves/round-43; V=W/verification/freeze; C=W/controls-r42. Every time below is 2026-10-23, UTC−03:00. Paired extensions enumerate both files with identical mtimes.
| Artifact | Filesystem mtime | Versus b49cba9 |
|---|---|---|
| V/build-1.{json,log} | 16:36:29.171206229 | before |
| V/build-2.{json,log} | 16:36:29.217925922 | before |
| V/build-3.{json,log} | 16:36:28.985549419 | before |
| V/census-after-r43.txt | 16:43:49.422589686 | before |
| V/counter-v4.sha256 | 16:36:05.418224004 | before |
| V/exits.txt | 16:36:35.945251821 | before |
| V/r42ctl-M8-port-five-digits.json | 16:36:29.151849417 | before |
| V/r42ctl-M8-port-five-digits.log | 16:36:29.151901427 | before |
| V/r42ctl-junk_constant.{json,log} | 16:36:21.259322937 | before |
| V/r42ctl-v1_casefold.{json,log} | 16:36:30.266621889 | before |
| V/r42ctl-v2_prefix32.{json,log} | 16:36:28.473491838 | before |
| V/r42ctl-v4_hosttable.{json,log} | 16:36:29.531241737 | before |
| V/ref41-base.{json,log} | 16:36:35.938295124 | before |
| V/registry-count-r42-check.txt | 16:40:39.340436203 | before |
| V/registry-count-r42-claims.json | 16:40:17.530421979 | before |
| V/registry-count-r43-check.txt | 16:40:39.368436221 | before |
| V/registry-count-r43-claims.json | 16:40:17.530908072 | before |
| V/sweep-after.txt | 16:38:16.269335198 | before |
| V/sweep-before.exit | 16:37:05.267277415 | before |
| V/sweep-before.txt | 16:37:05.257277407 | before |
| W/make_w1_spec.py | 16:51:07.549586486 | after |
| W/w1-spec.json | 16:51:07.567913522 | after |
| W/w1-run-stderr.txt | 16:51:18.758313940 | after |
| W/w1-run-output.json | 16:51:18.790270518 | after |
| W/w1-taskcall.json | 16:51:18.806944097 | after |
| W/w1-dispatch-log.txt | 16:51:44.588946273 | after |
| W/w1/swarm-registry.json | 16:51:18.787976051 | after |
Holds: all 28 verification files are committed at b49cba9; content reads and the recursive provenance search identify L1 freeze evidence, not round-43 seat results. SCORECARD.md:3186-3190 explicitly places these L1 receipts before dispatch.
Strongest attempted counterexample: V/build-1.json:6-13 and V/build-1.log:1 score before freeze, but identify the held round-42 revision 020bc4574729ed674299f6cab02faac1582d9464 and label freeze-build-1; this is not evidence of a round-43 seat scoring early. The other eight receipts/logs likewise use freeze-* labels; controls point into C (receipt :7-8).
Holds: V/sweep-before.txt:2 and V/sweep-after.txt:2 internally date generation to 19:37:05Z and 19:38:16Z, respectively; other retained check/census/hash/exit files contain no contrary dispatch or seat timestamp. V/exits.txt:1-9 records three build exits 0 and six control exits 1; not rerun here.
Holds on committed scope: parent 61046fcf has no round-43 path history; b49cba9 has no w1 artifacts; dispatch commit eddbbf607fd9069028d8c67b682582fd17881d02 directly follows b49cba9 at 19:51:44Z. Its log W/w1-dispatch-log.txt:1 names 19:51Z, after freeze. Registry commit 7c070797 follows at 19:52:23Z; registry :4-5 records 19:51:18.787Z. All-ref history also exposes same-time snapshot variants, not an earlier seat artifact.
Limit / overstated interpretation: Git stores no filesystem mtimes and cannot prove absence of never-committed, deleted, or off-repo scores. The table is live stat evidence; committed identities/content and ancestry support only the scoped chronology. “Every receipt postdates freeze” would be wrong (18 receipt/log files predate it), but is not the stated L1-versus-seat rule.
Smallest safe correction: none to the frozen approach on this evidence; retain the L1/round-43-seat distinction and qualify any global absence assertion. No demonstrated chronology harm to either reviewed axis.
Decisive commands below ran with exit 0; cwd /home/vgpnk/Projects/shokunin/kake-shokunin unless -C is explicit. Empty history/tree/diff output is the observed absence/equality evidence.
`timeout 30 prlimit --as=8000000000 -- git show --no-patch --format='%H parent=%P committer=%cI author=%aI' b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee eddbbf607fd9069028d8c67b682582fd17881d02 7c070797eb5b6661983995705b546a0b07a9ea41` → 0.
`timeout 30 prlimit --as=8000000000 -- git log --all --format='%H %P %cI %s' --name-status -- .ufo/waves/round-43` → 0.
`timeout 30 prlimit --as=8000000000 -- git -C /home/vgpnk/Projects/shokunin/kake-shokunin log b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee^ --format='%H %cI %s' --name-status -- .ufo/waves/round-43` → 0, empty.
`timeout 30 prlimit --as=8000000000 -- git ls-tree -r -l b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee -- .ufo/waves/round-43/w1/ .ufo/waves/round-43/w1-dispatch-log.txt .ufo/waves/round-43/w1-spec.json .ufo/waves/round-43/w1-taskcall.json .ufo/waves/round-43/w1-run-output.json` → 0, empty.
`timeout 30 prlimit --as=8000000000 -- git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --exit-code b49cba9ca7f15bb0dfaae33b638afa7cb4c793ee -- SCORECARD.md .ufo/waves/round-43/verification/ .ufo/waves/round-43/c43_count_v4.py .ufo/waves/round-43/controls-r42/` → 0, empty.
`timeout 30 prlimit --as=8000000000 -- git diff --exit-code 7c070797eb5b6661983995705b546a0b07a9ea41 -- .ufo/waves/round-43/w1-dispatch-log.txt .ufo/waves/round-43/w1-spec.json .ufo/waves/round-43/w1-taskcall.json .ufo/waves/round-43/w1-run-output.json .ufo/waves/round-43/w1-run-stderr.txt .ufo/waves/round-43/make_w1_spec.py .ufo/waves/round-43/w1/swarm-registry.json` → 0, empty.
`timeout 30 prlimit --as=8000000000 -- stat --printf='%n | %y | %s bytes\n' /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-43/verification/freeze/* /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-43/w1* /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-43/make_w1_spec.py` → 0.
`timeout 30 prlimit --as=8000000000 -- stat --printf='%n | %y | %s bytes\n' .ufo/waves/round-43/w1/*` → 0.
`timeout 30 prlimit --as=8000000000 -- sha256sum .ufo/waves/round-43/c43_count_v4.py .ufo/waves/round-43/registry_count_check.py .ufo/waves/round-43/controls-r42/*.py` → 0.
Tool identity: W/c43_count_v4.py SHA256 1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab; W/registry_count_check.py SHA256 35ca6d40f91215ab59b79ee9ccbf6e920bfc4067c3caf87173a86a6a87c535db.
Historical build: scripts/sitemap_audit.py at 020bc4574729ed674299f6cab02faac1582d9464, receipt SHA256 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021.
C/M8-port-five-digits.py SHA256 391608309640431acfc873d48e33189cf71a399faaa410ce6d65b910282bbb1f.
C/junk_constant.py SHA256 e1cf856673f57ef4ed65dcb903d198011cfaf17f3696139a3cea14ac0aa91c60.
C/v1_casefold.py SHA256 9993b842427d1592713309420626e46e42f1e56defab28b2f5349e6391cf4bc4.
C/v2_prefix32.py SHA256 eadf5df4b5c26059429a5dbffd2d87bcdbca6f460ba982c81360736e6856aa0f.
C/v4_hosttable.py SHA256 dc8b6ecdcc638d20d34f66aaeadd8aa8ba798f5307c2fa8d80a876d2ae16ece7.
No installs/upgrades, counter runs, builds, tests, network calls, subagents, or persistent processes. Only this report was written.
