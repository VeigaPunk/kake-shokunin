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

After the 2026-11-03 pass the same file holds 4 `absent` and 170 `restored` entries: the four
remaining absences are the three tokens named above, and every flipped entry carries the prior
observation under `history`.
