# ScoutReopenNewRows — freshness

**Result: FAIL to demonstrate the named freshness attack (inputs unavailable); no stale or matching quote is claimed.**

At `2026-10-24T01:59:37-03:00`, the retained source directory, upstream candidate manifest, and source-row draft were all missing. Consequently there were no URLs or ≤25-word quotes to reopen: completed 0 live GETs; current-page quote checks, per-row HTTP statuses, and per-row fetch times are unavailable. No drift was assessed or silently re-pinned.

Evidence:

```text
Command: mkdir -p /fast/scratch/hyaku/kake-r46/ScoutReopenNewRows /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-46/attack && date -Is && for p in /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-46/sources /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-46/build/source-candidates.md /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-46/drafts/lesson-gate.md; do if test -e "$p"; then printf 'PRESENT %s\n' "$p"; else printf 'MISSING %s\n' "$p"; fi; done
2026-10-24T01:59:37-03:00
MISSING /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-46/sources
MISSING /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-46/build/source-candidates.md
MISSING /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-46/drafts/lesson-gate.md
```

The three `read` attempts on those paths each returned `Path '<path>' not found`. No network fetch was run because the required row inputs were absent.

Files written: `.ufo/waves/round-46/attack/ScoutReopenNewRows.md`, `.ufo/waves/round-46/w1/ScoutReopenNewRows.md`. Scratch directory created: `/fast/scratch/hyaku/kake-r46/ScoutReopenNewRows/` (no scratch files). No tools installed.
