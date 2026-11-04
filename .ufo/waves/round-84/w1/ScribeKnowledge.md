# ScribeKnowledge — round 84 wave w1

Deliverable: `corpus/knowledge/policy-value-classes.md` (87 lines, 14,271 B at write time, sha256
`14fdba53da827e7896de25699ef3643ef2cc450f4f17f1d23433a1d82d926ab1` after the final correction below).
Receipts: `.ufo/waves/round-84/w1/ScribeKnowledge/`. No other production file was written; `corpus/SOURCES.md`
and `corpus/README.md` are ScribeRegistry's and I did not touch them (the `M` on both in `git status` is that seat's).

## What I did

1. Read `.ufo/waves/round-84/contract.md` §C1/§C2, the frozen counter `.ufo/waves/round-84/c84_policy_values.py`
   in full, `.ufo/waves/round-84/policy-expectations.json`, the item at `.ufo/waves/round-84/w1-spec.json#items[0]`
   (ScoutSources), the ScribeRegistry item, and the C2 tool-owner item. Read `scripts/header_change_class.py`
   through `load_surface`/`classify`, and `scripts/policy_value_class.py` in full once it landed at 11:06.
2. Read the retained bytes `.ufo/waves/round-84/w1/ScoutSources/rfc9111.txt` (84,477 B, sha256
   `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`) and confirmed it is byte-identical to the
   round-83 copy the item names (`sha256sum` on both: same digest). Read `.ufo/waves/round-84/w1/ScoutSources/rfc9111-httpwg.html`
   (178,573 B, sha256 `999f4013…f64`) and located its anchors by byte offset.
3. L0 correction from KakeR84 (arrived mid-run) applied: `S457` is the httpwg HTML rendering opened this round and gets
   HTML line anchors only; `S456` is the rfc-editor `.txt` rendering and gets `.txt` line anchors only. The entry says they
   are two renderings of one document and names which anchor belongs to which; no second registry row on the `.txt` URL.
4. Wrote the entry with the provenance trio (`source:`, `verified-at:`, `recheck:`) plus the house `ground:`/`scope:`,
   the eight-class table with one exercised example each, the verdict order, and seven limits — the two required ones (text
   not quality; two captures not a history) plus five observed precision limits.

## Commands and exit codes

| Command | Exit |
|---|---|
| `sha256sum .ufo/waves/round-84/w1/ScoutSources/rfc9111.txt .ufo/waves/round-83/w1/ScoutSources/rfc9111.txt` (identical) | 0 |
| `sha256sum …/rfc9111-httpwg.html …/rfc9111.txt` | 0 |
| python3 quote audit over `rfc9111.txt` (14 spans, `quote-substrings.tsv`) | 0 |
| python3 HTML anchor locator (`html-anchors.tsv`) | 0 |
| `python3 -B scripts/policy_value_class.py --a .ufo/waves/round-81/capture --b .ufo/waves/round-82/capture --declared .ufo/waves/round-81/capture-expectations.json` | 0 (`tool-real-pair.exit=exit=0`) |
| `python3 -B scripts/policy_value_class.py --a .ufo/waves/round-84/capture-control/control/a --b …/control/b --declared …` | 0 |
| `python3 -B scripts/policy_value_class.py --a …/equivalent/a --b …/equivalent/b --declared …` | 0 |
| `python3 -B scripts/policy_value_class.py --selftest --work .ufo/waves/round-84/w1/ScribeKnowledge/selftest-work` | 0 (`selftest: 15/15 passed`) |
| python3 `value_class` edge probe (`value-class-edges.txt`) | 0 |
| python3 entry-quote audit over the written file (`entry-quote-audit.txt`) | 0, 14/14 PASS |

Tool outputs as printed: real pair `summary surfaces=3 changed=0 … verdict=policy-unchanged`; `control`
`changed=3` with `cache-control numeric_parameter`, `x-frame-options header_added`, `referrer-policy reordered`,
`verdict=policy-changed`; `equivalent` `changed=1` (`referrer-policy reordered`), `verdict=policy-rewritten-equivalent`.
All three match `policy-expectations.json`.

## Independent re-derivation

Using `header_change_class.load_surface` (which returns canonicalized headers) over the two captures: 4 + 5 + 5 = 14
moved names, all `per-request`; 0 changed policy headers. The four policy-class fields present on every surface —
`access-control-allow-origin: *`, `cache-control: max-age=600`, `expires`, `server: GitHub.com` — are identical on both
sides. My first pass double-canonicalized the already-canonical dict and read 0 headers; I caught it, re-ran correctly,
and the entry states the verified numbers, not the first pass.

## Findings (reported, not patched)

1. **Item wording is wrong about the section number.** The ScoutSources item and the L1 correction say "§5.2.2.2
   `max-age`". In both retained renderings §5.2.2.2 is `must-revalidate`; `max-age` is §5.2.2.1 (HTML
   `id="rfc.section.5.2.2.1"` line 282 col 6944; `.txt` line 1208). The entry uses §5.2.2.1 and the defect is filed
   here and to KakeR84 rather than propagated.
2. **`reordered` is multiset equality, not order-only.** `max-age=600, max-age=60` → `max-age=60, max-age=600`
   classifies `reordered` → `policy-rewritten-equivalent`, while RFC 9111 §4.2.1 (`rfc9111.txt` 677-679) says of
   duplicate values that the first occurrence is used or the response is stale — so position can select 600 vs 60 s.
   The entry records this as limit 3.
3. **Case/whitespace-only moves read as `reordered`.** `Max-Age=600` → `max-age=600` and `max-age = 600` →
   `max-age=600` classify `reordered` though nothing was reordered (limit 4).
4. **`numeric_parameter` is decided by digit-string inequality.** `max-age=0600` → `max-age=600` classifies
   `numeric_parameter` though the numeric value did not move (limit 5).
5. **Quoted-string arguments read as `directive_changed`.** `max-age="600"` → `max-age=600` is a formatting move, but
   the grammar does not unquote; RFC 9111 §5.2 says recipients ought to accept both forms (`.txt` 1099-1102) (limit 6).
None of 2-5 occurs in the real pair or the two control pairs; the frozen predicate is unaffected. They are candidate
routed defects for round 85, not reasons to reopen C2.

## Scope honesty

I did not edit the frozen files, `corpus/SOURCES.md`, `corpus/README.md`, `considerthese/`, or the fleet repo. I made no
network call (the httpwg and rfc-editor bytes were retained by ScoutSources). No tool install or upgrade was needed or
performed. Scratch `/fast/scratch/hyaku/kake-r84/ScribeKnowledge/` was emptied and removed (`rmdir` exit 0); the selftest
fixture tree written under the receipts dir was deleted before yield. `ScribeRegistry-2` was messaged that the entry exists
and may take the after-census; its census result is not mine to claim and was not observed by me.

## Verdict

Entry written and self-verified: 14/14 quotes are raw substrings of the named `.txt` lines at ≤25 words each, the five
HTML anchor coordinates resolve in the retained HTML, and all four tool runs exit 0 with the frozen expected verdicts.
C2's knowledge surface is complete; the §5.2.2.2-vs-§5.2.2.1 wording and the four class-boundary imprecisions above are
reported as findings for the canonical judge.
