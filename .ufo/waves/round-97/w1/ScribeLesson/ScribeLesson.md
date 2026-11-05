# ScribeLesson — round-97 lesson sections (draft for the L1)

Seat: ScribeLesson (scribe, leaf member — no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Round base `36d148f5c60100021304903c30e5663207c72f4f`; instruments
`74bda9b7d14a5108b1dfa119534ed4045a4b35a3` (v1) and
`a2208ac7b8ce6e1148e5069b4c884c78f97dfb3e` (v2, frozen); freeze
`5d5f608f3cd9aa9a73136cf05f81bef38bea40cb`; C1 repair
`9e27ce0b2a8d168e032ab79ea11471b36eaceedf` (lane tip at the start of this seat,
re-read: `git -C LANE rev-parse master` → `9e27ce0b…`).

## Deliverables

- `.ufo/waves/round-97/w1/ScribeLesson/mistakes.md` — the `## Mistakes` draft
  (3 rows, table shape class · evidence pointer · captured-by · fix).
- `.ufo/waves/round-97/w1/ScribeLesson/routed.md` — the `## Routed to round 98`
  draft (6 items).
- Receipts in this directory (all written by this seat; see below).
- This seat report is written twice, byte-identically, at
  `.ufo/waves/round-97/w1/ScribeLesson/ScribeLesson.md` (inside the seat
  directory) and at the trailer path `.ufo/waves/round-97/w1/ScribeLesson.md`,
  because the trailer names the second and the lane bound names the first;
  round 96 carries the same pair of forms. Both are untracked files under
  `w1/` written by this seat only — no other seat's directory was touched.

Both drafts are prose only and assert no verdict that the L1 has not recorded.
The C1 predicate's second conjunct (row review in `w1/ReviewIndexA/verdicts.tsv`
+ `w1/ReviewIndexB/verdicts.tsv`) and the C2 verdict line are the L1's to
record; neither is claimed here.

## What was read (committed bytes only)

`.ufo/waves/round-97/freeze.md`; `.ufo/waves/round-97/controls/` (17 tracked
receipts + `instrument-sha256.txt`); `controls/v1-forgery-crash/ctl-c2-slot-table-74bda9b7.txt`;
the repair commit `9e27ce0b`; `corpus/lessons/round-96.md` (`## Mistakes`,
`## Routed to round 97`); `corpus/lessons/round-96-verifier-spotcheck.md` (§1
conformance defect 2, §6 R97-D1); `corpus/lessons/round-95.md` (R95-2, R95-6,
R95-7, R95-8); `SKILL.md` registry rows; `CORPUS.md:46`.

Frozen digests verified before use (`sha256sum` against
`controls/instrument-sha256.txt`): `c97_index.py` `8535150e…a008`,
`c97_reval.py` `f3895a32…9266`, `frozen/neg-lookup-table.py` `898df9a2…60cc`
— all three match. No instrument byte was touched.

## Re-derivations run by this seat (read-only against the lane; fixtures in scratch)

| receipt | command | observed rc / line |
|---|---|---|
| `receipt-c1-base.txt` | `python3 -B .ufo/waves/round-97/c97_index.py --root LANE --revision 36d148f5… --work $SCRATCH/w-base` | rc=1, `entries=84 indexed=46 unindexed=38 dangling=0 mismatches=38 met=false` |
| `receipt-c1-repair.txt` | same counter, `--revision 9e27ce0b…` | rc=0, `entries=84 indexed=84 unindexed=0 dangling=0 mismatches=0 met=true` |
| `receipt-c2-v1-forgery-crash.txt` | v1 instruments (`74bda9b7`) + v1 frozen forgery in the candidate slot of a `--shared` clone, `c97_reval.py --root $FX --revision $R` | rc=1, `hand=20/37 generated=0/104 heldout=0/53 … met=false`; direct sandbox run of the subject prints `ModuleNotFoundError: No module named 'hashlib'` |
| `receipt-c2-v2-slot-table.txt` | v2 instruments (`a2208ac7`) + v2 frozen forgery in the candidate slot | rc=1, `hand=37/37 generated=104/104 heldout=18/53 … met=false` — refused on held-out only |
| `receipt-sandbox-import-probe.txt` | subject importing one stdlib module under the frozen `SANDBOX` | `json`/`re`/`collections` import; `hashlib`/`base64`/`random`/`textwrap` → `ModuleNotFoundError` (the sandbox names `hashlib` in its allowlist, but the stdlib is not on `sys.path` after `sys.path[:] = [root]`, so the failure is `ModuleNotFoundError`, not the audit hook's `PermissionError`) |
| `receipt-sandbox-effectful-probe.txt` | `os.kill(os.getppid(),0)`, `os.listdir('/etc')`, `os.scandir('/')` under the frozen `SANDBOX` | `kill-ppid: ALLOWED`; `/etc` listing returns 196 entries; `/` scandir returns 23 — the R96-4 vectors are still open |
| `receipt-sandbox-escape-probe.txt` | `os.execv`, in-tree symlink → `/etc/hostname` then open | `PermissionError: sandbox: process creation denied: os.exec`; `PermissionError: sandbox: open outside the subject tree: /etc/hostname` — the R95-7 vectors are closed by these bytes |
| `receipt-c55-counter-base-and-tip.txt` | `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision 36d148f5…` and `--revision 9e27ce0b…` | rc=1 at both; `index_mismatches=29 knowledge_files=90 met=False`, `unindexed=24` including `revalidation-exchange.md`; the unindexed set is byte-identical before and after the repair |

Fixture discipline: one clone per seat under
`/fast/scratch/hyaku/kake-r97/ScribeLesson/` (`fx1`, `fx2`), each created with
`git clone --shared LANE`, with `git rev-parse --show-toplevel` asserted equal
to the fixture dir before the single commit, identity
`scribelesson@example.invalid` passed with `-c` flags only. No mutating git or
jj command was run in the lane or the fleet repo; the lane working tree was
left untouched by this seat (verified with `git status --porcelain`).

## Findings

1. **M1 (mistakes.md row 1).** The v1 lookup-table forgery imported `hashlib`,
   which the counter sandbox cannot import; the forgery crashed, so its
   "refusal" was a crash artefact. Concretely: `hand=20/37` because the
   counter treats a `None` answer as a correct refusal and exactly 20 of the
   37 hand cases expect a refusal (`hand_cases()`: 37 cases, 20 with expected
   `None`); `generated=0/104`; and the forge note for `neg-lookup-table.py`
   reads `"admitted": false, "refused_ok": true` with first-failure text
   `… got Non` — the crashed subject satisfied the counter's forgery-refusal
   test (`not admitted`) without any of the anti-table or held-out defenses
   being exercised. Caught pre-freeze by reading the failure text; the v2
   forgery (no `hashlib`, only `json`/`sys`) now answers every hand and
   generated case from memory and is refused on held-out only.
2. **M2 (mistakes.md row 2).** R97-D1 generalises: at the base, 38 of the 84
   committed `corpus/knowledge/*.md` entries were unindexed — 12 with no index
   row at all, 26 with a row that omits a source id the entry's own `source:`
   line cites (`revalidation-exchange.md` is one of the 12). The CORPUS
   index-row rule and the round-96 closure caught the rule; no lane instrument
   measured the population, and the lane's registered coverage-index counter
   was red by design since round 59. Fixed by `c97_index.py` (shown able to
   fail: base 38 → exit 1; path-only rows → `unindexed=38` exit 1; fenced rows
   → `unindexed=38` exit 1; selftest 14/14) plus the repair commit
   `9e27ce0b` (→ `mismatches=0 met=true` exit 0).
3. **M3 / R97-S1 (mistakes.md row 3, routed.md item 6).** The round-97 freeze
   says the lane "held no coverage-index instrument" for C1. Committed bytes
   say otherwise: `.ufo/waves/round-55/c55_readme_index.py` exists, is
   registered in `SKILL.md`, and measures this same surface. Worse, the two
   counters now disagree about the same file: after the repair the historical
   counter still reports the identical 24 unindexed (it reads only
   `## Coverage map`), while `c97_index.py` reads `mismatches=0`. Same defect
   class as round-96 Mistake 3 — routed, not repaired by this seat.
4. **R96-2 residue.** The v2 memorizing forgery passes `anti_table=ok`
   (`anti_hits: []`, `anti_stems: []`) and every hand and generated case, and
   is refused only by the commit-id-seeded held-out population. The blacklist
   is not the defense; the held-out cases are. The R96-2 refusal-coarseness
   class also stays open — the counter keeps only a 120-character `first`
   failure string per forgery, so a crash and a wrong decision look alike.
5. **R96-3.** The four false-green shapes (RX01/RX02/RX03b/RX09), the
   absence-annotation laundering route, the vocabulary-stuffing route and the
   `git replace` route all name `c96_selfassess.py`, whose bytes are unchanged
   at the round-97 tip (`a282da65…` at `9177e658` and at `9e27ce0b`) and which
   remains the registered gate. Round 97's C1 claim is a different surface and
   cannot close them.
6. **R96-4.** The round-97 C2 successor inherits the round-96 `SANDBOX`
   byte-for-byte; the named effectful-shadow vectors (`os.kill(ppid, 0)`,
   outside metadata listing) are still open — verified by probe. The R95-7
   vectors (`os.execv`, in-tree symlink escape) are closed by the same bytes
   and may be dropped. The C1-side PATH-`git` item of R96-4 is closed for
   `c97_index.py` (`GIT = "/usr/bin/git"`, `GIT_NO_REPLACE_OBJECTS=1`) but
   remains open on `c96_selfassess.py` (line 179 runs bare `git` with no env
   pin).
7. **R95-2.** Still open: the L0 line at fleet `.ufo/l0-questions.md` line 371
   is the only R95-2 line in that file, so no operator ruling has landed.
   `c97_reval.py` kills a mutant on any failure (`is_killed = bool(fails)`),
   i.e. it adopts the loose reading by default while the question is pending.

## Out of scope for this seat (not touched, not claimed)

- No product code, instrument, counter, ledger or registry was edited.
- No verdict is asserted for C1 or C2; the row-review conjunct and the C2
  verdict line are the L1's to record.
- The C1 counter's declared shuffle limit is carried as a route, not as a
  defect claim: the shuffle fixture is *expected* to pass (`met=true`, exit 0
  in `controls/ctl-c1-forgery-shuffle.txt`), which is why the predicate carries
  the row-review conjunct.
- Nothing was committed, pushed, published or deployed; no other runtime was
  invoked.

## Tooling

No tool was installed or upgraded by this seat; the work used only the
repository's committed Python 3 counters and `git` already present on the
host. No `pacman`, `uv`, `npx` or `~/.local/bin` action was taken.

## Incident note (host-side, not a lane defect)

At ~18:14Z peer `ConnectorScope-23` reported that it ran
`rm -rf /fast/scratch/hyaku/kake-r97` — the round parent directory — and
deleted several sibling seats' scratch trees, including this seat's. This seat
recreated `/fast/scratch/hyaku/kake-r97/ScribeLesson/` and re-derived every
result above from the frozen instruments and the committed controls; no frozen
byte, LANE tree, MANIFEST or host sysctl was affected. The peer stated it
would not clean again. This seat's own scratch tree was removed before it
yielded.

Verdict line: SCRIBE-LESSON mistakes=3 routed=6
