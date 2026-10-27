#!/usr/bin/env bash
# ProbeBodyStability: fetch each round-59 source URL 3 times, spaced >= 30s, with a fixed UA.
set -u
S=/fast/scratch/hyaku/kake-r59/ProbeBodyStability
mkdir -p "$S/fetches"
UA='kake-shokunin-round59-probe'
S425_URL='https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers'
S426_URL='https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests'

fetch() { # $1=id $2=url $3=n
  local id=$1 url=$2 n=$3 out="$S/fetches/$1.$3.html"
  local ts
  ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  local code
  code=$(curl -sS -L --max-time 60 --compressed \
      -A "$UA" \
      -H 'Accept-Language: en-US,en;q=0.9' \
      -o "$out" -w '%{http_code}' "$url" 2>"$S/fetches/$1.$3.err" || echo "ERR")
  local sha
  sha=$(sha256sum "$out" | cut -d' ' -f1)
  local size
  size=$(stat -c %s "$out" 2>/dev/null || echo 0)
  printf '%s fetch=%s http=%s bytes=%s sha256=%s\n' "$id" "$n" "$code" "$size" "$sha" >> "$S/fetches/timeline.txt"
  echo "$ts $id fetch$n http=$code bytes=$size sha=$sha" >> "$S/fetches/timeline.txt"
}

: > "$S/fetches/timeline.txt"
for round in 1 2 3; do
  fetch S425 "$S425_URL" "$round" &
  fetch S426 "$S426_URL" "$round" &
  wait
  if [ "$round" -lt 3 ]; then sleep 35; fi
done
echo "DONE" >> "$S/fetches/timeline.txt"
