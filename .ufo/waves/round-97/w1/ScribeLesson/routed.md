# round-97 — `## Routed to round 98` (draft for the L1 to integrate into `corpus/lessons/round-97.md`)

Drafted by seat ScribeLesson from committed bytes only: the round-97 freeze,
the committed pre-freeze receipts under `.ufo/waves/round-97/controls/`, the
v1-crash receipt, the repair commit `9e27ce0b2a8d168e032ab79ea11471b36eaceedf`,
`corpus/lessons/round-96.md` (its `## Routed to round 97` section),
`corpus/lessons/round-95.md` (`## Routed to round 96`) and
`corpus/lessons/round-96-verifier-spotcheck.md` §6. Each item below names the
pointer it rests on. No verdict of either round-97 claim is asserted here.

## Routed to round 98

- **R96-2 residue — the anti-table blacklist is not the defense; the held-out
  cases are.** The round-97 successor widens the anti-table as R96-2 asked
  (raw canonical and minified JSON texts, sha256/sha1/md5 digests of both
  forms, their alternate-nibble halves and base64/urlsafe-base64 encodings —
  `c97_reval.py` docstring and `input_digests`), and adds held-out cases whose
  seed is derived from the scored commit id. The committed control shows which
  of the two actually does the work: with the v2 memorizing forgery in the
  candidate slot, `controls/ctl-c2-slot-table.txt` reads
  `hand=37/37 generated=104/104 heldout=22/57 forgeries_refused=7/7 positive=admitted
  mutants=14/14 survivors=none anti_table=ok population=ok seed=97 met=false`,
  exit 1 — the blacklist never fired (`anti_hits: []`, `anti_stems: []`,
  `anti_table=ok`), the subject answered every hand and generated case from
  memory, and only the commit-id-seeded held-out population refused it.
  Round 98 must keep the held-out cases as the load-bearing defense and must
  not treat an `anti_table=ok` line as evidence that a memorizing subject was
  caught. The R96-2 refusal-coarseness class (MutReval N05/N06/N07/N08/N11:
  one refusal must not stand for another) also stays open — the counter records
  per-forgery only a `first` failure string truncated to 120 characters
  (`c97_reval.py` `score_fixture`/`forge_notes`), so a crash and a wrong
  decision are the same shape of evidence; round 97's own v1 receipt is the
  demonstration (see `mistakes.md` row 1).

- **R96-3 — the round-96 C1 self-assessment counter's false-green shapes are
  unclosed.** `corpus/lessons/round-96.md` routes R96-3 (ReviewC1,
  `w1/ReviewC1/routes.md`): RX01 decisions only inside an HTML comment, RX02
  decisions only inside fenced code, RX03b an entire `## Gate` inside a fence,
  RX09 a subdir lesson whose round number hijacks the `>= 96` vocabulary
  guard — plus the absence-annotation laundering route (CriticClaims C1-02),
  the two-token vocabulary-stuffing route (C1-03) and the `git replace`
  substitution route (C1-05). The instrument those routes name is
  `.ufo/waves/round-96/c96_selfassess.py`; its bytes are unchanged at the
  round-97 tip (sha256 `a282da654d5ee6af923abb2cae4bd0a4fd6e4309db81de5a67999ed7b25ad134`
  at `9177e658` and at `9e27ce0b` alike), it is still the registered
  `c96_selfassess.py` gate in `SKILL.md`, and round 97's C1 claim is a
  different surface (the `corpus/README.md` coverage index, scored by
  `c97_index.py`) that does not supersede it. Round 98 must therefore either
  repair the self-assessment counter against these classes or state that it is
  retired in favour of another instrument; the routes cannot be closed by the
  round-97 C1 work.

- **R96-4 — the C2 sandbox still has no effectful-shadow defense.** R96-4
  (SentinelScope F2/F3/F4) named the C2 sandbox's missing effectful-shadow
  defense and the unaudited vectors `os.kill(ppid, 0)` and outside metadata
  listing. The round-97 C2 successor inherits that sandbox unchanged — the
  `SANDBOX` constant in `c97_reval.py` is byte-identical to the one in
  `c96_reval.py` (both extracted from their committed revisions and compared
  equal), and it still audits `open`, `import` and process creation only.
  Probing the frozen sandbox confirms the two named vectors are open: a
  subject's `os.kill(os.getppid(), 0)` is allowed, `os.listdir('/etc')` returns
  196 entries and `os.scandir('/')` returns 23 entries
  (`receipt-sandbox-effectful-probe.txt`). The two vectors R95-7 named for
  this sandbox are, by contrast, closed by the same bytes and may be dropped:
  `os.execv` is refused (`PermissionError: sandbox: process creation denied:
  os.exec`) and an in-tree symlink to `/etc/hostname` cannot be opened
  (`PermissionError: sandbox: open outside the subject tree: /etc/hostname`)
  — `receipt-sandbox-escape-probe.txt`. Round 98 must close the effectful
  shadow (or record that the defense is deliberately out of scope for a
  counter that runs untrusted subjects).
  The R96-4 F2 item — the C1 counter resolving `git` from PATH — also remains
  open on the instrument it names: `c96_selfassess.py` line 179 runs
  `subprocess.run(["git", "-C", root, *args], capture_output=True)` with no
  `GIT_NO_REPLACE_OBJECTS` and no pinned `git` path, at unchanged bytes. The
  round-97 C1 counter does pin both (`GIT = "/usr/bin/git"`,
  `GIT_NO_REPLACE_OBJECTS=1` in `c97_index.py`), which closes that class for
  the new instrument only, not for the registered one.

- **R95-2 — the L0 kill-predicate question is still open, with the L1's own
  rule standing in the meantime.** `corpus/lessons/round-95.md` routes R95-2:
  the lanes define "a mutant is killed" differently (kumitate K43 requires an
  immediate rerun with identical sorted failing case names; tabi declares
  equivalence at catalogue authoring time; kake requires digest-pinned
  equivalence receipts for any surviving mutant, R94-4). The L0 line was filed
  in the fleet repo at `.ufo/l0-questions.md` line 371
  (`kake | round-96 | R95-2 fleet kill-predicate arbitration owed: …`); it is
  still the only R95-2 line in that file, so no operator ruling has landed.
  Round 97 neither asked nor answered it: `c97_reval.py` kills a mutant when
  the mutant produces any failure (`is_killed = bool(fails)`), i.e. it adopts
  the loose reading by default. Round 98 must carry the question to the
  operator again and must not silently adopt a sibling's predicate in the
  meantime.

- **The C1 counter's declared shuffle limit — the counter cannot judge prose
  accuracy, so the row-review conjunct is load-bearing.** `c97_index.py`
  declares the limit before any data ("Known limit, declared before data: a
  row assembled from shuffled entry words passes (a)-(c); prose accuracy is
  judged by review, not by this counter", fixture `known-limit-shuffle`,
  expected exit 0), and the committed control shows it behaving exactly as
  declared: `controls/ctl-c1-forgery-shuffle.txt` reads
  `C1v97 revision=98aac10e… entries=84 indexed=84 unindexed=0 dangling=0
  mismatches=0 met=true`, exit 0, on rows assembled from shuffled entry words
  with the right ids. The frozen C1 predicate therefore carries a second
  conjunct — every row of the round-97 index section judged `agree` in
  `w1/ReviewIndexA/verdicts.tsv` and `w1/ReviewIndexB/verdicts.tsv` — and
  that conjunct, not the counter, is what certifies the prose. Round 98 must
  either keep the row-review conjunct mandatory and state that the counter's
  green is not a prose verdict, or build prose-judging into a successor
  counter; the shuffle forgery must continue to be expected to pass.

- **R97-S1 (new this round; routed by this seat, not repaired here) — two
  lane counters disagree about the same file, and the round-97 freeze's
  do-nothing sentence does not name the instrument set that defines the
  do-nothing lane.** The round-97 freeze states, for C1, that "the lane held
  no coverage-index instrument" and that the do-nothing tree is the base README
  scored by the successor counter. Committed bytes show the lane did hold one:
  `.ufo/waves/round-55/c55_readme_index.py`, registered in `SKILL.md` as the
  `readme-index-counter` gate, measuring `corpus/README.md`'s `## Coverage map`
  against the committed tree. At the round-97 base it reports
  `index_mismatches=29 knowledge_files=90 met=False` and already names
  `revalidation-exchange.md` among its 24 unindexed. After the C1 repair
  (`9e27ce0b`) it reports the *identical* 24 unindexed, because the 38 new
  rows landed in a new section `## Coverage index — round 97 (calibration
  repair)` (`corpus/README.md:794`) that `c55_readme_index.py` does not read,
  while `c97_index.py` — which reads any Entry-headed table — reads
  `mismatches=0 met=true` (`receipt-c55-counter-base-and-tip.txt`,
  `receipt-c1-repair.txt`). Two registered instruments over one surface now
  disagree about the same repository. Round 98's freeze must name the
  do-nothing instrument set explicitly (the historical `c55_readme_index.py`
  at the base plus the successor at the base), and the lane must either
  reconcile the two counters over `corpus/README.md` or retire one of them in
  the registry — the same defect class as round-96 Mistake 3, which is why it
  is routed rather than repaired by this seat.

## Notes the L1 should carry into the prose

- The list above carries six items: the R96-2 residue, R96-3, R96-4, R95-2,
  the C1 counter's declared shuffle limit, and the new R97-S1.
- Two of the six are closed-by-evidence statements rather than open routes and
  are marked as such: the R95-7 symlink/`os.execv` vectors (closed by the
  frozen sandbox bytes) and the R96-4 git-PATH item for the round-97 C1
  counter (closed for `c97_index.py`, still open for `c96_selfassess.py`).
- Nothing here claims a C1 or C2 verdict; the C1 row-review conjunct and the
  C2 verdict line are the L1's to record.
