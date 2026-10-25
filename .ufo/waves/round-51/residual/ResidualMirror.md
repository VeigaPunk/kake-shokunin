# ResidualMirror — residual attack on the rebuilt pre-append mirror at `907790c` (round 51, C2/C8)

Seat: `L1Kake51.ResidualMirror`, residual wave 2, dispatched after wave 1 landed at
`907790c78008819fc95c988431188f90b81f0d5f`. Assigned question: does the **rebuilt** pre-append mirror
carry the pre-append bytes, do its census receipts bind, and does C8's sentence now hold under **both**
readings of "the mirror's registry"? Judged axis: freshness (C2/C8). Method: committed bytes only —
`git show`/`ls-tree`/`log`/`merge-base`/`diff`, independent `## Registry` parse, and a read-only re-run of
`scripts/sources-census.sh` (`validate` and `census`) against the mirror and against a `/tmp` reconstruction
of the contaminated subject. Read-only; the only file written by this seat is this report. Tooling: git
2.56.0, `sources-census.sh` sha256 `3fb72615…` (35 466 bytes, 2026-10-19). No installs, no `jj`, no
mutating git.

## Verdict on the assigned questions

| question | measured answer |
|---|---|
| data rows in the mirror `SOURCES.md` | **143** — `## Registry` holds 145 eleven-cell lines = header + separator + 143 rows; independent parser 143; `census … --file` prints `file rows 143` and `FLEET rows 143`; ids unique, max `S286`, no duplicates |
| sha256 vs `census-correction.txt` | **matches both digests it names.** mirror = `cd9ee4cf951f9708f12d9bfb26c6afb783842960d8698c20184fd12292189117` (correction's "after"); the correction's "before" `4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3` is exactly the blob the mirror held at `19a99bd` |
| equals `git show 19a99bd:corpus/SOURCES.md` | **yes, byte-identical** (both `cd9ee4cf…`, 256 lines) — and also byte-identical to base `007d66e:corpus/SOURCES.md`, as the correction states |
| corrected census receipts | `--file` + the mirror path present, `--root` absent (0 matches in both argv files); exit `0` (`0\n`, 2 bytes) for both runs; `rows 143` (file and FLEET); no `E03`/`E04` anywhere in the eight receipt files; `validate` stdout = 12 × `W04` duplicate-URL warnings + `ok <mirror path>`, `stderr` empty |
| receipts reproducible today | **yes, byte-for-byte** — re-running both exact argv lines reproduces `census-stdout.txt` (`6dbb5497…`) and `census-count-stdout.txt` (`be830845…`) with `diff` clean |
| C8 under reading A (mirror file at the measured revision) | **holds** — `cd9ee4cf…`, 143 rows, `S262` count 0, `S263` count 0 |
| C8 under reading B (live registry at the mirror commit) | **holds** — `19a99bd:corpus/SOURCES.md` = `cd9ee4cf…`, 143 rows, no adopted ids |
| C8 under a third reading (mirror blob **at** `19a99bd`) | **fails, permanently** — `4ea81a5…`, 145 rows, both adopted ids present. See Attack 3 |

Frozen counters at the measured revision, as run by this seat:

```
C1 ledger 3/3 met=True        exit=0   (L1 pass, L2 pass, L3 pass)
C2 quote-truth 8/8 met=True   exit=0   (C7 notes [], C8 notes [])
base 007d66e: C1 0/3 met=False exit=1 ; C2 0/8 met=False exit=1 (C8: "no commit adds the pre-append mirror")
```

Precision note on "unchanged since the base": `contract.json` does not exist at base `007d66e` (it is
introduced by `19a99bd`), and its sha256 is identical at `19a99bd` and `907790c`
(`1f158422622ce027a3938428953bef40b3189281625768befd351f396aa79d18`). The claims and all eight condition
sentences are therefore unchanged **since declaration**, and the repair touched no rule.

## Attack 1 — the `validate` receipt cannot bind the mirror's content (demonstrated, not asserted)

The correction's own load-bearing sentence — "`validate` alone cannot tell a 143-row registry from a 145-row
one, so this receipt is what binds the count to the bytes" — is true, and I reproduced the mechanism rather
than taking it on trust.

Counterexample construction: a faithful copy of the pre-append tree (`cp -a …/pre-append /tmp/pptest`), with
`corpus/SOURCES.md` overwritten by the **145-row post-append** bytes
(`git show 907790c:corpus/SOURCES.md`), validated with the same `--file` argv shape:

```
sources-census.sh validate --file /tmp/pptest/corpus/SOURCES.md   → exit 0
  0 × E03 / E04 / E11 ;  12 × W04 ;  "file ok /tmp/pptest/corpus/SOURCES.md"
```

With the path substituted back, that stdout is **byte-identical** to the corrected `census-stdout.txt` and to
`superseded/census-stdout.txt`. So C7's receipt is satisfied identically by the contaminated and the
corrected subject: it is a *path-and-shape* receipt (argv, exit, absence of `E03`/`E04`), never a content
pin. The binding to 143 rows is carried by `census-count-*` (`rows 143`) and by C8's own parse of the mirror
bytes — neither of which the frozen C7 sentence reads.

Why `E11` did not fire on the contaminated subject (the one thing that could have made the receipts
distinguishable): the mirror tree already carried `corpus/knowledge/canonical-selection.md`
(`6fee23e4…`) and `crawler-identity.md` (`cac13588…`), both added by `19a99bd`. They are *drafts* — their
blobs differ from the landed lane entries (`e0b27e1a…`, `c97fd09b…`) — but `E11` checks existence only, so
the contaminated rows' `used-by` resolved and the run stayed clean. My `/tmp` reconstruction inherits that
same tree, so it is faithful for `E11` purposes.

## Attack 2 — `superseded/` is not distinct evidence

All four files are byte-identical to the corrected receipts:

| file | sha256 (identical in both locations) |
|---|---|
| `census-argv.txt` | `d25c02bb5d157f5e9b224ae37bac7a8826c353b47094f95110f98174c49f10b5` |
| `census-stdout.txt` | `6dbb5497639eaf00bf8dd56a84d62a780fc2e5e3985e7042c8818f2aaf0f7141` |
| `census-stderr.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) |
| `census-exit.txt` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` (`0\n`) |

No retained receipt anywhere names or pins the contaminated blob `4ea81a5…`. The repair's "before" survives
only in immutable git history (`git show 19a99bd:<mirror>` = `4ea81a5…`, 258 lines, 145 rows) and in the
correction prose. This does not move the predicate — it is a durability property worth stating so no later
reader treats `superseded/` as an independent witness. ("Moved to `superseded/` unchanged" is unobservable
either way; the copies are identical as copies.)

Confirmed provenance of the repair commit itself: `git diff 19a99bd 907790c -- …/pre-append/corpus/SOURCES.md`
is exactly two deletions (the `S262` and `S263` lines) and zero insertions, and the resulting bytes equal
base. No other mirror-dir file was rewritten.

## Attack 3 — C8's sentence has a third referent that can never hold

The frozen counter resolves "the mirror's registry" to **the live registry at the mirror commit**, not to the
mirror file: `c51_quote_truth.py` finds `mirror_commits = git log --diff-filter=A --format=%H <rev> -- MIRROR`
(one add: `19a99bd`), then calls `show(root, mirror_commit, REGISTRY)` where `REGISTRY = "corpus/SOURCES.md"`.
`MIRROR` is used for the *location* of the commit, never read as bytes.

The sentence's phrase admits a third reading — the mirror blob **as committed at** `19a99bd` — and that
referent is `4ea81a5…`: 145 rows, carrying both adopted ids. Under it C8 reads `['S262: the mirror already
carries the row', 'S263: the mirror already carries the row']` → FAIL. Because `19a99bd` is immutable for a
verifier, that reading can never be satisfied by any future evidence repair.

Today this is latent, not live: the repair made the two named readings coincide (`cd9ee4cf…` both), so the
predicate is met and the code's referent agrees with the artifact. It becomes a false negative the moment a
reader scores the sentence literally instead of running the frozen counter — exactly the divergence
ExecRegistryDiff found pre-repair, now reversed in sign.

Latent, unexercised: `mirror_commits[-1]` picks the **oldest** `--diff-filter=A` commit. A delete-and-re-add
of the mirror would silently pin the stale add. Only one add exists, so nothing is scored wrong here.

## Impacted axes

- **freshness (C2/C8): no new defect.** The mirror bytes are the correct pre-append bytes, the append is
  genuine (base 143 → tip 145, +`S262`/`S263`), and both counters read 3/3 and 8/8 at `907790c`, 0 at base.
- **evidence durability: weakened twice, both non-scoring.** C7's receipt is content-blind (Attack 1) and
  `superseded/` is a duplicate rather than a witness (Attack 2). What carries the claim is the mirror's
  sha256 + row parse + `census-count-*`, all independently reproducible — I reproduced both receipts
  byte-for-byte today.
- **sentence/code agreement: latent ambiguity** (Attack 3); no predicate effect at `907790c`.
- **chronology/provenance: needs one clarifying line.** The mirror *directory* is contemporaneous
  (`19a99bd`), but `SOURCES.md` inside it is a reconstruction written at `907790c`. Readers must not infer
  that the whole `pre-append/` tree predates the append: its `corpus/knowledge/` entries are
  `19a99bd`-dated drafts, not the landed entries.

## Smallest safe correction (documentation only — the contract is frozen)

Append three lines to `…/pre-append/census-correction.txt` (no rule, predicate, sentence or counter edit):

1. C7's `validate` receipt is path-and-shape only; the 143-row binding is `census-count-*` (`rows 143`) plus
   C8's own parse of the mirror. It would read identically over the 145-row blob (reproduced above).
2. `superseded/` duplicates the corrected receipts byte-for-byte; the contaminated subject `4ea81a5…`
   survives only at `19a99bd` in git history.
3. "The mirror's registry" resolves to the mirror bytes **at the measured revision** and to the live registry
   **at the mirror commit** (both `cd9ee4cf…`, 143 rows), never to the mirror blob at `19a99bd`
   (`4ea81a5…`), which history cannot change.

If a rule change were on the table in a later round (it is not, this round): read `MIRROR` at `rev` **and**
`MIRROR` at `mirror_commits[0]`, so the check names the file it claims to judge and pins the newest add.

## Risks

1. A verifier who scores C8's sentence against the mirror blob at `19a99bd` reports 7/8 and a false stop.
   Probability falls to near zero once correction line 3 lands; without it the ambiguity is permanent.
2. Anyone citing C7 as proof that the *pre-append bytes* were validated inherits a claim the receipt cannot
   support. Cite `census-count-*` + the mirror sha256 instead.
3. `git log … -- MIRROR` is cwd-relative: running the frozen command from a subdirectory (e.g.
   `--root .ufo/waves/round-51`) prints `C8_append_after_mirror false "no commit adds the pre-append mirror"`
   while C1–C7 still pass — i.e. a harness-position artifact that looks like a C8 failure. I hit this myself
   and re-ran with `--root .` (8/8). Always invoke from the lane root, as the contract's `countingCommand`
   does.

## Blockers

None. Nothing unreadable, no command failed, no rebase/checkout/index touch, scratch stayed in `/tmp`
(`/tmp/post-append-145.md`, `/tmp/pptest/`). Tool installs/upgrades: **none**.

## Reproduction

```
L=/home/vgpnk/Projects/shokunin/kake-shokunin
M=.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md
git -C $L show 19a99bd8c30d36a4d664871236ba2015d893b5b9:$M | sha256sum     # 4ea81a5a… (contaminated)
git -C $L show 907790c78008819fc95c988431188f90b81f0d5f:$M | sha256sum      # cd9ee4cf… (repaired)
git -C $L show 19a99bd8c30d36a4d664871236ba2015d893b5b9:corpus/SOURCES.md | sha256sum   # cd9ee4cf…
git -C $L show 907790c78008819fc95c988431188f90b81f0d5f:corpus/SOURCES.md | sha256sum    # 4ea81a5a…
git -C $L merge-base --is-ancestor 19a99bd 907790c ; echo $?                # 0
git -C $L diff 19a99bd 907790c -- $M | grep -c '^-[|] S'                    # 2 deletions, 0 insertions
scripts/sources-census.sh validate --file $L/$M            # exit 0, 12×W04 + ok, no E03/E04
scripts/sources-census.sh census   --file $L/$M            # rows 143 (file and FLEET)
git -C $L show 907790c:corpus/SOURCES.md > /tmp/post-append-145.md
cp -a $L/.ufo/waves/round-51/assimilation/pre-append/. /tmp/pptest/
cp /tmp/post-append-145.md /tmp/pptest/corpus/SOURCES.md
scripts/sources-census.sh validate --file /tmp/pptest/corpus/SOURCES.md    # exit 0, stdout ≡ receipt
python3 -B $L/.ufo/waves/round-51/c51_quote_truth.py --root $L --revision 907790c… # 8/8
```
