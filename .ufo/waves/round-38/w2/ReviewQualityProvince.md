# Kake R38 W2 — ReviewQualityProvince

Scope: QUALITY round-38 (j)–(n), PROVINCE r38 step, corpus/README r38 row, SKILL r38 amendment. Compared base `af43a50fa399881eead9381d835b78a015e277a6` to tip `adab4c7e9ec2178657395f49346f18800ff4796f`. Axes: operability; freshness (web properties/publishing).

## Finding — Low, evidence gap

- QUALITY (k) is **overstated/unverified**: it says round 38 had no dead seat (`corpus/QUALITY.md:948-950`), but the dispatch records 32 spawns (`.ufo/waves/round-38/w1-dispatch.json:16-19`) and includes `RevengerExemption` (`w1-dispatch.json:318-325`; assigned item at `make_w1_spec.py:177-180`). `w1/` has 31 `.md` reports and no `RevengerExemption.md` (count command below). Absence does not prove the seat died, but neither proves no dead seat; publish the disposition or say “no recorded dead seat; criterion not exercised.”

## Verdicts

- QUALITY (j): **holds**; red r37 and green r36/r38 reproduced. Name-based classification limitation is disclosed at `corpus/QUALITY.md:945-947`.
- QUALITY (k): **overstated/unverified**, as above; no death inferred.
- QUALITY (l): **holds**; old receipt has only a tool path; pinned reruns bind revisions and hashes and pass 137/137 and 194/194.
- QUALITY (m): **holds**; r37 receipt is 435s late; three r38 receipts are 58s early.
- QUALITY (n): **holds**; the v2 wrapper control meets and justifies C1 withdrawal; all rerun C2 declared controls are below 20/20. The four full-rule tools scoring 20 are explicitly build-class, not controls.
- PROVINCE `:307-324`, corpus/README `:367`, SKILL `:1104-1113`: **hold** against rerun results; no discrepancy found.

## Re-runs and observations

All counters/selftests ran in `/fast/scratch/hyaku/kake-r38w2/KakeR38.ReviewQualityProvince/clone` at the tip; `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` unset; `TMPDIR` in my sandbox; `prlimit --as=4000000000`; all runs `timeout`-capped (20s timeline, 30s criteria, 900s counters/selftests). No installs or network requests.

- `control_consequence_check.py --selftest`: exit 0, 10/10. `--verification .ufo/waves/round-36/verification`: exit 0, no tainted counter; round 37: exit 1, two claim violations under the 28/28 shortcut; round 38 at tip: exit 0, 150 receipts, one tainted v2 counter, no claim violations.
- `timeline_check.py` for `.ufo/waves/round-37/verification/control-CtlC1Shortcut-followup.json`: exit 1, −435s. For r38 `control-CtlStdlibV2.json`, `control-CtlBaseWrapper-care.json`, and `control-CtlLabelShortcut-delegate_ceiling.json`: exit 0 each, +58s.
- `sealed_count_v3.py --root . --revision af43a50fa399881eead9381d835b78a015e277a6 --key-revision 99357694f68886d3175fc6c386979c350be789bc`: exit 1, 8/20. Same command at `3ed8e15c2707ac4cec88f48fc9be48b35be4f2b0`: exit 0, 20/20; tool sha `f4d057c4afac885b998de404da8c19f2d5d0a4d754a9d539e49b07d3f36baace`.
- Same v3 `--tool-file F` form: base 8, stdlib-patched 13, label shortcut 16, minimal wrapper 14, r37 shortcut 7; eight ablations 16–18; trivial controls 0/0/0 and no-reader 1; r37 retained controls 0–5. Four full-rule build-class tools each scored 20/20. Every named control class stayed below predicate.
- All 42 private-reference mutants rerun, max 8 workers, via `prlimit --as=4000000000 timeout 900s python3 -B .ufo/waves/round-38/sealed_count{,_v3}.py --root . --tool-file <M01.py…M42.py> --key-revision 99357694f68886d3175fc6c386979c350be789bc`: v2 29/42 met; v3 0/42 met (16–19/20).
- v2 wrapper `CtlBaseWrapper-care.py`: exit 0, 20/20. Round-37 counter in `--tool-file` mode: build tool 28/28 (exit 0), `CtlC1Shortcut-followup` 28/28 (exit 0), stock `CtlC1NaiveReader` 20/28 (exit 1).
- `pinned_selftest.py` at base: exit 0, 137/137, tool sha `944d2f51f396fb6e1ba3c7cf07112eb3f55d011e9bbc16bb1a59af517be1d3e5`. Tool at `3ed8e15c`, selftest at `145a6468`: exit 0, 194/194; tool sha `f4d057c4…baace`, selftest sha `bab98f444bdb6b10a375652977beb083c1d28adbed9b60b1857f36f0bec508c1`.
- `printf '%s\n' /fast/scratch/hyaku/kake-r38w2/KakeR38.ReviewQualityProvince/clone/.ufo/waves/round-38/w1/*.md | wc -l`: exit 0, 31. `RevengerExemption` was assigned a report path in dispatch but no report is present.

## Evidence anchors / hashes

- Reviewed tip `adab4c7e9ec2178657395f49346f18800ff4796f`. Docs SHA-256: `corpus/QUALITY.md` `9cd828b1ced81c5d06c88fbbedccd4c9ef3f2bc155b4a9507015d7c9b1b83c36`; `PROVINCE.md` `712fd3e099d9f81243742ec16c663037f0ae67268c63cdff3fefe058d8adde7f`; `corpus/README.md` `11bffcf77a328293aae8270ddd7a5ab6ec5312e8a107308fbe9d2302da01581c`; `SKILL.md` `ee55d0868be8f4d276591ea4ee804d72d4b33eb21b211a5e157c9c8eb080ad1e`.
- Scorecard SHA `59dc78772f32f07fea70e5a04a22c11ff680e7d5c43292477aaf9eeafcdd1f1c`; C1 control receipt SHA `98743b5cd52c5f5ed7a848f5bfacbb023dd821f31acfa032c57d78806f166d23`; dispatch SHA `5e40d8744c27bb3950eecffc143284cdcb2444f9ea1c3ae883a0390df8c6b377`.
- Sandbox pinned outputs: `/fast/scratch/hyaku/kake-r38w2/KakeR38.ReviewQualityProvince/r37-pinned.json` SHA `e3d0319dc91ae28a7ba114b985e89dad6206f5e4488de00c021e36d7a6d2d7e9`; `r38-pinned.json` SHA `7fdb707524ba5d8aecb393a3bb498b86dcfb6fcfc366928144d42954bf31be16`.

Verification gap: no `lsp` device/server was mounted (`xd://lsp` reported only `ast_edit` and `debug` devices); no semantic LSP queries were available. Static review was anchored to the commit and rerun receipts, not grep as semantic proof.
