# KakeR35.CriticSealedDesign — routes around the round-35 seal

I did not read, list, stat or open anything under /fast/scratch/hyaku/kake-r35/sealed/. Every fact here comes from the public counter, the SCORECARD and the committed receipts.

Inputs: the counter `.ufo/waves/round-35/sealed_count.py` at 318561ef (281 lines) and the SCORECARD at lines 1356-1454. Sandbox: /fast/scratch/hyaku/kake-r35/w1/CriticSealedDesign/. Tools installed: none.

## Routes (line numbers are in sealed_count.py)
1. **Key held under another path at the measured revision: closed, apart from the held sandbox line.** The refusal at :272 only checks the exact `keyPath`, so a key committed under another name is not refused. It still cannot be used. C2 probes come only from `load_key` (:215, :245), and an entry is data that cannot run. The C1 tool runs from a copy in a random temp directory (:147). Its working directory is a fresh case directory, and its environment is reduced to PATH, HOME, LC_ALL and PYTHONDONTWRITEBYTECODE (:163-167). Nothing tells it where the repository is. The tool could only reach a key by reading the host filesystem by absolute path, meaning the repository clone or the sealed directory. That is a sandbox-threat question under the KakeR31.CriticSandboxThreatModel hold, so I stopped that line: no build and no test.
2. **Key fetched from a ref the counter resolves: closed.** `--key-revision` is resolved in `--root` (:103-104). Any blob whose sha256 is not pinned is refused (:107-109, with the pins at :48-49). A ref injected by a bundle fetch can only give the real key or exit 2. Measuring the key revision itself also exits 2 (:272).
3. **Counter paths that pass without running the tool: closed.** If the tool is missing, a run times out, or the output is not a JSON object, the case gets `proc=None` or a parse failure, which scores False (:123, :125-130). A pass needs a matching exit code, verdict and finding multiset (:134). The only free passes are cases where clean output is correct: the constant control got 7, and the base tool, doing nothing, got 14 (receipt `control-c1-base-tool.json`).
4. **Cheapest C1 tool without the claimed work: closed for every control that skips the repairs.** The constant and lookup controls score 7 and the base scores 14. A tool with no HTML parsing cannot get verdicts right without seeing the cases. **Not yet measured: how strictly the cases check that the repairs are complete.** Contract (b) says nesting is counted (SCORECARD :1385-1386), and the L1's own reference patch is about 20 lines (:1419-1420). The 24 cases are split 12 and 12 across three repairs (:1374), so at most 2 failures are allowed. If 2 or fewer cases test nesting, a builder can skip nesting counting and still reach 22. Bundle A tests this.
5. **C2 entry that passes the probes without studying the sources: open by design.** `copied` only penalizes overlap with the retained texts (:228-233). `cites` only checks the row's shape: one row with 11 or more cells, `status` equal to mined, `opened` equal to 2026-10-22, and the entry path in `used-by` (:238-242). The probes check that facts are present (:245). None of the three can tell an entry grounded in S078-S085 from one written out of general knowledge of RFC 9116. The SCORECARD already says junk rows meet `cites` (:1452-1454). Bundle B is that control. Measured with the counter's own code, without the probes, it shows:
   - `words` 864 and `copiedShare` 0.0055, with the pinned texts intact;
   - good cites S078, S079 and S080, on rows whose cells literally say "CONTROL ROW (retained text not studied)";
   - entry, size, copied and cites all true.

   The probes are the only C2 condition this control has not already met. If the L1 scores it at 9 or more of 12, C2 `met` measures RFC knowledge, not the sourced-learning claim.
6. **Weakening the copied check by changing the sources directory: closed.** All nine `.txt` files present at 318561ef are pinned (:62-72, checked at :225-227). Adding texts can only raise the shingle pool. Fewer than 8 words gives copiedShare 1.0 and fails (:232).

## Bundles for L1 scoring (prerequisite 318561efa67206699fdaf259ffb86e39f2d916a8)
- **A** /fast/scratch/hyaku/kake-r35/w1/CriticSealedDesign/bundles/r35-critic-c1-flag-no-nesting.bundle
  - Head: `refs/heads/ctl/c1-flag-no-nesting` = f302eee6cc366770ad493065ec9befda878c8093
  - Bundle sha256: 4e93cfbe9ae6e6af5cebebd6a6dae58623eecb50fb07a4cff1aedd27e3a6efe3
  - Tool sha256: ea6ca8364fe74b3a67afc3615cf792557c8360110456bd7ad0b128dc7dc6e3e9
  - Changes from the base: repair (a) at :256-257 and repair (c) at :227 and :285, both complete. Repair (b) uses one boolean flag (:85, :89, :91, :120) instead of a nesting count, so any `</svg>`, `</template>` or `</math>` end tag reopens counting.
  - Reading the result: 22 or more means the cases do not enforce "nesting is counted", and C1 can be met without it.
- **B** /fast/scratch/hyaku/kake-r35/w1/CriticSealedDesign/bundles/r35-critic-c2-unsourced.bundle
  - Head: `refs/heads/ctl/c2-unsourced` = 169e5039f7a99055cc180c0941140bad41edd253
  - Bundle sha256: ca02bcbd8c466fe808363bb1dfeac9972aae0ae115ef491709d2541b7abec7a6
  - Contents: an entry written from general knowledge, with three control rows.
  - Reading the result: `met` true means C2 does not measure "grounded in rows opened this round".
- Fetch: `git fetch <bundle> 'refs/heads/*:refs/heads/critic/*'`. Score with the frozen counter and the L1's `--key-file` or reveal commit.

## Commands run (all in the sandbox; each exited 0)
- `git clone -q <lane> clone` followed by `checkout -q 318561ef`.
- Smoke test of bundle A on five synthetic pages of my own:
  - multi: two og:url values gave `og_url_multiple`, exit 1.
  - tmpl: `<svg/>` followed by an og:url inside `<template>` gave clean, exit 0.
  - nested: `<svg><svg></svg><meta og:url>` gave a wrong `og_url_multiple`, exit 1. This is the planted shortcut.
  - mixed: a non-UTF-8 page plus a readable page gave `page_unreadable` and `og_required_missing`, `could-not-evaluate`, exit 2.
- `selfcheck_c2.py`: `sealed_count.run_c2` with `load_key` swapped for an empty probe list, output as in route 5.
- `git bundle create` and then `git bundle verify` on both bundles: "is okay".

## Not verified
- I scored neither bundle against the sealed keys. That is the L1's job.
- I did not check the truth of the entry's claims against S078-S085, on purpose, because doing so is what the control skips.
- I made no live fetches.

## Smallest safe corrections
- **C2, route 5:** the counter cannot measure grounding, so don't add another regex. Keep the non-author closure's row-truth and anchor read as a hard gate for C2, and state in the claim that `met` measures that facts are present, not where they came from. Alternatively, add a sealed probe for a fact that appears only in a retained text, such as a detail from S084 or S085's live files or an S083 registry entry, which general RFC knowledge cannot give.
- **C1, route 4:** if bundle A reaches 22, make the declared target 24 of 24 or add more sealed nesting cases at the reveal. Don't relax the contract.
- **Route 1:** whether a C1 tool can read the key from the host filesystem stays under the hold. It needs a seat that is allowed to model sandbox threats.
