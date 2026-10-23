# G10 head/tail window class

## Axes

- **Operability (target):** the G10 class returns 120 deterministic one-value units and witnesses both listed controls on both tested seeds.
- **Freshness (non-target):** unchanged.

## Change and behavior

Wrote `.ufo/waves/round-44/classes/g10_headtail_windows.py`. It emits 120 `("value", "loc", value)` units: 30 each of clean head-window path-crossing values, head-window values with a grammar defect after code point 64, clean tail-suffix values, and tail-suffix values with a grammar defect before the retained suffix. All use the zero-padded in-range port `:000080`; the generated tail suffixes are exactly 64 code points and parse as clean URLs. `n` is 120.

The hidden-defect cases are semantic witnesses: reference output has `loc_not_absolute`, while the relevant head/tail control judges the retained window clean. All four required probe invocations returned exit 1 with differing stdout hashes.

## Exact probe commands and output

Working directory for each command: `/home/vgpnk/Projects/shokunin/kake-shokunin`.

Command:
`python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G10 --tool-file .ufo/waves/round-44/controls-r43/headtail-V4-longport-head64.py --seed 4401`

```json
{
 "probe": "G10",
 "seed": 4401,
 "units": 120,
 "values": 120,
 "ref41Exit": 1,
 "candExit": 1,
 "ref41OutSha256": "e99d824995275daf32b305b40b6dbbd7ca7e42881f3cb4092b81270caa1dff79",
 "candOutSha256": "e644e45f75d1688dbf8832dc2ca5fe6be4a5c5ccd3279adce87468779f1595d8",
 "equal": false,
 "ref41Tail": ", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}, {\"id\": \"i60tm85cbu3y\", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}, {\"id\": \"ng39sdrbey79\", \"status\": \"clean\", \"error\": null, \"findings\": []}, {\"id\": \"mfl8qh1\", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}]}\\n",
 "candTail": ", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}, {\"id\": \"i60tm85cbu3y\", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}, {\"id\": \"ng39sdrbey79\", \"status\": \"clean\", \"error\": null, \"findings\": []}, {\"id\": \"mfl8qh1\", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}]}\\n"
}
```

Command:
`python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G10 --tool-file .ufo/waves/round-44/controls-r43/headtail-V4-longport-head64.py --seed 4402`

```json
{
 "probe": "G10",
 "seed": 4402,
 "units": 120,
 "values": 120,
 "ref41Exit": 1,
 "candExit": 1,
 "ref41OutSha256": "018ff3df513d06243d298535f9b938b6b03ff0e3904e12c7984fdab96c0546b8",
 "candOutSha256": "8149ff566b67f6399572bb0686e65fa2e4b410040cf4fa3cf234a04d38f36b52",
 "equal": false,
 "ref41Tail": "l, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}, {\"id\": \"pn6e02\", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}, {\"id\": \"mzu1kb2zllc\", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}, {\"id\": \"aga6d65\", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}]}\\n",
 "candTail": "l, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}, {\"id\": \"pn6e02\", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}, {\"id\": \"mzu1kb2zllc\", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}, {\"id\": \"aga6d65\", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}]}\\n"
}
```

Command:
`python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G10 --tool-file .ufo/waves/round-44/controls-r43/headtail-V8-longport-tail64.py --seed 4401`

```json
{
 "probe": "G10",
 "seed": 4401,
 "units": 120,
 "values": 120,
 "ref41Exit": 1,
 "candExit": 1,
 "ref41OutSha256": "e99d824995275daf32b305b40b6dbbd7ca7e42881f3cb4092b81270caa1dff79",
 "candOutSha256": "dc12c2a82e7f55f55dc443f6891c293fb926982dc3ed66a3eaa255a68b5ed96e",
 "equal": false,
 "ref41Tail": ", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}, {\"id\": \"i60tm85cbu3y\", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}, {\"id\": \"ng39sdrbey79\", \"status\": \"clean\", \"error\": null, \"findings\": []}, {\"id\": \"mfl8qh1\", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}]}\\n",
 "candTail": " \"clean\", \"error\": null, \"findings\": []}, {\"id\": \"f65zlp1s\", \"status\": \"clean\", \"error\": null, \"findings\": []}, {\"id\": \"o5jnkt2i\", \"status\": \"clean\", \"error\": null, \"findings\": []}, {\"id\": \"i60tm85cbu3y\", \"status\": \"clean\", \"error\": null, \"findings\": []}, {\"id\": \"ng39sdrbey79\", \"status\": \"clean\", \"error\": null, \"findings\": []}, {\"id\": \"mfl8qh1\", \"status\": \"clean\", \"error\": null, \"findings\": []}]}\\n"
}
```

Command:
`python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G10 --tool-file .ufo/waves/round-44/controls-r43/headtail-V8-longport-tail64.py --seed 4402`

```json
{
 "probe": "G10",
 "seed": 4402,
 "units": 120,
 "values": 120,
 "ref41Exit": 1,
 "candExit": 1,
 "ref41OutSha256": "018ff3df513d06243d298535f9b938b6b03ff0e3904e12c7984fdab96c0546b8",
 "candOutSha256": "8bb0c43c762a2fd756bf9fc8fb554794cf4d787d1be73f899ba2224467cf5d72",
 "equal": false,
 "ref41Tail": "l, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}, {\"id\": \"pn6e02\", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}, {\"id\": \"mzu1kb2zllc\", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}, {\"id\": \"aga6d65\", \"status\": \"findings\", \"error\": null, \"findings\": [{\"code\": \"loc_not_absolute\", \"entry\": 1}]}]}\\n",
 "candTail": ": \"clean\", \"error\": null, \"findings\": []}, {\"id\": \"xfaqmr1yw\", \"status\": \"clean\", \"error\": null, \"findings\": []}, {\"id\": \"rb9f46h8unk9\", \"status\": \"clean\", \"error\": null, \"findings\": []}, {\"id\": \"pn6e02\", \"status\": \"clean\", \"error\": null, \"findings\": []}, {\"id\": \"mzu1kb2zllc\", \"status\": \"clean\", \"error\": null, \"findings\": []}, {\"id\": \"aga6d65\", \"status\": \"clean\", \"error\": null, \"findings\": []}]}\\n"
}
```

The probe commands exited 1 by design (witness); the JSON fields above are the tool output. No full counter, build, lint, formatting, or other tests were run. No tools were installed. The shell command `mkdir -p /fast/scratch/hyaku/kake-r44/ExecG10Windows /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/w1` completed with no output; scratch directory created, no temporary files used.

## Scope-shape blocker

The requested `loc_out_of_scope` path-window shape cannot be generated using the frozen counter's `value/loc` layout: `.ufo/waves/round-44/c44_count_v5.py` `layout_f` sends every such value to `derived_smu(v)` (lines 580–586), while `derived_smu` builds the sitemap URL at the authority root (lines 569–572). A truncated path whose first segment crosses code point 64 remains under that root, so the clean crossing-path cases do not create the specified scope divergence. The hidden-defect cases do witness both controls and satisfy the probe acceptance; achieving the separate scope witness requires a segment-based per-value sitemap URL in the frozen layout or an allowed custom layout, neither of which this item permits. This is the main risk/blocker; the class does not claim a scope witness.

LSP was unavailable in the exposed tool inventory; no LSP result was assumed. No installs or updates were made.
