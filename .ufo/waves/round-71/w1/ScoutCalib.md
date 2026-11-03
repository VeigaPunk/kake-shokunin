# ScoutCalib Report — Round 71 (Wave 1)

## S132 Verification
- Source: `/home/vgpnk/Projects/shokunin/kama-shokunin/corpus/knowledge/self-assessment-at-writing.md`
- Access date: 2026-11-03 (`date -I` exit 0: 2026-11-03)
- File SHA-256: `cd6e3730085ed08ca583604390e84c352ea122e4a6386e383d261a0a0b4cf959`
- Section heading: `# Checking self-assessment statements at writing`
- Located quote (18 words, line 7, first section-prose paragraph):
  `The check then evaluates the statement against the committed tree/history at `W`, not just against the current tip.`
- Substring confirmation:
  `grep -F -c 'The check then evaluates the statement against the committed tree/history at `W`, not just against the current tip.' ...` -> count 1 (exit 0)
- Historical companion quote (10 words, line 7):
  `records a calibration error present when the statement was written`
  `grep -F -c 'records a calibration error present when the statement was written' ...` -> count 1 (exit 0)

## Independent C1 Base Enumeration (commit cc6b4e0b8c35e72dfb02c6184b847f68c1262153)
1. `## Planned` headings:
   - Command: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc6b4e0b8c35e72dfb02c6184b847f68c1262153:SCORECARD.md | grep -n '^## Planned'`
   - Line 21: `## Planned` (body specifies `**Round 21**`)
   - Line 3990: `## Planned — round 48` (heading specifies round 48)
   - Total stale planned (< 72): 2 (`stale_planned=2`, lines [21, 3990])
2. Stated `attack share K/N`:
   - Command: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc6b4e0b8c35e72dfb02c6184b847f68c1262153:SCORECARD.md | grep -n 'attack share'`
   - Line 4770: `1 sentinel; attack share 4/14 ≈ 28.6 %), dispatched through the inline spawn handoff; no residual`
   - Stated attack share: `4/14` (K=4, N=14; count = 1 statement)
3. Strict attack role count in `.ufo/waves/round-70/w1-results.json`:
   - Command: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cc6b4e0b8c35e72dfb02c6184b847f68c1262153:.ufo/waves/round-70/w1-results.json | jq -r '.results[].agent' | sort | uniq -c`
   - Population: 14 results (connector 1, critic 1, executor 3, mutation-tester 1, revenger 1, reviewer 1, scout 3, scribe 2, sentinel 1)
   - Strict roles (`reviewer`, `critic`, `mutation-tester`, `labrat`): reviewer 1, critic 1, mutation-tester 1, labrat 0 -> strict count = 3/14 (revenger is excluded)
   - Attack mismatch: stated 4/14 != strict 3/14 -> `attack_mismatch=1`

## Counter Verification
- Command: `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-71/c71_calibration.py --revision cc6b4e0b8c35e72dfb02c6184b847f68c1262153`
- Output: `C1 revision=cc6b4e0b8c35e72dfb02c6184b847f68c1262153 stale_planned=2 stale_at=[21, 3990] attack_stated=4/14 attack_strict=3/14 attack_mismatch=1 guard=ok mismatches=3 met=False`
- Exit code: 1
- Parity: Exact match between independent counts and counter output (`stale_planned=2`, `attack_stated=4/14`, `attack_strict=3/14`, `attack_mismatch=1`, `guard=ok`, `mismatches=3`, `met=False`).

## Attacks and Verdicts
- Attack: S132 raw substring check (`grep -F -c`) — VERDICT: PASS (exact substring, count 1)
- Attack: S132 quote length <= 25 words — VERDICT: PASS (18 words)
- Attack: Stale planned headings in SCORECARD.md at base — VERDICT: DEFECT CONFIRMED (2 stale headings, lines 21 and 3990)
- Attack: Stated attack share vs strict count at base — VERDICT: DEFECT CONFIRMED (stated 4/14 vs strict 3/14, mismatch 1)
- Attack: Counter vs independent calculation — VERDICT: PASS (exact parity)
