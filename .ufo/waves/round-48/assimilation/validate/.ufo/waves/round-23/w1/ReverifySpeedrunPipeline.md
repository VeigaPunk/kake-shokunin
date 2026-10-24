## Verdict

HOLD — author-side C1 freshness recommendation, not independent admission. The live published-data schema and canonical URL observations hold; one unflagged source citation is stale, and three operational claims cannot be established from the surviving surfaces.

## Findings

- **P2 — Stale keeper-source citations (C1 freshness).** The unit says the keeper card and `speedrun-r1` carry no absence flag, but both cited files are absent now.
  - **Command:**
    ```text
    for p in /home/vgpnk/Projects/webzites/docs/SPEEDRUN-PROTOCOL.md /home/vgpnk/Projects/webzites/src/speedrun.mjs /home/vgpnk/Projects/ds4cc-marketplace/speedrun /home/vgpnk/Projects/webzites/agents/webzites-speedrun.md /home/vgpnk/Projects/webzites/reports/keepers/speedrun-r1.md; do if test -e "$p"; then printf 'present %s\n' "$p"; else printf 'absent %s\n' "$p"; fi; done
    ```
  - **Exact observed output:**
    ```text
    absent /home/vgpnk/Projects/webzites/docs/SPEEDRUN-PROTOCOL.md
    absent /home/vgpnk/Projects/webzites/src/speedrun.mjs
    absent /home/vgpnk/Projects/ds4cc-marketplace/speedrun
    absent /home/vgpnk/Projects/webzites/agents/webzites-speedrun.md
    absent /home/vgpnk/Projects/webzites/reports/keepers/speedrun-r1.md
    ```
  - **Smallest fix:** Add explicit absence notes for the keeper card and report, or remove/replace those citations; do not present them as unflagged current sources.

## Checked and held

- Read `corpus/knowledge/speedrun-pipeline.md` in full. `git diff --no-ext-diff --unified=0 b5d599e19bead54b96f589444e9ec64cdf67c28a...HEAD -- corpus/knowledge/speedrun-pipeline.md` produced no output, so the anchors below match the base unit text.
- Primary page and manifest returned `200`; the public manifest currently references nine run JSONs. GET-and-parse of those nine records found an 18-key top-level intersection and `budget_usd` explicitly null in four records.
- The live Pages mirror returned `200` and declares `https://ds4cc.com/speedrun/` as its canonical URL. Its manifest currently has three run entries while the primary manifest has nine.
- Timer inventory showed `ai-usage.timer` (last 03:58:28 -03, next 04:03:28 -03), `cursor-shim-healthcheck.timer`, and no speedrun-named timer; the system timer list had nine entries and no speedrun-named timer. `crontab -l` failed with `error: command not found: crontab` (exit 127).

```json
{
  "unit": "speedrun-pipeline",
  "path": "corpus/knowledge/speedrun-pipeline.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "absence flags (re-census 2026-10-14) cover SPEEDRUN-PROTOCOL.md, speedrun.mjs",
      "claim": "The previously flagged local runbook and implementation paths remain absent.",
      "surface": "/home/vgpnk/Projects/webzites/docs/SPEEDRUN-PROTOCOL.md; /home/vgpnk/Projects/webzites/src/speedrun.mjs",
      "method": "test -e",
      "observation": "absent /home/vgpnk/Projects/webzites/docs/SPEEDRUN-PROTOCOL.md\nabsent /home/vgpnk/Projects/webzites/src/speedrun.mjs",
      "verdict": "HOLD"
    },
    {
      "id": "c2",
      "anchor": "while the keeper card and speedrun-r1 carry no absence flag",
      "claim": "The unflagged keeper-card and keeper-report references remain extant current source files.",
      "surface": "/home/vgpnk/Projects/webzites/agents/webzites-speedrun.md; /home/vgpnk/Projects/webzites/reports/keepers/speedrun-r1.md",
      "method": "test -e",
      "observation": "absent /home/vgpnk/Projects/webzites/agents/webzites-speedrun.md\nabsent /home/vgpnk/Projects/webzites/reports/keepers/speedrun-r1.md",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, `/home/vgpnk/Projects/webzites/agents/webzites-speedrun.md` and `/home/vgpnk/Projects/webzites/reports/keepers/speedrun-r1.md` are absent and should be marked unavailable rather than unflagged current sources."
    },
    {
      "id": "c3",
      "anchor": "Authority: `~/Projects/ds4cc-marketplace/speedrun/` ONLY;",
      "claim": "The historically designated local authority path remains absent.",
      "surface": "/home/vgpnk/Projects/ds4cc-marketplace/speedrun",
      "method": "test -e",
      "observation": "absent /home/vgpnk/Projects/ds4cc-marketplace/speedrun",
      "verdict": "HOLD"
    },
    {
      "id": "c4",
      "anchor": "refuses `--out` outside it.",
      "claim": "The live `prep --write` implementation refuses output paths outside the keeper mission root.",
      "surface": "/home/vgpnk/Projects/webzites and /home/vgpnk/Projects/webzites/src/speedrun.mjs",
      "method": "test -e",
      "observation": "absent /home/vgpnk/Projects/webzites\nabsent /home/vgpnk/Projects/webzites/src/speedrun.mjs",
      "verdict": "UNVERIFIABLE",
      "reason": "Both the named mission root and the implementation path are absent, so no current CLI is available to execute this guard and decide the behavior."
    },
    {
      "id": "c5",
      "anchor": "Board pollers ran at 5min;",
      "claim": "The cited board poller currently runs on a five-minute cadence.",
      "surface": "systemctl --user list-timers --all --no-pager; systemctl list-timers --all --no-pager; crontab -l",
      "method": "run",
      "observation": "User timers: ai-usage.timer last Wed 2026-10-21 03:58:28 -03, next Wed 2026-10-21 04:03:28 -03; cursor-shim-healthcheck.timer. System timers: 9 listed, none named speedrun. `crontab -l`: `error: command not found: crontab` (exit 127).",
      "verdict": "UNVERIFIABLE",
      "reason": "No current timer is identified as a speedrun/board poller, and the five-minute `ai-usage.timer` cannot be attributed to that poller from the available evidence."
    },
    {
      "id": "c6",
      "anchor": "`speedrun/data/run-*.json` (18 keys; `budget_usd` nullable in 4/9 runs;",
      "claim": "The primary board's currently served run records still have 18 common top-level keys and `budget_usd` explicitly null in four of nine records.",
      "surface": "GET https://ds4cc.com/speedrun/data/manifest.json and its nine `runs[]` JSON URLs",
      "method": "GET",
      "observation": "records=9\nnullable_budget_usd=4\nintersection_keys=18\nbudget_usd\ncategory\ncurrency\nduration\nid\nlinks\nmetrics\nnot_a_grant\npaid\nproduct\nprovider\nrunner\nstatus\nsummary\ntags\ntimeline\ntitle\nvenue",
      "verdict": "HOLD"
    },
    {
      "id": "c7",
      "anchor": "there is **no HTTP upload API**.",
      "claim": "The public board is served from GitHub Pages and has no HTTP upload API.",
      "surface": "GET https://ds4cc.com/speedrun/; GET https://ds4cc.com/speedrun/main.js; GET https://ds4cc.com/speedrun/data/manifest.json",
      "method": "GET",
      "observation": "Primary page 200 (13,521 bytes); manifest 200 (1,296 bytes); HTML contains `<script src=\"main.js\" type=\"module\"></script>`; `main.js` uses `fetch(path, { cache: \"no-store\" })` and parses JSON.",
      "verdict": "UNVERIFIABLE",
      "reason": "The local source/authority tree is absent; public GETs show a JSON-backed page but cannot establish its GitHub Pages origin or prove that no separate upload endpoint exists."
    },
    {
      "id": "c8",
      "anchor": "is a frozen `rel=canonical` copy — never stage into it.",
      "claim": "The live Pages mirror declares `https://ds4cc.com/speedrun/` as its canonical URL.",
      "surface": "GET https://veigapunk.github.io/plazir-15-site/speedrun/",
      "method": "GET",
      "observation": "200; raw HTML contains `<link rel=\"canonical\" href=\"https://ds4cc.com/speedrun/\" />`; mirror manifest has 3 `runs[]` entries while the primary has 9.",
      "verdict": "HOLD"
    }
  ]
}
```

## Limits

- **Skipped: `Cursor-Ultra empirical median 181s`.** The five-minute timer claim could not be attributed to a speedrun poller; no historical telemetry or corresponding source tree is present to re-establish the median.
- **Skipped: “frozen” mirror status and the `2026-10-12` removal date/cause.** A single GET confirms the current canonical link and that the mirror differs (3 entries versus 9), but cannot establish whether it was unchanged over time or when/why the local tree disappeared.
- **Skipped: sole-authority provenance and absence of an upload endpoint.** The local `ds4cc-marketplace` tree is absent; the public static page and JSON do not establish which repository is authoritative for the keeper CLI or prove endpoint nonexistence.
- **Skipped: sampling/source fallback, report generation, `prep` schema/redaction/failure behavior, duplicate-ID checks, staged receipt bytes, and post-draft/never-retry behavior.** The `webzites` implementation and mission root are absent; no telemetry or staged artifacts are available. No `prep --write`, copy, commit, push, deploy, account action, or X post was attempted.
- No build, lint, formatter, or tests were run; no tool was installed or updated. This assignment did not exercise candidate runtime code or assess unrelated canonical-runtime, rerouting, or saturation behavior.
