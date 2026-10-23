# ConnectorSiblings — round 38 wave 1 (kake lane)

Axes: operability (primary), freshness (lane). Scope: read-only sibling scan for strict JSON (NaN/Infinity, long ints), URL-char validation, robots.txt.

Commands run (read-only; exit 0 unless noted):
- `find ... -path '*/.ufo' -prune -o ... -name '*.py' -print | xargs grep -l "parse_constant"` -> 0 (filtered)
- `grep -rn "robots" .../PROVINCE.md .../SKILL.md .../README.md` across sibling lanes -> tabi only
- `git -C kake-shokunin show 2dab...:scripts/robots_audit.py | sha256sum` -> `944d2f51...d3e5`

## Overlap table

| Lane | Surface / tool | Path (line) | Rule held | Relation to kake C2 (h)/(i)/(k) |
|---|---|---|---|---|
| tabi | client-side crawler discipline | `tabi-shokunin/SKILL.md:323-327`; `corpus/knowledge/external-class-fixture-v2.md:61,178` | first request `/robots.txt`; obey `Disallow:`; stop on 429/403/interstitial | Opposite side of the same file; no shared parser. Boundary: tabi fetches/obeys, kake audits publisher file. Do not import tabi logic. |
| kagi | feature-claims manifest gate | `kagi-shokunin/corpus/feature-claims.py:296-303` | `json.loads(parse_constant=_reject_constant, object_pairs_hook=_no_duplicate_keys)` | Reusable pattern for (h) NaN/Infinity; no long-int rule, no URL chars, no robots. |
| tameshi | registry-check gate | `tameshi-shokunin/tools/registry-check.py:331,356` | `parse_constant=_reject_json_constant` + location reporting | Reusable pattern for (h); parse_float NOT set, so `1e999` -> inf slips through (conflicting reading vs citing_set). |
| kama | evidence/identity tools | `kama-shokunin/tools/gguf-identity.py`, `kama-ollama-evidence.py` | parse_constant reject | Same as above; no URL/robots. |
| kotodama | claim-separability gate | `kotodama-shokunin/tools/check-claim-separability.py` | parse_constant reject | Same; no URL/robots. |
| mado | audit/tripwire tools | `mado-shokunin/tools/mado-*.py` | parse_constant reject | Same; no URL/robots. |
| mori | dispatch/evidence tools | `mori-shokunin/tools/mori-*.py` | parse_constant reject | Same; no URL/robots. |
| tsukuroi | recheck tool | `tsukuroi-shokunin/tools/measure-update-recheck.py` | parse_constant reject | Same; no URL/robots. |
| kake (own) | citing_set / receipt_replay | `kake-shokunin/scripts/citing_set.py:522-531`; `receipt_replay.py:123-124` | parse_constant + parse_float (finite) — best pattern | Adopt for robots_audit (h): reject NaN/Infinity AND non-finite `1e999`. base_path_audit/accessibility_packet use parse_constant only (gap). |
| kake (own) | base robots_audit | `kake-shokunin/scripts/robots_audit.py:397` (`json.loads(text)`) | plain stdlib json: accepts NaN/Infinity/1e999 | This is the (h) defect. |
| chousa | quote-reopen URL gate | `chousa-shokunin/tools/quote-reopen.py:195-214` | `urlsplit`; strips trailing `.,;)` from matched URL; refuses userinfo | Conflicting reading for (i): chousa mutates URL text before validation; kake (i) judges chars as written, including trailing. |
| kagi | release-clock | `kagi-shokunin/corpus/release-clock.py:50,176-244` | strips trailing `.` from host and `/` from path | Conflicting reading for (k): kagi normalizes trailing slash; kake (k) keeps normalized path exact `/robots.txt`. |

## Boundary statement

- robots.txt is split by side: tabi owns client-side crawler discipline (fetch, obey, stop rules); kake owns publisher-side offline audit. No shared parser; do not import across.
- Strict JSON (h) reusable pattern lives in-lane: `citing_set.py`/`receipt_replay.py` (parse_constant + parse_float). Sibling lanes use parse_constant-only (gap on 1e999) or plain json.loads (accepts NaN).
- URL-char validation (i) and implicit-allow (k) are kake-owned; no sibling holds a comparable rule; conflicting readings (chousa trailing-punct strip, kagi trailing-slash strip) must not be adopted.

## Not verified

- Did not run any sibling tools; no sibling robots/URL-char tests exist to execute. Long-integer handling (h) has no sibling equivalent (kake-only). No network used.