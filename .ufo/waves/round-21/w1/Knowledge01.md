# Knowledge01 — crawl-scope-per-host.md provenance audit (round 21, w1)

## Behavior
- Target: `corpus/knowledge/crawl-scope-per-host.md` (52 lines, 3160 bytes, committed at HEAD `02b6dd0`, clean working tree).
- The provenance trio already opens the entry (lines 1–3, blank line 4). Per contract the target was left **unchanged**; zero bytes edited. Field truth was audited instead.
- Existing prefix: lines 1–4 = **357 bytes** (`head -n 4 | wc -c`). No prefix was added, so no prefix-length change occurred.
- No recheck was run. No network read was made. No credential or auth file was read. Nothing installed or upgraded (no pacman, uv, npm, or binary installs).

## Gates
| Field | Verdict | Evidence |
|---|---|---|
| `source:` | PASS on IDs; minor anchor gap | `corpus/SOURCES.md` rows S011 (RFC 9309, tier A, `used-by` includes this entry), S012 (sitemaps.org, A), S013 (Google Search Central, A) all exist. S013 "last updated 2026-07-08 UTC" matches the verified-at date. |
| `verified-at:` | PARTIAL | Dates match SOURCES `opened` 2026-10-19 and the RFC September 2022 publication. The date is the original evidence date, not today (2026-10-20). **Missing** the required `historical-not-live-reverified` statement. Body wording "quotes reopened 2026-10-19" reads like a live reopen. |
| `recheck:` | FAIL vs contract | The only command is `curl -fsSL https://www.rfc-editor.org/rfc/rfc9309.txt \| grep -cF …`. That is a remote network read, not a safe local reading command. No local RFC copy exists (`find / -xdev -iname 'rfc9309*'` returned nothing). It covers S011 only. S012 (365d) and S013 (90d) have no recheck argv, though `corpus/QUALITY.md` requires a recheck argv for platform-mechanism claims. No restore-or-retire clause (not triggered, since no local source vanished). |

## Field-truth details
1. **§2.3.1.3 citation gap.** The trio and body cite §2.3.1.3 ("MAY access any resources"). The SOURCES S011 anchor lists only "Section 2.3 Access Method and 2.3.1.4 Unreachable Status". The registry does not carry §2.3.1.3.
2. **URL form.** Trio uses `https://www.rfc-editor.org/rfc/rfc9309`; SOURCES uses `.../rfc9309.html`. Same document, different form.
3. **S019 unresolved.** `grep -rn S019` finds it only in `.ufo/waves/round-21/wave1-spec.json`. SOURCES.md ends at S018 (18 rows). The S019 metadata authority is not yet registered; L1 owns CORPUS.md registration this round. The entry does not cite S019, and the trio needs no change for that once L1 registers it.
4. **Body spot checks.**
   - Lane population: `grep -oE 'veigapunk\.github\.io/[A-Za-z0-9-]+/' SKILL.md corpus/knowledge/fleet-registry.md | sort -u` yields lucario, charter-ufo-fsd, plazir-15-site, so **3** unique. Matches the stated count.
   - The RFC "returned 1 occurrence" claim is undated and not reproducible offline; treat as historical.
   - `cb807bc` resolves as a commit.
   - `freshness-sweep.md:58` matches the ds4cc sitemap/robots row. `publish-queue.md:88-93` covers the ds4cc canonical 404 bullet (92–93). `sitemap-orphan-audit.md:40-47` covers the sitemap procedure with live-sitemap sources (43–47); partial fit, acceptable.
5. **Named debt preserved.** The status of `veigapunk.github.io/robots.txt` is recorded as unknown with owner operator/webzites. Absence flag kept.

## Recommendations (not applied; target is frozen by contract)
- Next round, amend the trio: add `historical-not-live-reverified` to `verified-at:`; replace the curl recheck with a local-only reading command or record a restore-or-retire requirement; add recheck argv coverage for S012 and S013 or name them as uncovered.
- L1: register S019 in CORPUS.md; add §2.3.1.3 to the S011 anchor in SOURCES.md.

## Scope and limits
- Out-of-scope items: none edited; SCORECARD, LOG, QUALITY, SOURCES, README, SKILL untouched.
- Limitations: online RFC, sitemaps.org, and Google sources not re-read (no additional domain network reads permitted). §2.3.1.3 and the "1 occurrence" quote are unverified in this round.
- Commands run were read-only: `read`, `grep`, `wc`, `head`, `find` on the local tree, `git log`/`git status`/`git cat-file` on the target path.
