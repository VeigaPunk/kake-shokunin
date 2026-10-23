ATTACK SUPPORTED — v3 was redesigned after live-seat scores; “before the build was scored” is not “before data.”
Axes: operability (measurement/admission provenance); freshness not exercised. No round verdict or admission issued.
Scope: read/grep/glob inspection only; no shell, code, counter, test, judge, network, or other runtime invoked. No command exit codes observed by this seat; no processes started; no installs/updates. Only this report written.
Paths: R=/home/vgpnk/Projects/shokunin/kake-shokunin; W=$R/.ufo/waves/round-42; S=/fast/scratch/hyaku/kake-r42w1/MutRegexPct; T=/fast/scratch/hyaku/kake-r42/shared/tip41.py. References below are relative to R unless absolute.

Per-statement assessment
- HOLDS, documentary: v2/v3 and declaration preceded build-counter scoring. SCORECARD.md:2995,3019,3057,3084-3093 records that ordering. Commit chronology was not independently audited here.
- WRONG: that ordering alone establishes “fix before data.” The canonical round prompt /home/vgpnk/Projects/shokunin/.ufo/prompts/kake-round-42.md:357-360 says a rule changed after ANY seat has scored is not the claim’s rule. SCORECARD.md:2972-2975,2988-2991 substitutes a later boundary, build scoring. Local pre-freeze labels/QUALITY cannot relax the prompt.
- OVERSTATED, v1→v2: restoring an exact ≤2.0 comparison corrects an implementation defect; adding run D and changing scheme/password/T4 generation also changes the evaluated population (SCORECARD.md:2995-3011). Original v1 L1 measurements already existed (:2951-2958). A live-control-score-versus-v2 timestamp is not established by this review; the decisive post-seat-data case is v3 below.
- WRONG, v2→v3 “redesigned before data”: SCORECARD.md:3021-3032 expressly says meeting live-seat controls with witnesses caused redesign; :3034-3045 adds E, alters timing distributions/isolation and removes seeded scoring. These are useful engineering repairs, but not pre-seat-data rules. :3071-3072 also records nine witnessed/manipulating v1 successes.
- HOLDS: the predicate sentence remains identical. OVERSTATED: therefore the counter/claim rule is unchanged. Its quantified set grows 8→9→10 runs and timing populations change (SCORECARD.md:3003,3047-3054); §6.9 freezes counter, kill rule AND predicate, not merely the prose label.
- HOLDS: the behavior-based exclusion was predeclared. SCORECARD.md:2959-2971 requires a differing `_parse_url`/CLI witness or demonstrated measurement manipulation and excludes equivalent implementations. Treating every regex edit as a control would contradict that definition.
- OVERSTATED: the exact “frozen equivalence differential” was fixed before scores. The initial prescription names A–C at seeds 42101–42103 (:2968-2971); the later 31,415-value test uses v3 A–E plus targeted values (:3064-3067; equivalence/equiv_diff.py:10-21). Its exact bytes/hash are not pinned in the initial prescription. Witness criterion: predeclared; final executable/population: not the same predeclared screen. Static count also gives 728 appended strings (16×5×3×3+8), not the stated 240.
- HOLDS, bounded: all three v3 receipts are met, and equivalence/meeting-v3.json:1-16 records zero `_parse_url` differences on 31,415 values. OVERSTATED: this proves equality on EVERY value. The script tests finite values and only `_parse_url` (equivalence/equiv_diff.py:23-30), not full CLI equivalence or measurement integrity.
- HOLDS under the predeclared witness criterion: no supplied behavioral witness makes portpct, empty_host or port_letters a control. Their original seats already classified them this way (w1/MutRegexPct.md:19,29-39; w1/MutRegexStructure.md:23-24,31-32,50). This is not a demonstrated post-score reclassification.
- Source-level support: portpct.py:82 widens ports to `%`, mutant_port_letters.py:82 to `a`, but both retain parts.port/ValueError rejection at :102-104; mutant_empty_host.py:81 allows an empty host but retains host rejection at :99-101. These explain masked regex changes; no new witness was tested here. Do not claim these three alone activate the kill rule.

Strongest closure attack / retained counterexample
- Use the genuine witnessed v1 control, not the three masked v3 survivors: `https://example.test/%\u06610` (U+0661 followed by ASCII 0). S/witnesses.json:292-338 records tip41 None / CLI exit 1 loc_not_absolute versus unicodedigit’s parsed URL / CLI exit 0 clean.
- S/unicodedigit.json:2-15,157-163 records v1 met=true, equality 8/8, ratios [1.217,1.433,1.104,1.078,1.898]. W/verification/w1v3/MutRegexPct__unicodedigit.json:2-15,49-55 records the SAME tool hash failing only newly added E (9/10, met=false). This is direct local evidence that changed scored rules neutralized an already scored control.
- Thus a stronger v3 and honest behavior-based exclusions do not close §6.9’s provenance objection. This is a measurement-contract defect, not evidence that the scanner itself is worse; no harm/freshness verdict follows from it.

Smallest safe correction / exploratory disposition
- Preserve original scores and all counter versions; append an explicit post-seat-data-redesign disclosure. Do not repair provenance by another counter change or by declaring the three equivalent-looking rewrites controls.
- Recommendation: C1 should be presented as exploratory engineering improvement, not a cleanly frozen measured admission. The declared pre-build kill branch offered that route (SCORECARD.md:2972-2974); its broader redesign permission cannot override §6.9. Because the build is now scored, disclose the timing rather than fabricate an earlier exploratory declaration.
- Exploratory is not automatic success: AXES.md:43-55 requires a named outside non-author reviewer with reasons; a lane-dispatched seat is insufficient. Without that, retain unprovable/honest-stop treatment. Canonical closure owns the disposition; this leaf does not judge it.

Recorded commands / exit codes — NOT rerun by this seat
- `timeout 900 prlimit --as=8000000000 -- env TMPDIR=$S python3 -B $W/c42_count.py --root $R --tool-file $S/unicodedigit.py --label MutRegexPct-unicodedigit --seed 42071 --out $S/unicodedigit.json` → 0, per w1/MutRegexPct.md:8,21.
- `timeout 30 prlimit --as=8000000000 -- python3 -B $T --manifest $S/witnesses/unicodedigit/manifest.json` → 1; same argv with tool `$S/mutants/unicodedigit.py` → 0 (S/witnesses.json:305-335).
- V3 exits recorded in score-b.log:39,42,51,54: portpct 0, unicodedigit 1, empty_host 0, port_letters 0. Driver argv are score_v3.sh:18-20; no additional scoring performed here.

Recorded SHA256 pins — read from scorecard/receipts, not freshly recomputed
- W/c42_count.py: 7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6
- W/c42_count_v2.py: 01d3fb8de064cd86f5ec05be4641f154bb23a7961ff36e542a3777809208808e
- W/c42_count_v3.py: ce2d5a0ca2c3768ce2b1d7b9a57592817d7f16616ee7fb25989e580a70160acc
- T (tip41.py): 50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d
- W/controls/w1/MutRegexPct/unicodedigit.py: 7498d17f310c4fa790107db7a8252097b921d815e0cf74227f6d9461de8e2a4f
- W/controls/w1/MutRegexPct/portpct.py: d1e06ba366c6253229d30948a809e14d58f1fc2306b26ea61f382802d1bfa504
- W/controls/w1/MutRegexStructure/mutant_empty_host.py: 4686d24626a68e0eded04a2621c4d3c2af8c0d6e6cbbbc3100fd70ad08200b9e
- W/controls/w1/MutRegexStructure/mutant_port_letters.py: 0995bba947ca9b858b76b9619f98016609276d1ec78967b9800e42f1a99e7c9d
- scripts/sitemap_audit.py at 020bc457: 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021
