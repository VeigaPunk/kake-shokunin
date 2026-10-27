# MutExtractor — mutation test of quote-class/extract_text.py

Round 63, wave w1, seat MutExtractor (mutation-tester, leaf).

Target: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/quote-class/extract_text.py`
(committed sha256 `6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405`, 3514 bytes, 103 lines).

Detectors (the two the item names):
1. `python3 <mutant> --selftest` — the tool's own 1/1 selftest
   (`extract_text.py:75-88`, sample `Tom &amp; Jerry` + script + `<br>`).
2. `python3 <mutant> --raw S432.html --out out.txt` then
   `cmp out.txt` vs the frozen committed
   `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/quote-class/S432.txt`
   (sha256 `8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69`,
   290480 bytes). Input: retained blob
   `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/sources/S432.html`
   (sha256 `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`,
   1854393 bytes), read via symlink, never written.

Method: `cp extract_text.py /fast/scratch/hyaku/kake-r63/MutExtractor/pristine.py`;
`work.py` was the mutable scratch copy. Each mutant = one `edit` on `work.py`,
then both detectors, then `cp pristine.py work.py` + `sha256sum` verify
(`6b0a88cd…` after every restore). Python 3.14.8; no git, no installs, no
network. Scratch deleted at the end.

## Baseline (pristine)

```
python3 work.py --selftest                    → selftest 1/1, exit 0
python3 work.py --raw S432.html --out out.txt → extracted 1854393 bytes -> 286933 chars
cmp out.txt S432.frozen.txt                   → identical (exit 0)
sha256 out.txt                                → 8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69
```

Pristine reproduces the committed S432.txt byte-for-byte: baseline is green,
so mutant verdicts are meaningful.

## Mutants (6, item required ≥5)

| # | Mutation (smallest change) | selftest | S432 cmp | verdict |
|---|----------------------------|----------|----------|---------|
| M1 | line 27 `SKIP = {"script","style","noscript"}` → `SKIP = set()` | FAIL exit 1: `'Tom & Jerry var a = 1 &lt; 2; multi line text second a b\n'` | differ at char 16; mutant out 989871 bytes (986316 chars) sha `ae41e2f2…` | **KILLED** (both) |
| M2 | line 54 `append(data)` → `append(html.unescape(data))` (charrefs decoded twice) | PASS 1/1 | **identical** (exit 0, 290480 B, same sha) | **SURVIVED both** |
| M3 | lines 21–26 `BLOCK = {…33 tags…}` → `BLOCK = set()` | FAIL exit 1: `'Tom & Jerrymulti line textsecondab\n'` | **identical** (exit 0, 290480 B, same sha) | **KILLED** by selftest; **invisible to S432 cmp** |
| M4 | line 57 `" ".join("".join(parts).split()) + "\n"` → `"".join(parts)` | FAIL exit 1: `'\nTom & Jerry\n\nmulti line text\n\nsecond\n\na\nb\n'` | differ at char 1; mutant out 361046 B (356393 chars) sha `90ca1f02…` | **KILLED** (both) |
| M5 | line 32 `convert_charrefs=True` → `False` | FAIL exit 1: `'Tom Jerry multi line text second a b\n'` (`&amp;` dropped — `handle_entityref`/`handle_charref` are no-ops) | differ at char 21196; mutant out 290425 B (−55) sha `4b3336ee…`; 253086 byte-positions differ | **KILLED** (both) |
| M6 | line 47 `if tag in SKIP and self._skip:` → `if tag in SKIP:` (stray `</script>`/`</noscript>` can drive `_skip` negative → all later text swallowed) | PASS 1/1 | **identical** (exit 0, 290480 B) | **SURVIVED both** |

Mutant diffs (as applied and reverted):

```diff
M1:  -SKIP = {"script", "style", "noscript"}        +SKIP = set()
M2:  -self._parts.append(data)                      +self._parts.append(html.unescape(data))
M3:  -BLOCK = { …6-line literal… }                  +BLOCK = set()
M4:  -return " ".join("".join(self._parts).split()) + "\n"
     +return "".join(self._parts)
M5:  -super().__init__(convert_charrefs=True)       +super().__init__(convert_charrefs=False)
M6:  -if tag in SKIP and self._skip:                +if tag in SKIP:
```

## Score and coverage findings

- Overall kill rate (either detector): **4/6 killed** (M1, M3, M4, M5).
- S432-re-extraction cmp alone: **3/6** — it is blind to M2, M3 and M6.
- Selftest alone: **4/6** — it is blind to M2 and M6.

Surviving mutants are coverage findings on the *detectors*, not defects in
the frozen tool; nothing here licenses touching the committed files.

- **M2 (double unescape) survives both.** Real corpus: S432.html contains only
  4 `&amp;` occurrences (raw lines 5800, 10850, 13742, 13746) and every one
  decodes to `&` followed by non-entity text (`&&`, `&data=`, `& cache`) — a
  second `unescape` is the identity. Frozen S432.txt contains 5 `&` and zero
  `&entity;` tokens. The selftest's only entity is `&amp;`→`&`, idempotent
  under a second pass. Neither detector can see this mutant.
- **M6 (dropped `_skip` guard) survives both.** S432.html SKIP-tags are
  balanced — `<script` 8 opens / `</script>` 8 closes, `<style` 3 / `</style>`
  3, `<noscript` 0 — so the unguarded decrement never fires below zero and
  output is byte-identical.
- **M3 (block tags not breaking) is invisible to the S432 cmp detector.**
  The retained blob is whitespace-dense: every block boundary in it is already
  preceded/followed by whitespace or text that separates, so removing the
  synthetic `"\n"` leaves the collapsed rendering identical. The selftest
  catches it only because its sample packs block tags back-to-back with no
  whitespace (`</p><script>`, `</b>`, `<p>a<br>b</p>`).

Suggested coverage hardening (corpus/selftest enrichment only — a finding for
the lane, not a change this seat may make): add a doubly-escaped entity
(`&amp;lt;`) and an unbalanced `</noscript>`/`</script>` to the selftest
sample; add a second pinned input whose text differs when block boundaries
are lost.

## Restoration evidence

- After every mutant: `sha256sum work.py` = `6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405` (== pristine).
- Final `cmp work.py pristine.py` → identical; scratch dir
  `/fast/scratch/hyaku/kake-r63/MutExtractor/` removed entirely.
- Post-run fleet hashes (unchanged): extract_text.py `6b0a88cd…`,
  S432.txt `8b90d096…`, S432.html `63b0a018…`. No fleet file written; no
  git/jj run anywhere; nothing installed.
