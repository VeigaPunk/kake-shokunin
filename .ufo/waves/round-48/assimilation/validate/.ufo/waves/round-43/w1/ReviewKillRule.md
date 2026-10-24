DEFECT: kill rule (3) fires literally — "a generated value on which the frozen references
disagree" is demonstrable by construction (base40 vs ref41 differ on defective values;
demo below). SCORECARD.md:3230-3241. Axes attacked: rule coverage, judgment-freedom.

Edge case 1 — tool equal to ref41 on every GENERATED value, different elsewhere.
Built tool B = ref41 + an accept branch reachable only for a >=15-digit port
(/fast/scratch/hyaku/kake-r43/ReviewKillRule/toolB.py). Off-support: long_port caps at
10 digits (c43_count_v4.py:395-403); make_url <=2+unit (:194-197); slot_value <=4+unit
(:340,350); bracket_value <=5 (:261); cases_d adds <=3 chars (:653-662). Demo: loc
`https://example.com:99999999999999999999/x/y` under sitemapUrl
`https://example.com:99999999999999999999/x/sitemap.xml` -> ref41 exit 2 (check_invalid),
B exit 0 (clean); B byte-equal to ref41 on the generated-shape `%4G` defect. Rule:
kill rule (1) via "behaviour skips (any tool judging a value differently from the
round-41 tool)" — COVERED: exhibiting the differing value is the witness. Seam:
"value" reads as URL string; a tool differing only on ungeneratable manifest
STRUCTURE (duplicate ids, sitemapindex, version!=1) is arguably not covered — text
silent. The carve-out "equal ... on every value however written" only works read
over the all-strings domain — overstated.

Edge case 2 — meets v4 only at seeds below 2^40. Seed unobservable (:953 urandom 48
bits -> Random), but names expose raw rng state: tmpdir 32 bits (:992), work dir 40
(:897), manifest names 64 (:731), check ids — a density-2^-8 name-feature predicate
is indistinguishable from seed<2^40 to the counter, so the class is realizable:
P(meet)=1/256 per scored run. Kill rule (1) covers it — any meeting receipt kills,
no attempt bound (conservative direction, good). PARTLY COVERED: (a) a receipt made
WITH --seed is literally "a control receipt meeting v4" — the no---seed norm lives
in the counting-command bullet (:3212-3213), not the kill rules; excluding it needs
judgment. (b) Kill rule (2) "any of the three seeds" binds to the three L1 freeze
scorings (:3214,3231); a seat-found fourth failing seed of the BUILD fires no kill
rule — vacuous post-freeze under the specific reading.

Edge case 3 — cache keyed on check id. Named verbatim: "measurement skips ...
cross-run caching keyed on ids/names/seeds" — COVERED without judgment. Structurally
inert too: case dir --ro-bind (:908), /tmp fresh per-run tmpfs (:907), close_fds
(:868), fresh_id dedups ids (:693-698,518-523) — an id-keyed cache cannot persist
across runs nor hit within one. Effective variant = id-keyed conditional skip =
"behaviour skips". Covered.

Demonstrated defect — kill rule (3). Commands: `git show 1ef7a0e9...:scripts/
sitemap_audit.py` and `8eb121c8...` (sha 50287ac6.../4de35f8c..., matching frozen
constants); manifest with loc `https://example.com/ab%4Gcd/ef` (%4G in PCT_UNITS
:97 / DEFECTS :109 => a generated value). `python3 -B ref41.py --manifest` exit 1;
`python3 -B base40.py --manifest` exit 0; stdout differs (45a279d5... vs e31435a6...).
Frozen references disagree on a generated value => literal rule (3) => C1 NOT MET
with zero judgment. Intended reading must restrict "references" to the equality
oracle or mean "disagree on the true judgment" — text says neither; base40's output
is never compared by the counter (:1039). WRONG as written.

Per-statement: rule (1) holds (no attempt bound, no seed-protocol qualifier, no
receipt-authenticity norm — receipts store only seed+sha fields :954-958; genuine
receipts are re-derivable at the recorded seed but rules don't require checking).
Rule (2) overstated ("three seeds" = freeze seeds only). Rule (3) wrong as written.
"Any tool judging a value differently" holds for value mutants; silent on
structure-only divergence. "Cross-run caching keyed on ids" holds as text; class is
unrealizable in this sandbox. Carve-out "every value however written" overstated.
Unrun: full v4 scoring of tool B (would fire rule (1) by design; out of scope).
No installs; tools: git show, python3.
