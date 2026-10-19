# Lesson — round 7 (2026-09-28)

Cites: LOG.md round-7 entry; `corpus/knowledge/sitemap-orphan-audit.md`;
evidence = `/tmp/orphan-check.mjs` baseline (~20:20Z, 103 locs) +
`pages.yml` deploy-graph reads + `state/probe-latest.json` (18:51Z).
Commit `round-7`. Zero publishes, zero metered ops.

## The gap closed

README's residual "live-only orphan paths (needs sitemap crawl, not
source walk)" — closed two ways at once: a sitemap sweep baseline AND a
proof that the scary version of the gap can't exist on GHP. **[r20-correction 2026-10-19: the no-orphan conclusion requires checking actual uploaded/deployed artifact or build output, not inferring from the checkout — corpus/knowledge/ghp-served-set.md (S001, S004)]**

## What the audit actually found

- **103 sitemap-listed URLs across the three GHP rows: 0 orphans, 0
  dead listings, 0 listed-but-404.** ds4cc-com 93 locs from the *staged*
  (unpushed) `sitemap.xml` — doubles as a pre-push drift preview: every
  listed path already serves 200.
- **GHP live-only orphans are impossible by construction.** Both **[r20-correction 2026-10-19: the no-orphan conclusion requires checking actual uploaded/deployed artifact or build output, not inferring from the checkout — S001, S004]**
  `pages.yml` workflows do `upload-pages-artifact path: <repo root>` —
  every deploy ships the entire checked-out tree as a fresh artifact. **[r20-correction 2026-10-19: upload-pages-artifact excludes .git/.github and v4 excludes hidden paths by default (v5 adds include-hidden-files); check deployed artifact/build output rather than assuming full-tree coverage — S001, S002, S004]**
  A deleted file can't linger live; the served set ≡ last-pushed **[r20-correction 2026-10-19: a no-orphan result must be checked against actual deployed artifact/build output, not inferred from the checkout — S001, S004]**
  `origin/main` tree. The round-6 source walk against `origin/main`
  already covered this direction modulo push→deploy lag. **[r20-correction 2026-10-19: a checkout-based source walk does not establish live→source; compare live paths with the actual artifact/build output — S001, S004]**
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
  one `pages.yml` read disproved it. Read the deploy mechanism before **[r20-correction 2026-10-19: workflow shape alone does not establish deployed contents; inspect actual artifact/build output — S001, S004]**
  estimating audit surface. **[r20-correction 2026-10-19: a workflow's actual artifact/build output, not only its pages.yml, determines live→source membership — corpus/knowledge/ghp-served-set.md (S001, S004)]**
- **Two coverage directions need two different enumerations:** source
  walk catches rot (source→live); URL lists catch listing integrity
  (URL→live). On GHP the reverse direction (live→source) is provably **[r20-correction 2026-10-19: live→source requires comparison with actual uploaded/deployed artifact or build output, not inference from the checkout — S001, S004]**
  empty, leaving "unlisted URLs" as the only invisible cell — a list **[r20-correction 2026-10-19: verify the live→source direction against actual artifact/build output, not the checkout — S001, S004]**
  completeness problem, not a deploy defect.
- **Staged-but-unpushed files are a free lookahead.** ds4cc's 404
  `sitemap.xml` at local HEAD isn't drift to fix — it's the publish
  queue previewing itself. Same class as round-6's local-ahead diffs.
- **Standing fleet state re-verified, not re-churned:** dead rows
  (plazir15, charter-ufo-fsd-kimi, lucario 404s; plazir27-kimi-pro
  preview-404; xsnapshot-app NXDOMAIN) unchanged — config `status`
  remains a snapshot, and `lucario status:live` is still wrong.
