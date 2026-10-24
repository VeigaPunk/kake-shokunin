# ReopenGateS034 — r38 w2 falsify: RFC 8259 Gate line and S034 SOURCES row

Tip `adab4c7e9`, base `af43a50f`. Leaf seat, no subagents, no counter/selftest run, no lane mutation
(read-only `git show/diff`; clone at tip). No tools installed (nothing needed; curl 8.x, python 3).

Attacked: `corpus/lessons/round-38.md:27-29` access facts, the "identical to the 2026-10-21 opening"
claim, the verbatim quote, and `corpus/SOURCES.md:42` scope/anchor/teaches/used-by cells.

## Commands and exits

- `curl -sS -o rfc8259.txt -w 'HTTP=%{http_code} SIZE=%{size_download}'` → `HTTP=200 SIZE=28360`, exit 0; `sha256sum` → `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`.
- Second GET `b2.txt` → 200, 28360, `cmp -s` exit 0 (`BYTE_IDENTICAL=yes`), same digest; headers `etag: W/"effcde61d580b8bb9e8eb8fdca283c5f"` (same as `w1/ScoutReopenS034.md:12`), no redirect.
- `curl https://www.rfc-editor.org/rfc/rfc8259.json` → 200; `pub_date "December 2017"`, `obsoletes ["RFC7159"]`, `obsoleted_by []`, `status INTERNET STANDARD`.
- `grep -n "Numeric values that cannot be represented" rfc8259.txt` → `377` (sentence ends `378`), under heading `6.  Numbers` at `:362`.
- `grep -n "SHOULD be unique"` → `:322` (§4); `grep -n "MUST accept all texts"` → `:544` (§9); `unpredictable` → `:333` (§4).
- `curl -sSL https://www.rfc-editor.org/errata/rfc8259` → 200, 93426 bytes, sha256 `5819db2e…b7cf4`, byte-identical to the wave-1 saved copy; parsed 17 records, 5 Verified.
- `git diff af43a50f adab4c7e -- corpus/SOURCES.md` → exactly one S034 hunk: used-by appends `, corpus/knowledge/robots-txt-rules.md`; no other S034 cell moved.

## Verdicts per attacked statement

| Statement | Verdict | Evidence |
|---|---|---|
| HTTP 200, 28360 bytes, full sha256 | **holds** | two independent GETs today, identical bytes; 28360 = round-24 `w1/SourceRFC8259Json.md:47` |
| printed digest `61a5378f…2cd2d7` | **wrong** | real tails: 8 = `9b4cd2d7`, 6 = `4cd2d7`. `sha256sum rfc8259.txt \| rev \| cut -c1-6 \| rev` → `4cd2d7`; `2cd2d7` is not a suffix of the digest |
| "identical to the 2026-10-21 opening" | **holds** | full digest at `corpus/lessons/round-24.md:33`; `.ufo/waves/round-26/rechecks/S034.json` (HOLD, same digest); wave-1 sandbox `rfc8259.txt` reproduces it |
| quote verbatim, §6 | **holds** | `rfc8259.txt:377-378`, 18 words; whitespace-normalized equals the Gate line and `w1/ScoutReopenS034.md:22` |
| row anchor "Sections 3, 4, 6 and 9, December 2017" | **holds** | headings `:296`, `:316`, `:362`, `:541`; header `:7` |
| teaches "Object names SHOULD be unique" | **holds** | `:322` |
| teaches "NaN and Infinity are not JSON numbers" | **holds** | `:377-378`; RFC names no `-Infinity`, but minus must precede `int` digits (`:380`, `:399`, `:401`) |
| teaches "duplicate rejection is local policy" | **holds** | §9`:544` MUST-accept-conforming + §4`:333` unpredictable behavior; rejection is stricter than the RFC |
| used-by widening adds `robots-txt-rules.md` | **holds mechanically, gap in support** | `robots-txt-rules.md:96` cites S034 §§6,9 for "an implementation limit the range and precision of numbers" (`:407-408`, `:549`). The row's *scope* ("duplicate members, non-finite constants and boolean versus number types") and *teaches* record no limit statement; only the *anchor* names §9. A reader of the row cannot see the proposition the new consumer leans on |
| wave-1 "Errata: … none touches §6 or §9" (`ScoutReopenS034.md:16`) | **wrong as inventory** | page carries `7600` **Verified Technical §6**, `7603` Verified §1, `5318` Verified §7, plus `7617`/`8874` rejected §6. `7600` rewrites only the leading-zeros clause; the quoted sentence is untouched, so "keep" survives — the screen is incomplete, not the verdict |

## Harm / reach

No operative consumer parses lesson digests (`grep -n SOURCES scripts/source_recheck.py` → only
prose matches), so the bad tail is a reproduction defect for any reader/agent re-deriving the
evidence, not a runtime break. The Gate line's "keep, tier A, spec, mined" verdict is otherwise
supported by my own fetch; freshness is real (byte-identical across 2026-10-21 → 2026-10-23,
no successor RFC, no `obsoleted_by`).

Nit, inherited from `af43a50f` (not introduced this round): the row title drops the RFC's "(JSON)";
RFC title line reads "The JavaScript Object Notation (JSON) Data Interchange Format".

## Not verified

Wall-clock of the wave-1 GET (2026-10-23T04:30:20Z) — only the bytes and headers are reproducible
today; the timestamps match between Gate line and wave-1 report. Errata not re-verified past the
public errata page.

## Deliverables (absolute, sandbox)

- `/fast/scratch/hyaku/kake-r38w2/ReopenGateS034/rfc8259.txt` — 28360 B, sha256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`
- `/fast/scratch/hyaku/kake-r38w2/ReopenGateS034/b2.txt` — same sha256
- `/fast/scratch/hyaku/kake-r38w2/ReopenGateS034/errata.html` — sha256 `5819db2e0233addf17ed540db88cf92cbefda5a60c38877e0d4cbf6b876b7cf4`
- `/fast/scratch/hyaku/kake-r38w2/ReopenGateS034/eid7600.html` — sha256 `406547d978747e30a867b7f89f6fb1f1a23024676d667adfb725fcf593ae6fb9`
- `/fast/scratch/hyaku/kake-r38w2/ReopenGateS034/meta.json` — sha256 `5de136e66c519d883f0fc66947ba25e88a6b11c54770429bf287b0ac5782c724`
- `/fast/scratch/hyaku/kake-r38w2/ReopenGateS034/clone` — read-only checkout of `adab4c7e9`
