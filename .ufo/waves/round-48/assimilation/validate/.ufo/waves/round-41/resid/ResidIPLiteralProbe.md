# Residual seat ResidIPLiteralProbe — exhaustive IP-literal slot probe (round 41, final build)

Sandbox `/fast/scratch/hyaku/kake-r41resid/ResidIPLiteralProbe/` (probe.py, results.json, cli_base/first/final.json). Lane repo untouched except this report.

## Bytes reviewed (sha256, extracted with `git show <rev>:scripts/sitemap_audit.py`, exit 0)
- base `8eb121c8` = `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e` (declared round-40 tool)
- first build `eae5ae2c` = `0b485431d96268d46c8dc9052eec92520248a03989896bd83f4521f15f13edbf` (declared)
- final `b9bf1a39` = `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d` (declared final)
- oracle wheel `.ufo/waves/round-41/oracle/abnf-2.9.1-py3-none-any.whl` = `cdcac127b3693ded2b00565878d8ed2b96d34b29f0ee199c06d7b40baaf60917` = PyPI pin in SCORECARD

## Method (770 cases per entry point; Python 3.14.8 judges all four)
Bracketed host `[2001:db8::1]` and `[v1.abc]`; every ASCII 0x00–0x7F inserted at start/mid/end of the host (+2 unmodified sanity) in `http://[…]/a`. Judged through the production entries, not a reimplementation: `loc` → module `_audit_loc` (sentence-21 strip in `_text_of`), accepted iff no `loc_not_absolute`; `sitemapUrl` → module `_evaluate_check` against a real manifest+file fixture, accepted iff not `check_invalid`; plus `abnf.grammars.rfc3986.Rule("URI").parse_all` as oracle. Commands: `python3 -m venv oven && oven/bin/pip install --no-index --no-deps <wheel>` (exit 0); `prlimit --as=4000000000 -- timeout 300 oven/bin/python probe.py` (exit 0); CLI confirmation `prlimit --as=4000000000 -- timeout 60 oven/bin/python -B {base,first,final}.py --manifest fixdir/m.json` → base exit 2, first exit 1, final exit 2 (verdicts below). Tooling: no pacman, no external installs (stdlib venv + local wheel only).

## Results (full table `results.json`; loc ≡ sitemapUrl on all 770 cases for every version)
1. **Final accepts & base rejects: 0 of 770 in both `loc` and `sitemapUrl`.** The requested list is empty — the final build never widens acceptance over the round-40 base on this class.
2. **First accepts & base rejects: 18 of 770 per entry** — exactly TAB, LF, CR × start/mid/end × both hosts (`urlsplit` deletes them from the netloc): precisely the wave-2 regression, no additional character.
3. **Final vs oracle:** final accepts where the oracle rejects only `%` at mid/end of `[v1.abc]` (2/770 per entry: `http://[v1.%abc]/a`, `http://[v1.abc%]/a`) — the documented exclusion (SKILL.md "round-41 URL rule": IP-literal contents "still judged by urlsplit"; zone ids keep round-40 acceptance). Final rejects where the oracle accepts: **0/770** — no false rejection anywhere in the class. Totals: base 287, first 305, final 204, oracle 202 accepted.
4. **Final vs first:** final accepts where first rejects: 0/770; the revision is pure tightening.
5. CLI confirmation (manifest with four checks): base and final both reject TAB-in-literal (`c2` sitemapUrl → `check_invalid`; `c4` loc via `&#9;` → `loc_not_absolute`), first build accepts both (findings/clean) — regression and fix confirmed end-to-end.

## Findings
- No HIGH/MEDIUM finding against the final build in scope.
- INFO (documented, not a defect): `%` accepted inside `[v1.abc]` (result 3); SKILL/SCORECARD record it.
- INFO (historic): base accepted NUL/DEL/space inside the literal (`urlsplit` tolerates them); final rejects; oracle rejects too — tightening only, no claim affected.

## Statement verdicts
- "IP-literal branch admits only `[A-Za-z0-9._~:!$&'()*+,;=%-]`" (SCORECARD wave-2 section; final.py:80) — **holds** as behaviour on all 770×2 cases.
- "TAB/LF/CR inside an IP literal accepted by `0b485431…`, rejected by the revision" — **holds** (18/18 first-accept cases final-rejected; CLI confirmed).
- "`loc` (after strip) and `sitemapUrl` judged identically by `_parse_url`" — **holds** here; note `loc` C0 cases other than TAB/LF/CR are XML-unreachable in production (recorded as data only, rejected by every judge anyway).
- Round-41 URL-rule text — nothing found **wrong** or **overstated** within this probe's class.

## Residual risk / gaps
One IPv6 shape and one IPvFuture shape; 3 of len+1 insertion positions; ASCII only; ports and U+0080+ out of assignment scope (also outside the round-41 counter class). Empty-set claim (result 1) is bounded by exactly that class.
