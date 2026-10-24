# AttackSourcesRows — registry-row census attack (S133 / S134)

Seat: `kake-r45.AttackSourcesRows`, round-45 wave 2 (falsify). Lane: kake-shokunin.
Target: `corpus/SOURCES.md` rows S133/S134 and the CORPUS.md manual census over the registry.
Measured file: `corpus/SOURCES.md` at sha256 `646c7c02263cd2b2a8dab8597ef9fe4fa9f764540393c95f57729cbff8111876`
(worktree bytes, 2026-10-24T04:01Z). Read-only over the lane; scratch at
`/fast/scratch/hyaku/kake-r45/AttackSourcesRows/`; no tool installed.

**Named attack verdict: PASS on every assigned checklist item** — the frozen census reproduces
134 rows / 0 malformed / A=111 B=6 C=17 / mined=104 queued=8 rejected=22 / no duplicate ids / no enum
violations / no missing `used-by` path, both target rows carry 11 cells, tier A vs C matches the
scope cell, and S134's `teaches` opens `REJECTED:` with a `flip:`. Four row-quality defects were found
*outside* the checklist: **1 MEDIUM (freshness pin), 1 LOW (anchor under-coverage), 2 informational.**

LSP note: no `lsp` device is exposed to this seat, and the target is a Markdown data table, not a
code file any language server indexes; the CORPUS.md census is itself the canonical instrument for
this artifact (awk/`grep -cE`), so shell measurement is the specified tool here, not a fallback
around a semantic check.

## 1. Census — frozen commands, run verbatim from the lane root

Commands are copied unchanged from `/home/vgpnk/Projects/shokunin/CORPUS.md` §Census (lines 131-149).

```sh
cd /home/vgpnk/Projects/shokunin/kake-shokunin
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
```

Verbatim output (all nine checks; empty lines are the empty-set checks):

```text
row count (grep -cE) 134
malformed rows (NF!=13) 0
tier histogram: A=111 B=6 C=17
status histogram: mined=104 queued=8 rejected=22
duplicate ids:            <no output>
enum violations:          <no output>
missing used-by (mined):  <no output>
```

Histogram sums equal the row count (111+6+17 = 134; 104+8+22 = 134), so no row hides in an
unmatched bucket.

## 2. Deterministic extensions (not frozen; each one independently checkable)

```sh
awk -F'|' 'NR==141||NR==142{print NR": NF="NF}' corpus/SOURCES.md
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort > ids.txt; wc -l < ids.txt; seq -f 'S%03g' 1 $(wc -l < ids.txt) | diff - ids.txt
grep -nE '^ {1,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md | wc -l        # indented rows the frozen regex would miss
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {r=$11; gsub(/^[[:space:]]+|[[:space:]]+$/,"",r); n[r]++} END{for(k in n) printf "%s=%d\n", k, n[k]}' corpus/SOURCES.md | sort
awk -F'|' 'NR==141||NR==142{for(i=2;i<=12;i++){c=$i; gsub(/^[[:space:]]+|[[:space:]]+$/,"",c); if(c=="") print NR": empty cell "i}}' corpus/SOURCES.md
awk -F'|' 'NR==141||NR==142{t=$8; gsub(/^[[:space:]]+|[[:space:]]+$/,"",t); printf "%s opens_REJECTED=%s has_flip=%s\n", $2, (t ~ /^REJECTED:/)?"YES":"NO", (t ~ /flip:/)?"YES":"NO"}' corpus/SOURCES.md
```

```text
141: NF=13
142: NF=13
134
sequence S001..S134 contiguous          <- ids.txt diffs empty against seq -f 'S%03g' 1 134
0                                        <- zero rows indented 1-3 spaces: frozen and maintained parsers agree on the row set
180d=2
365d=30
90d=80
on-release=18
on-use=4                                 <- recheck enum in use; sum 134; S133=on-release and S134=180d are both attested values
S133 opens_REJECTED=NO has_flip=NO       <- correct: S133 is mined, not rejected
S134 opens_REJECTED=YES has_flip=YES     <- the required rejected-row shape, in the teaches column ($8)
```

No empty cell in either row; `used-by` for S133 = `corpus/knowledge/receipt-integrity.md,
corpus/lessons/round-45.md`, for S134 = `corpus/lessons/round-45.md`; both files exist
(`ls -la` 9533 B / 7269 B) and both cite the row (`grep -n 'S13[34]'` hits
`receipt-integrity.md:1,44` and `lessons/round-45.md:5,6,12,13`). Tier/kind pairs: S133
`docs`+`A`+`mined`, S134 `community`+`C`+`rejected` — both inside the enum and both consistent with
their scope cells ("child-process exit-status semantics used by receipt gates" vs "signal-number
meaning … (illustrative only; not the receipt-gate scope)").

## 3. Artifact re-derivation (the rows' hashes and quotes)

```sh
sha256sum .ufo/waves/round-45/sources/*
```

```text
702954fd1946cfa2e3895804f48c850acd25a47523a780e1599e7851716ffcd1  so-answer.json      (723 B)
b3fa82dbdb49e626204b635e5c7ca1399dc4603ff07f6e65276de52f49afaae0  so-question.json   (2857 B)
eceda6f6363491ad1d0bf2aeaed06c3c37605f502aecdb36f7326ed1e5bdf0dd  subprocess.html   (208624 B)
```

All three digests and byte counts are exactly the elided pins in the two rows
(`b3fa82db…49afaae0`, `702954fd…716ffcd1`, `eceda6f6…e5bdf0dd`, 2,857 / 723 / 208,624). Quote
fidelity, from the retained bytes with markup stripped and whitespace normalized:

```text
S133 lesson quote "A negative value -N indicates that the child was terminated by signal N (POSIX only).": n=2   (Popen.returncode p3 + CompletedProcess.returncode p1)
S133 p2 "A None value indicates that the process hadn’t yet terminated at the time of the last method call.": n=1
S134 lesson quote "A negative return code usually means that the process was terminated by a signal.": n=1  (answer body, single paragraph)
answer owner display_name = 'sth' | user_id 56338 | accepted = True | answer_id = 24139472
Q question_id = 24139389 | title = 'Unable to find out what return code of -11 means' | accepted_answer_id = 24139472 | answer_count = 1
```

The anchor's paragraph numbering is exact: p1 "The child return code. Initially None…", p2 the
None-while-running sentence, p3 the `-N` sentence — "paragraph 2 = None-while-running, paragraph 3 =
negative -N signal" is literally true of the retained bytes. The API JSON is a real
`{items:[…],quota_*}` response whose only item is question 24139389, and the answer body reads
`Return code -11 means "segmentation fault". A negative return code usually means that the process
was terminated by a signal. Return code -11 means it was signal 11, which is SIGSEGV.` — so S134's
rejection reason ("durable point already carried by S133; the 11→SIGSEGV mapping is not made by the
opened primary") is substantiated by the bytes, and the flip is satisfiable and observable (a tier-A
POSIX/`signal` source naming signal 11).

Live HTTP re-check, 2026-10-24T04:00Z, default curl UA:

```text
docs.python.org/3/library/subprocess.html : HTTP 200, 208624 B   (title "Python 3.15.1 documentation")
stackoverflow.com/questions/24139389/...   : HTTP 403,  5659 B    <- the row's "direct HTML GET … answered HTTP 403" claim reproduces
```

## 4. Findings

### F1 — MEDIUM (freshness) — S133's whole-page sha256 is not a reproducible pin

`corpus/SOURCES.md:141` pins the source as `sha256 eceda6f6…e5bdf0dd` over the raw response. That
response embeds a per-build footer. A re-fetch **seventeen minutes after the wave-1 fetch** returns
the identical 208,624 bytes and a **different digest**:

```text
$ curl -sS -o live-plain.html -w 'plain fetch: %{http_code} %{size_download}B\n' https://docs.python.org/3/library/subprocess.html
plain fetch: 200 208624B
$ sha256sum live-plain.html
b4c58392796b5dedeae51c96f051a6f265f196f55041e56072c2c80f43d19355  live-plain.html
$ cmp -l .ufo/waves/round-45/sources/subprocess.html live-plain.html | wc -l
3
$ diff -u .ufo/waves/round-45/sources/subprocess.html live-plain.html
-      Last updated on Oct 24, 2026 (00:13 UTC).
+      Last updated on Oct 24, 2026 (03:37 UTC).
```

Three bytes differ; the entire rest of the page (every paragraph of `Popen.returncode`,
`CompletedProcess.returncode`, the 15-word quoted sentence) is unchanged, and the markup-stripped
text hashes equal on both copies:

```text
markup-stripped text equal after masking footer: True
retained text sha256: 167c39e5ae8000b27a93da5a6ab11844a21bd25a7b4ae319a279c8155d1d1daf
live     text sha256: 167c39e5ae8000b27a93da5a6ab11844a21bd25a7b4ae319a279c8155d1d1daf
raw retained sha256: eceda6f6363491ad1d0bf2aeaed06c3c37605f502aecdb36f7326ed1e5bdf0dd
raw live     sha256: b4c58392796b5dedeae51c96f051a6f265f196f55041e56072c2c80f43d19355
```

Why it is a registry defect rather than a fact of the web: the row's own corpus already solved this
class for S095 ("the body hash varies per fetch (analytics script), the visible-text hash does not",
`corpus/SOURCES.md` notes tail), and S133's `recheck` is `on-release` — an operative pin that will
mismatch on *every* recheck while the content is provably unchanged, inviting a false "source
changed" verdict or a silent "close enough". The URL is also the floating `/3/` alias while the
claim is version-bound in prose only, so on the 3.16 release the pinned identity is un-recheckable
from the cited URL. Minimal repair: add the visible-text digest (167c39e5…) or the section digest
next to the raw digest, and cite `https://docs.python.org/3.15/library/subprocess.html`.
Corroboration, same observation independently: `w2/ReopenS133.md:11`, `w2/ReopenS134.md:16,64,81-82`.
Not double-counted here as a content falsification: the quoted sentence itself survives.

### F2 — LOW — the S133 anchor is narrower than its `teaches`; the "0 success" half is unanchored

`teaches` asserts `0 success, a negative value a signal termination, None not-yet-terminated — so only
an explicit 0 or 1 can carry witness credit`, but `anchor` names only "§Popen Objects →
Popen.returncode, paragraphs 2-3". Those two paragraphs say nothing about 0:

```text
'only an explicit 0 or 1': n=0          (in the retained page)
'Exit status of the child process. Typically, an exit status of 0 indicates that it ran successfully.': n=1
  section context: … class subprocess. CompletedProcess ¶ … returncode ¶ Exit status of the child process. Typica…
```

So the 0-is-success half lives in `CompletedProcess.returncode` paragraph 1 — a **different section**
from the anchor — and that sentence is hedged ("Typically, an exit status of 0 …"), a hedge the row
drops. The `{0,1}` admissibility rule is lane policy (round-44 counter contract), not a doc
sentence; it is presented as a consequence ("so …"). No false claim, but a rechecker who opens only
the named paragraphs cannot confirm the row's first clause. Repair: extend the anchor to
`§Using the subprocess Module → CompletedProcess.returncode, paragraph 1` and keep "Typically".
The knowledge entry already cites both sections (`receipt-integrity.md:1`), so the row is the only
place the anchor is short.

### F3 — LOW (latent) — S056's `used-by` is an ASCII hyphen, which the frozen census reads as a path

The frozen check exempts only the em dash (`p!="—"`). Scanning **all** statuses instead of `mined`
surfaces one hit, a queued row whose placeholder is a plain `-`:

```text
missing:  S056  -> -
```

`corpus/SOURCES.md:64`, cell 12 is `-` (U+002D), not `—` (U+2014). Today the frozen census never
sees it because S056 is `queued`; the moment S056 is mined the canonical command prints a spurious
`missing: -`. Cheap fix: make the placeholder `—` like every other empty `used-by`, or exempt `-`.

### F4 — INFORMATIONAL — the Gate log's third row has no retained bytes in the lane

`corpus/lessons/round-45.md:14` (the candidate row, SO answer 5631819) quotes
"A negative value -N indicates that the child was terminated by signal N (Unix only)." and records
access "via the Stack Exchange API", but `.ufo/waves/round-45/sources/` holds only
`so-answer.json`, `so-question.json`, `subprocess.html`: the 5631819 response lived in
`/fast/scratch/…` and was not retained, and the row carries no digest. The quote is traceable to a
wave-1 seat's scratch transcript (`.ufo/waves/round-45/w1/ScribeLessonMistakes.md:275-284`), so it is
not fabricated — but it is the one quoted line in this round's Gate log that cannot be re-derived
from lane bytes. No decision rests on it (candidate only, no id), so this is hygiene, not a defect
of either registry row.

## 5. Residual risk and verification gaps

- **Not re-run:** the claim that the wave-1 fetch saw HTTP 200 at fetch time — the retained artifact
  is self-consistent (footer build `00:13 UTC`, file mtime 03:42 UTC) and a live GET is 200, but the
  historical status code is not observable from bytes.
- **Not observable:** whether the S133/S134 write touched any other registry row. No pre-write copy
  of `SOURCES.md` exists in the lane; the wave-1 census snapshot
  (`w1/ScribeLessonMistakes.md:292-297`: "132 rows, malformed=0, tail S130/S131/S132") is consistent
  with a pure append of exactly two rows, but it is a count, not a byte diff.
- **`cmp` byte-count coincidence:** the retained and live pages are both 208,624 B while differing
  in 3 bytes — the footer `HH:MM` swap is length-preserving. A size-only recheck (a plausible
  "freshness sweep" shortcut) would wrongly call the pin intact; only a digest catches F1.
- **Tier judgment:** S133 tier A rests on "vendor's own documentation of its own runtime", which the
  registry already applies to S026/S100/S123; I did not re-litigate the tier rubric itself.
- **Scope:** the candidate row (F4) and the knowledge entry's own section attribution (already filed
  as `w2/AttackKnowledgeEntry.md` F3) are outside the two rows; I did not re-derive them here.

Files written by this seat: `.ufo/waves/round-45/w2/AttackSourcesRows.md` (this report). Scratch only:
`/fast/scratch/hyaku/kake-r45/AttackSourcesRows/{census.txt,artifacts.txt,so.txt,returncode.txt,
quotecheck.txt,quotecheck2.txt,anchor.txt,textstable.txt,ids.txt,live.html,live-plain.html}`.
