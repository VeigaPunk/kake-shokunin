# G9 port-digit witnesses

## What changed

Wrote `.ufo/waves/round-44/classes/g9_port_digits.py` with deterministic `cases(rng, h)` generation: 60 port-cache groups, 60 explicit-default-branch pairs, plus 60 samples of the requested implicit-port pair shape. The cache groups include separate `loc` values on distinct hosts with the same `0008443` port spelling, followed by pairfiles whose sitemap URL uses canonical `8443` while a later loc uses `0008443`; that exposes the digit-only cache to both cache controls, including the control restricted to six/seven digit keys. The branch-witness pairs use explicit `:443` for the first member and `:8443` for a later member.

Source observation / risk: `buildport-m6-default-branch.py:303-306` rewrites a port to the scheme default only when `port is not None`; an implicit port remains `None`. Therefore the requested implicit sitemap-port plus explicit `:8443` contrast does not make that control's authority tuples equal. The module retains that requested sample, and also includes the explicit-`:443` form that actually witnesses the branch. If the acceptance requires the exact implicit-port motif itself to be the witness, the target description conflicts with the frozen control implementation.

LSP was unavailable in the exposed tool inventory; no LSP operation was performed. No tools were installed.

## Commands and verbatim decisive output

Each command below ran in the lane repo. Exit 1 is the probe's documented witness result. The JSON fields shown are copied verbatim from each probe output; `equal` was `false` in every run.

```sh
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G9 --tool-file .ufo/waves/round-44/controls-r43/portvalue-memo-digits.py --seed 4401
```
```json
{"probe":"G9","seed":4401,"units":300,"values":1200,"ref41Exit":1,"candExit":1,"ref41OutSha256":"c1591cf08324bf54e695d0891a5709dd9aa58cb0c28fcc36ffa5b4b8bda479c8","candOutSha256":"5deaeb0679f68a095eda17b93060b2494423bc19abbb59f6c594442ef7f8a5b8","equal":false}
```

```sh
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G9 --tool-file .ufo/waves/round-44/controls-r43/portvalue-memo-digits.py --seed 4402
```
```json
{"probe":"G9","seed":4402,"units":300,"values":1200,"ref41Exit":1,"candExit":1,"ref41OutSha256":"eb30f884050620dfd57964fbb364226475d105860fc34fca4deab590889cd7e5","candOutSha256":"f4c72fb9c023424b6dff13be743fca05400aade253ebdad5afee45720c7e8245","equal":false}
```

```sh
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G9 --tool-file .ufo/waves/round-44/controls-r43/portvalue-memo-digits-67.py --seed 4401
```
```json
{"probe":"G9","seed":4401,"units":300,"values":1200,"ref41Exit":1,"candExit":1,"ref41OutSha256":"c1591cf08324bf54e695d0891a5709dd9aa58cb0c28fcc36ffa5b4b8bda479c8","candOutSha256":"5deaeb0679f68a095eda17b93060b2494423bc19abbb59f6c594442ef7f8a5b8","equal":false}
```

```sh
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G9 --tool-file .ufo/waves/round-44/controls-r43/portvalue-memo-digits-67.py --seed 4402
```
```json
{"probe":"G9","seed":4402,"units":300,"values":1200,"ref41Exit":1,"candExit":1,"ref41OutSha256":"eb30f884050620dfd57964fbb364226475d105860fc34fca4deab590889cd7e5","candOutSha256":"f4c72fb9c023424b6dff13be743fca05400aade253ebdad5afee45720c7e8245","equal":false}
```

```sh
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G9 --tool-file .ufo/waves/round-44/controls-r43/buildport-m6-default-branch.py --seed 4401
```
```json
{"probe":"G9","seed":4401,"units":300,"values":1200,"ref41Exit":1,"candExit":1,"ref41OutSha256":"c1591cf08324bf54e695d0891a5709dd9aa58cb0c28fcc36ffa5b4b8bda479c8","candOutSha256":"0dd95170ba2061de264ab0ca6bf7dc444ad9992850398666d2a3b07dd8e98339","equal":false}
```

```sh
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G9 --tool-file .ufo/waves/round-44/controls-r43/buildport-m6-default-branch.py --seed 4402
```
```json
{"probe":"G9","seed":4402,"units":300,"values":1200,"ref41Exit":1,"candExit":1,"ref41OutSha256":"eb30f884050620dfd57964fbb364226475d105860fc34fca4deab590889cd7e5","candOutSha256":"1d5b3c5e88469a0990db0cfb1f3a5060fa9f9e8f6a8f054018695ceeb24082cf","equal":false}
```

## Files written

- `.ufo/waves/round-44/classes/g9_port_digits.py`
- `.ufo/waves/round-44/w1/ExecG9PortDigits.md`

No other files were written. No blocker to the requested two-seed probe witness criterion; see the implicit-port discrepancy above.
