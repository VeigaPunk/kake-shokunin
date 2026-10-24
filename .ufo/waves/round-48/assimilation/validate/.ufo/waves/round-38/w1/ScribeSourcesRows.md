# Round 38 — ScribeSourcesRows

## Behavior and gate
- Axes: operability and freshness; this leaf covered source freshness/curation only.
- Canonical claim check: the snapshot at `SCORECARD.md` commit `2dab7f3` explicitly withdraws C1 before any build (line 2196); the later C2 declaration at line 2211 and 20/20 predicate at line 2221 match the supplied context. No predicate conflict.
- All five requested URLs were opened with one GET each at 2026-10-23T04:30:34Z; each returned HTTP 200 with no redirect. Saved copies and byte counts: RFC 8259 8,885; RFC 3986 41,367; RFC 9309 HTML 18,660; Python JSON docs 18,294; WHATWG URL 97,951.
- Gate decisions in the sandbox draft: S034 re-open/retain; S098 RFC 3986 §§2.1–2.3 admit A/spec/queued; S011 re-open/retain; S099 broader RFC 9309 row admit A/spec/queued; S100 Python JSON docs admit A/docs/queued; S101 WHATWG URL reject A/spec with a flip condition.
- S098 distinguishes RFC 3986 character classes from S029 §3 and S089 §5.2. S100 grounds Python's default acceptance of non-finite constants; S101 is rejected because the lane's rule is RFC 3986 and `robots_audit.py` uses `urllib.parse`, not WHATWG parsing.
- S011/S034 existing cells unchanged: S011 `mined→mined`, `365d→365d`, used-by unchanged; S034 `mined→mined`, `365d→365d`, used-by unchanged. New rows are queued or rejected with used-by `—`; queued rows remain queued until a real citing path exists. The round-38 lesson path does not exist yet.

## Commands and observed outcomes
- `mkdir -p /fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/tmp /fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/sources` — exit 0.
- `date -u; timeout 130s prlimit --as=4000000000 -- curl --compressed --location --request GET --max-time 120 --silent --show-error --output /fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/sources/rfc8259.txt --write-out 'HTTP %{http_code} final=%{url_effective} bytes=%{size_download}\n' https://www.rfc-editor.org/rfc/rfc8259.txt; rc=$?; printf 'curl exit=%s\n' "$rc"; exit 0` — shell/curl exit 0; `2026-10-23 04:30:34Z`, HTTP 200, 8,885 bytes.
- `date -u; timeout 130s prlimit --as=4000000000 -- curl --compressed --location --request GET --max-time 120 --silent --show-error --output /fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/sources/rfc3986.txt --write-out 'HTTP %{http_code} final=%{url_effective} bytes=%{size_download}\n' https://www.rfc-editor.org/rfc/rfc3986.txt; rc=$?; printf 'curl exit=%s\n' "$rc"; exit 0` — shell/curl exit 0; `2026-10-23 04:30:34Z`, HTTP 200, 41,367 bytes.
- `date -u; timeout 130s prlimit --as=4000000000 -- curl --compressed --location --request GET --max-time 120 --silent --show-error --output /fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/sources/rfc9309.html --write-out 'HTTP %{http_code} final=%{url_effective} bytes=%{size_download}\n' https://www.rfc-editor.org/rfc/rfc9309.html; rc=$?; printf 'curl exit=%s\n' "$rc"; exit 0` — shell/curl exit 0; `2026-10-23 04:30:34Z`, HTTP 200, 18,660 bytes.
- `date -u; timeout 130s prlimit --as=4000000000 -- curl --compressed --location --request GET --max-time 120 --silent --show-error --output /fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/sources/python-json.html --write-out 'HTTP %{http_code} final=%{url_effective} bytes=%{size_download}\n' https://docs.python.org/3/library/json.html; rc=$?; printf 'curl exit=%s\n' "$rc"; exit 0` — shell/curl exit 0; `2026-10-23 04:30:34Z`, HTTP 200, 18,294 bytes.
- `date -u; timeout 130s prlimit --as=4000000000 -- curl --compressed --location --request GET --max-time 120 --silent --show-error --output /fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/sources/whatwg-url.html --write-out 'HTTP %{http_code} final=%{url_effective} bytes=%{size_download}\n' https://url.spec.whatwg.org/; rc=$?; printf 'curl exit=%s\n' "$rc"; exit 0` — shell/curl exit 0; `2026-10-23 04:30:34Z`, HTTP 200, 97,951 bytes.
- `timeout 30s prlimit --as=4000000000 -- sha256sum /fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/sources/rfc8259.txt /fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/sources/rfc3986.txt /fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/sources/rfc9309.html /fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/sources/python-json.html /fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/sources/whatwg-url.html; printf 'sha256sum exit=%s\n' "$?"` — exit 0; hashes below.
- `timeout 30s prlimit --as=4000000000 -- sha256sum /fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/sources-rows.md` — exit 0; final draft SHA256 `9abfa636c2501c7c306d94bc19a6285be45f95feabe6a9b7ae77b70d380aa9db`.
- `functions.grep` over the retained copies returned the quote excerpts (line references and excerpts pasted in `sources-rows.md`); the tool does not expose shell exit codes. Draft records the source-specific search patterns, including both RFC 3986 §2.2/§2.3 and inline-HTML notes for Python/WHATWG quotes. The Python 3.15.1 page identifies itself as v3.15.1; WHATWG says Living Standard last updated 2026-10-19.
- `export TMPDIR=/fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/tmp; unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; timeout 30s prlimit --as=4000000000 -- git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 2dab7f3114f3e9dcf072b524c88816ab05fdfcf1:SCORECARD.md > /fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/SCORECARD-2dab7f3.md; rc=$?; printf 'git show exit=%s\n' "$rc"; exit 0` — exit 0.
- `timeout 30s prlimit --as=4000000000 -- sha256sum /fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/SCORECARD-2dab7f3.md; printf 'sha256sum exit=%s\n' "$?"` — exit 0; SHA256 `b7432d69ffc4302bf0f5f6604913699f1d9ad996846e866230ceb257d7b31841`.

## Findings and limits
- S034 §6 re-open quote excludes Infinity/NaN from JSON numbers; the retained row remains correctly scoped.
- S011 §2.2.2 says `/robots.txt` is implicitly allowed. That statement does not itself specify this round's normalized-path implementation choice. Proposed S099 addresses the round-37 finding that existing S011 scope was narrower than the knowledge entry's use; S099 must remain queued until the knowledge citation is updated.
- Verbatim S011 conflict from `corpus/lessons/round-37.md:72-74`: “S011 section 2.2.2 says octets "in the reserved range" MUST be percent-encoded before comparison; read literally, `%2F` and `/` compare equal. The contract follows Figure 4 instead (`ScoutReopenS011` D1); the knowledge entry now says so.” Keep this source-versus-local-contract conflict visible.
- No lane registry/product file was edited; no counters, tests, builds or selftests were run. No sealed-case trees were opened or searched. No tools were installed.

## Touched surfaces and artifacts
- Report only in the lane: `.ufo/waves/round-38/w1/ScribeSourcesRows.md`.
- Review draft: `/fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/sources-rows.md` (SHA256 above); contains proposed rows, Gate lines, grep excerpts and cell transitions.
- Requested claim snapshot: `/fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/SCORECARD-2dab7f3.md` (SHA256 above); no sealed cases or counters were inspected.
- Retained source copies under `/fast/scratch/hyaku/kake-r38w1/ScribeSourcesRows/sources/`:
  - `rfc8259.txt` SHA256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`
  - `rfc3986.txt` SHA256 `3102dae4b68cebe40337730312fcb612297b8928547267e8b3d1ee6002b2d683`
  - `rfc9309.html` SHA256 `bbaa280636d3e38f0a1a130a5ce40e9753db1ed18c860945b0bf795ff8dc1a87`
  - `python-json.html` SHA256 `234b80bf7385ea72e198521156d012cbe8997bab428740468f46f881a07f792e`
  - `whatwg-url.html` SHA256 `08cb42a9a8575dab006676378c846fdd8a72d06897c27929aa51eaf099656be4`
- No installs or upgrades.