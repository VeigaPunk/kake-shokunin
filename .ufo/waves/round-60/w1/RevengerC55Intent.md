# RevengerC55Intent

Claim C2 / R59-D1 intent. Read-only reconstruction at base `97cdc12` (round-60 open). Method: source and contract
reading plus a scratch prototype of the round-60 contract's C2 rule (`RevengerC55Intent.files/proto_guard.py`) run
against committed lane bytes; `scripts/append_guard.py` does **not** exist at `97cdc12` (`ls` → absent), so nothing
below is a run of the tool that is being built this wave. The only lane code executed was the frozen
`c55_readme_index.py` (read-only, committed bytes). Nothing was installed; no pacman run.

## INTENT:

**The term.** `head_changed` (c55 v2.1, `.ufo/waves/round-55/c55_readme_index.py:194-200`) is a byte-prefix test:

```
old = git show BASE_REV:corpus/knowledge/<rel>; new = git show <rev>:...
if not new.startswith(old): head_changed.append(rel)
```

Its docstring states the intent in one clause (`:30-31`): "files present at the base revision whose full base text
is not preserved byte-for-byte as a prefix at the measured revision (**entries change only by appended text**)". The
base is a frozen constant, not a CLI argument (`:60 BASE_REV = fcaf4b85…`, `:130`), so the invariant is measured
against the round-55 tree for every later round.

**What it was built against.**
- v2 (`git show 2bda8e4:.ufo/waves/round-55/c55_readme_index.py:192-198`) was the same test over `old[:1500]`. Its
  motivating attack is the w1 list in the docstring (`:14-16`): "entry-edited-to-fit" — a junk coverage cell made
  true by rewriting the entry's head instead of the row.
- v2.1 widened it to the whole base text (`contract.md:111`, "kills body truncation") after w2
  `CriticJunkC1.md:32` V7: truncating every knowledge body to 1 500 chars, index untouched, **passed** v2 with
  `47 files changed, 46 insertions(+), 5894 deletions(-)`.
- It is explicitly **not** an immutability test: selftest `:330 pass_entry_appended_correction` accepts appended text,
  and w2 `MutC1V2Counter.md:34` M22 shows the mutant `new != old` is killed by that same case.

So the protected invariant is: **a knowledge entry is an append-only record — base bytes survive unchanged and in
order, and everything new sits after them.** Two sub-properties: (a) no silent rewrite (anti "edit the file to fit the
row"), (b) no shrinkage (anti "delete the text the row describes"). The "after them" placement clause is the only part
that speaks about *where* added text may go, and it is the clause the round-59 contract collided with.

**The round-59 collision.** `c59_quote_truth.py:656-662` requires the correction inserted where the stale bullet ends
(`i1 == end and end <= s + 1 + STALE_WINDOW`), i.e. mid-file (`contract.md:73`, `:81`, `:127`). The landed correction
is 16 inserted lines starting at line 35 of `corpus/knowledge/crawler-identity.md` (`git diff -U1 fd6303ce 97cdc12`),
first line `  **[r59-correction 2026-10-27]** The claim in the bullet above is wrong as stated: …`; the diff carries
`+` lines only, so the stale bullet is intact. Observed at the round-60 base:
`c55_readme_index.py --root . --revision 97cdc12` → `index_mismatches=1 … head_changed=1: crawler-identity.md`, exit 1
(`RevengerC55Intent.files/c55-at-97cdc12.txt`). The collision was predicted before data
(`.ufo/waves/round-59/w1/ExecHistoricalGates.md:80-89`), recorded as harm (`.ufo/waves/round-59/a2r1/ReviewerNoHarm.md`,
HARMS ¶1) and as the lesson row `corpus/lessons/round-59.md:175`; the row is now `historical from round 59` with pin
`64c0ce12…` at `SKILL.md:1233`.

**Does a tagged in-file correction violate that intent?** No on substance, yes on the letter.
- Substance: nothing is rewritten or deleted; the base text survives in order and the stale sentence stays present
  (the round-60 C9 restates this: "the base line holding `these fetchers ignore robots.txt rules.` is still present").
  Both sub-properties (a) and (b) hold.
- Letter: it violates "entries change only by appended text" — the addition is not at the end. The *reason* for the
  placement clause is auditability: an untagged mid-file insertion is indistinguishable from original prose, whereas
  an appended tail is visibly a later layer. The guard replaces that mechanism with a stronger one (the insertion must
  open a run and must carry a rendered, dated, round-tagged marker) — it buys back the auditability the prefix rule
  got for free, at the cost of permitting the insertion at all.

## PROTECTIONS:

Each protection `head_changed` carried, and whether the round-60 guard keeps it. "Observed" = the scratch prototype
of the contract rule on real lane bytes (`RevengerC55Intent.files/rule-cases.txt`, `r1-sweep.txt`).

| # | Protection | Where it lives in c55 | Kept by the guard? | Evidence |
|---|---|---|---|---|
| P1 | No byte-level rewrite of any base line (incl. trailing space, CRLF, one-word edits) | `:194-200`; selftest `:327 fail_head_edited_to_fit` | **KEPT** | base must be an ordered subsequence → any altered line breaks it: K4/K13/K14 and a real head-word edit all read `changed` (observed) |
| P2 | No deletion / body truncation (the v2.1 hardening, V7) | `contract.md:111`; selftest `:351 fail_body_truncated` | **KEPT** | truncating the real `crawler-identity.md` at 1 500 chars → `changed` (observed); whole-file loss → `deleted` (K6/K7/K18) |
| P3 | No reordering of base lines | same test | **KEPT** | K12 swap → `changed` (observed) |
| P4 | No **unmarked** insertion | same test (blanket: no mid-file insertion at all) | **RELAXED BY DESIGN**; the marked form is kept and strengthened | K2 accepted, K3/K8 (tag not first in run) rejected, K9/K10 (tag hidden in comment / code span) rejected, K15 accepted only because a tagged alignment exists (all observed) |
| P5 | Contiguity: base bytes are one uninterrupted block, so additions are visibly at the tail | same test | **LOST by design**; residual risk | run granularity: with a base that predates the tag, an untagged line placed next to the tag rides inside the same run. Observed on real bytes: base `fd6303ce`, one untagged line inserted after the r59 tag → **accepted**, while `head_changed` flags it. Same insertion against base `97cdc12` (rolling base) → **`changed`** (observed). Closed by scoring a second real-lane case at `--base 97cdc12`; the contract scores only R1 (`--base fd6303ce`). |
| P6 | Scope: every base blob under `corpus/knowledge/`, any extension | `:130-200` iterates `ls-tree -r` | **LOST unless scope widens** | base holds 56 blobs: 53 `.md` + `accessibility-review-cards.json`, `freshness-pins.json`, `freshness-sidecar.json`; the contract's default scope is `corpus/knowledge/**/*.md`. K17 (out-of-scope `SKILL.md` → 0) shows the scope is deliberate, so the json files need an explicit `--scope`. |
| P7 | Cumulative window: measured against a frozen round-55 base forever | `:60`, `:130` | **CONDITIONAL** | the guard's base is a CLI argument; R1 pins `fd6303ce`, not `fcaf4b85`, so the guard as specified does not reproduce c55's window. Only a run at `--base fcaf4b85…` does, and the contract scores none. |
| P8 | Enforcement: the term sits inside a frozen predicate with a historical pin and a SKILL row | `SKILL.md:1233`; C1 population | **CONDITIONAL** | the guard is a tool until `c60_guard_cases.py` lands 24/24 (R1/R2); C1 must keep the row historical + pinned, which it already is. The guard does not turn c55 green — the supersession is of intent, not of exit code. |

Feasibility of the contract's own R1 expectation: the prototype run over all 56 base blobs (`fd6303ce` → `97cdc12`)
returns **0 findings** (`r1-sweep.txt`) — only `crawler-identity.md` differs among base blobs; the other two changed
paths are new at the revision and out of scope. So R1's expected exit 0 is consistent with the rule, not in tension
with it.

What the guard adds that `head_changed` never had: the marker must be *rendered* prose (not an HTML comment, not a
backtick span) and must open the run; the verdict is existential over alignments, so a deletion-plus-reinsertion
cannot masquerade as an insertion (K16 observed `changed`). What it cannot test, and `head_changed` could not either:
whether a tagged run is a *faithful* correction (the contract says so explicitly) — that stays a reviewer term.

## VERDICT:

A tagged in-file correction violates only the placement clause, not the substance: base bytes survive in order, nothing
is deleted, and the addition is marked and dated — exactly what the prefix rule was for. P1–P4 are kept. P5 is a
residual of run granularity that a rolling-base real-lane case closes (observed: the same untagged insertion is
accepted against `fd6303ce` and rejected against `97cdc12`). P6 needs `--scope` widened past `**/*.md` for the three
json blobs. P7 is not reproduced by any scored run and should be recorded as dropped, not claimed.

VERDICT: supersede is sound for P1–P4; P5/P6/P7 are real protection losses that need the three named counter changes before the guard can be called a full replacement.
