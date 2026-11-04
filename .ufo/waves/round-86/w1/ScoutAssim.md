# ScoutAssim — CrUX Vis re-grounding

Axes: source fidelity, additive knowledge, collision safety. Author-side scout evidence only; no independent closure or production integration.

## Fresh GET evidence

GET https://developer.chrome.com/docs/crux/vis returned HTTP 200, curl exit 0, effective URL unchanged, 114607 raw bytes. Response Date: `Wed, 04 Nov 2026 15:36:49 GMT`; receipt recorded `2026-11-04T15:36:59.079177+00:00`. Raw HTML SHA-256: `664df84e30fbbcf73dd513b61210a6053521ebce86836a61a0dda6047e41a518`. Page still says `Last updated 2025-05-06 UTC` (stripped text line 227), matching staged S303.

Retained under `.ufo/waves/round-86/w1/ScoutAssim/`: `crux-vis.html` (raw body), `crux-vis.headers.txt`, `crux-vis.txt` (HTMLParser-stripped/whitespace-normalized text), `receipt.json`, `quote-checks.json`.

## Verified quotes (each ≤25 whitespace-delimited words)

Source section: **Does it work for all websites?**, stripped text lines 140–143.

| Claim | Verbatim quote | Words | Location |
| --- | --- | ---: | --- |
| No-data failure | “If your origin is not included in the CrUX dataset, there will be no data to display.” | 17 | line 141 |
| Wrong protocol | “Some common issues with origins are providing the wrong protocol, for example http:// instead of https://,” | 16 | line 142 |
| Omitted subdomain | “and omitting the subdomain when needed.” | 6 | line 142 |
| Redirect/canonical host | “if http://example.com redirects to https://www.example.com, then you should use the latter, which is the canonical version of the origin.” | 19 | line 142 |

All four exact substrings remain present; quote assertion cell exited successfully. The last quote is an excerpt beginning mid-sentence, not a newly composed sentence. These are documented lookup pitfalls, not proof that any particular property qualifies or that every no-data result is a false negative.

## Staged S303 comparison and URL collision search

Read staged row `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md:23`. No drift in the four requested claims or published revision. Weekly historical data from the History API remains explicit (line 135); origin-or-URL launch at `cruxvis.withgoogle.com` remains explicit (line 137). Qualification: the page gives direct launch instructions without a key step, but does not explicitly say “without a key”; staged **key-free** wording is an inference from the documented dashboard access route, not a literal quote or an exercised dashboard/API test. The documentation separately says querying the backing History API uses a CrUX API key (line 223). Do not generalize dashboard access to keyless API access.

Lane registry `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md` was searched with the grep tool using `^ {0,3}\\|.*https://developer\\.chrome\\.com/docs/crux/vis`; result: **No matches found**. A second unrestricted literal-URL regex search also returned **No matches found**. Thus zero observed URL collisions, including table rows with 0–3 leading spaces. This is a literal registry search, not a source-ID guard fixture or mirror census; neither required pre-append gate is established by this scout result, and no append was attempted.

## Additive boundary

The adopted `crux-keyless-check.md` theme adds a documented dashboard route for inspecting origin/URL weekly CrUX history without provisioning a key for the dashboard launch, plus an explicit pre-eligibility lookup check for wrong protocol, missing subdomain, and redirects to the canonical host. Existing `corpus/knowledge/field-performance-cwv.md` holds metric thresholds, contributor/discoverability/popularity eligibility, the no-field-data-not-a-pass rule, and keyed API boundaries (especially lines 103–142); it notes that API normalization does not follow redirects but does not hold the CrUX Vis launch route or this dashboard-specific lookup checklist. The addition therefore supplies a bounded inspection path and avoids misdiagnosing an origin spelling/host mismatch as demonstrated ineligibility; it does not add a property measurement, guarantee coverage, supersede eligibility rules, remove the API-key boundary, or claim a CWV pass.

## Commands, outcomes, defects, limits

- Read host RULES, frozen contract, and counter source lines 1–180 before source acquisition; no counter execution assigned or performed.
- Fetch command: `mkdir -p /fast/scratch/hyaku/kake-r86/ScoutAssim /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/ScoutAssim && curl --request GET --location --silent --show-error --fail --dump-header /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/ScoutAssim/crux-vis.headers.txt --output /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/ScoutAssim/crux-vis.html --write-out 'http_status=%{http_code}\\nurl_effective=%{url_effective}\\nbytes=%{size_download}\\n' https://developer.chrome.com/docs/crux/vis` — exit 0; observed HTTP 200 / 114607 bytes.
- Python stdlib HTMLParser stripping, hashlib receipt construction, and exact-substring/≤25-word assertions completed without error; no tools installed or updated.
- Preflight defects: initial bash call selected a not-yet-created scratch cwd and did not execute; retried from the fleet cwd with absolute write destinations. Initial count.py glob used an unavailable internal local path; recovered by reading the counter path specified in the contract. One optional staged-entry lookup used an absent path and returned not found; no claim here relies on that file (the assigned staged S303 row was read directly).
- Only public documentation GET performed. No browser, account, POST/API probe, VCS mutation, source append, sibling write, or production edit. No code contract was changed or investigated, so LSP tracing is not applicable. D84-2/D84-3 remain retained-open; no C1/C2 or whole-queue closure claim.
- Scratch cleanup command and its outcome are retained in `.ufo/waves/round-86/w1/ScoutAssim/cleanup.txt`.

Report: .ufo/waves/round-86/w1/ScoutAssim.md
