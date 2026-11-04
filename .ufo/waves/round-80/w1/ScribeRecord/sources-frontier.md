# Round-80 sources & frontier paragraphs (for the report and `corpus/README.md`)

All numbers below are this seat's own measurements on 2026-11-04: the **before** values at the base
`9998dc7a586b9fe76379014c8123aa3606f2d8b9`, the **after** values on the lane worktree once the `S453`
row (`corpus/SOURCES.md:200`) and `corpus/knowledge/http-date-grammar.md` had landed. The L1 re-runs
both commands at the carrier; if either number moves, the carrier's value wins.

**Rows before → after.** Counting command, read-only:

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census \
  --file /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
```

Before (base `9998dc7a`): `rows 190`, `tier.A 166`, `tier.B 7`, `tier.C 17`, `status.mined 160`,
`status.queued 8`, `status.rejected 22`. After: `rows 191`, `tier.A 167`, `tier.B 7`, `tier.C 17`,
`status.mined 161`, `status.queued 8`, `status.rejected 22` — registry **190 → 191 rows**. The
matching validation stays clean and moves the warning count, not the exit:
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
kake` exits 0 with 19 `W04` lines at the base (`controls/census-before.txt`) and 20 after, the new line
being `W04 S453 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes`. That warning is the
expected shape of the admit, not a defect: `S453` is a second scoped row on a document already held at
`S028` (empty-host URI validity), with the same plain-text digest `21c1cdce…7232a`, and `rfc9110.txt`
was already shared by `S028`/`S033`.

**Rows added by tier.** One row this round, and it is tier A: `S453` — RFC 9110, *HTTP Semantics*,
§5.6.7 *Date/Time Formats*, kind `spec`, status `mined`, opened 2026-11-04, recheck `365d`, used-by
`corpus/knowledge/http-date-grammar.md`. No tier-B and no tier-C row was added, no existing row was
rewritten, and no other registry cell changed: `tier.B` stays 7 and `tier.C` stays 17. The knowledge
side moves with it by exactly one entry — `corpus/knowledge/*.md` was 66 files at the base and is 67
after (measured with `ls corpus/knowledge/*.md | wc -l`).

**Frontier line for `corpus/README.md` §Frontier.**

> *(round 80, 2026-11-04)* The `unavailable_after` HTTP-date grammar is now held ground: the three
> RFC 9110 §5.6.7 shapes — IMF-fixdate, the obsolete RFC 850 form and asctime — the comma-bearing forms
> among them, and the `unavailable_after` decision over them are carried by `S453` (tier A, RFC 9110
> §5.6.7), `corpus/knowledge/http-date-grammar.md`, `.ufo/waves/round-80/amendments/amendment-1.md` and
> the frozen 12-case set. Still frontier, and not to be read as covered by that: per-bot effective
> resolution (the tool reports a global `effective` set only), conflicts between a meta declaration and a
> header declaration on the same URL, and header inheritance across redirect hops. These are owed work,
> not source silence — S452 states the merge rule for multiple crawlers (“the search engine will use the
> sum of the negative rules”, retained text line 252) and the lane does not implement it.
