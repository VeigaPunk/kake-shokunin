# ExecCensusLane — full-repo kake census validate

**Seat:** executor. Leaf. No labrat. No other file written.
**Axes:** operability, freshness.
**Milestone:** Round 49 v1 wave: attack the frozen order proof and crawl-budget quote truth.
**Lane:** `/home/vgpnk/Projects/shokunin/kake-shokunin`.
**When:** 2026-10-25T00:37:12Z.
**HEAD at run:** `1c846ed2d67b1692ea966be064f0fc04542763c6`. `git status --porcelain -- corpus/SOURCES.md` empty; `git diff --exit-code -- corpus/SOURCES.md` exit 0. The command reads the worktree registry, which matches that revision.

## Command

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
```

Working directory: `/home/vgpnk/Projects/shokunin`.

This is a lane validation (`validate` + lane id `kake` + `--root`), not `validate --file`.

## Exit code

`0`

Header of `scripts/sources-census.sh` (lines 16–18): exit 0 is clean or warnings; W-codes never change status. W04 is "same URL across scopes (warnings do not affect clean lanes)" (line 33).

## Ok line

```
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
```

That line is the last line of the script's stdout. The lane token is `kake`, not `file`.

## Stdout (full)

```
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
kake	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
kake	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
kake	W04	S110 duplicate url www.w3.org/TR/xml across scopes
kake	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
```

Twelve W04 lines, then the ok line. No E-code. Stderr empty.

## Axis read

- **Operability:** the maintained census script runs against the live lane registry and exits 0. W04 does not fail the gate.
- **Freshness:** the ok line names the live `corpus/SOURCES.md`, not the pre-append `--file` mirror. The pre-append receipt (`assimilation/pre-append/census-argv.txt`) is `validate --file .../assimilation/pre-append/corpus/SOURCES.md` and its ok token is `file`. This run is the full-repo lane validation.

No production edit. No `jj`. No fleet write. No commit.

Report: .ufo/waves/round-49/w1/ExecCensusLane.md
