# ExecResolverFleetRuns

Fleet adjacency probe of the round-57 C2 tool, read-only, working trees, no `--revision`.

Tool under test: `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py`,
worktree sha256 `2bee5a8fa08efb432d946465f361db169e6572a9cfe5697f6de3ffd6f3bdfba5`, blob `2937c653b829`.
Byte-identical to its copy at the round's build revision `4b8c73050470ada9e6583f3b12d659d1bed6a17f`
(`git show 4b8c7305…:scripts/id_resolver.py | sha256sum`) and clean against lane HEAD
`51921b97124616d8526160231aec5c5708c74f3d`; the fleet numbers below are the build-under-attack tool's.

Invocation per lane, 21 lanes (every `*-shokunin` under `/home/vgpnk/Projects/shokunin` that has
`corpus/knowledge/`), confirmed by running:

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py \
  --root /home/vgpnk/Projects/shokunin/<lane> --fleet /home/vgpnk/Projects/shokunin
```

Exit distribution: 13 × 0, 8 × 1, 0 × 2. No write touched any sibling (only this file was written).

TABLE:

| lane | exit | ids_cited | dangling | owned_elsewhere | unowned |
|---|---|---|---|---|---|
| audio-shokunin | 0 | 15 | 0 | 0 | 0 |
| chousa-shokunin | 1 | 88 | 1 | 1 | 0 |
| game-dev-2d-shokunin | 0 | 10 | 0 | 0 | 0 |
| game-dev-3d-shokunin | 0 | 8 | 0 | 0 | 0 |
| kagi-shokunin | 0 | 21 | 0 | 0 | 0 |
| kaidoku-shokunin | 0 | 79 | 0 | 0 | 0 |
| kake-shokunin | 0 | 106 | 0 | 0 | 0 |
| kama-shokunin | 0 | 104 | 0 | 0 | 0 |
| kasegi-shokunin | 1 | 38 | 1 | 1 | 0 |
| kengaku-shokunin | 0 | 88 | 0 | 0 | 0 |
| kotoba-shokunin | 1 | 133 | 10 | 9 | 1 |
| kotodama-shokunin | 1 | 717 | 17 | 0 | 17 |
| kumitate-shokunin | 1 | 91 | 2 | 2 | 0 |
| lore-shokunin | 0 | 4 | 0 | 0 | 0 |
| mado-shokunin | 1 | 208 | 1 | 1 | 0 |
| mori-shokunin | 0 | 170 | 0 | 0 | 0 |
| revenger-shokunin | 0 | 41 | 0 | 0 | 0 |
| souji-shokunin | 1 | 83 | 7 | 7 | 0 |
| tabi-shokunin | 0 | 96 | 0 | 0 | 0 |
| tameshi-shokunin | 1 | 82 | 2 | 1 | 1 |
| tsukuroi-shokunin | 0 | 165 | 0 | 0 | 0 |

Totals: 41 dangling ids in 8 lanes; 22 owned elsewhere; 19 unowned. `url-match` is `-` for all 41.

PER-LANE DETAIL:

Every row below is one `DANGLING …` line from the tool, with the citing entry's sentence read to
classify the id. `url-match=-` on 22/22 owned rows means no citing entry contains any owner row's
URL. Class tags: `staged` = explicitly labelled a shokuknow `merge/<lane>/` staged id (renumber-on-
adoption, disclosed in the entry); `filename` = an id-shaped file-name prefix; `fragment` = a
DOI/SciELO-pid substring inside a URL; `label` = a fixture/check identifier; `lane-id` = used as one
of the lane's own registry rows.

chousa-shokunin (exit 1) — 1
- S118 cited-by `corpus/knowledge/search-log-method-r39.md:27`; owners kake,kama,kotoba,kotodama,kumitate,mado,mori,souji,tsukuroi; url-match `-`. `staged` — "The staged citation id was S118. The lane id is S078 because the URL is the evidence".

kasegi-shokunin (exit 1) — 1
- S068 cited-by `vendor-disclosure-policy-commitments-crosswalk.md:113`; owners chousa,kaidoku,kake,kama,kengaku,kotoba,kotodama,kumitate,mado,mori,souji,tabi,tameshi,tsukuroi (14); url-match `-`. `staged` — "its Cisco row is **staged S068**, not this lane's S040".

kotoba-shokunin (exit 1) — 10
- S231 / S234 / S285 / S286 / S301 / S303 (n=6, kotodama and mori/mado/kake coincidences, url-match `-`) `staged` — "rows S234 and S231, renumbered…", "staged S285/S286", "the announcement post (staged S301)", "the description improver (staged S303)".
- S262 owners kake,kotodama,mori; S263 owners kake,kotodama; S264 owner kotodama; url-match `-` — `filename`: all three occur only as backticked snapshot names (`S262-factory-droid-skills.md`, `S263-pi-skills.md`, `S264-hermes-skills.md`) that exist under `.ufo/waves/round-72/snapshots/`; the entry's row citations are S214/S215/S216, all registered (`corpus/lessons/round-72.md:21` maps staged S262→S214, S263→S215, S264→S216).
- S901 owners `-`; url-match `-` — `label`: "S901's `and` clause …"; S901 appears only as a verifier fixture id (`verifiers/check_*.py`, e.g. `check_explicit_invocation.py:468`), never a registry row.

kotodama-shokunin (exit 1) — 17, all unowned, all `fragment` (DOI suffix or SciELO `pid=` value)
- S0002731600048587 `civilizations/mississippian.md:6` (`10.1017/S0002731600048587`)
- S0021853700031868 `civilizations/zimbabwe-shona.md:21`; S0047404500001020 `synthesis/dialect-faction-map-workflow.md:7`; S0047404500007600 `civilizations/australia-aboriginal.md`; S0066154600008760 `civilizations/anatolia-hittite.md`; S0068246214000087 `civilizations/carthage.md`; S0075426925100281 `verification/myth-consistency-gate.md:205`; S0305440313002975 `civilizations/mesoamerica-primary-sources.md`; S0956536105050017 `civilizations/maya-classic.md:10`; S0959774320000098 `civilizations/celts.md:169` (7 further: S0071, S0271, S0717, S0718, S2071, S0956536108000229, S0956536119000257 — same class: `pid=S0071-1675…`, `10.1016/S0271-5309(03)00012-0`, `pid=S0717-7356…`, `pid=S2071-5072…`).

kumitate-shokunin (exit 1) — 2
- S121 cited-by `agent-isolation-substrates.md:262`, `mcp-orchestration-contract.md`; owners kake,kama,kotoba,kotodama,mado,mori,souji,tsukuroi; url-match `-`. Deliberate cross-lane by-number reference — "Tsukuroi's `memory-pressure-r25.md` cites its S121 (systemd v262 `systemd.resource-control.xml`)". The intended row exists (tsukuroi S121) but the entry quotes only the file name, so the tool cannot confirm it.
- S141 cited-by `durable-execution-failure-detection.md:94`; owners kama,kotodama,mado,mori,tsukuroi; url-match `-`. `staged` — "The campaign's own `S141` row … the lane does not adopt that row".

mado-shokunin (exit 1) — 1
- S243 cited-by `request-limits-upstream-r31.md:32`; owner kotodama; url-match `-`. `staged` — "byte-identical to the draft's cited S243" (refused package draft under `merge/mado/`); mado's registry has S253 in that neighbourhood, no S243.

souji-shokunin (exit 1) — 7
- S146 cited-by `origin-record-exclusivity-r28.md:11` and `:36`; owners kama,kotodama,mado,mori,tsukuroi; url-match `-`. **`lane-id` and unresolved**: "The previous F4 entries (S022, S146, S152, S210, S211)…", "held at S022 (FreeDesktop shape) and S146 (GVFS reader), with GLib's writer at S152". S022/S152/S210/S211 are rows; S146 is not, and no commit ever carried an S146 row (`git log -S"S146" -- corpus/SOURCES.md` → one commit, `765fe8b`, whose only S146 text is inside S212's row prose; registry jumps S132 → S152).
- S134, S138, S141, S147, S153, S216 (owners kake/kama/kotodama/kumitate/mado/mori/tameshi/tsukuroi/kotoba coincidences; url-match `-`) — all `staged`: "REJECT: staged row S134", "REJECT: staged S138", "provenance cells as-is (S130 S131 S134 S141 S147 S153)", "its shokuknow-only S153 row", "REJECT: staged S216".

tameshi-shokunin (exit 1) — 2
- S203 cited-by `r8-gtest-primer-independence.md:10`; owners kotoba,kotodama,mado,mori,tsukuroi; url-match `-`. `staged` — "The adopted package entry (shokuknow `merge/tameshi`, staged S203)".
- S1000 owners `-`; url-match `-`. `label` — "The sweep's S1000 line shows the mutant reporting `entries_with_source=2`"; S1000 is a sources-check sweep case label (`.ufo/evidence/round-18/sources-check/sweep/sweep.txt:13`).

OBSERVATIONS:

1. Eight lanes (chousa, kasegi, kotoba, kotodama, kumitate, mado, souji, tameshi) cite ids their own
   registry lacks — the round-52 kake shape exists fleet-wide (confirmed by running). But only one of
   the 41 is a missing source row: souji **S146**, used in a list of lane rows that cites no `staged`
   label and names no source ([INFERENCE] it was intended to be a GVFS reader row; no lane holds a GVFS
   row at S146 — kotodama's S146 is Julien Meyer's whistled-speech paper). The rest are the resolver
   over-matching its own documented id rule: 17 DOI/SciELO fragments (kotodama), 17 explicitly
   `staged` shokuknow ids, 3 id-shaped snapshot filenames (kotoba), 2 fixture/check labels (kotoba
   S901, tameshi S1000), 1 deliberate cross-lane by-number mention (kumitate S121).
2. Cross-lane resolution is number coincidence, not citation: fleet-wide 815 distinct registry ids,
   287 of them present in ≥2 lane registries, S008–S015 in all 21. Samples of the owners the tool
   names: kake S118 = PyPI `abnf` vs chousa's staged search-log citation; kama S068 = Nix Archive
   format; kotodama S146 = whistled speech; kotodama S243 = a 2025 heritage paper. `url-match=-` on
   all 22 owned ids is the only sound discriminator the tool has, and it matches nowhere in the fleet.
3. None of the 21 lane registries makes the tool exit 2 (0 exits of 2). All 21 have exactly one
   `## Registry` heading, ≥15 parseable rows, zero intra-lane duplicate row ids, zero rows indented
   4+ spaces, and a non-empty `corpus/knowledge/`; the two exit-2 triggers in the code (registry
   absent, no knowledge file) never fire. Layout risk not exercised: a registry heading reworded from
   `## Registry` would yield an empty registry and report every cited id as dangling at exit 1 rather
   than 2 ([INFERENCE] from `parse_registry`/`evaluate` at `scripts/id_resolver.py:77-104,208-242`) —
   no lane is in that state today.
4. kake itself is green on the working tree the build sits on: `ids_cited=106 ids_resolved=106
   dangling=0`, exit 0, i.e. G5's `ids_cited >= 100` and `dangling == 0` both hold at the worktree
   level (the gate measures a pinned revision, which this seat did not run).
5. Working-tree vs HEAD asymmetry: the tool reads the *lane* registry/knowledge from the working tree
   and each *sibling* registry from `HEAD:` (`scripts/id_resolver.py:122-206`). Two lanes are dirty in
   the probed paths — chousa `corpus/knowledge/{chinese-search-record-r39,japanese-search-record-r38}.md`,
   kama `corpus/SOURCES.md` plus untracked `corpus/knowledge/sglang-native-route-deprecation.md` — so
   kama's clean result mixes a modified lane registry with committed sibling snapshots.
6. Not run here (out of scope): `c57_idresolver_gate.py`, the tool's `--selftest`, `--revision` runs,
   and any claim counter. No tool installs were made; no pacman call was needed.

VERDICT: 8 of 21 fleet lanes cite ids their own registry lacks (41 ids, exit 1), but 40 are not missing source rows (17 DOI/pid fragments, 17 entries that themselves label the id a shokuknow staged id, 3 snapshot-filename prefixes, 2 fixture/check labels, 1 deliberate cross-lane by-number mention); the single missing-row instance is souji S146, all 22 sibling "owners" are same-number/different-source coincidences with url-match nowhere, and no lane's registry layout makes the tool exit 2.
