import sys

row = (
    "| S463 | RFC 9111 - HTTP Caching, 4.1 Calculating Cache Keys with the Vary Header Field "
    "- https://httpwg.org/specs/rfc9111.html | spec | A | "
    "Vary-match semantics for the conservative reader: field-name case-insensitivity, absence symmetry "
    "and the wildcard member; not cache-key construction, storage, revalidation or browser behaviour | "
    "RFC 9111 June 2022 section 4.1 paragraphs 1-5; GET 200 2026-11-04 | "
    "A cache must not use a stored response without revalidation unless all nominated Vary fields match; "
    "absent-from-both matches; a wildcard member always fails | mined | 2026-11-04 | 180d | "
    "corpus/knowledge/vary-matching.md |"
)

src = sys.argv[1]
out = sys.argv[2]
lines = open(src, encoding="utf-8").read().split("\n")
for i, line in enumerate(lines):
    if line.startswith("| S462 |"):
        lines.insert(i + 1, row)
        break
else:
    raise SystemExit("S462 row not found")
open(out, "w", encoding="utf-8").write("\n".join(lines))
print("inserted S463 after S462")
