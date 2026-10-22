# ReviewSkillTable34 — SKILL.md "Link-preview metadata — round 34" at 24a1647

Scope: SKILL.md:993-1015 (13 table rows) + condensed grounding (1019-1023) + trailer
(1024). Method: sandbox clone at /fast/scratch/hyaku/kake-r34/w2/ReviewSkillTable34/clone
(HEAD 24a16474ee73e20453f3e1be9d2f33573c5196d9); every cited phrase tested at its byte
offset in the retained .txt; every read-only command executed in the clone.

## Finding

F1 (minor, grounding): all four S068 byte offsets are wrong — each lands inside the
preceding sentence, 8-20 bytes before the quoted phrase. The phrases themselves are
verbatim and unique in S068.txt; only the offsets are stale.
- row 4 (1011 area, :1006): `S068.txt@6801`; phrase actually starts at 6821.
- row 5 (:1007): `S068.txt@3896`; phrase starts at 3906.
- row 7 (:1009): `S068.txt@2626`; phrase starts at 2634.
- row 12 (:1014): `S068.txt@4546`; phrase starts at 4558.
All other offsets verified exact: S067@955, S067@1303, S069@685, S069@974, S070@3020,
S071@0, S072@0.

## Per-row verdict

1. (:1003) PASS. Interface `manifest v1` phrase verbatim; invocation matches matrix
   `invocation`; ran `python3 -B scripts/link_preview_audit.py --manifest manifest.json`
   on a sandbox manifest: exit 1, `failed-policy`, three `og_required_missing`. No
   network imports in the tool (grep socket/urllib/requests/http/urlopen: none).
2. (:1004) PASS. Docstring quote verbatim (c1_matrix_count.py:11-13). Ran counter at
   d08d8de: passed 0/28, toolPresent false, byKind 0/6+0/13+0/7+0/2,
   constantGatesAllRejected true — matches verification/c1-at-d08d8de.json. At 24a1647:
   28/28, gates rejected, exit 0. Dated receipt state, not stale-as-current.
3. (:1005) PASS. D1-D6 exit 1 `og_required_missing`; D7 exactly `og_required_missing
   og:image`; K6 exit 0 (values have surrounding spaces, still clean). D6 content="   "
   proves whitespace-only counts as empty. S067@955 and `name=` interface phrase exact.
4. (:1006) PASS except offset (F1). Census arithmetic checked: 102-1=101 lack og:image,
   all-four=1; dominant defect claim holds (og:title/og:type/og:url all 87 vs image 1).
5. (:1007) PASS except offset (F1). D10 `og_type_multiple og:type`; K2 has two og:image
   metas and expects exit 0 — "repeated og:image is not a finding" verified.
6. (:1008) PASS. D9 `og_url_not_absolute og:url`; both grounding phrases exact.
7. (:1009) PASS except offset (F1). D8+D12 `og_url_not_canonical`; D12 is a literal
   scheme-only difference (http vs https) and fails — "scheme-only still fails" verified.
   K3 relative-canonical-resolves-equal and K4 no-canonical exit 0. Interface phrase exact.
8. (:1010) PASS with nit. I1-I7: 6 input_invalid + 1 page_unreadable, exit 2 phrase exact.
   Nit: `page_unreadable` glossed "(not UTF-8)" but I4 shows a missing file is also
   page_unreadable; the row mirrors the interface's own shorthand, so low impact.
9. (:1011) PASS. U1/U2 exit 64; verified live (no args -> exit 64, argparse error, no JSON).
10. (:1012) PASS. Independent recount of html.tar.xz (own HTMLParser, urljoin against
    https://ds4cc.com/<path>, index.html stripped) gives 102/87/87/1/87/1/87 — equals the
    census line and entry line. Counter at d08d8de: met 0/5, `census.derived` identical to
    verification/c2-at-d08d8de.json; at 24a1647 met 5/5. "met 0/5" is explicitly dated.
    Docstring condition (e) quoted verbatim.
11. (:1013) PASS. S069@685 and S070@3020 exact substrings.
12. (:1014) PASS except offset (F1). S069@974 exact; S068 scrape/debugger sentence present.
13. (:1015) PASS. S071@0 and S072@0 exact; S072 text does document a repository Settings
    social-media-preview image ("Settings" cluster at ~3991), so the scoping claim holds.

Condensed grounding (1019-1023): consistent with per-row findings; rows 4-7 offset claims
inherit F1. Trailer (1024): all verified — `--tool` flag exists (selftest:114), 29 fixture
dirs / 85 files, zero fixture bytes equal any matrix case file (byte-set compare), selftest
runs to exit 0 (29 cases, 0 failures), lesson Mistakes row 4 is exactly the hollow-counter
class describing dcef39b5/0cce15f0, and S073 states verbatim "The key comes from name if
present, otherwise from property" — so the property-only rule is indeed stricter than
Discord for <meta name="og:*">.

## Commands run (all in sandbox clone; TMPDIR=sandbox)

- python3 -B clone/scripts/link_preview_audit.py --manifest tmp/audit-run/manifest.json -> exit 1
- python3 -B clone/scripts/link_preview_audit.py (no args) -> exit 64
- python3 -B clone/.ufo/waves/round-34/c1_matrix_count.py --root clone --revision d08d8de -> exit 1, 0/28
- same at 24a1647 -> exit 0, 28/28, constantGatesAllRejected true
- python3 -B clone/.ufo/waves/round-34/c2_source_census.py --root clone --revision d08d8de -> exit 1, met 0/5
- same at 24a1647 -> exit 0, met 5/5, controlBroken false
- python3 -B clone/scripts/link_preview_selftest.py -> exit 0, 29 cases 0 failures

## Not verified / residual

- Whether the four S068 offsets were once correct against a pre-collapse extraction of
  S068; they are wrong against the pinned textSha256 bytes at 24a1647 either way.
- Row 8's `page_unreadable` paraphrase elides the missing-file case (I4); matches the
  interface's own wording, so I did not promote it beyond a nit.
- No lane files were edited; no network or live requests used.

Tooling: none installed; stock python3/tarfile/lzma sufficed. Pacman untouched (paused).
