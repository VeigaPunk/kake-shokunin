# KakeR32.RerunC2Before — C2 before-measurement rerun

Axis: freshness. Scope: rerun the committed C2 counter at base rev
a0b0dffcd95b2215f638a5ff7591dd4fde325d27 against the lane and compare with
the L1 receipt .ufo/waves/round-32/verification/c2-before-a0b0dff.json.

## Commands run

1. `git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse HEAD`
   -> 285abcad632e3c1c57bb402232e7d218054db383 (lane tip), exit 0.
2. Read-only audit of .ufo/waves/round-32/c2_retained_count.py before running:
   it issues only `git rev-parse --verify` (line 36), `git ls-tree -r` (line 41)
   and `git show` (lines 50, 59) against the given --repo/--rev; no writes, no
   network. Safe to run with --repo on the lane.
3. `TMPDIR=/fast/scratch/hyaku/kake-r32/w1/RerunC2Before/tmp python3 -B
   /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-32/c2_retained_count.py
   --repo /home/vgpnk/Projects/shokunin/kake-shokunin --rev
   a0b0dffcd95b2215f638a5ff7591dd4fde325d27`
   -> exit 0, JSON printed on stdout (below).

## Observed output (my run)

```
{
 "schema": "kake-r32-c2-retained-v1",
 "rev": "a0b0dffcd95b2215f638a5ff7591dd4fde325d27",
 "c1BlobPaths": {
  "render.yaml": [],
  "apps-sdk/Dockerfile": []
 },
 "c1": false,
 "c2RowIds": [],
 "c2": false,
 "c3Cites": {},
 "c3": false,
 "met": 0
}
```

## Comparison vs verification/c2-before-a0b0dff.json

Identical on every field: schema, rev, c1BlobPaths (both keys present, both
path lists empty), c1 false, c2RowIds [], c2 false, c3Cites {}, c3 false,
met 0. Zero differences.

## Field notes

- c1 false: neither expected blob id (render.yaml
  d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252, apps-sdk/Dockerfile
  ee0b63819a9ce71e51469796541b9075e9676ae9) appears in `git ls-tree -r` of the
  base rev — no retained copies at base.
- c2 false: no `## Registry` row in corpus/SOURCES.md at base has a source
  cell containing both `ds4cc-marketplace` and `1fbdb8ed` with opened cell
  `2026-10-22` — the S062 row does not exist at base.
- c3 false: with zero matching row ids there are no citations to count in
  corpus/knowledge/render-web-services.md.
- Counter exit contract held: exit 0 on a valid revision, `met` in 0..3 (here 0).

## Not verified / bounds kept

- Did not rerun the after-rev measurement (RerunC2After's seat) and did not
  byte-compare the retained copies against ~/Projects/ds4cc-marketplace;
  this seat only checked the before state.
- No lane mutation: only read-only git invocations; TMPDIR pointed at my
  sandbox /fast/scratch/hyaku/kake-r32/w1/RerunC2Before/tmp; this report is
  the only file written in the lane.
- No tools installed or updated; no network use; no live requests to owned
  properties.

Report: .ufo/waves/round-32/w1/RerunC2Before.md
