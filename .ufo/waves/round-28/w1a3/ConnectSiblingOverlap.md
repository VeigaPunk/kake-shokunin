# ConnectSiblingOverlap — round 28 attempt 3, wave 1 (connector, advisory)

Seat: KakeR28a3.ConnectSiblingOverlap. Axes: freshness (C2), operability (C1).
Scope: read-only scan of the 20 sibling lanes `/home/vgpnk/Projects/shokunin/*-shokunin` other than kake:
their `corpus/knowledge/`, `SKILL.md` and `PROVINCE.md` (57 paths exist). No lane, sibling or fleet file was mutated.
No network access. No install. Scratch dir `/fast/scratch/hyaku/kake-r28a3/w1/ConnectSiblingOverlap/` was created empty and left unused.

## Commands (all run from /home/vgpnk/Projects/shokunin)
1. `rg -n -i` for core web vitals | crux | INP | LCP | field performance | field data | web-vitals | pagespeed | lighthouse | interaction to next paint | largest contentful | layout shift | chrome ux report, over the 57 sibling paths — exit 0, 6 hits, all of them false positives or incidental (below).
2. `rg -n -i` for citing.set | citing_set | FIFO | non-blocking | O_NONBLOCK | named pipe | S_ISREG | special file, over the same paths — exit 0. Per-lane hit counts: audio 22, kumitate 18, mori 15, tameshi 12, kama 5, souji 5, kagi 3. `citing.set` or `citing_set`: 0 hits in any sibling lane.
3. `rg -n -i` for web vitals | PerformanceObserver | RUM | real user monitoring | page speed | lab data — exit 0, no on-topic hits.
4. `rg -n -i` for web.dev | developer.chrome.com/docs/(crux|lighthouse|devtools/performance) | chromeuxreport | pagespeed over `*/corpus/SOURCES.md` and `*/corpus/knowledge` (kake included) — exit 0, one hit, in kake.
5. `git -C kake-shokunin show b5d423f:scripts/citing_set.py` (lines 192-290, 338-372); `sed`/`rg` over the lane `PROVINCE.md` files and `.ufo/waves/round-28/sources/*.txt` — exit 0.

## C2 (field performance) — hit list
- No sibling lane holds Core Web Vitals, CrUX, LCP, INP or CLS knowledge. The false positives were:
  `kotodama-shokunin/corpus/knowledge/myth-symbol/flood-traditions.md:48,88` ("crux" meaning a textual crux),
  `kotodama-shokunin/corpus/knowledge/myth-symbol/ritual-liminality.md:111` ("lighthouse keeper"),
  `kasegi-shokunin/corpus/knowledge/ai-assisted-finding-validation.md:39,46` ("field performance" of a security benchmark, unrelated).
- The only incidental web-tooling touch: `tabi-shokunin/corpus/knowledge/chrome-remote-debugging-profile-boundary.md:93` lists Lighthouse as a supported consumer of the DevTools protocol (tabi's ground: browser driving and the DevTools protocol).
- Kake's own prior ground in this area: `kake-shokunin/corpus/SOURCES.md:26` (round-20 row on Firefox INP support) and `:92-94` (unopened leads: W3C Event Timing, web.dev "Optimize INP", Chromium speed metrics changelog). Kake lists the topic as its own frontier: `kake-shokunin/PROVINCE.md:24-26`, and again at `:77`.
- Ownership: tabi (`tabi-shokunin/PROVINCE.md:3-12`) owns browser driving, DevTools protocol sessions and capture of page evidence, and routes web publishing to kake (`:16`). Chousa (`chousa-shokunin/PROVINCE.md:5-8`) owns source hierarchy and research method. Kake's adjacency lines (`kake-shokunin/PROVINCE.md:30-33`) record both splits.
- Verdict on absorption: **the C2 entry, as declared, does not absorb sibling ground.** Thresholds and CrUX eligibility rules are publisher-side domain findings that kake already lists as its own frontier.

## C2 — contested scope (named, not resolved)
1. **Lab measurement belongs to tabi.** S036 (`.ufo/waves/round-28/sources/S036.txt`, sha256 f356a5aa…0078) contains a table of field tools and lab tools (Chrome DevTools, Lighthouse; for INP, Lighthouse says "use TBT instead"). An entry that turns that table into a procedure (run Lighthouse, record a DevTools trace) moves into tabi's browser-execution ground. Holding the table as a fact is kake's; executing it is not.
2. **The CrUX API needs a key, which is kagi custody plus operator authority.** S039 (sha256 cfc40358…b0062) says "Using the CrUX API requires a Google Cloud API key" and shows `queryRecord?key=[YOUR_API_KEY]`. A recheck recipe or gate that calls the API would cross into kagi's ground (`kake-shokunin/PROVINCE.md:34`) and the operator's bounds for this round. CrUX queries also observe live properties, which the round bounds prohibit.
3. **Source hierarchy belongs to chousa.** Whether web.dev articles count as primary sources next to developer.chrome.com documentation is chousa's method question. Kake keeps only its own `SOURCES.md` rows (`kake-shokunin/PROVINCE.md:32-33`).
4. **Contradiction to state, not smooth over:** `kake-shokunin/PROVINCE.md:26` says ground "moves to Core only with source-backed entries and a gate". The C2 counter (`.ufo/waves/round-28/c2_source_count.py:8-21`, sha256 a415dd79…a18) counts cited sources, entry metadata and a lesson line. It is a round measurement, not a domain gate. So C2 can bring held knowledge in but cannot, on its own terms, move field performance from Frontier to Core.

## C1 (citing-set input gate) — hit list
- No sibling owns `citing_set` or any citing-set gate (0 hits). The gate is kake-only (`kake-shokunin/SKILL.md:616-618`).
- Prior art on non-blocking input gates in siblings (method only, no ownership conflict):
  - `kumitate-shokunin/corpus/knowledge/remaining-scripts-census.md:616`: `readBoundedFile` opens O_RDONLY|O_NOFOLLOW|O_NONBLOCK, rejects non-regular descriptors and files over 1 MiB, and re-runs fstat after the read.
  - `kumitate-shokunin/corpus/knowledge/local-ship.md:129-133,225`: O_CLOEXEC|O_NONBLOCK with no O_NOFOLLOW (symlinks followed by design), then an fstat recheck.
  - `kumitate-shokunin/corpus/knowledge/native-trial-launch.md:71`: guarded writes using O_NOFOLLOW|O_NONBLOCK, fstat and refusal when nlink is greater than 1.
  - `souji-shokunin/SKILL.md:103,116`: "a type guard is not a bound". A stat check followed by a separate blocking open hangs on a FIFO swapped in after the check.
  - `audio-shokunin/corpus/knowledge/2026-10-14-sox-fifo-hold-bound.md:11,18`: an open on a FIFO with no writer blocks indefinitely.
  - `tameshi-shokunin/corpus/knowledge/mutation-case-kimi-census.md:67,72,132` and `arm-class-matrix.md:62`: FIFO fixtures used as kill witnesses for file-kind pins.
- How the repair compares: b5d423f `scripts/citing_set.py:219-228` opens with O_NONBLOCK|O_CLOEXEC and checks S_ISREG on the opened descriptor. That matches kumitate's pattern and avoids souji's post-guard swap race, because the type check runs on the inode that is actually read. Ownership: the repair stays kake's. Siblings own only their own gates (`tameshi-shokunin/PROVINCE.md:14-15`).

## Proposed move (one, bounded)
When the L1 drafts `field-performance-cwv.md`, add a boundary paragraph modeled on the round-25 accessibility boundary (`kake-shokunin/PROVINCE.md:70-78`). It would say four things:
- The entry holds thresholds (S037), the metric set (S036) and CrUX eligibility and methodology (S038, S039) as publisher-side knowledge only.
- Running Lighthouse or DevTools lab measurements is tabi-adjacent work.
- CrUX API or PageSpeed queries need a key and live observation, so they stay with the operator and kagi. Any recheck line uses saved source receipts, never an API call.
- Field performance stays Frontier in `PROVINCE.md:24` until a domain gate exists.
Axes: freshness gains clean ground with no overlap dispute. Operability is unharmed: the entry introduces no network or key-bearing recipe. No change to C1 is proposed.

## Risks
- The paragraph adds a few lines that the counter does not check. It is neutral to the C2 count, but the counter's `recheck:` requirement (`c2_source_count.py:15`) might be met by an API-calling recheck line if drafters are not warned.
- A future round may want a gate that counts lab tools. That would need a tabi handoff, which this proposal does not settle.

## Not verified
- I did not run `c2_source_count.py`, `c1_interface_count.py` or the `citing_set` selftest.
- I did not test whether a document that is a symlink inside the root reads the same in working-tree mode (followed, `citing_set.py:214-221`) and in Git mode (`git show` prints the link text, `:341-342`). [INFERENCE] These behave differently. Under the contract the Git-mode result is probably exit 2 for invalid JSON, but this is unmeasured. Sibling `RunRealInputParity.md` may cover it.
- Sibling lanes' `corpus/lessons`, `scripts` and `.ufo` trees were not scanned. The scope was knowledge, SKILL and PROVINCE files only.
