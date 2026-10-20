# NoPublish — round 21 W1 sentinel report

Scope: the boundary between the round-21 corpus work (C1 provenance trio, C2 historical Gate sections) and operator-owned publishing. Only `SKILL.md` and `PROVINCE.md` were inspected, and both were read in full. I did not open any knowledge or lesson files, credential or auth files, or `agent.db`. No network reads, no commands that could write, and no tool installs or updates.

## Evidence base

- HEAD = shared base `5009ecaa1cce10b895617a585ddd3f7c7c923a84`. `git diff --stat <base> -- SKILL.md PROVINCE.md` printed nothing, and `git status --short` on both files also printed nothing, so both files match the base exactly.
- sha256 `SKILL.md` = `db765562cc968e462507062d2bf03a6cbf08e8db866d9c29f4ab9af5a58da19b`; `PROVINCE.md` = `650e65224fff95351a35f5c30755a77e8e8fe5bb2a9c3af5feab69610dac9a39`.
- `test -e` (2026-10-20) found all of these missing: `~/Projects/webzites`, `…/bin/webzites.mjs`, `…/scripts/kimi-surface.mjs`, `~/Projects/ds4cc-marketplace`, `~/Projects/plazir-15-site`, `~/Projects/lucario`, `~/Projects/origin-work`, `kake-shokunin/scripts/kimi-surface.mjs`. `command -v webzites` returned nothing.
- **Result:** none of the commands SKILL lists for writing or publishing can run on this host today, because the binaries and source trees are gone. The risk is that a C1 or C2 author copies one of them into a "recheck" line. If the tools are later restored, that line becomes a live command.

## Red lines — never acceptable as a C1/C2 recheck recipe

| # | Sev | Recipe text in SKILL | Effect if executed | Exploit path / impact |
|---|---|---|---|---|
| R1 | Critical | `update\|recreate\|rebuild <id> --fire --confirm=<id>` (SKILL:126-128). The `--chat=<uuid>` preflight form is one flag away (SKILL:127) | Uses up one metered fire. Firing into a chat already bound to a live site **hot-swaps that live site** (SKILL:21, "One chat = one publish slot"; `ufo-fsd.kimi.pro`/`.page` share a site-id, so one fire may write both) | This works as a publish even though no Publish click happens. The only safeguard is `--confirm`, a flag any agent can type. A Gate line such as "recheck: rebuild preflight" loses the word *preflight* when copied, and the mistake cannot be undone. |
| R2 | Critical | `git push origin main` (SKILL:122, 155, 375); version-card Publish / Share→Update click (SKILL:129); `PublishApp`/`PublishDeployment`/`UnpublishApp` (SKILL:130, 376) | Live deploy | These are already hard operator red lines (SKILL:375-377; PROVINCE Core "Publishing itself stays operator-gated"). No recheck may cite them, even as a "verify by re-pushing" step. |
| R3 | High | `node -e` eval of the `const PROPERTIES = [...]` literal from the fetched vault body (SKILL:231, 260-261) | **Runs remote page content as code** with full Node privileges (fs, child_process, network) | Anyone who can change the veigapunk.kimi.page body, whether via a Kimi chat fire or a compromised slot, can append code after the array. That code then runs on the operator host with every permission the agent has, so it can write, push, or exfiltrate. This is a trust-boundary break inside a recipe labelled read-only. **Smallest fix:** extract the literal and parse it without evaluating it (for example `JSON.parse` after normalising, or an AST parser that rejects anything other than a literal). Never use `eval`, `node -e`, or `vm`. |
| R4 | High | "treat as `git fetch sourceDir` + spotcheck" (SKILL:222, GHP reconcile blind spot) | Writes refs and objects into a **domain source tree** and reads the network | Breaks the round contract that domain source trees are read-only, and runs a network read nobody authorised. The read-only alternative is `git show origin/main:<rel>` (SKILL:228) against refs that already exist. |
| R5 | High | `deploy-github-pages.sh` (SKILL:123, 365) | Per SKILL it is a setup script that edits CNAME and remotes and prints DNS settings. Whether it can push is not established `[INFERENCE: source absent, unread]` | Running it to "recheck" the domain setting writes to the source tree, and its push behaviour is unknown. |
| R6 | Medium | `webzites probe --all` / `probe <id>` (SKILL:59-60, 87-105, 220) | Overwrites `state/probe-latest.json` and appends a permanent history line | **Fake readiness:** a one-id probe shrinks the snapshot to `total:1`, so `webzites status` exits 0 while 5 violated rows and 1 error row are hidden fleet-wide (SKILL:104-107). A C2 Gate that says "recheck: `probe <id>`" would turn a failing gate into a passing one. |
| R7 | Medium | `webzites grokbot tick` (SKILL:225); `bots task` (SKILL:92) | Writes state and appends keeper logs for every site | Listed under "drift detection", but it writes. Keeper enable-vs-retire is an operator decision (SKILL:77-78). |
| R8 | Medium | The probe "recipe": `cp probe-latest.json` → run → `cp` back (SKILL:94-97) | Restoring the file still leaves a permanent `total:1` history line | The "backup/restore" wording makes it look harmless when it is not. |
| R9 | Medium | `webzites lease acquire` (SKILL:159); `kimi-map`, `GetWebsiteByChatID` (SKILL:126, 134-135, 223, 281, 288, 327) | Writes lease state and drives the shared `the-musketeer` logged-in profile (CDP :9222) | The profile is auth custody (kagi), and its scope is contested and held by the integrator (PROVINCE Adjacent). SKILL's word **"free" means unmetered, not read-only and not auth-free** (SKILL:126-127, 133). A Gate that copies "free reads" claims a safety the recipe does not have. |
| R10 | Medium | `speedrun record → report → prep --write`; operator `cp` into `ds4cc-marketplace/speedrun/data/` (SKILL:151-155) | Writes staged run bodies, and the operator step writes into the domain source and then pushes | Must stay operator-only. `speedrun post` only prints, but it sits in the same chain. |
| R11 | Medium | Edit `expect.marker` in `fleet.config.json` (SKILL:175-179); `git format-patch` / `git am --check` against a fresh clone (SKILL:119-120); commit path-scoped in source repo (SKILL:116) | Writes to the registry or source, and cloning reads the network | SKILL itself routes the marker edit through the publish queue (SKILL:178-179). None of these are allowed as a round-21 recheck. |
| R12 | Medium (round contract) | Bare `node scripts/freshness-sweep.mjs` (SKILL:184, 350 "Run it before citing anything"); every "GET …" row (SKILL:227-231); `sync-check` (SKILL:221); `grep -o` on a fetched body (SKILL:177) | Domain network reads | Round 21 bans extra domain network reads, and the registry row says the bare form needs authorisation for network checks (SKILL:212). SKILL:184 and SKILL:350 still present the bare form as the default instruction. A C1 "re-verify" line that cites the bare form also implies a live check, which C1 is explicitly not meant to be. |
| R13 | Low | `freshness-sweep.mjs --selftest` (SKILL:212) | Writes fixtures. Isolation is only safe if the caller sets `HOME` and `KAKE_SELFTEST_DIR` to temporary directories | The registry itself says confinement is incomplete: aliasing, bracket access, multi-line calls, metadata/fd writes and child-process side effects are named residual bypasses (SKILL:212). |

## Hazards in the text itself (no edits made; SKILL is L1-owned)

- **H1:** Rows in the drift table are written as runnable commands but carry no historical annotation on the same line. SKILL:220 (`webzites probe <id>`), 222 (`webzites grokbot reconcile`), 223 (`node ~/Projects/webzites/scripts/kimi-surface.mjs kimi-map`, which cites a missing absolute path) and 225 (`webzites grokbot tick`) lack the "historical record, not an executable instruction" note that SKILL:59 and SKILL:111 carry. SKILL:221 uses the relative path `node scripts/kimi-surface.mjs`, which from the kake repo points to a missing file and from any other cwd is ambiguous. These lines are the most likely source of copy-paste recheck recipes. `[INFERENCE]` SKILL:223 may also be counted by freshness-sweep §paths as a citation without an annotation; not run here, so Main should confirm with the `--offline` sweep.
- **H2:** SKILL:184 and SKILL:350 (bare sweep as the default) contradict SKILL:212 (bare form needs authorisation).
- **H3:** PROVINCE.md is consistent with the boundary: it states operator-gated publishing, kagi custody and the contested profile, and that round 20 was documentation-only with no probes. Nothing there needs action.

## Allowlist for C1/C2 recheck recipes this round

Use only commands that read local state and need no auth:

- `test -e <path>`
- `git -C kake-shokunin log|show|diff`, read-only, against the kake repo only
- `grep -F` over corpus files
- `node scripts/freshness-sweep.mjs --offline`. The registry says its normal path only reads, and that the static confinement proof is incomplete.
- `node scripts/probe-delta.mjs`. SKILL says it only reads. `[INFERENCE]` Its input `~/Projects/webzites/state/probe-history.jsonl` is missing, so it will report could-not-evaluate rather than give a verdict.

Anything else must be written as a dated historical citation: "historical record, not an executable instruction", following the SKILL:59 pattern. It must never be written as a recheck step.

## Recommendation to Main/L1 (smallest remediation)

1. Integration gate for the C1/C2 diffs. Before integrating, grep every new line for `--fire|--confirm|git push|git fetch|probe --all|probe <|grokbot tick|bots task|lease acquire|node -e|kimi-map|GetWebsiteByChatID|deploy-github-pages|prep --write|format-patch|clone|freshness-sweep.mjs(?! --offline)| GET `. Each hit must either sit inside an explicit historical-record annotation or be rejected. I did not inspect the knowledge or lesson files, so I cannot say whether any are present.
2. L1 (SKILL owner): add the same-line historical annotation to SKILL:220-225 and replace the `node -e` eval in SKILL:231 and SKILL:261 with a parse that does not execute code (R3). Both are prefix or inline additions, but they edit lines that already exist, so the byte-identical preservation rule means they need L1 and operator sign-off rather than a round-21 seat edit.

## Limitations

- Only `SKILL.md` and `PROVINCE.md` were inspected. The new C1/C2 content was out of scope and not reviewed.
- R5 and the probe-delta input behaviour are inferences, because the source trees are missing from the host.
- I ran no sweep, no selftest and no network commands.
- `resume_continuity_v1` zero-mutation was not on this surface and was not exercised.

## File changes

- Created: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-21/w1/NoPublish.md` (this report). No other files were touched.
- Tools installed or updated: none.
