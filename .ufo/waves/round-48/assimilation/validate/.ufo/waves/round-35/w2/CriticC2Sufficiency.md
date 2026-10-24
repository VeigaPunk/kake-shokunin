# CriticC2Sufficiency — attacks what C2's `met` proves: can a cheaper entry, written without this round's primary sources, reach `met`?

Verdict: yes. `met` does not require this round's primary sources. An entry written from the public topic list
with no source text opened scores 11 of 12 probes. One added line naming three landed row ids makes it
`met` true (counter exit 0). The probes do reject the two secondary sources on their own: S081 gives 1 of 12
and S079 gives 5 of 12. So C2 proves the stated facts are present, but it does not prove they came from S078–S085.

## Method (sandbox only; nothing in the lane changed except this report)
- Clone `/fast/scratch/hyaku/kake-r35/w2/CriticC2Sufficiency/clone` at `7deacc46`. Each branch is one commit on 7deacc46. It removes
  `.ufo/waves/round-35/sealed/`, because the counter exits 2 when a key is visible (`sealed_count.py:300-302`). Where an entry is
  scored, it replaces `corpus/knowledge/security-txt-publishing.md`. Landed SOURCES rows and retained texts are unchanged.
- The entries were written and committed before I opened `c2-probes.json`. I did not read the landed entry.
- Counter: lane `.ufo/waves/round-35/sealed_count.py`, sha256 `1b4d9d59…3469b` (version 2), run as
  `timeout 60 python3 -B <lane>/.ufo/waves/round-35/sealed_count.py c2 --root <clone> --revision <branch> --key-revision 4c6be2bdec5630166c4013e53c226b1119ec63cc`.
- Entries: `/fast/scratch/hyaku/kake-r35/w2/CriticC2Sufficiency/entries/{A-s081-only,B-topic-list-no-source,C-s079-only}.md`.
  Score JSON: `.../CriticC2Sufficiency/scores/<branch>.json`. Bundle: `.../CriticC2Sufficiency/c2-sufficiency.bundle`
  (sha256 `52686405…f28d6280`, prerequisite 7deacc46).

## Scores (sealed C2 counter v2)
| Branch | Commit | Exit | met | probes | words | copied | goodCites | failed probes |
|---|---|---|---|---|---|---|---|---|
| landed entry, key removed (reproduces the claim) | 5512f0b1 | 0 | true | 12 | 1388 | 0.0 | 8 | none |
| A: from S081 (Wikipedia) only, cites S081 | 9ae53f32 | 1 | false | 1 | 352 | 0.0 | 0 | P02–P12 |
| B: from public topic list, no source opened, no ids | d055aef3 | 1 | false | **11** | 634 | 0.0 | 0 | P02 |
| C: from S079 (securitytxt.org) only, cites S079 | 119b92ad | 1 | false | 5 | 407 | 0.0075 | 1 | P02 P03 P06 P08 P09 P11 P12 |
| A + line "Registry rows: S078, S082, S083." | 24bd487e | 1 | false | 1 | 357 | 0.0 | 3 | P02–P12 |
| B + the same line | 0b7779dc | **0** | **true** | 11 | 639 | 0.0 | 3 | P02 |
| C + the same line | cce82d39 | 1 | false | 5 | 412 | 0.0074 | 4 | as C |

## Reasons
1. The probes test facts, not where they came from. Entry B passed P01 and P03–P12 from general knowledge of RFC 9116 and
   GitHub Pages: contact order, the key itself kept out of Encryption, subdomains not covered, `include:` and `.nojekyll`,
   and less than a year. The only miss was P02, the rule that the well-known file wins when both locations exist. One more
   sentence would score 12 of 12. All 12 probe facts are textbook RFC 9116 and Jekyll facts
   (`sealed/c2-probes.json:5-103`), and the declaration lists their topics in public (`SCORECARD.md:1398-1401`).
2. The landed rows make `cites` free for any entry at this path. The rows S078–S086 already carry `mined`, `2026-10-22`,
   a retained receipt URL and this entry path in used-by. So `sealed_count.py:261-271` counts any S078–S099 id the entry
   merely names. One line moved B from `cites` false to `met` true. That is sharper than the disclosed limit at
   `SCORECARD.md:1491-1494`: it needs no junk rows at all, only the honest landed ones.
3. `copied` cannot catch this. An entry written from memory shares no 8-word shingles with the retained texts (B: 0.0).
4. Secondary sources alone do fail. S081 covers only the location (1 of 12). S079 adds Contact required, Expires used once,
   ISO 8601 and OpenPGP cleartext signing (5 of 12), and it misses utf-8, the one-year bound, contact order, the key
   itself, scope and the GitHub Pages path. So reaching `met` takes RFC 9116 and GitHub Pages content. That content is
   in S078/S006/S080/S086, but it is equally available from prior knowledge.
5. Confirmed part: the landed entry reproduces `met` true with 12 of 12 at 5512f0b1. The "≥ 9 of 12 from the pinned
   source set" claim stands as measured. Only the reading "grounded in rows opened this round" (`SCORECARD.md:1376`) is
   stronger than what `met` shows.

## Impacted axes
freshness: C2 is a "sourced learning claim on new ground", and `met` is reachable with zero sources opened.
Provenance is carried only by the non-author read of the entry and the rows. Operability is not touched.

## Smallest safe correction
Do not change the counter after measurement. Narrow the wording of what `met` shows in SCORECARD measured results and
the lesson: "the entry states 12 of 12 sealed facts and names good rows; provenance from S078–S085 is not measured."
Keep the closure's per-claim source check as the provenance gate. For later rounds: seal at least two probes on facts
found only in this round's opened texts, such as S083's registration date 2021-07-13 or S084/S085's served Expires
values, so that an entry written from memory cannot pass them.

## Limits and what I did not verify
- Contamination of B, disclosed. Before writing B, I had read S079 and S081 for entries A and C, and my first grep of
  `corpus/SOURCES.md` showed the row summary cells (truncated to 768 bytes). They name Contact required, Expires at most
  once, less than a year, text/plain utf-8 (S078 row), dotfile exclusion (S006) and `.nojekyll` (S086). So B is really
  "topic list plus landed registry summary cells, no source text opened". That is still a cheaper path than this round's
  primary reads. P08, P09 and P11 appear in none of what I saw. A clean-room writer who has seen no row is still owed;
  as a leaf I could not dispatch one.
- I did not check that B's sentences are true. Its claim that Actions artifacts drop dotfiles is hedged and unchecked,
  and the counter does not test truth.
- No network, no tool installs, no pacman. I did not measure probe leniency or counter trust; those are other seats' items.
