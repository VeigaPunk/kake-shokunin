## Verdict

Counterexample found: **P3 claim-selection coverage gap only**. No tested HOLD is false, so there is no P1. The three UNVERIFIABLE claims c4/c5/c6 remain undecidable from the reachable present-day surfaces; I found no live copy of the missing webzites tree or its source.

## Findings

### P3 — Receipt omits the more consequential reconcile false-green contract (freshness / claim-selection coverage)

`corpus/knowledge/free-read-verbs.md:150-157` records two high-impact reconcile hazards: `in-sync` can mask GHP byte drift, and `no-source-file` is excluded from reconcile's exit-1 set, so a missing root page can render `NOSRC` while the command exits 0. The selected c5/c6 claims cover probe snapshot clobbering and status exit behavior, but the receipt has no reconcile-verb claim. This omitted contract is more consequential to a keeper relying on the free-read verbs than c8's single-page HTTP/byte-count observation. I cannot establish that the historical behavior still holds: the required implementation sources are absent:

```text
$ for p in /home/vgpnk/Projects/webzites/src/cli.mjs /home/vgpnk/Projects/webzites/src/reconcile.mjs; do test -e "$p" && echo "PRESENT $p" || echo "ABSENT $p"; done
ABSENT /home/vgpnk/Projects/webzites/src/cli.mjs
ABSENT /home/vgpnk/Projects/webzites/src/reconcile.mjs
```

Smallest fix: include the reconcile false-green hazard in the freshness selection, explicitly UNVERIFIABLE while its source is absent, or clearly scope the old code-derived warning as historical. This is a coverage gap, not evidence that the warning is false today.

## Checked and held

- **c1 HOLD holds.** Command: `test -e /home/vgpnk/Projects/webzites; echo "c1 test -e rc=$?"`. Output: `c1 test -e rc=1`. The path is absent.
- **c3 HOLD holds.** Command: `command -v webzites || echo "webzites: not on PATH"`. Output: `webzites: not on PATH`. A separate login-shell check also returned `login shell: webzites not on PATH`.
- **c8 HOLD holds.** Command: `curl -sS -o /dev/null -w 'status=%{http_code} effective_url=%{url_effective} size_download=%{size_download} content_type=%{content_type} redirects=%{num_redirects}\n' https://veigapunk.github.io/plazir-15-site/`. Output: `status=200 effective_url=https://veigapunk.github.io/plazir-15-site/ size_download=38337 content_type=text/html; charset=utf-8 redirects=0`. A body capture returned `size_download=38337`, SHA-256 `d82af77aee401d2270c719c6e818256298cc8aad7a71c3e7c4d65bd41f6af18e`, and `wc -c` `38337`. This matches the historical served-body hash prefix and size; it does **not** compare against the absent historical local source tree.
- **c4 remains UNVERIFIABLE.** `test -e /home/vgpnk/Projects/webzites/fleet/fleet.config.json && echo PRESENT || echo ABSENT` returned `ABSENT`. The file's present-day row counts cannot be derived from this missing config.
- **c5 remains UNVERIFIABLE.** The exact source/capture checks returned:
  ```text
  ABSENT /home/vgpnk/Projects/webzites/src/cli.mjs
  ABSENT /tmp/kake-r11/probe-ds4cc.out
  ABSENT /tmp/kake-r11/labrat-probe.md
  ```
- **c6 remains UNVERIFIABLE.** The exact source/capture checks returned:
  ```text
  ABSENT /home/vgpnk/Projects/webzites/src/cli.mjs
  ABSENT /tmp/kake-r12/live/status-json.out
  ABSENT /tmp/kake-r12/labrat.md
  ```
  I checked for alternate reachable source: `/home/vgpnk/Projects` has no `webzites` tree, a home search found no other `*webzites*` path at the searched depth, Trash had no retained copy, `https://github.com/VeigaPunk/webzites` returned 404, and the public VeigaPunk repository filter for `webzites` returned `0 results`. The GitHub API endpoint returned 403, so it was not treated as evidence.
- **Selection check:** The live `ds4cc.com` GET is another candidate surface, but its dated 2026-09-28 79,453-byte observation is explicitly historical in the knowledge file. The current read-only GET returned `ds4cc status=200 size=76159`; this is not a false HOLD in the receipt because no c1 claim asserts that old size is current. The selected c5/c6 claims already cover the document's principal probe/status hazards; the P3 gap above is the more consequential omitted reconcile hazard.

## Limits

Read-only checks only; no source restore, command execution, state mutation, builds, or tests. The absence of accessible source/captures leaves c4/c5/c6 and the reconcile behavior unverified; a private or otherwise inaccessible source copy cannot be ruled out. No tools were installed or updated.