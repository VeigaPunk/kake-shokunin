# CriticS062KindTier — S062 row contract (kind, tier, status, recheck)

Seat: KakeR32.CriticS062KindTier (critic, leaf). Axis judged: freshness. Revs read: 285abca (row tip
at dispatch), 7e05aa8 (lane tip at write time; adds corpus/lessons/round-32.md, S062 row unchanged:
`git diff 285abca 7e05aa8 -- corpus/SOURCES.md` empty). Contract: /home/vgpnk/Projects/shokunin/CORPUS.md
section "SOURCES.md — where a shokunin learns" (lines 64-148, contract v1, frozen).

## Verdict per cell (all four hold; no cell defect)

| cell | S062 value | verdict | contract sentence it rests on |
|---|---|---|---|
| kind | `code` | right | CORPUS.md:91-92 enum lists `code`; `own-work` is reserved for "a repo path or command for `own-work`" (CORPUS.md:90) and "the lane's own re-runnable gate output" (CORPUS.md:95-96). ds4cc-marketplace is a separate repo (origin github.com/VeigaPunk/ds4cc-marketplace), and render.yaml plus the Dockerfile are config-as-code, not a kake gate. |
| tier | `A` | right | CORPUS.md:93-94 "tier — scoped to `scope`, never global. A: primary or authoritative for that scope (spec, official docs, source code, ...)". The scope is "the content of the operator's own Blueprint file and Dockerfile at one commit, read offline; not a statement about the live Render service". A file at a pinned commit is the primary source for its own content. |
| status | `mined` | right | CORPUS.md:103 "`mined` (cited by ≥1 path in `used-by`)". used-by = corpus/knowledge/render-web-services.md. That file exists, and its appended section "Retained copies (round 32, append-only)" cites S062 twice (render-web-services.md:82, :88). |
| recheck | `90d` | right (valid); a tradeoff, not a defect | CORPUS.md:105-106 "`recheck` — ISO date or cadence (`90d`, `180d`, `on-release`)". The first value, "on ds4cc-marketplace render.yaml or Dockerfile change" (2f2f12d), was outside that form. The census flagged it as E09. The change to `90d` at 285abca is logged old to new in corpus/lessons/round-32.md:33-36 (at 7e05aa8), as rule 2 requires (CORPUS.md:116-117). |

## Comparison rows (tip 285abca, cells split on " | ")

- S014 (own-work, A, mined, 90d) and S019 (own-work, A, mined, on-release): both cite a kake script plus its
  run command (scripts/freshness-sweep.mjs, scripts/corpus-contract.mjs). S062 cites no kake script or
  command, so `own-work` would be the wrong kind.
- S056 (docs, B, queued, on-release): another lane's corpus prose, kept at B because it is "not a primary
  source for any fact about kake's citing-set gate". S062 is the artifact itself, not prose about it, so
  A is consistent with S056 being B.
- S001 (code, A, mined, on-release) is the closest precedent: a YAML file (action.yml) at a pinned commit,
  kind `code`, tier A. That supports S062's kind and tier.

## Strongest counterexamples tried

1. Kind. The entry heading "## The lane's render.yaml at ds4cc-marketplace 1fbdb8ed"
   (render-web-services.md:50, introduced at fde133a, round 31) calls the file "the lane's", which suggests `own-work`.
   Rejected: CORPUS.md:95-96 ties own-work at tier A to the lane's re-runnable gate output, and S001 sets the
   precedent for a pinned config file as `code`. Only the heading wording conflicts; the row is fine.
2. Tier. The row is anchored on the GitHub URL, but the source was opened with `git cat-file` on the local clone, not the URL.
   This does not weaken the tier: git objects are content-addressed, and both blob ids match (see below).
3. Recheck. The scope pins an immutable commit, so a recheck of the scoped content can never find a change.
   The precedents S001 and S056 both use `on-release`, and that symbolic cadence would also have passed the census.
   `90d` is valid, but its action is undefined (next section). This is a tradeoff the judge may weigh, not a contract break.

## Adjacent gaps (freshness; outside the four cells, fixable)

- No recheck action is tied to S062. The entry's `recheck:` line (render-web-services.md:3) re-opens only the
  Render Docs pages (S057-S060). The appended section re-checks sentences against the retained copies, a
  byte-for-byte comparison that cannot detect upstream drift. When 90d expires, nobody has a defined step
  that would notice a later ds4cc commit. Smallest safe correction (append-only, new section in the entry):
  name the drift check `git -C ~/Projects/ds4cc-marketplace diff --stat 1fbdb8ed <HEAD after fetch> -- render.yaml
  apps-sdk/Dockerfile`.
- The entry's `source:` line (render-web-services.md:1) lists only S057-S060. A freshness sweep that reads
  `source:` will not see S062 (CORPUS.md:163-167, the kaika rule on the provenance trio; strictly binding only on new entries).
- The Gate quote (round-32.md:31) covers render.yaml lines 2-7 only. The row's `teaches` also claims "OPENAI_APPS_CHALLENGE
  as sync: false", which is on lines 15-16 and outside the quote, so the quote only partly grounds `teaches`
  (CORPUS.md:112-114). The quote also says "13 words"; I count 12 whitespace-separated tokens. Both are cosmetic.

## Commands run (exit codes)

- `git rev-parse HEAD` in the lane, at dispatch → 285abca…; later `git log --oneline -3` → 7e05aa8 on top (exit 0).
- awk cell split of header + S014/S019/S056/S062 (exit 0): every row has 11 cells.
- `git show 285abca -- corpus/SOURCES.md`: S062 recheck `-on ds4cc-marketplace render.yaml or Dockerfile change` / `+90d` (exit 0).
- In sandbox clone /fast/scratch/hyaku/kake-r32/w1/CriticS062KindTier/clone at 285abca:
  `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-22 --file corpus/SOURCES.md` → exit 0;
  only `W04 S033`, no finding on S062. The overdue mode prints `cadence S062 recheck=90d opened=2026-10-22`.
- The same validate run on `git show 2f2f12d:corpus/SOURCES.md`, copied to the sandbox tmp dir → exit 1, `E09 S062 recheck=on ds4cc-marketplace
  render.yaml or Dockerfile change`. Its E11 lines are an artifact of validating a copy outside the repo:
  used-by paths resolve against the tmp dir. They are not lane defects.
- `git cat-file blob d17ab7e5…` in ~/Projects/ds4cc-marketplace (read-only) → 20 lines. Line 2 `type: web`, line 4 `runtime: docker`,
  line 6 `dockerContext: .`, line 7 `healthCheckPath: /health`, lines 15-16 `OPENAI_APPS_CHALLENGE` `sync: false`.
  These match `teaches`.
  `git rev-parse 1fbdb8ed:render.yaml 1fbdb8ed:apps-sdk/Dockerfile` → d17ab7e5…, ee0b6381… (match the anchor).
- `git hash-object` on the retained copies → d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252 and ee0b63819a9ce71e51469796541b9075e9676ae9 (exit 0).
- The local ds4cc clone's HEAD is 1fbdb8ed itself (2026-10-21), so no drift is visible locally.

## Not verified

- Whether github.com/VeigaPunk/ds4cc-marketplace is public. Rule 6 (CORPUS.md:129) bars private URLs from rows.
  This seat had no network authorization; the URL was not opened.
- Whether upstream ds4cc has commits after 1fbdb8ed. The local clone was not fetched.
- The c2 counter and the receipts belong to sibling seats; I did not rerun them.

Tooling: none installed or updated. Impacted axes: freshness (recheck action gap); operability untouched.
