# MutSelftestTolerance — round 37 wave 1
Axes: operability (assigned); freshness unchanged. Advisory fixture analysis, not a round verdict or C2 claim.
Sandbox B=/fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance; clone checked out at 4b089da699cfaaf5ebeb6a0746b7e4238602e20a; measured fixtures at 621fb528ba9116b9f440b8332be6dfc0cad4e972.
Observed counter: 101/101 fixtures valid on both E1 and E2; 27/32 mutants killed; survivors M07, M08, M09, M11, M24; exit 1 (predicate unmet, not execution failure).
Tolerant means nonempty accept OR shape=False, exactly the requested mechanical filter: 8 fixtures (4 alternative-outcome, 4 usage-shape).
Fixture anchors below refer to /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/source_recheck_selftest-at-621fb528.py (sha256 0ad5623b9bbfafccd0f9f558c927d90651fabb5da4fd003e9fa2e73c96d5e419).
- a08-final-hop-is-a-redirect :283-286 — primary exit 2/could-not-evaluate/check_invalid/evaluated 0; accepts 1/failed-policy/http_error/evaluated 1 (check k1).
- g05-manifest-file-missing :537-539 — primary 2/could-not-evaluate/input_invalid/check null/evaluated 0; accepts exit 64 without JSON judgment.
- g22-non-final-hop-not-a-redirect :598-601 — primary 2/could-not-evaluate/check_invalid/evaluated 0; accepts 0/clean/no findings/evaluated 1 (check k1).
- g28-final-hop-without-location :627-631 — primary 0/clean/no findings/evaluated 1; accepts 2/could-not-evaluate/check_invalid/evaluated 0 (check k1).
- u01-usage-missing-manifest-option :654-655 — shape=False, exit 64 only.
- u02-usage-manifest-option-without-value :656-657 — shape=False, exit 64 only.
- u03-usage-unknown-option :658-659 — shape=False, exit 64 only.
- u04-usage-unknown-option-without-manifest :660-661 — shape=False, exit 64 only.
The four usage fixtures need no JSON under the stated usage contract; their flag alone is not a defect. g19 has no accept alternative. Counter judgment is clone/.ufo/waves/round-37/c2_mutkill.py:175-205.
## Per-mutant killers (N = not tolerant; [] = survivor)
| Mutant | Complete killer list, with tolerance flags |
|---|---|
| M01 | a03-final-410-gone [N] |
| M02 | b01-301-permanent-moved [N]; b02-308-permanent-moved [N]; b03-302-temporary-no-moved [N]; b04-303-temporary-no-moved [N]; b05-307-temporary-no-moved [N]; b06-leading-permanent-run-target-is-last-permanent-hop [N]; b07-permanent-then-temporary-only-leading-run-counts [N]; b08-leading-temporary-suppresses-moved-entirely [N]; b09-relative-location-resolved-rfc3986 [N]; b10-moved-plus-final-status-outcome [N]; b11-absolute-location-target [N] |
| M03 | a05-final-204-other-2xx-http-error [N] |
| M04 | a02-final-404-gone [N]; b10-moved-plus-final-status-outcome [N] |
| M05 | b01-301-permanent-moved [N]; b03-302-temporary-no-moved [N]; b06-leading-permanent-run-target-is-last-permanent-hop [N]; b07-permanent-then-temporary-only-leading-run-counts [N]; b08-leading-temporary-suppresses-moved-entirely [N]; b09-relative-location-resolved-rfc3986 [N]; b10-moved-plus-final-status-outcome [N] |
| M06 | b06-leading-permanent-run-target-is-last-permanent-hop [N] |
| M07 | [] |
| M08 | [] |
| M09 | [] |
| M10 | c01-script-contents-removed [N]; c02-style-contents-removed [N]; c03-template-contents-removed [N]; c09-script-end-tag-case-insensitive [N]; c10-xhtml-media-type-uses-html-rules [N] |
| M11 | [] |
| M12 | c06-named-character-reference-decoded [N]; c07-decimal-and-hexadecimal-references-decoded [N] |
| M13 | c09-script-end-tag-case-insensitive [N] |
| M14 | c02-style-contents-removed [N] |
| M15 | d01-nfkc-fullwidth [N]; d06-nfkc-compatibility-ligature [N] |
| M16 | d02-whitespace-deleted-from-both [N]; d07-nbsp-is-whitespace [N] |
| M17 | d03-matching-is-case-sensitive [N] |
| M18 | c08-title-text-kept [N]; d04-substring-of-text-holds [N]; o02-report-shape-two-checks-two-evaluated [N] |
| M19 | e05-media-type-ascii-case-insensitive [N] |
| M20 | f11-charset-parameter-name-case-insensitive [N] |
| M21 | e01-text-plain-body-as-is-no-tag-processing [N]; e02-text-plain-no-reference-processing [N]; e03-text-plain-literal-amp-holds [N] |
| M22 | c10-xhtml-media-type-uses-html-rules [N] |
| M23 | f01-utf8-bom-overrides-charset [N]; f12-utf16le-bom [N]; f13-utf16be-bom [N] |
| M24 | [] |
| M25 | f10-charset-parameter-quotes-removed [N] |
| M26 | f05-charset-ascii-means-windows-1252 [N] |
| M27 | d01-nfkc-fullwidth [N]; d06-nfkc-compatibility-ligature [N]; d07-nbsp-is-whitespace [N]; f09-no-bom-no-charset-means-utf8 [N] |
| M28 | f16-invalid-bytes-become-replacement-character [N] |
| M29 | g25-one-invalid-one-valid-check [N]; g26-one-invalid-one-valid-check-missing-quote [N] |
| M30 | g09-body-path-escapes-manifest-directory [N] |
| M31 | g07-check-with-empty-id [N] |
| M32 | g02-manifest-version-not-1 [N] |
Counter :286 truncates killers[:8]; only M02 was truncated (11 total). The three omitted names above were recovered by running its unchanged run_fixture against all 101 valid fixtures, with count and first-eight equality recorded by collect.py.
**No mutant among M01–M32 is killed only by a tolerant fixture; none has any tolerant killer.** This matrix does not establish that tolerance caused any of the five survivors.
## One supplementary mutation probe (separate from M01–M32)
Mutant: measured E1 copied to B/probe.py:450; `if location is not None and not isinstance(location, str):` became `if not isinstance(location, str):` (require location even on final hops). No other source change.
Expected detector: unchanged frozen C2 run_fixture over the same 101 base fixtures; a final hop without location should remain valid under the prose reading. g28 explicitly exercises that input, but accepts check_invalid too.
Actual pristine → mutated → restored: 101/101 exit 0 → 49/101 exit 1 (52 failures) → 101/101 exit 0. Verdict: KILLED by the full suite; g28 itself still passed through its alternative, not a suite-level masking finding.
g28 raw pristine/restored: exit 0, {"version":1,"verdict":"clean","checksEvaluated":1,"findings":[]}; mutated: exit 2, {"version":1,"verdict":"could-not-evaluate","checksEvaluated":0,"findings":[{"check":"k1","reason":"check_invalid","target":null}]}; stderr empty in all three.
Source doc :64-65 says every fixture carries location, but chk default :236 is [{"status":200}]; those strict fixtures explain the 52 kills. No contract or fixture was changed.
Before/restored SHA256 = 577b2d7d028964e06152f5a7b792141e586045eaa8ec9262ee7f416ba5510d48; mutated SHA256 = e1618b2ef283adc658e62e34a8df907ca9ca21fad1fa40ed42ed420e00e7e802. Source unchanged during each detector; exact-byte `cmp -s` pristine.py/probe.py exited 0 after restoration.
## Exact behavioral commands and exits
Preparation (exit 0): `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && mkdir -p /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/tmp && export TMPDIR=/fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/tmp && timeout 120 git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/clone && timeout 30 git -C /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/clone checkout -q 4b089da699cfaaf5ebeb6a0746b7e4238602e20a`.
Collector (exit 0): `timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/tmp PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/collect.py`.
Nested counter (exit 1): `timeout 780 /usr/bin/python3 -B /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/clone/.ufo/waves/round-37/c2_mutkill.py --root /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/clone --revision 621fb528ba9116b9f440b8332be6dfc0cad4e972 --jobs 2`; cwd B; counter SHA256 d72e232e4d4f120b6b45139958c40e9364d44d3d902207c0705ac97c1b6d5cb6. Full argv/exit/stdout hash in B/c2-at-621fb528-command.json; jail fixture-dump argv/exit 0 in B/fixtures-command.json.
Pristine (exit 0): `timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/tmp PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/detect_probe.py pristine`.
Mutated (exit 1): `timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/tmp PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/detect_probe.py mutated`.
Restored (exit 0): `timeout 300 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/tmp PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/detect_probe.py restored`.
Restoration (exit 0): `timeout 10 cmp -s /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/pristine.py /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/probe.py`; hashes recorded with timeout-bounded sha256sum.
## Evidence paths and SHA256
/fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/c2-at-621fb528.json:1 — cf1a886152efce8beb4205047e1ab35ba32fc71be5546902bf8b9195a7fcc03c
/fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/per-mutant-tolerant-flags.json:1 — 3b8467abc1b2073318192700718497a6fa0a24fc95cec8d05fc90708adee9f7d (full names and separate acceptAlternatives/shapeFalse/tolerant flags).
/fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/tolerant-fixtures.json:1 — dadd3879804d65d844dde2ead57941db7da15b5329658630b535a45f1d8c2979; /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/fixtures.json:1 — 773019d42fe0014812e16ce16be01e4e3cd1c3f3a97f3cdfc1cc5ec85c2e04ac.
/fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/probe-pristine.json:1 — 5d4e6bf9207cb3d233a6ea3aff757bbbcf188fad77aafe21bd1171b1ffdd8476; /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/probe-mutated.json:1 — 6a3ff11b6f1c3e781a0c58aa2521be03481b9ba855678abf6b1f4a0a7a2ec876; /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/probe-restored.json:1 — 180cf099cbedbac34c806afdd7b95b981628c3c1b5164dbbaf21a1d799750c42.
/fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/probe-mutated-source.py:450 — e1618b2ef283adc658e62e34a8df907ca9ca21fad1fa40ed42ed420e00e7e802; /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/probe.py:450 — 577b2d7d028964e06152f5a7b792141e586045eaa8ec9262ee7f416ba5510d48 (restored).
/fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/collect.py:1 — c8e57e1992f91f59c3e84bcfb26eb706f3624e9bb08fb6443764eb28e1b6af2c; /fast/scratch/hyaku/kake-r37w1/MutSelftestTolerance/detect_probe.py:1 — 54d37e5baf64ace279f9c56035e0e8856acb5dbc22ba67d74159a7dc8ff03024.
Limits: no C1 counter or sealed tree access, network, live site checks, integration, round judgment, additional mutation probes beyond the one reported, or alternative-expectation tightening. No lane writes except this report. All started jobs finished; temporary fixture jails cleaned. Existing Python 3.14.8 and bubblewrap 0.13.1 used; no tool install/update.
