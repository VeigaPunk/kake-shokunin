# Residual no-harm review — corpus surface (KakeR28a3.ReviewNoHarmCorpus)

Range: 22c1669c1fec83d1a0769de6b9ce686c75657e66..8ecbefe31b81462239c572fbe23d21404442a177
(lane master HEAD; 4 commits: 84ea5b1 declare, b5d423f C1, e57f601 C2, 8ecbefe C1 follow-up).
Axes: operability (C1 gate repair), freshness (C2 field-performance knowledge). Read-only review;
no lane file, index, or jj state mutated. No installs performed; no network fetched.

## 1. File table (append-only / edited / unchanged)

Prefix method: old blob is a byte prefix of the new blob iff
`git cat-file blob A:<f>` bytes are a prefix of `git cat-file blob B:<f>` (checked in-memory with
python3 subprocess; no git state written). Exit 0 on all.

| File | Old→New bytes | Verdict | First divergence |
|---|---|---|---|
| PROVINCE.md | 4938→5060 | IN_PLACE (edit) | byte 1185 |
| SCORECARD.md | 53150→55114 | APPEND_ONLY | — |
| SKILL.md | 76889→77943 | APPEND_ONLY | — |
| corpus/QUALITY.md | 23806→25570 | APPEND_ONLY | — |
| corpus/README.md | 18895→19790 | IN_PLACE (insertions only) | byte 5684 |
| corpus/SOURCES.md | 32083→35523 | IN_PLACE (insertions only) | byte 19581 |
| scripts/citing_set.py | 24856→27617 | IN_PLACE (edit) | byte 1649 |

`git diff --name-status` over the whole tree: 13 additions (round-28 wave files,
`corpus/knowledge/field-performance-cwv.md`, `corpus/lessons/round-28.md`), the 7 modifications
above, no deletions, no renames. Per-commit scoping (`git diff --name-status` per pair):
84ea5b1..b5d423f touches only `scripts/citing_set.py` + 2 new verification JSONs;
b5d423f..e57f601 touches only corpus/province files + additions; e57f601..8ecbefe touches only
`scripts/citing_set.py`. Nothing else moved.

Scope checks (all pass):
- Only script changed: `scripts/citing_set.py` (diff of `scripts/` shows only it).
- Only knowledge entry added: `corpus/knowledge/field-performance-cwv.md`; the other 26 entries
  unchanged (no M under `corpus/knowledge`).
- No earlier wave file changed: diff of `.ufo/waves` lists only new round-28 paths; no
  round-26/27 file appears. Worktree has only untracked `??` wave artifacts (incl. untracked
  `round-26/__pycache__/` from counter runs — not a tracked change).

## 2. In-place edit judgments

- PROVINCE.md:24-29 (5+/3−): rewrite confined to the Field-performance Frontier clause; the
  closing rule "Ground moves to Core only with source-backed entries and a gate" kept verbatim,
  and the new text self-labels "knowledge only, no gate, no property measured" — the entry stays
  Frontier. Judged consistent (see §3).
- corpus/SOURCES.md: 7 insertions, 0 deletions. Rows S036–S039 inserted after S035 in id order
  (SOURCES.md:44-47), one Paths reading-path line (:58), one bounded question in the search log
  (:90). Mid-file insertion is why the byte-prefix test fails, but no prior row, rejection, or
  lead is altered; S018's rejection is restated and left rejected (:90).
- corpus/README.md: 12 insertions, 0 deletions: one coverage-table row (:43) plus an EOF
  round-28 section (:237-247). No prior row or "Known gaps" text altered.
- scripts/citing_set.py (64+/13−): static consistency judged line by line.
  - Docstring rewritten with the code (:31-73): FIFO/device refusal (:216-243, `os.open` with
    O_NONBLOCK + `stat.S_ISREG`, fd closed on every path, `import stat` present at :101),
    `corpus_directory_missing`/`corpus_empty`/`not_a_directory` in both sources
    (:249, :258-259, :360-361, :369-370), `population_id_unreachable` (:424-425, matches
    `id_key` returning `("n", n)` at :165-170 and the grammar that only produces `S<digits>`),
    top-level-root refusal (:295-313), and `revision is not None` at :701.
  - The `is not None` change is a real repair: `--revision ""` now reaches
    `_resolve`, which raises `revision_not_found` (:328-330) instead of silently measuring the
    working tree — closing a false-green path, matching the docstring's "blank or unknown".
  - Follow-up 8ecbefe (`_require_top_level`, :295-313) uses `rev-parse --show-prefix` emptiness,
    per its docstring accepting bare repositories and refusing nested roots; no realpath or
    whitespace-stripping comparison. Consistent with Git's top-relative paths used in `_git`.
  - No dead code left behind; every changed finding id is named in the docstring.

## 3. Contradiction checks — none found

- raw-200 rule: SKILL.md:65 "Raw `200` is not proof … trust `expect`, not status alone";
  `corpus/knowledge/free-read-verbs.md:69` concurs. The new entry defers to it explicitly
  (`field-performance-cwv.md:106`: "a raw 200 is not proof of a served page (`SKILL.md`)") and
  SKILL.md:695 uses final-200 only as the S038 eligibility exclusion, reporting "no field data",
  never pass/fail. No conflict.
- PROVINCE.md ownership lines: field-performance knowledge is inside "Owns: the domain
  knowledge" (PROVINCE.md:7); lab tools route to tabi (PROVINCE.md:32-34 vs entry :126-127);
  key custody routes to operator/kagi (PROVINCE.md:37-38 vs entry :127-128); source-hierarchy
  question left to chousa (entry :128-129). Frontier-to-Core rule retained (PROVINCE.md:27-29).
- Existing knowledge: `git grep -iE 'crux|core web vitals|\bLCP\b|\bINP\b|\bCLS\b|75th'` at the
  old commit hits only the old frontier mentions (PROVINCE.md:24, README.md:104), the rejected
  S018 row, and an unopened lead — no pre-existing entry states thresholds or CrUX claims to
  contradict. Thresholds are identical in all four new placements: SOURCES.md:44-47,
  SKILL.md:687-689, QUALITY.md:321-324, entry :9-10 (LCP ≤2.5s/>4s, INP ≤200ms/>500ms,
  CLS ≤0.1/>0.25, p75, 28-day window).
- SCORECARD.md appended section (:575-595) names the round-27 routed defects CLI-FIFO,
  CLI-SCOPE-FALSE-GREEN, JSON-PROTOCOL — all present in
  `.ufo/waves/round-27/unresolved-acceptance.json:27,35,44`. Internally consistent.

## 4. Not verified (residual risk)

- Runtime behavior: I ran no counter, selftest, or fixture; the declared 15/15 and 4/4 are L1's
  evidence, not re-executed here (main's verification job). My C1 judgment is static.
- `_resolve`'s `GIT_SUBPROCESS_ENV` and untouched hunks of `citing_set.py` were not line-audited;
  only hunks in the diff were reviewed.
- Retained source texts (`sources/a3/S036-39.txt`, receipts) verified present and committed, not
  content-checked against the live pages (no network authorization for this seat).
- Line numbers are worktree@8ecbefe numbers; tracked worktree files are clean versus HEAD, so
  they equal blob line numbers.

Verdict for the L1: no no-harm violation found on the corpus/script surface within this scope.
