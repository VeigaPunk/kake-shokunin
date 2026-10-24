# Round 25 packet counter

## Files changed

- `.ufo/waves/round-25/sandboxes/counter/.ufo/waves/round-25/measure.py` — added the revision-bound, offline packet counter.
- `.ufo/waves/round-25/w1/PacketCounter.md` — this scoped implementation report.

## Behavior and usage

The counter resolves a full Git commit hash, reads the candidate packet tool and card corpus from that revision's Git blobs, copies those exact bytes plus the pinned WCAG fixtures into a temporary snapshot, runs the candidate CLI with Python bytecode disabled, and independently computes each criterion's result from the pinned population. It cross-checks the candidate's complete JSON result and exit code, including the fixed 55-row order, accepted total, findings, and `websiteConformance: not-assessed`.

The independent oracle checks exact card keys and metadata, nonempty review prose, status `not-assessed`, and a six-to-25 whitespace-word quote normalized for punctuation spacing and matched at word boundaries within `normativeText`. Unknown extra criteria remain a global failure even if all 55 expected rows are accepted. A missing candidate packet tool reports `accepted: 0`, `expected: 55`, and exits 1; invalid/tampered inputs or a failed cross-check exit 2. The baseline's missing round-25 fixture blobs use only exact-hash local copies of the pinned source inputs; candidate blobs, when present, must match their pins.

Usage:

```sh
python3 -B .ufo/waves/round-25/sandboxes/counter/.ufo/waves/round-25/measure.py \
  --root /path/to/kake-shokunin --revision <full-commit-hash>
```

`--revision` accepts a full 40- or 64-character hexadecimal commit hash. The command prints one JSON object with schema `kake-accessibility-packet-v1`; exit codes are 0 for a clean packet, 1 for absent capability or a structurally failed packet, 2 for unevaluable input/cross-check, and 64 for usage errors.

## Exact retained evidence

- The sandbox checkout reported `HEAD` `6883f1d580d811f7c434d1db4642596362f822b1`.
- The population query returned exactly 55 criterion IDs; population rows have separate `text` and `normativeText` fields. The working pinned population byte digest observed with `sha256sum` is `4751dc24db2e3698c2b276bb81bff57412c8fbf6c1c0a62f1aa2ad9e0f903058`, and its `sourceSha256` is `6e3c5fe397257cae509a2fb4752b73062cf8cbeb92c2cec618989b17e4cf7057`.
- `git show 6883f1d580d811f7c434d1db4642596362f822b1:.ufo/waves/round-25/population.json` reported that the path is absent in the base revision. The counter therefore has an exact-digest-only fixture fallback for that baseline; it does not fetch or mutate repository files.
- Static reading of `scripts/accessibility_packet.py` showed the loader's pinned population and `source-wcag22.html` hashes, use of `normativeText`, punctuation-space normalization, a six-to-25-word quote limit, and word-boundary matching. The counter carries those pins and copies the raw source HTML into the candidate snapshot.

## Risks and blockers

- No tests, build, linter, formatter, or runtime verification was run; the parent owns post-integration verification.
- No LSP device was available in the tool surface; this standalone script was implemented against the observed CLI source and shared contract.
- No tools were installed or updated. No known blocker. The lane's instruction limits edits to the assigned implementation and report, so no `LOG.md` change was made.
