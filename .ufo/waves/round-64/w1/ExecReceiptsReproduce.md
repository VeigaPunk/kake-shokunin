# ExecReceiptsReproduce — round 64

## Scope and method

Read-only lane inspection; isolated fixture build under `/fast/scratch/hyaku/kake-r64/ExecReceiptsReproduce/fixtures` via:

```sh
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/fixtures/build_fixtures.py /fast/scratch/hyaku/kake-r64/ExecReceiptsReproduce/fixtures --lane /home/vgpnk/Projects/shokunin/kake-shokunin
```

The fixture driver's actual revisions were: stub `c23918296faffa89038607d6babc5214e82f670d`; marker `02a7dbae5420dbef030bf7974c8301d53dee61ff`; fabrication `2349b707934f328bf163245ae282ff6b77e2eb19`; junk `0929c50c13488217395b207e55e3cb36bce428cb`. These differ from committed `controls/fixture-builds.txt` revisions because Git commit IDs incorporate repository/time metadata; the fixtures' target semantics matched by the output bodies.

## Reproduced outcomes

Commands used frozen lane scripts against each newly built fixture (all returned the indicated status; stdout is given):

```sh
python3 -B .../c64_calibration.py --root <fixture> --revision <new fixture HEAD>
```

- Marker: exit 1; `revision=02a7dbae5420dbef030bf7974c8301d53dee61ff disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false`
- Fabrication: exit 1; same body and fields, revision `2349b707934f328bf163245ae282ff6b77e2eb19`, `met=false`.
- Junk: exit 1; `revision=0929c50c13488217395b207e55e3cb36bce428cb disagreements=1 pins=0 pin_drift=drift:raw,text,ledger,recipe recipe_rederive=0 ledger_state=ledger_absent derived=unevaluable class_match=0 located=unevaluable quote_correction=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false`.

C2 stub differential:

```sh
python3 -B .../c64_quote_tool.py --root <stub-repo> --revision c23918296faffa89038607d6babc5214e82f670d
```

exit 1; `revision=c23918296faffa89038607d6babc5214e82f670d present=1 tool_sha=mismatch selftest=skipped frozen_cases=missing rederive=unevaluable met=false`.

```sh
python3 -B .../round-63/c63_quote_tool.py --root <stub-repo> --revision c23918296faffa89038607d6babc5214e82f670d
```

exit 0; `revision=c23918296faffa89038607d6babc5214e82f670d present=1 selftest=4/4 frozen_cases=ok met=true`.

C1 selftest on lane root, with `--selftest-work <scratch>`: exit 0, `selftest 26/26`. C2 selftest likewise: exit 0, `selftest 11/11`. (An initial attempt used unsupported `--workdir` and a fixture root without the base blobs; both were corrected using the documented `--selftest-work` option and lane root.)

Base C1:

```sh
python3 -B .../c64_calibration.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 1a48131577ba82c967650561be34e8dba909432a
```

exit 1; `revision=1a48131577ba82c967650561be34e8dba909432a disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false`.

## Verdict, mismatch, and blockers

All exercised outcome bodies and exit statuses agree with the committed receipts' expected behavior: marker/fabrication/junk rejected, C1 26/26, C2 11/11, C2 rejects stub while C3 counter reproduces the stub defect, and base C1 rejects. They are **not byte-for-byte identical receipts**: the fixture IDs differ, and stdout is not the complete receipt (the committed receipt includes the shell command and `exit=N` trailer). `diff -u` confirmed these expected differences. No lane files or frozen claims/receipts were changed.

The ledger-mut control was **not reproduced**. `build_fixtures.py` creates only stub/marker/fabrication/junk; `controls/control-ledger-mut.txt` describes a separately mutated marker fixture and its frozen revision, but does not specify the exact mutation recipe. I did not invent or modify a lane fixture to guess it. The committed ledger-mut expected result is exit 1 with `pins=0 pin_drift=drift:ledger recipe_rederive=0 ledger_state=ledger_absent ... met=false` at revision `5b981bd0c43dd30c1546a1966d971f4227f60973`.

The committed `control-*`, `stub-*`, and `base-c1` files do not have corresponding full results byte-identical to scratch runs because of path/revision and receipt-wrapper differences above. Tool installs: none. Scratch tree removed before report write.