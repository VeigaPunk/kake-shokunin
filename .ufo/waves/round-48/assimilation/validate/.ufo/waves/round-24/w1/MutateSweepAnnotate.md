# Freshness mutation probe — annotate / set delta

## Verdict

**8 of 13 isolated mutants SURVIVED the existing 15-case selftest; 5 were KILLED; 0 were inconclusive.** This is author-side mutation evidence for C1 / freshness, milestone r24-build, not independent admission.

Survivors: removal of **gone, vanished, emptied, no longer, dangling, no such file, never published** from ABSENT_RE (seven independent mutants), plus **recovered list ignored**. The symmetric ±1 and ±3 window changes, removal of absent or missing, and inverted newMissing filter were killed.

## Findings

### P2 — Seven supported absence phrases can disappear without a selftest failure

- Impacted claim / axis: frozen C1 citation reconciliation / freshness. Mutated source: /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/freshness-sweep.mjs:122, in the isolated clone only.
- Exact command D (also includes the pre-run SHA-256 observation):

```sh
sha256sum /tmp/kake-r24-MutateSweepAnnotate-nRnj/clone/scripts/freshness-sweep.mjs && env -i PATH=/usr/bin:/bin HOME=/tmp/kake-r24-MutateSweepAnnotate-nRnj/home TMPDIR=/tmp/kake-r24-MutateSweepAnnotate-nRnj/tmp KAKE_SELFTEST_DIR=/tmp/kake-r24-MutateSweepAnnotate-nRnj/fixtures timeout --kill-after=5s 45s node /tmp/kake-r24-MutateSweepAnnotate-nRnj/clone/scripts/freshness-sweep.mjs --selftest
```

- Each of the seven single-alternative deletions returned exit 0 and the exact stdout summary **`selftest: 15/15 passed`**. No behavioral case failed. Full actual outputs are retained at the absolute paths below.
- Expected detector: on every mutated source, the same bounded selftest should exit nonzero with a behavioral FAIL; on pristine/restored source it should exit 0. The current fixtures exercise absent in prose and missing in the loose-window prose. The occurrence of gone in the case-b path is intentionally blanked and is not a positive prose-vocabulary test.
- Smallest selftest change to kill these survivors: table-drive one hermetic missing target per supported phrase, with exactly that phrase as its sole absence prose, and assert declaredAbsent, no drift, and matching evidence.word. Use a neutral path name so the phrase cannot come from the cite itself. Keep the existing case-b blanking control. Apply the same phrase cases through the round-24 sidecar interpretation if it consumes this vocabulary; sidecar behavior itself was not tested here.

### P2 — Ignoring every recovered token is invisible to the selftest

- Impacted claim / axis: frozen C1 reconciliation of four recovered targets / freshness. Mutated source: /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/freshness-sweep.mjs:480, in the isolated clone only.
- Single behavior-bearing replacement: `setDelta.recovered = [];`. Exact command: D above, unchanged.
- Exact observed result: exit 0; stdout **`selftest: 15/15 passed`**; no behavioral FAIL. The only pinned-miss selftest fixture pins an empty set, so it cannot positively exercise recovery.
- Smallest selftest change to kill this survivor: reuse the hermetic present target and the annotated missing target. Pin both in pathsMissSet, scan the same fixture, and require newMissing to be empty and recovered to equal exactly the present target while missSet still contains exactly the absent target. Keep exit 0: recovery is informational in the existing sweep contract, not a new drift gate. Assert the recovered JSON list, not merely the process exit. Round-24 reconciliation must still account for recovered receipts/pins separately.

### Complete mutation outcomes

Each row is one mutant, applied alone after a pristine/restored pass. The expected detector for every mutant was the same bounded D command returning nonzero; KILLED means its baseline passed and at least one behavioral assertion failed. All source line numbers refer to the frozen base file.

| Mutant | Smallest change | Exit | Exact stdout summary | Verdict | Failing case(s) |
|---|---|---:|---|---|---|
| `window-pm1` | Lines 322–323: change both window bounds from i ± 2 to i ± 1 | 1 | `selftest: 14/15 passed` | KILLED | f (documented limitation) unrelated absent-word in ±2 lines -> declaredAbsent |
| `window-pm3` | Lines 322–323: change both window bounds from i ± 2 to i ± 3 | 1 | `selftest: 14/15 passed` | KILLED | m cross-citation leak -> drift, exit 1; annotated dup control stays declaredAbsent |
| `word-without-absent` | Line 122: remove only the absent alternative from ABSENT_RE | 1 | `selftest: 10/15 passed` | KILLED | a annotated-missing -> declaredAbsent, exit-neutral; g pinned-empty pathsMissSet -> first-seen miss fails (set-delta verdict); h1 spec-literal ±2 window: trailing annotation -> declaredAbsent, exit 0; h2 strict pin (pathsAbsenceStrictSameLine): unnamed trailing annotation -> drift, exit 1; m cross-citation leak -> drift, exit 1; annotated dup control stays declaredAbsent |
| `word-without-gone` | Line 122: remove only the gone alternative from ABSENT_RE | 0 | `selftest: 15/15 passed` | SURVIVED | none |
| `word-without-vanished` | Line 122: remove only the vanished alternative from ABSENT_RE | 0 | `selftest: 15/15 passed` | SURVIVED | none |
| `word-without-emptied` | Line 122: remove only the emptied alternative from ABSENT_RE | 0 | `selftest: 15/15 passed` | SURVIVED | none |
| `word-without-no-longer` | Line 122: remove only the no longer alternative from ABSENT_RE | 0 | `selftest: 15/15 passed` | SURVIVED | none |
| `word-without-dangling` | Line 122: remove only the dangling alternative from ABSENT_RE | 0 | `selftest: 15/15 passed` | SURVIVED | none |
| `word-without-no-such-file` | Line 122: remove only the no such file alternative from ABSENT_RE | 0 | `selftest: 15/15 passed` | SURVIVED | none |
| `word-without-never-published` | Line 122: remove only the never published alternative from ABSENT_RE | 0 | `selftest: 15/15 passed` | SURVIVED | none |
| `word-without-missing` | Line 122: remove only the missing alternative from ABSENT_RE | 1 | `selftest: 14/15 passed` | KILLED | f (documented limitation) unrelated absent-word in ±2 lines -> declaredAbsent |
| `newmissing-invert-filter` | Line 477: remove ! from !pins.pathsMissSet.includes(t) | 1 | `selftest: 14/15 passed` | KILLED | g pinned-empty pathsMissSet -> first-seen miss fails (set-delta verdict) |
| `recovered-ignored` | Line 480: replace the recovered filter expression with [] | 0 | `selftest: 15/15 passed` | SURVIVED | none |

## Checked and held

- Read frozen /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-24/contract.json before investigation; read skill://godspeed and /home/vgpnk/.omp/agent/RULES.md.
- Clone creation command: `git clone --no-hardlinks -- /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r24-MutateSweepAnnotate-nRnj/clone`.
- `git -C /tmp/kake-r24-MutateSweepAnnotate-nRnj/clone rev-parse HEAD` observed exactly `f7de3ab4e9f030a15a857a5a08631bd8e690f436`; the read-only lane HEAD observation matched.
- Pristine D: exit 0, exact summary `selftest: 15/15 passed`. An earlier pre-capture pristine run also passed. The 27 saved detector records contain one pristine run, 13 mutated runs, and 13 restored runs.
- After **every** mutant, the exact original source bytes were restored before running D again. Every restored run returned exit 0 and `selftest: 15/15 passed`. The previous restored run served as the next mutant's pristine control; no source changes were stacked.
- All selftest fixtures were isolated using HOME=/tmp/kake-r24-MutateSweepAnnotate-nRnj/home, TMPDIR=/tmp/kake-r24-MutateSweepAnnotate-nRnj/tmp, and KAKE_SELFTEST_DIR=/tmp/kake-r24-MutateSweepAnnotate-nRnj/fixtures. This includes the selftest's normally home-resident resolve fixture.
- No lane production files, historical runners, domain trees, git index, fleet configuration, or sibling sources were written. This report is the only lane write. No commits, builds, linters, formatters, network probes, or subagent dispatch were performed.
- Existing tools observed: Node `v24.21.0`, Git `2.56.0`. No tool installs/upgrades; no pacman transactions.

### Before / mutated / after hashes

SHA-256 H0, observed initially for both lane and clone source and before every restored detector run:

```text
5ff6ab47000a677fcc267c56e9bf460c56bcd7f6032e50d4fe2ab78d9b2e8c16
```

The source path tested was /tmp/kake-r24-MutateSweepAnnotate-nRnj/clone/scripts/freshness-sweep.mjs. Before each mutant = H0. Every after/restored hash below = H0. The final restored detector also observed H0.

| Mutant | Mutated source SHA-256 | Restored source SHA-256 |
|---|---|---|
| `window-pm1` | `fe2913fc1eec30b948dfa3ed353ea9d07defecf4a030bbcbabe1ad74d5998cc0` | H0 |
| `window-pm3` | `4e1cf4893dc6eb182488c7c2b30b6edc7a2ac408e941785f9b43d85bdaceb07a` | H0 |
| `word-without-absent` | `42cd330fe89756300ec30707c6a9896878b9abd3e002f7e1afe5f25c3015f04d` | H0 |
| `word-without-gone` | `adb6ffd62f794ac3cde6b009ab757d71d429fd39c269f1fdc724b38ccb921d23` | H0 |
| `word-without-vanished` | `bb9528933e5244ad5f5c572e07998bca1a89ef40ba64e6614edb57bc746f60ad` | H0 |
| `word-without-emptied` | `194f2bf1d3726de95b949513f1268a7d6ffca9a48e40f2785a6c392e7ed62c8f` | H0 |
| `word-without-no-longer` | `d6276f13612db5e128d56eeeb7f6277d648f0acb9e2c675e96bff87e0dace525` | H0 |
| `word-without-dangling` | `7ce33779b7786bbc362af7f7bc4940fb3803b39a34d18ddd40f55c871f339050` | H0 |
| `word-without-no-such-file` | `318507e1fe5de944086df1dd7bb64b8478a953b98aeaad3cb528e5c8269de54a` | H0 |
| `word-without-never-published` | `a54e4fb27bd3bccc6418f8a0d5fc34dcc4c20b14fb7d57fa9f0956853978b4c1` | H0 |
| `word-without-missing` | `cc2a2759e53da4ccab96b748394798e25eabb26dddc937c76d76de56992b177e` | H0 |
| `newmissing-invert-filter` | `2ffac4d3f454be0b89dfc543c63ea35d8fb7323b903ba46d732d288c825bf417` | H0 |
| `recovered-ignored` | `e730cd72413fa991f10e915f0e1c9afbfe0d255055a1f6c6f8292586d7dd65ed` | H0 |

### Exact killed-mutant outputs

### window-pm1

```text
  FAIL  f (documented limitation) unrelated absent-word in ±2 lines -> declaredAbsent
        expect: exit 0 · declaredAbsent contains selftest-unrelated.md · drift [] — spec-mandated window semantics
        got:    exit 1 · declaredAbsent [] · drift ["~/Projects/webzites/selftest-unrelated.md"]
selftest: 14/15 passed
```

### window-pm3

```text
  FAIL  m cross-citation leak -> drift, exit 1; annotated dup control stays declaredAbsent
        expect: exit 1 · canonical leak target · unannotatedCites ['SKILL.md:3'] · cites lists both locations · annotated duplicate stays declaredAbsent
        got:    exit 0 · drift [] · declaredAbsent [["~/Projects/webzites/selftest-dup.md",["SKILL.md:6","corpus/knowledge/note.md:3"]],["~/Projects/webzites/selftest-leak.md",["SKILL.md:3","corpus/knowledge/note.md:1"]]]
selftest: 14/15 passed
```

### word-without-absent

```text
  FAIL  a annotated-missing -> declaredAbsent, exit-neutral
        expect: exit 0 · declaredAbsent contains selftest-missing.md · drift [] · resolve contains selftest-present.md
        got:    exit 1 · declaredAbsent [] · drift ["~/Projects/webzites/selftest-missing.md"] · resolve ["~/.kake-freshness-selftest-981163/selftest-present.md"]
  FAIL  g pinned-empty pathsMissSet -> first-seen miss fails (set-delta verdict)
        expect: exit 1 · setDelta.newMissing contains selftest-missing.md · drift []
        got:    exit 1 · newMissing ["~/Projects/webzites/selftest-missing.md"] · drift ["~/Projects/webzites/selftest-missing.md"]
  FAIL  h1 spec-literal ±2 window: trailing annotation -> declaredAbsent, exit 0
        expect: exit 0 · declaredAbsent has trailing+named · drift []
        got:    exit 1 · declaredAbsent [] · drift ["~/Projects/webzites/selftest-named.md","~/Projects/webzites/selftest-trailing.md"]
  FAIL  h2 strict pin (pathsAbsenceStrictSameLine): unnamed trailing annotation -> drift, exit 1
        expect: exit 1 · drift has trailing · declaredAbsent has named · evidence.direct/mentions recorded
        got:    exit 1 · drift ["~/Projects/webzites/selftest-named.md","~/Projects/webzites/selftest-trailing.md"] · declaredAbsent []
  FAIL  m cross-citation leak -> drift, exit 1; annotated dup control stays declaredAbsent
        expect: exit 1 · canonical leak target · unannotatedCites ['SKILL.md:3'] · cites lists both locations · annotated duplicate stays declaredAbsent
        got:    exit 1 · drift [["~/Projects/webzites/selftest-dup.md",["SKILL.md:6","corpus/knowledge/note.md:3"],["SKILL.md:6","corpus/knowledge/note.md:3"]],["~/Projects/webzites/selftest-leak.md",["SKILL.md:3","corpus/knowledge/note.md:1"],["SKILL.md:3","corpus/knowledge/note.md:1"]]] · declaredAbsent []
selftest: 10/15 passed
```

### word-without-missing

```text
  FAIL  f (documented limitation) unrelated absent-word in ±2 lines -> declaredAbsent
        expect: exit 0 · declaredAbsent contains selftest-unrelated.md · drift [] — spec-mandated window semantics
        got:    exit 1 · declaredAbsent [] · drift ["~/Projects/webzites/selftest-unrelated.md"]
selftest: 14/15 passed
```

### newmissing-invert-filter

```text
  FAIL  g pinned-empty pathsMissSet -> first-seen miss fails (set-delta verdict)
        expect: exit 1 · setDelta.newMissing contains selftest-missing.md · drift []
        got:    exit 0 · newMissing [] · drift []
selftest: 14/15 passed
```

### Saved output evidence

Machine-readable summary: /tmp/kake-r24-MutateSweepAnnotate-nRnj/summary.json, SHA-256 `0d996bd07eb4b22a939e5d78cf21600e75eb0ee6e2c65b9a64bf6c6fed5a199f`.

Each JSON below contains the exact command and unabridged tool output/exit metadata, including the pre-run source hash. Successful bash-tool results omit exitCode; they have no error, print all 15 PASS cases, and selftest returns 0 on that path. Nonzero results explicitly carry exitCode 1. Summary.json normalizes successful exits to 0.

```text
bbfa5de3c5f972d360fe2aff15171583821a587c3d43f26960e24cfeee5506ea  /tmp/kake-r24-MutateSweepAnnotate-nRnj/baseline-pristine.json
3c269368925c574d22bf261a7090c8cf8825f7bed59d46466c52c48cc889c6bb  /tmp/kake-r24-MutateSweepAnnotate-nRnj/newmissing-invert-filter-mutated.json
21871c380f425208644a4730b0f69ba2e8bfe710af7f90710ddf050992816922  /tmp/kake-r24-MutateSweepAnnotate-nRnj/recovered-ignored-mutated.json
1ed202a7cfca23fa5b1093a2b38d8281c1868391622786746e6163e9764c029e  /tmp/kake-r24-MutateSweepAnnotate-nRnj/window-pm1-mutated.json
e006609659b07225ffcb47c0184ad644cef0381983d519e37b0ffc0ed42fd9bf  /tmp/kake-r24-MutateSweepAnnotate-nRnj/window-pm3-mutated.json
b0953b296f0b639b320b54d9c357cefab971e72aa6d33f6e952926ed3efc7307  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-absent-mutated.json
96e4003ddc895c0583baf072461859dccbc63674eb19090b5cd6221d1c476c6b  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-dangling-mutated.json
f8a697e82af92fde716faa11aae89193d550962f81fc2398f35325bada4beab8  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-emptied-mutated.json
c42cb6941637ae59b19180dfc439d029059273f0650a45871b230d7f248ca720  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-gone-mutated.json
bc6921015736962cf3edd1201792d9b8cad820e4c68862fd87c2778bef18619d  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-missing-mutated.json
46711d76cba0cdfe6414204878a4b3b77ebfb11e398c49f17473534a948d0785  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-never-published-mutated.json
c8b9646fc311c8ec92d6660c3910c7dfb162413e3ceca3a3b546cd349f740225  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-no-longer-mutated.json
ca7e34c7dfd9ef15aab0782599c4fb3840fe53be25d84b78cf8205b2b9f9d70d  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-no-such-file-mutated.json
d4caf4500d7eb2d994fc39b62c08b3dfd7d31ee13e85b2ff3c376d9b0cbbab8b  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-vanished-mutated.json
664c3ff6a771f7945fd66fed2d3675acf7fba65e2b27c757aa7d9ac35f2be010  /tmp/kake-r24-MutateSweepAnnotate-nRnj/newmissing-invert-filter-restored.json
3f1ca186cf0432dff7591093af7165cc8208bd81069a52c69f6b11e0e2b2c824  /tmp/kake-r24-MutateSweepAnnotate-nRnj/recovered-ignored-restored.json
ca2c7a2afd5096204a806237d2179e2a51e274bc8a9ca1a432c7385ae03b1e0e  /tmp/kake-r24-MutateSweepAnnotate-nRnj/window-pm1-restored.json
d493bca5f5304f3e88cf4a34f8f7c07fe560b146d0af290c85a5f7cd50c4878c  /tmp/kake-r24-MutateSweepAnnotate-nRnj/window-pm3-restored.json
677d97bf3ec1bb0c7afe540e164afc64c1ef83a725be3957fc4f27306bf5e9b3  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-absent-restored.json
b7b67d0fb84620929394007f71d8f099e7e3057bf029b5f62ca31ff5957f7dc7  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-dangling-restored.json
f7cbd82cd897aabb32a6556135e0c31db900d3a83affa44f740e86751217925b  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-emptied-restored.json
4ddb37f84f1ff349c00d1d03175302ab50e27763f492ee3b47f95807468f29f6  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-gone-restored.json
e6944ab7dbf31737c430a278c023d541a4424cca067cebbd958d7f2c537350b1  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-missing-restored.json
88d6049acaebbebff86e80ae7e5b6f4f06778734c04e1d044fccdefb2f2272a0  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-never-published-restored.json
f1e50ec5267250725b60f7e04b42b9518f08d92380f359fb76a4f10f3a96f283  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-no-longer-restored.json
f34442cf6d72ecbed9598cf6e18d8fe66f23022c0781f4ef67abde875ba91765  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-no-such-file-restored.json
4c22fce916c995d72ab81bbf2258f765736ebb01450eb9efd8c6de45d2d2712f  /tmp/kake-r24-MutateSweepAnnotate-nRnj/word-without-vanished-restored.json
```

## Limits

- This probe evaluated only the specified mutation families against the existing base-revision selftest: symmetric window ±2→±1/±3, one regex alternative deleted at a time, newMissing filter inversion, and recovered cleared. One-sided window changes, phrase combinations, and unrelated logic were not probed.
- A surviving mutant is a selftest coverage finding, not permission to weaken the vocabulary, recovery output, or frozen C1 contract. No proposed selftest additions were implemented or run.
- No round-24 sidecar implementation, live 19-target sweep, receipt replay, full C1/C2 counter, or admission check was exercised. The positive tests described above are scoped recommendations for the integration owner, not claimed passing checks.
- Scratch evidence and fixtures remain under /tmp/kake-r24-MutateSweepAnnotate-nRnj for inspection; the cloned sweep source has been restored to H0. No mutant remains applied.
