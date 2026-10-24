# ResidFinalBuildReview — fresh review of the final tool bytes (round 41 residual, leaf seat)

Bytes reviewed: `scripts/sitemap_audit.py` @ tip `b9bf1a39…`, blob sha256 `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d` (= worktree; expected value confirmed). Also reviewed: base `4de35f8c…1460e` (@ `8eb121c8`), first build `0b485431…` (@ `eae5ae2c`), selftest `18752057c8b0f7cb1b8567e8fff01be79faae0235b78201f344e7ec5c6e01bf8`, oracle wheel `cdcac127…0917`. No tools installed (none needed); `jq` here is jaq 3.1.1. No `lsp` device is mounted (xd://lsp absent), so definition/def-use checks were done by direct read of this single-file tool, located via grep, not presented as LSP proof.

## What I ran (all offline, sandbox copies; exit 0 unless noted)

1. `git -C <lane> diff 8eb121c8 b9bf1a39… -- scripts/sitemap_audit.py`: one hunk, 24+/2− — comment, `_UNRESERVED/_SUB_DELIMS/_PCT/_PCHAR`, `_URI_RE` added; `_parse_url`'s old guard (`value[:1] <= " " or TAB/CR/LF`) replaced by `if _URI_RE.match(value) is None: return None`.
2. `git -C <lane> diff eae5ae2c b9bf1a39… -- scripts/sitemap_audit.py`: one changed line — IP-literal branch `[^\]]*` → `[A-Za-z0-9._~:!$&'()*+,;=%\-]*`.
3. Class-by-class vs RFC 3986 App. A (script lines 77-88): scheme `[A-Za-z][A-Za-z0-9+.\-]*` = exact; userinfo `(unreserved|SD|":")*@` exact; reg-name branch `(unreserved|SD|%HH)+` exact per character (`+` = required non-empty host, contract, base-equivalent); port `(?::[0-9]*)?` = `*DIGIT` exact incl. empty; path-abempty/pchar, query, fragment `pchar|"/"|"?"` exact; pct `%[0-9A-Fa-f]{2}` exact; `\A…\Z` anchors (no `$` newline hole); second `#`, `@` in userinfo, `[`/`]` outside brackets, space, C0, DEL, `"<>\^`{|}` all excluded. IP-literal class ⊇ IPv6address ∪ IPvFuture charsets (HEXDIG, `v`, `.`, unreserved, sub-delims, `:`) plus `%` — a per-character superset with structure and port range delegated to urlsplit; TAB/LF/CR and all other non-class chars excluded, which closes the wave-2 regression at the regex level.
4. Callers of `_parse_url`: exactly two — `_audit_loc` (line 308; value = `_text_of` = sentence-21 ` \t\r\n` strip, other-namespace text ignored) and `_evaluate_check` (line 382; manifest `sitemapUrl` as written); both map None → `loc_not_absolute`/`check_invalid`; scope rule downstream unchanged.
5. Differential, 60,100 cases (93 handcrafted boundary + seeded fuzz, seed 41001; oracle abnf 2.9.1 `Rule("URI").parse_all` from the vendored wheel; sandbox copies of base/first/final loaded as modules): (a) RFC-valid ∧ base-accepted values where final ≠ base: **0**; (b) final accepts where base rejects: **0**; (c) final accepts where oracle says non-RFC: only documented classes — non-ASCII as unreserved 1,180, `%`/zone-id in brackets 83, nothing else; (d) first accepts ∧ final rejects: 106, all TAB/LF/CR-in-IP-literal shapes.
6. `prlimit --as=4000000000 timeout 600 python3 -B sitemap_audit_selftest.py --tool ./sitemap_audit_final.py --fault-injection` → `PASS 225/225`, silent and constant-clean fault tools both rejected, exit 0.
7. Real run on `.ufo/waves/round-41/realrun/manifest.json` (sandbox copy), `| jq -S . | sha256sum` → `fd985a41867ed31b02ab03797562a1f01969aa3fc01c293eda145c2a7a4bc8a5`, exit 0 — byte-equal to the recorded round-39/40 real-run hash.

## Findings

None actionable. No defect found in the final bytes: no ASCII class omission vs RFC 3986 App. A, the IP-literal fix is present and sufficient, and both callers preserve round-40 behavior on the RFC ∩ base-accepted intersection.

## Statement check (holds / overstated / wrong)

- Final gate judges as written against RFC 3986 URI with authority + non-empty host — **holds** on ASCII, modulo the three supersets the code comment and SKILL.md both document (U+0080+ as unreserved; `%` inside brackets/zone ids; IP-literal shape and port range left to urlsplit). Not overstated.
- Wave-2 regression (TAB/LF/CR in IP literal) fixed in `50287ac6…` and present in `0b485431…` — **holds** (trio base/first/final = reject/accept/reject for all three chars; 106 fuzz cases).
- Caller behavior preserved on values both RFC 3986 and base accept — **holds** (0/60,100 violations; acceptance set is a strict subset of base's; real run byte-equal).
- SKILL's enumerated rejection families (space, `"<>\^`{|}`, DEL, C0, `[`/`]` in path/query/fragment, second `#`, `@` in userinfo, broken `%`) — **holds**, each observed flipping from base-accept to reject, none outside the claimed class.
- Selftest 225 fixtures pass at the build — **holds** (PASS 225/225, fault injection rejects both probes, exit 0).

## Residual risk / gaps

- Oracle direction: invariant (a) is proven only over values abnf accepts; an abnf false-reject could mask a hit. Mitigated by the per-character analytic proof (no ASCII omission possible) and the round's own rfc3987 second-oracle cross-check (14,340/14,340). Not re-run here.
- I did not rerun counter v1/v2 (frozen, information-only; owned by other seats) and did not re-verify the base/first selftest red-green matrices (SCORECARD `verification/build3/` records them; I verified the final side only).
- Manifest JSON lone-surrogate escapes were not tested; analysis says non-delta (gate acceptance is a subset of base's, so behavior cannot change in the accept direction).
