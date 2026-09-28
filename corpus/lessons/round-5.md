# Lesson — round 5 (2026-09-28)

Cites: LOG.md round-5 entry; `corpus/knowledge/{ops-automation,
origin-repos,speedrun-pipeline}.md`; evidence in
`~/Projects/webzites/{state/probe-history.jsonl,
reports/keepers/repos-r{1..8}.md, reports/keepers/speedrun-r1.md,
docs/SPEEDRUN-PROTOCOL.md}` + `~/.config/systemd/user/webzites-*.timer`.
Commit `round-5`.

## The gap closed

Rounds 1–4 documented the *static* playbook: registry, publish verbs,
drift commands, journal codes. What they missed was the **ops layer that
was already running** and the **repo-evidence lane that already answered
the corpus's own "known gap"**.

Three surfaces had zero corpus coverage despite producing the strongest
evidence on disk:

1. **`webzites-probe.timer` (6h) + `webzites-keeper.timer` (daily)** —
   systemd user units since ~09-21; `probe-history.jsonl` holds 76 rows.
   Round-3's lesson ran a manual `probe --all` as though nothing watched
   the fleet — a <6h-old `probe-latest.json` was already on disk.
2. **`repos-r1..r8` wz-repos lane** — the README's "50 cloned repos
   undocumented" gap was *closed upstream* on 2026-09-21: 50/50 clones
   mapped, canonical writers byte-verified, 5 sourceless artifacts
   fingerprinted, frontier declared terminal. The corpus gap entry was a
   week stale the day it was written.
3. **Speedrun pipeline** — a complete second publish surface
   (record→report→prep→operator-push→X-draft) with its own redaction and
   fail-closed rules, absent from `publish-channels.md`.

## Evidence mined

- `probe-history.jsonl` transitions: `veigapunk-page` left `violated[]`
  between 09-21T04:14 and 09-22T22:58 (the human publish click);
  `charter-ghp` entered `violated[]` between 09-27T00:22–06:22 (marker
  churn, not an outage); `lucario` appeared already-violated at
  total-17→18 (registration event); `xsnapshot-app` `errors[]` every run
  = armed NXDOMAIN baseline, not a bug.
- `repos-r5` byte-verdicts: `ds4cc-website` is NOT the ds4cc.com source
  (sitemap lies; sha `70b2241e…` ≠ live `b6f65899…`); root
  `veigapunk.github.io` = `repos/VeigaPunk.github.io`, not
  `plazir-15-site` (single-writer risk); `burnerchrome.kimi.page`
  canonical = `repos/burnerchrome`, not the vendored
  `ds4cc-marketplace/burnerchrome/` dir.
- Full CLI verb surface (`webzites.mjs --help`): `status`, `map`, `auth`,
  `install`, `speedrun`, `ask`, `grokbot {start,log,reconcile,tick}`,
  `grokbots`, `bots {list,run,task,mint,digest,report}` — the
  per-site keeper-bot fleet was entirely undocumented in the corpus.

## Learned

- **Check `probe-latest.json` age before re-probing** — the timer already
  paid the fetch cost; a manual `--all` duplicates it unless the snapshot
  is stale.
- **History rows need per-row detail to mean anything** —
  `violated[]`/`errors[]` summary alone can't distinguish outage from
  marker-churn from registration; open `probe-latest.json` for the
  `fail[]` reasons.
- **"Known gaps" rot too** — the README's gap list itself needs
  verification each round; two of its three entries were already answered
  by evidence on disk (probe cadence: `probe-history.jsonl`; 50 repos:
  `repos-r8.md`).
- **A flat frontier upstream is still corpus work downstream** —
  wz-repos hit terminal saturation because remaining moves were
  operator-gated; its *evidence* was the payload this domain needed.
