# KakeR31a2.RerunC2Counters — wave-2 falsify, C2 measurement rerun

Scope: re-run both C2 checks at f1ffb81 / b801ac8 / fde133a, compare with the
four verification receipts, run the SCORECARD "Closure checks" commands as
written, check both counter hashes. Sandbox:
/fast/scratch/hyaku/kake-r31/a2-w2/RerunC2Counters/ (clone of the lane at
fde133a; the two after-receipts copied in from lane commit 92235a0 because
fde133a predates them).

## Commands run (all inside the clone, cwd = clone root)

  git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin <sandbox>/clone
  git checkout -q fde133ab48086bb9a06911b4ab045e2ad9086347
  python3 -B .ufo/waves/round-31/c2_quote_truth.py --root . --revision <rev>
  python3 -B .ufo/waves/round-31/c2_strict_checks.py --root . --revision <rev>
  git show fde133a:.ufo/waves/round-31/c1_sandbox_probes.py | sha256sum
  git show fde133a:.ufo/waves/round-31/c2_quote_truth.py | sha256sum
  git show fde133a:.ufo/waves/round-31/c2_strict_checks.py | sha256sum
  git show b801ac8:.ufo/waves/round-31/c2_strict_checks.py | sha256sum
  git diff --quiet a16602a fde133a -- .ufo/waves/round-31/sources/receipts.json \
    sources/S057.txt S058.txt S059.txt S060.txt S061.txt fetch_sources.py

## Results

- c2_quote_truth.py exit 1 / 0-4 at f1ffb81; exit 1 / 0-4 at b801ac8;
  exit 0 / 4-4 at fde133a, controlBroken=false.
- c2_strict_checks.py exit 1 / 0-5 at f1ffb81; exit 1 / 1-5 (S5 only) at
  b801ac8; exit 0 / 5-5 at fde133a.
- diff vs verification/c2-before-f1ffb81.json: IDENTICAL (exit 0).
- diff vs verification/c2-after-fde133a.json (from 92235a0): IDENTICAL.
- diff vs verification/c2-strict-before-f1ffb81.json: IDENTICAL.
- diff vs verification/c2-strict-after-fde133a.json (from 92235a0): IDENTICAL.
- Strict at b801ac8 equals verification/c2-strict-before-c88b97e.json except
  the "revision" field (b801ac8 vs c88b97e). All check outcomes identical
  (1/5, S5 only). Expected: c88b97e..b801ac8 touches only the strict checker,
  receipts and SCORECARD (git diff --name-only), no content files — so the
  same measurement. Not a discrepancy.
- Counter hashes at fde133a: c1_sandbox_probes.py
  4707cebf8831eb9a8e79405fcc07ad77e118110f980dac2826c5934a43166d1a
  (SCORECARD declares 4707cebf…6d1a — match); c2_quote_truth.py
  de48d460aad8645fc59e70792577d4f5a5ceb0032417f021d186e7cc6e0c31b8
  (declares de48d460…31b8 — match); c2_strict_checks.py
  5111264f14ad74cdecf9568a7c41942fb009024210a6eb0ac82d533ec11846ad
  (declaration notes 5111264f…46ad — match). Both after-receipts name these
  hashes in counterSha256/checkerSha256.
- Counter bytes are revision-stable: c2_quote_truth.py and c1_sandbox_probes.py
  have zero diff a16602a→fde133a; c2_strict_checks.py blob at b801ac8 hashes
  identically to fde133a (new file in that range, unchanged since).
- Sources-unchanged closure command exits 0 (no diff a16602a→fde133a for
  receipts.json, S057–S061.txt, fetch_sources.py).

## Interpretation (advisory)

- C2 measurement reproduces exactly: before 0/4 and 0/5, after 4/4 and 5/5,
  byte-identical JSON including per-id quotes and controlBroken=false.
- Counters discriminate: at b801ac8 (declared supplement present, C2 entry
  absent) quote-truth still scores 0/4 and strict 1/5 — they are not
  vacuously passing.
- No discrepancy found in the C2 measurement chain in scope.

## Not verified

- Truth of the S057–S060 source bodies against live render.com (network
  restricted to named seats; I did not fetch).
- C1 counter runs, hostile selftest, .html.gz bytes beyond what the two
  counters themselves hash-check (S5 inside the strict run covers the
  gz/text/receipt consistency and passed).
- Whether the quotes are semantically the best evidence for the claims —
  only that they exist in the retained bodies and are unique per page.

Tooling: no installs. Evidence files: out-quote-*.json, out-strict-*.json,
err-*.txt, c2-after-fde133a.json, c2-strict-after-fde133a.json under
/fast/scratch/hyaku/kake-r31/a2-w2/RerunC2Counters/.
