# ExecRevisionReceipts — round-76 routed defect D1 repaired (revision-bound receipts)

Seat: ExecRevisionReceipts, kake round 77, wave w1. Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`,
base revision `a2cc5f51002433e11cc3d2f70e650a6c60ad5e68` (contract §open). Read-only elsewhere: no round-76 file,
no `scripts/hreflang_audit.py`, and neither counter was touched by this seat. At report time
`git status --porcelain` additionally shows `M scripts/sitemap_audit.py` and `?? corpus/knowledge/sitemap-formats.md`
— another seat's in-flight C2 work, not this seat's; `scripts/hreflang_audit.py` is unmodified.

Receipts written (both under the seat's own control paths):

- `.ufo/waves/round-77/controls/r77-hreflang-matrix.txt` — sha256 `b2e5d00109407ef2d317c4c481183139fc84497dc13ec95b93133bf024cc355b`, 124 lines
- `.ufo/waves/round-77/controls/r77-hreflang-realrun.txt` — sha256 `fe205a6e7c9d7eae9853c31fcd5df7fbae7de88a3e67fe23c94e469def1365e9`, 51 lines

## 1. The defect, in bytes

Round-76 shipped a C2 matrix verdict whose provenance line does not re-anchor its tree. The control receipt
`.ufo/waves/round-76/controls/after-c2-matrix.txt:4` reads:

```
revision=master revision_ok=yes head=d00ea7fb1471f66bf6067cd6fcb5d82c743159c8
```

while the same file's line 1–2 name `tool=…/scripts/hreflang_audit.py` and
`tool_sha256=0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac`. Three independent faults:

1. **`revision=master` is a ref, not a hash.** `git rev-parse master` today is
   `bc2e5fb91e23c8acdac2470ac0f042c76f75417e` — the same word names a different tree than it did at round-76
   closure. A reader cannot reconstruct which bytes were measured.
2. **`revision_ok=yes` only proves the commit exists.** The counter's `revision_note()` runs
   `git cat-file -e <rev>^{commit}` (`c76_hreflang_matrix.py:405-427`); it never checks the *tool*.
   Observed at the named head:

   ```
   $ git cat-file -e d00ea7fb1471f66bf6067cd6fcb5d82c743159c8:scripts/hreflang_audit.py
   fatal: path 'scripts/hreflang_audit.py' exists on disk, but not in 'd00ea7fb1471f66bf6067cd6fcb5d82c743159c8'
   rc=128
   ```

   The wave copy is absent there too (`…:d00ea7fb:.ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py`,
   rc=128); `d00ea7fb` is an ancestor of `a2cc5f51` (`git merge-base --is-ancestor … rc=0`) and the tool landed
   later, at `2cccd59a` (`git log --diff-filter=A --oneline -- scripts/hreflang_audit.py`).
3. **The non-defect control.** The tool bytes themselves were right: `0762452f…` is the digest of the landed
   blob. But the receipt recorded a head that never contained it, so the verdict was unverifiable rather than
   wrong.

The same failure appears in `.ufo/waves/round-76/w1/ExecAuditMatrix/receipts/matrix-run-{execaudittool,ref}.txt`
and `const-*.txt`: they pass `--revision b758cb040d53374b1b63b89702c7128f77212d23` (a concrete hash — good)
but the tool under test was an uncommitted working-tree file, and
`git cat-file -e b758cb04…:scripts/hreflang_audit.py` is likewise `rc=128`. A concrete hash in the argument is
not enough; the artifact must exist at that hash.

## 2. Repair run A — frozen C2 matrix at a full hash, landed tool

Command (exactly as run, cwd = lane root, `S=/fast/scratch/hyaku/kake-r77/ExecRevisionReceipts`):

```sh
python3 -B .ufo/waves/round-76/w1/ExecAuditMatrix/c76_hreflang_matrix.py --root . \
  --tool scripts/hreflang_audit.py --revision a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 \
  --cases .ufo/waves/round-76/w1/ExecAuditMatrix/cases \
  --consts .ufo/waves/round-76/w1/ExecAuditMatrix/consts \
  --work "$S/work/tool-final"
```

Observed stdout header and terminal line (full 71-case + 4-constant transcript in
`controls/r77-hreflang-matrix.txt`):

```
tool=/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/hreflang_audit.py
tool_sha256=0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac
cases_sha256=fa64d448331aa0b2ae4a851afd6e5815919320e8f1381ece0c35283d3bbd9fb5
revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68 revision_ok=yes head=bc2e5fb91e23c8acdac2470ac0f042c76f75417e
…
cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true
observed-exit=0
```

No scratch copy of the matrix, cases or consts was made: the committed round-76 files were exercised in place
(read-only) with the digests in the table below, so the case bytes and counter bytes are exactly what the
round-76 receipts hash.

Required records:

| record | observed |
|---|---|
| receipt prints a concrete revision | yes — `revision=a2cc5f51002433e11cc3d2f70e650a6c60ad5e68` (40 hex chars, not `master`/`HEAD`) |
| artifact exists at that revision | yes — `git cat-file -e a2cc5f51…:scripts/hreflang_audit.py` → `rc=0` |
| named tool sha256 vs blob at that revision | equal — receipt `tool_sha256=0762452f…`, `git show a2cc5f51…:scripts/hreflang_audit.py \| sha256sum` → `0762452f…  -` |
| working-tree copy vs blob | equal — `sha256sum scripts/hreflang_audit.py` → `0762452f…`, blob oid `3f3744727dd22c5e85079af98f6a34e3abb28c56` |
| matrix script / cases / consts provenance | committed at `a2cc5f51` — `git ls-tree -r --name-only a2cc5f51 -- .ufo/waves/round-76/w1/ExecAuditMatrix` lists 86 files; `cases_sha256` equals the round-76 value `fa64d448…`; script digest `sha256sum .ufo/waves/round-76/w1/ExecAuditMatrix/c76_hreflang_matrix.py` → `4958ede07559d15cfb95af57b99dcaee98883420a071847f78f02db248ad7756`, equal to `ExecAuditMatrix/receipts/artifact-sha256.txt:5` |
| tree unmodified at run time | `git status --porcelain -- .ufo/waves/round-76 scripts/hreflang_audit.py` → 0 lines (run before the matrix run), so the bytes exercised were the committed bytes |

`head=bc2e5fb9…` in the line is the lane tip at run time (the round-77 contract commit); it is informational
and mutable. The binding token is `revision=`.

## 3. Repair run B — 8-page real-input manifest, landed tool digest

Round-76 ran this manifest against the pinned predecessor `58a2cdce…`
(`.ufo/waves/round-76/w1/ExecAuditRealRun/receipts/tool-identity.txt`). Re-run on the landed tool:

```sh
python3 -B scripts/hreflang_audit.py \
  --manifest .ufo/waves/round-76/w1/ExecAuditRealRun/real-manifest.json \
  --root . --json --work "$S/work-real"
```

Observed stdout (verbatim) and exit:

```
{"version": 1, "pages": 8, "findings": [], "counts": {"policy": 0, "info": 0, "input": 0, "by_id": {"hreflang_missing_value": 0, "hreflang_invalid_tag": 0, "hreflang_relative_href": 0, "hreflang_duplicate_pair": 0, "hreflang_multiple_xdefault": 0, "hreflang_self_missing": 0, "hreflang_nonreciprocal": 0, "hreflang_canonical_not_self": 0, "hreflang_external_target": 0, "input_unreadable": 0, "input_duplicate_url": 0, "input_url_not_absolute": 0}}, "exit": 0}
observed-exit=0 pages=8 findings=0
```

`pages=8` and `findings=0` match the round-76 pinned run (`real-input-run.txt`: `pages=8`, `findings=[]`,
exit 0) — but now against digest `0762452f…`, the blob at `a2cc5f51`, not `58a2cdce…`.

Retained-byte verification (as the round-76 seat did): manifest sha256
`448ebd9c73c2f563e88a43cc784734447ebe46fc6a077f59e7d2c406a366bc47`, 8 pages, and `page.html` sha256 against each
sibling `fetch.json` → **8/8 true**. Premise correction: the 8 pages are **not** under `.ufo/waves/round-76/w1/`
(`find .ufo/waves/round-76/w1 -name page.html` → 0); the manifest's `file` fields all point at
`.ufo/waves/round-23/live/<id>/page.html`, and each of those is committed at `a2cc5f51` with the same bytes —
`git show a2cc5f51:<path> | sha256sum` equals `sha256sum <path>` for all 8, and
`git status --porcelain -- .ufo/waves/round-23` is empty.

```
burnerchrome-kimi  11976  200  44dc3491…  match=true
charter-ghp        53660  200  7c243a1d…  match=true
ds4cc-kimi         74641  200  108f5aca…  match=true
ds4cc-primary      76159  200  ccb3f46e…  match=true
lucario-ghp         3435  200  bee2d9f5…  match=true
plazir15-ghp       38337  200  d82af77a…  match=true
ufo-fsd-kimi-pro     612  200  1df92e30…  match=true
vault-index-kimi   10059  200  a0a7f33a…  match=true
pages_verified=8/8
```

(Exact lines incl. both digests per page are in `controls/r77-hreflang-realrun.txt`; digests above are
truncated only in this table.)

## 4. Reusable recipe — what makes a receipt revision-bound

Three checks, all cheap (`git` only, no network):

1. **Concrete hash.** The counter prints `revision=<40-hex>`; `master`, `HEAD`, and abbreviations are rejected
   as binding tokens (the counter's `--revision` accepts any revision — passing a ref is the defect).
2. **Artifact exists at that hash.** `git cat-file -e <rev>:<tool>` must exit 0. A commit existing
   (`revision_ok=yes`) is not this check.
3. **Named digest equals the blob.** `tool_sha256=` printed by the counter must equal
   `git show <rev>:<tool> | sha256sum`. This catches a working-tree file run against an unrelated commit.

One-command form for next round (tested both ways below; paste from the lane root, replace `<seat>` with the
round's scratch seat name):

```sh
# prints the matrix verdict line, then BOUND/UNBOUND with the binding triple
R=.ufo/waves/round-76/w1/ExecAuditMatrix; S=/fast/scratch/hyaku/kake-r77/<seat>; mkdir -p "$S"
rev=$(git rev-parse HEAD); tool=scripts/hreflang_audit.py
out=$(TMPDIR="$S" python3 -B "$R/c76_hreflang_matrix.py" --root . --tool "$tool" --revision "$rev" \
        --cases "$R/cases" --consts "$R/consts" --work "$S/work/one-liner" 2>&1)
named=$(printf '%s\n' "$out" | grep -m1 '^tool_sha256=' | cut -d= -f2)
blob=$(git show "$rev:$tool" 2>/dev/null | sha256sum | cut -d' ' -f1)
git cat-file -e "$rev:$tool" 2>/dev/null && [ -n "$named" ] && [ "$named" = "$blob" ] \
  && printf '%s\n' "$out" | tail -1 \
  && echo "BOUND rev=$rev tool=$tool sha256=$named" || echo "UNBOUND rev=$rev tool=$tool named=$named blob=$blob"
```

Observed discrimination (same gate, two revisions):

```
cases=71 decided=69 correct=69 wrong=0 undecided=2 constants_failed=4/4 met=true
BOUND rev=bc2e5fb91e23c8acdac2470ac0f042c76f75417e tool=scripts/hreflang_audit.py sha256=0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac
UNBOUND rev=d00ea7fb1471f66bf6067cd6fcb5d82c743159c8 tool=scripts/hreflang_audit.py named=0762452fd86e55d6e34dd9072260ff0ae864fdf9199b8ff4734d09ecb8b60aac blob=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

The first pair is `rev=$(git rev-parse HEAD)` at run time (`bc2e5fb9…`, the round-77 contract commit; the tool is
present there with the same blob as at `a2cc5f51`). The second is the round-76 receipt's named head evaluated
by the same gate. (`e3b0c442…` is `sha256sum` of empty input: `git show` printed nothing because the path is
absent at that revision.) The matrix line `met=true` is *not* part of the binding gate: bind provenance first,
then read the verdict.

## 5. Risks and residual notes

- **The frozen counter remains unable to detect this class by itself.** `c76_hreflang_matrix.py` checks only
  commit existence (`revision_ok`), prints whatever was passed (`revision=master` included), and never compares
  its `tool_sha256` to a blob. Repairing D1 here means producing bound receipts and this surrounding gate; the
  counter is round-76 frozen bytes and this seat may not edit it.
- **`head=` is not a binding token.** It is `git rev-parse HEAD` at run time (`c76_hreflang_matrix.py:419-427`)
  and changes whenever the lane commits. Any future citation must quote `revision=`, not `head=`.
- **The real-input run used the working-tree `scripts/hreflang_audit.py`.** It is byte-identical to the blob at
  `a2cc5f51` (`0762452f…` both) and `git status --porcelain -- scripts/hreflang_audit.py` is empty, so the bytes
  measured are the revision's bytes; if the file is ever edited, run the blob
  (`git show <rev>:scripts/hreflang_audit.py > $S/tool.py`) instead.
- **Scope.** No score, claim, or counter was touched; no network, no package installs (none needed), no git/jj
  mutation. Scratch `/fast/scratch/hyaku/kake-r77/ExecRevisionReceipts` is removed after the receipts above were
  copied into this wave dir.
