# Seat SentinelFetchSecurity — round-63 w1

**Item.** Security review of the round's network and tool surface: (a) the
committed live fetch receipt `.ufo/waves/round-63/sources/S432.live.html`
contains no credential material; (b) `extract_text.py` and
`scripts/quote_class.py` have no network, no eval, no path traversal beyond
named args; (c) the counters' subprocess use is git only. Verify each claim by
reading the code; report any finding.

**Verdict.**

| claim | verdict |
|---|---|
| live receipt holds no credential material | **CONFIRMED CLEAN** (1.85 MB scanned; only spec prose, two content hashes, and one published editor address) |
| `extract_text.py`: no network / no eval / named-arg I/O only | **CONFIRMED CLEAN** |
| `scripts/quote_class.py`: no network / no eval / named-arg I/O only | **CONFIRMED CLEAN** (reads four fixed relative fixtures under cwd — disclosed by the contract's freeze note) |
| counters invoke subprocess **git only** | **FALSE AS STATED** — `c63_calibration.py` is git-only (confirmed); `c63_quote_tool.py` also **executes the measured revision's `scripts/quote_class.py`** with the invoking interpreter (`c63_quote_tool.py:61-67`). See F1. |

Two provenance defects were proved while attacking the counters, both on the
C2 counter family (F1/F2/F3 below). The measured-commit receipt itself is not
contradicted — the relevant working tree is clean at `05b0d7f4` (`git status
--porcelain` shows only untracked `w1*` files). Whether F2/F3 land C2
`unprovable` under the contract's kill rule is the L1's call; this seat
reports evidence, not adjudication.

**Method.** Source read + AST audit of all four committed artifacts, a
credential-shape scan of the 1,853,393-byte receipt, immutable-asset
re-derivation (`extract_text.py` → `S432.txt`), and two throwaway git fixtures
under `/fast/scratch/hyaku/kake-r63/` (a hostile stand-in tool; a real-tool
tree whose committed vs working-tree bytes differ). No strace, no re-fetch.
Nothing in the fleet repo, `.ufo/state`, `scripts/`, `templates/`, the corpus,
`SOURCES.md`, or `considerthese/` was modified; no git/jj mutation was run
against the fleet root or any sibling repo. This report is the only path
written outside scratch. Scratch dirs
`/fast/scratch/hyaku/kake-r63/SentinelFetchSecurity{,-wt,-run}` were created
with `git -C "$D" init -q` after asserting `git -C "$D" rev-parse
--show-toplevel` == `$D`, used a throwaway identity local to each fixture, and
were deleted; `ls /fast/scratch/hyaku/kake-r63/` no longer lists them.

**Tooling.** None installed; no `pacman` transaction was run (paused
host-wide).

---

## 1. Frozen artifacts — hashes re-verified against the contract

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ sha256sum .ufo/waves/round-63/c63_calibration.py .ufo/waves/round-63/c63_quote_tool.py \
            scripts/quote_class.py .ufo/waves/round-63/quote-class/quote-classes.json \
            .ufo/waves/round-63/sources/S432.live.html
bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91  …/c63_calibration.py
9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e  …/c63_quote_tool.py
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d  …/quote-class/quote-classes.json
63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b  …/sources/S432.live.html
```

All four contract-pinned digests match (`bcd16f68…`, `9fcbfad0…`,
`431e75e8…`, `5f48e26b…`); the receipt digest matches the ledger's
`rawSha256` and the digest quoted in `corpus/lessons/round-63.md`.

## 2. Claim (a) — no credential material in `S432.live.html` — CLEAN

Scanned patterns (case-insensitive, `grep -Eoi`, counts):

```
authorization 10   bearer 0   api[_-]?key 0   secret 2   password 30   passwd 0
set-cookie 54      cookie 265  csrf 0         x-auth 0   session[_-]?id 0
xox[baprs]- 0      SG\.[A-Za-z0-9_-]{10,} 0   glpat- 0  npm_[A-Za-z0-9]{10,} 0
hf_[A-Za-z0-9]{10,} 0  AIza… 0  sk_live_ 0  pk_live_ 0  AKIA[0-9A-Z]{16} 0
ASIA[0-9A-Z]{16} 0   eyJ…(JWT) 0  Bearer [token] 0  Basic [b64] 0
BEGIN (RSA|OPENSSH|EC|PGP) 0   '://user:pass@' 0   '^(authorization|cookie|set-cookie|x-api-key):' 0
/home/ 0   email-shaped unique 1: annevk@annevk.nl (public spec-editor address in the WHATWG footer)
NUL bytes 0   CRLF lines 0   <base> 0   http-equiv="refresh" 0   forms/iframes/objects 0
```

Every hit is the standard's own prose or data, verified by context extraction:

- `Authorization` → spec algorithm text (`<var>authorizationValue</var>`,
  "case-insensitive match for `<code>Authorization</code>`", "`Authorization`
  header is removed").
- `cookie`/`set-cookie`/`password`/`secret` → forbidden-header lists and prose
  ("If we expose redirects that secret would be available through a
  cross-site…"), not values.
- `key=730d67a37d7f3d802e96396d00280768773813fbe726d116944d814422fc1a45` is
  inside an inline **code example** (`S432.live.html:5800`):
  `var url = "https://bar.invalid/api?key=…&data=about:unicorn";` — a
  `.invalid` host, i.e. spec sample data, not a credential.
- `59afe349913d56898c947576216f1c2579308be7` is the WHATWG build's
  commit-snapshot id (`/commit-snapshots/…/`, `S432.live.html:414`); the 64-hex
  string is the sample URL's `key` value above.
- 516 unique 32+-char runs are kebab-case HTML ids/anchors
  (`abstract-opdef-append-the-fetch-metadata-headers-for-a-request`, …).

No request headers were ever in scope: the blob is a bare response **body**
(first 60 bytes `<!doctype html><html lang="en">…`, no header block, no
sidecar `.headers`; `sources/` holds only this one file).

## 3. Claim (b) — no network, no eval, named-arg I/O — CLEAN

AST import/inventory (`ast.walk`, all files at the frozen digests):

| file | imports | writes | file reads |
|---|---|---|---|
| `quote-class/extract_text.py` | `argparse`, `html.parser`, `sys` | `open(args.out,"w",…)` (:96) | `open(args.raw,"rb")` (:93) |
| `scripts/quote_class.py` | `argparse`, `json`, `sys`, `pathlib` | none | `Path(args.raw)` (:129), `Path(args.text)` (:130), four fixed relative fixtures (:43-58) |

- No `urllib`/`requests`/`httpx`/`socket`/`http.client`/`curl` anywhere in the
  round's committed Python; no `eval`/`exec`/`compile`/`__import__`/
  `importlib`/`pickle`/`os.system`/`shell=True`.
- No traversal beyond the named arguments: `extract_text.py` opens exactly
  `args.raw`/`args.out` and nothing else (no glob, no directory walk, no
  normalization); `quote_class.py` opens the two named paths plus four
  hardcoded relative constants joined to `LANE_ROOT = Path.cwd()` (:24) — the
  contract's freeze note names exactly this binding. Neither tool deletes,
  renames, or writes outside the paths given.
- No regex over untrusted text in `quote_class.classify` (:32-37; plain
  substring containment), so no ReDoS surface.
- Deterministic behaviour re-derived, not assumed:

```
$ python3 -B .ufo/waves/round-63/quote-class/extract_text.py --selftest
selftest 1/1
$ python3 -B .ufo/waves/round-63/quote-class/extract_text.py \
    --raw .ufo/waves/round-61/sources/S432.html --out /fast/scratch/…/S432.txt
extracted 1854393 bytes -> 286933 chars        # rc 0
re-derived sha256 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69
committed  sha256 8b90d096…2a69  → identical
$ python3 -B scripts/quote_class.py classify --quote "The \`X-Content-Type-Options\` … destination of a request." \
    --raw .ufo/waves/round-61/sources/S432.html --text .ufo/waves/round-63/quote-class/S432.txt
derived=collapsed-only
$ python3 -B scripts/quote_class.py --selftest      # from the fleet root
selftest 4/4                                       # rc 0
```

The only network code in the neighbourhood is the pre-existing
`scripts/live_snapshot.py` / `response_snapshot.py` (not part of this round's
committed surface); where it matters, `live_snapshot.py` is GET-only, sends
no cookie/auth header, and writes member files `O_NOFOLLOW`/single-link/0600.

## 4. Claim (c) — counters' subprocess is git only — FALSE for C2

`c63_calibration.py` (C1): git only, and **revision-bound** — every evidence
byte comes from `git -C <root> show <rev>:<path>` (:70-74, :93, :107-109);
there is no `open()` in the file, so no working-tree dependence.

`c63_quote_tool.py` (C2): three subprocess calls —

1. `git -C root rev-parse --verify <rev>` (:50)
2. `git -C root show <rev>:scripts/quote_class.py` (:34)
3. **`[sys.executable, "-B", <tmp>/quote_class.py, "--selftest", "--json"]`
   with `cwd=root` (:64-67)** — the committed tool blob is written to a temp
   dir (:61-63) and executed.

Call 3 is the deviation from the ticket's claim, and it is material: the
counter executes whatever code sits at `scripts/quote_class.py` in the
revision it is pointed at, as the invoking user, with `cwd` set to the
`--root` working tree. It also means the C2 result is produced by the
measuring tool's *self-report*, with no identity binding (see F3).

---

## FINDINGS

| # | severity | issue | smallest fix |
|---|---|---|---|
| F1 | MEDIUM | C2 counter executes the measured revision's `scripts/quote_class.py` (code execution surface); contradicts "counters subprocess git only" | `hashlib.sha256(tool_blob).hexdigest() == "431e75e8…"` gate before the exec (`c63_quote_tool.py:60`) |
| F2 | **HIGH** | C2 measurement is not revision-bound: selftest runs against the **working tree** at `--root`, so a revision whose committed fixtures are corrupt can print `met=true` | run the selftest against blobs materialized from `<rev>` (temp tree), not `cwd=root` |
| F3 | MEDIUM | C2 counter trusts the tool's self-reported JSON and never checks the frozen tool sha256; a 20-line stub greens (`met=true`) with no corpus at all — the contract's "a stub tool passes" condition | same sha256 gate as F1 (one check closes both) |
| F4 | LOW | "live fetch receipt" has no committed transport metadata; byte-identical to the round-61 body; no counter reads it — provenance rests on lesson prose | commit a fetch receipt (status/finalUrl/bytes/sha) beside the body, as round-61 did |
| F5 | INFO | receipt is live untrusted HTML with inline + external scripts | keep parsing with `html.parser` (never a browser); already the case |
| F6 | INFO | `-`-prefixed `--revision` values: argparse blocks the space form; the `=` form reaches git but fails harmlessly | add `--end-of-options` / `^[0-9a-f]{40}$` validation if ever driven by untrusted strings |

### F1 — the C2 counter runs code from the revision it measures (proved)

Fixture: throwaway repo with only `scripts/quote_class.py`, a 6-line stand-in
that writes a marker file and prints a fabricated green document.

```
$ git -C "$D" rev-parse --show-toplevel
/fast/scratch/hyaku/kake-r63/SentinelFetchSecurity        # == $D, asserted
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root "$D" --revision 949e6f0ba617f9eb7d02cfa7f3bc05a0aa3ca6e4
revision=949e6f0ba617f9eb7d02cfa7f3bc05a0aa3ca6e4 present=1 selftest=4/4 frozen_cases=ok met=true
exit=0
$ cat "$D/EXECUTED"
ran
```

**Exploit path.** A seat or operator runs the counting command with
`--revision <hostile>` (the lane bounds explicitly allow reading sibling
repos and arbitrary revisions). `c63_quote_tool.py:61-67` writes that
revision's `scripts/quote_class.py` to a temp dir and executes it with
`cwd=<root>`. The payload therefore runs as the invoking user with the
`--root` working tree as cwd and the user's write permissions there; exfiltration
of anything readable and mutation of the `--root` tree are both reachable, and
the receipt looks like an ordinary green.

**Impact.** Local code execution gated only by "which revision is measured".
The frozen measured commit is safe (tool sha verified `431e75e8…`), but the
counter is the artifact future rounds will point at other revisions.

**Smallest remediation.** Bind identity before execution — one line at
`c63_quote_tool.py:60`:

```python
import hashlib
if hashlib.sha256(tool_blob).hexdigest() != FROZEN_TOOL_SHA:   # "431e75e8…"
    print(f"revision={rev} present=1 selftest=tool-identity-mismatch met=false"); return 1
```

That single check removes the code-execution path (a hostile revision no
longer matches the frozen digest) and simultaneously closes F3. It is a
counter edit, so it belongs to a future freeze, not to this seat.

### F2 — C2 green at a revision whose committed bytes are red (proved)

Fixture: throwaway repo holding the **real** frozen `scripts/quote_class.py`
(copied from the fleet root at sha `431e75e8…`), the four fixtures, the
round-61 body and `S432.txt`. Two tests on one revision:

```
$ git -C "$D2" rev-parse HEAD
84a6936ff0f69682a758f41a9ac5af9c49e66019
# (i) clean tree, real fixtures
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root "$D2" --revision 84a6936ff0f69682a758f41a9ac5af9c49e66019
revision=84a6936ff0f69682a758f41a9ac5af9c49e66019 present=1 selftest=4/4 frozen_cases=ok met=true   # exit 0
# (ii) same revision, working-tree S432.txt corrupted (rev bytes untouched)
$ git -C "$D2" status --porcelain
M .ufo/waves/round-63/quote-class/S432.txt
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root "$D2" --revision 84a6936ff0f69682a758f41a9ac5af9c49e66019
revision=84a6936ff0f69682a758f41a9ac5af9c49e66019 present=1 selftest=failed met=false             # exit 1
```

Then the dangerous direction — commit the corruption as the revision, restore
only the working tree:

```
$ git -C "$D2" show <rev>:.ufo/waves/round-63/quote-class/S432.txt
'corrupted\n'                          # committed blob at the measured revision is red
$ git -C "$D2" rev-parse HEAD
242fc6597fd972df64eda5fd5dce58b48bc3b021
$ git -C "$D2" status --porcelain
M .ufo/waves/round-63/quote-class/S432.txt
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root "$D2" --revision 242fc6597fd972df64eda5fd5dce58b48bc3b021
revision=242fc6597fd972df64eda5fd5dce58b48bc3b021 present=1 selftest=4/4 frozen_cases=ok met=true   # exit 0
```

**Exploit path.** Commit a tree with missing/corrupt fixture blobs (or an
absent `S432.txt`), leave the good bytes only in the working tree, run the
counting command, and commit the `met=true` receipt against the bad revision —
the receipt's `revision=` field names bytes that cannot produce it.
`quote_class.py:24,79-85` reads fixtures from `LANE_ROOT` (= the counter's
`cwd=root`); the counter never materializes `<rev>`'s blobs. The reverse
(red receipt against a good revision) is equally free.

**Impact.** The round-63 C1 defect class — a counter green with the source
body absent — recurs on the C2 side in a new shape: green with the source body
**corrupt** at the named revision. "At the measured revision" is a claim the
counter does not enforce. The after receipt is not contradicted (at
`05b0d7f4` the fixture tree is clean), but the guard the wave relies on does
not hold against a tree that differs from its revision.

**Smallest remediation.** Run the tool's selftest in a temp tree populated
from the revision (`git show <rev>:<path>` for the four fixtures and two
blobs), or refuse to run when
`git -C root status --porcelain -- scripts/fixtures/quote-class .ufo/waves/round-63/quote-class .ufo/waves/round-61/sources`
is non-empty and record that check in the receipt.

### F3 — C2 accepts a self-reporting stub (reproduced; same finding as ExecC2CounterAttack §8.1)

The fixture in F1 has **no** fixture files, no corpus, and no `S432` anywhere;
it prints four fabricated cases with the frozen ids and greens:
`present=1 selftest=4/4 frozen_cases=ok met=true`, exit 0. `c63_quote_tool.py`
never imports `hashlib` and never compares `tool_blob` to the contract's
`431e75e8…`; `frozen_ok` (:79-84) checks the tool's own `derived == expected`
claims, which the stub simply states. `result.get("ok")` is truthiness, not
`is True` (`:84`) — the string `"false"` would also pass, per
`ExecC2CounterAttack.md` §8.2.

**Impact.** The contract's C2 kill rule names "a stub tool passes" as an
`unprovable` condition, and its stated defence is the frozen-case-set check;
a stub that emits the four ids defeats it because the check is on ids, not
identity. The C2 *receipt* is honest — the measured commit's tool is the
frozen one — but the counter cannot distinguish it. L1 owns the kill ruling.

**Smallest remediation.** The F1 sha256 gate. (If the intent is to keep the
counter able to measure a *future* tool, gate on "the blob's sha256 equals the
sha256 named in the contract the counter is run against" and print both.)

### F4 — the "live fetch receipt" is body-only and read by nothing

```
$ sha256sum .ufo/waves/round-61/sources/S432.html .ufo/waves/round-63/sources/S432.live.html
63b0a018…911b  .ufo/waves/round-61/sources/S432.html
63b0a018…911b  .ufo/waves/round-63/sources/S432.live.html
$ cmp .ufo/waves/round-61/sources/S432.html .ufo/waves/round-63/sources/S432.live.html && echo IDENTICAL
IDENTICAL
$ grep -c 'S432.live.html' .ufo/waves/round-63/c63_calibration.py .ufo/waves/round-63/c63_quote_tool.py scripts/quote_class.py
0 0 0
$ grep -n 'QUOTE_REL' .ufo/waves/round-63/c63_calibration.py | head -1
41:QUOTE_REL = ".ufo/waves/round-61/sources/S432.html"
```

Byte identity is **disclosed**, not smuggled: `corpus/lessons/round-63.md`
records "opened 2026-10-27, one GET, HTTP 200, 1,854,393 bytes; sha256
byte-identical to the round-61 retained body", and those numbers reconcile
with the committed blob. But the receipt itself carries no URL/status/date/
digest, no in-round fetcher is committed, and neither counter nor tool reads
it — C1's `blobs_match` re-derives from the round-61 path (`QUOTE_REL`, line
41). So the file is corroboration whose "live" provenance is prose-attested
only; a reader cannot distinguish a real re-fetch that returned identical
bytes from a copy, and no counter would notice its absence. That is the
round-61 F1 discipline (retain the run's receipt, not just its body) not yet
applied here. No fabrication evidence: dates, byte count, and digest are
mutually consistent, and byte identity is stated plainly.

**Smallest fix.** Land a one-file receipt next to the body (`status`,
`finalUrl`, `fetchedAt`, `bytes`, `sha256`), as round-61's `response.json`
did, and cite it from the re-open case.

### F5 — retained HTML is active content (INFO)

7 `<script>` blocks (6 inline, 1 external
`src="https://resources.whatwg.org/commit-snapshot-shortcut-key.js"`), no
`<base>`, no meta-refresh, no forms/iframes/objects, NUL-free, LF-only, UTF-8.
Reading it in a browser executes publisher JS and fetches from `whatwg.org`;
the lane's parser (`html.parser`, `extract_text.py:60-63`) never executes
anything, and the analysis tools are pure text processing. No action required;
worth keeping `html.parser` (never a headless browser) for retained blobs.

### F6 — git argv injection is unreachable as shipped (INFO)

```
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root "$D" --revision --all
c63_quote_tool.py: error: argument --revision: expected one argument     # rc 2 (argparse)
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root "$D" --revision=--all
could-not-evaluate: revision --all unreadable                            # rc 2 (rev-parse rc 128)
$ python3 -B .ufo/waves/round-63/c63_quote_tool.py --root "$D" --revision=--output=/fast/scratch/hyaku/kake-r63/out2.txt
could-not-evaluate: revision --output=/… unreadable                      # rc 2; no file written
```

The space-separated form cannot reach `git` (argparse consumes `--all` as an
option); the `=` form reaches `git rev-parse --verify`, which exits 128 for
every option-shaped value tried, so the counter returns 2 before any
`git show`. `c63_calibration.py` behaves identically:

```
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision --all
c63_calibration.py: error: argument --revision: expected one argument     # rc 2
$ python3 -B .ufo/waves/round-63/c63_calibration.py --root . --revision=--all
could-not-evaluate: revision --all unreadable                             # rc 2
```

No injection, no file write. Residual hardening only: `git show` args are
built as `f"{rev}:{rel}"` with no `--end-of-options`, so the safety argument
rests on `rev-parse` rejecting option strings; add `--end-of-options` and/or
validate `^[0-9a-f]{40}$` if a future counter is driven by untrusted strings.

---

## Attested clean (no finding)

- Both tools and both counters are free of network imports and of
  `eval`/`exec`/`compile`/`__import__`/`importlib`/`pickle`/`os.system`/
  `shell=True` (AST + text audit; the only `subprocess` uses are enumerated in
  §4 and all but one are `git`).
- `c63_calibration.py` reads **only** `git show` output — it cannot be greened
  by an untracked working-tree edit; C1's evidence is revision-bound.
- `extract_text.py` reproduces the committed `S432.txt` byte-exactly
  (`8b90d096…2a69`), so the `collapsed-only` class rests on a re-derivable
  recipe, and the C1 counter's inline `classify` (`c63_calibration.py:56-63`)
  matches the tool's semantics without importing it (separability holds).
- Receipt integrity: single regular file, 1,853,393 bytes, sha256
  `63b0a018…911b`, no header block, no NUL/CRLF, no userinfo URLs, no
  provider-token shapes, no private-key material, no local paths.
- `S432.live.html` and the round-61 body are byte-identical, and the ledger's
  `rawSha256`/`textSha256` are the digests of those exact bytes — the ledger's
  numbers re-derive from the retained blobs.

## Receipts / evidence files

All commands above were run from
`/home/vgpnk/Projects/shokunin/kake-shokunin`; scratch fixtures were
`/fast/scratch/hyaku/kake-r63/SentinelFetchSecurity` (hostile stand-in, rev
`949e6f0b…`), `…/SentinelFetchSecurity-wt` (real tool, revs `84a6936f…`,
`242fc65…`), and `…/SentinelFetchSecurity-run` (extract/classify); all were
deleted (`ls /fast/scratch/hyaku/kake-r63/` shows only sibling seats' dirs).

## Unrun

No `strace`/syscall trace (imports and the AST inventory settle the
network/exec question); no independent re-fetch of the S432 URL
(`ScoutS432Reopen` owns currency); no run of `c63_calibration.py` against the
fleet repo (other seats own that measurement; nothing in this review depends
on it). No tool installs, no `pacman`.

**Bottom line.** The receipt and both tools pass the assigned security checks
cleanly. The counters do **not** match the ticket's "subprocess git only"
characterisation — `c63_quote_tool.py` executes the measured revision's tool —
and that exec path is the same line that makes C2's measurement non-revision-
bound (F2, proved: `met=true` at a revision whose committed fixture is
`corrupted\n`) and lets a self-reporting stub green it (F3). One sha256 gate
plus revision-materialized fixtures would close all three; both are counter
edits and therefore future-freeze work, not this seat's.
