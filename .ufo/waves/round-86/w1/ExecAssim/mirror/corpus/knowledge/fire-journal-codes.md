source: ~/Projects/webzites/scripts/kimi-surface.mjs (die/throw sites) + ~/Projects/webzites/state/{update,recreate,rebuild}-*.json run journals + state/rebuild-charter-fire.log (own-work; no SOURCES.md id); metadata format per S019 (metadata authority only, not a platform source)
verified-at: 2026-09-28 (die/throw sites in kimi-surface.mjs; journals 2026-09-26/09-27) — historical-not-live-reverified; script absent per the r20 correction below
recheck: on journal or script change — test -e ~/Projects/webzites/scripts/kimi-surface.mjs && echo present || echo absent; grep -lE '"fire": *true' ~/Projects/webzites/state/recreate-plazir15-*.json; script vanished in W7 — operator must restore it or retire this entry

# kimi-surface fire journals & exit codes

Source: `~/Projects/webzites/scripts/kimi-surface.mjs` (die/throw sites grep'd
> *[r20 citation-local 2026-10-19: `~/Projects/webzites/scripts/kimi-surface.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; historical record, not an executable instruction.]*
2026-09-28) + `~/Projects/webzites/state/{update,recreate,rebuild}-*.json`
run journals (09-26/09-27) + `state/rebuild-charter-fire.log`.

Every metered run writes a journal JSON to `state/`. **Top-level keys, measured
over all 28 journals (r16 union) — exactly six:** `site`, `mode`, `startedAt`,
`steps[]`, `fire: bool`, and optionally `error: {message, code}` (12/28 have
`error`). The r1–r15 text listed `newVersion`, `preview`, `operatorNext`,
`liveAfter` as if top-level: they are **not** — `preview`/`liveAfter` appear as
`steps[]` entry names, `operatorNext` only in `state/rebuild-charter-fire.log`,
and `newVersion` nowhere as a key. **The exit code alone
does not tell you if a metered fire was consumed — read `fire` + which step
died.**

## Exit codes (from throw sites, 2026-09-28)

| code | Meaning | Fire consumed? | Next action |
|---|---|---|---|
| 1 | lease held / generic die() | no | wait for lease TTL or find holder; retry |
| 2 | lane/preflight infrastructure (CDP down, no kimi tab, tab new, live fetch) | no | `browser ensure`, re-check live URL, retry |
| 3 | binding/target safety refusal (not uuidv8, no chat binds url, ambiguous binding, non-owner chat, stale publishedUrl, slot not dead, vessel not pristine, chat already published) | no | resolve binding via `kimi-map`/`GetWebsiteByChatID`; pick correct verb; do not retry same args |
| 4 | mid-prep DOM failure AFTER tab/attach (page never ready, draft in composer, insert failed, send click failed, send unconfirmed) | **check journal** — `fire:true` + error code 4 means send may have happened | journal `fired` step: if present, operator inspects chat before any retry; if died at ready/draft/insert, safe to retry |
| 5 | abort-before-send guard (no transfer payload, require-zip failed, send never armed, both channels failed) | **no** — abort happened before send | fix payload/zip/attach and retry freely |
| 6 | post-fire anomaly on new-chat flow (never navigated to /chat/uuid, could not read chat id, no description-matched version within 15min) | **yes — metered fire consumed** | do NOT refire blindly; inspect browser/chat for the version card; recover chat id manually |
| 7 | auth expiry OR post-fire anomaly (session expired at RPC, baseline ListVersions failed, foreign versions on target, GATE FAILED liveAfter) | **yes if journal got past `fired`** | auth: operator re-login + `browser status`; anomaly: operator inspects card, never auto-retry |
| 8 | transport failure (`Failed to fetch` at an RPC) | no | transient — retry once (kimiFetch already retries internally) |
| 64 | usage/flag error (unknown site arg shape, missing --confirm, bad --canonical, rebuild without --chat) | no | fix invocation |

## Journal anatomy (what each step proves)

- `liveBefore` `{status,sha256,dead:true}` — proves the slot was the kimi
  dead-slot page before firing (recreate gate).
- `slugCheck` `{available:true}` — slug was free at fire time.
- `zip` `{path,bytes,sha256}` — the payload sent; keep the path for audit.
- `canonCheck` `{status:200,markerPresent:true}` — canonical fetch verified
  (fallback transfer channel when zip attach fails).
- `attach {ok,confirmed}` / `fired {sentConfirmed}` — the metered moment.
  Anything before `fired` is free; anything after is post-fire.
- `baseline {seedCount}` → `versionWait {tipAfter {id,short}}` — the new
  version card claimed, matched by fire-description.
- `preview {status:200,url:https://p-*.kimi.page/,markerPresent}` — the
  *preview* URL works. **A green preview does NOT flip the live slot.**
- `liveAfter {stillDead:true, chatPublishedUrl:null}` — normal terminal
  state: live URL stays 404 until a human clicks the version card and sets
  the slug. `GATE FAILED` (code 7) is only for unexpected post-fire live
  states, not for stillDead.
- `operatorNext` — verbatim human instruction (chat URL + slug to set).

## Observed run outcomes (state/ 09-26→09-27)

| Run | Outcome | Reading |
|---|---|---|
| `recreate plazir15` ×3 fired | code 7 (session expired mid-run), code 4 (`tab` died), code 6 (no /chat/uuid nav) | fires likely consumed on the code-6 run; **three** journals carry `fire:true` (r16 re-count over `state/recreate-plazir15-*.json`: `…T142712310Z` c7, `…T144433810Z` c4, `…T144616014Z` c6) — r1–r15 said "×2", an undercount; slot still 404 — version cards may exist orphaned in chats; operator must inspect |
| `rebuild charter-ufo-fsd-kimi` | success end-to-end: version `efc1830` card created, preview 200+marker, `liveAfter.stillDead:true` | correct terminal state; awaits human publish + slug `charter-ufo-fsd` |
| `update ds4cc-kimi-mirror` ×7 | preflight mix: lease-held (1), transport (8), then fired run hit code 7 session-expired at ListVersions | the fire consumed but version-baseline read failed → code-7 anomaly; operator inspects that chat before any refire |
| `recreate lucario` ×3 | all preflight (`fire:false`), stopped at canonCheck | zero fires consumed; safe to re-run |

## Rules for the next agent

1. **Never decide retry from the exit code alone** — open the journal, find
   whether a `fired` step exists, and which step died.
2. **Codes 6 and 7 post-`fired` = ANOMALY**: a metered fire was consumed and
   state is uncertain. Hand to operator; do not auto-refire.
3. **Successful recreate/rebuild never flips the live URL.** Terminal
   `stillDead:true` + a claimed version card + working `p-*.kimi.page`
   preview = done for the agent; the rest is the human publish click.
4. **Orphan risk**: a fired run that dies before `versionWait` (code 4/6/7)
   can leave a version card in an unknown chat. `kimi-map` sweep + match by
   fire-description timestamp is the recovery path.

## Live re-verification — round 23 (2026-10-21)

Read-only live checks; receipt `.ufo/waves/round-23/receipts/fire-journal-codes.json` (claim, surface, method, observation). A HOLD is an observation on 2026-10-21, not a guarantee. Where this section and earlier text disagree, this section is newer.

- [fire-journal-codes:c1] **HOLD** — The recorded kimi-surface.mjs path remains absent now. Surface: `/home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs`.
- [fire-journal-codes:c2] **UNVERIFIABLE** — The current implementation writes each metered run to a JSON journal under state/. Surface: `/home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs`. Unverifiable: The cited implementation and its state directory are both absent; no live source remains to inspect or run to establish this behavior.
- [fire-journal-codes:c3] **UNVERIFIABLE** — The historical 28-journal corpus has exactly six top-level keys, with error optional. Surface: `/home/vgpnk/Projects/webzites/state/`. Unverifiable: The cited state directory and its 28-journal corpus are absent, so the key census cannot be repeated.
- [fire-journal-codes:c4] **UNVERIFIABLE** — The listed code-6 new-chat anomaly is classified as consuming a metered fire. Surface: `/home/vgpnk/Projects/webzites/scripts/kimi-surface.mjs`. Unverifiable: The throw-site implementation and the associated journals are unavailable, so the historical code-6 behavior and fired-step state cannot be checked.
- [fire-journal-codes:c5] **UNVERIFIABLE** — The historical charter rebuild created version efc1830, had a marker-present 200 preview, and ended with stillDead true. Surface: `/home/vgpnk/Projects/webzites/state/rebuild-charter-fire.log`. Unverifiable: The cited run log is absent, and the local artifacts needed to re-establish the historical preview result are unavailable.
- [fire-journal-codes:c6] **HOLD** — The charter-ufo-fsd Kimi live URL currently responds 404. Surface: `https://charter-ufo-fsd.kimi.page/`.
