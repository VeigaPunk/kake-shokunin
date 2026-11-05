readme-row-check.txt — round-98 C2 knowledge entry README row (seat ScribeEntry)
counter .ufo/waves/round-97/c97_index.py, its own audit() reused over a fixture

fixture /fast/scratch/hyaku/kake-r98/ScribeEntry/fx (clone of the lane, toplevel verified)
fixture commit e9ca37341a9ac217bfb338f8920ed9ff7bac1806

entry source: ids from the entry's own source: line = ['S478', 'S480', 'S482', 'S483']
entry population=85  index_rows=130  dangling=[]
unindexed=none

rule (a) Entry cell carries `knowledge/stale-extensions` -> True
  Entry cell: `knowledge/stale-extensions.md` (S482, S483, S480, S478)
rule (b) every source id in the row -> True (missing=none)
  ids present in the row line: ['S478', 'S480', 'S482', 'S483']
rule (c) other cells hold >= 8 words and share >= 2 long words with the entry -> True
  other-cell word count=38  shared long words=['contract', 'decided', 'decision', 'extensions', 'request', 'response', 'revalidation', 'served', 'stale-serving', 'storage', 'stored', 'supplied', 'values', 'whether']

row line: | Stale-serving extensions decision (r98) | `knowledge/stale-extensions.md` (S482, S483, S480, S478) | Whether a stale stored response may be served on a request or on an error, and for how long, decided over supplied values under contract v1; no live cache, no storage, no revalidation scheduling |
violations=0
