# ScoutAppendOnly — round-63 append-only verification

## Assignment

Verify the round-63 edits to `corpus/knowledge/response-header-expectations.md` and
`corpus/QUALITY.md` are append-only against base
`13d4519818db28cd0aa912e49020659140d7b9fa`; measured commit
`05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`.

## Verdict

PASS — both files are pure append-only. No base line was changed or deleted in
either file. All round-63 content was appended after the final base line.

## Evidence

### 1. Commit identities (repo: /home/vgpnk/Projects/shokunin/kake-shokunin)

```
$ git log --oneline -1 13d4519818db28cd0aa912e49020659140d7b9fa
13d45198 round-62 verifier spot-check (integrator, hyaku): non-author admit/reject
$ git log --oneline -1 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f
05b0d7f4 round-63: bind quote-class tool fixtures to cwd; contract freeze-note (pre-wave)
```

### 2. Zero deletions / zero modifications

```
$ git diff 13d45198..05b0d7f4 -- corpus/knowledge/response-header-expectations.md corpus/QUALITY.md | grep -c '^-[^-]'
0
```

(`^-[^-]` excludes the `---` diff headers; a modified base line would appear as a
`-`/`+` pair, so 0 means none.)

```
$ git diff --numstat 13d45198..05b0d7f4 -- corpus/knowledge/response-header-expectations.md corpus/QUALITY.md
4	0	corpus/QUALITY.md
29	0	corpus/knowledge/response-header-expectations.md
```

29 + 4 additions, 0 deletions.

### 3. Single tail hunk per file — additions sit after the last base line

```
$ git diff 13d45198..05b0d7f4 -- corpus/knowledge/response-header-expectations.md corpus/QUALITY.md | grep '^@@'
@@ -1410,3 +1410,7 @@ The round-47 criteria above are motivated and shown able to fail in `corpus/less
@@ -219,3 +219,32 @@ whether a serving stack would keep the same fields on the next request.
```

- `corpus/QUALITY.md`: hunk covers base lines 1410–1412, i.e. the file's final 3
  lines (base file = 1412 lines), all as context; 4 lines appended (1413–1416).
- `corpus/knowledge/response-header-expectations.md`: hunk covers base lines
  219–221, the file's final 3 lines (base file = 221 lines), all as context;
  29 lines appended (222–250).

Line counts confirm:

```
base  response-header-expectations.md: 221   measured: 250   (+29)
base  QUALITY.md:                        1412  measured: 1416  (+4)
```

Deltas equal the numstat addition counts exactly, consistent with pure appends.

### 4. Content of the appended hunks

- `corpus/knowledge/response-header-expectations.md` (after base line 221):
  adds `## Round-63 correction — S432 field-purpose span admitted as
  collapsed-only` and the `[r63-correction 2026-10-27]` paragraph quoting the
  Fetch §3.6 field-purpose sentence, classing it `collapsed-only` per the
  round-50 rule, citing
  `.ufo/waves/round-63/quote-class/S432.txt`,
  `.ufo/waves/round-63/quote-class/quote-classes.json`,
  `scripts/quote_class.py`, and the retained S432 blob digests.
- `corpus/QUALITY.md` (after base line 1412): adds `## Round-63 criteria` and
  one criterion bullet: "A frozen calibration counter's `resolved` predicate
  binds semantic evidence, not marker strings," with freeze rule.

No diff hunks report any changed or deleted base line — nothing to itemize.

## Commands used

- `git log --oneline -1 <rev>` (both commits)
- `git diff 13d4519818db28cd0aa912e49020659140d7b9fa..05b0d7f4b4a23513390f7b92547e2b0f1fccb06f -- corpus/knowledge/response-header-expectations.md`
- `git diff 13d4519818db28cd0aa912e49020659140d7b9fa..05b0d7f4b4a23513390f7b92547e2b0f1fccb06f -- corpus/QUALITY.md`
- `git diff ... | grep -c '^-[^-]'` (deletion count = 0)
- `git diff ... | grep '^@@'` (hunk inventory)
- `git diff --numstat ...`
- `git show <rev>:<path> | wc -l` (line counts)

All read-only against the fleet repo. No fixtures, no installs, no tool
changes this round.

## Confidence and remaining unknowns

High confidence: the claim is directly decidable from git diff output, and
zero `-` lines plus single tail hunks is dispositive for append-only.

Scope note: this seat verified only the two files named in the assignment.
Other files in the measured commit are outside this seat's scope.
