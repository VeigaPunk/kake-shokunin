DEFECT: every pinned digest verifies, but SCORECARD.md/LOG.md quote timing ratios that disagree with the frozen receipt bytes — the prose numbers are stale, from an earlier scoring pass than the committed receipts.

Per-digest results (expected | observed | match):
- counter v4 `.ufo/waves/round-43/c43_count_v4.py`: 1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab | worktree sha256 identical; `git show b49cba9:…c43_count_v4.py` identical; `verification/freeze/counter-v4.sha256` agrees | match
- tool @ `020bc4574729ed674299f6cab02faac1582d9464`: 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021 | `git show 020bc457:scripts/sitemap_audit.py | sha256sum` identical; build-{1,2,3}.json `toolSha256` identical | match
- ref41 pin: 50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d @1ef7a0e95f6884dd113fe583a997c633fe330ddd (counter lines 84–85) | git-show hash identical; all receipts' `ref41Sha256` identical | match
- base40 pin: 4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e @8eb121c81ffebada064eefcabcd94dd2303d646f (lines 86–87) | git-show hash identical; receipts' `base40Sha256` identical | match
- `controls-r42/SHA256SUMS`: `sha256sum -c` exit 0, 4/4 OK; receipt `toolSha256` equals file sha for M8 `39160830…` and junk `e1cf8566…` | match
- PREDICATE: counter `PREDICATE` (c43_count_v4.py:78-80) == SCORECARD.md:3214 indented sentence == `predicate` field of build-1.json and ref41-base.json (python `==`) | match

Commands run (exit codes): `sha256sum c43_count_v4.py` 0; `cd controls-r42 && sha256sum -c SHA256SUMS` 0; `git show <rev>:scripts/sitemap_audit.py | sha256sum` ×3, 0; `git show --name-status b49cba9` 0; python receipt parsers 0.

DEFECT detail — stale ratio prose vs frozen receipts (committed blobs == worktree for build-{1,2,3}, ref41-base, r42ctl-junk_constant):
- SCORECARD.md:3217-3218 claims ref41-base "ratios T1 4.272, T2 1.931, T3 1.223, T4 1.229, T5 8.679"; frozen `ref41-base.json`/`.log`: T1 4.207, T2 1.917, T3 1.152, T4 1.228, T5 7.047 (seed 43001). Holds/overstated: verdict still **not met** (T1, T5 > 2.0) but every quoted digit is wrong.
- SCORECARD.md:3222-3223 claims build ranges T1 1.002–1.020, T2 1.150–1.194, T3 1.289–1.305, T4 1.245–1.258, T5 1.129–1.179; frozen receipts: T2 {1.201,1.250,1.213} all above quoted max; T3 {1.334,1.318,1.327} above quoted max; T4 {1.266,1.252,1.211} one below quoted min; T5 {1.105,1.144,1.215} one below min, one above max. Still **met ×3, 11/11**; ranges wrong.
- LOG.md round-43 entry repeats the stale numbers (ref41-base "T1 4.27, T5 8.68"; builds "T1 1.00–1.02, T5 1.13–1.18").

Conformant checks:
- Control receipts' unequal-run sets equal LOG's claims exactly: M8 F,T3; v1_casefold F,T2; v2_prefix32 E,F,T2,T3; v4_hosttable F,T3; junk 0/11 equal; ref41-base 11/11 equal, not met on cost.
- `git show --name-status b49cba9`: 46 paths, all inside the categories the message names (counter v4+builder, freeze receipts, controls-r42, registry checker, C2 pins/annotations incl. the two dated census EOF comments, SOURCES, lesson, LOG/SCORECARD). No off-message path.
- No seat score predates the freeze: the commit contains only L1 receipts; w1 spec landed in follow-up `eddbbf6`, `w1-spec.json` mtime 16:51:07 > commit 16:44:33 -0300. HEAD is `7c07079` (freeze +2).

Tool installs: none. Verdict on predicate-quoted ratio lines: overstated (stale), verdicts themselves hold.
