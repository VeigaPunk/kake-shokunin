DRAFTED

Axes: freshness. This is a lesson-supplement draft, not a round verdict.

Behavior: wrote `/fast/scratch/hyaku/kake-r43/ScribeLessonSupplement/lesson-supplement.md` with `## Gate supplement` and `## Mistakes digest`.
Evidence identities: frozen counter `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-43/c43_count_v4.py` sha256 `1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab`; freshness sweep `scripts/freshness-sweep.mjs` sha256 `a1aa79d114093cc5b663e811e86a20a57bf37357dd8a3598c9e02084770d8d8b`. Reopen payloads: `/fast/scratch/hyaku/kake-r43/kake-r43-w1-ScoutReopen/re.html` sha256 `c5771cb13c076a0bf9413c0a9632ff7d3273bc703a889845c4d4eadaa261c231`; `rfc9844.txt` sha256 `7585b9a9ed2e6d350ac4e79d0bbb722e5ab3d22c93fb2a40ad03d832cdb4b135`.

Gate candidates:
- S126 — retain the existing mined row; opened 2026-10-23T19:53:08Z, quoted text holds; only a five-byte docs-footer clock changed vs the retained snapshot (`corpus/SOURCES.md:134`; `.ufo/waves/round-43/w1/ScoutReopen.md:11-16`).
- S127 — retain the existing mined row; opened 2026-10-23T19:53:08Z, quoted text holds and live bytes equal retention (`corpus/SOURCES.md:135`; `.ufo/waves/round-43/w1/ScoutReopen.md:18-22`).
- No new-source admission/rejection is evidenced. S129/S130 are L1 pre-wave imports, not seat openings (`SCORECARD.md:3273-3278`; `corpus/SOURCES.md:137-138`). Their locator convention and ReviewFreeze seat attribution have separate findings below.

Mistake classes included in the draft, each with evidence paths: stale SCORECARD/LOG timing figures and invalid control-before-build/fixed-seed/baseline claims (`RevengerFreeze.md`, `CriticC1Sizing.md`); overbroad C1 kill rule (`ReviewKillRule.md`); live controls that meet v4 (`CtlHeadTail.md`, `CtlPortLen.md`, `CtlCaseMemo.md`); seed-dependent v2-prefix evidence (`RevengerV3Receipts.md`, `ExecRerunControls.md`, `MutCounterPrefix.md`); counter coverage holes for port, scope/path, default-port, entry/exit, common/repeated-host, case-fold/T2 and untested F/T2 members (`MutCounterPort.md`, `MutBuildScope.md`, `MutBuildScheme.md`, `MutBuildPort.md`, `MutBuildMisc.md`, `MutCounterHost.md`, `MutCounterFold.md`, `MutCounterT2.md`, `SimplifierCounter.md`); generator prose/T3 scope issues (`ReviewCounterDiff.md`); registry checker census mismatch (`ReviewQualityV.md`); stale/mismatched C2 receipt counts and +2 movement-pointer shift (`ScribeReportInputs.md`, `ExecSweepFull.md`, `ReviewC2B.md`); whole-sweep §armed red is pre-existing, while the declared §paths gate passes (`ExecSweepFull.md`, `ReviewC2A.md`); S129/S130 locator/attribution precision and lesson taxonomy/disposition issues (`CriticFrontier.md`, `ReviewSourcesRows.md`, `ReviewLesson43.md`); receipt byte-equality overclaim (`ReviewCounterDet.md`).

C1 kill-rule evidence: `CtlHeadTail.md:1-18` confirms five live-seat controls with round-41-differing witnesses met v4 11/11 (a sixth met on one of three seeds); `CtlPortLen.md:1,12-31` confirms three more controls met across three seeds each; `CtlCaseMemo.md:1-3,16-35` confirms four more controls met 11/11 with witnesses. These reports directly confirm frozen rule (1) is triggered. Additional `met:true` scratch receipts for CtlRepeat and CtlPrefixCache await witness reports. The L1 owns the canonical judgment.

- Commands / outcomes: this scribe's `mkdir -p /fast/scratch/hyaku/kake-r43/ScribeLessonSupplement` completed with no output/error. Seat-reported, not rerun: `node scripts/freshness-sweep.mjs --section=paths` → exit 0, `VERDICT: OK` (`ReviewC2A.md:5-9`); `node scripts/freshness-sweep.mjs` → exit 1 at §armed and `--offline` → exit 0 partial (`ExecSweepFull.md:17-23`); source GETs and `sha256sum` → exit 0 (`ScoutReopen.md:5-9`). No build, test, sweep, scoring, network request, or install was run by this scribe. No product code, git/index state, or other lane file changed; only this report was written in the lane.

Out of scope: no source fetch by this scribe; no integration or round verdict. Some control-seat reports and other attack reports remained unlanded; missing reports are not treated as “none found.”

Artifacts:
- `/fast/scratch/hyaku/kake-r43/ScribeLessonSupplement/lesson-supplement.md`
- `.ufo/waves/round-43/w1/ScribeLessonSupplement.md`
