# ReviewC2 — round 83 wave w1

Scope: C2 (`freshness`) attack on the frozen counter `.ufo/waves/round-83/c83_drift_class.py`
(481 lines) and the frozen classifier `scripts/header_change_class.py` (326 lines). Both were read
in full (not sampled) and executed; neither was edited. `git -C <lane> status --porcelain --
scripts/header_change_class.py .ufo/waves/round-83/c83_drift_class.py` printed nothing (rc=0), so
both frozen files are byte-unchanged by this seat. No production file was written; the only lane
writes are this report and `.ufo/waves/round-83/w1/ReviewC2/`. Scratch was
`/fast/scratch/hyaku/kake-r83/ReviewC2/` (deleted before yield). Leaf seat: no subagent, one probe
program (`attacks.py`) in scratch.

Method limits stated up front: no language-server device was mounted in this seat, so
caller/definition checks were done by full-file read plus importing a scratch copy of the counter
(`c83_probe.py`, used to call `load_surface` / `tool_offline` directly), not by LSP. Shell `grep`
was used only for symbol scans, never as proof of absence. Host interpreter: Python 3.14.8.

## Commands run and exit codes

| # | Command (cwd = lane unless noted) | rc | Result |
|---|---|---|---|
| 1 | `python3 -B .ufo/waves/round-83/c83_drift_class.py --root <lane> --work <scratch>/lane-work` | 0 | `met=true`, `control_ok=1`, 14 diffs, all per-request |
| 2 | `python3 -B scripts/header_change_class.py --selftest --work <scratch>/tool-st` | 0 | `selftest: 6/6 passed` |
| 3 | `python3 -B .ufo/waves/round-83/c83_drift_class.py --selftest` | 0 | `selftest: 9/9 passed` |
| 4 | `strace -f -e trace=%network -o …/strace-tool.txt python3 -B scripts/header_change_class.py --a … --b … --declared …` | 0 | **0 network syscalls**; trace has 1 line (`+++ exited with 0 +++`) |
| 5 | `strace -f -e trace=%network -o …/strace-counter.txt python3 -B c83_drift_class.py --root <lane> --work …` | 0 | **0 network syscalls**; 7 traced lines = `SIGCHLD` + exits |
| 6 | `strace -f -e trace=%network … c83_drift_class.py --root <lane> --revision 826b0061… --work …` | 1 | **0 network syscalls**; 9 lines; line byte-identical to `controls/base-c83-drift-class.txt` (`tool_absent=1 met=false`) |
| 7 | `grep -nE '^(import\|from) ' <both files>` | 0 | counter: argparse, ast, hashlib, io, json, re, shutil, subprocess, sys, tarfile, tempfile, pathlib; tool: argparse, hashlib, json, shutil, sys, tempfile, pathlib |
| 8 | `grep -nE '\b(socket\|urllib\|requests\|httpx\|http\.client\|urlopen\|urlretrieve\|ftplib\|smtplib\|telnetlib\|asyncio\|aiohttp\|webbrowser\|xmlrpc)\b'` | 0 | counter 3 hits (its own `NETWORK` constant :54, its docstring :24, its selftest mutant string :440); tool 1 hit (docstring phrase "opens no socket"). No executable reference |
| 9 | `grep -n 'shell=' <both files>` | 1 | absent: all three `subprocess.run` sites pass argv lists |
| 10 | fixture: `D=$(mktemp -d …); git -C "$D" init -q; git -C "$D" config tar.tar.command …; git -C "$D" archive --format=tar HEAD` | 0 | 10 240-byte valid tar, `f.txt` listed, **no marker file** → `tar.<format>.command` is not honored for builtin `tar` |
| 11 | `python3 -B <scratch>/attacks.py` | 0 | all attacks below |
| 12 | `git -C <lane> status --porcelain -- <both frozen files>` | 0 | empty output (unmodified) |
| 13 | `python3 -B -c 'ast.parse(...)' <both files>` | 0 | both parse; counter has 16 functions, tool 10 |

## 1. Network I/O — true of the committed bytes, not guaranteed by the checker

Every code path was read. The counter's only process spawns are `git -C <root> archive --format=tar
<revision>` (`c83_drift_class.py:99`, `--revision` mode only), and `sys.executable -B <root>/TOOL
--a … --b … --declared …` twice plus `--selftest` (`:190-199`, `:280-284`). No `shell=True`; no
`urllib`, `http.client`, `socket`, `requests`, `httpx`; no URL is ever opened. The tool imports no
`subprocess` at all and reads only files under the two capture roots, `d.json`, and its own fixtures.

Syscall-level confirmation: strace with `trace=%network` shows **zero** `socket`/`connect`/`send*`/
`recv*`/`getaddrinfo` calls on the tool run, the counter worktree run, and the counter
`--revision` run (which is the only path that executes `git archive`). The `git archive`
config-execution vector was tested and refuted (#10). **The C2 claim "no network call is made by
the tool or the counter" is proved for the committed bytes.**

`tool_offline` is not what proves it. It is a five-token source denylist
(`NETWORK`, `:54`) applied after stripping the module docstring by *text replacement*
(`:202-215`). Mutation probes on scratch copies of the tool:

| mutant | `tool_offline` | note |
|---|---|---|
| honest `import socket` appended | **False** (caught) | regex is source-global |
| `import socket` inside a nested `def helper()` | **False** (caught) | **nesting is NOT an evasion** — the regex scans the whole text, not top-level statements |
| `importlib.import_module("sock" + "et")` | **True** (evades) | adjacency split defeats `\bsocket\b` |
| `from http import client` | **True** (evades) | pattern only matches `http.client` |
| `subprocess.run(["curl", …])` | **True** (evades) | `subprocess`, `curl` not in the denylist |
| `os.system("wget …")` | **True** (evades) | `os`, `wget` not in the denylist |
| docstring replaced with `sock`, then `import socket` | **True** (evades) | see below |

The docstring-stripping step is itself the hole, and it is the sharpest one: `tool_offline` calls
`ast.parse`, reads `body[0].value.value`, then does a *global* `source.replace(docstring_text, "")`.
A file whose docstring is `"sock"` and which contains `import socket` is scanned as `import et`, so
`NETWORK.search` returns `None` while the interpreter executes `import socket`. That mutant still
compiles (verified with `compile()`). Separately, the check would *false-positive* on the word
"socket" in an ordinary inline comment, and it inspects only `scripts/header_change_class.py`, not
anything that file might import. The evading mutants were never executed (no socket was opened by
this seat); only the checker verdict on their source is claimed.

Neither the tool nor the counter is sandboxed: `sys.executable -B` omits `-I`, `-E` and `-S`.
`PYTHONPATH=<scratch>/inject python3 -B c83_drift_class.py …` produced `met=true` **and** wrote
`<scratch>/inject/marker.txt` via a `sitecustomize.py`, i.e. arbitrary code runs inside the
measurement process before any lane byte is read. "Offline" is a property of the reviewed source,
not of the process that executes it.

## 2. Fabrication — a synthetic capture tree passes the whole predicate

Built `q2-fabricated` in scratch: the real declaration (three `ds4cc.com` ids/URLs), receipts whose
`url` and `finalUrl` are `https://example.test/`, bodies synthesised as
`ghost-body-for-<id>` (never fetched from any socket, correct `bytes` and `sha256`), headers
differing only in `Date` and `X-Cache`, the committed control pair copied verbatim, and the record
generated from the tool's own stdout (exactly what `build_green` does). Counter: **rc=0,
`met=true`**, `receipts_ok=1 diffs=6 validator=0 representation=0 unknown=0 verdict=same-object`.
A second variant with **empty bodies** (`bytes=0`, `sha256=e3b0c442…`) also reads **`met=true`**.

What the counter reads: `response.json` fields `method`, `status`, `bytes`, `sha256`, `truncated`,
`headers` and the local body file (`:120-138`); the declaration's `id` list only; the committed
record; the control pair; the tool source. It never reads the declaration `url`, never compares a
receipt's `url`/`finalUrl`/`fetchedAt` to the declaration, never checks the `Content-Length` header
against the body (proved in §4 by a receipt with body length 78897 and header 78898), and never
checks that two runs came from different instants. `load_surface` also accepts an **absolute**
`bodyFile` (`/etc/hostname` verified accepted; a `../../../` relative escape resolved and failed),
so "reads only committed lane bytes" is false for a crafted receipt.

What the claim can prove: the retained bodies match their declared digests/lengths, the committed
tool is deterministic and reproduces the committed record on this diff set, the committed control
pair classifies as representation-changed, and the tool's selftest is green. What it cannot prove:
that any byte came from `https://ds4cc.com/`, that the two captures are distinct observations, that
the recorded header list is complete, or that the origin behaved as recorded. A hand-built tree is
indistinguishable from a real capture.

## 3. Classification attack — both directions, with the frozen tool

All cases single-surface, body `hello` in both captures unless stated; each row is the tool's own
`surface=` line, rc=0 for every command.

**Frozen table says `same-object` although a crawler's behaviour changes**
- `X-Robots-Tag: noindex, nofollow` → `index, follow`: `policy=1`, `verdict=same-object`. Class row
  **policy**. The lane's own knowledge page quotes MDN: "The X-Robots-Tag response header defines
  how crawlers should index URLs" (`corpus/knowledge/x-robots-tag-header.md:14`, S452:136), and the
  lane ships a dedicated parser (`scripts/x_robots_tag_audit.py`). A change of the indexing
  directive is exactly the crawl-freshness event this gate exists to see, yet it is waved through.
- `Link: <https://ds4cc.com/>; rel="canonical"` → `<https://other.example/>; rel="canonical"`:
  `policy=1`, `verdict=same-object`. Class row **policy**; canonical selection is a documented
  crawler decision factor (`corpus/knowledge/canonical-selection.md:22`, S262).
- `Cache-Control: max-age=600` → `no-store` on a robots.txt surface: `policy=1`,
  `verdict=same-object`. Class row **policy**; RFC 9309 lets a crawler reuse a cached robots copy
  (`corpus/knowledge/robots-txt-rules.md:21`, S011 §2.3.1.4), so this changes what the crawler
  acts on. (`Expires` behaves identically.)

**Frozen table says `representation-changed` although the crawler-visible bytes are identical**
- `Accept-Ranges: bytes` → absent: `representation=1`, `verdict=representation-changed`, with the
  same body sha256 in both captures. Class row **representation**. Range support is a capability
  advertisement; it does not alter the payload a non-range crawler GET receives.
- `Digest: sha-256=AAAA` → `sha-256=BBBB`, body byte-identical: `representation=1`,
  `representation-changed`. Class row **representation**. (`Content-MD5` identical.) `Vary`
  also lands in this row; that one is genuinely ambiguous (a shared cache may key differently), so
  it is not offered as the clean example.

**Contract/code table drift (a conformance defect, not a table-intent defect)**
- The contract's policy row is `access-control-allow-*` (wildcard); the code enumerates only
  `access-control-allow-{headers,methods,origin}`. `Access-Control-Allow-Credentials` absent→`true`
  reads `unknown=1`, `verdict=representation-changed`, where the frozen contract says policy and
  therefore `same-object`. `access-control-allow-private-network` is likewise absent. The
  `cross-origin-*-policy` wildcard *is* fully expanded (3/3). Programmatic diff:
  per-request 21/21, validator 2/2, representation 9/9 exact; policy 15 literals + 2 wildcards,
  expansion incomplete as above (`w1/ReviewC2/contract-table-diff.txt`).

## 4. Control-pair attack — `control_ok` is pinned to the validator row

The committed control pair changes bodies on all three surfaces (so the body-sha arm alone yields
`representation-changed`) plus one `ETag` on `ds4cc-primary`. To isolate each header I equalised
control-B bodies to control-A in scratch and applied one delta. Scratch roots are copies; the
committed `capture-control/` pair was never touched.

| variant | rc | `control_ok` | printed control line |
|---|---|---|---|
| unmodified copy of the tree (`q4-base`) | 0 | 1 | `verdict=representation-changed validator=1`, `met=true` |
| `Content-Length` +1 only (bodies equalised) | **1** | **0** | `validator=0`, `met=false` — **does not flip** |
| `Content-Length` +1 only, committed bodies kept, ETag reverted | **1** | **0** | `validator=0`, `met=false` — **does not flip** |
| `Last-Modified` ±1 h only (bodies equalised) | 0 | 1 | `validator=3`, `met=true` — **flips** |

Both Content-Length constructions satisfy `receipts_ok=1` because the receipt's `bytes` field
matches the body; only the `Content-Length` *header* lies, and nothing validates it. `control_ok`
(`:262-276`) requires `ctl_verdict == "representation-changed" and ctl_totals["validator"] >= 1`,
so a representation-class change alone can never satisfy it — the control is not a general
"any decisive change" witness. It also never runs the tool: it calls the counter's own duplicated
`classify` (`:174-188`), so it cannot detect drift between the two copies of the table.

## Findings

**HIGH-1 — the predicate certifies a classifier that ignores representation drift.** A scratch
copy of the tool with the nine `REPRESENTATION` names moved into `POLICY` (nothing else changed)
passes its own selftest 6/6 and the counter reads `met=true control_ok=1 record_equal=1`. That
mutant prints `verdict=same-object` for a real `Content-Type: text/plain → text/html` change. The
main capture pair only exercises the per-request row (14 diffs, `validator=0 representation=0
unknown=0`), `record_equal` pins only that output, and `control_ok` accepts only `validator>=1`.
Nothing in the frozen predicate exercises the representation row through a header, in either
selftest (`scripts/header_change_class.py:275-281` has no representation-header case; the counter's
selftest has `body-changed`, not a representation header — `c83_drift_class.py:398-442`). This is the main gap: C2 as frozen cannot
distinguish the committed classifier from a representation-blind one.

**HIGH-2 — receipts carry no provenance binding, so a fabricated capture pair reads `met=true`.**
Synthetic bodies, `example.test` URLs under `ds4cc.com` ids, and even zero-byte bodies pass (§2).
The predicate measures internal consistency, not observation.

**MEDIUM-1 — crawler-visible header changes classify `same-object`** (`x-robots-tag`, `Link`
canonical, `cache-control`/`expires` on robots.txt; all policy row). For a freshness gate over
`ds4cc.com/`, `robots.txt` and `sitemap.xml`, these are the changes the gate should surface.

**MEDIUM-2 — byte-identical payloads classify `representation-changed`** (`accept-ranges`,
`digest`, `content-md5`; representation row). The row conflates payload-describing metadata with
payload identity, and the counter's strongest evidence (equal body sha256) is overridden by it.

**MEDIUM-3 — `access-control-allow-*` is under-expanded**, so
`Access-Control-Allow-Credentials` reads `unknown` → `representation-changed` against the contract's
own policy row. The code is not a faithful implementation of the frozen table.

**MEDIUM-4 — `tool_offline` is an evadable five-token denylist** (5/7 mutants pass), the
docstring-strip creates a positive hole, and the measurement process is not isolated (`sitecustomize`
executed via inherited `PYTHONPATH`). `tool_offline=1` must not be read as "this code cannot make a
network call".

**LOW-1** — `load_surface` follows an absolute `bodyFile` out of the tree (`:128`): a crafted receipt
makes the counter hash an arbitrary local file.
**LOW-2** — `record_equal` uses `rstrip(b"\n")` on both sides (`:259`), so any number of trailing
newlines is accepted; the contract wording is "one trailing newline". Verified: record + 4 newlines
still `met=true`.
**LOW-3** — the tool's `--json` flag (`:304`) is never read (`args.json` absent); it is a dead CLI
option that prints the same text. The contract says "`--json` adds nothing the counter reads", but
the flag adds nothing at all.
**LOW-4** — `archive.extractall(target)` (`:107`) passes no explicit `filter=`; safety depends on
the interpreter (3.14 default is `data`; an older `python3` would be `fully_trusted`).
**Positive** — both class tables are identical (`21/2/9/21`); per-request, validator and
representation literals match the contract exactly; the frozen base receipt is reproduced
byte-for-byte under `--revision`; the tool, counter and revision paths make zero network syscalls.

## Residual risk and verification gaps
- The evading `tool_offline` mutants were **not executed** (seat rule: no socket); their evasion is
  proved as a checker verdict plus a compile check, not as observed traffic.
- Provenance of the committed round-81/82 captures was not re-verified (no network this seat), so I
  make no claim about whether the committed receipts are genuine — only that the counter cannot tell.
- `git archive` was tested for `tar.<format>.command` override with a clean fixture; other git config
  hooks (filters, `GIT_*` env) were not exhaustively enumerated.
- The mutant classifier used the counter's unchanged table, so the demonstration is exactly "the tool
  may drift from the frozen table undetected", not "the counter's table is wrong".
- No LSP device was mounted; semantic reference checks were done by full read plus runtime import.

## Verdict
`met=true` reproduces (rc=0) and the committed counter + tool are genuinely offline at the syscall
level, but C2 as frozen is **not decision-grade for its stated claim**. A classifier that ignores
all nine representation headers passes every frozen check (`met=true`, selftest green) while calling
a real `Content-Type` change `same-object`, and a wholly fabricated or empty-bodied capture tree also
reads `met=true`; the only external witness never exercises the tool and accepts only a
validator-class change. Recommendation: C2 evidence should be read as "the committed bytes are
internally consistent and the committed classifier reproduces its record on a per-request-only diff
set" — not as "every moved header is classified correctly" or "the surfaces were observed".
