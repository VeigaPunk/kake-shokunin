# Residual seat — counter reruns (ResidCounterRerun), 2026-10-23

Scope: fresh reruns of round-41 counters v1 and v2, two runs each with random seeds, on the FINAL
build at lane tip `b9bf1a39362ec7c7fe06d80cc4162aa8ca3bca8f`. Sandbox:
`/fast/scratch/hyaku/kake-r41resid/ResidCounterRerun/` (v1-1.json, v1-2.json, v2-1.json, v2-2.json).

## Commands and exits (each: `timeout 600 prlimit --as=4000000000 python3 -B <counter> --root
/home/vgpnk/Projects/shokunin/kake-shokunin --revision b9bf1a39362ec7c7fe06d80cc4162aa8ca3bca8f
--out <sandbox>/<out> --label <label>`)

| Run | Counter | exit | seed (recorded) | passed | met | toolSha256 |
|---|---|---|---|---|---|---|
| resid-v1-r1 | c1_count.py | 0 | 241377799312099 | 1434/1434 | true | 50287ac6…1dde7d |
| resid-v1-r2 | c1_count.py | 0 | 194553218322845 | 1434/1434 | true | 50287ac6…1dde7d |
| resid-v2-r1 | c1_count_v2.py | 0 | 213894384587311 | 1434/1434 | true | 50287ac6…1dde7d |
| resid-v2-r2 | c1_count_v2.py | 0 | 58601083554260 | 1434/1434 | true | 50287ac6…1dde7d |

All four: byField loc 630/630, sitemapUrl 804/804; note null; counterSha256 / oracleSha256 as below.

## sha256 of reviewed bytes

- audited tool at revision (`git show b9bf1a39…:scripts/sitemap_audit.py`):
  `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d` — equals the SCORECARD final tool.
- counter v1 `.ufo/waves/round-41/c1_count.py`: `2acc443af33466796ad178d8c1ad8350d36250b29e7383bba4ba10d2e4fe67b4`
  (= recorded counterSha256 in both v1 outputs).
- counter v2 `.ufo/waves/round-41/c1_count_v2.py`: `53a0ec1bef93c6a3f70b9af096caf6832a132b938be9a1c5815c670366a45f8d`
  (= recorded counterSha256 in both v2 outputs).
- oracle wheel `.ufo/waves/round-41/oracle/abnf-2.9.1-py3-none-any.whl`:
  `cdcac127b3693ded2b00565878d8ed2b96d34b29f0ee199c06d7b40baaf60917` (= ORACLE_SHA256 in both counters,
  = S118's pinned digest).
- No tools installed or upgraded (none needed); no pacman use.

## Findings

1. HOLDS — the counter records reproduce on the final build from fresh random seeds: passed 1434/1434,
   met true under both v1 and v2, tool bytes 50287ac6… identical in all four. Consistent with
   `verification/build3/c1-v{1,2}-build3-4100{1,2,3}.json` (same passed/met/toolSha256).
2. `toolExit: 2` in all four records is the established baseline, not new behavior: the wave-2 build3
   records show the same toolExit 2 (mixed input/policy findings on a manifest that deliberately contains
   invalid values); the counter judges stdout findings only and does not require tool exit 0.
3. The counter's predicate remains met while SCORECARD/SKILL correctly keep labeling it "information"
   (kill rule (1) fired pre-build because wave-1 controls also met it) — rerunning does not contradict
   the exploratory status: a met counter over a class that junk controls also pass is consistent with
   both the lesson's wave-1 section and SKILL.md:1173-1175.

## Verification gaps

- Four seeds only (2 per counter) — statistical, not exhaustive; seeds recorded above for replay.
- Counter case generator and oracle logic were read (sha256 above), not independently reimplemented;
  the oracle wheel bytes are the vendored S118 digest, not re-fetched (no network used).
