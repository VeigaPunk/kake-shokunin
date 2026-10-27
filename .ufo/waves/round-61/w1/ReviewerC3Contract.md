# ReviewerC3Contract

Scope: contract § Claim C3 reviewed against `corpus/QUALITY.md` and the canonical corpus
contract (`kimi-shokunin/skills/shokunin/protocol/CORPUS.md`, read-only). Base
`9f07731a873585e655a6518233ea39f5d9fb8204`; contract committed at `eaa9177`. All registry
facts re-derived from committed bytes at base; timings measured on this host.

## FINDINGS:

- **major — C6 wording literally fails every honest run (C2↔C3 coordination hazard).**
  C6 freezes: "rows not in the due set are byte-identical to base (append-only registry
  outside the recheck-cell changes)". At the measured revision the registry necessarily
  contains S430–S433 (C2 appends); those rows are not in the due set and cannot be
  byte-identical to base (absent at base). A literal implementation of the frozen sentence
  is red on any conforming run. The intended semantics — base rows unchanged, new rows are
  pure appends — is exactly how round-60's C8 was implemented ("the measured registry minus
  the three new rows reproduces the mirror bytes", round-60 contract). Fix before freeze:
  rephrase C6 to "every registry row present at base and not in the due set is byte-identical
  to its base bytes; every row absent at base is an appended row carrying a next-unused id",
  or have the counter carry this reading in its notes.

- **major — S433's W04 note wording can collide with C6.** The C2 source blurb says S433
  "adds one W04 duplicate-URL-across-scopes note with the existing S088 row". W04 notes are
  census-emitted lines (`controls/census-before.txt` format), not registry-row content —
  S088's base row carries no W04 text (cells 1–11 inspected: id, source, kind, tier, scope,
  anchor, teaches, status=mined, opened=2026-10-23, recheck=90d, used-by=scripts/source_recheck.py).
  If a C2 seat implements "add a note with S088" by editing S088's row, C6 goes red on a
  non-due row. Fix: state explicitly "the census-after run emits the W04 pair; no registry
  row other than the four appends changes".

- **medium — due-set rows have no cell-mutation coverage.** C6 guards only non-due rows.
  For the ten due rows nothing in C1–C6 fails if `teaches`/`anchor`/`scope`/`source`/`used-by`
  is rewritten alongside a valid pin. (Status flips on due rows ARE caught: C1 re-derives the
  due set at the measured revision, so a rejected flip changes the lowest-10 cut.) Canonical
  rule 2 permits in-place `status`/`recheck`/`used-by` changes with old→new lesson logs; a
  canonical-legal `used-by` flip on a due row is counter-unchecked (the log requirement is
  prose, not counter-enforced). Not fixable by loosening the frozen conditions; record as a
  v2 tightening candidate ("each due row differs from base only in its recheck cell") and
  note it under "What the counter does not test".

- **minor — C6's parenthetical misquotes canonical append-only rule 2.** CORPUS.md SOURCES
  rule 2: only `status`, `recheck`, `used-by` change in place, each logged old→new. C6's
  parenthetical "(append-only registry outside the recheck-cell changes)" is stricter and
  round-local. No live conflict this round (nothing needs a status/used-by flip outside the
  due set), but the frozen text should not be cited back as canonical rule 2.

- **ok — predicate is a single sentence.** "met: conditions_passed == 6 of 6" is one
  sentence; the claim-header sentence ("the ten oldest registry rows re-verified live…") is
  not the PREDICATE and is not carried by the counter. Consistent with the contract header
  sentence ("The predicate sentence of each claim… is the sentence the counter's code
  carries"). No fix.

- **ok — C6 byte-identity cost is a non-issue (measured).** The registry is one file:
  156,537 bytes, 282 lines, 167 rows at base. `git cat-file blob 9f07731a…:corpus/SOURCES.md`
  + `sha256sum` measured ≈1 ms; a row-level parse-and-compare in Python is the same order.
  The counter is offline/committed-bytes; base is an ancestor of the measured revision so
  the base blob is present. Expense concern: none.

- **ok — due-set freeze verified against base bytes.** At base, 18 rows carry
  opened=2026-10-19; 2 are rejected (S017, S018) → 16 non-rejected ties; lowest 10 by id =
  S001–S010, matching contract.md and contract.json. Their recheck cells are all cadences
  (on-release ×2, 90d ×5, 365d ×3 — the C3 do-nothing "C2 fails, 0 concrete dates" is
  reachable). Pin dates check out: 2026-10-19 +90d = 2027-01-17, +365d = 2027-10-19
  (`date -u` verified). Nits: (a) "frozen at base by rule" vs C1's "re-derived at the
  measured revision" can only diverge via a due-row opened/status mutation, which C1
  catches — sound; (b) the freeze sentence does not say the remaining 6 ties are ordinary
  non-due rows under C6 — one clarifying phrase; (c) backdating is structurally impossible:
  new rows take next-unused S### ids ≥ S430, so the lowest-10 cut is stable.

- **ok — C2 do-nothing failure at base is reachable.** `scripts/header_snapshot.py`…
  specifically `scripts/response_snapshot.py` and `scripts/header_audit.py` are both absent
  from `scripts/` at base 9f07731a; the round-23 population `.ufo/waves/round-23/live/`
  carries exactly 12 surfaces. With the audit tool absent, the counter running the tool "as
  committed at the revision" scores 0/18 → predicate false. Reachable and honest.

- **ok — amendment surface mapped.** (a) contract.md/contract.json: committed pre-dispatch
  at `eaa9177`; amendment now = one L1 commit before the counters freeze; after freeze only
  a v2 tightening per the round-shape paragraph. (b) The round-61 contract has no
  `## Counter versions` section yet — the round-shape paragraph references it; round-60's
  contract carried one and round-61 grows it at v2 integration (dangling forward reference,
  cosmetic). (c) Canonical CORPUS.md lives outside the lane (read-only protocol) — the lane
  cannot amend it; C6's tightening is round-local, never a canonical change. (d) The
  registry and the lesson `## Gate` are evidence surfaces, not condition-amendment surfaces.
  (e) contract.json's machine-readable `due_set` matches contract.md; the header sentence
  makes contract.md the predicate source if they ever diverge.

VERDICT: C3 conditions are feasible and the freeze is sound, but C6 as worded literally
fails any conforming run because of C2's S430–S433 appends (and the S433 W04 note wording)
— rephrase C6 and the S433 blurb before the counters freeze; the due-row cell-mutation gap
is a recorded v2 tightening candidate, everything else verified clean.
