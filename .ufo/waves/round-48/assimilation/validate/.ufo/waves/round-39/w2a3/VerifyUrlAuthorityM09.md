# VerifyUrlAuthorityM09 — MutUrlAuthority M09 review

**Verdict: valid control** (mutant breaks contract sentence 4, which the reference obeys).

## Evidence

sha256 (all match mutants.json; M09 hash matches receipt `toolSha256`):
- `mutants/M09.py` `95fae2ad406c3df6bf9c4688d19c2803426d64657495dce977ad2c496f8c6497`
- `shared/reference.py` `663e051e10b9fca2db55fa13497b965fb19fb107b3791123769fc8534a2d69f8`
- `witnesses/M09/manifest.json` `e7daa4c0ca64bef1874c9e80dc7921cd133bb212f7b2ae987497508eb75652e3`
- `witnesses/M09/sitemap.xml` `066bcaa09c62edf2fbc48b44b61a90b30e506a1a3b3c3305656be56d8181f4d8`

`diff -u reference.py mutants/M09.py` → exit 1, exactly one line changed (reference.py:215):
```
-        if os.path.isabs(fp) or ".." in re.split(r"[/\\]", fp) or absurl(c["sitemapUrl"]) is None:
+        if os.path.isabs(fp) or ".." in re.split(r"[/\\]", fp) or absurl(c["sitemapUrl"]) is None or urlsplit(c["sitemapUrl"]).fragment:
```
Adds `check_invalid` for any `sitemapUrl` with a non-empty fragment — matches the mutants.json mutation record verbatim.

`prlimit --as=4000000000 timeout 60 python3 -B shared/reference.py --manifest witnesses/M09/manifest.json` → exit 0:
```
{"version": 1, "verdict": "clean", "checks": [{"id": "w", "status": "clean", "error": null, "findings": []}]}
```
`prlimit --as=4000000000 timeout 60 python3 -B mutants/M09.py --manifest witnesses/M09/manifest.json` → exit 2:
```
{"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": "w", "status": "error", "error": "check_invalid", "findings": []}]}
```
Both reproduce the recorded reference_output/mutant_output in mutants.json exactly.

## Contract analysis

Sentence 4 (c1-contract.md:22–25): "Each check is an object with string members `id`, `file`, `sitemapUrl`. A check that … has a `sitemapUrl` that is not an absolute `http`/`https` URL with a host, is an error check with error `check_invalid`."

Witness `sitemapUrl` = `https://example.test/maps/s.xml#part`: scheme `https`, host `example.test` — satisfies every disqualifier sentence 4 lists. The only question is whether the `#part` fragment strips "absolute". Contract alone decides no:

- The contract cites no URI grammar; its sources (S102 sitemaps.org, S103/S104 XSDs) never mention fragments, and the XSD `anyURI` type admits fragments.
- The contract says "URL", not RFC 3986 "absolute-URI" (the only grammar excluding fragments). Under the WHATWG URL standard an absolute-URL string may carry a fragment; "absolute" here reads as "has a scheme / not relative", which the witness satisfies.
- Sentence 22 uses identical "absolute URL" wording for `loc`; the mutant does not touch the loc path — its own author treats fragments as tolerated there, so the added clause is a new condition, not a clarified reading.
- Reference `absurl()` (reference.py:23–31) implements exactly the contract's tests (scheme http/https, non-empty host, valid port) and ignores fragments — consistent both ways.
- Scope rules (25–26) then use directory `/maps/`; loc `https://example.test/maps/a` is in scope → clean under any reading.

The contract determines the witness: `clean`, exit 0 — the reference's output. The mutant emits `check_invalid` for an input sentence 4 does not mark invalid → breaks sentence 4.

## Receipt note

`verification/a3/w1a3-MutUrlAuthority__M09.json`: `met`=true, `passed` 24/24, `toolSha256` matches M09.py. A genuine contract violator survives the sealed key → the 24-case key contains no fragment-carrying `sitemapUrl` case (key coverage gap, not equivalence). Kill-rule evidence is the real contract divergence, invisible to the counter.
