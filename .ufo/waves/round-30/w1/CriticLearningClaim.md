# CriticLearningClaim — round 30, wave 1 (C2 as the learning claim)

Seat: KakeR30.CriticLearningClaim (critic, leaf). Axis judged: freshness. Base 0356681, declaration 4580c78.
No network, no installs, no lane mutation except this report. Sandbox: /fast/scratch/hyaku/kake-r30/w1/CriticLearningClaim/

## Verdict

1. **Uncovered frontier ground: yes, but only part of it.** Render is open Frontier ground:
   PROVINCE.md:29-30 ("Render deploy semantics remain open"), PROVINCE.md:92, corpus/README.md:105 and :267-268.
   The Frontier item is *Render deploy semantics*. C2 takes the *static-site* subset.
2. **Duplicative: no.** At 4580c78, `git grep -i 'render\.com\|onrender' -- corpus SKILL.md PROVINCE.md` returns
   nothing. No SOURCES row cites render.com. The only Render knowledge in the corpus is the Docker web service for
   app.ds4cc.com: publish-channels.md:24-28, SKILL.md:28, the round-23 HOLD at publish-channels.md:72 and
   fleet-registry.md:13-14. ghp-custom-domain.md covers GitHub Pages, which is a different platform.
3. **Knowledge entry alone: enough for "expansion: improved", but not more than that.** LEARNING.md:33 defines
   expansion as "admitted `knowledge/` entries on ground the coverage map did not hold … each citing its
   coverage-map row". Round 28 set the precedent: a knowledge-only frontier entry was admitted
   (round-28-verifier-spotcheck.md:177-182, :200). Three limits apply:
   - With no gate, the ground stays Frontier and cannot move to Core (PROVINCE.md:30).
   - The quality trend stays "unchanged" unless an existing entry is re-verified or deepened. Rounds 28 and 29 were
     both judged "quality: unchanged" (round-28-verifier-spotcheck.md:183-187, round-29-verifier-spotcheck.md:203-209).
   - The C2 counter does not measure the expansion observable (counterexample A below).

## Counterexample A: a content-free entry scores C2 4/4 (measured)

In my sandbox clone at 4580c78 I committed three files:
- an entry made of 8 blank lines plus `Sources: S049 S050 S051 S052.`;
- four 11-cell SOURCES rows (`mined`, `2026-10-22`, with the receipt URLs);
- a lesson `## Gate` holding the same Render navigation-menu string as the quote for all four ids:
  "Platform features by plan Use with coding agents FAQ Templates".

Command: `python3 -B .ufo/waves/round-30/c2_quote_truth.py --root . --revision 8548d047fce375ab9c1b23e1cfcc530416d42098`.
Result: exit 0, `C2 4/4`, controlBroken false, counterSha256 a2cd3164…975e7a (matches the lane file's sha256; blob bae263ac).
Output: /fast/scratch/hyaku/kake-r30/w1/CriticLearningClaim/hollow-c2.json. Clone: …/CriticLearningClaim/clone.

Why it passes:
- The retained text keeps the site chrome. The textRule only strips tags. The navigation runs up to the "Copy page"
  marker and takes up 41%, 47%, 69% and 27% of the S049-S052 texts. A navigation string is therefore an exact
  substring for every id.
- Check b accepts any id token after line 8.
- Nothing requires a README coverage row, a PROVINCE update or a single teaching sentence.

SCORECARD.md:724-726 already says C2 "proves sourcing, not that each entry sentence follows". This counterexample is
stronger than that: 4/4 is reachable with **zero** Render knowledge. Impacted axes: freshness and the expansion trend
(false provenance risk). This is a fixable defect. The declared target stays valid only if the closure reads the
entry body.

## Counterexample B: premature saturation of the Render Frontier item (risk, not yet landed)

- The lane's one Render property is a Docker web service. Evidence: /home/vgpnk/Projects/ds4cc-marketplace/render.yaml:2-4
  (`type: web`, `runtime: docker`; HEAD 1fbdb8ed, blob d17ab7e5) and SKILL.md:28.
- No owned property is a Render static site, so the entry is platform knowledge with no lane consumer.
- S049 itself separates the two: "Deploying a dynamic site, such as a Rails app? Create a web service instead of a
  static site." (S049.txt).
- Suppose integration rewrites PROVINCE.md:29-30 or README.md:267 to show "Render deploy semantics" as held. That
  would overstate the step, the same pattern as the stale round-25 sentence that PROVINCE.md:86-88 had to correct.
- The round-30 wave-1 spec plans the SKILL table, screened rejects (ScreenRenderCandidates) and a local-use scout.
  It plans no README coverage row wording, PROVINCE wording or quality move (searched w1-spec.json for
  "publish-channels", "superseded" and "re-verif": 0 hits).

## Smallest safe corrections (for the L1)

1. **README and PROVINCE wording.** Add a README coverage row, "Render static sites (r30)", citing S049-S052. Change
   PROVINCE.md:29-30 and README.md:267 to "Render static-site semantics held (first entry, no gate); Render web-service
   deploys (the owned app.ds4cc.com) remain open". Do not delete "Render" from the open list.
2. **Closure reads the entry body.** Record in the declaration notes (before measurement) that 4/4 is reachable with an
   empty entry (counterexample A). If the counter changes, it should match quotes only after the page's "Copy page"
   marker and should require the README row. A counter change after declaration is a re-declaration, so a note is the
   safe move this round.
3. **Make it stronger (SKILL table).** Add a "Render static-site triage — round 30" table in the round-28/29 shape
   (SKILL.md:680-719): symptom → check → remedy → cited ids. Rows grounded in located text:
   - S050: SPA deep link 404 → add a `/* → /index.html` rewrite. Rules are skipped when a resource exists at the
     path: "Render does not apply redirect or rewrite rules to a path if a resource exists at that path."
   - S051: `Cache-Control` and custom response headers.
   - S052: the custom domain keeps its onrender.com subdomain until that is disabled; AAAA records are removed; the
     www/root pair is added and redirected.
   - S049: the dynamic-site cut-over to a web service.
   Each row must say "platform knowledge, no owned static site".
4. **Cheap quality move (offline, no network).** S052 states "You can apply your own custom domains to Render web
   services and static sites" and "Services with a custom domain also keep their onrender.com subdomain". This
   applies directly to the owned web service.
   - Append a dated, sourced deepening tail to publish-channels.md "Render — app.ds4cc.com" (lines 24-28). The entry
     lists APP_ORIGIN and ALLOWED_ORIGINS. The present local render.yaml:11-12 also sets
     `ALLOWED_HOSTS=ds4cc-marketplace-app.onrender.com`, which the entry omits.
   - Cite render.yaml by blob d17ab7e5 at checkout 1fbdb8ed.
   - This is append-only and touches no owned site. It gives the quality trend a candidate "deepened" entry
     (LEARNING.md:34). Whether app.ds4cc.com is reachable on both hosts is [INFERENCE] and must stay unverified
     (no live requests).
5. **Keep the screened rejects.** Keep ScreenRenderCandidates' rejected rows. Without them the round regresses on
   round-28 routed defect 4, which round 29 closed (round-29-verifier-spotcheck.md:210-212).

## Commands run (all exit 0)

- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin …/CriticLearningClaim/clone`, then `git checkout 4580c78`,
  a sandbox commit 8548d04, and the C2 counter as above (exit 0, 4/4).
- `git grep -n -i 'render\.com\|onrender' 4580c78 -- corpus SKILL.md PROVINCE.md` → no output.
- `git -C ~/Projects/ds4cc-marketplace rev-parse HEAD HEAD:render.yaml` → 1fbdb8ed…, d17ab7e5….
- `sha256sum .ufo/waves/round-30/c2_quote_truth.py` → a2cd3164…975e7a.
- Python one-liners: the "Copy page" offset in each S0NN.txt, term counts and context windows (quotes above copied
  from that output).

## Not verified

- The C2 counter was not run on any real draft entry (none exists in the lane yet).
- The completeness of the S051 retained text (69% navigation, about 1.2k article characters) was not checked against
  the gzip body; that belongs to ReviewRetainedCompleteness.
- No live Render or owned-site state was checked.
- Installs: none.
