# ExecCensusCommands — round 64 census

T0 observed at lane HEAD `cc8add1fa740b920ea5179a71152680ab220c70c` (`git -C /home/vgpnk/Projects/shokunin/kake-shokunin rev-parse HEAD`). Source contract and frozen commands: `/home/vgpnk/Projects/shokunin/CORPUS.md:131-147`. Source tested: `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`.

## Seven frozen manual commands and T0 output

Executed from `/home/vgpnk/Projects/shokunin/kake-shokunin`:

1. `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`
   ```
   171
   ```
2. `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md`
   ```
   0
   ```
3. `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md`
   ```
   A=148 B=6 C=17
   ```
4. `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md`
   ```
   mined=141 queued=8 rejected=22
   ```
5. `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d`
   ```
   [no output]
   ```
6. `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md`
   ```
   [no output]
   ```
7. `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done`
   ```
   [no output]
   ```

## Verdict and receipt comparison

Confirmed 171 registry rows; 0 malformed; 0 duplicate IDs; 0 enum violations/tier inflation; 0 missing mined `used-by` paths. Histograms were A=148/B=6/C=17 and mined=141/queued=8/rejected=22.

Compared with `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/controls/census-before.txt:1-18` and `census-after.txt:1-18`: the receipts are byte-identical, listing the same 16 cross-scope duplicate-URL notices, `kake ok` for the absolute SOURCES.md path, and `census-*-exit=0`. These are not the seven manual command outputs: they do not contain the row count, malformed count, histograms, duplicate-ID, enum/tier, or used-by results. Thus the independent T0 execution supports the expected census properties; the before/after receipts alone do not document those seven outputs.

No tools installed. No lane files modified except this scoped report; preexisting untracked lane artifacts were observed in `git status --short` and left untouched.
