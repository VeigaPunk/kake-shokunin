# ConnectSiblingOverlap — sibling-overlap scan for C1 and C2 (round 30, wave 1)

Read-only seat. Axes: operability (C1) and freshness (C2). No lane file was edited apart from this report. I made no network request and installed nothing.

## Verdict
- C2: no sibling lane holds any Render knowledge, so there is nothing to conflict with. The only conflict risk is inside kake: its existing Render text describes app.ds4cc.com as a Docker web service, not a static site.
- C1: no sibling entry conflicts with the interface contract. Five siblings already implement strict JSON with an `object_pairs_hook` and `parse_constant`, which is a reusable pattern. However, the contract and the counter leave four gaps open: overflow to infinity, the regex anchor, option abbreviation and precedence between two defects. Each gap is shown below by a probe.

## C2 — Render overlap
- Sibling search, case-insensitive, for `render.com|onrender.com|render.yaml|render static site|render web service` across all 20 sibling `*-shokunin` trees. It excluded `.git`, `node_modules`, `*.gz`, `*.jsonl` and files over 2 MB. Exit 0, zero files.
- A narrower search over sibling `corpus/knowledge`, `SKILL.md`, `scripts` and `tools` (adding `_redirects` and `_headers`) returned only unrelated `end_headers`/`*_HEADERS` hits, for example tabi-shokunin/corpus/knowledge/network-evidence-rung.md:573. There were no Render hits.
- The source ids S049-S052 are free in corpus/SOURCES.md, whose last row is S048 at line 56. corpus/knowledge/freshness-pins.json contains no Render host.
- Kake's own Render surfaces that the new entry must not contradict:
  - corpus/knowledge/publish-channels.md:24-28 (`## Render — app.ds4cc.com`, a Docker web service, `ds4cc-marketplace-app`)
  - SKILL.md:28 and SKILL.md:427 (property map: "Render web service ... Docker")
  - corpus/knowledge/fleet-registry.md:13-14 ("app.ds4cc.com is NOT a registry row ... do not add it here")
  - publish-channels.md:3, which says the dependent Render claims need operator re-derivation.
- Conflict criteria for `corpus/knowledge/render-static-sites.md`. No draft exists yet: none in the lane, and none at `/fast/scratch/hyaku/kake-r30/w1/*/clone/corpus/knowledge/render-static-sites.md`.
  1. It must not imply that app.ds4cc.com is a Render static site, or that static-site semantics apply to it. These include atomic per-push builds, CDN invalidation, `_redirects`/headers rules and custom-domain flow; S049-S052 cover the static-site service type only.
  2. It must not add app.ds4cc.com or any Render host to fleet-registry.md or freshness-pins.json.
  3. It should say that the entry is vendor documentation (S049-S052) and not a live check of any owned property. That keeps the owned-site bound intact.
  4. Any cross-link to publish-channels.md should carry that file's re-derivation caveat (line 3) and not restate its claims as current.

## C1 — reusable sibling patterns (path:line)
- mado-shokunin/tools/mado-evidence-audit.py:29-53 is the most complete pattern. It has a pairs hook, a `parse_constant` that raises, and a post-parse iterative `finite()` walk that also catches overflow such as `1e400`.
- Hook plus constant without overflow handling:
  - mado-shokunin/tools/mado-action-plan.py:187-212, with fixtures `plan-duplicate-key` and `plan-nonfinite` at :614-619
  - mado-shokunin/tools/mado-tripwire.py:3234-3238 and :3467-3468
  - mori-shokunin/tools/mori-round16-regressions.py:218-227
  - mori-shokunin/tools/mori-journal-window.py:87-88
  - game-dev-3d-shokunin/corpus/artifacts/unreal-r22/verify_descriptor.py:22
- kagi-shokunin/corpus/feature-claims.py:191-305 has a distinct `FC-JSON-DUPLICATE-KEY` code. Nonfinite values fold into `FC-JSON-INVALID` (:200 raises a bare ValueError, caught at :306).
- mado-action-plan folds both defects into `plan_malformed`. No sibling has a distinct nonfinite reason code, so kake's contract is stricter than any sibling. Copy the mechanics, not the codes.
- Comparing a multiset of pairs: souji-shokunin/census/round-17/gate-replays.py:165-189 sorts (id, path) pairs and compares them with `Counter`. It also reports `missing`/`extra` differences. That shape fits the runner's (id, reason) comparison with null for a missing reason, and makes failure output readable.
- Mutant ledgers, as form models only (none covers JSON reason codes):
  - mado-shokunin/SKILL.md:622 (`measure-mutants.json`, bites/no_bite)
  - kama-shokunin/SCORECARD.md:1166 and :1260 (named-row kills, survivors listed)
  - tameshi-shokunin/corpus/QUALITY.md:123
- Siblings that rely on last-wins duplicates (game-dev-2d r73/r74 scribe tables, kagi op-ref-consumption.md:53, chousa metadata-screen-r25.md:122) are not about JSON gates and do not conflict.

## C1 — contract gaps proven by probe (Python 3.14.8)
1. Overflow. `json.loads('{"rows":[{"id":"S001","w":1e400}]}', object_pairs_hook=..., parse_constant=...)` returns `inf` (and `-1e400` returns `-inf`) without calling `parse_constant`. A gate that follows the contract literally ("NaN, Infinity or -Infinity") accepts a document that holds a non-finite value. The counter's F02 tests only the three literal tokens (c1_reason_count.py:281), so such a gate still scores 14/14. **Contradiction for the L1:** under RFC 8259, `1e400` is valid JSON grammar, yet it decodes to a non-finite value. Pick one policy and state it.
2. Precedence between two defects. Hooks fire when an object closes, but `parse_constant` fires on the token. Results:
   - `{"a":1,"a":2,"b":NaN}` gives nonfinite, even though the duplicate comes first.
   - `{"o":{"k":1,"k":2},"z":NaN}` gives duplicate.

   Because the runner compares (id, reason) pairs exactly, a fixture that carries both defects pins decoder internals. Keep one defect per fixture, or write the precedence rule into the contract.
3. Exception class. `InputInvalid` subclasses `Exception` (citing_set.py:138), and `load_json_document` catches `ValueError` as `document_not_json` (:417-419). If hooks raise `ValueError` the way mado and mori do, both new codes silently become `document_not_json`. They must raise `InputInvalid` (or a non-ValueError type), or be caught before `ValueError`.
4. Id anchor. `re.match(r'^S[0-9]{3,}$', 'S001\n')` returns True, but `re.fullmatch(r'S[0-9]{3,}', 'S001\n')` returns False. Python's `$` also matches before a trailing newline, and the scanner token at citing_set.py:126 never equals `"S001\n"`. Use `fullmatch` or `\Z`.
5. Option abbreviation. With argparse's default `allow_abbrev=True`, `--population a --pop b` parses as `population='b'` (probe). F04 tests only the four full names, so an argv string scan for `--population`/`--population=` scores 14/14 and still lets `--pop b` win silently. I found no abbreviated use of the gate anywhere in the lane (search over the lane for `citing_set.py ... --<prefix>`, zero hits).
6. Escaped duplicate keys. `{"a":1,"\u0061":2}` is caught by the hook, because keys arrive decoded. This is worth one fixture, since a raw-text duplicate scan would miss it.

## Proposed move (one, bounded; the L1 decides)
Create a single strict loader in `load_json_document`, modelled on mado-evidence-audit.py:29-53:
- The pairs hook raises `InputInvalid("document_duplicate_key")`.
- `parse_constant` raises `InputInvalid("document_nonfinite_number")`.
- An iterative post-parse finite walk raises the same nonfinite code, if the L1 extends the contract to cover overflow.

For repeated options, use one argparse `Action` that raises a usage error on the second assignment. This covers `--x v`, `--x=v` and abbreviations in one place. Validate ids with `re.fullmatch`.

Add these fixtures, each with one defect and object-form expected entries:
- the escaped duplicate key
- `1e400` (only if the policy is adopted)
- `S001\n` as an id, giving `population_id_unreachable`
- `--pop` repeated against `--population`, giving exit 64

Affected axes: operability improves; freshness is untouched. Risks:
- Rejecting `1e400` goes beyond the declared contract text. The L1 must either amend the contract or drop that fixture.
- Changing `allow_abbrev` instead of adding the `Action` would turn a single `--pop x` into exit 64, which is a behaviour change. The `Action` avoids that.

## Commands run (exit codes)
- `ls -d /home/vgpnk/Projects/shokunin/*-shokunin`: exit 0 (21 lanes).
- Per-lane `rg -in 'duplicate[_ -]key|object_pairs_hook|parse_constant|nonfinite|non-finite|allow_nan'` (excluding `.ufo`): exit 0.
- Per-lane `rg` for `parse_float|isfinite(` in the sibling tools: exit 0; one hit, mado-evidence-audit.py:42.
- The two Render searches described above: exit 0, no Render hits.
- Whole-tree search per sibling lane, `rg -il --hidden -g '!.git' -g '!node_modules' 'render\.com|onrender\.com|render static|static site.*render|render.*static site|render\.yaml'`, with no size or type exclusions (so it covers `.ufo`, `*.jsonl` and large files): finished after 75 s with no output, so zero files. Its stderr went to `/dev/null`, so an unreadable file would not have been reported.
- Per-lane `rg -l '"reason"'` over `expected.json`, and the mutant-ledger search: exit 0.
- Decoder probe and regex/argparse probe, run in the sandbox with `TMPDIR=/fast/scratch/hyaku/kake-r30/w1/ConnectSiblingOverlap/tmp`: exit 0, outputs as quoted above.

## Not verified
- I did not run the C1 or C2 counters, the gate or the runner. I did not see the drafted Render entry, because none existed at scan time.
- The fleet repository root was not scanned; only `*-shokunin` lanes were.

Artifacts: sandbox `/fast/scratch/hyaku/kake-r30/w1/ConnectSiblingOverlap/tmp` (empty TMPDIR). This report is the only deliverable.
