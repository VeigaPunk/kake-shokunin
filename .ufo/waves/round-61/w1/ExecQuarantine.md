# ExecQuarantine

Round-61 w1 (build) · lane kake-shokunin · seat leaf · access date 2026-10-27 (UTC) · base `9f07731a873585e655a6518233ea39f5d9fb8204`.

Scope: re-derive the kake quarantine slice from the §10 contract command, byte-compare it against the round-60
record and the round-58 derivation, write the slice to `.ufo/waves/round-61/assimilation/quarantine-slice`. Two
things were deliberately not done: no URL of the 12 rows was re-opened this round (the verdict per row stays as
previously recorded), and nothing was appended to `corpus/SOURCES.md` or to any registry.

## SLICE:

Register (read-only, unmodified): `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`,
sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, 83621 bytes, mtime 2026-10-24 08:37:00 -0300.
Command run verbatim:

```
awk -F'|' -v l='kake' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R"
```

Result: **12 data rows**, 453 bytes, 12 lines, sha256
`6d92f4408c7482e59fb93c2085676f7d9c4fedb687bcfd501060f63c15d2d63a`. Class split 9 `payload-absent` + 3
unfetchable (`the cited source could not be fetched, so no quote was checked`), matching the register's own
aggregate row at line 242 (`| \`kake\` | 9 |`), which the awk excludes because it carries no round and no S-id.

Head (first four lines, whitespace shown as derived, each line has one trailing ASCII space before the newline):

```
 S142   `payload-absent` 
 S143   `payload-absent` 
 S148   `payload-absent` 
 S156   `payload-absent` 
```

Per-row derivation (id, register round, class, cited URL, register line):

| id | round | class | cited URL | line |
|---|---|---|---|---|
| S142 | round1 | `payload-absent` | https://www.kimi.com/help/websites/websites-faq | 83 |
| S143 | round1 | `payload-absent` | https://developer.chrome.com/docs/crux/methodology/tools | 84 |
| S148 | round1 | `payload-absent` | https://arxiv.org/abs/2308.06409 | 85 |
| S156 | round2 | `payload-absent` | https://kimi.page/ | 86 |
| S161 | round3 | `payload-absent` | https://developers.google.com/crawling/docs/crawlers-fetchers/reduce-crawl-rate | 87 |
| S193 | round6 | `payload-absent` | https://github.com/VeigaPunk/kake-shokunin.git | 88 |
| S194 | round6 | `payload-absent` | https://github.com/VeigaPunk/kake-shokunin.git | 89 |
| S195 | round6 | `payload-absent` | https://github.com/VeigaPunk/kake-shokunin.git | 90 |
| S206 | round7 | `payload-absent` | https://github.com/VeigaPunk/kake-shokunin.git | 91 |
| S154 | round2 | unfetchable | https://chromeuxreport.googleapis.com/v1/records:queryRecord | 319 |
| S178 | round4 | unfetchable | https://www.googleapis.com/pagespeedonline/v5/runPagespeed | 320 |
| S184 | round5 | unfetchable | https://chromeuxreport.googleapis.com/v1/records:queryRecord | 321 |

Two register-side shape facts are carried, not fixed (the register is read-only to this lane and the slice must stay
byte-stable): the three unfetchable rows put the S-id in the class column with a stray backtick (`S154\``, `S178\``,
`S184\``), so `$4` = `S154\`` and `$5` = the prose note; and the same ids exist as *other-lane* rows elsewhere in
the register (e.g. line 205 `tabi | round3 | S154 | payload-absent`, line 339 `kumitate | round8 | S178`), which the
lane-anchored `$2` predicate correctly excludes.

Every line carries exactly one S-id: verified per line on the written file — 12/12 lines, one `S[0-9]+` token each
(evidence block `## per-line S-id presence`).

## BYTE-COMPARE:

- `cmp` round-61 slice vs `.ufo/waves/round-60/assimilation/quarantine-slice` → **exit 0** (byte-identical).
- `cmp` round-61 slice vs `.ufo/waves/round-58/assimilation/quarantine-slice` → **exit 0** (byte-identical).
- Extended to the intervening records, all **exit 0**, all sha256 `6d92f440…d2d63a`, all 453 bytes / 12 lines:
  round-55, round-56, round-57, round-58, round-59, round-60.
- The round-60 record is also named by that round's own seat, `.ufo/waves/round-60/w1/ReviewerQuarantineHold.md`
  (12 rows, "byte-identical … to both round-60 and round-59", same sha), and its `.files/slice-sha256.txt` carries
  the identical digest.
- Round-58 derivation: `.ufo/waves/round-58/w1/ScoutQuarantine.md` ("12 rows; `cmp` … byte-identical") and
  `w1/ReviewerAssimPlan.md` check 9 (same 12 ids, same class split) agree id-for-id with this derivation.
- Register unchanged across the derivation: sha256 identical before and after; nothing in `/home/vgpnk/Projects/shokuknow`
  was written.
- No row of the slice is a registry row at the measured base: `grep -c "^| <id> "` is 0 for all twelve ids in
  `corpus/SOURCES.md` (167 rows at base), so nothing from the slice is adopted or appended and the append-only
  registry is untouched by this seat.

Evidence (generated, not hand-typed): `w1/ExecQuarantine.files/compare-r61.txt` (register sha, verbatim command,
per-row table with register line numbers, all `cmp` exits and digests, per-line S-id check, SOURCES.md check, the
still-open L0 row) and `w1/ExecQuarantine.files/quarantine-slice.r61` (byte copy of the derived stream).
Written record: `.ufo/waves/round-61/assimilation/quarantine-slice` (slice only, 12 lines, no notes appended — see
below).

Design note: the record file carries the slice and nothing else so the next round's byte-compare stays meaningful
(R60-D5 requires "re-verified byte-identical"); comparison notes therefore live in this report and in `.files/`
rather than in the record.

## VERDICT:

All 12 rows (S142 S143 S148 S154 S156 S161 S178 S184 S193 S194 S195 S206) held as previously recorded, re-derived
byte-identically to rounds 55–60, no URL re-opened, nothing appended — `Assimilation: none` stands.
VERDICT: quarantine slice re-derived = 12 rows, byte-identical to the round-58/59/60 records (sha256 6d92f440…d2d63a, 453 bytes, 12/12 lines carry an S-id); all held, no URL re-opened, nothing appended.
