# ScribeSourcesRows — round-44 wave-2 source-registry supersession rows

Axes: **freshness** (source locator correctness carried in the registry) and **operability**
(the registry stays machine-validatable: census exit 0, no new E/W codes).

## Behavior

Appended exactly two rows — **S131** (supersedes S129) and **S132** (supersedes S130) — to
`/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`, immediately after the S130 row
inside the `## Registry` table (before the `## Paths` heading). The `anchor` and `teaches` cells
were copied **byte-exact** from the two tables in `corpus/lessons/round-44.md` § *Superseding
source rows* (lines 18–19), extracted programmatically from that file (regex on the lesson table
rows) rather than retyped. The `source`, `kind`, `tier` and `scope` cells mirror S129/S130
respectively (own-work, tier A); `status` = `mined`, `recheck` = `on-use`, `opened` = `2026-10-23`,
matching the file's existing column shape for the two rows they supersede. `used-by` =
`corpus/lessons/round-44.md, SCORECARD.md` — both paths exist on disk, and both documents name
S131/S132 (`corpus/lessons/round-44.md:14,18,19`; `SCORECARD.md:3536`).

**No other row was touched.** The diff is two added lines; `git diff --stat corpus/SOURCES.md`
reports `1 file changed, 2 insertions(+)`. S129 and S130 are byte-unchanged (both were captured
before the edit and the pre-edit copy is kept in scratch).

## Decisive command output

The named check, run exactly as specified from the fleet root:

```text
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
kake	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
kake	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
kake	W04	S110 duplicate url www.w3.org/TR/xml across scopes
kake	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
EXIT=0
```

Output tail (last three lines) and exit code:

```text
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake 2>&1 | tail -3; echo "EXIT=${PIPESTATUS[0]}"
kake	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
EXIT=0
```

**Before/after equivalence** — the same census run against the pre-edit registry (the file was
swapped back to the captured pre-edit copy, the census run, then the post-edit file restored):

```text
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake > census-before.txt 2>&1; echo "BEFORE_EXIT=$?"
BEFORE_EXIT=0
$ … > census-after.txt 2>&1; echo "AFTER_EXIT=$?"
AFTER_EXIT=0
$ diff census-before.txt census-after.txt; echo "DIFF_EXIT=$?"
DIFF_EXIT=0
```

The 12 `W04` lines are pre-existing (same URL across scopes, rows S033–S127) and are unchanged by
this edit; **the two new rows add no W04 and no E code**. They add no W04 because both rows are
`own-work` with local filesystem paths in the `source` cell — the census's URL extraction
(`url_of()`) only matches `https?://…`, so these rows carry no URL and cannot collide on the
duplicate-URL axis.

Byte-exactness of the copied cells (re-read from the written registry, compared against the
cells extracted from the lesson):

```text
$ python3 - <<'PY'   # cells.json = anchor/teaches extracted from corpus/lessons/round-44.md
S131 anchor exact: True | teaches exact: True | nf: 12
S132 anchor exact: True | teaches exact: True | nf: 12
PY
```

(The `nf: 12` count is the Python split on `' | '` of 11 columns plus the trailing separator; the
census's own `NF!=13` awk check reports `malformed rows: 0` for the whole registry.)

Contract census commands on the edited registry:

```text
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print "malformed rows:", n+0}' corpus/SOURCES.md
malformed rows: 0
$ awk -F'|' '…{i=$2; …; print i}' corpus/SOURCES.md | sort | uniq -d
(no output — no duplicate id)
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
132
```

Row count moved **130 → 132**.

## Gates run (and what they prove)

1. **Census validate (the item's named check): PASS.** Exit 0, `kake ok`, output identical before
   and after the edit.
2. **Byte-exactness of the mandated cells: PASS.** `anchor` and `teaches` of S131/S132 equal the
   lesson's table cells byte-for-byte.
3. **Append-only: PASS.** `git diff --stat corpus/SOURCES.md` → `1 file changed, 2 insertions(+)`;
   no other row's bytes changed.
4. **Able-to-fail, used-by axis: PASS.** Mutating the two new rows' `used-by` to a nonexistent
   path (`corpus/lessons/round-99.md`) on a scratch copy turns the census red with exactly
   `E11 S131 missing used-by corpus/lessons/round-99.md` and
   `E11 S132 missing used-by corpus/lessons/round-99.md` (exit 1). The `used-by` paths I wrote are
   therefore load-bearing, not decorative.

## Findings (reported, not fixed — outside this seat's write scope)

- **The `supersedes S0NN — ` contract is not machine-enforced for these two rows.** Mutant A
  (dropping `supersedes S129 — ` from S131's `teaches`) leaves the census **green** for S131/S132.
  The census's E04 duplicate-URL check is the only rule that reads the `supersedes` marker, and it
  is gated on a `https?://` URL in the `source` cell; `own-work` rows with local paths never
  reach it. So "the new row opens `supersedes S129 — `" is currently held only by review, not by
  the validator — the same weakness the round-37 `S011` note records for a different row family.
  I did not change the validator (`scripts/sources-census.sh` is a fleet script, out of scope).
- **Row count statements elsewhere in the lane are now one edit behind.** `corpus/lessons/round-43.md:20`
  says "registry 128 → 130 rows at this lesson's commit" and `SCORECARD.md:3275,3371` repeat
  "128 → 130 rows at the freeze commit". Those statements are scoped to the round-43 freeze
  commit and remain true of that revision; nothing in the live registry states a *current* row
  count, so no live figure is falsified by this edit. A statement of the form "the registry has N
  rows today" would now need N = 132. I did not edit those texts (append-only rule, and they are
  the L1's history).
- `corpus/knowledge/claim-count-derivation.md:1` still declares `source: S130 (…)`; under contract
  rule 2 the knowledge entry's citation of the *method* now resolves through S132, but editing an
  existing entry's `source:` line is not a `status`/`recheck`/`used-by` change and is not this
  seat's scope. Reported for the L1 to route.

## Files written

- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md` — **edited** (two rows appended:
  S131, S132; nothing else changed). sha256 after edit `d54d630cdea5d0199ce457486d7c342d21fd4008de7112ce4f5893929277ddbd`; before edit `9ec92ad6ff29ae4890f7a40955ccf78b31f9724b6c41af0eeefe56693cc7cf2f`.
- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/w2/ScribeSourcesRows.md` — this report.
- Scratch only (no repo paths): `/fast/scratch/hyaku/kake-r44/ScribeSourcesRows/` —
  `SOURCES.md.before`, `SOURCES.md.after`, `cells.json`, `census-before.txt`, `census-after.txt`,
  `mutA/`, `mutB/` (mutation fixtures).

## Addendum — independent confirmation (peer)

Peer `kake-r44.CriticExploratoryCap` (round-44 wave-2 critic) confirmed the S131/S132 rows and
the corrected locators; its bounded citation audit exits 0, recorded in its own report with a
closure addendum preserving the initial snapshot. It did not rerun my census. The registry was
re-verified after that message and is unchanged since this seat's edit:

```text
$ git diff --numstat corpus/SOURCES.md
2	0	corpus/SOURCES.md
$ sha256sum corpus/SOURCES.md
d54d630cdea5d0199ce457486d7c342d21fd4008de7112ce4f5893929277ddbd  corpus/SOURCES.md
$ sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake | tail -2; echo "EXIT=${PIPESTATUS[0]}"
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
EXIT=0
```

No tool was installed or updated for this seat. No git commit, jj, push, publish or deploy was
performed. Nothing under `.ufo/state/`, `MANIFEST.json`, `templates/`, fleet scripts, route tables
or `mcp.json` was read-modified or written.
