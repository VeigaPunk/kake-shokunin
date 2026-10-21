# Rejection12S027 — falsify L1's rejection of the S027 version-label/date STALE

Milestone: r26-recheck-falsify. Axis: freshness. Candidate e28312b, base 97404de.

## Verdict: AGREE (the rejection is correct; it hides no staleness)

The seat finding was a STALE verdict on line 2 of the static-canonical-preflight entry, `verified-at: 2026-10-20 (S020-S027)`, and on the "Python 3.15" label. Neither statement is wrong at its own stated scope. Every teaching that depends on S027 still holds on the retained 2026-10-21 bytes and on a Python 3.15 runtime.

## Attack 1: was the date or label false at its stated scope? No.

- Scope of the date. Base `corpus/knowledge/static-canonical-preflight.md:2` reads "verified-at: 2026-10-20 (S020-S027) … documentation opened this round". It is scoped to round 22. `git log -S'verified-at: 2026-10-20 (S020-S027)'` gives `c0fd6d5 2026-10-20 18:30:55 -0300 round-22: offline canonical publishing preflight`, so the date matches the commit that recorded the opening.
- Scope of the label. Base `corpus/lessons/round-22.md:52-53` says "The Python URLs opened as Python 3.15 documentation; that version labels the documentation, not the installed runtime". The label names the 3.15 family.
- What the page said at base time. Base `.ufo/waves/round-22/w1/PythonURL.md:12-13` records "3.15 page title: `Python 3.15.0 documentation`" and "`/3/` alias … Serves the 3.15 page today … title 3.15.0". The 2026-10-20 reading was therefore 3.15.0, inside the 3.15 family. The seat report said "No 2026-10-20 S027 bytes are retained", but this in-lane record covers the gap. It also supports the candidate lesson's "3.15.0→3.15.1" wording (`corpus/lessons/round-26.md:58`).
- Current bytes. `fetched/text/S027-1.txt` starts "urllib.parse — Parse URLs into components — Python 3.15.1 documentation", with the footer "Last updated on Oct 21, 2026 (13:02 UTC)." at offset 30245. That is a patch bump within the same family.
- Rule. `corpus/QUALITY.md:217-221` says "A historical verified-at date, … or a patch-version label in the same documented family is not a stale claim; record it as a note. A statement whose attribution was false even at its base revision is STALE." The attribution was true at base, so the second sentence does not apply. The ledger rule in `statements.json` agrees: "Historical dates and base-scoped pointers are not stale."

## Attack 2: does 3.15 or 3.15.1 change any teaching that relies on S027? No.

- Every "Changed in version 3.15" note in the retained text (offsets 8013, 12539, 14100 and 16323) only adds parameters: `missing_as_none` and `keep_empty`. None changes validation behaviour, netloc detection or urljoin semantics.
- The anchors relied on are each present exactly once:
  - "does not perform validation" at offset 7285;
  - "cannot be claimed compliant" at 17819;
  - "urlsplit() recognizes" at 4054;
  - "attacker-controlled" at 15253.
- The seat checked the urljoin behaviour behind entry lines 85-86 only on Python 3.14.8. I re-ran it on the documented 3.15 family with `~/.local/bin/python3.15` (Python 3.15.0, built Oct 9 2026). The result is unchanged:
  - `urljoin('https://example.test/project/b.html','///project/a.html')` returns `'https://example.test/project/a.html'`;
  - `urlsplit('///project/a.html')` returns `SplitResult(scheme='', netloc='', path='/project/a.html', query='', fragment='')`.

  No 3.15.1 runtime was available. The retained 3.15.1 page has no urljoin change note.

## Attack 3: was the rejection dropped without a record? No.

- `statements.json` S027 has `stale: 0`, with l1Disposition "version label/date only; relied-on warnings unchanged (note in S026 block)."
- The candidate entry's S026 bullet says "The page now labels itself Python 3.15.1 documentation (S026 and S027 alike); the 3.15 family and the relied-on sentences are unchanged."
- The SOURCES.md S027 row has recheck cadence `on-release`, and the 3.15.1 release triggered it. The round-26 recheck paragraph in SOURCES.md records the re-fetch.

## Observation (advisory, not a defect in the rejection)

The S027 version note sits inside a bullet tagged `[r26-recheck S026 STALE]`. A search for S027 recheck tags finds no S027-tagged line. That is a discoverability gap, not a correctness problem. It does not change counts, because S027 is `stale: 0` and the S026 bullet is the admitted S026 correction. The smallest optional improvement would be a separate untagged "Version note (not STALE): S026/S027 …" bullet, like the existing RFC 9557 note. The rule does not require it.

## Commands and tooling

- Read: QUALITY.md lines 40-84 and 200-224, the S027 seat and row reports, `rechecks/S027.json`, the `statements.json` S026 and S027 rows, the manifest S027 row, and the retained `S027-1.txt` (offset probes in the stdlib).
- Git (read-only): `git show`, `git diff`, `git log -S` and `git grep` at 97404de and e28312b.
- One local stdlib probe with `~/.local/bin/python3.15`. No network access, no writes other than this report, and no round-24 material.
- No tools were installed or updated.

```json
{"target":"S027 L1 rejection (Python 3.15.1 label / 2026-10-20 date)","verdict":"AGREE","severity":"none"}
```
