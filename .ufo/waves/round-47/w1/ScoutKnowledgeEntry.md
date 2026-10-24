# ScoutKnowledgeEntry — commit-citation-hygiene provenance trio + S136 usage

Seat: ScoutKnowledgeEntry (scout, wave 1, freshness axis). Read-only audit; no files modified except this report. Lane repo only.

## Verdict

**PASS on the assigned question, with one bounded precision caveat.** The entry confines the resolution rule to repository-local object names and nowhere claims a dead token is globally nonexistent. The caveat: the gloss "uniqueness, not length, is the resolvability test" is verbatim-faithful to S136 but omits Git's observed minimum-abbreviation floor — empirically a unique 3-hex prefix does not resolve here.

## Evidence

### Provenance trio (entry lines 1–3)

- Convention matches sibling entries (`corpus/knowledge/receipt-integrity.md:1-3` uses the same `source:` / `verified-at:` / `recheck:` front matter).
- `verified-at: 2026-10-24` matches the S136 fetch receipt `.ufo/waves/round-47/sources/receipts.log` (`GET https://git-scm.com/docs/gitrevisions  2026-10-24T06:31:20Z / HTTP_STATUS=200 BYTES=74526 exit=0`) and today.
- `recheck:` line names the lane's actual resolution probe, `git rev-parse -q --verify <token>` — the same invocation the gate uses at `scripts/citation_lint.py:128`.
- Freshness: `git log -- corpus/knowledge/commit-citation-hygiene.md` → `846138c` (add) and `59146c9` (scope-note amend), both 2026-10-24. `git status --porcelain` on the entry and `corpus/SOURCES.md` → empty (committed, unmodified). `git cat-file -e cd42e3c3…:corpus/knowledge/commit-citation-hygiene.md` → exit 128, "exists on disk, but not in 'cd42e3c3…'" — new round-47 artifact, absent at frozen base. `git merge-base --is-ancestor cd42e3c3 HEAD` → exit 0.

### S136 receipt and quote fidelity

- `sha256sum .ufo/waves/round-47/sources/S136.txt` → `33a99ba212228d6968e7721a87197558b0e88a450ecfc303eaa34d8321d2da8c`; `wc -c` → 74526. Matches `corpus/SOURCES.md:144` anchor (`…fetched 2026-10-24T06:31:20Z, HTTP 200, 74,526 bytes, retained text sha256 33a99ba2…2d2da8c`) and `corpus/lessons/round-47.md:63-69`.
- The entry's quoted phrase `"a leading substring that is unique within the repository"` is verbatim at `S136.txt:2180`, inside the `<sha1>` `<dt>` entry whose `<dd>` reads (lines 2181-2184): "The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique within the repository." — matching the row anchor ("paragraph beginning 'The full SHA-1 object name'").
- S136 row scope cell limits the source to "Git's own revision-token abbreviation and resolution semantics only; not a claim about any hosting platform"; the entry uses it only for object-name semantics — no out-of-scope absorption observed.

### Repository-local scoping (the assigned check)

- Line 24: "Dead-token verdicts are repository-scoped, never universal." Line 25: "`e5455253` … is dead **in this lane repo**". Lines 28-29: external-repo tokens "can never resolve here" — all verdicts carry an explicit repository scope; no sentence asserts global nonexistence.
- Empirical (read-only): `git rev-parse -q --verify e5455253` → exit 1; `git rev-parse -q --verify e54552553eaff4d7` → exit 0, `e54552553eaff4d7033dc2df299300fc056f4a0d` — the full commit named by `corpus/lessons/round-45-verifier-spotcheck.md:68` and `round-46-verifier-spotcheck.md:38`.
- `git cat-file --batch-all-objects --batch-check | grep -c '^e5455253'` → **0**: the token is dead here by *absence*, not ambiguity. (Ambiguity is the second way a prefix dies, per `round-46-verifier-spotcheck.md`'s logic; not exercised here.) The converse claim "may resolve in another repository" is not testable inside lane bounds — marked [INFERENCE] only as a direction the rule permits; no sibling repo was opened.
- External-repo ledger classes named at lines 30-34 exist: `corpus/quality/citation-adjudications.md:10-11` shows `quoted-dead-token` for `e5455253` in SCORECARD/LOG; grep of the ledger confirms the `external-repo` classes.

### Scope-note honesty (lines 54–65)

- The §"What the gate cannot prove" + residual-scope note correctly disclaim complete citation-hygiene certification. Consistent with gate internals: `scripts/citation_lint.py:40` `TOKEN_RE = …([0-9a-f]{7,40})…` is lowercase-hex only (case-sensitive extraction, matching the "misses `Base`" caveat family), and population is `{SCORECARD.md, LOG.md}` (`:37`). `corpus/QUALITY.md:1071-1072` contain both criteria the entry cites.

## Adversarial caveat (bounded, low severity)

"Uniqueness, not length, is the resolvability test" (lines 18-19) and the row teaches ("uniqueness, not length, is what makes a short hash resolve") omit a length floor the retained source does not state. In this repo's object store: `00b` is a unique 3-hex prefix containing a-f, yet `git rev-parse -q --verify 00b` → exit 1; a unique 4-hex prefix `0001` → exit 0 (`000129bc91…`). `grep -ni 'minimum\|abbrev' S136.txt` finds no minimum-length qualification (only the `describeOutput` entry's "abbreviated object name", line 2189). So Git applies an unwritten ≥4-hex floor the source text doesn't mention. Impact: nil for the gate (TOKEN_RE matches 7–40 only) and for every cited consequence (all examples are 7–8 hex), but the categorical gloss overstates the source. Suggested future tightening, not a falsification.

Minor rhetorical note: "Tokens naming an external repository … can never resolve here" (line 28) is shorthand — a coincidental object *could* resolve; the entry self-covers at lines 56-58 ("only that it is *a* commit here"), so the imprecision is contained.

## Remaining unknowns

- Whether `e5455253` resolves in any other repository (untestable without leaving lane bounds; claim is permissive only).
- Whether future gitrevisions edits add a minimum-length clause; the `recheck:` field already covers re-opening on syntax changes.

Checks not run: none beyond the two declared out-of-scope items above. All commands were read-only (`rev-parse`, `cat-file`, `merge-base`, `log`, `status`, `sha256sum`, `wc`, `grep`, `awk`).
