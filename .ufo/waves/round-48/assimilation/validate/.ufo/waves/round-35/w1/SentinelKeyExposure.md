# KakeR35.SentinelKeyExposure — pre-reveal key exposure

I did not read, list, copy or grep anything under /fast/scratch/hyaku/kake-r35/sealed/. Only
`stat -c '%a %U'` on the directory itself, as permitted. One 64-byte run of the C1 key was
observed indirectly, through a round-34 agent transcript (finding 3); I did not open the key.

**Verdict: no committed or shared byte carries the sealed case/probe content, but the seal is
leak-prone in three ways that do not need the keys: the 0700 mode isolates nobody, the public
pre-reveal SCORECARD names the sealed path and the `--key-file` oracle, and the committed
receipts disclose sealed expectations that can be reconstructed with the committed controls.**

## What I ran (all in clone /fast/scratch/hyaku/kake-r35/w1/SentinelKeyExposure/clone, at 318561ef)

1. `stat -c '%a %U' /fast/scratch/hyaku/kake-r35/sealed` -> `700 vgpnk`, exit 0. `id` -> `uid=1000(vgpnk)`.
2. Hashed every object of the lane (3215 blobs, including unreachable) and of every commit in
   `git log --all`: 0 matches of C1 `a861dccd…` / C2 `111bceea…`, exit 0.
3. `git log --all -p | grep -c` for `c1-cases|c2-probes|"expect"|"regex"`: only the counter and the
   receipts (key paths and pinned digests) plus round-34's public `c1-matrix.json` expects.
4. `git log --all --diff-filter=A -- '.ufo/waves/round-35/sealed/*'` -> exactly one commit,
   `4c6be2b` (reveal, 19:37:28). `git log --all --find-object=<key blobs>` -> `4c6be2b` and
   `f1599cb` (refs/jj/keep), same second. Nothing pre-reveal.
5. Fleet repo: 5078 blobs hashed, 0 matches; fleet working tree path/string grep -> only the lane's
   own post-reveal copies. Fleet `.ufo/**` shingle scan: 0.
6. /fast/scratch/hyaku/kake-r35 outside `sealed/`: 71,051 files shingle-scanned (64-byte key
   runs), plus all 40 git repos' blobs -> only `l1/clone/.ufo/waves/round-35/sealed/*` (L1's own
   post-reveal clone, mtime 19:42). Sibling `w1/*/keys/` files are synthetic (`c2-probes.json`
   sha `f8959be9…`, not `111bceea…`).
7. `/home/vgpnk/.omp` 60,765 files shingle-scanned -> 1 file (finding 3).

## Findings

1. **Sealed input landed only at the reveal.** Lane keys first appear at `4c6be2b` (19:37:28); the
   measured revisions (`b1cbbc39` 19:35:03 C1 build, `95abec21` 19:37:14 C2 build, `16a6b8b`,
   `318561ef`) hold no key bytes. Ordering is correct.
2. **The 0700 seal gives no isolation between seats (real exposure path).** `stat` -> `700 vgpnk`
   and every seat runs as `uid=1000(vgpnk)` (my own `id`). Any wave seat could have opened
   `/fast/scratch/hyaku/kake-r35/sealed/c1-cases.json` at any time pre-reveal; the seal is
   procedural, not a permission boundary. Severity: high, but only a policy violation until
   someone uses it. Smallest remediation: run the L1 under a distinct uid, or keep the keys
   outside every seat's uid (e.g. root-owned 0700).
3. **The C1 key's case markup is reachable from a shared transcript.** One 64-byte run of
   `c1-cases.json` (offset 11904) also occurs in
   `~/.omp/agent/sessions/.../KakeR34/KakeR34.SentinelToolInputs.jsonl:117376` (round-34 seat
   transcript, mtime 18:32 today); 1 of 333 key blocks, 0 of 57 probe blocks. It is generic
   HTML/`og:` head markup (22 distinct chars, 6 quotes), not case-specific, and it discloses no
   expectation or probe text. Impact: none measurable.
4. **A committed byte plus a committed tool reconstructs 7 of 24 sealed C1 expectations.**
   The constant control (`5f767534`, public in `r35-control-c1-constant.bundle`) prints
   `exit 0 / clean / no findings`, so it passes a case iff the sealed expectation is exactly that.
   `control-c1-constant-clean.json` therefore discloses that `case-02,03,04,05,09,11,19` are the
   clean-expectation cases — a reconstruction of their full `expect` block without the key.
   The lookup control `dcef39b5` returns the same 7 (its table misses and it falls back to clean),
   corroborating. Case *inputs* stay hidden.
5. **A committed byte plus public texts constrains every C2 probe.** With the keyword and
   transcript control entries public in committed bundles, the probe flags leak a 12-bit match
   vector per known text: `P01,P03,P07` match both; `P02,P06,P08,P09,P11` match the RFC 2.5-3.1
   verbatim only; `P04,P05,P10,P12` match neither. That fixes each probe's subject class (e.g. P02
   must match RFC body text that the TOC list lacks) without giving regex text.
6. **The oracle is documented pre-reveal, so the flags are not the only channel.**
   `318561ef:SCORECARD.md:1365` names the sealed directory and mode 0700, `:1434` documents the
   `--key-file` invocation used for the controls, and `:1419-1420` names `sealed/ref/` as holding a
   20-line patch that scored 24/24. Anyone can run the counter as an iterative grader:
   `python3 -B .ufo/waves/round-35/sealed_count.py c1 --root <lane> --revision b1cbbc39
   --key-file <lane>/.ufo/waves/round-35/sealed/c1-cases.json` -> `passed 24`, `met true`,
   24-entry perCase, exit 0 (run post-reveal, but identical pre-reveal under finding 2).
   Smallest remediation: stop publishing the sealed path and the `--key-file` shape in the
   pre-reveal SCORECARD.
7. **Reveal landed before wave 1 finished.** `4c6be2b` (19:37:28) precedes my own and several
   sibling seats' completion, so keys are readable now in the lane tree and in every seat clone
   fetched after 19:37. That is by design for measurement, but it means "before the reveal" holds
   only for the byte snapshot, not for the seats.

## Not verified
- I did not open the sealed directory (bounds), so I cannot state its file list or the state of
  `sealed/ref/`; finding 2 rests on the mode/owner pair plus my own uid.
- Nothing was installed; no builds, linters, tests or counters beyond those listed.
