# CriticCitationOverreach — residual attack on `scripts/citation_lint.py` (round 46, C2)

Seat: `CriticCitationOverreach`, wave `kake-r46-residual`. Target claim: the gate
"resolves every lane-commit citation over {SCORECARD.md, LOG.md}" and the
adjudication ledger classes what it suppresses. Method: independent token census
(781 TOKEN_RE matches across both files) with per-rule skip attribution, ground
truth via `git cat-file -e` on all 363 distinct tokens, per-line verification of
all 20 ledger rows, and an end-to-end synthetic battery run through the
committed CLI on a scratch repo (`/fast/scratch/hyaku/kake-r46-residual/CriticCitationOverreach/fixture/`).
Tool versions: git 2.56.0, gate at `ee43e663` (sha256 `3c78a0a8…`), lane tip `cd42e3c3`.

## Verdict

The claim fails twice on live population, and the exit-0 receipt is materially
softer than it reads: `resolves()` is not an existence check for 40-hex tokens,
and the ledger is a transcript of the gate's own flagged set, not an
independent enumeration of dead citations.

## Finding 1 — `git rev-parse -q --verify` does not check existence for full-40-hex tokens (gate defect, live miss)

`resolves()` (citation_lint.py:126-130) treats `git rev-parse -q --verify <tok>`
rc 0 as "object exists". Empirically on git 2.56.0:

    $ git rev-parse -q --verify deadbeefdeadbeefdeadbeefdeadbeefdeadbeef
    deadbeefdeadbeefdeadbeefdeadbeefdeadbeef   # rc 0
    $ git cat-file -e deadbeefdeadbeef…          # rc 1 — object absent

rev-parse validates a full hex token *syntactically* without opening the object
store. Consequence: every dead **full-40-hex** commit citation silently passes.
The selftest only plants a 7-char dead token (`dead = "e5455253"`), so the hole
is unexercised. Short tokens are unaffected (rc 1 on absent objects).

Live instance the gate misses: `SCORECARD.md:1111` cites
`` `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` (one commit, …)`` — context "one
commit" matches CONTEXT_RE, the token reaches `resolves()`, rev-parse returns
0, gate reports clean; `git cat-file -e` confirms the object is absent
(external ds4cc-marketplace commit, legitimately external — but excluded via
the buggy path, not via EXTERNAL_RE which does not match that line's words).
Its short form `7fc6aa2f` is ledgered as external; the 40-hex twin is not in
the ledger at all and is adjudicated by nothing.

Synthetic battery (committed CLI, scratch repo): a dead 40-hex on a context
line produces **no violation** while the adjacent dead 7-hex is flagged:

    measured at commit `deadbeef…deadbeef` per this line.   → silent
    report cites commit `deadbe0` which does not resolve.    → flagged

Secondary effect: `resolves()` accepts **any** object, not commits
(`rev-parse <sha>` succeeds for blobs/trees/tags). `d17ab7e5` and three
counter-blob sha256s in the population resolve as blobs — correctly used there,
but the gate cannot distinguish "cited commit exists" from "a blob of that id
exists". A dead commit hash that happens to collide with any live object id
also passes.

## Finding 2 — case-sensitive CONTEXT_RE + dead full-40 → `SCORECARD.md:1572` missed

`CONTEXT_RE` is compiled without `re.I`, so the corpus' conventional
"Base \`<hex>\`" heading form supplies no context. Live:
`SCORECARD.md:1572` — ``Base `b720d79976a1fb8fe6a8eb4b9f50e946b0cd5e07` `` —
is a dead commit citation (the disclosed L1 typo'd base hash; the real commit
is `b720d799ae99c19a…`, and the very next lines say the written hash "is
wrong"). The gate's contract is mechanical — dead citation → violation or
ledger row — yet this is neither: `Base` ≠ `\bbase\b`, so no-context skips it.
Even with context restored it would survive via Finding 1 (full-40). Two
independent defects stack on one live line. The ledger has no row for it
either — the disclosed typo is unadjudicated dead citation debt.

## Finding 3 — the ledger was built from the gate's own flagged list (provenance)

The C2-before receipt (`verification/c2-before-7cdbaefd.json`, run at base
`7cdbaefd` where the ledger is absent) lists exactly 28 violations — the
20 ledger rows' citing occurrences, nothing else. So the ledger enumerates the
gate's flagged set, while the much larger dead-citation corpus the exclusions
swallow (100 ellipsis, 90 digest-word, 32 no-context, 13 external-word,
9 pin-word, 18 digits — dead-token occurrence counts from my census) was never
adjudicated. Examples of dead, commit-cited, **non-ledgered** tokens kept green
only by incidental rules:

- `a8f1e2b` (LOG:50,51,108) — same 2026-09-28 push series whose siblings
  `b74190e`/`d69dd22`/`0c767c2`/`b9db4b1` are ledgered; saved by the word
  "sha" at :50 and the one-line context window at :51/:108.
- `e82a262` (LOG:107), `61d0ce6` (LOG:52), `84bade0` (LOG:591, fleet root —
  "fleet root" misses `fleet repo`), `efc1830` (LOG:6, saved by "pin"),
  `1fbdb8ed`, `c2-matrix.json` blobs are fine, but sandbox control commits
  `489714be`, `b6580c79`'s siblings `e5263d41`/`ae9fb361`/`dce145db`/
  `79277c9f`/`c2e38e5d` (SCORECARD:1459-1497), `e068bc4b` (:1566),
  `bf9b2089` (:1755), `da09e6c7` (:1948), `03a0f94c` (:3868, "(fleet
  03a0f94c)" — one word short of `fleet repo`), and the all-digit
  `04848219` (:1458/:1492 — suppressed by the digits rule AND no-context).
  Any reflow, wording edit, or `git grep`-style recheck that adds a context
  word turns each into a fresh violation — the clean verdict rests on
  wording luck, not on disposition.

## Finding 4 — ledger-key overreach: (token, file) suppresses every occurrence

`load_adjudications` keys rows `(token, file)`; `scan` consults the key before
resolving. Confirmed end-to-end: two `deadc0de` commit citations on different
lines — only the first covered by the row's reason — are **both** reported
adjudicated. A later line citing the same token as genuine lane provenance is
silently suppressed. Live shape exists: `0cce15f0` at SCORECARD:1457 (named
control — matches row) and :1458 (round-34 *shape* reference inside another
row) both report the same "Round-34 hollow-control commit" class.

## Finding 5 — digits rule is unsound for commit hashes (live instance)

`if not re.search(r"[a-f]", token): continue` assumes real hashes contain
letters. `04848219` (SCORECARD:1458/:1492) is a cited all-digit sandbox control
commit — dead, unadjudicated, suppressed twice over (digits + no-context).
Probability that a uniform 7-hex has no a-f digit: (10/16)^7 ≈ 3.7% — the rule
will keep eating ~1-in-27 dead short citations.

## Finding 6 — ellipsis rule asymmetric across `X…Y` / `X...Y` (live shape)

`…`/`...` after a <40-hex token → treated as digest prefix. In
`b74190e…a8f1e2b` (LOG:108) the head token is swallowed as a "digest" while
the tail `a8f1e2b` is only saved by no-context — for git range syntax both are
commits. Also `…`-suffixed fragment tails of any kind ≥7 chars (e.g.
`749ef6a6…77b63aa6`, SCORECARD:2345) are exempt from the ellipsis rule
entirely (it only inspects the token's right edge).

## Finding 7 — context window is one physical line (live instances)

`context_line = line if CONTEXT_RE.search(line) else prev_line`. Wrapped
citations die two lines below the context word (`a8f1e2b` LOG:51 —
context at LOG:48) or carry it on their own line only. Markdown's
line-wrapping convention guarantees this keeps biting.

## Secondary observations (contract-loose, not independently fatal)

- `--revision` mode: `resolves()` checks presence in the *current* object
  store, not ancestry of the measured revision — a forward-dated commit
  citation "resolves" at the before-revision. The C2 criterion's own
  precedent (round-45 lesson) used `git merge-base --is-ancestor`.
- Ambiguous-but-valid prefixes: a short hex naming two live objects fails
  rev-parse → false violation. No live instances found.
- `7fc6aa2f` ledger row is real but inert at 5 of its 6 citing lines (pin-word
  / no-context / external-word win first) — benign given correct class.
- All 20 ledger rows verified individually: token occurs in the named file,
  `cat-file -e` confirms absent, and the asserted class matches every citing
  line's text (task said 12 rows; the ledger now has 20 — all checked). The
  `e5455253` pair correctly quotes the r45 defect (real commit
  `e54552553eaff4d7…`, live at `e5455255`). **No false class found** — the
  ledger's stated classes are accurate; its coverage and granularity are the
  problem.
- `Base83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba` (SCORECARD:544, LOG:1068):
  41-char glued token invisible to TOKEN_RE; commit exists, so formatting wart
  rather than dead citation — noted because the glue pattern is the same class
  that hid the `b720d799…e07` typo.

## Smallest safe corrections

1. `resolves()`: `git cat-file -e <tok>^{commit}` (existence + commit type in
   one probe); in `--revision` mode use
   `git merge-base --is-ancestor <tok> <rev>` for the strict reading, or
   document object-store presence as the contract.
2. `CONTEXT_RE`: add `re.I`.
3. Digits rule: drop it or require ≥2 a-f chars *and* a non-commit context —
   `12345678`-shaped commits are legal hex.
4. Ellipsis rule: only skip when the token is *adjacent* to a longer hex run or
   explicitly marked digest context (e.g. `sha…`-shaped pairs), or treat `X…Y`
   with both sides hex-shaped as a range and check both.
5. Ledger keys: `(token, file, line)` — the rows already name one citing line
   in spirit; make the key match. Then re-audit the dead-token corpus this
   report lists (the ~30 unadjudicated dead commits above) and either add
   rows or reword the citing lines.
6. Selftest: plant a dead full-40 token, a `Base`-capitalized line, an
   all-digit commit, a wrapped citation (context N-2), and a two-line
   ledger-suppression fixture.

## Impacted axes

- Operability: the gate is silently blind to the most common citation length
  (full 40-hex) — its core check is a format check. Before/after receipts
  remain true as *records*, but "0 violations" overstates verified hygiene.
- Freshness: live dead citations survive unadjudicated (`b720d799…e07`,
  `7fc6aa2f…0884`, `a8f1e2b`, `e82a262`, `61d0ce6`, `84bade0`, `efc1830`,
  `04848219`, `e5263d41`, `ae9fb361`, `dce145db`, `79277c9f`, `c2e38e5d`,
  `489714be`, `e068bc4b`, `bf9b2089`, `da09e6c7`, `03a0f94c`, `5f767534`@1454).
- Quality/provenance: ledger completeness claim is weaker than implied —
  derived from the gate's flagged set, keyed too coarsely.

Artifacts: census + existence maps under
`/fast/scratch/hyaku/kake-r46-residual/CriticCitationOverreach/`
(`census.py`, `census.json`, `exists.json`, `fixture/`).
