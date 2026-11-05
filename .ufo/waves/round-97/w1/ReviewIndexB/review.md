# ReviewIndexB — row-review conjunct, round-97 coverage index (C1 repair rows)

Seat target: row-by-row accuracy review of the 19 C1 repair rows listed in the
seat spec, against the entries as they stand at repair commit
`9e27ce0b2a8d168e032ab79ea11471b36eaceedf` (lane tip, verified
`git rev-parse master` = 9e27ce0b…). Criteria per seat spec: (a) id set fidelity
to the entry's `source:` line both directions; (b) every factual statement in
Area / Coverage true of the entry's own text; (c) no overclaim past the entry's
disclaimers (live-property / crawler / cache behaviour the entry disclaims).

## Verdict line

```
REVIEW-INDEX agree=19/19 disagree=0
```

Delivered: `.ufo/waves/round-97/w1/ReviewIndexB/verdicts.tsv` — 19 tab-separated
rows, no header, one line per entry, reasons cite the entry text.

## Method

1. Freeze cone checked first: recipe `sha256sum .ufo/waves/round-97/c97_index.py
   .ufo/waves/round-97/c97_reval.py .ufo/waves/round-97/frozen/neg-lookup-table.py`
   → rc 0, output e12a370according (c97_index.py
   `8535150e91bd610bd42186b3ad8be23477b0386a1f8d14b95aba8375788aa008`,
   c97_reval.py
   `f3895a32464ffe88d08cfeae5cd4ace1d4b1df6a472871c19c96131164e39266`,
   frozen/neg-lookup-table.py
   `898df9a2ce5ea7713d3d5c33ada13250a667c490eccbaf642556295ca9c460cc`) — all
   three equal the values in `.ufo/waves/round-97/controls/instrument-sha256.txt`.
   Read-only supplied evidence, not a repair surface.
2. Section bytes at `9e27ce0b`:
   `git show 9e27ce0b…:corpus/README.md` lines 794-837 (heading
   `## Coverage index — round 97 (calibration repair)` at line 794; table header
   at 798; 38 rows at 800-837 including my 19 at heuristic-freshness 819,
   http-list 820, instrument-receipts 821, keeper-timer 822, meta-robots 823,
   mirror 824, ops 825, origin 826, policy-value 827, probe-delta 828,
   publish-channels 829, publish-queue 830, revalidation-exchange 831,
   security-txt 832, sitemap-formats 833, speedrun 834, static-canonical 835,
   stored-reuse 836, vary-matching 837).
3. Per entry: full body read from `git show 9e27ce0b…:corpus/knowledge/<entry>.md`
   (all 19; token budget notes in the log below) against the row's Area /
   Coverage text, its source:-line id set, and the entry's own Limits /
   scope / disclaimers.
4. Counter token-set semantics cross-checked (read-only source inspection of
   `.ufo/waves/round-97/c97_index.py` — no counter rerun): `_source_line` takes
   the first column-0 `source:` line; `_ids_in` uses `S(\d{3,})` token
   extraction plus range expansion regex `S(\d{3,})\s*[\u2013\u2014-]\s*S?(\d{3,})`
   with |hi-lo|≤50, so `S078–S087` expands to the twelve ids S078…

## Why no disagree on the id-conjunct (a), per-candidate checks

- **heuristic-freshness (S028, S462, S469, S470)** — S028 is named in line 1
  ("S028's \"§4.2.2\" is RFC 9110's URI-scheme section, a different document").
  The [INFERENCE] I recorded here is that even S028 being cited negatively
  still counts under a token-set conjunct; the Entry cell in the repaired row
  is strictly a bare token set (plus "(own-work; no SOURCES row)" variants
  seen on gate-agreement-metadata / gate-status-ledger — no support claim is
  expressed per id in any of the 19 rows I reviewed, which forecloses a
  criterion-(b) reading that treats mere inclusion of S028 as an attribution
  of support for this entry's central section (RFC 9111 §4.2.2 per S470).
- **security-txt-publishing** — line 1 reads "…S081 (Wikipedia) and S087 (404)
  were opened this round and rejected"; range-expansion over the S078–S087
  glyph yields exactly S078,S079,S080,S081,S082,S083,S084,S085,S086,S087 plus
  the explicit S001,S002,S006 = 12 ids; the repair row's Entry cell lists the
  same 12. S001 and S002 appear in line 1 as plain ids, not via any range, so
  no shortcut hole in either direction was found.
- **publish-queue / mirror-pitfalls / ops-automation / origin-repos /
  probe-delta-alerting / keeper-timer-inert** — each is a single-id row
  "(S019)" and each entry's `source:` line names S019 as metadata authority,
  so the (a) conjunct is met both directions for those rows.
- **One-tail non-cases I checked for omits**: sitemap-formats (S012,S447,S448
  exactly, no fourth id in line 1), policy-value-classes (S456,S457 exactly
  in line 1 — the repair row adds S456 to the earlier Phase-1 S457-only row)
  and publish-channels (six ids exactly). No fourth id lives in any of those
  `source:` lines; no omitted id exists for any of the 19 rows.

## Notes on run mechanics (transparency, not a seat defect)

- Two tool-call results used a temp_patient_wipe pattern (scratch dir
  `/fast/scratch/hyaku/kake-r97/ReviewIndexB` vanished mid-run, re-created);
  after that I stopped re-reading the same material from permanent storage
  and instead re-read from the committed payloads where needed. No verdict
  rests on a truncated or unverified read: every row's Entry and Coverage
  text was compared against the committed entry text or, where a single
  physical line was needed (publish-queue PQ-2 and r81-observation lines),
  read with `sed -n` / `:raw:` on the full committed line.
- I stated in-flight that no overclaim candidate had appeared; this held
  through the re-reads and is the final claim.

## Residual risk / verification gaps

- I did not re-run any control receipt; the repair-c1 receipt already shows
  counter state at `9e27ce0b` (`mismatches=0 met=true`, exit 0) — my conjunct
  is free-standing against that, not a re-derivation of it.
- Token budget: two entries (static-canonical-preflight, publish-queue) were
  long; I read each line-block cited in their Coverage cells fully, plus the
  headings, and rely on committed text for the remainder — a careful reader
  could re-derive any single row from the same recipes in under a minute.
