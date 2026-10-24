## Verdict

C1 `fire-journal-codes` is only partially re-verifiable as of 2026-10-21: two selected claims are HOLD (the cited script path remains absent; the slug URL remains 404), and five source/history claims are UNVERIFIABLE because the cited source and journal corpus are no longer available. No STALE verdict was assigned: absence of the historical corpus does not disprove its past contents. This is an author-side receipt, not independent admission.

```json
{
  "unit": "fire-journal-codes",
  "path": "corpus/knowledge/fire-journal-codes.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "script absent per the r20 correction below",
      "claim": "The recorded kimi-surface.mjs path remains absent now.",
      "surface": "/home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs",
      "method": "test -e",
      "observation": "script=absent",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "Every metered run writes a journal JSON to `state/`.",
      "claim": "The current implementation writes each metered run to a JSON journal under state/.",
      "surface": "/home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs",
      "method": "test -e",
      "observation": "script=absent",
      "verdict": "UNVERIFIABLE",
      "reason": "The cited implementation and its state directory are both absent; no live source remains to inspect or run to establish this behavior."
    },
    {
      "id": "c1",
      "anchor": "Top-level keys, measured over all 28 journals (r16 union) — exactly six:",
      "claim": "The historical 28-journal corpus has exactly six top-level keys, with error optional.",
      "surface": "/home/vgpnk/Projects/webzites/state/",
      "method": "test -e",
      "observation": "/home/vgpnk/Projects/webzites/state=absent",
      "verdict": "UNVERIFIABLE",
      "reason": "The cited state directory and its 28-journal corpus are absent, so the key census cannot be repeated."
    },
    {
      "id": "c1",
      "anchor": "post-fire anomaly on new-chat flow",
      "claim": "The listed code-6 new-chat anomaly is classified as consuming a metered fire.",
      "surface": "/home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs",
      "method": "test -e",
      "observation": "script=absent",
      "verdict": "UNVERIFIABLE",
      "reason": "The throw-site implementation and the associated journals are unavailable, so the historical code-6 behavior and fired-step state cannot be checked."
    },
    {
      "id": "c1",
      "anchor": "three journals carry `fire:true`",
      "claim": "The historical recreate-plazir15 run has three journals carrying fire:true.",
      "surface": "/home/vgpnk/Projects/webzites/state/recreate-plazir15-*.json",
      "method": "run",
      "observation": "matches=0",
      "verdict": "UNVERIFIABLE",
      "reason": "No matching journal is currently available at the cited path; that absence does not determine what the removed historical files contained."
    },
    {
      "id": "c1",
      "anchor": "version `efc1830` card created, preview 200+marker, `liveAfter.stillDead:true`",
      "claim": "The historical charter rebuild created version efc1830, had a marker-present 200 preview, and ended with stillDead true.",
      "surface": "/home/vgpnk/Projects/webzites/state/rebuild-charter-fire.log",
      "method": "test -e",
      "observation": "/home/vgpnk/Projects/webzites/state/rebuild-charter-fire.log=absent",
      "verdict": "UNVERIFIABLE",
      "reason": "The cited run log is absent, and the local artifacts needed to re-establish the historical preview result are unavailable."
    },
    {
      "id": "c1",
      "anchor": "state: live URL stays 404 until a human clicks the version card and sets",
      "claim": "The charter-ufo-fsd Kimi live URL currently responds 404.",
      "surface": "https://charter-ufo-fsd.kimi.page/",
      "method": "HEAD",
      "observation": "HTTP/2 404\ndate: Wed, 21 Oct 2026 07:00:26 GMT\n…\nstatus=404\nurl=https://charter-ufo-fsd.kimi.page/",
      "verdict": "HOLD"
    }
  ]
}
```

## Findings

### P2 — Cited implementation and journal evidence are unavailable

- **Exact commands:** `p=/home/vgpnk/Projects/shokunin/kake-shokunin; test -e /home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs && printf 'script=present\\n' || printf 'script=absent\\n'; git -C "$p" diff --quiet b5d599e19bead54b96f589444e9ec64cdf67c28a -- corpus/knowledge/fire-journal-codes.md && printf 'base_file=identical\\n' || printf 'base_file=differs_or_unavailable\\n'; for f in /home/vgpnk/Projects/webzites/state/rebuild-charter-fire.log /home/vgpnk/Projects/webzites/state; do test -e "$f" && printf '%s=present\\n' "$f" || printf '%s=absent\\n' "$f"; done` and `n=0; for f in /home/vgpnk/Projects/webzites/state/recreate-plazir15-*.json; do if test -e "$f"; then printf '%s\\n' "$f"; n=$((n+1)); fi; done; printf 'matches=%s\\n' "$n"; test -e /home/vgpnk/Projects/webzites/state/rebuild-charter-fire.log && printf 'charter_log=present\\n' || printf 'charter_log=absent\\n'`.
- **Exact observed output:** `script=absent`; `base_file=identical`; `/home/vgpnk/Projects/webzites/state/rebuild-charter-fire.log=absent`; `/home/vgpnk/Projects/webzites/state=absent`; second command: `matches=0` and `charter_log=absent`. Recursive globs for the named source script, charter log, and recreate journals under `/home/vgpnk/Projects/**` each returned `No files found matching pattern`.
- **Impact:** C1 freshness; the live journaling behavior, 28-journal key census, code-6 fire-consumption semantics, three-file fire count, and charter rebuild log claims cannot be independently reverified from their named source surfaces.
- **Smallest fix:** restore the cited source and immutable journal/log artifacts from a read-only archive, or explicitly retire/restate those historical claims as unverifiable. No run, publish, chat access, or other mutation is appropriate for this verification.

## Checked and held

- Read the full unit and the population manifest; the manifest names `fire-journal-codes` at `corpus/knowledge/fire-journal-codes.md`.
- `git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --quiet b5d599e19bead54b96f589444e9ec64cdf67c28a -- corpus/knowledge/fire-journal-codes.md` yielded `base_file=identical`, so the cited anchors match the required base revision.
- The public URL `https://charter-ufo-fsd.kimi.page/` is also named in `corpus/knowledge/publish-queue.md`; HEAD returned `HTTP/2 404`, `date: Wed, 21 Oct 2026 07:00:26 GMT`, `status=404`, `url=https://charter-ufo-fsd.kimi.page/`. This supports only the current 404 status at that exact URL, not the historical version-card or publish event.
- No selected claim was STALE, so no correction sentence applies. The number of files currently at the recreate glob is zero, but that does not falsify their historical contents.
- **Skipped claims and why:** exit-code meanings 1–5, 7, 8, and 64; remaining journal anatomy (`liveBefore`, `slugCheck`, `zip`, `canonCheck`, `attach`/`fired`, `baseline`, `versionWait`, `preview`, `liveAfter`, `operatorNext`); the `update ds4cc-kimi-mirror` and `recreate lucario` outcomes; the remaining `recreate plazir15` details; and the orphan/recovery rules. These depend on the unavailable script, journals, charter log, exact preview URL, or authenticated chat state; no Kimi chat was accessed. The S019 metadata-format note was not treated as a platform behavior claim and was not independently reverified.

## Limits

Only read-only local path checks, repository comparison, file reads, and one public HEAD were used. The current 404 does not establish whether a version card exists or whether any human action occurred. Historical claims remain unverified rather than disproved. No tools were installed or updated, and no build, lint, formatter, test, write/publish verb, or Kimi chat interaction was performed.