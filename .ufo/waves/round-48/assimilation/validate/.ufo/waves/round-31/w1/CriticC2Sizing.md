# Round 31 wave 1 — CriticC2Sizing (C2 counter and claim sizing, freshness)

Seat: KakeR31.CriticC2Sizing. Base f1ffb81, declaration a16602a961da5d6e75cfa09a1118a416ad01225b. All writes in /fast/scratch/hyaku/kake-r31/w1/CriticC2Sizing/ except this report; no network, no installs.

## Counterexample: a hollow commit scores C2 4/4
Sandbox clone commit `b6580c798108b263fe4898178c4d7cedbdf30e56` (parent a16602a) adds 22 lines in 3 files:
- `corpus/SOURCES.md`: four rows `| S05x | <receipt URL> | x | x | x | x | x | mined | 2026-10-22 | x | x |`,
  appended after the file's closing prose, outside the `## Registry` table, every teaching cell `x`.
- `corpus/knowledge/render-web-services.md`: 9 lines; lines 2-8 are `.`, line 9 is `<!-- S057 S058 S059 S060 -->`
  (an HTML comment, invisible when rendered; the entry teaches nothing).
- `corpus/lessons/round-31.md` `## Gate`: S057 `“: '0 * * * *'”` (zero letters, from a cron example);
  S058 `“Home Your first deploy Free instances Platform”`, S059 `“Docs Changelog Search Ask AI Sign in”`,
  S060 `“Pricing Blog Security Customers Careers ©”` (sidebar, header and footer text present once in each of
  S057-S061, so each quote would "ground" any of the five ids).

`python3 -B .ufo/waves/round-31/c2_quote_truth.py --root . --revision b6580c79…` (in the clone) exit 0,
stderr `C2 4/4`, `controlBroken: false`, `counterSha256: de48d460…0c31b8`, all four checks true per id.
Output: /fast/scratch/hyaku/kake-r31/w1/CriticC2Sizing/hollow-c2.json (sha256 a7d6303d…e0fa7f).
Same counter at a16602a: exit 1, `C2 0/4`.

## Why it passes (c2_quote_truth.py at a16602a, blob sha256 de48d460…0c31b8)
1. Check d (lines 111-115) tests substring only, not where the quote sits: page navigation and footer chrome
   pass, and so does text shared by all five pages.
2. Check c (line 110) counts whitespace tokens, not words: `: '0 * * * *'` is 6 tokens with no letters. The
   control (lines 70-74, 117) then appends ` q` to a quote with no letters, so it holds trivially and catches nothing.
3. Check a (lines 102-105) takes the first line anywhere in SOURCES.md that matches `| S05x |`, not a row
   inside the Registry table. The URL test is `url in cells[1]` (a prefix-extended URL also passes), and the
   scope, anchor and teaches cells are never read.
4. Check b (line 106) needs only the bare id token after line 8, so a comment or an id list passes. No
   content, length or truth requirement exists for the entry.
5. Sizing: the declared after-value is "4/4 declared ids", which counts sourcing. SCORECARD.md:877-878
   admits this ("C2 proves sourcing ... the closure should read the entry body"), but the claim is labeled
   a learning claim (SCORECARD.md:834). Its other promise, "checks the lane's own Render property file
   against it" (SCORECARD.md:828-829), is not measured by the counter or by any closure check. The after-value
   can be reached for about 22 lines of zero knowledge, so a 4/4 result does not tell the hollow entry apart
   from a real one. Impacted axis: freshness. The risks are premature saturation and false provenance of
   learning.
6. counterSha256 (line 122) hashes the file that was executed, not the committed blob. An after-receipt
   naming de48d460… proves which file ran, not that it equals `<commit>:` (the closure's identity check
   covers that separately).

Fixable defect versus tradeoff: the counter is frozen by the declared identity hash (SCORECARD.md:882-884),
so editing it now breaks the closure's own identity check. The smallest safe correction is in the closure
reading, not in the counter. Do not change the counter mid-round.

## Do the "Closure checks" pass as written? Yes, and the hollow commit passes them too
- Identity: `git show b6580c79:.ufo/waves/round-31/c1_sandbox_probes.py | sha256sum` gives 4707cebf8831…3166d1a,
  and the same for c2_quote_truth.py gives de48d460aad8…e0c31b8, equal to the declared prefixes and
  suffixes and to `counterSha256` in verification/c1-before-f1ffb81.json and c2-before-f1ffb81.json (exit 0).
  The SCORECARD shows the hashes elided, so the full values have to come from those before-receipts.
- Stability: `git diff --quiet a16602a b6580c79 -- <the 7 listed paths>` exit 0. "<declaration commit>" is
  not named in SCORECARD (it cannot name itself). It resolves unambiguously:
  `git log --format=%H --diff-filter=A -- .ufo/waves/round-31/sources/receipts.json` and
  `git log -1 --format=%H -S'## Round 31 — declared claims' -- SCORECARD.md` both give a16602a96… (exit 0).
- Gap: the `S05x.html.gz` bodies are not in the diff list. At a16602a every body's sha256 equals receipts
  `bodySha256`, and re-running fetch_sources.py's `visible_text` on each body reproduces its `.txt` byte for
  byte, for S057-S061. Add the `.html.gz` files to the diff list or re-derive the text the same way.
- Both checks cover identity and stability only. Neither reads quotes or the entry, so neither catches the
  hollow construction.
- The round-30 provenance in the counter docstring ("blob a2cd3164") holds: it is the sha256 prefix of
  `HEAD:.ufo/waves/round-30/c2_quote_truth.py` (a2cd3164f67e…975e7a), not a Git blob id.

## Recommended closure reading
R1 (mechanical; prototype /fast/scratch/hyaku/kake-r31/w1/CriticC2Sizing/closure_probe.py, sha256 500f267e…aa6694).
  Each Gate quote must (a) sit in the page body, between the first and last `Copy page` marker or in the
  code tail after `© Render 2026`; (b) be absent from every other retained text, S057-S061; (c) have at
  least 4 tokens that contain a letter; and (d) its `.txt` must re-derive from its `.html.gz` and match
  `receipts.json`.
  Against the hollow commit it exits 1: S057 has 0 letter words; S058, S059 and S060 are outside the body
  and also appear in all four other pages (/fast/scratch/hyaku/kake-r31/w1/CriticC2Sizing/hollow-closure.json).
  Against a control commit `5eabd69c17093d2e9c1879b101644609964d18d4` it exits 0. That commit has real body
  sentences: S057 "healthCheckPath Web services only. The path of the service's health check endpoint .",
  S058 "The default value of PORT is 10000 for all Render web services.", S059 "Render can build your
  service's Docker image based on the Dockerfile in your project repo.", S060 "If an instance fails
  consecutive health checks for 60 seconds, Render automatically restarts the instance .".
  The body markers are a heuristic that fits these five Render pages only.
R2 (registry): each S057-S060 row must lie inside the `## Registry` table, have an exact source URL, and have
  scope, anchor and teaches cells whose anchor locates the Gate quote.
R3 (entry body, read by a person; required because the control commit `5eabd69c` keeps the empty entry and
  still passes both the counter (4/4, exit 0, control-c2.json) and R1). Strip HTML comments first. For each
  id, at least one entry sentence must state a Render semantic supported by retained body text, and no
  sentence may contradict it. Concretely, the entry should check ds4cc-marketplace render.yaml
  (`git show 1fbdb8ed:render.yaml`, blob d17ab7e5d44b…f7252, verified) field by field: `type: web`,
  `runtime: docker`, `dockerfilePath`, `dockerContext` (S057, S059); `healthCheckPath: /health` ("Web
  services only", "always starts with a /", S057); the 15 s stop-routing and 60 s restart rules (S060); the
  PORT default 10000 and binding to 0.0.0.0 (S058), which the file does not set; `envVars` with
  `sync: false` (S057). If that comparison is missing, the SCORECARD.md:828-829 promise is unmet
  regardless of the 4/4 result.

## Commands run (exit codes)
- Lane, read-only: `git log`, `git show a16602a:<counters> | sha256sum`, `git log --diff-filter=A …`,
  `git log -S …` (all 0); `python3 -B c2_quote_truth.py --root . --revision a16602a` in the clone (1, 0/4).
- Clone: `git clone -q <lane> clone` (0); two sandbox commits (0); counter at b6580c79 (0) and 5eabd69c (0);
  closure_probe at b6580c79 (1) and 5eabd69c (0); the identity and `git diff --quiet` closure checks at b6580c79 (0).
- `git -C /home/vgpnk/Projects/ds4cc-marketplace show 1fbdb8ed:render.yaml` and `rev-parse` (0).

## Not verified
The C1 counter was not run. No real C2 implementation has landed, so none was attacked. R3 is a reading
protocol not tested against a real entry. R1's body markers were not tested beyond S057-S061.
