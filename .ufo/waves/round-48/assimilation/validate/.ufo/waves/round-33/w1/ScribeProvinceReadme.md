# w1 — ScribeProvinceReadme (r33 build lane; axes: operability + freshness)
Built append-only docs, not product code: a PROVINCE count correction (round-32 routed item 5) and a Round-33
note for PROVINCE + corpus/README.md on the ds4cc pin move and the citing-set refusal-code repair. No lane
file written but this report; additivity proved in a sandbox clone.

Spec count (the attack on "five"):
```
$ ls -1 scripts/fixtures/citing-set-hostile/ -> 6 dirs, each one hostile.json: P1-selftest-argv,
  P2-fixture-dot-git, P3-commit-without-init, P4-expected-json-guard, P5-symlinked-case, P6-commit-before-init
$ ls -1d scripts/fixtures/citing-set-hostile/*/ | wc -l -> 6  |  git ls-tree b1752a2 <dir> | grep -c '^' -> 6 (5777d5a -> 6)
$ nl -ba PROVINCE.md | sed -n '122p' -> "containment for five hostile fixture shapes
  (`scripts/citing_set_hostile_selftest.py`);"   identical at bc6c4a8:122
```
"six" holds and line 122 is stale; the draft leaves it alone and corrects it in an appended paragraph (defect
text: corpus/lessons/round-32-verifier-spotcheck.md:136).

Freshness facts the note asserts, re-derived here rather than copied from the entry:
```
$ git clone -q https://github.com/VeigaPunk/ds4cc-marketplace.git upstream   exit 0
$ show -s --format='%H|%ci|%s' 7fc6aa2f -> 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 |
  2026-10-21 17:32:55 +0000 | magga: Frostbite — Classic & Remastered at /magga/frostbite/
$ diff --stat 1fbdb8ed 7fc6aa2f -> 12 files, 3734 insertions(+); sitemap.xml -> 3 added <loc>
  (new lines 15-17), locs 97 -> 100; the four S062 files -> empty diff (unchanged)
$ cat-file blob vs retained bytes -> 4/4 IDENTICAL, mode 100644 (67d8c7a5, e0d9ee29, 12c58e2d, 4e6d70ae)
$ ~/Projects/ds4cc-marketplace: HEAD 1fbdb8e, cat-file -e 7fc6aa2f -> absent (never fetched into)
```
C1 shape at b1752a2: citing_set_selftest.py:395-396 two-line guard raising `CaseRefusal("setup_commit_before_init",
..."needs an earlier 'git_init'")`, apply-time `setup_commit_without_repo` at :523, `"code"` in result rows at
:563,:595,:757. Receipts read, not re-run by me: c1 2/4 at bc6c4a8 → 4/4 guard_ok true, benign 45/0 at b1752a2;
c2 0/4 → 4/4 (sitemapLocs 100, three `clean`). S065: 11 cells, kind code, tier A, status mined, opened 2026-10-22, used-by
names sitemap-orphan-audit.

Additivity gate (sandbox clone at b1752a2 only): `node clone/scripts/corpus-contract.mjs` exit 0,
output byte-identical to the clean run ("0 findings · 27 knowledge entries · 27 lane lessons · 17 skipped ·
0 errors"); numstat `66 0 PROVINCE.md`, `26 0 corpus/README.md`; `diff -U0 | grep -c '^-[^-]'` -> 0.
Targets: end of PROVINCE.md:131 and end of corpus/README.md:301.

## Draft — province.md (append at end of PROVINCE.md; reflowed below, byte-exact in sandbox)
<!-- Draft: append only, after PROVINCE.md:131 (current end of file). Append-only rule: the round-31 sentence at PROVINCE.md:122 stays as written; this section corrects its count and records the round-33 step. -->

## Round-33 citing-set refusal codes and ds4cc source pin

The round-31 sentence above — "the citing-set fixture runner gained containment for five hostile fixture shapes" (`PROVINCE.md:122`) — is historical for its date and is not the present count: `scripts/fixtures/citing-set-hostile/` holds six shapes, P1–P6, each a directory with one `hostile.json` (`P1-selftest-argv`, `P2-fixture-dot-git`, `P3-commit-without-init`, `P4-expected-json-guard`, `P5-symlinked-case`, `P6-commit-before-init`); P6 came in round 32. This paragraph is the correction routed as round-32 item 5; whether it closes is the non-author closure's call, not this text's.

Round 33 repaired P6's dependence on message text (round-32 routed items 2 and 3). In `scripts/citing_set_selftest.py` the load-time guard keeps its two-line shape (`if step["op"] == "git_commit" and not initialized:` then one `raise`); that raise is `CaseRefusal("setup_commit_before_init", …)` and its message still carries the unchanged fragment "needs an earlier 'git_init'". The apply-time re-check raises a different code, `setup_commit_without_repo`. The runner reports a `code` per refusal; `scripts/citing_set_hostile_selftest.py` accepts an optional spec key `reason_code`, and `scripts/fixtures/citing-set-hostile/P6-commit-before-init/hostile.json` pins `"reason_code": "setup_commit_before_init"` instead of matching message text. The four-variant counter `.ufo/waves/round-33/c1_code_probe.py` reports met 4 of 4 at `b1752a2` — pristine pass, reworded guard message pass, m3 (guard deleted) killed, recoded code literal killed, `guard_ok` true, benign 45 cases 0 failed — against met 2 at base `5777d5a` (reworded failed P6, recoded not applicable). Receipts: `.ufo/waves/round-33/verification/c1-at-bc6c4a8.json` and `c1-after-b1752a2.json`. What the check does not cover: a runner without the Git pins still passes it, so a green run is not a Git-escape guarantee.

The corpus' ds4cc-marketplace source pin advances from `1fbdb8ed` to upstream `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` (2026-10-21T17:32:55Z, "magga: Frostbite — Classic & Remastered at /magga/frostbite/"; one commit, 12 files, 3 734 insertions). That commit adds three pages under `/magga/frostbite/` (hub, `classic/`, `remastered/`) with their scripts and covers, links them from `magga/index.html`, and adds three `sitemap.xml` locs (97 → 100, lines 15–17); it changes none of the four files recorded with S062 (`render.yaml`, `apps-sdk/Dockerfile`, `apps-sdk/src/server.ts`, `.dockerignore`). The corpus now records this as source row S065 in `corpus/SOURCES.md` (status mined, opened 2026-10-22, used by `corpus/knowledge/sitemap-orphan-audit.md`) and as that entry's "Round-33 ds4cc source pin 7fc6aa2f" section, whose `sitemap-locs: 100` line and three `canonical <url>: clean` lines are re-derived from the retained bytes with the revision's own `scripts/canonical_audit.py` by `.ufo/waves/round-33/c2_pin_count.py` (met 4 of 4 at `b1752a2`). The retained bytes are four files at `.ufo/waves/round-33/sources/ds4cc-7fc6aa2f/`, mode 100644, byte-identical to the upstream blobs (`sitemap.xml` `67d8c7a5`, `magga/frostbite/index.html` `e0d9ee29`, `magga/frostbite/classic/index.html` `12c58e2d`, `magga/frostbite/remastered/index.html` `4e6d70ae`, abbreviated).

No Frontier bullet closes here: the sitemap/orphan entry stays held ground one commit fresher, the refusing-code repair changes the lane's own fixture runner and not a domain gate, and no ground moves to Core.

Limits: source-side only. Nothing was fetched from ds4cc.com or any other owned property, so whether this commit is deployed and what the live sitemap lists is not known from this section; `clean` is the lane's offline canonical policy on each page's own head link, not a search-engine selection. The local checkout `~/Projects/ds4cc-marketplace` stays at `1fbdb8ed` and was not fetched into. Accessibility conformance, live Render deploy semantics and the operator restore-or-retire queue above stay open as stated.

---
## Draft — readme.md (append at end of corpus/README.md; reflowed below, byte-exact in sandbox)
<!-- Draft: append only, after corpus/README.md:301 (current end of file). -->

## Coverage — round 33 (2026-10-22)

| Area | Entry | Coverage |
|---|---|---|
| ds4cc source pin 7fc6aa2f (r33) | `knowledge/sitemap-orphan-audit.md` section "Round-33 ds4cc source pin 7fc6aa2f"; row S065 in `SOURCES.md` | The corpus' ds4cc-marketplace reads move one commit, from `1fbdb8ed` to upstream `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` (2026-10-21T17:32:55Z): three new pages under `/magga/frostbite/` (hub, `classic/`, `remastered/`) with their scripts and covers, linked from `magga/index.html`, and three `sitemap.xml` locs added (97 → 100, lines 15–17). Four files are retained byte-identical at mode 100644 under `.ufo/waves/round-33/sources/ds4cc-7fc6aa2f/`; the four S062 files are unchanged. Source-side only: `sitemap-locs: 100` and three `canonical <url>: clean` verdicts are re-derived offline from the retained bytes with `scripts/canonical_audit.py`. |

Round 33 also repaired the citing-set refusal check. The load-time guard in `scripts/citing_set_selftest.py` raises the structured code `setup_commit_before_init` (its message keeps the fragment "needs an earlier 'git_init'"), the apply-time re-check raises `setup_commit_without_repo`, the runner reports a `code` per refusal, and the P6 hostile spec names it through `reason_code` instead of matching message text. This is the round-32 routed items 2–3 repair. Round-32 routed item 5 — "five hostile fixture shapes" at `../PROVINCE.md:122` — is corrected in `../PROVINCE.md` §Round-33: the directory holds six, P1–P6.

The pin move adds no new domain knowledge: the same sitemap/orphan capability, one commit fresher, and no coverage-map area moves; the refusing-code repair is lane-tooling operability, not domain coverage. `clean` stays the lane's offline canonical policy on a page's own head link, not a search-engine selection, and nothing was fetched from ds4cc.com, so deployment state and the live sitemap stay unknown. Accessibility conformance, live Render deploy semantics and the operator restore-or-retire queue in "Known gaps" are unchanged by this round.

---

## Paths, limits, not verified
- Sandbox (absolute): province.md sha256 9346e4db…7bb4a; readme.md sha256 bc020104…e4494; append patch
  province-readme-append.patch sha256 2a5b2bd5…86d4; reflowed province.compact.md / readme.compact.md
  (pasted above); clone/ at b1752a2 with drafts applied only there.
- Not verified: I did not run c1_code_probe.py, c2_pin_count.py or the hostile selftest — receipts are the
  L1's, quoted as such; nothing about what ds4cc.com serves (no owned property fetched); the 97-loc prior
  count is from the local checkout at 1fbdb8ed, not upstream bytes; corpus-contract.mjs reads neither
  PROVINCE.md nor corpus/README.md, so no lane gate covers them.
- L1: never edit line 122; land both appends with their headings so the correction is dated. Tooling:
  no installs/updates (node v24.21.0, python3 pre-existing); one network git clone of the public
  ds4cc-marketplace repo into the sandbox, nothing else.
