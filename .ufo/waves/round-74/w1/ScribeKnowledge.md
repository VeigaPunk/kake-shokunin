# ScribeKnowledge — kake round 74, wave w1, attempt 1

Seat: leaf scribe, no dispatch. Lane `/home/vgpnk/Projects/shokunin/kake-shokunin` read-only.
Measured revision: `ced2878a1e77f57afb4ee3baebf1021e5130399b` (the contract's base). Every
lane fact below was read with `git show <rev>:<path>` or from the frozen wave directory; no
production file was edited, staged or committed, and no git/jj mutation was run anywhere.

Axes named: (a) provenance fidelity — every claim carries a located quote or a receipt file;
(b) evidence locality — quotes come from the retained 2026-11-03 bytes, not from memory;
(c) scope discipline — no live-property claim, no claim about another host;
(d) integration fit — README/SOURCES rows match the committed table shapes and the sweep's
fail-closed binding.

Deliverables are drafted, not applied. Nothing below is an edit instruction to the lane.

---

## (1) Draft — `corpus/knowledge/sidecar-reobservation.md`

````markdown
source: S441, S442 — Python documentation: os.path.exists (https://docs.python.org/3/library/os.path.html#os.path.exists) and os.stat (https://docs.python.org/3/library/os.html#os.stat); rows in `corpus/SOURCES.md`, retained bytes at `.ufo/waves/round-74/sources/python-os-path.txt` and `.ufo/waves/round-74/sources/python-os-stat.txt`
verified-at: 2026-11-03
recheck: 90d
ground: freshness — whether the local-path notes in `corpus/knowledge/freshness-sidecar.json` still describe the host that reads them
scope: one sidecar file and one probe; this entry says nothing about any published site, deploy or remote host

# Re-observing a local-path absence note

## What the sidecar records

`corpus/knowledge/freshness-sidecar.json` (schema `kake-paths-sidecar-v1`) holds one
`entries` array. Each entry binds a note to one cited line, never to the document:

- `file` and `line` — the citing line, in `SKILL.md` or a `corpus/**` markdown file;
- `lineSha256` — the sha256 of that line's current text;
- `token` — the cited path, in canonical home form (a leading tilde, then a slash). The
  sweep normalises a cite's absolute home prefix to that form before matching, and rejects
  an entry whose own token is spelled any other way;
- `kind` — `absent` or `restored`;
- `date` and `note` — when and how the observation was made.

The binding points at the citing line because the annotation is an erratum attached to a
line whose bytes must not change (QUALITY's round-20 ruling, restated in
`corpus/knowledge/freshness-sweep.md`). That is what lets a flip rewrite the note without
touching the document that names the path. `scripts/freshness-sweep.mjs`
(`loadPathSidecar`) validates the binding and fails closed: the file must be `SKILL.md` or
a `corpus/**/*.md` path, the line's sha256 must match, the line must itself carry the token, an
`absent` note must carry absence vocabulary and the phrase "historical record, not an
executable instruction", and a `restored` note must carry none of that vocabulary. A
violation raises `paths sidecar binding invalid: <file>:<line>` and the sweep exits 2.

At the round-74 base revision the array holds 174 entries: 148 `absent` and 26
`restored`. Thirty carry the date 2026-10-21 (the 26 restored plus 4 absent); 144 carry
2026-10-31, all `absent`.

## An absence note is a dated observation on one host

A note records a verdict and, at best, the probe that produced it: all 30 notes of the
2026-10-21 batch carry a `test -e` probe and its exit code (exit 1 for the four absences,
exit 0 for the twenty-six restorations), while the 144 notes written on 2026-10-31 carry no
instrument at all — only a host narrative, "absent on this host — an old-host home path; the
Windows host migration removed every former home tree, so this target does not exist on the
current machine". Either way the note is an event: one machine, one moment, one cause
inferred. It does not record which machine, which mount, which account, or which of several
causes produced the negative — removal, a different home directory, an unmounted volume, a
name that never existed there. Read as a standing fact about "the path", it becomes false as
soon as the corpus is read somewhere else.

That is what the round-74 census found. All 144 contradicted notes carry 2026-10-31 and all
144 say "on this host" in their own prose, attributing the absence to a host migration;
none of them has a field that names the host it observed. A reader on this host therefore
cannot tell an observation of this machine from an observation of the machine before it.
The four notes that still hold were written 2026-10-21, a different batch.

The repair is not to delete the old notes — they are evidence of what was seen, and the
citing lines must stay byte-identical — but to date a new observation beside them.

## The three states a `stat` probe can report

| probe outcome | classification |
|---|---|
| `os.stat(token)` returns a `stat_result` | `present` |
| `FileNotFoundError` or `NotADirectoryError` | `absent` |
| any other `OSError` (`PermissionError`, `ELOOP`, `EIO`, and the rest) | `unevaluable` |

`unevaluable` is a third state, not an error to be retried away: it says the probe could
not see, so the entry keeps whatever it said before. The repair tool refuses the whole
write when any token lands there, and the counter reports the counts and exits 2 rather
than 0.

## Why `exists()` alone cannot carry the note

A boolean existence probe answers one bit. The documentation of `os.path.exists` gives two
reasons that bit is not the classification above (retained text
`.ufo/waves/round-74/sources/python-os-path.txt`, lines 325-329):

> Return True if path refers to an existing path or an open file descriptor.  Returns False for broken symbolic links.

> On some platforms, this function may return False if permission is not granted to execute os.stat() on the requested file, even if the path physically exists.

The second sentence is the false negative: a permission failure and a genuinely unrelated
path produce the same `False`. A note built on that bit cannot distinguish "not there" from
"not tellable here", which is exactly the `absent` / `unevaluable` distinction the sidecar
needs. The first sentence shows a second conflation: a broken link is reported as absent,
although a directory entry exists.

`os.stat` is where the distinction lives (retained text
`.ufo/waves/round-74/sources/python-os-stat.txt`, lines 3519-3526 and lines 237-239):

> Get the status of a file or a file descriptor. Perform the equivalent of a stat() system call on the given path.

> All functions in this module raise OSError (or subclasses thereof) in the case of invalid or inaccessible file names and paths, or other arguments that have the correct type, but are not accepted by the operating system.

Because failure arrives as an exception type rather than a boolean, `FileNotFoundError` and
`NotADirectoryError` can be separated from the remaining `OSError` failures that a boolean
probe would hide. The same entry also fixes what a success means (lines 3525-3526):

> This function normally follows symlinks; to stat a symlink add the argument follow_symlinks=False, or use lstat().

So `absent` in this sidecar means "no resolvable target", not "no directory entry": a
broken link lands in `absent`, and a link to a live target lands in `present`. The
classification describes the token's resolution on the measuring host, nothing more.

## The 2026-11-03 census

Measured at revision `ced2878a1e77f57afb4ee3baebf1021e5130399b` on this host
(`linux-x86_64`), by `os.stat` over each entry's token:

- 174 entries, 148 `absent`, 26 `restored`;
- 144 of the 148 absent entries name a token that resolves here — 144 contradictions;
- 4 absent entries still name a non-resolving token, over 3 distinct tokens;
- all 26 restored entries resolve, and they name 4 distinct tokens between them.

The counter prints one line and exits 1 on that state:

> C2v1 revision=ced2878a1e77f57afb4ee3baebf1021e5130399b entries=174 absent=148 restored=26 absent_present=144 absent_absent=4 absent_unevaluable=0 restored_present=26 restored_absent=0 restored_unevaluable=0 contradictions=144 met=false

The round's predicate names the same quantities `absent_notes_resolving`,
`restored_notes_absent` and `unevaluable`; the counter prints them per kind
(`absent_present`, `restored_absent`, `absent_unevaluable`, `restored_unevaluable`) and
derives `contradictions = absent_present + restored_absent` and
`met = contradictions == 0 and unevaluable == 0`.

## The procedure

`scripts/sidecar_reobserve.py` re-observes every entry against the live host. It reads the
sidecar, stats each token, and never opens the file the entry cites.

- `--check` (the default) reports only and writes nothing. It prints
  `sidecar_reobserve mode=check entries=… absent=… restored=… present=… absent_present=…
  absent_absent=… restored_absent=… unevaluable=… flipped=0 wrote=false` and exits 0; any
  `unevaluable` count adds an `error=` field and exits 2.
- `--write --date YYYY-MM-DD [--host <class>]` flips every `absent` entry whose token
  resolves to `restored`, appends the superseded observation to `history`, writes the new
  note, and re-serialises the file. `--date` is required with `--write`. The default host
  class is the platform string (system name, lowercased, then a hyphen, then the machine
  type — `linux-x86_64` here); the operator may pass any class.
- `--json` emits the same fields as sorted JSON; `--selftest` runs the fixture set under
  `--work <dir>` (else `TMPDIR`); `--root` defaults to the current directory.

Refusals, all exit 2 with no file write:

- any token `unevaluable` — the whole write is refused, not just that entry;
- the sidecar resolving outside `--root`, or being a symlink (the output open also uses
  `O_NOFOLLOW`);
- a missing or malformed `--date`, a wrong schema, or a malformed `history` array;
- a would-be new note that matches the sweep's absence vocabulary (checked before any
  entry is changed, so a refusal leaves the file untouched).

The new note has the form

> 2026-11-03: re-observed on linux-x86_64; token resolves (stat ok). Prior 2026-10-31 observation retained under history. Citation corpus/lessons/round-29-verifier-spotcheck.md:190 is a historical record.

A second `--write` with no new candidate flips nothing and writes nothing (observed:
`flipped=0 wrote=false`, file sha256 unchanged), so the tool is safe to re-run.

`--check` is the read-only form to run at round open; `--write` is the repair.

## The counter

`.ufo/waves/round-74/c74_sidecar_reobserve.py` is the offline, revision-bound instrument
for the claim: it reads committed bytes with

`git show --end-of-options <rev>:corpus/knowledge/freshness-sidecar.json`

probes each token with `os.stat`, and never reads the cited
document for existence. `--root`, `--revision`, `--json`, `--selftest`; exit 0 met, 1 not
met, 2 unevaluable, 64 usage. Its `--selftest` fixtures are the six the round's contract
names (a contradicted absent entry, a stale restored entry, an unevaluable probe that must
exit 2, a restored note with absence vocabulary, a flipped entry without a preserved prior
observation, and home expansion from `HOME`). Revision-bound means at a later revision it
still compares against the base sidecar's entries for the history conjunct.

## The history array

A flipped entry keeps its superseded observation in `history`, one object per observation
with the same three keys the note had: `date`, `kind`, `note`. The array accumulates: a
second flip appends, it does not replace. The prior note is preserved as its exact string
value, so the date and the probe that produced it survive the flip; a comparison should
decode both documents first, because the serialiser's escaping rules belong to the writer,
not to the note.

The sweep does not validate `history` — it validates the record note — so `history` is the
audit trail, not the gate. The tool validates its shape on read (an array of objects with
three string fields) and the counter reports a missing or mismatched prior observation
independently, without letting it change the `stat` classification.

## Limits

- A present token proves that this host resolves it now. It does not prove the historical
  absence note false on the host where it was observed; the note may have been right there
  and wrong only here. The flip says the note no longer describes this host.
- Symlinks are followed, so a present token may be a link whose target sits elsewhere. That
  presence does not vouch for the byte identity of the artifact the citing line discusses.
- `unevaluable` never flips. A permission failure, a loop or an I/O error leaves the entry
  exactly as it was; the census then reports a non-zero `unevaluable` and does not claim
  met.
- `absent` means no resolvable target, not no directory entry: a broken symlink is `absent`
  (S441's broken-link sentence, S442's follow-symlinks sentence), and `lexists` would
  disagree about the same path.
- The flip changes the note only. The citing document, its `lineSha256` binding and the
  claim the line makes are not re-verified by this procedure; the sweep validates the
  binding, and a moved line is a binding failure, not a re-observation.
- The census is host- and time-relative. The numbers above describe this host on
  2026-11-03 at one revision; they are not a standing property of the corpus.
- No published property is measured or implied here. Whether any site serves, deploys or
  resolves is outside this entry.

Cross-reference: `corpus/knowledge/freshness-sweep.md` carries the instrument and the
annotation discipline; this entry adds the re-observation class, the `stat` classification
and the repair procedure, and it is the row consumer for S441 and S442.
````

---

## (2) Draft — one `corpus/README.md` coverage-map row

Table shape at base (README line 17-18): `| Area | Entry | Coverage |`. Proposed row, no
pipe inside a cell, no bare tilde token:

````markdown
| Sidecar re-observation (r74) | `knowledge/sidecar-reobservation.md` + `scripts/sidecar_reobserve.py` (S441, S442) | host-relative absence notes: the sidecar's file/line/sha256 binding, `present`/`absent`/`unevaluable` from `os.stat`, the `--check`/`--write` procedure with its `history` array, and the 2026-11-03 census (174 entries — 148 absent, 26 restored; 144 contradicted, 4 still absent over 3 tokens) |
````

Placement: after line 55 (`| Local-path freshness sidecar | ... |`), so the two sidecar rows
read together. If the L1 prefers the table tail, the row is position-independent.

---

## (3) Draft — two `corpus/SOURCES.md` registry rows (S441, S442)

Eleven columns per the frozen contract: `id | source | kind | tier | scope | anchor |
teaches | status | opened | recheck | used-by`. Ids are free at base (highest is S440).
Fields per ScoutSources' assignment: kind `docs`, tier `A`, status `mined`, opened
`2026-11-03`, recheck `90d`, used-by `corpus/knowledge/sidecar-reobservation.md`; each
`scope` states what the source does not establish; no literal or escaped pipe in any cell.

````markdown
| S441 | Python documentation: os.path.exists — https://docs.python.org/3/library/os.path.html#os.path.exists | docs | A | What a boolean existence probe can and cannot report on one host — the documented false-negative class of os.path.exists; it does not establish that an unresolved path is absent on another host, does not name a permission failure as such, and says nothing about os.stat's exception taxonomy | The os.path.exists entry; retained tag-stripped body `.ufo/waves/round-74/sources/python-os-path.txt` lines 324-329 (page fetched 2026-11-03; HTML sha256 aa392ce964293f0919e77c51a35e3007bec1c2a1c81504cde98b308e31e479a8, 90223 bytes; text sha256 f7e7bd912a7cc2fdfa3c502d5864623cf541d2ea411f77d64165a93d3985a784) | exists() returns True for an existing path or an open file descriptor and False for broken symbolic links, and on some platforms it also returns False when permission to execute os.stat() on the requested file is not granted even though the path physically exists — so a False result conflates absence with an unreportable state | mined | 2026-11-03 | 90d | corpus/knowledge/sidecar-reobservation.md |
| S442 | Python documentation: os.stat — https://docs.python.org/3/library/os.html#os.stat | docs | A | The exception-shaped status probe the re-observation class rests on — os.stat plus the module-level OSError note; it does not establish which OSError subclass a given filesystem raises for a given failure, does not promise that a successful stat identifies the artifact behind a symlink, and says nothing about any host other than the measuring one | The os.stat entry at `.ufo/waves/round-74/sources/python-os-stat.txt` lines 3519-3526 and the module-level OSError note at lines 237-239 (page fetched 2026-11-03; HTML sha256 4a8bb54c83fab12232926148f2a8cc72868ce62dffb401c547174c70273d287a, 791358 bytes; text sha256 8d1cbad5cf62b0eb101f17903c23727a6c106f120b680bf1f0204c13b574cc5f) | os.stat returns a stat_result for a path and normally follows symlinks, while every function in the module raises OSError or a subclass for invalid or inaccessible file names and paths — so FileNotFoundError and NotADirectoryError can be separated from the remaining OSError failures that a boolean probe would hide | mined | 2026-11-03 | 90d | corpus/knowledge/sidecar-reobservation.md |
````

Gate material for `corpus/lessons/round-74.md` § Gate (not a deliverable of this seat; given
so the lesson cannot misquote the retained bytes). Each quote is a raw substring of the
retained tag-stripped text with line breaks joined by one space, and each is ≤25 words:

- S441 — https://docs.python.org/3/library/os.path.html#os.path.exists — accessed
  2026-11-03 — "may return False if permission is not granted to execute os.stat() on the
  requested file, even if the path physically exists" (21 words; `.ufo/waves/round-74/
  sources/python-os-path.txt` lines 326-329, the sentence starting at the end of line 326).
- S442 — https://docs.python.org/3/library/os.html#os.stat — accessed 2026-11-03 — "All
  functions in this module raise OSError (or subclasses thereof) in the case of invalid or
  inaccessible file names and paths" (21 words; `.ufo/waves/round-74/sources/
  python-os-stat.txt` lines 237-238, the quote ending mid-line 238).
- S442 second located quote, if the lesson wants the probe's own sentence — "Get the status
  of a file or a file descriptor. Perform the equivalent of a stat() system call on the
  given path." (22 words; same file, the `os.stat()` entry at lines 3519-3526, the quoted
  sentence at lines 3520-3521).

---

## Receipts — commands run and their outcomes

All runs read committed bytes or the scribe's scratch copy; none wrote the lane. Full
outputs beside this report under `.ufo/waves/round-74/w1/ScribeKnowledge/`.

| # | command | outcome |
|---|---|---|
| 1 | `git -C <lane> show ced2878a…:corpus/knowledge/freshness-sidecar.json` (then JSON census) | exit 0; 174 entries, 148 absent, 26 restored; dates 2026-10-21 ×30, 2026-10-31 ×144; no `history` key on any base entry; key set exactly `{file,line,token,lineSha256,kind,date,note}` |
| 2 | `python3 -B /fast/scratch/hyaku/kake-r74/ScribeKnowledge/census.py` | exit 0; independent `os.stat` census reproduced the frozen control byte-for-byte |
| 3 | `diff -u controls/base-c2-sidecar.txt census-out.txt` | **exit 0**; both files sha256 `1d4fb00e184b1c27bdcd22c649083f368ef1c19fba4320c434bc0352fa283935` |
| 4 | `python3 -B …/ExecC2Counter/c74_sidecar_reobserve.py --root <lane> --revision ced2878a…` | exit **1**; the one-line summary quoted in the entry; stderr empty |
| 5 | `python3 -B …/ExecC2Tool/sidecar_reobserve.py --check --root <scratch>/demo` | exit 0; `entries=174 absent=148 restored=26 present=170 absent_present=144 absent_absent=4 restored_absent=0 unevaluable=0 flipped=0 wrote=false` |
| 6 | `… --write --date 2026-11-03 --host linux-x86_64 --root <scratch>/demo` | exit 0; `flipped=144 wrote=true`; result 170 restored / 4 absent; 144 `history` arrays; the four survivors are the 2026-10-21 absent entries |
| 7 | same `--write` again, `--date 2026-11-04` | exit 0; `flipped=0 wrote=false`; `sha256sum -c` exit 0 — file bytes unchanged |
| 8 | unevaluable fixture (`locked/x` under a mode-000 directory, `id -u` = 1000) `--check` then `--write` | both exit **2**, `unevaluable=1`, `error=one or more tokens could not be evaluated; no write`; sidecar sha256 identical before and after (no write) |
| 9 | `sha256sum .ufo/waves/round-74/sources/python-os-{path,stat}.{html,txt}` | path.html `aa392ce9…e479a8` (90,223 B), path.txt `f7e7bd91…85a784` (23,886 B), stat.html `4a8bb54c…3d287a` (791,358 B), stat.txt `8d1cbad5…74cc5f` (190,195 B) |
| 10 | base-sidecar serialisation probe: `json.dumps(parsed, indent=2)` vs `indent=2, ensure_ascii=False` | default round-trip **not** byte-identical; `ensure_ascii=False` round-trip **identical**; 432 non-ASCII bytes, all in the 144 notes that get flipped |
| 11 | `grep -c 'u2014' <scratch>/demo3/corpus/knowledge/freshness-sidecar.json` | 144 — the rewrite escapes the em dash inside the preserved `history` notes |

Reads that ground the prose: `contract.md`; `controls/base-c2-sidecar.txt` and
`controls/base-c2-sweep.txt`; both retained source text files (line numbers above); the base
sidecar; `scripts/freshness-sweep.mjs` lines 352-393 (`loadPathSidecar`, `ABSENT_RE`) and
line 136 (`PATH_RE`); `corpus/knowledge/freshness-sweep.md` line 197-199;
`corpus/README.md` lines 15-60; `corpus/SOURCES.md` lines 7-9 and 179-186, plus the id grep;
`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` §Registry rules and
§Additional corpus rules; the delivered counter and tool bytes quoted above.

Scratch: `/fast/scratch/hyaku/kake-r74/ScribeKnowledge/` — receipts copied to
`.ufo/waves/round-74/w1/ScribeKnowledge/` before the tree was removed (`rm -rf` in the
final step; the seat reports a survivor as a defect of its own). No tool was installed or
upgraded, so no install record applies.

---

## Findings

1. **The counter/control layout tension — report verbatim, no verdict.** The frozen
   contract says the counter's run at base MUST reproduce `controls/base-c2-sidecar.txt`
   exactly. The control file has 14 lines (four numeric lines, six `sample` lines, three
   `absent_token` lines); the delivered counter prints one line. Observed at base: exit 1,
   one line, stderr empty; the four numeric lines' fields and values match the control's
   first four lines, and `contradictions=144 met=false`. The counter's own seat disclosed
   the same tension. This is a contract-internal question for the canonical judge, not
   something this seat can resolve, and the knowledge entry quotes the line actually
   printed.

2. **History preservation is exact as a decoded string, not as raw bytes.**
   `json.dumps(..., indent=2)` (the tool's serialisation) escapes non-ASCII; the base file
   carries 432 non-ASCII bytes, all em dashes inside the 144 notes that get flipped. After
   the observed `--write`, the 144 `history` notes contain `\u2014` where the base file had
   the literal character. `ensure_ascii=False` round-trips the base file byte-identically
   (receipt 10), so a one-token change makes the write byte-faithful for every preserved
   note. Until then, any "history differs from the base note bytes" check must compare
   JSON-decoded strings. Handed to the tool owner / L1; not edited here.

3. **`corpus/README.md` line 55 is stale at base and the draft does not fix it.** It says
   "30 entries dated 2026-10-21"; the base file has 174 (30 dated 2026-10-21, 144 dated
   2026-10-31). My scope was one new row, so the stale cell is reported, not edited. If the
   L1 wants it corrected in the same landing, the minimal replacement coverage cell is:
   "174 entries dated 2026-10-21 and 2026-10-31, each naming a cited file and line number, a
   home-anchored path token, the line SHA-256 as of that date, kind `absent` or `restored`,
   and a note marking the citation historical; re-observation rules in
   `knowledge/sidecar-reobservation.md`." That replacement edits an existing README cell,
   which is the L1's call — this seat's scope was one new row, and it is offered only so a
   stale census line is not left standing beside a fresh one.

4. **The three still-absent tokens are deliberately not spelled in the entry or the README
   row.** The sweep scans `SKILL.md` and every `corpus/**` markdown file with `PATH_RE`; a
   new line naming one of those tokens without a bound sidecar entry would be a new
   unannotated miss and would change the `~/projects` single-drift verdict. The entry names
   them by count ("4 absent entries, 3 distinct tokens") and the sidecar itself carries the
   exact spelling. This is a prose constraint, not a precision loss: the census receipt has
   the tokens.

5. **The tool's new note satisfies the C2 note conjuncts as observed** — it contains the
   observation date, the host class, a `stat ok` present-state statement, the prior date,
   and the "historical record" marker, and it matched none of the sweep's absence
   vocabulary when generated (the tool checks this before writing). The note does not itself
   state the host-relative limit; that framing lives in the knowledge entry.

6. **ScoutSources' draft was not on disk when this report was written** (its artifact
   directory was empty). The two rows were therefore composed from the retained bytes and
   the field values fixed in ScoutSources' assignment and the contract (kind, tier, status,
   opened, recheck 90d, used-by). If the scout's wording lands differently, the teaches and
   scope cells are the reconciliation points; the anchor line numbers and hashes are
   receipts and should not change.

7. **The tool and counter bytes quoted here are wave artifacts, not landed production
   paths.** The entry names the landing paths the contract fixes
   (`scripts/sidecar_reobserve.py`, `.ufo/waves/round-74/c74_sidecar_reobserve.py`). If the
   L1 lands either elsewhere, the entry's two path mentions and the SOURCES `used-by` are
   the only places to adjust.

## Out of scope / not run

- No lane edit, no commit, no git/jj mutation of any kind (the `git show` reads and the
  scratch fixture are the only git calls; the fixture `init`-free copy used a plain `cp`).
- The sweep acceptance of the flipped file (`--selftest` 36/36, `--offline` exit ≤1, the
  binding validation on the rewritten sidecar) was **not run** by this seat: it needs the
  corpus tree and it is ReviewerC2's / the L1's gate. The entry describes the binding from
  the committed validator, not from a run of it.
- No counter `--selftest` was run here (the counter's own seat left it to the parent); the
  entry says the fixtures exist, never that they pass.
- No live-property claim: no site, deploy, DNS, crawler or remote host was touched or
  inferred.
