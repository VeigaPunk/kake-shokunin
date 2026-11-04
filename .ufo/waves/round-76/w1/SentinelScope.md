# SentinelScope — round 76, wave w1 (scope, secrets, reproducibility)

Seat: leaf sentinel, kake lane round 76 w1 attempt 1. Lane checkout read-only; every experiment ran in
`git clone --shared` trees under `S=/fast/scratch/hyaku/kake-r76/SentinelScope` with `TMPDIR=$S/tmp`.
Base revision for every before-state: `a0491fcd041cbc3fff2c964ecf6268557e45a5c1`.
Measurement instant for every count below: **2026-11-03 22:14 -0300 (`01:14Z`)**, lane HEAD
`152bffd5`. The wave was in flight throughout: the L1 committed `442d36c6`, `d2555766`, `d00ea7fb` and
`152bffd5` during the audit, and the C1 instrument itself was rewritten **seven times**; the last build
this seat measured is `e7f86d3a…` (49,077 B, 22:13:35, `63/63` selftest cases; §5.2), and it was still
being rewritten when this report was written. One seat report was still unwritten — §7. No tool was
installed or upgraded; no model was named; this seat used no network.

---

## 1. Write scope

### 1.1 Observed inventory (603 files, 19 top-level, 14 seat reports)

| Path | Files | Owner |
|---|---|---|
| `.ufo/waves/round-76/` top level (`contract.md`, `c76_quote_truth.py`, `mk_w1_spec.py`, amendments 1–8, `l1-dispositions.md`, `blocks-{knowledge,quality,lesson}.md`, `w1-spec.json`, `w1-dispatch.json`, `w1.ready`, `w1.ready.dispatched`) | 19 | L1 |
| `.ufo/waves/round-76/controls/` (base receipts, `ctl-*.txt`, `base-c1-quote-truth-v2.txt`, `after-c2-{matrix,realrun}.txt`, `census-before.txt`, `sweep-r76.txt`, `harm-base.txt`, `r1-r2-digests.txt`) | 13 | L1 / gates |
| `w1/ExecAuditMatrix/` | 86 | ExecAuditMatrix |
| `w1/ExecAuditRealRun/` | 27 | ExecAuditRealRun |
| `w1/ExecAuditTool/` | 15 | ExecAuditTool |
| `w1/ExecQuoteCounter/` (instrument + receipts; no report at cutoff) | 13 | ExecQuoteCounter |
| `w1/ExecQuoteRepair/` | 16 | ExecQuoteRepair |
| `w1/MutationTesterGates/` | 64 | MutationTesterGates |
| `w1/ReviewerC1/` | 147 | ReviewerC1 |
| `w1/ReviewerC2/` | 177 | ReviewerC2 |
| `w1/ScoutHreflangSources/` | 10 | ScoutHreflangSources |
| `w1/*.md` | 14 | the seats |
| `w1/swarm-registry.json` | 1 | dispatcher artifact |

Every observed path is inside `.ufo/waves/round-76/`, with the landing writes in §1.2. Every seat's
files sit under its declared report/artifact paths; `ExecAuditTool/hreflang_audit.py` is in the wave dir as
its item requires.

### 1.2 Scope confirmations and the landing writes

`git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --porcelain` at the instant:

```
?? .ufo/waves/round-76/blocks-knowledge.md
?? .ufo/waves/round-76/blocks-lesson.md
?? .ufo/waves/round-76/blocks-quality.md
?? .ufo/waves/round-76/controls/after-c2-matrix.txt
?? .ufo/waves/round-76/controls/after-c2-realrun.txt
?? .ufo/waves/round-76/controls/base-c1-quote-truth-v2.txt
?? .ufo/waves/round-76/controls/harm-base.txt
?? .ufo/waves/round-76/controls/r1-r2-digests.txt
?? .ufo/waves/round-76/w1.ready
?? .ufo/waves/round-76/w1.ready.dispatched
?? .ufo/waves/round-76/w1/
?? corpus/lessons/round-76.md
?? scripts/doc_quote_truth.py
?? scripts/hreflang_audit.py
```

No lane **root** file (`SCORECARD.md`, `LOG.md`, `SKILL.md`, `PROVINCE.md`) and no file under
`.ufo/state/` was touched. **No seat wrote under `scripts/`, `corpus/`, a lane root file or a sibling
lane.** The non-wave-dir paths are L1 landing work, verified:

| Path | Evidence it is the L1's, not a seat's |
|---|---|
| `scripts/doc_quote_truth.py` | byte-identical to the wave copy when copied (`eae3ce48…`), mtime 22:08:27 — 2 s after that wave copy; the ExecQuoteCounter item delivers into the wave dir only. It is now **stale** relative to the final wave build (§5.3 F3) |
| `scripts/hreflang_audit.py` | byte-identical to `w1/ExecAuditTool/hreflang_audit.py` (`0762452f…`, mtime 22:12:20), as the ExecAuditTool item requires the L1 to copy it |
| `corpus/SOURCES.md` (+3 rows S444–S446), `corpus/knowledge/hreflang-declaration.md`, `corpus/README.md`, `corpus/lessons/round-76.md` | L1 landing from the wave's `blocks-*.md` (the ScribeKnowledge item forbids that seat from writing `corpus/`; the knowledge file opens with the same `source:` line as its first fenced block) |

**Post-instant drift (22:15Z).** While this report was being written the L1 applied the round-76 claim
table to `SCORECARD.md` (`git diff --stat` = 32 insertions, pure append including the five correction
rows) and left `corpus/lessons/round-76.md` untracked. Both are landing writes, not seat writes; they
postdate the status block above and must not be read as a scope breach.

Lane `.ufo/state/` does not exist; `.ufo/watchdog.log` is absent in the lane.

`git -C /home/vgpnk/Projects/shokunin status --porcelain` (fleet root) at the instant:

```
 M .scratch/goal-20261103-hyaku-run15.md
 M .scratch/run15-state.json
?? .scratch/run13-state.json
?? .scratch/run15-kernel.py
?? .ufo/reports/round-71/kama.md
?? after
```

| Path | mtime / size | Owner guess |
|---|---|---|
| `after` | 2026-11-03 20:05:14, 24 B (`== SCORECARD diff base-`) | pre-round stray from an earlier hyaku integrator shell; predates round open, not a wave-76 seat |
| `.ufo/reports/round-71/kama.md` | 21:53:31, 12,722 B | kama lane round-71 report (its header self-identifies); sibling seat |
| `.scratch/goal-20261103-hyaku-run15.md` (M) | 16:26:59 | hyaku inline-run goal document |
| `.scratch/run15-state.json` (M) | 21:58:09 | hyaku inline dispatcher state (host runner) |
| `.scratch/run13-state.json` (??) | 2026-10-30 16:05 | stale hyaku run-13 state |
| `.scratch/run15-kernel.py` (??) | 19:24:49 | hyaku run-15 harness kernel |

Sibling lanes (`audio`, `chousa`, `game-dev-2d`, `game-dev-3d`, `kagi`, `kaidoku`, `kama`, `kasegi`,
`kengaku`, `kotoba`, `kotodama`, `kumitate`, `lore`, `mado`, `mori`, `revenger`, `souji`, `tabi`,
`tameshi`, `tsukuroi`): `git status --porcelain | grep -iE 'kake|round-76'` → zero hits. Non-git fleet
dirs (`scripts/`, `tools/`, `templates/`, `research/`, `kumitate-shokinin/`) hold no file newer than
21:43.

---

## 2. Secrets

Every file under `.ufo/waves/round-76/` (2.4 MB, all extensions) scanned for: `op://` refs, `ghp_`,
`github_pat_`, `AKIA…`, PEM private-key markers, `Bearer <token>`, `Cookie:`/`Set-Cookie:`,
`session_token`/`csrf_token` assignments, and URLs carrying `?token=|key=|sig=|auth=|code=|session=`.

**Zero matches.** No operator credential, cookie or session material is present; curl ran without a cookie
jar or headers, so the retained bodies carry none by construction.

One credential-shaped hit, class + location only (value not copied):

| File:line | Class | Count | Assessment |
|---|---|---|---|
| `.ufo/waves/round-76/w1/ScoutHreflangSources/google-localized-versions.html:5104` | Google API key (`AIza…`, in a devsite JS config blob) | 3 | Third-party and public — Google's own docs-page key, not an operator secret, not usable against an operator property. It is inside the raw bytes the source item required to retain. Risk: low. If receipts must be clean, mask it in a future retained copy and record that the retained sha is then not the fetched sha (the page is already not byte-stable). |

A high-entropy heuristic (32+ mixed-case-and-digit alphanumerics, hex excluded) returned only these three
plus one long path fragment in the historical `w1/ReviewerC1/base_SCORECARD.md` copy.

---

## 3. Host-absolute paths

Counts over `.ufo/waves/round-76/` at the instant (`grep -rF` occurrences / distinct files):

| Class | Occurrences | Files | Where | Risk |
|---|---|---|---|---|
| `/fast/scratch` | 304 | 151 | seat receipts and drivers that record their scratch work dirs (`ReviewerC1/*/run.json`, `ReviewerC2/receipts/*`, `MutationTesterGates/receipts/*`, `ExecAuditRealRun/receipts/*`, `ScoutHreflangSources/refetch-record.txt`, `ExecQuoteRepair/receipts/*`), the L1 generator/dispatch, and report prose | **Dead citation at closure**: every seat must `rm -rf` its scratch. The observed outputs and most fixture trees are copied into the wave dir, so evidence survives; the recorded `--root`/`--work` paths do not. Counter re-runs against ReviewerC1's copied fixtures are impossible because the copies carry no `.git`. |
| `/tmp` | 153 | 85 | 46 in two copies of pre-existing repo files (`ReviewerC1/base_SCORECARD.md` 34, `base_QUALITY.md` 12); the rest are `TMPDIR=/fast/scratch/.../tmp` command lines in receipts, instruction prose, and one report line | No delivered tool contains a `/tmp` literal: `grep -n '/tmp'` is empty for `w1/ExecAuditTool/hreflang_audit.py` and for both copies of `doc_quote_truth.py`. The scratch-discipline rule holds for every tool that exists. |
| `/home/<user>` | 248 (`/home/` 249, the extra being the `/home/<user>` placeholder in the seat item text) | 132 | absolute lane paths in receipts/reports | These resolve at closure because the lane persists. None points at another user's tree or a sibling lane. |

The new `scripts/` tool (`scripts/doc_quote_truth.py`) is clean of both `/tmp` and network imports.

---

## 4. Operator-owned surfaces

### 4.1 Endpoints contacted anywhere in the wave

| Endpoint | Class | Observed | Evidence |
|---|---|---|---|
| `https://developers.google.com/search/docs/specialty/international/localized-versions` | public documentation | GET 200, 0 redirects, 199,246 B, curl exit 0; refetch 199,242 B (dynamic page) | `w1/ScoutHreflangSources.md` §1; `ScoutHreflangSources/refetch-record.txt` |
| `https://html.spec.whatwg.org/multipage/links.html` | public standard | GET 200, 381,019 B, byte-identical on refetch | same |
| `https://www.rfc-editor.org/rfc/rfc5646.txt` | public standard | GET 200, 208,592 B, byte-identical on refetch | same |

I re-hashed the retained files: `12fbe2816a3643796fbe496f694c13ec895ad9533d2ba8210efe66af89dc8d7b`,
`2f21e82b78d069ee01d61aca14a7b07832a4ab58b9633db88b45983a0f14eec3`,
`5d9515f053163c80e7294a84d18217dc83471acc7caa9773da2ac40deeec8228` — all match the scout's table.
No other `curl`/`wget` invocation exists anywhere in the wave.

### 4.2 What was not touched

- No seat fetched an operator-owned property. The only property host names are **manifest identifiers**
  in `w1/ExecAuditRealRun/real-manifest.json`: `https://ds4cc.com/`, `https://ds4cc.kimi.page/`,
  `https://burnerchrome.kimi.page/`, `https://ufo-fsd.kimi.pro/`, `https://veigapunk.github.io/<project>/`,
  while every `file` field points at committed round-23 retained bytes
  (`.ufo/waves/round-23/live/<id>/page.html`). The audit tool parses with `urllib.parse` only — no
  fetch — and my run left the retained tree untouched (`find .ufo/waves/round-23/live -newermt '-2 min'`
  empty).
- `scripts/canonical_audit.py`, invoked by the real-run receipts, imports no `socket`/
  `urllib.request`/`http.client`/`requests`: offline.
- No authenticated call, form post or write against any property appears in any receipt.
- Amendment 1's population correction is true as measured: 12 dirs under `.ufo/waves/round-23/live/`,
  exactly 8 with `page.html`+`manifest.json`; the four named not-served dirs carry only
  `audit.json`+`fetch.json`. I also verified all **8/8** retained `page.html` sha256 values equal their
  `fetch.json` sha256 (the real-run seat's central claim), independently.

---

## 5. Reproducibility

### 5.1 Instruments (hash = sha256 of the measured bytes)

| Instrument | Bytes | Selftest, TMPDIR unset / set | Exit contract exercised | Revision identity |
|---|---|---|---|---|
| `c76_quote_truth.py` v1, `c9311780…` | 18,130 | `13/13` / `13/13`, rc 0 both | 0 met / 1 findings / 2 input / 64 usage — all observed | prints the **argument** truncated (`revision=HEAD`, `revision=master`, `revision=a0491fcd`) |
| `w1/ExecQuoteCounter/doc_quote_truth.py`, `e7f86d3a…` (last measured build, 49,077 B, 22:13:35) | 49,077 | `63/63` / `63/63`, rc 0 both | 1 at base, 0 at the repaired tip, 0 on green fixtures (observed) | same literal-argument print, full string when a full sha is passed |
| `scripts/doc_quote_truth.py`, `eae3ce48…` | 44,101 | `52/52` / `52/52` | — | **stale copy** of the 22:08 wave build; it measures `9` at base and `2` at the repaired tip — §5.3 F3 |
| `w1/ExecAuditTool/hreflang_audit.py` and its landed copy `scripts/hreflang_audit.py`, both `0762452f…` | 59,734 | `59/59` / `59/59`, rc 0 both, ~1.5 s | 0 clean / 1 policy / 2 input (also when both) / 64 usage; no args → 64, `--selftest` without `--work` → 64, missing manifest → 2 | prints `{version,pages,findings,counts,exit}` only — **no manifest path, digest, root or revision**; the receipt's command line is the only input identity. `tempfile.mkdtemp(dir=work)`, writes nothing outside `--work`, no `/tmp`, no network imports |

C2 matrix receipts, independently read: 71 cases, **68 decided, 68/68 correct**, 3 undecided (excluded per
kill rule 1), **4/4 constants fail** (`const-noop` and `const-report_all` 0/68 correct, `const-always_clean`
16/68, `const-empty_list` 22/68), exit 0 at tool sha `0762452f…`
(`w1/ExecAuditMatrix/receipts/matrix-run-execaudittool.txt`, `const-*.txt`). Real-input run: 8 pages,
0 findings, exit 0.

### 5.2 C1 measurement ladder (all commands `--root <tree> --base a0491fcd --rounds 75,76`)

The C1 instrument was rewritten seven times during the audit; each build measures a different
before/after pair. Same trees, same base:

| Build | Base `a0491fcd` | Repaired tip `442d36c6` | `base + wave, no repair` | `repair + wave` | Note |
|---|---|---|---|---|---|
| v1 `c9311780` | `findings=8` rc 1 | — | `findings=0 met=true` rc 0 | — | self-laundering |
| v2 `1f49514e` (41,759 B) | `7` | `0 met=true` | `0 met=true` | `0` | controls excluded by name only; seat receipts launder |
| v2 `eae3ce48` (44,101 B) | `9` | `2` rc 1 | `9` rc 1 | `2` rc 1 | D1 read as *all* measured rounds, dropping round-75 evidence |
| v2 `33162b61` (44,966 B) | `8` | `1` rc 1 | `8` rc 1 | `1` rc 1 | closing-round exclusion, but the data-extension fallback removal still dropped the round-75 digest |
| v2 `8f3eb531` (46,131 B) | **`7` rc 1** | **`0 met=true`** | **`7` rc 1** | **`0 met=true`** | matches Amendment 3 B6 / 7 F2; laundering blocked |
| v2 `302bcb9b` (47,511 B) | **`7` rc 1** | **`0 met=true`** | **`7` rc 1** | **`0 met=true`** | same numbers; selftest grew 55→57 |
| v2 `e7f86d3a` (49,077 B, last measured) | **`7` rc 1** | **`0 met=true`** | **`7` rc 1** | **`0 met=true`** | same numbers; selftest 63/63 |

Exact observed lines, final build (hash verified unchanged before and after the runs):

```
$ python3 -B doc_quote_truth.py --root <base-clone> --revision a0491fcd --base a0491fcd --rounds 75,76
C1v2 revision=a0491fcd rows=16 receipt_files=7923 spans=25 exempted=0 corrections=0 findings=7 met=false
  [the seven findings of Amendment 3 B6]
$ python3 -B doc_quote_truth.py --root <lane> --revision 442d36c6 --base a0491fcd --rounds 75,76
C1v2 revision=442d36c6 rows=23 receipt_files=7925 spans=41 exempted=7 corrections=7 findings=0 met=true
  missing corpus/lessons/round-76.md
$ # base tree + the full round-76 wave tree, no repair
C1v2 revision=HEAD rows=16 receipt_files=7926 spans=25 exempted=0 corrections=0 findings=7 met=false
$ # repaired tip + the full round-76 wave tree
C1v2 revision=HEAD rows=23 receipt_files=7926 spans=41 exempted=7 corrections=7 findings=0 met=true
```

### 5.3 Findings

**F1 (critical, resolved in the final build) — C1's before-state self-laundered; Amendments 5 and 7 close
it, and the amended numbers now hold.**

- *Laundering, proven on v1 and the 22:05 build.* v1: base tree + only
  `.ufo/waves/round-76/controls/base-c1-quote-truth.txt` → `findings=0 met=true` rc 0; base tree + only
  `w1/ExecQuoteRepair/receipts/01-base-run.txt` → the same; lane HEAD at the time →
  `corrections=0 findings=0`. The counter prints each defective span as `findings[].detail`, so a committed
  copy of its own output satisfied T1 for every defect. Corroborated inside the wave by
  `w1/ExecQuoteRepair.md:186-198` (with `receipts/09-launder-probe-hardened.txt`) and
  `w1/ScribeKnowledge.md:258-269`.
- *Closed by terms.* Amendment 5 D1 (the closing round's seat tree is never a receipt) + D2 (diagnostic
  lines `^\s*(T1|T2|T4|A1)\s+\S+:\d+\s` stripped from every receipt), narrowed by Amendment 7 F1 to the
  **newest** measured round. Verified on the last three builds (`8f3eb531`, `302bcb9b`, `e7f86d3a`):
  base + full wave tree with no repair = `7 met=false` (not 0), repair + wave = `0 met=true`.
- *Residual bookkeeping, not a predicate defect.* `controls/base-c1-quote-truth-v2.txt` still records the
  intermediate `receipt_files=7724 … findings=9` produced by the `eae3ce48` build; it must be re-cut
  against the final build (base 7) or the registry row will cite a contradicting number (§5.3 F5).
- *Tie the claim to a build.* The instrument changed seven times in 25 minutes and four of those
  builds printed a different base count (`8, 7, 9, 8, 7, 7, 7`); the last three builds agree on `7`/`0`,
  so the claim is stable only if the landing names the hash. The registry row and the lesson must name
  `e7f86d3a…` (or whatever build is final at the copy step); the hash is what makes the claim checkable.

**F2 (high) — no measurement is tied to a commit.** The counter prints the *argument* it was given
(`revision=master`, `revision=HEAD`, `revision=a0491fcd` — 8 chars). Every frozen base receipt says
`revision=master`, so the receipt alone cannot re-anchor its tree. Smallest fix: print
`git rev-parse <rev>` beside the argument, or reject symbolic revisions.

**F3 (high) — the landed `scripts/` instrument is stale.** `scripts/doc_quote_truth.py` is
`eae3ce48…` (44,101 B), while the wave-dir build is `e7f86d3a…` (49,077 B). The landed copy measures
`findings=9` at base and `findings=2` at the repaired tip — i.e. it reports C1 **red on the landed
after-state**, while the final wave build reports `7` and `0`. The L1 must re-copy after the instrument
freezes and name the final hash in the registry row; the wave build must not change again after that copy.

**F4 (medium, reduced) — the selftest crash was real and is fixed in the final build.** The 22:01 build
(34,685 B) and the 22:05 build both aborted before printing a tally:

```
$ python3 -B doc_quote_truth.py --selftest --work <dir>
RuntimeError: git -C …/green_commit_citation … commit -q --no-verify -m fixture 2 failed:
```

Cause: the fixture helper was invoked twice over byte-identical payloads, so the second `git add -A` had
nothing to stage and `git commit` exited 1 with "nothing to commit, working tree clean" on stdout (the
raised message's stderr is empty). Last measured build `e7f86d3a…` passes `63/63` in both TMPDIR modes; the crash
history is why Amendment 5 D5 exists. Nothing further is owed except recording the final tally in the
report the seat has not yet written.

**F5 (medium, mostly resolved) — an amendment briefly cited a report that did not exist, and one receipt
is stale.** When `amendment-5.md` first appeared it opened "two independent seats, same finding:
`w1/MutationTesterGates.md` and `w1/ScribeKnowledge.md` both measured…", while `MutationTesterGates.md`
was absent; the report has since landed, and amendment 5 is now committed as `152bffd5`. The residue is
`controls/base-c1-quote-truth-v2.txt`, still untracked and still recording the intermediate
`findings=9` from the `eae3ce48` build, which no longer matches the delivered instrument's `7`. It must be
re-cut and committed, or it will contradict the registry row and the lesson.

**F6 (medium, reduced) — seat-minted receipts.** A fixture with a claim row `| S | \`minted=1\` |` plus
`w1/SomeSeat/receipts/mint.txt` containing `minted=1` produced `met=true` rc 0 on v1. Under the final
terms the closing round's `w1/` is never a receipt, so this path is closed for the rounds being measured;
minting into an *older* round's receipt directory would still work but requires committing to a closed
round's tree, which the append-only gates watch. No further action beyond the existing gates.

**F7 (low) — stray artifacts.** `.ufo/waves/round-76/__pycache__/c76_quote_truth.cpython-314.pyc` is
gitignored (`.gitignore:2`) and will not be committed. `w1/swarm-registry.json` (mode 600, 30,795 B) will
be committed unless removed; the counter excludes it from receipts.

**F8 (low) — commands that cannot be re-run after scratch cleanup.** ReviewerC1's `run.json` files record
`--root /fast/scratch/…/fixtures/<case>`; the fixture trees are copied into `w1/ReviewerC1/<case>/` but
without `.git`, so the counter cannot be re-run on them once scratch is deleted. The outputs survive; the
commands do not. ReviewerC2 and MutationTesterGates receipts have the same shape (297 `/fast/scratch`
occurrences in 147 files, §3).

**F9 (low) — the only credential-shaped string is third-party.** See §2: Google's public docs key, three
occurrences on one line inside bytes the source item required to retain.

**F10 (info) — L1 landing writes are in scope and named.** `scripts/doc_quote_truth.py` (copy),
`corpus/SOURCES.md` (+S444–S446), `corpus/knowledge/hreflang-declaration.md` and `corpus/README.md` are the
L1's, not a seat breach (§1.2); the first is already stale (F3), the rest are `.md` files and outside the
C1 receipt universe.

---

## 6. What this audit did not cover

- C2 case-by-case matrix correctness and the undecided residue (ReviewerC2's remit). I only verified the
  matrix receipt's own totals, the tool's offline/scratch/exit behaviour, the four constants' failure, and
  the real-input run.
- The content of the C1 correction rows (whether each quotes a whole receipt line and names the span) —
  ReviewerC1 / CriticClaims's remit. I verified the measurement that consumes them, and that the
  measurement is no longer satisfiable without them at the delivered build.
- The one seat whose report was unwritten at the cutoff: `ExecQuoteCounter` (§7). Its receipts were
  audited; its prose was not.

## 7. Seats still running at the cutoff

`ExecQuoteCounter` (instrument and receipts delivered, report absent). All other seats' reports are in
the wave dir, including `MutationTesterGates.md` and `ReviewerC2.md`.

## 8. Re-run recipe (for the L1 at closure)

```sh
# scope
git -C /home/vgpnk/Projects/shokunin/kake-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin status --porcelain
# secrets and paths
grep -rnE 'op://|ghp_[A-Za-z0-9]{20}|github_pat_|AKIA[0-9A-Z]{16}|-----BEGIN|Bearer [A-Za-z0-9._-]{12}' .ufo/waves/round-76/
grep -rnF '/tmp' .ufo/waves/round-76/ | cut -d: -f1 | sort | uniq -c
grep -rnF '/fast/scratch' .ufo/waves/round-76/ | cut -d: -f1 | sort | uniq -c
# instruments (both must print a tally and exit 0; re-copy scripts/doc_quote_truth.py first — F3)
env -u TMPDIR python3 -B scripts/doc_quote_truth.py --selftest --work "$S/dq-u"
TMPDIR=$S/tmp python3 -B scripts/doc_quote_truth.py --selftest --work "$S/dq-s"
env -u TMPDIR python3 -B .ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py --selftest --work "$S/hl-u"
TMPDIR=$S/tmp python3 -B .ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py --selftest --work "$S/hl-s"
# C1 before/after at the landed tip (final build: 7 at base, 0 at the repaired tip; stale copy gives 9/2)
python3 -B scripts/doc_quote_truth.py --root . --revision "$(git rev-parse HEAD)" \
  --base a0491fcd --rounds 75,76
```

*Scratch `/fast/scratch/hyaku/kake-r76/SentinelScope` was removed after this file was written; only this
wave-dir report survives, by design.*
