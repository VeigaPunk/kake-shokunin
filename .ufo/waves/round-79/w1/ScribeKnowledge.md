# ScribeKnowledge — round 79 w1: knowledge entry and registry row

verdict: landed. `corpus/knowledge/x-robots-tag-header.md` (new, 227 lines), one S452 registry row
(`corpus/SOURCES.md:199`), one S449 `used-by` change, one coverage-map row plus the three append-only
coverage-map corrections from the L1 ruling. `sources-census.sh validate` exits 0; the W04 line count
is unchanged at 19 and the before/after outputs are byte-identical, so this row adds no warning.

## Landed bytes (2026-11-04T09:56:40Z)

| path | action | bytes | lines | sha256 |
|---|---|---|---|---|
| `corpus/knowledge/x-robots-tag-header.md` | new | 19,468 | 227 | `37a6a75ea2f598d74de51d16fc304cc9279da54d10a99c48e3a4756ef62a29b1` |
| `corpus/SOURCES.md` | +2/−1 lines | 175,232 | 307 | `e9a50be8329e82ee096571504e0e8abadbe4970228ffb43ff88677322a3ba39e` |
| `corpus/README.md` | +16 lines | 60,018 | 582 | `6b87908bdda1cb8abe2ffa07a02d991f958aec7011b9d53323703ade814f2d91` |
| `PROVINCE.md` | +8 lines | 42,614 | 598 | `d355deaee8749d4c5bd94029e695e2e67a53d295a011df728716cc24245a7623` |
| `corpus/knowledge/meta-robots-directives.md` | +2 lines (append only) | 13,167 | 140 | `4c0f5f03f7e5682f463cc5fd698cd6450f1e2135302ea8766a6ce72832871e55` |

`git diff --stat` over the four tracked files: 28 insertions, 1 deletion — the deletion is the S449
row re-added with its new `used-by` cell; no other held-row byte moved
(`.ufo/waves/round-79/w1/ScribeKnowledge/landed-bytes.txt`).

## Entry

`corpus/knowledge/x-robots-tag-header.md` — front matter carries both sources with hashes, the access
date, `ground: operability — the offline X-Robots-Tag declaration audit (round-79 C2)` and
`terms:` citing `contract-amendment-1.md` (`43e0a9b7`). Body: declaration role; grammar (field values
and comma lists, multiple field lines, the optional `<bot-name>:` scope binding subsequent rules in
that field, directive and value forms); conflicts and combination; five lane readings; what the tool
decides and does not; S452/S449 cross-checks; limits.

Content decisions worth the reviewer's eye:

- **S452 is quoted for the header's own syntax** (definition, de-facto status, `<bot-name>` scope,
  field-line examples, directive list, value forms, conflict fragment, date sentence, robots.txt
  interaction); **S449 is quoted for the rules that only it states in clean form** (unprefixed rules
  are global, case-insensitivity of header/agent/value, the multi-field/comma-list sentence, the
  full conflict sentence, the negative-rule sum, `noarchive` as historical, the date families). Both
  are cited side by side; the entry does not treat MDN as the sole authority.
- **`noarchive` follows amendment 1 A1**: the entry states that S452 never names it, that S449 lists it
  as historical, and that the lane admits it as a value-less directive under A1 with no current Google
  effect claimed. No grammar/oracle disagreement is described (the earlier report to the L1 was
  settled by the amendment; frozen artifacts were not touched by this seat).
- **Directive-name precedence, per-field scope and per-bot exclusion** are marked `[INFERENCE]`/lane
  reading; the entry names what would supersede them.
- **One open lane edge, unpinned by any case**: duplicate `max-snippet`/`max-video-preview` collapse to
  the numeric minimum, but `-1` means "no limit" (`S452:202`) and "Google will choose"
  (`google-robots-meta.txt:1104-1105`), so a `-1` beside a concrete bound collapses to the *least*
  restrictive value while S452's principle is the more restrictive rule. The entry records this as a
  contract edge, not a sourced precedence rule. No action requested; no case pins it.
- **S449's own header example is outside the frozen date grammar**: `unavailable_after: 25 Jun 2010
  15:00:00 PST` (`google-robots-meta.txt:997`) has no weekday and a named zone, which the frozen
  RFC-822-shaped branch rejects; S452's own example (`Wed, 03 Dec 2025 13:09:53 GMT`) fits. Recorded
  as a limit of the lane grammar, not as a source conflict.

## Registry

- **S452 row** at `corpus/SOURCES.md:199`, inside `## Registry` (after S451, before `## Paths`):
  kind `docs`, tier `B`, status `mined`, opened `2026-11-04`, recheck `90d`, used-by
  `corpus/knowledge/x-robots-tag-header.md`. 11 cells, separator-split NF=13.
  Gate quote: `An optional <bot-name>: specifies the user agent that the subsequent rules should
  apply to` — 14 words, exact substring of the retained text, exactly 1 occurrence, inside the content
  block (Syntax section). Access date and pointer are in the anchor cell:
  `https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Robots-Tag`, fetched
  2026-11-04T09:39:04Z, HTTP 200, 218,816 B, raw sha256 `c4216ffb…7aaf38`, text sha256 `8be2a406…482556e`,
  retained at `.ufo/waves/round-79/sources/S452-mdn-x-robots-tag.raw` (frozen input of `e1a9a897`, not a
  seat tree). Receipt: `.ufo/waves/round-79/w1/ScribeKnowledge/sources-row-check.txt`.
- **S449 `used-by` changed** (`corpus/SOURCES.md:196`), other ten cells byte-equal — for the lesson
  Gate:
  old `corpus/knowledge/meta-robots-directives.md`
  new `corpus/knowledge/meta-robots-directives.md, corpus/knowledge/x-robots-tag-header.md`
- **No S453 row.** RFC 9309 was not appended in any status; the reject belongs in the round Gate.
  Sweep: `grep -ci 'x-robots-tag' .ufo/waves/round-79/sources/reject-rfc9309.txt` prints `0`, **exit 1**
  (no match; the `exit 0` wording in the coordination note is wrong — `grep -c` prints 0 and exits 1).
  Context control: `grep -ci 'robots'` on the same file prints `42`, exit 0. Flip: an RFC or update
  that defines header-level X-Robots-Tag processing. S099 already holds RFC 9309 for robots.txt
  (`corpus/SOURCES.md:107`). Receipt: `.ufo/waves/round-79/w1/ScribeKnowledge/rfc9309-sweep.txt`.

## Census

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
```

before (at `24476085`): exit 0, 20 output lines, 19 W04 lines. after (final tree): exit 0, 20 output
lines, 19 W04 lines; `diff` before/after is empty. Row count 189 → 190. Receipts:
`census-before.txt`, `census-after.txt`.

## Quote truth

`.ufo/waves/round-79/w1/ScribeKnowledge/verify_quotes.py` checks 47 stored quotes (S452 and S449):
each is a whitespace-collapsed raw substring inside its named line range, 1–25 units, and the Gate
quote occurs once in its page. Result: `checked=47 failures=0 max_units=23`, exit 0
(`verify-output.txt`, `quote-receipts.json`).

A second pass over the entry itself (`entry-span-check.txt`): 32 quoted spans, 29 found in the two
retained bodies, 2 contract heading quotes (`C2 tool interface (frozen)`), 1 quoted registry cell
(`not header processing`), 0 unknown, 0 over 25 units, max 23. One span that had backticks inside the
quoted text was corrected to the raw sentence before this receipt.

## Coverage map (ruling 4 / ConnectorC)

Append-only; no existing line rewritten.

- `corpus/README.md`: new `## Coverage — round 79 (2026-11-04)` section at EOF — one coverage row for
  the entry/tool/cases, the sources-opened line (registry 189 → 190, census exit 0), and a
  `[r79-correction 2026-11-04]` paragraph naming `scripts/x_robots_tag_audit.py` and calling the
  round-78 exclusion paragraph historical (the snapshot/header instruments parse no robots directive).
- `PROVINCE.md`: appended `[r79-correction 2026-11-04]` paragraph naming the new instrument and the
  contract/amendment; the "What it refuses" paragraph stays verbatim.
- `corpus/knowledge/meta-robots-directives.md`: one appended line opening with
  `[r79-correction 2026-11-04]`; the file only gained lines.

## 31-case contract read (review evidence only; no measurement run)

I read every `cases/cNN/manifest.json` against the contract's clauses as frozen (before amendment 1)
and against `expect/expect.json`. 30 of 31 cases agreed with the contract as written; the exception was
c26 (`noarchive`), which I routed to the L1 as a contract/oracle mismatch. The L1 landed
`contract-amendment-1.md` (`43e0a9b7`, terms-only, before any after-state) adding `noarchive` under
A1 and pinning normalization under A2, which settles c26 in favour of the frozen expectation. The
entry now cites A1 and describes no open conflict. I ran no case and no counter; the C2 measurement
belongs to ExecC2Tool/Critic/the counter receipt.

## Out of scope / not done

- No `SCORECARD.md`, `LOG.md` or `corpus/lessons/` edit (record scribe owns them). The S449 `used-by`
  change old→new was sent to `ScribeRecord-4` for the lesson Gate and is recorded above.
- No tool run, no network fetch, no install or upgrade (nothing to record under the tooling rule).
- Scratch `/fast/scratch/hyaku/kake-r79/ScribeKnowledge` was created and removed; a sibling seat's
  tree under the same parent was not touched.

## Receipts

All under `.ufo/waves/round-79/w1/ScribeKnowledge/`:
`verify_quotes.py`, `quote-receipts.json`, `verify-output.txt`, `entry-span-check.txt`,
`sources-row-check.txt`, `rfc9309-sweep.txt`, `census-before.txt`, `census-after.txt`,
`landed-bytes.txt`.
