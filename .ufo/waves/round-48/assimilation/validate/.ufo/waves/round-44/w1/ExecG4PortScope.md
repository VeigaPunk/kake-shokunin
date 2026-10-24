# G4 port-scope witness

Axes: operability and freshness. Implemented G4 as 60 pairfiles (360 URL values). Each file's first loc gives `layout_f` a sitemapUrl with an explicit port; the second loc uses a different port on the same scheme, host, and directory. The remaining four locs stay on the first port. Port pairs vary across `8443/9443`, `8080/8081`, and `443/80`. Round 41 reports the second entry as `loc_out_of_scope`; the targeted control ignores the port and reports clean.

## Files written

- `.ufo/waves/round-44/classes/g4_port_scope.py`
- `.ufo/waves/round-44/w1/ExecG4PortScope.md`

## Required probe evidence

Command:

```text
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G4 --tool-file .ufo/waves/round-44/controls-r43/buildscope-m4-port-dropped.py --seed 44
```

Verbatim decisive JSON fields (trimmed output):

```json
{
 "probe": "G4",
 "seed": 44,
 "units": 60,
 "values": 360,
 "ref41Exit": 1,
 "candExit": 0,
 "ref41OutSha256": "ad07753367dfd050cb95605686a92f5e20cc0025a6558f2af3b68cd91eaf37b1",
 "candOutSha256": "47139f1b3e9cfad30e051c84a4949575105f1b26e82a137bef48a3dade1b43d6",
 "equal": false
}
```

Probe process exit status: `1`.

Command:

```text
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G4 --tool-file .ufo/waves/round-44/controls-r43/buildscope-m4-port-dropped.py --seed 440
```

Verbatim decisive JSON fields (trimmed output):

```json
{
 "probe": "G4",
 "seed": 440,
 "units": 60,
 "values": 360,
 "ref41Exit": 1,
 "candExit": 0,
 "ref41OutSha256": "02d653713fe82875668d3fc0cbae6dfdffafb6dece696b40a5423ce34318183b",
 "candOutSha256": "dcb91890f6226c2003614b6ff38c0628b1460583a9de2ca4e12a997c756590e0",
 "equal": false
}
```

Probe process exit status: `1`.

No tools were installed. No LSP interface was exposed in the available tools; no LSP-backed symbol lookup or refactor was needed for this new module. No checks other than the two assignment-required probes were run. Blockers: none.
