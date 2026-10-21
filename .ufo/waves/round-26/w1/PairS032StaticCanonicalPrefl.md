# Pair S032 × corpus/knowledge/static-canonical-preflight.md — r26 freshness recheck (2026-10-21)

Evidence base: re-fetched bytes retained today under `.ufo/waves/round-26/fetched/`: `text/S032-1.txt` (fetchIndex 1; https://www.rfc-editor.org/rfc/rfc3339.txt; fetchedAt 2026-10-21T15:10:51.912841+00:00; 29,786 bytes, all ASCII, one line; text sha256 ba73293a…). The manifest row S032 (index 1) and `population.json:720-739` agree on URL, fetchedAt and raw sha256 (9ab2b886…). Every quote was located by exact substring match in that text file today; offsets are character indices into it. Entry lines come from `corpus/knowledge/static-canonical-preflight.md` (180 lines; tag 8B13). Superseded-status checks used public RFC Editor info pages for RFC 3339 and RFC 9557 (documentation reads, not retained; marked [RFC3339 page] and [RFC9557 page], not S032 bytes). No S032 re-fetch, no build/test/lint, no corpus edits, no tools installed or updated.
Page links for the [RFC3339 page] and [RFC9557 page] labels: https://www.rfc-editor.org/info/rfc3339/ and https://www.rfc-editor.org/info/rfc9557/ (read 2026-10-21).

## Statements attributed to S032

| # | file:line | Statement | Verdict | Verbatim quote from S032-1.txt | Anchor observed now | Reason |
|---|---|---|---|---|---|---|
| 1 | corpus/knowledge/static-canonical-preflight.md:159 | "Sources: S032 (RFC3339 §5.6–5.7) … all opened this round." | HOLD | "5.6. Internet Date/Time Format The following profile of ISO 8601 [ISO8601] dates SHOULD be used in new protocols on the Internet." / "5.7. Restrictions The grammar element date-mday represents the day number within the current month." | §5.6 heading at char 14397; §5.7 heading at char 16005 (TOC entries at chars 1704 and 1766) | Both anchors exist under the titles the SOURCES S032 row gives. §5.6–5.7 are not among the sections RFC 9557 revises (see Supersession). "Opened this round" dates the round-24 opening (2026-10-21, entry :157) and is accurate as a record. |
| 2 | :159 | "The former lexical timestamp prefix comparison accepted malformed and future strings." | HOLD (scope: malformed) | "5.7. Restrictions The grammar element date-mday represents the day number within the current month." | §5.7 heading at char 16005; maxima table follows | S032 supports calendar-based malformation (day-of-month limited by month and leap year). "Future strings" is lane bounds policy, not an S032 claim, and is not judged here. S032 never mentions prefix or lexical comparison, so that critique is the lane's inference, not S032's teaching. |
| 3 | :173 | "c1 observedAt permits RFC3339's full-date production as well as date-time, preserving historical date-only observations." | HOLD | "full-date = date-fullyear "-" date-month "-" date-mday" | §5.6 ABNF, char 15033 | The production exists unchanged. S032 §2 defines a timestamp as an instant: "Timestamp This term is used in this document to refer to an unambiguous representation of some instant in time." (char 5696). Date-only support is therefore lane policy, as the same bullet states (row 6). |
| 4 | :173 | "c2 fetchedAt requires date-time with offset." | HOLD | "full-time = partial-time time-offset date-time = full-date "T" full-time" | §5.6 ABNF, char 15088 | full-time requires time-offset, so date-time requires an offset. RFC 9557 §4.1 imports date-time unchanged, and its §2.2 keeps Z as an offset [RFC9557 page]. |
| 5 | :173 | "Values are parsed, not prefix-compared: real calendar/clock fields, ASCII digits, …" | HOLD (ASCII part outside S032) | "The maximum value varies based on the month and year as follows:" | §5.7 maxima table at char 16105; §5.6 field ranges from char 14397 | Calendar and clock limits are in S032: date-mday by month and year; hour 00-23; second 00-58/59/60. The ASCII qualifier rests on the ABNF DIGIT, which S032 defers to ABNF: "This is specified using the syntax description notation defined in [ABNF]." (char 14527). RFC 9557 §4.1 imports DIGIT from RFC 5234 Appendix B.1 [RFC9557 page]. RFC 5234 is outside the population and was not read, so the ASCII part is not decided here. The UTC-bounds clause in the same sentence is lane policy (excluded). |
| 6 | :173 | "Date-only support and the bounds are lane policy, not an assertion that RFC3339 date-time is date-only." | HOLD | "full-time = partial-time time-offset date-time = full-date "T" full-time" | §5.6 ABNF, char 15088 | S032's date-time requires a full-time, so a date-only value is not an RFC 3339 date-time. The entry makes no such assertion and labels date-only support as lane policy. |
| 7 | :173 | "Runtime-supported calendar/seconds are the local profile; leap-second spellings are not evaluated as valid instants." | HOLD | "The grammar element time-second may have the value "60" at the end of months in which a leap second occurs" | §5.7 leap paragraph, char 16537 | S032 permits "60" only in leap-second months, so a local profile that does not evaluate such spellings narrows the RFC and says so. The §5.7 "to date" month list is a 2002 snapshot in the cited anchor; the entry does not cite it (see Supersession). |

### Excluded (no S032 attribution)

- :1-2 `source:` and `verified-at:` headers cover S020-S029 only. S032 is not attributed there (S030-S031 and S033-S034 are also absent). Not an S032 verdict.
- :134 `fetchedAt` is a receipt field name in the live-snapshot section; it cites no source.
- :140 and :143 `[r23-correction]` tags cite S021 and S025 only.
- :159 S033/S034 clause and the untyped Content-Type sentence; :174-176 cite S033/S034 or local policy.
- :169-172 and :177-180 (round-24 reader, commands, historical counter) cite no S032.
- :173 "UTC lower bound 2026-10-21 and no later than the revision's committer instant (UTC date for date-only observations)" is lane policy with no S032 reliance.

## Correction tails and appended sections

- No `[r20-correction]` tail exists in the entry. A search for `r20`, `round-20`, `round 20` and `correction` finds only the round-23 heading (:96) and the `[r23-correction]` tags (:140, :143). The assignment's r20 reference has no match in the current bytes, so nothing is judged against it.
- The only later appended section with S032 reliance is "Receipt replay hardening — round 24 (2026-10-21)" (:157-180). Its only S032 lines are :159 and :173.

## Version/date/anchor supersession scan

- RFC Editor info page for RFC 3339: "This RFC was updated, see RFC 9557." [RFC3339 page]
- RFC 9557 (Proposed Standard, U. Sharma and C. Bormann, 2024-04-26), abstract: "It updates RFC 3339 in the specific interpretation of the local offset Z, which is no longer understood to" [RFC9557 page]. Its §2.2: "This specification updates Section 4.3 of RFC3339" (links stripped) [RFC9557 page]. The §4.3 text it revises is in S032-1.txt at char 8919 ("4.3. Unknown Local Offset Convention"); the RFC 3339 sentence at char 9078 reads: "This differs semantically from an offset of "Z" or "+00:00", which imply that UTC is the preferred reference point for the specified time."
- The cited anchors are not superseded. RFC 9557 §4.1 imports "date-time and time-numoffset" from RFC 3339 §5.6 unchanged [RFC9557 page]. The "updat" hits in that page name the abstract, §2 (§2.2 names §4.3), §3.4, and the time-zone sense of "updates"; none names §5.6 or §5.7. Rows 1-7 rely on text that stands.
- Flag, not STALE: the RFC 3339 version named at :159 and :173 (rows 1, 3 and 6 name it; row 4 relies on the same grammar) is partly superseded at §4.3, which no row cites.
- Dated text inside the cited anchor: §5.7 "to date: June (XXXX-06- 30T23:59:60Z) or December (XXXX-12-31T23:59:60Z)" (char 16647) is a July 2002 snapshot, and §5.7 itself says "Leap seconds cannot be predicted far into the future." (char 17084). Row 7 relies on the "60" grammar, not on the list. Flag only.
- Errata: none shown on the RFC 3339 info page as read.
- Dated references: "all opened this round" (:159) means round 24 (2026-10-21, entry :157). SOURCES.md:40 records "opened 2026-10-21" with freshness 365d. Current.
- SOURCES.md:40 (S032 row): teaching and anchor match the entry and the re-fetched bytes. Its used-by also lists `corpus/lessons/round-24.md`, which is outside this pair.

## Verdict

- Statements attributed to S032: 7 (:159 ×2, :173 ×5). HOLD 7, STALE 0.
- No anchor moved, no quote failed, no cited date is superseded.
- Superseded flag: RFC 3339 is partly superseded at §4.3 by RFC 9557 (uncited by this entry). Rows 1, 3 and 6 name RFC 3339 and are affected by the version flag only, not by the verdict; row 4 relies on the same grammar. Row 7's anchor (§5.7) carries the dated "to date" list, but row 7 does not rely on it.
- Corrections: none required, because nothing is STALE. Optional disclosure, not counted, for L1 if the version flag should appear at :159 and :173:

> [r26-recheck S032 disclosure] RFC 3339 §4.3 was revised by RFC 9557 §2.2 (2024-04-26) so that an unknown local offset is written Z. Sections 5.6 and 5.7 are imported unchanged (RFC 9557 §4.1); the statements above depend on neither §4.3 nor the Z interpretation.

## Residual risk and gaps

- The ASCII qualifier in row 5 depends on RFC 5234 Appendix B.1, which is outside S032 and the population and was not read.
- Superseded-status checks used RFC Editor info pages (public documentation), not retained bytes. RFC 9557 quotes are not S032 quotes.
- The raw `S032-1.raw.gz` was not decompressed. Raw digest 9ab2b886… comes from manifest.json and population.json:736, which agree. All quotes use the text view, as the contract requires.
- The round-26 count (`measure.py`) was not run; it belongs to L1.

## Verification log

- Exact substring match (Python `in`) of every quote against `fetched/text/S032-1.txt` (sha256 ba73293a7503a1c2182158199c2922247fa88be6e01601ff5b4fa38d0959b4a0): 11 quotes, all FOUND, 7-21 words each. Offsets: 14397, 16005, 15033, 15088, 16105, 16537, 14527, 5696, 9078, 17084, 16647.
- Tooling: none installed or updated. No builds, tests or linters run.

```json
{"pair":"S032xstatic-canonical-preflight","statements":7,"hold":7,"stale":0,"corrections":[]}
```
