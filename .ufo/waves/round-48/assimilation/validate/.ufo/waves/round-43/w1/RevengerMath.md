CONFIRMED — the r43 registry-arithmetic correction re-derives exactly from committed bytes; the r42 stated counts fail at both ends.

Seat: kake-r43-w1-RevengerMath. Target: routed repair 1 (SCORECARD.md:3264-3271). Independent
re-derivation with the CORPUS.md census commands (`/home/vgpnk/Projects/shokunin/CORPUS.md:131-147`,
recorded argv/output `.ufo/round-20/resume/sources-census.txt`), no read of
`registry_count_check.py` output or freeze receipts before deriving.
Commands (all exit 0 unless noted):
  git show 1ef7a0e95f6884dd113fe583a997c633fe330ddd:corpus/SOURCES.md
  git show 5949e66ffe803859372adc975dd7392f0f07d626:corpus/SOURCES.md
  grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' <file>
  awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{...}' <file>
  plus the NF!=13 / duplicate-id / enum validation commands.

Derived table (my derivation vs r43 correction vs r42 claim at the same named revisions):

| count     | base 1ef7a0e9 derived | r43 states | r42 states |
| rows      | 119                   | 119        | 128        |
| mined     | 92                    | (implied)  | 99         |
| queued    | 8                     | (implied)  | 8          |
| rejected  | 19                    | (implied)  | 21         |
| malformed | 0                     | —          | —          |

| count     | tip 5949e66ffe derived | r43 states | r42 states |
| rows      | 128                    | 128        | 131        |
| mined     | 99                     | (implied)  | 100        |
| queued    | 8                      | (implied)  | 8          |
| rejected  | 21                     | (implied)  | 21         |
| malformed | 0                      | —          | —          |

| delta     | derived | r43 states | r42 states |
| mined     | +7      | +7         | +1         |
| queued    | +0      | +0         | (0)        |
| rejected  | +2      | +2         | (0)        |

Id-status diff base→tip: pure additions S120–S128 = 7 mined (S120–S124, S126, S127) + 2
rejected (S125, S128); zero status transitions on pre-existing rows. r42's "128" is the tip
value restated as the base; "131" has no support in committed bytes at either named revision.

Revisions named by the rounds: r42 base `1ef7a0e9` (SCORECARD.md:2909); tip `5949e66ffe`
(SCORECARD.md:3184 names it the r42 verdict revision; `corpus/knowledge/claim-count-
derivation.md:12-14` confirms it is the registry tip r42's census covered). r42 claim text:
SCORECARD.md:3172 "rows 128 → 131, mined rows +1 net of supersessions".

Census validator re-run (independent of count derivation):
  `timeout 600 bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
     --root /home/vgpnk/Projects/shokunin kake` → exit 0; 12 W04 duplicate-url warnings
  (S033 S088 S092 S098 S099 S102 S110 S111 S115 S116 S117 S127) + `kake ok`; no E-findings.
  Matches `verification/freeze/census-after-r43.txt` shape (advisory W04s, not failures).

Cross-check at freeze commit b49cba9: grep census → 130 rows (S129/S130 landed);
mined=101 queued=8 rejected=21; malformed 0. Consistent with SCORECARD.md:3275 (128→130).

Checked statements:
- SCORECARD.md:3266-3267 "119 → 128 rows; mined +7; queued +0; rejected +2" — holds exactly.
- "superseding rows S120–S128 added on top of base 1ef7a0e9" — holds (9 rows, all new ids).
- SCORECARD.md:3269-3270 checker red on r42 claims / green on r43 correction — consistent
  with my derivation (r42 stated 128/99/8/21→131/100/8/21 mismatches every base+tip number;
  r43's 119/92/8/19→128/99/8/21 matches all; I verified the checker's claims JSON inputs, not
  its printed output, as required).
- SCORECARD.md:3172 r42 "rows 128 → 131, mined +1 net of supersessions" — wrong at all four
  stated numbers (overstated base by 9, tip by 3, under-delta mined).
- Census validator "exit 0 after" (SCORECARD.md:3171, 3274) — holds on re-run.

Tools: GNU Awk 5.4.1, git, coreutils — no installs needed; nothing installed.
Lane repo untouched; only this report written. Sandbox artifacts: none (worked on /tmp copies).
