# VerifyEntryNumberingM02 — mutant M02 attack report

Verdict: **valid control** (mutant breaks the contract on the witness; reference matches).

## What I checked

- Target receipt `verification/a3/w1a3-MutEntryNumbering__M02.json`: label `w1a3-MutEntryNumbering__M02`, passed 24/24, met=true, toolSha256 `bf48b6d0adb326e241a4e7656044a722077a137d92d84c7ba949a9c870caad11` (rows/why not read, per bounds). Sha matches the `file` sha256 in the M02 entry of `mutants.json`.
- Diff `reference.py` vs `mutants/M02.py`: exactly one change (mutants.json:186–191 claims single-point, confirmed). Reference line 151 `for i, e in enumerate(ents, 1):` is replaced by a re-parse of `data` via `xml.etree.ElementTree.fromstring`; entry ordinals then count every root child that is either a sitemap-namespace entry OR any foreign-namespace element (`not child.tag.startswith("{NS}")`), so foreign-namespace root children advance finding ordinals.

## Commands (cwd = witnesses/M02; run with `timeout 60 python3 -B <tool> --manifest manifest.json`)

- Reference: exit 1, stdout `{"version": 1, "verdict": "failed-policy", "checks": [{"id": "w", "status": "findings", "error": null, "findings": [{"code": "loc_missing", "entry": 1}]}]}`
- Mutant M02: exit 1, stdout `{"version": 1, "verdict": "failed-policy", "checks": [{"id": "w", "status": "findings", "error": null, "findings": [{"code": "loc_missing", "entry": 2}]}]}`

Both match `reference_stdout`/`mutant_stdout` recorded in mutants.json:278–279.

## Witness

`manifest.json` names `s.xml`; `s.xml` = `<urlset xmlns="…/0.9" xmlns:e="urn:ext"><e:extra/><url/></urlset>` — one foreign-namespace root child before the sole `url` entry.

## Contract sentences

- Sentence 11: "The entries are the root's child elements in the sitemap namespace named `url` (in a `urlset`) or `sitemap` (in a `sitemapindex`)."
- Sentence 33: "…`"findings": [{"code": C, "entry": N|null}, …]`" — and the rule-of-record preamble (line 31): "`entry` is the 1-based position of the entry among the root's entries (rule (d))". Sentence 14: elements in other namespaces are ignored.
- The document has exactly one entry (the `url`); its `loc_missing` finding must carry `entry: 1`. The contract fully decides the witness. Reference emits 1 (correct); mutant emits 2, counting the foreign `e:extra` child — violating the sentence-11 entry set the ordinal is defined over (sentence 33's `N` is thereby wrong).

## Attacked statements: 11 holds, 33 holds

Equivalence scan: the mutant's second parse via ElementTree cannot diverge elsewhere — expat already accepted the file, ET uses the same parser, and `zip(positions, ents)` lengths always agree (both count the same entry-tag children). The only divergence is entry ordinals when foreign-namespace root children exist. Kill rule (1) fired correctly.

No tools installed; no network used; only read/run commands listed above.
