#!/bin/bash
# ConnectorC round-82 sibling-overlap scan receipt. Read-only.
set -u
FLEET=/home/vgpnk/Projects/shokunin
echo "## merged-scan host: $(uname -sr); fleet: $FLEET"
echo

echo "=== 1. which lanes have a scripts/ entry named for capture/drift/receipt/header/etag ==="
for repo in "$FLEET"/*-shokunin/; do
  name=$(basename "$repo")
  [ "$name" = "kake-shokunin" ] && continue
  hits=$(ls "$repo"scripts 2>/dev/null | grep -iE 'capture|snapshot|delta|drift|receipt|header|etag|validator' | tr '\n' ' ')
  [ -n "$hits" ] && echo "  $name: $hits"
done
echo

echo "=== 2. literal 'capture_delta' / 'capture-to-capture' outside kake ==="
grep -rn 'capture_delta' "$FLEET" --include=*.md --include=*.py --include=*.mjs --include=*.json 2>/dev/null \
  | grep -v '/\.git/' | grep -v '^'"$FLEET"'/kake-shokunin/' | head -5
echo "  (capture-to-capture table:)"
grep -rn 'capture-to-capture' "$FLEET" --include=*.md --include=*.py --include=*.json 2>/dev/null \
  | grep -v '/\.git/' | grep -v '^'"$FLEET"'/kake-shokunin/' | cut -c1-150 | head -6
echo

echo "=== 3. RFC 9110 8.8.3 citations outside kake (ETag section?) ==="
grep -rlI '8\.8\.3' "$FLEET"/*-shokunin/ 2>/dev/null | grep -v '/\.git/' \
  | grep -v '^'"$FLEET"'/kake-shokunin/' | sed 's#'"$FLEET"'/##' | head -14
echo "  tabi csrf-defense-shape-boundary.md:39 context:"
sed -n '39p' "$FLEET/tabi-shokunin/corpus/knowledge/csrf-defense-shape-boundary.md" | cut -c1-160
echo

echo "=== 4. receipt-ledger / rewrites gates outside kake ==="
echo "  kama (append-only disclosure ledger):"
grep -n 'append-only disclosure ledger' "$FLEET/kama-shokunin/SKILL.md" | cut -c1-200
echo "  tameshi (receipt -> revision):"
grep -n 'receipt-revision-gate.py' "$FLEET/tameshi-shokunin/SKILL.md" | head -2 | cut -c1-200
echo "  kumitate (SOURCES row -> committed capture bytes):"
sed -n '26,34p' "$FLEET/kumitate-shokunin/scripts/source-capture.mjs"
echo "  souji TOOL_SHA256 occurrence:"
grep -rn 'TOOL_SHA256' "$FLEET/souji-shokunin"/SKILL.md 2>/dev/null | head -2 | cut -c1-160
echo

echo "=== 4b. kake's own receipt-ledger / append-guard gates (this lane, cited for contrast) ==="
grep -n 'c79_receipt_ledger.py |' "$FLEET/kake-shokunin/SKILL.md" | cut -c1-200
grep -n 'ledger_append_guard.py |' "$FLEET/kake-shokunin/SKILL.md" | cut -c1-200
grep -n 'receipt-rewrite-counter |' "$FLEET/kake-shokunin/SKILL.md" | cut -c1-200
echo

echo "=== 5. two-capture doctrines outside kake: idempotence vs drift ==="
sed -n '371p' "$FLEET/tabi-shokunin/SKILL.md" | cut -c1-260
sed -n '110p' "$FLEET/tabi-shokunin/corpus/knowledge/live-dynamic-capture.md" | cut -c1-160
echo "  kaidoku re-capture (custody receipt reproducibility):"
sed -n '759,761p' "$FLEET/kaidoku-shokunin/SKILL.md" | cut -c1-200
echo

echo "=== 6. who owns ds4cc.com ==="
grep -n 'ds4cc' "$FLEET/kasegi-shokunin/.ufo/waves/round-23/build/OverlapWeb.md" | head -2 | cut -c1-260
grep -n 'remote surfaces' "$FLEET/kama-shokunin/MINT.md" | cut -c1-200
echo

echo "=== 7. sibling ground that bears on reading a capture-to-capture delta ==="
echo "  mori S594 (RFC 9111 4.1 Vary) row head:"
sed -n '375p' "$FLEET/mori-shokunin/corpus/SOURCES.md" | cut -c1-330
echo "  mori entry ua-serving-normative-r79.md K2 (lines 24-26):"
sed -n '24,26p' "$FLEET/mori-shokunin/corpus/knowledge/ua-serving-normative-r79.md" | cut -c1-300
echo "  mori entry K4 (line 34):"
sed -n '34p' "$FLEET/mori-shokunin/corpus/knowledge/ua-serving-normative-r79.md" | cut -c1-200
echo "  kumitate S237 (RFC 9111 Age) row head:"
sed -n '191p' "$FLEET/kumitate-shokunin/corpus/SOURCES.md" | cut -c1-260
echo "  kumitate entry receipt-age-on-the-compare-path.md:1-3:"
sed -n '1,3p' "$FLEET/kumitate-shokunin/corpus/knowledge/receipt-age-on-the-compare-path.md" | cut -c1-220
echo

echo "=== 8. exit status ==="
echo "receipt complete"
