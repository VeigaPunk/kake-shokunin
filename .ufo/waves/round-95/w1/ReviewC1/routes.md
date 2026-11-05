# ReviewC1 — round-95 C1 counter attack (Summary routes table)

Verdict line: **C1-ATTACK refused=27 false-greens=NG01,NG08,NG11**

Full analysis, receipts and residual risks: `ReviewC1.md` (sitting next to this file). Per-run
receipts under `receipts/runs/`. Fixture code under `receipts/fixtures/`.

Refused: R01 R02b R03 R05 R05b R08 R09 R10b R12 R18 NG02 NG03 NG04 NG05 NG06 NG07 NG09 G7a G7b G7c
False-greens (audit level, zero scope today on the real lane):
- **NG01/NG08** — round-95 lesson with a `## Gate — admit X, reject Y` **heading** over a junk
  body reads `mismatches=0` under E1 (the regex `admit|reject` matches the heading, which is
  enough; body junk is not separately checked once the heading carries one admit and one
  reject token).
- **NG11** — E1 matches `admit`/`reject` as SUBSTRINGS of unrelated words (`admiralty`,
  `rejection`) — an arbitrary-prose body reads clean.
