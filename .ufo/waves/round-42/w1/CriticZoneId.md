# CriticZoneId — static review
Axes: operability (URL compatibility and truthful rule description); freshness is contextual, unscored.
Scope: read-only review; no code, CLI, selftest, counter, oracle, or performance runs; no round verdict.

## Checked statements
- **HOLDS — the round-42 declaration matches the regex.** SCORECARD.md:2915–2920 names exactly the bracket-content character class in scripts/sitemap_audit.py:80. The escaped hyphen is literal; no regex flags widen ASCII ranges. `_parse_url` checks it before `urlsplit` (:92–95).
- **HOLDS — literal non-ASCII and literal `|` inside brackets are rejected.** Neither is in that class; the reg-name alternative (:81) cannot consume the surrounding brackets. This describes characters as written, not decoded zone identifiers.
- **HOLDS — no RFC 3986 IP-literal needs a bracket-content character outside the set.** R3986:2722–2738 gives IPv6 (hex, colon, decimal dots) and IPvFuture (v, hex, dot, unreserved, sub-delims, colon); :2784–2788 expands the latter classes. All are included.
- **HOLDS — no RFC 6874 formal zone-id spelling needs a character outside the set.** R6874:198–202 gives `IPv6addrz = IPv6address "%25" ZoneID` and `ZoneID = 1*(unreserved / pct-encoded)`; R3986:2782 defines percent encoding using `%` and hex digits. Non-unreserved identifier characters MUST be percent-encoded (R6874:175–183).
- **HOLDS — RFC 3986 itself has no zone-id production.** Its complete IP-literal alternatives are IPv6address and IPvFuture (R3986:2722).
- **HOLDS, conditional — declaring the tightening now is an allowed disposition.** Closure:162–164 explicitly allows either re-establishing no-harm under a correctly frozen rule with cost bound and declared zone behaviour, or restoring parity. SCORECARD.md:2915–2920 records the first choice. Declaration alone is not the required no-harm evidence and cannot reverse round 41's rejection (Closure:100–117).
- **WRONG — the surviving source comment says IP-literal contents are judged only by `urlsplit`.** scripts/sitemap_audit.py:67–72,80 omit the earlier lexical restriction. Closure:152–154,165–166 already routes this correction. The round-42 declaration fixes the description in SCORECARD, not yet in the inspected source.

## Strongest local counterexample and bounds
- `http://[fe80::1%é]/a` and `http://[fe80::1%en|0]/a` refute unchanged round-40 zone acceptance / exclusive delegation: Closure:76–78 records base acceptance and final `check_invalid`. These are retained observations, not fresh executions by this seat.
- Neither is a counterexample to the current declaration or a valid RFC 6874 URI spelling. The ASCII gate also permits syntactically invalid material: e.g. `http://[v1.a%]/a` passes this regex but `%` is absent from RFC 3986 IPvFuture's repertoire. Thus character coverage is not full RFC validation; downstream acceptance was not run.
- Historical RFC 6874 would spell a zone containing `|` with `%7C`, which uses only admitted characters. This is a lexical-coverage statement, not a claim that `urlsplit` accepts every encoded zone form.
- Standards currency: R9844:192–198 completely obsoletes RFC 6874 and reverts its RFC 3986 URI-syntax extension. Treat the RFC 6874 analysis as historical syntax / compatibility evidence, not current URI authority.

## Smallest safe correction
Correct only the stale source comments to say: bracket contents first pass the declared ASCII gate, then `urlsplit`; raw non-ASCII and `|` are refused, and port range remains delegated. Keep the chosen compatibility disposition explicit; do not claim restored parity or completed no-harm merely from declaring it. The integrator must supply the newly frozen harm-rule evidence. Note RFC 9844 when opening the zone-syntax source row. No edit or admission by this seat.

## Evidence and execution provenance
R3986 = .ufo/waves/round-41/sources/rfc3986.txt ([RFC 3986](https://www.rfc-editor.org/rfc/rfc3986.txt)).
R6874 = /fast/scratch/hyaku/kake-r42w1/ScoutRFC6874/rfc6874.txt ([RFC 6874](https://www.rfc-editor.org/rfc/rfc6874.txt)).
R9844 = /fast/scratch/hyaku/kake-r42w1/ScoutRFC6874/rfc9844.txt ([RFC 9844](https://www.rfc-editor.org/rfc/rfc9844.txt)).
Closure = corpus/lessons/round-41-verifier-spotcheck.md.
Inspected tool: scripts/sitemap_audit.py; recorded sha256 `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d` (SCORECARD.md:2834–2835; not recomputed here).
Commands executed / exit codes: none; static read/grep/glob tools only. Tools built/scored: none; equalRuns, ratios, met: N/A. No installs, network requests, or processes started. Only this report written.
