# ScoutGithubPin — S062 row URL cell resolves publicly

Lane: kake-shokunin. Seat: wave 1, freshness / operability scout (C2 supporting check).
Sandbox: /fast/scratch/hyaku/kake-r32/w1/ScoutGithubPin/ (page.html, raw.yaml, commit.json,
compare.json, results.txt). No lane file touched except this report. No tool installs.
No owned property (ds4cc.com, *.onrender.com, kimi.*, veigapunk.github.io) contacted; only
github.com, raw.githubusercontent.com, api.github.com, and read-only git in the local clone.

## Question
Does the GitHub URL in the S062 row resolve publicly?

Row text (corpus/SOURCES.md:70, raw):
`S062 | ds4cc-marketplace render.yaml and apps-sdk/Dockerfile at commit 1fbdb8ed —
https://github.com/VeigaPunk/ds4cc-marketplace/blob/1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28/render.yaml; local clone ~/Projects/ds4cc-marketplace; retained byte-identical at .ufo/waves/round-32/sources/ds4cc-1fbdb8ed/`

## Answer: yes, it resolves publicly, anonymously, with no redirect
Observed, all exit 0:
- `curl -sI -o /dev/null -w '%{http_code}' <URL>` → 200, redirect_url empty (no login/redirect bounce).
- `curl -sL -o /dev/null -w '%{http_code} %{num_redirects} %{size_download}' <URL>` → 200, redirects 0, 224149 bytes.
- Anonymous recheck with cookies stripped (`-H 'Cookie:'`) → 200.
- Control: same path with bogus SHA `deadbeef…` → 404. So the 200 is a real hit, not a catch-all.
- Served page is the file page, not a soft-404: `<title>ds4cc-marketplace/render.yaml at
  1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28 · VeigaPunk/ds4cc-marketplace · GitHub</title>`;
  grep for "does not exist" / "page not found" → 0 matches.
- Content endpoint: `https://raw.githubusercontent.com/VeigaPunk/ds4cc-marketplace/1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28/render.yaml`
  → 200, 565 bytes.
- Public commit object: `https://api.github.com/repos/VeigaPunk/ds4cc-marketplace/commits/1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`
  → 200, `sha` echoes 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28, commit date 2026-10-21.
- Second cited file also public: `…/blob/1fbdb8ed…/apps-sdk/Dockerfile` → 200, redirects 0.

## Is the commit on a pushed branch? Yes
- `git -C ~/Projects/ds4cc-marketplace branch -a --contains 1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`
  → `* main`, `remotes/origin/HEAD -> origin/main`, `remotes/origin/main`; exit 0.
- `git -C ~/Projects/ds4cc-marketplace ls-remote origin refs/heads/main` → 7fc6aa2fc12451dd451fed5a9ee7125f3a90e884.
- `https://api.github.com/repos/VeigaPunk/ds4cc-marketplace/compare/1fbdb8ed…...7fc6aa2…`
  → 200, `status=ahead`, `ahead_by=1`, `behind_by=0`. So 1fbdb8ed is an ancestor of live main.

## Freshness side note (not a defect in S062)
- The local clone is one commit behind live main: `git rev-parse origin/main main` both print
  1fbdb8ed…; the remote tip is 7fc6aa2 (stale local refs, shallow=false).
- The single newer commit (7fc6aa2, "magga: Frostbite …") touches only `magga/**` and
  `sitemap.xml`; it does not modify `render.yaml` or `apps-sdk/Dockerfile`. So the pinned blobs
  are still the current main versions of those paths at check time. The row pins a commit and
  claims nothing about later commits ("not a statement about … any later commit"), so no wording
  change is required.

## Byte identity cross-check of the retained copies (supports C2)
- Retained `render.yaml` and freshly fetched raw bytes: sha256 identical
  `83e0ead9c360d1c315f0ad8774550e7da1fbe6be8ddc5ab52ef0edddb437920b` (both 565 bytes).
- `git hash-object` on the two retained files prints
  `d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252` and `ee0b63819a9ce71e51469796541b9075e9676ae9`,
  exactly the blob ids in the S062 row; both match `git rev-parse 1fbdb8ed:<path>` in the clone.
- `wc -l` on retained `render.yaml` = 20, matching the row's "(20 lines)".

## Verdict for the row
The URL cell is accurate as written; nothing should be changed. Confidence: high for the URL,
branch reachability, and blob-id equality (all from public endpoints plus read-only git).
[INFERENCE] GitHub resolves `/blob/<sha>/…` and `/commits/<sha>` only for objects reachable from
a public ref, so the 200s corroborate the local `--contains` result; the bogus-SHA 404 control
makes that inference concrete for this repo.

## Not verified
- `apps-sdk/src/server.ts` (blob `649726df…`) was not fetched or hashed — outside this seat.
- No live Render service or dashboard state was checked, by design (owned property; out of scope).
- The report does not re-check whether the retained copies' content is quoted correctly in
  corpus/knowledge/render-web-services.md:80-90; only that the entry section cites S062 and the
  blob ids it names equal the retained bytes.
