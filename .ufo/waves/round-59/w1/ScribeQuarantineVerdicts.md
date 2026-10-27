# ScribeQuarantineVerdicts

Seat scope: re-hand-check nine of the twelve quarantine-slice rows (S143, S148, S154, S156, S178, S184, S193, S195, S206) on
2026-10-27 (UTC, access date), each by opening its registered source and searching for the registered quote. Rows S142, S161, S194
belong to the ReviewerQuarantineHold seat and are not reported here. Inputs read only: slice
`.ufo/waves/round-59/assimilation/quarantine-slice` and the register
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (lines 84, 85, 86, 88, 90, 91, 319, 320,
321). No claim is scored by this seat; counters stay at version 1 and wave-1 attacks them, not this report. No file outside this
report and my scratch dir was written.

Probe method: `curl` GET/HEAD per registered URL into `/fast/scratch/hyaku/kake-r59/ScribeQuarantineVerdicts/`, then exact
`str.count` / `grep -F -c` of the registered quote (and of its fragments) on the decoded bytes; for the repo rows, the same string
search over the lane tree with `git grep -n -F` (read-only) plus the cited GitHub page. Receipt digests (sha256, first 16 hex) of the
saved payloads: `s143.html` 22e11fd146aaf43d · `s148abs.html` 2d148a78826d8cc5 · `s148.html` d062c8cac0d20a70 · `s148.src`
76d334f19113e65b · `s154.body` dc05119ba0d5e7f2 · `s156.hdr` 44d4a1947cec06a0 · `s178.body` dca4bd8ae19f1e6f · `s184.body`
da4b1ce0a6833588 · `gh.html` 5f5a33f0020d79f4. Full payloads were deleted with the scratch dir after the counts below were taken.

## ROWS:

| Row | Registered URL | Located text (2026-10-27 probe) | Verdict |
|---|---|---|---|
| S143 | `https://developer.chrome.com/docs/crux/methodology/tools` | GET 200, 106,747 B. `CrUX on BigQuery` 6×; the CrUX-on-BigQuery row cells are all present as separate cells — `CrUX on BigQuery` \| `Monthly` \| `All metrics (except LCP resource types and subparts)` \| `All dimensions` \| `Since 2017` \| `Origin`. The registered string joined by ` — ` has 0 occurrences, and the page's only em dash belongs to a different cell (`No country dimension No—See CrUX History API`) | absent as registered: the quote is a ` — ` concatenation across table cells, not a source span; each cell is present individually |
| S148 | `https://arxiv.org/abs/2308.06409` | abs page GET 200, 43,052 B → `ratio of total to distinct` 0, second registered fragment 0; `https://arxiv.org/html/2308.06409` GET 200, 141,403 B → both 0. E-print `https://arxiv.org/e-print/2308.06409` GET 200, 3,787,699 B gzip, 117 files → both fragments on `sections/analysis.tex` line 11 and fragment 1 again on line 22, and both lines are `%`-commented draft text; line 11 carries `\texthl{[check this and add the more recent dataset information]}` | absent as registered at the cited abstract page; the text exists only as commented-out draft in the paper's own e-print source, so it is a draft-text citation, not a fabrication |
| S154 | `https://chromeuxreport.googleapis.com/v1/records:queryRecord` | GET 404, 1,583 B Google error page (`Error 404 (Not Found)!!1`); no document body, so no quote can be located. Register class: `the cited source could not be fetched, so no quote was checked` | unverifiable-prose-class: a JSON custom-method endpoint, not a page; unreachable is not fabrication |
| S156 | `https://kimi.page/` | `curl -sSLI` → HTTP/2 200; response header line `cache-control: private, no-cache, no-store, max-age=0, must-revalidate` matches the registered quote byte for byte (`date: Tue, 27 Oct 2026 01:51:10 GMT`, `server: cloudflare`) | present — in the HTTP response header, not in the HTML body |
| S178 | `https://www.googleapis.com/pagespeedonline/v5/runPagespeed` | GET → 429, 1,346 B error JSON: `Quota exceeded for quota metric 'Queries' and limit 'Queries per day' … project_number:583797351490`; same 429 with `?url=https%3A%2F%2Fexample.com%2F&strategy=mobile` | unverifiable-prose-class: metered JSON API with no document body; today's probe yields the quota error only |
| S184 | `https://chromeuxreport.googleapis.com/v1/records:queryRecord` | POST `{}` → 403, 248 B: `Method doesn't allow unregistered callers (callers without established identity)…`; GET → 404. Separate register row from S154 (round5 vs round2), same endpoint | unverifiable-prose-class: keyed endpoint, no quotable body; unreachable is not fabrication |
| S193 | `https://github.com/VeigaPunk/kake-shokunin.git` | Page GET 200, 259,390 B: registered sentence 0×. Quote at `corpus/knowledge/crawl-scope-per-host.md:46` in the lane tree at tip `cb685273cc9e` (blob `9710e0343829…`), own-work prose; `git remote -v` shows this URL is the lane's own origin | present in the lane's own-work file; the registered GitHub URL is a repo placeholder whose landing page carries none of the quote |
| S195 | `https://github.com/VeigaPunk/kake-shokunin.git` | Page 0× for `Every publish ends in`. Quote at `corpus/knowledge/publish-queue.md:18` (blob `2fbeab366a2c…`), inside `` `none` (config/policy only). Every publish ends in `human-click` — the `` | present in the lane's own-work file; not at the cited repo landing page |
| S206 | `https://github.com/VeigaPunk/kake-shokunin.git` | Page 0× for `kake merged appendix`; lane tree: the register string appears only in `.ufo/waves/round-48/assimilation/quarantine-handcheck.json` (echoes the register). Artifact `/home/vgpnk/Projects/shokuknow/lanes/kake/round7/.evidence/merge_renumber_r7.txt` (2,610 B) line 1 reads `… round-3 copies at S164-S170, round-6 copies at S187-S193`; registered form with `S187-S199` count 0, `S187-S193` count 1. Its duplicate-title list (lines 34–41) pairs S164/S187 … S170/S193, i.e. 7 round-6 ids | absent as registered — one-token misquote (`S199` vs `S193`); substance verified by the artifact, citation form defective |

Class split of the nine: 3 absent as registered (S143 quote-form, S148, S206), 3 present (S156 header, S193, S195 own-work files),
3 unverifiable-prose-class (S154, S178, S184 — endpoint rows whose register class already says the source could not be fetched).
Today's probes agree with the round-58 hand-check on all nine rows; the only new fact is the S148 locating line (commented-out
`sections/analysis.tex:11/22` in the e-print, with a `[check this …]` marker), which the round-58 note ("0 matches in the opened
full HTML") did not name because it did not open the e-print source. No row's payload was re-derived here — the slice text was taken
as given — and nothing was appended: C3 is frozen to two rows and none of these documents is this round's theme.

## TABLE:

Round-58 `## Assimilation` shape, verdicts dated 2026-10-27 (three rows outside this seat — S142, S161, S194 — omitted; their
round-58 verdicts stand undisputed by this seat):

| Row | Source reopened / located text | Verdict this round |
|---|---|---|
| S143 | `https://developer.chrome.com/docs/crux/methodology/tools`; the CrUX-on-BigQuery cells hold the listed tool/frequency/metrics/dimensions/history/scope, but the registered string is a ` — ` join across cells (0 exact matches) | quote-form absent as registered; no fabrication verdict; not appended (C3 frozen) |
| S148 | `https://arxiv.org/abs/2308.06409` (abstract and HTML endpoints); `ratio of total to distinct` has 0 matches in both — it and the longer fragment sit only in `%`-commented draft lines of the e-print `sections/analysis.tex` (11, 22), one beside `\texthl{[check this …]}` | absent as registered at the cited page; draft-text only; refuse for this round |
| S154 | CrUX API endpoint `https://chromeuxreport.googleapis.com/v1/records:queryRecord`; GET 404, no document body; register class says the source could not be fetched and no quote was checked | unverifiable (prose class; unreachable is not fabrication) |
| S156 | `https://kimi.page/`; `curl -sSLI` returned HTTP/2 200 with `cache-control: private, no-cache, no-store, max-age=0, must-revalidate` | present in the HTTP response header; not appended (C3 frozen) |
| S178 | PageSpeed API `https://www.googleapis.com/pagespeedonline/v5/runPagespeed`; GET 429 quota-exceeded JSON, with and without a `url` parameter; no quotable body | unverifiable (prose class; unreachable is not fabrication) |
| S184 | CrUX API endpoint, same URL as S154; POST 403 `unregistered callers`, GET 404; no quotable body | unverifiable (prose class; unreachable is not fabrication) |
| S193 | GitHub row URL is the lane origin (`git remote -v`); landing page 200 but 0 matches; exact sentence at `corpus/knowledge/crawl-scope-per-host.md:46` (blob `9710e0343829…`) | present in own-work file; not appended (C3 frozen) |
| S195 | Same repo URL, 0 matches on the page; exact sentence at `corpus/knowledge/publish-queue.md:18` (blob `2fbeab366a2c…`) | present in own-work file; not appended (C3 frozen) |
| S206 | Repo landing page 0 matches; shokuknow artifact `lanes/kake/round7/.evidence/merge_renumber_r7.txt` line 1 reads `S187-S193`, the register `S187-S199`, and the artifact's duplicate list is 7 ids (S187–S193) | absent as registered (one-token misquote); substance verified by the artifact; refuse as registered |

Notes for the integrator: (1) four payloads that are genuinely present (S156 header, S193, S195, plus the round-58 S142/S161/S194
trio outside my slice) still cannot be appended under the frozen two-row C3 predicate — the same conformance question round 58
raised to L0, now with a second round of independent confirmation and no new decision from this seat; (2) the S148 draft-line
locating text is the only verdict detail that changed since round 58, and it strengthens the row (draft text, not invention);
(3) the S154/S178/S184 class is a property of the register rows themselves (API endpoints used as documents), so no future
hand-check can upgrade them without a keyed request, which is out of scope for every seat on this wave.

VERDICT: nine rows re-checked 2026-10-27 — S156/S193/S195 present (header and own-work files), S143/S148/S206 absent as registered (cell concatenation, draft-only text, one-token misquote), S154/S178/S184 unverifiable-prose-class; nothing appended, no counter scored.
