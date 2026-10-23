# Round 39 — sitemap file audit (C1 capability move)

author: kake L1, round 39 attempt 2 (KakeR39A2)

Claim and frozen rule: `SCORECARD.md` "Round 39 — C1 declared". Contract:
`.ufo/waves/round-39/c1-contract.md`. Attempt 1 landed nothing; its leftovers were moved out of the
lane unread (`/fast/scratch/hyaku/kake-r39a2/attempt1-leftovers/`).

## Gate

Sources opened this round by the L1 (retained under `.ufo/waves/round-39/sources/`, sums in
`SHA256SUMS` there).

| Row | URL | Accessed | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S102 | https://www.sitemaps.org/protocol.html | 2026-10-23T05:28:42Z, HTTP 200 | "each Sitemap file that you provide must have no more than 50,000 URLs and must be no larger than 50MB (52,428,800 bytes)" (`sitemaps-protocol.txt:176-177`) | admit, A, spec, mined; supersedes S012 (wider scope) |
| S103 | https://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd; …/siteindex.xsd | 2026-10-23T05:29:28Z, HTTP 200 | "The value for this element is a number between 0.0 and 1.0 where 0.0 identifies the lowest priority page(s)." (`sitemap.xsd`, tPriority documentation) | admit, A, spec, mined |
| S104 | https://www.w3.org/TR/NOTE-datetime | 2026-10-23T05:29:28Z, HTTP 200 | "YYYY-MM-DDThh:mm:ss.sTZD (eg 1997-07-16T19:20:30.45+01:00)" (`w3c-datetime.txt`, Formats) | admit, A, spec, mined |

Readings where the sources disagree (contract "lane reading" sentences): `loc` length — S102
"This value must be less than 2,048 characters" versus S103 `<xsd:maxLength value="2048"/>`; the
contract follows S102. `lastmod` — S102 and S103's documentation name the W3C Datetime format,
S103's type is `xsd:date` ∪ `xsd:dateTime`, which allows no time zone; the contract requires a
complete date and a TZD with any time (S104 levels 3–6).

Row changes: S012 `status` mined → mined (unchanged; S102 supersedes its scope, recorded in S102's
`teaches`). No other row touched.

## Attempt 3 (KakeR39A3) — sources re-opened, rows added

author: kake L1, round 39 attempt 3 (KakeR39A3)

S102–S104 were re-opened by the L1 at 2026-10-23T06:47:35–36Z: all four URLs HTTP 200, sha256 equal to
the retained bytes in `.ufo/waves/round-39/sources/SHA256SUMS`, and each Gate quote above found
verbatim (grep count 1–2). Wave-1 scouts opened five candidates; the L1 re-opened each at 06:56:39–41Z
before writing its row (retained under `.ufo/waves/round-39/sources/`; quotes checked in the fetched
text with markup stripped):

| Row | URL | Accessed | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S105 | https://www.w3.org/TR/xml/ | 06:56:39Z, HTTP 200 | "S (white space) consists of one or more space (#x20) characters, carriage returns, line feeds, or tabs." (§2.3) | admit, A, spec, mined |
| S106 | https://www.w3.org/TR/xml-names/ | 06:56:39Z, HTTP 200 | "The comparison is case-sensitive, and no %-escaping is done or undone." (§2.3) | admit, A, spec, mined |
| S107 | https://www.w3.org/TR/xmlschema11-2/ | 06:56:39Z, HTTP 200 | "timezoneFrag, if present, specifies an offset between UTC and local time." (§3.3.7.2) | admit, A, spec, mined |
| S108 | https://www.sitemaps.org/faq.html | 06:56:39Z, HTTP 200 | "Sitemaps should be no larger than 50MB (52,428,800 bytes) and can contain a maximum of 50,000 URLs." | admit, A, docs, mined |
| S109 | https://yandex.com/support/webmaster/en/controlling-robot/sitemap | 06:56:41Z, HTTP 200 | "The total character limit is 2048. 1024 Characters are intended for the site's domain name" | admit, A, docs, mined (recheck 90d: page bytes vary per fetch) |

What they teach the contract (readings, not changes; the contract is frozen): sentence 21's strip set
is exactly XML's S (S105); sentence 9 is a lane safety reading, since a DOCTYPE can be well-formed
(S105 §2.8); sentence 10's "whatever prefix" follows from expanded-name identity, and the namespace
URI compare is case-sensitive (S106); sentences 28–30 depart from `xsd:date`/`dateTime` (timezone
optional, `24:00:00`, ±14:00 offsets; S107), which S103's `tLastmod` names; one engine (S109) reads
`loc` length and scope differently from sentences 23 and 25–26, so the audit is a protocol check,
not an engine-acceptance check. Row changes: none to existing rows; S105–S109 added.

## Mistakes

1. **Class: a thin sealed key passed as a discriminating counter.** Evidence: of 54 single-sentence
   mutants of the reference that wave-1 seats wrote, 15 score 24 of 24, and a regex reader with no XML
   parser (`w1a3-CtlRegexTweak`, attempt 2's dead-seat tool plus a 39-line key-blind tweak) scores 24
   (`.ufo/waves/round-39/verification/a3/w1a3-*.json`; SCORECARD "kill rule (1) fired" and "Wave-1
   additions"). The declaration's key-design evidence was 34 L1-written ablations (6–23) and four
   cheap controls; it never ran an independent mutant family or a tweaked shortcut before freezing.
   Captured-by: §6 item 9 ("a target a do-nothing control or shortcut cannot reach") — the rule
   existed; the pre-declaration evidence did not exercise it. Fix: QUALITY (o) (below) requires a
   pre-declaration key-power run by non-author mutant and shortcut seats. Shown able to fail: the
   content check `criteria/control_consequence_check.py` v2.1 on the round's receipts exits 1 under
   both readings (`verification/a3-jcheck/v21-{A,B}.txt`).
2. **Class: control-class sentence covered a tool scored before the declaration.** Evidence:
   `915e9e87:SCORECARD.md` "Drafting defect" (the private reference, sha256 `663e051e…`, scored 24 and
   fell inside "every tool scored … other than the build bytes"). Captured-by: none. Fix: QUALITY (o).
   Overtaken this round by mistake 1: kill rule (1) fires under both readings.
3. **Class: role misroute — control tools given to critic seats.** Evidence: in attempt 3's wave 1,
   11 control-building items went to critics (`w1a3-spec.json`); the critic role forbids editing and
   running code, so seven returned source or diffs in their reports for the L1 to materialize and
   three were refused by the provider (`w1a3-dispatch-log.txt`). Attempt 2's wave 1 had the same shape
   (12 items). Captured-by: prompt §6 item 2 Routing ("give an item to an executor only when it writes
   or runs code") — not applied. Fix: `criteria/route_check.py` (exit 1 on a critic item with a code
   deliverable). Shown able to fail: `w1-spec.json` exit 1 (12), `w1a3-spec.json` exit 1 (11),
   `w2a3-spec.json` exit 0 (`verification/a3-jcheck/route_check.txt`).

## Wave-2 corrections to the Gate and rows

Fresh scouts re-opened S105–S109 (`.ufo/waves/round-39/w2a3/Reopen*.md`); all five fetched bytes or
visible text match. Corrections (rows are append-only; the corrected reading is recorded here):
- **S106 `teaches`:** "'ignored' in sentence 14 comes from S102" is wrong. S102's "Extending the
  Sitemaps protocol" only says a sitemap may use another namespace; neither S102 nor S106 says
  "ignored". Sentence 14's "ignored" is a lane reading. "(sentences 10–11)" is overstated: S106 grounds
  how namespace membership is decided, not what those sentences require.
- **S107 `teaches`:** `24:00:00` and required seconds belong to `xsd:dateTime`, not `xsd:date`.
- **S109 `anchor` and Gate quote:** the page's apostrophe is U+2019 ("site’s"); the row and Gate typed
  U+0027.
- **S105, S108:** hold as written.
Row changes this round: S105–S109 added; no `status`, `recheck` or `used-by` change to an existing row.

## Gate — rejects (attempt 3)

- **Rejected: the sealed 24-case counter as C1's admission instrument.** Reason: 16 controls meet
  its predicate before any build (15 single-sentence reference mutants, each judged a valid control by a
  wave-2 reviewer, and the regex reader `w1a3-CtlRegexTweak`). Consequence applied as frozen: kill rule
  (1), C1 exploratory (`SCORECARD.md` "Round 39 — kill rule (1) fired").
- **Rejected for adoption: the draft criterion-(o) inventory checker**
  (`.ufo/waves/round-39/criteria/draft-o/check_control_inventory.py`). Reason: `MutCriterionO` found 5 false
  accepts in 15 adversarial samples (`.ufo/waves/round-39/w2a3/MutCriterionO.md`). QUALITY (o) cites
  it as a draft only; its enforced half is the content check.
- **Rejected as wrong: S106's `teaches` clause "'ignored' in sentence 14 comes from S102".** Reason:
  neither S102 nor S106 says "ignored" (`w2a3/ReopenS106.md`); recorded under Wave-2 corrections.
- **Not landed: `RerunCcCheckFinal`'s fixture patch for (j) survivor M06.** Reason: it arrived after the
  build was judged; changing the (j) check now would change a gate after data. Carried.
