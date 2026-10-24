# ReopenS134 — freshness falsification

- Seat: `kake-r45.ReopenS134`.
- Axes: **freshness** (assigned attack); **operability** is the parent lane's other axis, not independently assessed here.
- **Verdict: reject reason still holds. PASS for the named re-verification item; FAIL to falsify the rejection as stale.** Confidence: high for these two fetched surfaces.
- Both live fetches completed at `2026-10-24T03:56:57Z`, HTTP **200**.

## Observed facts

The rejection at `corpus/SOURCES.md:142` and `corpus/lessons/round-45.md:13` has two parts: the general negative-return-code point duplicates tier-A S133, while the extra `-11` → signal 11 → `SIGSEGV` mapping is not supported by the opened primary subprocess page. Its flip requires an opened tier-A POSIX/Python signal source, with the answer used illustratively rather than as support.

1. [The Stack Exchange API](https://api.stackexchange.com/2.3/questions/24139389/answers?site=stackoverflow&filter=withbody) still returns exactly one answer, accepted answer **24139472** by **sth**, with `has_more=false`. Its HTML body is byte-identical to the retained `.ufo/waves/round-45/sources/so-answer.json` body's value. The response JSON differs only in `quota_remaining` (295 → 284), not answer content.
2. Literal answer to “does it carry **only** the point S133 covers?”: **no**. It also explicitly names segmentation fault and `SIGSEGV`. That extra mapping was already acknowledged by the rejection; it is not newly added evidence. The general negative-status semantics remain the duplicated, receipt-gate-relevant point.
3. [The Python subprocess page](https://docs.python.org/3/library/subprocess.html#subprocess.Popen.returncode) still contains the S133 negative-value sentence at `Popen.returncode`, paragraph 3 (fetched HTML lines 1191–1192), and also at `CompletedProcess.returncode`, paragraph 2. A case-insensitive sweep of the entire fetched HTML and its parsed visible text finds **zero** occurrences of `SIGSEGV`, `segmentation fault`, or `signal 11`.
4. Do **not** report that the substring `-11` is absent: its one occurrence is the unrelated issue label `gh-114539`, at fetched HTML line 995. It does not map a status or signal.
5. The Python page's hash changed, but the complete raw line diff contains only its footer build timestamp: `00:13 UTC` → `03:37 UTC`. No substantive source passage changed.

### HTTP/body identity

Hashes below cover the **decoded bytes saved by `curl --compressed`**, not gzip wire bytes. Both responses declared `content-encoding: gzip`. Curl's `size_download` was 492 / 30,429 bytes; the saved JSON/HTML sizes were 723 / 208,624 bytes.

| Surface | HTTP | Saved bytes | SHA-256 |
|---|---:|---:|---|
| SO answers JSON | 200 | 723 | `79c3ddc47dd57bd9b7586796936270178919920ab0df35fa9a0104a0e6697c8e` |
| Python subprocess HTML | 200 | 208624 | `b4c58392796b5dedeae51c96f051a6f265f196f55041e56072c2c80f43d19355` |

## Exact commands and decisive output

All shell commands used lane cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`. The two curl commands ran concurrently. The scratch analysis script uses only Python's standard library (`HTMLParser`, `json`, `hashlib`, `difflib`); it compares the fetched files against the retained source files and prints the entire HTML line diff.

```sh
mkdir -p /fast/scratch/hyaku/kake-r45/ReopenS134
curl -sS -L --compressed --max-time 90 --dump-header /fast/scratch/hyaku/kake-r45/ReopenS134/so-answer.headers --output /fast/scratch/hyaku/kake-r45/ReopenS134/so-answer.json --write-out 'so-answer HTTP=%{http_code} bytes=%{size_download} url=%{url_effective}\n' 'https://api.stackexchange.com/2.3/questions/24139389/answers?site=stackoverflow&filter=withbody' && sha256sum /fast/scratch/hyaku/kake-r45/ReopenS134/so-answer.json && date -u +FETCH_COMPLETED_UTC=%Y-%m-%dT%H:%M:%SZ
curl -sS -L --compressed --max-time 90 --dump-header /fast/scratch/hyaku/kake-r45/ReopenS134/subprocess.headers --output /fast/scratch/hyaku/kake-r45/ReopenS134/subprocess.html --write-out 'subprocess HTTP=%{http_code} bytes=%{size_download} url=%{url_effective}\n' 'https://docs.python.org/3/library/subprocess.html' && sha256sum /fast/scratch/hyaku/kake-r45/ReopenS134/subprocess.html && date -u +FETCH_COMPLETED_UTC=%Y-%m-%dT%H:%M:%SZ
wc -c /fast/scratch/hyaku/kake-r45/ReopenS134/so-answer.json /fast/scratch/hyaku/kake-r45/ReopenS134/subprocess.html
python3 -B /fast/scratch/hyaku/kake-r45/ReopenS134/analyze_sources.py
```

Verbatim fetch and size output:

```text
so-answer HTTP=200 bytes=492 url=https://api.stackexchange.com/2.3/questions/24139389/answers?site=stackoverflow&filter=withbody
79c3ddc47dd57bd9b7586796936270178919920ab0df35fa9a0104a0e6697c8e  /fast/scratch/hyaku/kake-r45/ReopenS134/so-answer.json
FETCH_COMPLETED_UTC=2026-10-24T03:56:57Z
subprocess HTTP=200 bytes=30429 url=https://docs.python.org/3/library/subprocess.html
b4c58392796b5dedeae51c96f051a6f265f196f55041e56072c2c80f43d19355  /fast/scratch/hyaku/kake-r45/ReopenS134/subprocess.html
FETCH_COMPLETED_UTC=2026-10-24T03:56:57Z
   723 /fast/scratch/hyaku/kake-r45/ReopenS134/so-answer.json
208624 /fast/scratch/hyaku/kake-r45/ReopenS134/subprocess.html
209347 total
```

Verbatim analysis output:

```text
ANSWER items=1 has_more=False
ANSWER id=24139472 author=sth accepted=True last_activity_date=1402398482
ANSWER text=Return code -11 means "segmentation fault". A negative return code usually means that the process was terminated by a signal. Return code -11 means it was signal 11, which is SIGSEGV.
ANSWER body_sha256=51b11fc5f8de927fd96cfa59761a7adce09d89fc8a77bed2bb571a7ec59c5ffe
ANSWER body_identical_to_retained=True
ANSWER top_level_changed_keys=quota_remaining
ANSWER raw_sha256 fresh=79c3ddc47dd57bd9b7586796936270178919920ab0df35fa9a0104a0e6697c8e retained=702954fd1946cfa2e3895804f48c850acd25a47523a780e1599e7851716ffcd1
DOCS raw_bytes fresh=208624 retained=208624
DOCS raw_sha256 fresh=b4c58392796b5dedeae51c96f051a6f265f196f55041e56072c2c80f43d19355 retained=eceda6f6363491ad1d0bf2aeaed06c3c37605f502aecdb36f7326ed1e5bdf0dd
DOCS visible_text_identical_to_retained=False
DOCS token='SIGSEGV' raw_count=0 visible_count=0
DOCS token='-11' raw_count=1 visible_count=1
DOCS token='segmentation fault' raw_count=0 visible_count=0
DOCS token='signal 11' raw_count=0 visible_count=0
DOCS negative_signal_quote_count=2
DOCS #subprocess.CompletedProcess.returncode paragraph_1=Exit status of the child process. Typically, an exit status of 0 indicates that it ran successfully.
DOCS #subprocess.CompletedProcess.returncode paragraph_2=A negative value -N indicates that the child was terminated by signal N (POSIX only).
DOCS #subprocess.Popen.returncode paragraph_1=The child return code. Initially None, returncode is set by a call to the poll(), wait(), or communicate() methods if they detect that the process has terminated.
DOCS #subprocess.Popen.returncode paragraph_2=A None value indicates that the process hadn’t yet terminated at the time of the last method call.
DOCS #subprocess.Popen.returncode paragraph_3=A negative value -N indicates that the child was terminated by signal N (POSIX only).
DOCS #subprocess.Popen.returncode paragraph_4=When shell=True, the return code reflects the exit status of the shell itself (e.g. /bin/sh), which may map signals to codes such as 128+N. See the documentation of the shell (for example, the Bash manual’s Exit Status) for details.
DOCS raw_diff:
--- retained/subprocess.html
+++ fresh/subprocess.html
@@ -2037 +2037 @@
-      Last updated on Oct 24, 2026 (00:13 UTC).
+      Last updated on Oct 24, 2026 (03:37 UTC).
```

The initial source search used `functions.grep` with `pattern="S134|S133|24139389"`; relevant registry/Gate rows were then read in full. The final literal false-positive check used `functions.grep` with `pattern="-11"`, `case=true`, `gitignore=false`, over the fetched `subprocess.html`. Its decisive matching line was:

```html
<code class="docutils literal notranslate"><span class="pre">shell=True</span></code> to allow Python to escape special characters. See <a class="reference external" href="https://github.com/python/cpython/issues/114539">gh-114539</a>
```

## Inference and remaining unknowns

- **Inference:** S134's rejection is fresh for its recorded receipt-gate scope: unchanged general semantics duplicate S133, while its unchanged extra signal-number mapping still lacks support on the opened primary page. The tier-C scope limit remains supported; this is not a claim that the mapping is false.
- The absence finding is limited to `library/subprocess.html`, not all Python documentation, all platforms, or linked pages. No additional tier-A POSIX/`signal` page was opened to exercise the recorded flip. No source dependency was missing.
- No exported-code contract was investigated; LSP definition/reference tracing was not applicable. No build, test, gate, or census was run or claimed. No tools were installed or updated. No committed lane source, frozen artifact, or other seat's file was changed.

## Every file written

Lane (only authorized report):
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w2/ReopenS134.md`

Scratch only:
- `/fast/scratch/hyaku/kake-r45/ReopenS134/so-answer.headers`
- `/fast/scratch/hyaku/kake-r45/ReopenS134/so-answer.json`
- `/fast/scratch/hyaku/kake-r45/ReopenS134/subprocess.headers`
- `/fast/scratch/hyaku/kake-r45/ReopenS134/subprocess.html`
- `/fast/scratch/hyaku/kake-r45/ReopenS134/analyze_sources.py`
