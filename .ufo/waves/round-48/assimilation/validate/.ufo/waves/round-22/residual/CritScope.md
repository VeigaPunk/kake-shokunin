## Verdict
Counterexample found — but not against either scope *decision*: both keep their ground. One P2 implementation defect inside decision (b)'s mechanism: `os.path.abspath` lexically collapses `..`, so a `--manifest` path containing `..` after a symlink audits a different file than the kernel-resolved path the caller passed.

## Findings

### Decision (a): usage errors emit `findings: []` with `could-not-evaluate` → **KEEP**

Contract text: outputs.stdout requires "findings array each containing id and page" — an empty array satisfies this vacuously; `findingIds` is a closed list with no usage id, so a synthetic `usage_invalid` would *contradict* the frozen contract, and reusing `input_invalid` would conflate the two distinct exitMap buckets 2/64. Observed (post-fix tree, public CLI):

- `python3 …/canonical_audit.py --manifest <m> --bogus` → exit 64, stdout `{"findings":[],"pagesChecked":0,"verdict":"could-not-evaluate"}`, usage text on stderr.
- `[]`, `--manifest` (missing value), `--selftest --json`, repeated `--manifest`, `--man x` (allow_abbrev=False) → same: exit 64 + USAGE_RESULT JSON.
- `--help` → exit 0, argparse help on stdout, no `"verdict"`, matching usage()'s documented exception.
- stderr/stdout streams are separated correctly; an automation consumer parses stdout and gets a contract-shaped object for every non-`--help` invocation.

Alternatives and cost: (i) add `usage_invalid` finding → requires editing the frozen contract's `findingIds`; cost = contract amendment, benefit ~0 (exit code already discriminates). (ii) `input_invalid` at exit 64 → mislabels argv errors as input errors. **Matrix impact: none** — all 32 invocations are valid-shaped.

### Decision (b): caller-trusted manifest dir path, no-follow file/page components → **KEEP decision, with one defect in its implementation**

Contract fileResolution scopes the symlink rule to "HTML paths relative to manifest directory" — the argv path is caller input, not manifest content; a manifest cannot smuggle a symlink via `file` (B4 probe: `alias/page.html` → exit 2 `input_invalid`). The single `dir_fd` anchors manifest+pages to one inode (TOCTOU-fair). w2's residual "manifest symlink" question is now closed explicitly: `manifest.json` symlink → exit 2 (B3); ancestor *and* final-dir-component symlinks in the dir path → clean (B1, B2), matching usage()'s new sentence and selftest case `manifest_dir_caller_prefix` (expect exit 0).

Alternatives: (i) `O_NOFOLLOW` on dir open — meaningless against ancestors, only breaks dir-symlink convenience; (ii) `realpath`-equality check — adds a second path walk (TOCTOU), breaks legit symlinked checkouts (~zero cost to matrix on this host: `/tmp` is a real directory, `matrix.py` `resolve()`s manifests, so still 32/32). Both buy no security: the caller already controls the input set.

**P2 defect — `..` after a symlink audits the wrong file.** `read_manifest_bytes` does `os.path.split(os.path.abspath(path))`; `abspath` collapses `..` lexically, diverging from kernel resolution when `..` follows a symlink. Exact probe:

```
tree: dv/alias -> deep/real; dv/deep/manifest.json = mismatching manifest; dv/manifest.json = clean manifest
ARG=$W/dv/alias/../manifest.json
readlink -m $ARG        → …/dv/deep/manifest.json   (kernel view)
python3 canonical_audit.py --manifest $ARG
  → {"findings":[],"pagesChecked":1,"verdict":"clean"}   exit=0   (audited dv/manifest.json)
python3 canonical_audit.py --manifest …/dv/deep/manifest.json
  → {"findings":[{"id":"canonical_mismatch",…}],"verdict":"failed-policy"}  exit=1
```

So a preflight of the path the caller literally named can print `clean` for a different manifest that fails policy — silent wrong-file audit, contrary to usage()'s "opened as given". Impacted: claim C1 operability (path-selection correctness). Smallest fix: split the path without `abspath` (`directory, name = os.path.split(path); os.open(directory or ".", O_RDONLY|O_DIRECTORY)`), letting the kernel resolve `..` once — ~3 lines, removes the lexical-collapse class entirely, keeps the single-dir_fd anchor. Matrix impact: none (oracle manifests carry no `..`); `manifest_traversal`/`symlink_html` unchanged (they test `file`, not argv). Severity P2 rather than P1: requires caller to pass `..` after a symlink; no silent pass/fail within the frozen population.

## Checked and held

- Post-fix matrix on the live lane: `python3 .ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --json` → exit 0, `accepted 32 / total 32`.
- Selftest already encodes both decisions (`manifest_dir_caller_prefix`→clean; `cli_*` cases→USAGE_RESULT; `manifest_symlink`→input_invalid), so either alternative would also require spec churn for no contract-backed gain.
- Non-regular manifest/page (FIFO) and symlinked `file` components still reject via O_NONBLOCK+fstat / O_NOFOLLOW walks.
- Usage decision alternatives both strictly worse under the frozen contract; kept.

## Limits

- Reviewed `usage()`, `parse_cli()`, `read_manifest_bytes()`, `read_page_bytes()`, `audit_manifest()`, `main()`, selftest specs; probes confined to `/tmp/kake-r22a2-critscope-5XyN` (lane untouched, read-only honored).
- The `..` divergence is shown only for the `..`-after-symlink shape; plain `..` paths (no symlink) resolve identically under both semantics.
- No builds/linters; no measure.py rerun (working-tree validator isn't addressable by `--revision`); matrix run is the named-allowed check. No tools installed; no pacman transactions.