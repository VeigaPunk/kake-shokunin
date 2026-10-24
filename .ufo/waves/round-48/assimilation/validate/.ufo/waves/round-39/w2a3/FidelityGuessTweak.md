W2A3 fidelity attack: CtlGuessTweak (shape 23: keyword guesser, no parse tree). Verdict: **faithful shortcut, materialized byte-exact.**

Target: `.ufo/waves/round-39/a3-controls/w1a3/CtlGuessTweak.py` sha256 `7ee98e6a296e17e0298caff3b8b7730436b72d6bf7d8190ab66d4493b215206e` (621 lines).

## Shape check — holds
- Imports (lines 13–18): `json, os, re, sys, datetime.date, urllib.parse.urlsplit`. No `xml.*`, `expat`, `html`, `lxml`, `sax`, or tree library — matches "no parse tree".
- `scan()` (lines 180–297) is a hand-written character scanner yielding flat events (`text`/`literal`/`start`/`end`/`doctype`); `audit_bytes` folds events through a frame stack — no DOM/tree built. Findings come from per-element regex/keyword checks (`_valid_lastmod`, `_valid_priority`, `_parse_url`, `CHANGEFREQ`).
- Skipped work is real: see divergences below — it does not implement full XML 1.0 well-formedness grammar, so it is a shortcut, not a hidden parser.

## Tweak check vs base — holds
- Base: `dead-w1/CtlCodeGuess.py`, `git show 72edf2123f92b9dc546494cbffcc777ed3c3cd3a:...` → sha256 `1d0a5d9f1ff859b1b7ba403b4ee4e5e775306de24103902bb27c10b590958448` — matches report line 3 exactly.
- `diff base ctl` = 8 hunks, 10 `-` / 14 `+` lines = 24 changed lines — matches report's "24 changed lines" (line 5). No new import or parser added.

## Materialization — byte-exact
- `patch -p1 base.py < l1-materialized.diff` → sha256 `7ee98e6a…` — BYTE-IDENTICAL to committed control.
- Fenced ` ```diff ` block extracted from `w1a3/CtlGuessTweak.md` ≡ `l1-materialized.diff` byte-for-byte (`diff` empty).
- Receipt `verification/a3/w1a3-CtlGuessTweak.json`: `passed:23, met:false, toolSha256:7ee98e6a…` — the scored bytes are the committed bytes.
- Minor: report (line 46) asked L1 to materialize `NOTE.md`; `/fast/scratch/hyaku/kake-r39a3w1/CtlGuessTweak/` contains only `control.py` + `l1-materialized.diff`. Non-scored artifact; does not affect the verdict.

## Divergence runs (control vs correct tool)
All inputs use manifest `{"version":1,"checks":[{"id":"t","file":"s.xml","sitemapUrl":"https://e.test/s.xml"}]}`; stdlib `xml.etree` confirms each is NOT well-formed XML → contract rule 8 → a correct tool emits `xml_malformed`, exit 1. Control run: `timeout 30s python3 ctl.py --manifest <d>/manifest.json`.
1. `<!-- -- -->` inside `<urlset>` (illegal `--` in comment): control → clean/exit 0; correct → xml_malformed. DISAGREES.
2. `https://e.test/a]]>b` inside `<loc>` (literal `]]>` in content): control → clean/exit 0; correct → xml_malformed. DISAGREES.
3. `<!FOO bar>` before root (non-DOCTYPE/comment `<!` declaration): control → clean/exit 0; correct → xml_malformed. DISAGREES.
4. `<![CDATA[x]]>` after root close (CDATA outside root): control → clean/exit 0; correct → xml_malformed. DISAGREES.
5. `<!doctype x>` (lowercase doctype keyword): control → `doctype_present`/exit 1; correct → xml_malformed. DISAGREES (wrong finding code; exit happens to match).

## Per-attacked statement
- Shape "keyword guesser, no parse tree": holds — imports clean, scanner stays event-flat, no tree.
- "Skips the work its shape says": holds — 5/5 crafted malformed inputs escaped its grammar (clean or wrong code vs xml_malformed).
- "L1 materialized seat text byte-for-byte": holds — base+diff ≡ committed file ≡ scored sha256.
- Report's own claims (base sha/commit, 24 changed lines, counterexample list): holds; `[INFERENCE]` tag on line 4 is honest — the claimed defects exist (e.g. its base accepted `&#0;`, literal-`]]>`, etc.).

Residual risk: the control is still lenient well-formedness-wise, so it can over-clean malformed sealed cases (consistent with `met:false, passed:23`).
