# Lesson — round 7 (2026-09-28)

Cites: LOG.md round-7 entry; `corpus/knowledge/sitemap-orphan-audit.md`;
evidence = `/tmp/orphan-check.mjs` baseline (~20:20Z, 103 locs) +
`pages.yml` deploy-graph reads + `state/probe-latest.json` (18:51Z).
Commit `round-7`. Zero publishes, zero metered ops.

## The gap closed

README's residual "live-only orphan paths (needs sitemap crawl, not
source walk)" — closed two ways at once: a sitemap sweep baseline AND a
proof that the scary version of the gap can't exist on GHP.

## What the audit actually found

- **103 sitemap-listed URLs across the three GHP rows: 0 orphans, 0
  dead listings, 0 listed-but-404.** ds4cc-com 93 locs from the *staged*
  (unpushed) `sitemap.xml` — doubles as a pre-push drift preview: every
  listed path already serves 200.
- **GHP live-only orphans are impossible by construction.** Both
  `pages.yml` workflows do `upload-pages-artifact path: <repo root>` —
  every deploy ships the entire checked-out tree as a fresh artifact.
  A deleted file can't linger live; the served set ≡ last-pushed
  `origin/main` tree. The round-6 source walk against `origin/main`
  already covered this direction modulo push→deploy lag.
- **`/` is `index.html`** — the membership classifier needs the
  `rel`, `rel/index.html`, AND root-`index.html` candidates; the first
  pass emitted three false ORPHANs on bare roots.
- **charter-ghp marker failed a SECOND consecutive probe** (18:51Z):
  pin `2026-09-26 scribe beat` vs live `2026-09-28 scribe beat
  (the-scribe via local-fallback)`. The round-3 pin was extracted but
  never landed in `fleet.config.json` — beat pins die ~daily while the
  daily scribe lands, and the re-pin belongs to the keeper's publish
  queue anyway. Recorded, not edited.

## Learned

- **The residual that sounds scary often isn't.** "file deleted from
  source stays served until redeploy" assumed artifact accumulation;
  one `pages.yml` read disproved it. Read the deploy mechanism before
  estimating audit surface.
- **Two coverage directions need two different enumerations:** source
  walk catches rot (source→live); URL lists catch listing integrity
  (URL→live). On GHP the reverse direction (live→source) is provably
  empty, leaving "unlisted URLs" as the only invisible cell — a list
  completeness problem, not a deploy defect.
- **Staged-but-unpushed files are a free lookahead.** ds4cc's 404
  `sitemap.xml` at local HEAD isn't drift to fix — it's the publish
  queue previewing itself. Same class as round-6's local-ahead diffs.
- **Standing fleet state re-verified, not re-churned:** dead rows
  (plazir15, charter-ufo-fsd-kimi, lucario 404s; plazir27-kimi-pro
  preview-404; xsnapshot-app NXDOMAIN) unchanged — config `status`
  remains a snapshot, and `lucario status:live` is still wrong.

## Round-20 corrections (append-only; base `cb807bc`)

- Base `corpus/lessons/round-7.md:12`: **[r20-correction 2026-10-19: the no-orphan conclusion requires checking actual uploaded/deployed artifact or build output, not inferring from the checkout — corpus/knowledge/ghp-served-set.md (S001, S004)]**
- Base `corpus/lessons/round-7.md:20`: **[r20-correction 2026-10-19: the no-orphan conclusion requires checking actual uploaded/deployed artifact or build output, not inferring from the checkout — S001, S004]**
- Base `corpus/lessons/round-7.md:22`: **[r20-correction 2026-10-19: upload-pages-artifact excludes .git/.github and v4 excludes hidden paths by default (v5 adds include-hidden-files); check deployed artifact/build output rather than assuming full-tree coverage — S001, S002, S004]**
- Base `corpus/lessons/round-7.md:23`: **[r20-correction 2026-10-19: a no-orphan result must be checked against actual deployed artifact/build output, not inferred from the checkout — S001, S004]**
- Base `corpus/lessons/round-7.md:25`: **[r20-correction 2026-10-19: a checkout-based source walk does not establish live→source; compare live paths with the actual artifact/build output — S001, S004]**
- Base `corpus/lessons/round-7.md:40`: **[r20-correction 2026-10-19: workflow shape alone does not establish deployed contents; inspect actual artifact/build output — S001, S004]**
- Base `corpus/lessons/round-7.md:41`: **[r20-correction 2026-10-19: a workflow's actual artifact/build output, not only its pages.yml, determines live→source membership — corpus/knowledge/ghp-served-set.md (S001, S004)]**
- Base `corpus/lessons/round-7.md:44`: **[r20-correction 2026-10-19: live→source requires comparison with actual uploaded/deployed artifact or build output, not inference from the checkout — S001, S004]**
- Base `corpus/lessons/round-7.md:45`: **[r20-correction 2026-10-19: verify the live→source direction against actual artifact/build output, not the checkout — S001, S004]**

## Gate

Retrospective round-21 reconstruction, written by the round-21 lane (Lesson13). It is not the original round-7 admission: no round-7 gate was recorded at the time. No live state was re-verified.

Basis read: this lesson's sections `The gap closed` (lines 8-12), `What the audit actually found` (14-34), `Learned` (36-53), and `Round-20 corrections` (55-65); the LOG.md round-7 entry (line 10); the round-20 lesson row A2 naming this file (`corpus/lessons/round-20.md:261`); the round-20 Gate and resume Gate (`corpus/lessons/round-20.md:41-60`, `:182-196`) as the format precedent; the round-21 lesson `corpus/lessons/round-21.md` (not present when read); the S019 metadata/gate contract named in the round-21 wave spec, which is not registered in `corpus/SOURCES.md` when read. S019 is cited by name only; no S019 row was opened.

Candidates considered, with historically supported outcome:

- **Live-only GHP orphans impossible by construction** (lines 20-22). Outcome: landed without a recorded gate; superseded and rejected as a current inference by round-20 mistake A2 and QUALITY.md Platform mechanism. The workflow shape did not establish the actual served artifact; the new gate does not admit this claim.
- **Two coverage directions need different enumerations** (lines 42-46). Outcome: the method split is historically documented, not retrospectively admitted; its “provably empty” live→source premise is superseded by the round-20 artifact/build-output correction.
- **First-pass `/` classifier defect** (lines 26-28). Outcome: admitted as a recorded first-pass observation and fix; no later correction in the file.
- **103 sitemap locs: 0 orphans, 0 dead listings, 0 listed-but-404** (lines 16-19). Outcome: unverified as current state. Basis is the `/tmp/orphan-check.mjs` baseline (~20:20Z), which is outside the repository; it is a 2026-09-28 observation only.
- **Staged unpushed sitemap as pre-push preview** (lines 17-19, 47-49). Outcome: unverified observation at local HEAD; the publish-queue reading is an inference, not checked.
- **charter-ghp marker pin mismatch on a second consecutive probe** (lines 29-34). Outcome: admitted with qualification as a recorded probe result (`state/probe-latest.json`, 18:51Z). "Recorded, not edited" is a deferral to the keeper's publish queue, not a rejection.
- **Standing fleet dead rows unchanged; config status is a snapshot** (lines 50-53). Outcome: admitted only as a 2026-09-28 snapshot. No current-state claim.
- **Round label `~20:20Z`** (lines 3-4). Flagged as future-dated by `corpus/lessons/round-6-aggregator-audit.md:88-92,132` (open at round 6). The label is still present in the current file; this gate does not correct it.

Rejected: not recorded. No rejected candidate, reason, or alternative appears in the original sections. The round-20 tails supersede claims but are not labelled as rejections in any recorded gate.

Outside spot-check: not recorded. `corpus/lessons/round-20-verifier-spotcheck.md` samples round-20 decisions only (crawl-scope-per-host admit; S017 and S018 reject) and does not cover round-7. `corpus/lessons/round-20.md:58-60` recorded the round-20 outside spot-check as unavailable at its 2026-10-15 attempt (header, line 3); that state is superseded by `corpus/lessons/round-20-verifier-spotcheck.md` (commit 7e17c66, 2026-10-19). The round-6 aggregator finding (`round-6-aggregator-audit.md:88`) is a timestamp-label check, not a decision spot-check.

Contract: this block follows the round-20 Gate format (`corpus/lessons/round-20.md:41`) and the S019 metadata/gate contract. Original sections and round-20 tails are unchanged; this is an EOF addition only.
