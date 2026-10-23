# Round 41 wave 2 — SentinelBuildInput

Scope: operability; read-only review of `scripts/sitemap_audit.py` input parsing and filesystem access. No source edits or tool installs.

## Verdicts on checked statements
- `_URI_RE` / `_parse_url` crash resistance: **HOLDS for exercised cases only**. Sampled lone surrogates in host/path, odd Unicode, 5,000-digit port, and 1,000,010-character malformed URI caused no exception; malformed URI returned `None`. A direct sweep of 4,099 cases had 0 exceptions. The pattern range at line 73 does admit lone surrogates as URI data; this test did not assess broader grammar correctness.
- Very long values: **HOLDS at tested size, but resource use is unbounded**. A 2,097,173-codepoint sitemap URL and matching `<loc>` completed, reporting `loc_too_long`; no regex blowup observed. Manifest reading has no byte cap (328-345), so arbitrary-size inputs remain a resource-exhaustion risk.
- Manifest-directory read confinement: **WRONG** for symlink targets. Absolute paths and `..` segments are blocked lexically (357-360), but the later `open()` follows symlinks.
- Per-check unreadable-file handling: **WRONG** for an unpaired-surrogate pathname; it aborts evaluation into top-level `input_invalid`, rather than returning a `file_unreadable` check (contract sentence 5).
- Out-of-directory writes: **HOLDS for inspected filesystem operations**. The only file opens are read-only at 210 and 328; output is stdout at 408. No input-derived file write was found.

## Findings
1. **MEDIUM — symlink escapes manifest directory** (`scripts/sitemap_audit.py:357-360, 386`). Exploit: place `link.xml` in the manifest directory as a symlink to a readable file outside it, then name `link.xml` in `file`. The lexical guard accepts it and `open(os.path.join(...))` follows it. Reproduced with a controlled outside XML: the CLI returned its `root_invalid` finding (exit 1), proving it read the target. Impact: a manifest can make the audit read arbitrary files available to the invoking user; emitted content is limited to audit findings. Smallest fix: resolve and enforce containment beneath the manifest directory before opening; use descriptor-based no-follow traversal if that directory can change concurrently.
2. **LOW — surrogate filename escapes per-check error handling** (`scripts/sitemap_audit.py:210-213, 386, 443-446`). Exploit: a JSON `file` value containing `\ud800.xml` passes the type and path checks; opening it raises `UnicodeEncodeError`, which is not caught by `_audit_file`'s `except OSError`. Reproduced direct exception class `UnicodeEncodeError`; full CLI returned `input_invalid` with `checks: []` (exit 2), discarding an earlier missing-file result. Impact: one malformed pathname suppresses all per-check results. Smallest fix: treat `UnicodeError` (and other invalid-path exceptions) as `file_unreadable` at the file-open boundary.
3. **LOW — unbounded manifest / URL resource use** (`scripts/sitemap_audit.py:328-345, 382`). Exploit: provide an arbitrarily large manifest or `sitemapUrl`; the complete manifest is read and decoded, then the URL is matched without a length bound. This is a source-grounded resource risk, not a reproduced OOM; regex timing was linear on the 1 MB malformed probe and the 2 MB end-to-end URL completed. Impact: sufficiently large input can consume process memory/CPU and make the local audit unavailable. Smallest fix: impose a documented manifest byte limit using a bounded read, and reject oversized URL fields before matching.

## Exact bounded commands and outcomes
- URI edge probe: `timeout 20s prlimit --as=4000000000 --cpu=10 -- python3 -B -c 'import sys,time; sys.path.insert(0,"/home/vgpnk/Projects/shokunin/kake-shokunin/scripts"); import sitemap_audit as s; failures=[]; count=0
for cp in range(0xd800,0xe000):
 c=chr(cp)
 for u in ("http://example.test/"+c,"http://"+c+".example.test/"):
  try: s._parse_url(u); count+=1
  except Exception as e: failures.append((cp,type(e).__name__))
for u in ("http://["+chr(0xd800)+"]/","http://h:"+"9"*5000+"/","http://exa"+chr(0x212a)+"mple.test/"):
 try: s._parse_url(u); count+=1
 except Exception as e: failures.append((repr(u[:24]),type(e).__name__))
u="http://h/"+"/a"*500000+"%"; t=time.monotonic(); result=s._parse_url(u); elapsed=time.monotonic()-t; print("uri_cases",count,"exceptions",len(failures),"long_chars",len(u),"long_result",repr(result),"long_seconds",round(elapsed,3)); print("failures",repr(failures[:5])); sys.exit(bool(failures))'; printf 'probe_exit=%s\n' "$?"` → `probe_exit=0`; 4,099 URI cases, 0 exceptions, 1,000,010 chars, 0.117 s.
- `timeout 20s prlimit --as=4000000000 --cpu=10 -- python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/sitemap_audit.py --manifest /fast/scratch/hyaku/kake-r41w2/SentinelBuildInput/symlink-check/manifest-dir/manifest.json; printf 'audit_exit=%s\n' "$?"` → `root_invalid`, `audit_exit=1` (target was outside the manifest directory).
- `timeout 20s prlimit --as=4000000000 --cpu=10 -- python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/sitemap_audit.py --manifest /fast/scratch/hyaku/kake-r41w2/SentinelBuildInput/surrogate-check/manifest.json; printf 'audit_exit=%s\n' "$?"` → `input_invalid`, empty checks, `audit_exit=2`.
- `timeout 20s prlimit --as=4000000000 --cpu=10 -- python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/sitemap_audit.py --manifest /fast/scratch/hyaku/kake-r41w2/SentinelBuildInput/long-check/manifest.json; printf 'audit_exit=%s\n' "$?"` → `loc_too_long`, `audit_exit=1` (2,097,173-codepoint URL and `<loc>`).
