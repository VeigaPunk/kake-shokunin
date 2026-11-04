# ScoutAge — round 87 w1

Axes: calibration (2 HOLD), freshness (10 HOLD). Source scouting only: no score movement, outside admission, implementation correctness or cache permission claimed. Confidence high for the quoted source and registry observations; integration remains L1-owned.

## Observed source access

One actual GET of https://httpwg.org/specs/rfc9111.html, final URL unchanged, HTTP 200, 178573 bytes, zero redirects, curl exit 0. Raw SHA-256: `999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64`. HTTP Date: `Wed, 04 Nov 2026 18:22:14 GMT`; post-fetch receipt clock: `2026-11-04T18:22:26Z` (not request/response timing).

Retained absolute paths:
- /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScoutAge/rfc9111.html
- /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScoutAge/rfc9111.headers
- /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScoutAge/receipt.json

## Located quotes (each ≤25 whitespace-delimited words)

All from https://httpwg.org/specs/rfc9111.html#rfc.section.4.2.3. Byte positions below are zero-based UTF-8 starts in the retained raw HTML; line numbers are one-based. Section raw byte range: [79366,83153).

| Meaning | Exact quote | Words | Raw line; byte start |
|---|---|---:|---|
| Missing Age default, in age_value definition | “in a form appropriate for arithmetic operation; or 0, if not available.” | 12 | 270; 80380 |
| apparent_age | “apparent_age = max(0, response_time - date_value);” | 6 | 270; 82082 |
| response_delay | “response_delay = response_time - request_time;” | 5 | 272; 82136 |
| corrected_age_value | “corrected_age_value = age_value + response_delay;” | 5 | 273; 82185 |
| Permitted alternative | “The corrected_age_value MAY be used as the corrected_initial_age.” | 8 | 274; 82282 |
| Conservative alternative | “corrected_initial_age can be calculated more conservatively as” | 7 | 274; 82512 |
| Conservative maximum | “corrected_initial_age = max(apparent_age, corrected_age_value);” | 4 | 274; 82636 |
| resident_time | “resident_time = now - response_time;” | 5 | 275; 82997 |
| current_age | “current_age = corrected_initial_age + resident_time;” | 5 | 276; 83036 |

The MAY quote is rendered text: raw HTML is `The corrected_age_value <em class="bcp14">MAY</em> be used as the corrected_initial_age.` Other table quotes are literal contiguous raw substrings. The conservative prose specifies circumstances with very old cache implementations that might not correctly insert Age. Therefore the max profile is allowed, not the sole RFC-permitted corrected_initial_age algorithm.

## Local conventions versus RFC requirements

Observed §4.2.3 defines date_value as Date in a form appropriate for arithmetic; request_time/response_time/now as clock values; resident time in seconds. It does not prescribe this lane's JSON, integer epoch adapter, bool rejection, required-key list, nonnegative local clock domain, or ordering validation. These are the frozen contract's local interface. Negative date_value is an adapter allowance, not an assertion that RFC mandates negative Date values.

Important distinction: RFC §5.1 DOES define Age as a nonnegative integer in seconds, using delta-seconds. This must not be conflated with requiring every clock input to be integer epoch seconds. RFC §1.2.2 describes finite arithmetic and overflow handling; arbitrary-precision Python arithmetic and the absence of saturation when no overflow occurs are local implementation choices, not RFC mandates. This scouting does not implement an Age header parser or extend the source admission beyond §4.2.3.

## Registry scope and candidate identifier

Literal grep followed by exact row reads at /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md:203,208:
- **S456**, line 203: HTTP cache storage, freshness and validation for interpreting two dated URI captures; unrecognised stored headers, newer-header updates, Age as a clock estimate, ETag/Last-Modified equivalence. Explicitly excludes lane classifier buckets, server policy, ETag strength, directive-argument syntax and origin-byte observation. Its age anchors stop at the Age estimate/date_value definitions, not the full age arithmetic.
- **S461**, line 208: response Cache-Control lifetime first-match and duplicate first-occurrence option, token case-insensitivity, quoted arguments, no-store and delta-seconds overflow; excludes full permission and arbitrary-header equivalence. It supersedes S457 only for previously excluded ordering-rule support.
- Exact word-boundary `S462` search in /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md and /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge returned no matches at access. **Propose S462**, scoped only to §4.2.3 conservative age arithmetic. This is a point-in-time unused-id observation, not a reservation or production registry edit. Older wave fence-marker examples contain literal S462; those are not current source registry rows.

## Bounded planning data-walk (not a competing planner)

Observed definitions/call path in /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/count.py: `HERE` loads the frozen age-cases.json; `main()` C2 calls `git_bytes()` to read the selected revision's scripts/cache_current_age.py; it executes the extracted script with case JSON and compares exit codes plus complete decoded valid-case objects. Receipts and other claim output are not counter inputs. No counter execution was performed by this seat.

Actual affected lane paths, from the contract and seat assignments:
- /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/cache_current_age.py — proposed offline stdin/out integer arithmetic; executor candidate is /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ExecAge/cache_current_age.py.
- /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/age-cases.json and /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/count.py — frozen oracle and finite comparison; no amendments proposed.
- /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/cache-current-age.md — planned sourced entry explaining the equations and local boundaries.
- /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md — planned S462 row, used-by the new knowledge entry, not broader S461 scope.
- /home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md — planned probe registry entry; /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/README.md and /home/vgpnk/Projects/shokunin/kake-shokunin/PROVINCE.md — planned bounded coverage/frontier description.
- /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-87.md and /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/QUALITY.md — assigned lesson/Gate criterion; candidates only until L1 integrates.

Boundary reasoning: computed age alone supplies neither freshness lifetime nor the full storage/reuse gate; therefore cache storage/reuse approval remains out of scope. No browser is involved: the tool is offline and source/trial reads are public GETs. No publishing/deployment/source-repository modification is authorized. Missing Date cannot form required date_value; the contract requires could-not-evaluate for the live trial, never synthesized timing/Date. RFC's reference to HTTP requirements for responses without Date is not implemented here. C1's gate-agreement ledger is independent calibration metadata and not an input to C2.

Semantic-tool limit: `read xd://lsp` returned “No such tool”; no LSP device/server was available to trace definitions/references. The counter path above is textual source evidence, not semantic-reference proof. Candidate implementation and future integrations were not reviewed; no caller completeness claim is made.

## Commands, exits, defects and cleanup

The exact fetch command is retained in receipt.json; its observed curl exit is 0. It used relative output names after explicit `cd /fast/scratch/hyaku/kake-r87/ScoutAge`, contrary to the seat's stricter every-path-absolute wording; the cwd stayed inside owned scratch and no fleet-root write resulted. Initial scratch creation used `mkdir -p /fast/scratch/hyaku/kake-r87/ScoutAge && ls -la /fast/scratch/hyaku/kake-r87/ScoutAge && echo "scratch-ok"`, exit 0.

Hash/size/date commands run from owned scratch: `sha256sum rfc9111.html`, `wc -c rfc9111.html`, `grep -i '^date:' rfc9111.headers`, `date -u +'%Y-%m-%dT%H:%M:%SZ'`; compound command exit 0, outputs recorded above. Raw retention used `cp rfc9111.html /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScoutAge/rfc9111.html`, exit 0 within that compound command. Shell grep and ls were used during initial collection rather than specialized tools; record this process defect, not semantic proof.

Offline Python text-extraction commands exited 0. The first heading search returned -1 because the heading contains a nonbreaking space; its empty section was NOT treated as evidence of absence. Direct raw-term search located the actual section, and subsequent extraction/read provided all quotes. The initial broad grep also included irrelevant .jj binary metadata and historic experimental marker IDs; only the narrowed current corpus search supports unused-id status. No code, key material or session material was sought in that metadata. No production tests/builds/lints/counter/selftest were run. No installs, pacman transactions, service changes, clones, VCS mutations or sibling-file writes.

Final exact cleanup command: `cp /fast/scratch/hyaku/kake-r87/ScoutAge/rfc9111.headers /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScoutAge/rfc9111.headers && rm -r -- /fast/scratch/hyaku/kake-r87/ScoutAge && printf 'headers_retained_and_scratch_removed\n'` — exit 0, printed `headers_retained_and_scratch_removed`. Scratch deleted after retaining HTML and receipt; zero clones used.

Remaining unknowns: integrated carrier behavior and outside admission are not this seat's evidence. No source-blocking gap remains.
