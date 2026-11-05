# ExecC1Fixes — kake round 93, wave 1 — C1 classes E3 and E5

VERDICT: E3 and E5 hold at the worktree — all seven repairs satisfy the frozen c1 predicate;
the frozen counter at `master` still prints the committed-bytes before-values (mismatches=20,
exit 1) because it reads `git show <rev>:<path>`, and a worktree replica of its own E3/E5 scan
reads 0/0 with the row population unchanged at 255.

Seat: ExecC1Fixes (leaf executor; owns E3 + E5 only; sibling scribe owns E1/E2/E4).
Lane root: /home/vgpnk/Projects/shokunin/kake-shokunin. Freeze bb8012fee38c0e497cdaf36337072737bca0b3cd;
base 10ecbd1ade91d0721e87a9942a66a2b61d5ce8d5. No commits, no pushes, no frozen-file edits,
no C2 work, no registry appends (per L1 KakeR93: SKILL.md is this seat's for the six E5 rows).

## 1. Frozen-counter reading (required paste)

Command (seat-assigned, run 2026-11-04 ~22:2x local from the lane root):

    python3 -B .ufo/waves/round-93/c93_selfassess.py --root . --revision master

exit code 1, line 1 exact:

    C1v93 revision=191ef8dd3bed7c6ad83b90108c16663c134611db lessons=87 entries=80 rows=255 criteria=39 mismatches=20 E1=1 E2=8 E3=1 E4=4 E5=6 pins=ok met=false

Full stdout (line 1 + JSON detail line) in receipt `counter-at-master.txt`. Remaining
mismatches (from the JSON line, one per line):

    E1 corpus/lessons/round-85.md -- no '## Gate' heading
    E4 corpus/lessons/round-29.md -- blank line inside the Mistakes table after row 17
    E4 corpus/lessons/round-33.md -- blank line inside the Mistakes table after row 5
    E4 corpus/lessons/round-54.md -- blank line inside the Mistakes table after row 6
    E4 corpus/lessons/round-92.md -- blank line inside the Mistakes table after row 7
    E2 corpus/QUALITY.md -- section 'Round-31 wave-2 corrections to the round-31 criteria' names no corpus/lessons/ file
    E2 corpus/QUALITY.md -- section 'Round-32 criteria' names no corpus/lessons/ file
    E2 corpus/QUALITY.md -- section 'Round-34 wave-2 corrections to the round-34 criteria' names no corpus/lessons/ file
    E2 corpus/QUALITY.md -- section 'Round-35 wave-2 corrections to the round-35 criteria' names no corpus/lessons/ file
    E2 corpus/QUALITY.md -- section 'Round-40 criteria' names no corpus/lessons/ file
    E2 corpus/QUALITY.md -- section 'Round-41 criteria' names no corpus/lessons/ file
    E2 corpus/QUALITY.md -- section 'Round-47 pointer correction — R6' names no corpus/lessons/ file
    E2 corpus/QUALITY.md -- section 'Round-76 criterion — quoted receipts are whole' names no corpus/lessons/ file
    E3 corpus/knowledge/meta-robots-directives.md -- missing source:; missing verified-at:; missing recheck:
    E5 SKILL.md -- names missing path scripts/kimi-surface.mjs
    E5 SKILL.md -- names missing path .ufo/waves/round-52/selftest/   (two rows)
    E5 SKILL.md -- names missing path .ufo/waves/round-52/selftest/ladder/
    E5 SKILL.md -- names missing path .ufo/waves/round-52/selftest/registry/
    E5 SKILL.md -- names missing path corpus/knowledge/google-robots-txt-limits.md

E1/E2/E4 are the sibling scribe's. E3 and the six E5 items are closed at the worktree by this
seat (below). `master` = 191ef8dd ("round-93: wave-1 spec (13 seats), validated dispatch payload
and the ready handoff") — one commit past the named freeze bb8012fe, both bb8012fe and base
10ecbd1a verified ancestors (`git merge-base --is-ancestor`, rc 0). The reading equals the
declared before-values exactly, so nothing scored moved between freeze and this measurement.

## 2. E3 repair — corpus/knowledge/meta-robots-directives.md

Predicate (frozen): non-empty `source:`, `verified-at:`, `recheck:` lines within the first 8
lines; every `S\d{3,}` id on the `source:` line resolves to a row id in corpus/SOURCES.md.

Repair: 3-line prefix inserted directly above the former line 1 (`scope: …`), which is now line
4. The body is untouched; `git diff` shows pure additions (receipt `repairs.diff`, first hunk).
The entry's existing bottom provenance block (source/verified-at/recheck with full sha256 pairs,
plus the appended [r79-correction]) is byte-identical.

    line 1: source: S449 — https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag; S450 — https://html.spec.whatwg.org/multipage/semantics.html; S451 — https://www.rfc-editor.org/rfc/rfc3339.txt (raw/text sha256 pairs and retained paths in the source block at the end of this entry)
    line 2: verified-at: 2026-11-04 — r93 wave seat ExecC1Fixes re-opened S451 live (GET 2026-11-05T01:29:13Z, HTTP 200, 35064 bytes, sha256 9ab2b8864a85dca73a88f49b0927bc7bc85f596926e4fd1890905777924e700a — equal to the pinned raw digest) and re-read the retained S449/S450 round-78 bodies; the historical quotes and the bottom provenance block are unchanged
    line 3: recheck: 90d for S449/S450; 365d for S451; re-locate quotes and hashes when sources change

Id resolution: S449/S450/S451 are SOURCES.md rows 196/197/198; replica prints
`meta-robots source ids=['S449','S450','S451'] all_resolved=True`. No other `S\d{3,}` token
occurs on the line.

Source opened this round (seat minimum, one GET; full record in `s451-fetch.txt`):
GET https://www.rfc-editor.org/rfc/rfc3339.txt at 2026-11-05T01:29:13Z → HTTP 200, 35064 B,
sha256 9ab2b8864a85dca73a88f49b0927bc7bc85f596926e4fd1890905777924e700a — equal to the raw
sha256 pinned in SOURCES row S451 and the entry's provenance line; the retained local body
`.ufo/waves/round-78/w1/ScoutSources/rfc3339.txt` hashes to 1d35e529…eb620 = the pinned text
digest. Both pins reproduce; no drift.

Proof: receipt `worktree-replica.txt`: `E3-worktree entries=80 mismatches=0`; trio at lines
1-3 (`meta-robots trio line 1/2/3` rows).

## 3. E5 repairs — SKILL.md, six citations

Counter mechanics (read from the frozen bytes before editing): a row is any `SKILL.md` line
starting with `|` with ≥4 cells; the space-joined body is scanned with
`` `((?:scripts|corpus|\.ufo)/[^`\s]+)` ``; a trailing `:<line>`/`:<start>-<end>` is stripped;
braces expand; `<…>` and `*` skip; existence is `git show <rev>:<path>`. **There is no
annotation-skip** — a bare backticked repo-relative token fails existence regardless of any
adjacent annotation text. Therefore each repair either re-points the citation to the file that
exists, or moves the absent path INSIDE a backtick span that begins with `[r93-absence …`
(so PATH_RE cannot match it) — the path stays visible and greppable, and the wording follows
the lane's `[rNN … absent …]` family (r20 citation-local at SKILL.md:111, r71 absence at :227).

Absence evidence per path (all commands run this session, rc as shown):

- `scripts/kimi-surface.mjs` — `git cat-file -e master:scripts/kimi-surface.mjs` rc 1;
  `git log --all --diff-filter=D -- scripts/kimi-surface.mjs` → no output (never committed, so
  no deletion event). The tool lived in the webzites checkout (`~/Projects/webzites`), gone in
  the 2026-10-12 prune (W7) per the r20 citation-local note at SKILL.md:111. Nothing inside the
  lane to re-point to → annotated.
- `.ufo/waves/round-52/selftest/` (rows 1215 and 1216), `…/ladder/` (row 1351), `…/registry/`
  (row 1352) — `git ls-tree -r master -- .ufo/waves/round-52/selftest` → empty; no deletion
  events. Runtime-only selftest scratch the r52 counters create and remove (and gitignored,
  `.gitignore:4`) → annotated as runtime-only, never committed.
- `corpus/knowledge/google-robots-txt-limits.md` (row 1358) — `git cat-file -e master:…` rc 1;
  no deletion event. This is the round-60 STAGED draft name:
  `.ufo/waves/round-60/c60_quote_truth.py:108` `STAGED_ABSENT =
  ("corpus/knowledge/google-robots-txt-limits.md",)` and the same row's C1 asserts it does NOT
  exist — the path must stay absent, and creating it would flip a frozen gate. Re-pointed per
  seat instruction: the round's committed entry for the subject is
  `corpus/knowledge/robots-txt-limits.md` (S429, "staged S415, renumbered" per the c60 header;
  `git cat-file -e master:corpus/knowledge/robots-txt-limits.md` rc 0, `test -e` → 0).

The seven edits (hunks in `repairs.diff`):

1. E3 prefix, meta-robots-directives.md (above).
2. Row 222: `` (`scripts/kimi-surface.mjs:206-208`) `` →
   `` (`:206-208` of the sync-check tool — `[r93-absence 2026-11-04: scripts/kimi-surface.mjs absent — gone in the 2026-10-12 ~/Projects prune/migration (W7), per the r20 citation-local note at the drift-check preamble; never a lane-repo path; historical record, not an executable instruction]`) ``
3. Row 1215 (wave-evidence-ledger): bare `` `.ufo/waves/round-52/selftest/` `` →
   `` `[r93-absence 2026-11-04: .ufo/waves/round-52/selftest/ absent as a committed path — runtime-only selftest scratch the counter creates and removes on exit, never committed]` ``
4. Row 1216 (quote-truth-counter): same replacement (one replace_all edit covered both rows).
5. Row 1351 (ledger-mutation-ladder): `` `.ufo/waves/round-52/selftest/ladder/` `` →
   `` `[r93-absence 2026-11-04: …runtime-only ladder selftest scratch, removed on exit, never committed]` ``
6. Row 1352 (gate-registry-completeness-counter): `` `.ufo/waves/round-52/selftest/registry/` `` →
   `` `[r93-absence 2026-11-04: …runtime-only registry selftest scratch the counter creates and removes on exit, never committed]` ``
7. Row 1358 (user-triggered-quote-truth-counter): "the staged `` `corpus/knowledge/google-robots-txt-limits.md` `` does not" →
   "the staged candidate name does not (`` `[r93-absence 2026-11-04: corpus/knowledge/google-robots-txt-limits.md — the round-60 staged draft name, never committed and never deleted because no commit ever carried it; c60_quote_truth.py STAGED_ABSENT asserts this absence, so the path must stay absent]` ``; the round's committed entry for the subject is `` `corpus/knowledge/robots-txt-limits.md` ``)"

No row added or removed, no cell reordering, no unrelated cell touched; rows stay 255
(worktree replica and counter agree).

Proof (receipt `worktree-replica.txt`, scanner `verify_repairs.py` — replicates the frozen
PATH_RE/row/brace/strip logic, existence against the worktree = carrier content):

    E5-worktree rows=255 path_tokens=204 missing=0
    E5-token scripts/kimi-surface.mjs                     bare_matches=0 exists=False
    E5-token .ufo/waves/round-52/selftest/                bare_matches=0 exists=True (worktree-only, gitignored residue)
    E5-token .ufo/waves/round-52/selftest/ladder/         bare_matches=0 exists=False
    E5-token .ufo/waves/round-52/selftest/registry/       bare_matches=0 exists=True (worktree-only, gitignored residue)
    E5-token corpus/knowledge/google-robots-txt-limits.md bare_matches=0 exists=False
    E5-token corpus/knowledge/robots-txt-limits.md        bare_matches=1 exists=True

Per-path `test -e`: kimi-surface.mjs → 1; selftest/ladder → 1; google-robots-txt-limits.md → 1;
robots-txt-limits.md → 0; selftest/ and selftest/registry/ exist in the WORKTREE only (empty,
gitignored residue of old in-place selftest runs — the committed tree is absent, which is what
the counter reads).

## 4. Line-shift register (QUALITY.md round-21 rule)

The +3 prefix moves every later line: old line N → N+3. Per the round-21 rule, historical
literal pointers keep baseline coordinates; this register is the current-coordinate map.
In-file: the [r79-correction] block's "(line 123)" is a baseline coordinate (current 126).
External pointers into this entry, found with
`grep -rn 'meta-robots-directives\.md:[0-9]'` over the lane:

| Citing file:line | Baseline cite | Current coordinate |
|---|---|---|
| .ufo/waves/round-78/w1/CriticC.md:107 | :104-114 | :107-117 |
| .ufo/waves/round-79/w1-results.json:52,82 | :123 | :126 |
| .ufo/waves/round-79/w1/ConnectorC.md:12 | :123 | :126 |
| .ufo/waves/round-79/w1/ScribeRecord.md:66 | :123 | :126 |
| corpus/lessons/round-79.md:140,147 (and its r86 mirror copy) | :123, :140 | :126, :143 |

## 5. Findings (routed candidates; no frozen file touched)

- **F1 — predicate/repair-recipe gap.** The frozen counter's E5 has no annotation-skip: a
  lane-style absence annotation placed BESIDE a bare backticked repo-relative token (the visible
  style of r20 at SKILL.md:111 or r71 at :227) would NOT close the mismatch. The seat recipe's
  "annotate … in `[rNN … absent …]` style" only works in the counter's terms when the path moves
  inside a span PATH_RE cannot match (my form), or is re-pointed. A successor predicate should
  either state this token rule or teach the counter to skip documented-absence annotations.
  Found before scoring; not patched (frozen instrument).
- **F2 — append_guard interaction.** The E3 repair is an inserted run at the TOP of a
  corpus/knowledge file. scripts/append_guard.py's contract admits end-of-file appends and
  requires every other inserted run to begin with a `[rNN-correction YYYY-MM-DD]` tag, so a
  future guard run against a pre-r93 base would flag this untagged prefix. Precedent: the
  round-21 metadata prefixes are likewise untagged and were admitted with a per-file register
  (§4 here is that register). L1/successors running the guard across this commit should expect
  the prefix as a known registered exception, or extend the guard for metadata prefixes.
- **F3 — worktree residue (resolved, informational).** `.ufo/waves/round-52/selftest/{,registry/,ledger/,quote/}`
  exist in the worktree as EMPTY, gitignored (`.gitignore:4`) leftovers of old in-place selftest
  runs (mtimes Oct 25 / Nov 3); `git status --porcelain --untracked-files=all` over the path is
  silent. No `git add -A` hazard; committed view absent, as the counter requires. L1 may rmdir
  them at leisure; this seat did not touch them.
- **F4 — master advanced past the named freeze revision during dispatch** (bb8012fe → 191ef8dd,
  "wave-1 spec"); the counter reading at master equals the declared before-values exactly, so
  nothing scored moved. Recorded so the carrier measurement cites the right tip.
- **F5 — self-caught edit defect.** My first row-1358 replacement dropped the space before "C2"
  (`…robots-txt-limits.md`),C2…`); restored in a follow-up edit the same session. The hunk in
  `repairs.diff` carries the corrected text.

## 6. Limits

- All repairs are UNCOMMITTED worktree state; the counter reads committed bytes, so its
  20-mismatch reading stands until L1 lands the wave. The carrier reading (expected
  `mismatches=0 … met=true`, exit 0, modulo the sibling's E1/E2/E4 work landing too) is L1's to
  measure after commit; this seat ran no mutating git command.
- Only S451 was opened live (the seat's "at least one"); S449/S450 were re-read from retained
  round-78 bodies, and the verified-at line claims exactly that and no more.
- E3 checks presence/resolution of the trio, not that the sources support the entry (the frozen
  predicate says so); no semantic re-verification of the r78 quotes was attempted.
- The annotation spans make the five absent paths invisible to PATH_RE by construction; a
  grepper still finds each literal name inside its `[r93-absence …]` span.

## 7. Receipts (this directory)

- `counter-at-master.txt` — full stdout of the frozen counter at master (exit 1).
- `worktree-replica.txt` — E3/E5 replica scan: missing=0, mismatches=0, rows=255.
- `verify_repairs.py` — the read-only replica scanner (re-run with `python3 -B`).
- `repairs.diff` — `git diff -U2 -- SKILL.md corpus/knowledge/meta-robots-directives.md`
  (28 827 B, captured before scratch cleanup).
- `s451-fetch.txt` — GET record: status 200, 35064 B, sha256 9ab2b886…e700a, access
  2026-11-05T01:29:13Z, plus both pin comparisons.

Tooling authorization note: no tool installed or upgraded this seat (none needed); pacman
untouched. Scratch /fast/scratch/hyaku/kake-r93/ExecC1Fixes deleted before yield; no /tmp use.
