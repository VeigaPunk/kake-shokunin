# Round 91 assimilation evidence (kake)

Read-only work against `/home/vgpnk/Projects/shokuknow`; nothing was written, fetched or
committed there, and no campaign tool was run.

## Id collision check (scratch, before any append)

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' LANE/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u > reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' $S/merge/kake/SOURCES.append.md | grep -oE 'S[0-9]+' | sort -u > staged-ids
comm -12 reg-ids staged-ids > collisions
```

- `reg-ids` 205 ids (lane registry at base `5b20af16`), `staged-ids` 129 ids (package).
- `collisions` **8**: S312 S329 S367 S372 S373 S374 S390 S409 — unchanged since round 80.

The guard was proven able to fail in round 90 (`corpus/lessons/round-90.md`); this round
re-ran it and got the same nonempty set. A nonempty `collisions` file means the package
still cannot be adopted append-only without a renumber decided in scratch, so:

**Assimilation: none.** No `merge/kake` theme or entry was adopted this round; the
package's staged ids still collide with the lane's registry on the same eight ids.

## Quarantine slice (payload-absent register)

```
awk -F'|' -v l='kake' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```

12 data rows this round (9 `payload-absent`, 3 "could not be fetched"), same set as the
round-86 hand-check. Their verdicts are already on the record in
`corpus/lessons/round-86.md:148` and `.ufo/waves/round-86/assimilation-quarantine.md`:
each `payload-absent` row is refused as unverifiable (not fabrication) and each
"could not be fetched" row is marked unverifiable, with the flip "the cited source is
fetched and the quote located". No new row entered the slice, so nothing new is owed.

## considerthese

`considerthese/2026-10-26.md` Part 2 proposal 3 (operator-decision queue) is already on
the record in `corpus/lessons/round-90.md` §Operator-decision queue. The latest file has
no other still-unimplemented proposal that fits this round's claims; nothing was mined
from it this round.
