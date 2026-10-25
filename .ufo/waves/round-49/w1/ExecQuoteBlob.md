# ExecQuoteBlob — S273 quote vs committed blob

Seat: ExecQuoteBlob (leaf executor). Axes: operability, freshness.
Milestone: Round 49 v1 wave: attack the frozen order proof and crawl-budget quote truth.
Measured: 2026-10-25T00:37:35Z.
Revision: `1c846ed2` = `1c846ed2d67b1692ea966be064f0fc04542763c6` (ancestor of HEAD; `git merge-base --is-ancestor` exit 0). Subject: `round-49: append crawl-budget rows after the pre-append mirror` (2026-10-24 21:34:41 -0300).

## Verdict

The S273 gate quote is an exact substring of `git show 1c846ed2:.ufo/waves/round-49/sources/S273.txt`. Content sha256 of that blob is `ab4a685d7432b69e659f6d3717aeeffc66b9277e69ad54de601f72cc30d4347b`. The worktree file was not opened for this score.

## Commands

```
$ git rev-parse --verify 1c846ed2^{commit}
1c846ed2d67b1692ea966be064f0fc04542763c6
$ git cat-file -s 1c846ed2:.ufo/waves/round-49/sources/S273.txt
11123
$ git show --no-textconv 1c846ed2:.ufo/waves/round-49/sources/S273.txt >/dev/null
git_show_exit=0
$ git show 1c846ed2:.ufo/waves/round-49/sources/S273.txt | sha256sum
ab4a685d7432b69e659f6d3717aeeffc66b9277e69ad54de601f72cc30d4347b  -
pipe_exit=0
```

Quote taken only from `git show 1c846ed2:corpus/lessons/round-49.md` (exit 0), the `## Gate` span `quote:"..."` on the S273 line. 21 whitespace tokens, 134 characters:

> Google won't shift this newly available crawl budget to other pages unless Google is already hitting your site's crawl capacity limit.

Substring check on that same `git show` stdout (UTF-8 bytes; `quote.encode("utf-8") in blob`; `hashlib.sha256(blob).hexdigest()`):

- exact substring: true
- match index: 7423
- window: `you don't want Google to crawl at all. Google won't shift this newly available crawl budget to other pages unless Google is already hitting your site's crawl capacity limit. Return a 404 or 410 status code for per`

Receipt pin, from `git show 1c846ed2:.ufo/waves/round-49/sources/receipts.json` only: `textPath` `S273.txt`, `textSha256` `ab4a685d7432b69e659f6d3717aeeffc66b9277e69ad54de601f72cc30d4347b`. Equal to the blob sha256: true.

Git object id of the path (not the content sha256): `1c0a0794eea44b9aca390aafd9feb27163d12161`.

`git status --porcelain -- .ufo/waves/round-49/sources/S273.txt` printed no line (exit 0). That status was not the score.

## Bound

Only file written: `.ufo/waves/round-49/w1/ExecQuoteBlob.md`. No jj, no commit, no fleet write. Worktree `.ufo/waves/round-49/sources/S273.txt` was not opened.
