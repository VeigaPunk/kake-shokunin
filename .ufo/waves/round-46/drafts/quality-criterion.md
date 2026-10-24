# QUALITY.md receipt-identity criterion draft

- **Receipt identity for filed counts (round 46).** Any filed count or verdict against a receipt cites that receipt's path + sha256; a receipt citation without sha256 violates this criterion. Grounding: round-45 Mistake 15's fix says a count against “the claim receipt” must bind to that receipt's identity (path + sha256), and the count must be re-derived from the named receipt's committed bytes rather than another same-named receipt's values.

## Application check

Count this criterion's unique label in `corpus/QUALITY.md`:

```sh
grep -c '^- \*\*Receipt identity for filed counts' corpus/QUALITY.md
```

Frozen stdout shape: one decimal count and newline; expected `0` before the criterion is appended and `1` after exactly one occurrence is appended.

The broader proposed expression `grep -c '^- .*receipt.*\(path\|sha256\)' corpus/QUALITY.md` also matches older criteria, so it is not a reliable 0 → 1 check for this addition; record that discrepancy rather than treating its count as this criterion's count.
