source: S036, S037, S038, S039 (corpus/SOURCES.md) — https://web.dev/articles/vitals; https://web.dev/articles/defining-core-web-vitals-thresholds; https://developer.chrome.com/docs/crux/methodology; https://developer.chrome.com/docs/crux/api
verified-at: 2026-10-22 (pages last updated: S036 2024-10-31, S037 2025-05-07, S038 2024-06-20, S039 2026-10-13; all four opened with one public GET, HTTP 200, 2026-10-22T09:29Z)
recheck: 90d, or when a Core Web Vital changes stage — curl -fsSL https://web.dev/articles/vitals | grep -c '>INP</a>: Stable' (1 on 2026-10-22)

# Field performance: Core Web Vitals thresholds and CrUX eligibility

**Claim (falsifiable).** S036 says tools "should consider a page passing" when
the 75th percentile of page loads meets the good threshold for each of LCP, INP
and CLS; kake's own rule is stricter and judges that pass only on field data.
The thresholds are LCP ≤ 2.5 s (poor > 4 s),
INP ≤ 200 ms (poor > 500 ms) and CLS ≤ 0.1 (poor > 0.25). The public field
source, the Chrome UX Report (CrUX), only holds a page or origin that is
publicly discoverable and sufficiently popular among eligible Chrome users, so
a low-traffic or `noindex` property, or one whose visitors mostly use
browsers that send no data, can have no field data at all. "No field data" is
a finding to report, never a pass, and lab numbers do not replace it.

## What the sources say

### The metric set and its thresholds (S036, S037)

- The current Core Web Vitals are LCP (loading), INP (interactivity) and CLS
  (visual stability), and all three are at the stable stage of the metric
  lifecycle (S036, section *Core Web Vitals lifecycle*: "LCP : Stable CLS :
  Stable INP : Stable").
- Good thresholds: LCP within 2.5 seconds, INP 200 milliseconds or less, CLS
  0.1 or less (S036, *Core Web Vitals*). The threshold table in S037 gives the
  poor bounds in the same units: LCP > 4000 ms, INP > 500 ms, CLS > 0.25, each
  at percentile 75 (S037, table under *Refresher: Core Web Vitals metrics and
  thresholds*). Values between
  the good and poor bounds are "needs improvement".
- The page or site classification uses the 75th percentile of all page views;
  if at least 75 percent of page views meet the good threshold, the site is
  classified as good (S037, *Refresher: Core Web Vitals metrics and
  thresholds*; device treatment under *Whether to have the same or different
  criteria per device*).
- The thresholds are the same on mobile and desktop; only the measurement is
  segmented by device (S036 recommends the 75th percentile "segmented across
  mobile and desktop devices"; S037 states the thresholds "are not segregated
  by device"). S037 adds that most thresholds were set on mobile achievability
  and "more likely represent mobile thresholds".
- Thresholds were chosen for achievability with CrUX data. For LCP and CLS the
  poor bound targets 10–30% of origins falling into "poor" (S037, data as of
  April 2020). For INP a 300 ms poor bound was considered and rejected because
  INP has an inverse correlation with popularity, and 500 ms was chosen (S037,
  data as of May 2022). The numbers are policy choices that can change, not
  physical limits.

### Lifecycle and change cadence (S036)

- INP began as an experimental metric meant to cover runtime responsiveness
  more fully than First Input Delay (FID); it was promoted to pending in 2023
  "with the intent to eventually retire FID" (S036, *Pending*). kake therefore
  does not report FID as a current Core Web Vital.
- Stable metrics change at most once per year, and changes are announced in the
  metric's documentation and changelog; a stable metric can still be retired
  and replaced (S036, *Stable*). This entry still rechecks on its own 90-day
  cadence; the once-a-year bound is on metric changes, not on this entry.

### Field versus lab (S036)

- CrUX collects anonymized real-user data for each Core Web Vital and feeds
  PageSpeed Insights and the Search Console Core Web Vitals report (S036,
  *Field tools to measure Core Web Vitals*).
- Lighthouse loads pages without a user and cannot measure INP; Total
  Blocking Time (TBT) is its lab proxy. S036's lab table marks Chrome DevTools
  as able to measure INP (S036, *Lab tools to measure Core Web Vitals*). Lab
  measurement "is not a substitute for field measurement" (S036). A lab score
  is therefore development evidence, not a Core Web Vitals pass.

### CrUX eligibility (S038)

- Only some users contribute: they must enable usage statistic reporting,
  sync their browser history, have no Sync passphrase, and use desktop Chrome
  (Windows, macOS, ChromeOS, Linux) or Android Chrome, including Custom Tabs
  and WebAPKs. Chrome on iOS, Android apps using WebView and other Chromium
  browsers such as Microsoft Edge send no data, and the proportion of eligible
  users is not published (S038, *User*).
- A page must be publicly discoverable, judged with search-engine indexability
  criteria. A page fails discoverability when it is served with a final HTTP
  status other than 200 after redirects, an `X-Robots-Tag: noindex` header or
  equivalent, or a `<meta name="robots" content="noindex">` tag or equivalent
  (S038, *Publicly discoverable*).
- A page or origin must also be sufficiently popular; the minimum visitor
  count is not disclosed and is the same for pages and origins (S038,
  *Sufficiently popular*).
- An origin is included when its root page is discoverable and the origin is
  popular enough; S038 then says experiences on all its pages count at the
  origin level, regardless of individual page discoverability (*Origin*).
  The same page also says experiences that meet the User and Origin criteria
  but not the Page criteria are not in origin-level data (*Eligibility*). The
  two sentences pull in different directions; kake quotes both and does not
  resolve them. Origins in the dataset are lowercase.
- Query strings and fragments are stripped from page URLs, so URL variants
  aggregate into one page (S038, *Page*). Single-page-app route changes are
  attributed to the initial page view, so a route may have no page-level
  record of its own (S038).
- A page or origin with more than 20% of its traffic in ineligible dimension
  combinations is excluded entirely (S038).
- At the time of the page, pages cannot be submitted manually; inclusion
  changes automatically as eligibility changes (S038, *Eligibility*).

### The CrUX API (S039)

- One endpoint, `POST https://chromeuxreport.googleapis.com/v1/records:queryRecord`,
  takes either an `origin` or a `url` key, an optional `formFactor` (for
  example `PHONE`) and an optional `metrics` list (S039, *Schema*). A `url`
  query returns data for that URL only (S039, *URLs*).
- The data is a 28-day rolling average, updated daily around 04:00 UTC on a
  best-effort basis; after that update, repeated calls on the same day return
  the same result, so calls on either side of the update can differ (S039,
  *The rolling average*, *Daily updates*). The API is about two days behind
  today's date, and its collection period dates use Pacific Standard Time
  without daylight saving (S039, collection period note). A result therefore
  names its window end date, not the query date.
- Use requires a Google Cloud API key; the quota is 150 queries per minute per
  project, free, and cannot be raised by payment (S039, *CrUX API Key*, *Rate
  limits*).
- URL normalization is limited to basic automated changes; redirects are not
  followed (S039, *UrlNormalization*). Not found on the page this round: a
  documented response or error body for a key with no data, and a documented
  automatic fallback from page to origin data. kake assumes neither.

## How kake uses this

1. Before calling a property fast or slow, ask which field source exists:
   page-level CrUX, origin-level CrUX, or none. Record which one answered.
2. When CrUX has no record, check the S038 exclusion conditions first (final
   status other than 200, `noindex` header or meta tag or equivalent, root page
   not discoverable). S038 lists these as conditions that exclude a page, not
   as a complete test, and a raw 200 is not proof of a served page
   (`SKILL.md`). If none applies, too few eligible visitors is the likely but
   unconfirmed cause: either low traffic, or an audience on Chrome for iOS,
   WebView or other Chromium browsers, which send no data. Report "no field
   data", not a pass or a failure. For a single-page app, a route without its
   own record may be counted under the initial page view.
3. Judge each metric at p75 against the S037 table, per form factor, and name
   the 28-day window end date (S039) with the result.
4. Do not convert a Lighthouse or other lab score into a Core Web Vitals
   verdict (S036). Lab results may guide a fix; only field data closes it.
5. CrUX API calls need a Google Cloud API key (S039). kake holds no key; by
   lane policy it makes no API call without an operator-provisioned one.

## Limits of this entry

- Sourced from four documentation pages opened 2026-10-22. No CrUX or
  PageSpeed API call was made and no lane property was measured; nothing here
  says whether any kake property passes.
- Browser-support and per-engine metric availability are outside this entry
  (see the rejected S018 row in `corpus/SOURCES.md`).
- Boundary: kake holds the thresholds and eligibility rules as publisher-side
  knowledge. Running lab tools such as Lighthouse or DevTools is browser work
  and routes to tabi. A CrUX API query needs a Google Cloud key, so key custody
  routes to the operator and kagi. Whether web.dev pages rank as primary
  sources is chousa's method question; here they are scoped tier A for
  Google's own published thresholds only.
- Field performance stays in kake's Frontier (`PROVINCE.md`): this entry is
  knowledge without a gate, so it does not move the area to Core.
