# ExecC1SelftestHarden

Claim C1 counter hardening, before data. Read `.ufo/waves/round-58/c58_receipt_rewrites.py` (395 lines) in full, probed it with
throwaway fixtures, then produced a patched copy with the eight w1 fixture classes and the three defects they exposed fixed.

- Patched copy: `.ufo/waves/round-58/w1/ExecC1SelftestHarden.files/c58_receipt_rewrites.py` (535 lines)
- Full unified diff: `.ufo/waves/round-58/w1/ExecC1SelftestHarden.files/c58_receipt_rewrites.diff` (205 lines)
- Receipts: `selftest-v2.txt` (37/37), `selftest-v2-fixtures-only.txt` (32/37), `replay-base-0440485.txt`, `replay-base-0440485.json`
- The original counter is unmodified; nothing outside my report + `.files/` was written. No tools installed (none needed).

## DEFECTS

**D1 — a binary receipt rewrite collapses to one text, so its kind is invented.**
Input: `.ufo/waves/round-51/controls/after-c1-bin.txt` committed as `b"\x00\xff\x01binary\n"`, rewritten to `b"\x00\xfe\x01binary\n"`
(git treats both blobs as binary; the blob ids differ).
Observed (original): `_text` decoded with `"replace"`, so both blobs read `'\x00\ufffd\x01binary\n'` — identical strings for different
bytes; `classify` then returned `append` (both decodings are the same string, so `new.startswith(old)` holds). A ledger that
truthfully said `rerun` for a binary rewrite was counted `wrong_kind`; a ledger that said `append` passed.
Fix: decode blob bytes with `"surrogateescape"` (`_text`, line 127). Different bytes now stay different; the same input classifies `rerun`.

**D2 — a modification entry with `fromBlob: null` was reported as phantom.**
Input: ledger entry `{"status": "M", "fromBlob": null, "toBlob": <real blob>}` for a real modification event.
Observed (original): `malformed=0 phantom=1` — the entry was labelled "matches no event", i.e. a structurally impossible entry was
reported as a content mismatch, and the real malformed class was invisible in the receipt.
Fix: the malformed rule now rejects impossible blob/status combinations (`M` needs both blobs, `D` needs `fromBlob` only, `A` needs
`toBlob` only; lines 180–183), matching how `events()` builds those three statuses. After: `malformed=1 phantom=0`, still not met.

**D3 — `pointed()` rejects a `./`-prefixed evidence pointer.**
Input: note `see ./corpus/README.md` with `corpus/README.md` present at the tip.
Observed (original): `pointed() == False` → `unpointed`, although the contract counts "a repo-relative path that exists at the tip".
Fix: `POINTER_PATH_RE` accepts an optional `./` prefix (line 119). In-word text (`xyz.ufo/evidence.md`) and absent paths still do not
resolve; the negative check is part of the selftest.

**D4 — latent: merge-diff flag precedence.**
Input: merges whose receipt change arrives from the second parent (`--no-ff feat`), whose change is discarded (`-s ours`), and where both
parents changed the receipt and the resolution is a third value.
Observed (git 2.56.0): `-m --first-parent` emits only the first-parent diff, so today's counts are right — exactly one event at the merge,
`fromBlob` = blob at `commit^` (verified for all three shapes; `-m --first-parent`, `--first-parent` and `--diff-merges=first-parent` return
identical chunk sequences of commit ids, while plain `log` also walks the branch commit). `-m` is therefore inert here but would emit per-parent
chunks — and the parser pins `fromBlob` to `commit^` for every chunk, so those would appear as duplicate/spurious events — on any git where
`-m` wins over `--first-parent`.
Fix: `--diff-merges=first-parent` (line 88) states the intent the code already assumes. Needs git ≥ 2.31; on older git the `git log` call
raises and the counter reports unevaluable (exit 2) instead of silently double counting.

**Probed and sound, no change (each now a selftest fixture):** a receipt path with a space and one with non-ASCII characters (`-z` plus
`core.quotePath=false` keep both intact; both disclosed → met); a receipt changed then reverted (two events, oldest-first order, one entry
leaves exactly one undisclosed, both entries meet); a file below `controls/` in a subdirectory (outside the population — `POP_RE` is single
-segment, so it yields no event and cannot reach `new_rewritten`); a symlink receipt (counted as `M`, `toBlob` is the link blob, mode
120000; retarget classifies `rerun`, disclosed → met); pointers inside backticks, before `.` `,` `;` `)` `*`, in `**bold**` and in
`[text](path)` form all resolve, while a pointer embedded in a word does not.

## DIFF

Excerpt of `diff -u .ufo/waves/round-58/c58_receipt_rewrites.py <patched>` (the fixture block hunk `@@ -343,6 +358,131 @@` is summarised
in the next section; its 125 added lines are in the `.diff` file):

```diff
@@ -85,8 +85,8 @@
-    out = git(root, "log", "--reverse", "--no-renames", "--full-history", "-m", "--first-parent", "-z", "--name-status",
-              "--format=%x01%H", tip, "--", ".ufo/waves")
+    out = git(root, "log", "--reverse", "--no-renames", "--full-history", "--diff-merges=first-parent", "--first-parent",
+              "-z", "--name-status", "--format=%x01%H", tip, "--", ".ufo/waves")
@@ -116,7 +116,7 @@
-POINTER_PATH_RE = re.compile(r"(?<![\w/.-])((?:\.ufo|corpus|scripts|SCORECARD\.md|SKILL\.md|LOG\.md)[\w./-]*)")
+POINTER_PATH_RE = re.compile(r"(?<![\w/.-])(?:\./)?((?:\.ufo|corpus|scripts|SCORECARD\.md|SKILL\.md|LOG\.md)[\w./-]*)")
@@ -124,7 +124,7 @@
-    return p.stdout.decode("utf-8", "replace")
+    return p.stdout.decode("utf-8", "surrogateescape")
@@ -177,7 +177,10 @@
-               or any(e.get(k) is not None and not (isinstance(e.get(k), str) and HEX40.match(e[k])) for k in ("fromBlob", "toBlob")))
+               or any(e.get(k) is not None and not (isinstance(e.get(k), str) and HEX40.match(e[k])) for k in ("fromBlob", "toBlob"))
+               or (e.get("status") == "M" and (e.get("fromBlob") is None or e.get("toBlob") is None))
+               or (e.get("status") == "D" and (e.get("fromBlob") is None or e.get("toBlob") is not None))
+               or (e.get("status") == "A" and (e.get("fromBlob") is not None or e.get("toBlob") is None)))
@@ -233,8 +236,12 @@   # _commit: accept bytes fixtures            (helper only)
@@ -242,6 +249,14 @@   # + _link(d, rel, target): idempotent symlink (helper only)
```

## SELFTEST RUN

Command: `TMPDIR=/fast/scratch/hyaku/kake-r58/ExecC1SelftestHarden python3 -B <patched> --selftest` → **37/37, exit 0**
(18 v1 checks unchanged and still passing + 19 new). New checks, in the patched file's order:

| fixture class | check | result |
|---|---|---|
| merge, branch change kept | one event at the merge, `fromBlob` = first-parent blob | PASS |
| merge, branch change kept | disclosed by the merge commit → met | PASS |
| merge, `-s ours` discards branch | not an event, met | PASS |
| merge, both sides changed | one event per commit, no double count | PASS |
| merge, both sides changed | both entries disclosed → met | PASS |
| path with a space + non-ASCII path | 2 events, both paths exact | PASS |
| path with a space + non-ASCII path | disclosed → met | PASS |
| binary rewrite | old ≠ new, distinct blobs, `classify == rerun` | PASS |
| binary rewrite | ledger `append` → `wrong_kind=1` | PASS |
| binary rewrite | ledger `rerun` → met | PASS |
| changed and reverted | two events, order and commits exact | PASS |
| changed and reverted | one entry → exactly one undisclosed | PASS |
| changed and reverted | both entries → met | PASS |
| `M` with `fromBlob: null` | malformed=1, phantom=0 | PASS |
| `controls/sub/nested.txt` | events=0, new_rewritten=0, met | PASS |
| symlink receipt | one `M`, `toBlob` = link blob, old target read back | PASS |
| symlink receipt | disclosed → met | PASS |
| pointers | backticks, `.` `,` `;` `)` `*`, `**bold**`, `[t](p)`, `./` all resolve | PASS |
| pointers | in-word, absent, bare `x` do not resolve | PASS |

Control that the fixtures catch the defects: the same 37-check selftest run against a copy that keeps the original `_text`, malformed rule,
pointer regex and `-m` flag scores **32/37, exit 1** — exactly the five defect-bearing checks fail (binary ×3, null `fromBlob`, `./`
pointer), every other new fixture passes on the untouched code. Receipt: `selftest-v2-fixtures-only.txt`.

Real-lane replay (read-only, patched counter): at `0440485` the 19-event body is byte-identical to
`controls/base-c1-receipt-rewrites.txt` (`events=19 undisclosed=19 phantom=0 malformed=0 wrong_kind=0 unpointed=0 new_rewritten=0
new_receipts=0 met=False`, EXIT=1); `--json` agrees. The same holds at contract `fff3eea6` and at lane HEAD `cc8da16` (snapshot; the
ledger `.ufo/waves/round-58/receipt-rewrites.json` is still absent at that tip, as expected before data).

## RISKS

- D2 moves one class from `phantom` to `malformed`: a ledger that emits `M` with `fromBlob: null` still fails `met`, but its C1 line will
  read `malformed=1` instead of `phantom=1`. The base replay is unaffected (no ledger at that tip).
- D4 requires git ≥ 2.31 (host 2.56.0). On older git the counter becomes unevaluable (exit 2) rather than double counting.
- The merge fixtures use local `--no-ff` / `-s ours` merges only; no network, no host service.
- Not tested, still open by contract: whether the lane's eventual ledger uses any punished shape, and whether ledger notes are truthful in
  prose — [INFERENCE] both are reviewer/builder matters after data.
- Scratch `/fast/scratch/hyaku/kake-r58/ExecC1SelftestHarden` deleted after copying receipts into `.files/`.

VERDICT: Three real defects found and fixed (binary-blob collapse, impossible `M`/null-`fromBlob` mislabelled phantom, `./` pointer
rejection) plus one latent merge-flag hazard made explicit; patched selftest 37/37 with the original code scoring 32/37 on the same
fixtures, and the patched counter reproduces the base C1 receipt byte-for-byte.
