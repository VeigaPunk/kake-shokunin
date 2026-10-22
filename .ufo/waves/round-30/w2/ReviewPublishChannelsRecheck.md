# Review: Round-30 Render recheck tail (corpus/knowledge/publish-channels.md)

Seat: KakeR30.ReviewPublishChannelsRecheck. Leaf reviewer, wave 2 (falsify). Axis: freshness. Milestone r30-falsify.
Sandbox: /fast/scratch/hyaku/kake-r30/w2/ReviewPublishChannelsRecheck/ (render.yaml.HEAD, verification-summary.txt).

## Versions reviewed
- corpus/knowledge/publish-channels.md, working tree: sha256 4b9a70b122bcc4c62689999aa4bd047c995cb9b218f029b8a8981bbee189f255 (11600 bytes, mtime 10:23:37 -03:00). Committed HEAD 451e98f (10:18:33 -03:00) lacks the "(lines 9-10)" and "(lines 13-14)" citations at lines 96-97. Both versions carry the same claims.
- corpus/knowledge/render-static-sites.md, working tree: sha256 8d6a833fcb72ee5665f489192547242d740c38035c588959b6046153579f504b (mtime 10:24:35). It changed after my first read; this is the version I used.
- ~/Projects/ds4cc-marketplace: HEAD = refs/heads/main = refs/remotes/origin/main = 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28. render.yaml blob d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252. File clean.

## Findings, by severity

1. MEDIUM. Overreach on the Blueprint domain claim (publish-channels.md:101-102). The file-level fact holds: HEAD render.yaml has no case-insensitive "domain" match. But "so app.ds4cc.com is not attached by this Blueprint" is a claim about the Blueprint schema, and no retained page documents that schema. The sibling file says it is not settled: render-static-sites.md:105-110 cites an unretained wave-1 report of a `domains` field. The bracket "[INFERENCE: attached in the dashboard or not at all]" is narrower than the evidence. S052 names the dashboard as the add-domain path. Apart from navigation links, S052 mentions Blueprint and Render API only as ways to disable the onrender.com subdomain. Fix: tag "not attached by this Blueprint" as INFERENCE and cite the unsettled status.

2. MEDIUM-LOW. Blanket scope is wrong for custom domains (publish-channels.md:107-109). "Static-site semantics ... do not apply to this Docker web service" fails for domains and TLS. S052 says "You can apply your own custom domains to Render web services and static sites" and "Only web services and static sites support custom domains". render-static-sites.md:57 and :60 carry that over. S049, quoted at :60, says TLS covers "every site and service". What does not carry over: static build and CDN (S049, :31-32 "Create a web service instead of a static site."), static response headers (S051, :48-49), and static redirects (S050; SOURCES.md:58 heading "Static Site Redirects and Rewrites"). Fix: scope the sentence to build, CDN, redirect/rewrite and static headers.

3. LOW. Default-host qualifier omitted (publish-channels.md:102-106). S052 section "Disabling your onrender.com subdomain" (retained text, offsets about 6095-7051): a service with a custom domain can switch off its onrender.com subdomain in the Dashboard, the Blueprint, or the Render API; afterwards requests to it get 404. The tail says the service "keeps its default host" and that this is consistent with ALLOWED_HOSTS. That holds only while the subdomain is on. render.yaml sets no renderSubdomainPolicy. render-static-sites.md:64 already says this. Fix: add the qualifier.

4. LOW. "ADDED" misdates the lines (publish-channels.md:98-101). Git: ALLOWED_HOSTS and OPENAI_APPS_CHALLENGE entered render.yaml in 1c8feeb (2026-07-18T15:50:46-03:00). MAX_UNAUTHENTICATED_SESSIONS and MCP_SESSION_IDLE_TIMEOUT_MS entered in 3cd3534 (2026-07-19T13:39:41-03:00). The section was created in cd5b381 (2026-09-28T15:39:11-03:00) and names none of the four keys. So the gap dates from creation, not from a later edit. dockerContext: . (line 6, added in 3cd3534) is also missing from the section and from the list. Fix: "in the file since 2026-07-18/19; never listed in the section".

5. LOW. "Nothing live was fetched" is scoped too wide (publish-channels.md:106-107). The tail cites S052, which receipts.json shows was a live GET at 2026-10-22T11:49:45Z (status 200). Scope the sentence to the render.yaml and service check. The clause "whether the service is deployed and answers on either host is not observed here" is correct.

6. NOTE, freshness. "HOLD" label drift. publish-channels.md:65 defines HOLD as an observation from read-only live checks. Round 30 uses HOLD for a local checkout read. Its origin/main is a local remote-tracking ref. No FETCH_HEAD exists, and .git/packed-refs has mtime 2026-10-22 03:05:10 -03:00. I could not confirm GitHub's current main, since network is not permitted. "Still" therefore describes the last-fetched local ref. Fix: call it a local-checkout HOLD.

7. NOTE, integration. The lane working tree differs from committed HEAD: publish-channels.md has 2 insertions and 1 deletion (lines 96-97); render-static-sites.md has 44 insertions and 18 deletions. Both are uncommitted. The integrator must pin one version. The added line citations are correct.

## Statement by statement (working-tree tail, lines 86-109)

| # | Lines | Statement | Verdict and evidence |
|---|---|---|---|
| 1 | 88-89 | append-only; section above unchanged | Holds. Diff against base 035668132: one hunk `@@ -84,0 +85,25 @@`, 25 insertions, 0 deletions |
| 2 | 90-91 | checkout 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28 | Holds. HEAD = main = origin/main |
| 3 | 91-92 | render.yaml blob d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252 | Holds. rev-parse HEAD:render.yaml, hash-object and size 565 agree; blob unchanged since 3cd3534 |
| 4 | 92-93 | working tree clean for that file | Holds. `git diff --quiet HEAD -- render.yaml` exit 0; whole repo clean |
| 5 | 93-95 | HOLD lines 2-7: type web, runtime docker, dockerfilePath, healthCheckPath | Holds. render.yaml lines 2, 4, 5, 7; apps-sdk/Dockerfile is a blob at HEAD |
| 6 | 96 | APP_ORIGIN=https://app.ds4cc.com (lines 9-10) | Holds |
| 7 | 97 | ALLOWED_ORIGINS=https://chatgpt.com (lines 13-14) | Holds |
| 8 | 98-99 | ALLOWED_HOSTS=ds4cc-marketplace-app.onrender.com (lines 11-12) | Holds |
| 9 | 99-100 | MAX_UNAUTHENTICATED_SESSIONS, MCP_SESSION_IDLE_TIMEOUT_MS, non-synced OPENAI_APPS_CHALLENGE (lines 15-20) | Lines hold: 15-16 sync false, 17-18 "64", 19-20 "120000". Label defect: F4 |
| 10 | 100-101 | section above omits them | Holds. Section lines 24-28 name only the service, Dockerfile, /health, APP_ORIGIN, ALLOWED_ORIGINS |
| 11 | 101 | file has no domains key | Holds. `git grep -n -i domain HEAD -- render.yaml` exit 1 (no match at all) |
| 12 | 101-102 | not attached by this Blueprint [INFERENCE: dashboard or not at all] | Defect: F1 |
| 13 | 102-104 | S052: a web service can carry a custom domain | Holds. S052.txt: "You can apply your own custom domains to Render web services and static sites ." |
| 14 | 103-104 | "keeps its default host" | Holds as the default; qualifier omitted: F3 |
| 15 | 104-105 | quoted S052 sentence | Holds verbatim. See S052 check |
| 16 | 105-106 | consistent with onrender host in ALLOWED_HOSTS [INFERENCE] | Holds as a labeled inference, subject to F3 |
| 17 | 106-107 | "Nothing live was fetched" | Defect in scope: F5 |
| 18 | 107-108 | service deployed/answers not observed | Holds. No network use; /health and dashboard not touched |
| 19 | 108-109 | static-site semantics "do not apply" to this Docker web service | Defect: F2 |

## S052 quote check
- receipts.json S052: accessedUtc 2026-10-22T11:49:45Z; status 200; finalUrl https://render.com/docs/custom-domains; bodyBytes 371923; bodySha256 59469467... equals sha256 of gunzipped S052.html.gz; textSha256 6c1616f8... equals sha256 of S052.txt; textWords 1488.
- "Services with a custom domain also keep their onrender.com subdomain." occurs exactly once in S052.txt and once in the HTML text nodes (tags stripped, entities decoded). My rebuild of the stated text rule matches S052.txt word for word; only the trailing newline differs.
- Verdict: verbatim, holds.

## Commands run (exit codes as reported; 0 where the tool reported success)
- `mkdir -p /fast/scratch/hyaku/kake-r30/w2/ReviewPublishChannelsRecheck`: 0. First attempt used a missing cwd and failed; the re-run created it first.
- ds4cc (cwd /home/vgpnk/Projects/ds4cc-marketplace): `git rev-parse HEAD` 0; `git rev-parse HEAD:render.yaml` 0; `git status --porcelain` 0 with 0 entries (no --no-optional-locks, so it may refresh the index stat cache; no content change); `git cat-file -t` and `-s HEAD:render.yaml` 0; `git hash-object render.yaml` 0; `git diff --quiet HEAD -- render.yaml` 0; `git show HEAD:render.yaml | cat -n` 0; `git grep -n -i domain HEAD -- render.yaml` 1; `git cat-file -t HEAD:apps-sdk/Dockerfile` 0 (blob); `git log -p -- render.yaml` 0; `git log -S <key> -- render.yaml` per key 0; `git for-each-ref` 0; `stat .git/packed-refs` 0; `stat .git/FETCH_HEAD` error (absent); `git cat-file -t cd5b381` printed "fatal: Not a valid object name" (wrong repo, exit code not captured; the commit is in the lane).
- kake-shokunin, git with --no-optional-locks, read-only: `rev-parse HEAD`, `log -n 8`, `diff --stat` and `diff -U0` against 035668132 (0); `diff HEAD -- publish-channels.md` 0; `diff --stat HEAD -- render-static-sites.md` 0; `status --porcelain` 0; `grep -c 'Round-30 Render recheck' HEAD` (count 1); `grep -n 'Render — app.ds4cc.com' cd5b381` 0 (line 19); `merge-base --is-ancestor cd5b381 HEAD` 0.
- Python reads (sha256, quote counts, text-rule rebuild, section-at-cd5b381 check): 0. Sandbox writes only: render.yaml.HEAD (hash-object re-check matches d17ab7e5) and verification-summary.txt.
- No network request of any kind. No freshness-sweep, probe-delta or live_snapshot run. No install or update; no tool needed.

## Verification gaps
- Not observed: GitHub's current main (no ls-remote; network forbidden), the deployed Render service, /health, the Blueprint schema (the render.yaml reference is not retained), and the wave-1 `domains` and `staticPublishPath` reports (unretained).
- Not run: c2_quote_truth.py (it writes into the lane). The quote check used direct substring and hash checks instead.
- LSP: not applicable. The subjects are Markdown and a 20-line YAML file, with no callers or definitions.
- Both files changed during this review. Findings apply to the sha256 values above.
