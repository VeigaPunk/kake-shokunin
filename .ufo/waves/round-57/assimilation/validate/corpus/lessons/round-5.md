# Lesson — round 5 (2026-09-28)

Cites: LOG.md round-5 entry; `corpus/knowledge/{ops-automation,
origin-repos,speedrun-pipeline}.md`; evidence in
`~/Projects/webzites/{state/probe-history.jsonl,
reports/keepers/repos-r{1..8}.md, reports/keepers/speedrun-r1.md,
docs/SPEEDRUN-PROTOCOL.md}` <!-- r18 re-census 2026-10-14: the webzites tree (state/probe-history.jsonl · reports/keepers/repos-r1..r8 · speedrun-r1 · docs/SPEEDRUN-PROTOCOL.md) absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. --> + `~/.config/systemd/user/webzites-*.timer`.
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

## Gate

Retrospective round-21 reconstruction, not the original round-5 admission.
Round 5 recorded no Gate, candidate list, or admit/reject ledger. The outcomes
below are derived afterward from the corpus and aggregator files named per
item; they do not claim that round 5 admitted or rejected anything.

Candidates (from the original sections "The gap closed", "Evidence mined",
and "Learned"), with historically supported outcome:

- **Ops layer already running** (`webzites-probe.timer`,
  `webzites-keeper.timer`): split. Probe timer: admitted with qualification
  (enabled, active, and growing `probe-history.jsonl` were the aggregator's
  verified-true half). Keeper timer: **refuted**. `is-enabled` disabled,
  `is-active` inactive, journal empty; it had never executed
  (`round-5-aggregator-audit.md` Major 1; `keeper-timer-inert.md` r12
  correction to `ops-automation.md`).
- **veigapunk-page left `violated[]` between 09-21T04:14 and 09-22T22:58**:
  **refuted as a window**. Raw rows: last violated run 09-21T03:32:06, first
  clean run 09-21T04:14:50; the 04:14:50 and 09-22T22:58:23 sweeps carry
  identical `violated[]` sets (`round-5-aggregator-audit.md` Minor 2;
  `round-10.md`, "The r5 veigapunk-page record was wrong"). Round-10 records
  the correction in `ops-automation.md`; `round-6-aggregator-audit.md`
  detector row confirms the 04:14:50 EXIT event (correction landed dd4eabf).
- **charter-ghp entered `violated[]` 09-27T00:22–06:22 (marker churn, not
  outage)**: **unverified** for this exact window. `keeper-timer-inert.md`
  (r12) attributes the charter-ghp pin to config lag plus a human edit, which
  is consistent with the marker reading but does not check the window.
- **lucario appeared already-violated at total 17→18 (registration event)**:
  **admitted with qualification**. `round-5-aggregator-audit.md` re-executed
  the registration-event reading; `probe-delta-alerting.md` reproduction table
  matches the ENTER at 09-27T16:38:27 with UNIVERSE 17→18 (round 10).
- **xsnapshot-app `errors[]` every run = armed NXDOMAIN baseline**: the
  "every run" constancy is **refuted**. Membership is absent in 7 runs
  09-21T00:42→01:33; constant membership starts 09-21T01:34:20
  (`round-5-aggregator-audit.md` Minor 3). The NXDOMAIN-baseline reading
  itself was not contested in the sources read.
- **repos-r1..r8: 50/50 clones mapped; byte-verdicts** (ds4cc-website is not
  the ds4cc.com source; root `veigapunk.github.io` = `repos/VeigaPunk.github.io`;
  `burnerchrome` canonical = `repos/burnerchrome`): byte-verdicts **admitted**
  as corpus knowledge in `origin-repos.md` ("Byte-verified canonical writers
  (r5–r8)"). Their cited evidence (`repos-r1..r8.md`) is absent from the
  current tree per the lesson's own r18 re-census note, so they are
  **unverified against primary evidence now**. The "5 sourceless artifacts"
  count read as pass with a scope warning (5 ≠ 8 rows lacking `sourceDir`) in
  `round-6-aggregator-audit.md`.
- **Speedrun pipeline absent from `publish-channels.md`**: **unverified** in
  this pass; the cited `speedrun-pipeline.md` was not re-read.
- **Full CLI verb surface; keeper-bot fleet "entirely undocumented"**:
  **unverified** as a claim about round 5. Later `free-read-verbs.md`
  (r11/r12) documents `bots list` and `bots report`, so the gap was partly
  covered afterward; that does not show the original sweep was complete.
- **Learned: per-row detail is needed to read history rows**: **admitted with
  qualification**. Round 10 needed the raw rows to find the round-5 window
  error (`round-10.md`).
- **Learned: "known gaps" rot**: **admitted**. The README `violated[]`
  alerting gap, flagged round 5, stayed open until round 10 (`round-10.md`).
- **Learned: check `probe-latest.json` age before re-probing; a flat upstream
  frontier is still downstream work**: **unverified**. No later record in the
  sources read tests either claim.

Rejected: not recorded. Neither `round-5.md` nor the LOG.md round-5 entry
records a rejected candidate. The corrections above refute stated claims; they
are not rejections recorded by round 5.

Outside spot-check: existing independent non-author evidence, cited and not
newly run: `round-5-aggregator-audit.md` (aggregator round-5 reviewer, 26
citations re-executed, plus L1 re-run; verdict NOT conformant, 1 major and 3
minors) and `round-6-aggregator-audit.md` (re-check rows for the flip-window
correction and the sourceless count; keeper claim uncorrected through round
10). Admit/reject spot-check: not recorded.

Later in-lane corroboration (author-side, not outside): `round-10.md`
(delegated read-only L2 probes and L1 self-runs under `/tmp/kake-r10/`;
planner, labrat, and reviewer agreement on the veigapunk record) and
`keeper-timer-inert.md` (r12 read-only `systemctl`/`journalctl` check). These
are the lane's own seats and later rounds, not independent review.
Round 21 ran no new spot-check and did not re-verify live state.

Sources for this gate: original sections "The gap closed", "Evidence mined",
and "Learned" of this file. The round-21 lesson (`corpus/lessons/round-21.md`)
was not present in `corpus/lessons/` when this gate was appended, so it is not
cited as evidence. The S019 metadata/gate contract is referenced by
`.ufo/waves/round-21/wave1-spec.json` as metadata authority, to be registered
by L1 in CORPUS.md; no S019 entry or CORPUS.md was found in `corpus/` at read
time. This gate follows the round-20 `## Gate` shape (candidates, rejected,
outside spot-check).
