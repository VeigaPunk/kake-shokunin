# ScribeQualityCriteria — round 35 wave 1 report

Behavior: drafted `## Round-35 criteria` with four criteria, each carrying Reject, Grounding,
a check command and a Limit. Deliverable stays in the sandbox; this report is the only lane
file written. No product code, counter, judge, commit or lane ref touched; no subagents.

Deliverable: `/fast/scratch/hyaku/kake-r35/w1/ScribeQualityCriteria/quality.md` (123 lines,
4 criteria, 4 `Check` and 4 `Limit` occurrences).

Commands (sandbox clone /fast/scratch/hyaku/kake-r35/w1/ScribeQualityCriteria/clone):
- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin clone` exit 0;
  `git -C clone checkout -q 318561efa67206699fdaf259ffb86e39f2d916a8` exit 0;
  `git -C clone rev-parse HEAD` → `318561ef…` exit 0.
- `git merge-base --is-ancestor 81d9fd74f1460ba8cff007fc42f8fb8265aa2d4d 318561efa67206699fdaf259ffb86e39f2d916a8`
  exit 0; `git merge-base --is-ancestor 16a6b8b8144f4d6e6187e9ecbb4fb5f4528b911a 81d9fd74f1…` exit 0.
- `git fetch -q .ufo/waves/round-34/retained/r34-c1-lookup-dcef39b5.bundle 'refs/heads/*:refs/heads/r34/*'`
  exit 0, `refs/heads/r34/lookup-c1 dcef39b5f4e8373970eb74858d2c6175524cdfd0`.
- `git show dcef39b5:scripts/link_preview_audit.py` exit 0: line 8
  `files[p] = open(p, encoding="utf-8", errors="surrogateescape").read()`, line 12
  `h.update(rel.encode() + b"\0" + files[rel].encode("utf-8", "surrogateescape") + b"\0")`.
- `git show a2fe31b:.ufo/waves/round-34/verification/c2-at-d08d8de.json` exit 0:
  `revision d08d8de26c9a4290c44282b0eee2b860e8ea4ecc`, `census.derived` pages 102, og:title 87,
  og:type 87, og:image 1, og:url 87, all-four 1, og-url-equals-canonical 87.
- `git cat-file -e d08d8de:.ufo/waves/round-34/verification/c2-at-d08d8de.json` exit 1
  ("exists on disk, but not in 'd08d8de…'").
- `git show ce72dd1b:corpus/knowledge/link-preview-metadata.md | grep -n ds4cc-7fc6aa2f-og-census`
  → `128:ds4cc-7fc6aa2f-og-census: pages=102 …` exit 0.
- `git show a2fe31b:.ufo/.../c1-at-d08d8de.json` exit 0: `passed` 0 of 28; contains neither
  `102` nor `87`.
- Receipt field dump over the ten `.ufo/waves/round-35/verification/control-*.json` (exit 0):
  C1 base 14/24, declaration 14, lookup 7, constant clean 7, all target 22, all exit 1;
  C2 base/declaration/hollow 0 of 12, junk 0, keyword 3, transcript 8, target 9; transcript
  `copiedShare` 0.9951, `words` 1303; counter sha256 `c4d58dae…49ef` in all ten.
- `grep -nE '^\| *(canonical-audit|base-path-audit)' SKILL.md` → 411, 725; registry header 409;
  `SKILL.md:1003` is the round-34 task table row naming
  `python3 -B scripts/link_preview_audit.py --manifest`.
- `git ls-tree --name-only 318561ef:scripts` exit 0: link_preview_audit.py and
  link_preview_selftest.py present; `git show 318561ef:scripts/link_preview_audit.py` gives
  `:43 Exit codes: 0 clean, 1 failed-policy, 2 could-not-evaluate, 64 usage` and `:55-58` the four
  `EXIT_` constants.
- `git cat-file -e 318561ef:.ufo/waves/round-35/retained/r35-control-c1-constant.bundle` exit 0;
  all ten `control-*.json`/`.exit` pairs present at `318561ef`.

Findings:
1. Conflict, verbatim from the wave item: "receipt `.ufo/waves/round-34/verification/c2-at-d08d8de.json`
   at d08d8de26c9a4290c44282b0eee2b860e8ea4ecc". The file is not in that tree
   (`git cat-file -e` exit 1); it is added at `a2fe31b` and its own `revision` field is
   `d08d8de`. The criterion (b) command must use `--receipt-rev a2fe31b`, else the check exits 2.
2. Conflict on criterion (d): the CLI shape says "a markdown table row whose Name cell is the
   tool's kebab name or whose Entry command cell names the script path", but its own acceptance
   demands exit 1 at `318561ef`, where `SKILL.md:1003` (task table, columns Situation | What to
   check | Evidence command | Grounding phrase) already contains `scripts/link_preview_audit.py`.
   A literal path-cell match exits 0 there. Messaged `KakeR35.ExecRegistryRowCheck`; it replies
   that it matches only the exact Name/Entry command cells of a table with those headers
   (stated, not observed in code). The criterion requires that same restriction.
3. Criterion (b) scope: the ten pre-build receipts publish only control scores, thresholds
   (`target` 22, `probeTarget` 9), per-case/per-probe booleans and counter/key paths; none
   publishes a build-measured value. Thresholds in a receipt will match a threshold line, so the
   criterion in quality.md applies the check to the measured-result line.
4. Criterion (d) baseline: rows exist at `SKILL.md:411` canonical-audit, `:482` live-snapshot,
   `:537` receipt-replay, `:555` accessibility-packet, `:616` citing-set, `:725` base-path-audit;
   with selftests ignored, `scripts/link_preview_audit.py` is the only tool missing a row at
   `318561ef` among the scripts I inspected.

Not verified / not run:
- The three checks in criteria b, c and d were not run: their scripts are being written by other
  seats and their sandbox directories held only `clone/` and `tmp/` when I looked. Their exit
  behaviors are stated from the wave items, not observed.
- `sealed_count.py` was not re-run: it needs the sealed keys. I did not read, list, stat, copy or
  grep `/fast/scratch/hyaku/kake-r35/sealed/`; the only key strings seen are `keyPath` values in
  committed receipts. Control scores above are read from committed receipts, not re-derived.
- No live URL fetched; no installs or updates.

Out of scope: SCORECARD, lesson, SKILL row and gate text, product code, admission.

Artifacts: `/fast/scratch/hyaku/kake-r35/w1/ScribeQualityCriteria/quality.md`;
report `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-35/w1/ScribeQualityCriteria.md`.
