# R34 W2 — SentinelToolInputs: input handling of link_preview_audit.py

Target `scripts/link_preview_audit.py` @ `24a16474ee73e20453f3e1be9d2f33573c5196d9` (sha256 prefix `8dd00182 48e04d4e`, 259 lines), Python 3.14.8. Artifacts: `/fast/scratch/hyaku/kake-r34/w2/SentinelToolInputs/` (clone at `.../clone`). No installs, no network, no lane mutation; nothing here was reported by wave 1.

## F1 — HIGH — a canonical href starting with `[` aborts the run with a traceback and exit 1, which the contract defines as failed-policy

`scripts/link_preview_audit.py:218` calls `urljoin(page_url, parser.canonical_href)` outside any try; `absolute_http_url` guards `og:url` (ValueError caught) but not the canonical side. Triggers, page otherwise valid: `href="//["`, `"//[]"`, `"//[]]]"`, `"//[bad/x"`, `"http://[::1"` → `ValueError: Invalid IPv6 URL` (or `'' does not appear to be an IPv4 or IPv6 address`). Non-triggers: `"["`, `"/a[b"`, `"?["`, `"#["`, `"http://a/["`, `"//[::1]/x"`, `"//[::]:80/x"` (normal exit-1 JSON). `"//["` is a realistic truncated-paste typo.

Observed: single page → exit 1, **stdout empty**, stderr tail `ValueError: Invalid IPv6 URL`. Amplification (`t/amp`): 4 pages, 3 with genuine `og_required_missing`, the 4th carrying `href="//["` → exit 1, `stdout_len 0`; all six real findings lost, no report printed.

Impact: violates `c1-matrix.json` key `interface` line 1 ("stdout: one JSON object … for exits 0, 1 and 2") and line 2 (exit 1 = policy findings only). A CI gate trusting the exit code records a policy failure that was never measured; a gate parsing stdout gets nothing. One malformed page destroys the audit of every other page — same class as the disclosed hollow counters: exit 1 reachable with no policy finding in existence. Smallest remediation: wrap resolve-and-compare in `try/except ValueError` and emit `og_url_not_canonical` (an unparseable canonical cannot equal a valid og:url), keeping the frozen reason set and exit codes; add one matrix case for `href="//["`. The 28 cases need re-running after any fix — not done here.

## F2 — MEDIUM — a FIFO listed as a page blocks forever; no timeout, no regular-file check

`t/fifo`: `mkfifo pipe.html` + a manifest listing it → `timeout 5 … --manifest t/fifo/m.json` → **exit 124** (killed). `resolve()`/`relative_to()` accept a FIFO inside the manifest directory and the read at line 167 opens it, blocking until a writer appears. `tar` preserves FIFOs from untrusted archives, so an unpacked or shared corpus directory can carry one unnoticed. Impact: a CI audit hangs indefinitely holding the runner; no partial output exists because JSON prints only after all pages are read. Smallest remediation: require the resolved path to be a regular file (`os.stat` + `S_ISREG`, OSError → `page_unreadable`); also caps the `/dev/*` class.

## F3 — LOW-MEDIUM — one non-UTF-8 page discards every policy finding for the corpus

`t/lat`: valid page 1 + latin-1 page 2 → exit 2, one `page_unreadable`, `pagesChecked: 0`. Contract-conforming (interface line 2 restricts the exit-2 branch to input findings), so a failure-mode note, not a defect: `pagesChecked: 0` understates work already done, and an operator with one legacy-encoded page gets zero signal about the other N. Optional: report `pagesChecked = len(documents)` on the exit-2 path.

## F4 — LOW — a UTF-8 BOM manifest is rejected as "cannot be read as UTF-8 JSON"

`t/lat/m_bom.json` (BOM + valid JSON) → exit 2 `input_invalid`; `json.loads` keeps the BOM and raises, and the message at line 121 blames encoding although the file is UTF-8. A BOM'd *page* is fine (`m_bompage.json` → clean, 0). Cosmetic; `utf-8-sig` for the manifest fixes it.

## F5 — NOTE — containment is path-based and check-then-use, not open-based

Controls that held: `../outside.html`, `sub/../../outside.html`, absolute path, symlink to a file outside, symlink to `/etc/passwd` → all exit 2 `input_invalid` (`t/escape`). Residuals: a **hardlink** inside the directory to an outside file resolves inside and is audited (`t/misc/hardlink.html` → exit 0, its og values consumed), so path containment is not content-origin containment — relevant only if the corpus directory is untrusted (bind mounts likewise); and the check resolves then re-opens by name, so a writer in that directory can swap a file for a symlink (TOCTOU). Output echoes only parsed og values, so leakage is limited to HTML-shaped content; no race was executed.

## Verified non-findings

- **No socket, no write.** `strace -f -e trace=openat,open,socket,connect,write,creat,unlink,rename,mkdir`: zero socket/connect/creat/unlink/rename/mkdir, no `O_WRONLY|O_CREAT|O_RDWR`, writes only on fd 1/2 (`t/io/trace.txt`).
- **Pathological HTML is linear.** 2.2 MB / 200 000 nested `<div>` → 0.42 s; 1.2 MB of `<a ` ×400k → 0.22 s; 6 MB flat → 1.08 s; 3 MB of `<` → 0.88 s; 1.6 MB unterminated `<!--` → 0.04 s; all exit 0. No recursion crash (html.parser is iterative); 100 000 nested `[` in the manifest → exit 2, RecursionError caught.
- **Huge page list linear, unbounded.** 200 000 entries / 10 MB manifest → exit 0, `pagesChecked: 200000`, 10.0 s. No cap on `pages`; a file listed twice is read twice and reported `pagesChecked: 2`. Whole-file `read_text` has no size cap (a multi-GB page would be fully loaded).
- **Degenerate inputs all exit 2, none crash**: manifest is a directory, missing manifest, NUL in `file`, lone surrogate in `file`/`url`, extra manifest key, `--manifest /dev/stdin`. CLI: bare `--manifest` → 64, `--mani x` → 64 (abbrev off), `--help` → 0, repeated `--manifest` → last wins.

## Not tested

No fix applied (leaf scope): 28 frozen cases not re-run against a patch, `c1_matrix_count.py` not run. Symlink-swap TOCTOU not executed; >200 000 manifest entries not tried; other Python versions and non-Linux hosts not tried; counters, selftest, fixtures and non-input logic not reviewed.

## Commands (sandbox, `TMPDIR=$PWD/tmp`)

`git clone -q …/kake-shokunin clone; git -C clone checkout -q 24a1647` → 0. `… --manifest t/canon/manifest.json` → 1 + traceback (F1); `t/fuzz` 17-href loop → 5 traceback cases; `t/amp/m.json` → 1, empty stdout. `timeout 5 … t/fifo/m.json` → 124 (F2). `… t/lat/{m_nonutf8,m_bom,m_bompage}.json` → 2,2,0 (F3/F4). `… t/escape/m_{dotdot,sym,sym2,dd2}.json` → 2,2,2,2. `… t/misc/{hardlink,dirlink,nul,surrogate,surrurl,extrakey}.json`, `dirmanifest`, `missing.json` → 0,2,2,2,0,2,2,2. `strace … t/io/m.json` → 1 (policy findings), trace clean. `t/scale/m_{deep,soup,big}.json` → 0,0,0; `t/list/m_{big,dup,nest}.json` → 0,0,2.
