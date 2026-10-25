# RowRenderServices

Claim C1 (coverage-map calibration), one row only. Target section: `corpus/README.md`
§Coverage map (lines 15–46, i.e. up to the `## Known gaps` heading at line 47), whose
rows use the 3-cell form `| Area | Entry | Coverage |`. At base revision
`fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d` the C1 counter names this file as unindexed
there: `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`
printed `C1 readme-index index_mismatches=21 knowledge_files=46 met=False`, exit 1, with
`unindexed: render-web-services.md` in the list (read-only run; no write, no network).
The file is not edited; only this report is written.

ROW:

```markdown
| Render web services and Blueprint (r31) | `knowledge/render-web-services.md` (S057, S058, S059, S060) | Render's documentation for web services: the required 0.0.0.0 port bind, a Docker build context filtered by .dockerignore, health-check success at 2xx or 3xx within five seconds, and an offline key-by-key check of the lane's own render.yaml at ds4cc-marketplace commit 1fbdb8ed. |
```

Checks run in memory against the worktree bytes (no README edit, no counter re-run on a
patched tree): 3 cells; Area 6 words; Coverage 40 whitespace tokens (10–45 required, ≥5
for the counter); no `|` in the Coverage cell; does not start with `TBD`; Entry token
`knowledge/render-web-services.md` exists at base, so the counter's `dangling` term gains
nothing; the Coverage cell's 5+-letter words intersect the H1 plus first 1500 characters on
`render`, `services`, `docker`, `build`, `health-check`, `offline`.

EVIDENCE:

1. `corpus/knowledge/render-web-services.md:21` — "Your web service must bind to a port on host 0.0.0.0 to receive HTTP requests from the public internet." (19 units; raw substring, on that line, S058). Rests on: "the required 0.0.0.0 port bind".
2. `corpus/knowledge/render-web-services.md:30` — "Render omits files and directories from your build context based on your .dockerignore file." (14 units; raw substring, on that line, S059). Rests on: "a Docker build context filtered by .dockerignore".
3. `corpus/knowledge/render-web-services.md:36` — "For HTTP checks , Render considers a check successful if the instance responds with a 2xx or 3xx status code within five seconds." (23 units; raw substring, on that line, S060; the space before the comma is in the retained text). Rests on: "health-check success at 2xx or 3xx within five seconds".
4. `corpus/knowledge/render-web-services.md:4` — "an offline key-by-key check of the lane's own render.yaml at ds4cc-marketplace commit 1fbdb8ed" (13 units; raw substring, on that line; the header `scope:` line). Rests on: "an offline key-by-key check of the lane's own render.yaml at ds4cc-marketplace commit 1fbdb8ed". The section it points at is `## The lane's render.yaml at ds4cc-marketplace 1fbdb8ed` (line 50), whose line 52 records the offline read: "Read offline with `git -C ~/Projects/ds4cc-marketplace show 1fbdb8ed:render.yaml`" (8 units, raw substring).

The Area's `(r31)` tag is taken from the file's own header, which names the round twice
(`.ufo/waves/round-31/sources/` on line 2, the round-31 counter on line 3); the H1 is
"# Render web services and the Blueprint file" (line 10).

RISKS:

- Four-reference budget: the row cannot also state the facts the file carries on default
  port 10000 ("The default value of PORT is 10000 for all Render web services.", line 71,
  12 units), deploy on push (line 20), the container start / Docker Command rule (line 28),
  zero-downtime deploys (line 31), the deploy-cancel, routing-stop, restart and Host-header
  rules (lines 37–39), or the Blueprint retain and `sync: false` rules (lines 45–47). Saying
  any of them would need a fifth reference, so the row stops where its references stop; the
  round-31 row at `corpus/README.md:296` (inside `## Coverage — round 31`) carries that detail.
- The row must not describe the live service. The file's own header says "nothing about the
  live service is asserted" (line 4, 7 units); its lines 65–67 place the port, plan, region,
  deploy trigger and subdomain policy in dashboard state not visible from `render.yaml`.
- Duplicate index: `corpus/README.md:296` already indexes this same file in the round-31
  section. The counter reads only `## Coverage map` (`coverage_section` in
  `c55_readme_index.py`), so the new row is the one measured, but the two rows describe one
  file and can drift if the file is appended again; both must be touched together.
- Staleness: `verified-at` is 2026-10-22 with `recheck: 90d` (due 2027-01-20), so the file is
  not stale on the round date 2026-10-25. Its round-32 drift check ("the remote `main` is
  `7fc6aa2`, one commit ahead", lines 104–105) was not re-run this round and is historical;
  the row asserts no freshness beyond that.
- Inaccuracies in the file itself (corrected only by appended blocks, so a reader of the body
  alone meets them): line 22's bracketed `[INFERENCE]` says the PORT mechanism "is not stated
  from a source here" while line 71 supersedes it with the retained S058 sentence; lines 89–90
  say `apps-sdk/src/server.ts` "is not retained", superseded by the round-32 wave-1 correction
  at lines 92–101. The row therefore rests on neither statement.

VERDICT: One 3-cell §Coverage map row drafted for `knowledge/render-web-services.md`, all four Coverage clauses quote-backed (≤25 units, raw substrings) and the counter's thin/unindexed/dangling terms satisfied in-memory; file untouched.
