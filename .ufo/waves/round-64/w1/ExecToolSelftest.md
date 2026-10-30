# ExecToolSelftest — Round 64 C2 attack

## Verdict

The frozen quote-class tool is present unchanged in a pristine archive of measured T0. Its selftest passes 4/4, including `s432_real`, and explicit classification of the real S432 retained blobs with the frozen quote returns `collapsed-only` (exit 0). This seat's assigned C2 tool-selftest/classification attack **passes**; it did not reproduce a tool defect.

## Evidence

Source binding: `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/quote_class.py:32-37` derives the classification from the quote's presence in raw/text; lines `62-72` bind `s432_real` to `.ufo/waves/round-61/sources/S432.html`, `.ufo/waves/round-63/quote-class/S432.txt`, the exact quote, and expected `collapsed-only`. Selftest loads the blobs and compares derived vs expected at lines `76-100`.

Revision under test: measured T0 `4c8295fa5e3b628f1fdf3840299ae415c01849fb`, exported by `git archive` to `/fast/scratch/hyaku/kake-r64/ExecToolSelftest` and executed from the archive root. The archive scratch was removed on command exit.

Exact commands:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin archive 4c8295fa5e3b628f1fdf3840299ae415c01849fb | tar -xf - -C /fast/scratch/hyaku/kake-r64/ExecToolSelftest
cd /fast/scratch/hyaku/kake-r64/ExecToolSelftest
sha256sum scripts/quote_class.py
python3 -B scripts/quote_class.py --selftest
python3 -B scripts/quote_class.py --selftest --json
python3 -B scripts/quote_class.py classify --quote 'The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request.' --raw .ufo/waves/round-61/sources/S432.html --text .ufo/waves/round-63/quote-class/S432.txt
```

Exact outputs:

```text
431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14  scripts/quote_class.py
case inline_raw_substring: derived=raw-substring expected=raw-substring pass
case markup_collapsed_only: derived=collapsed-only expected=collapsed-only pass
case absent_everywhere: derived=absent expected=absent pass
case s432_real: derived=collapsed-only expected=collapsed-only pass
selftest 4/4
{"cases": [{"derived": "raw-substring", "expected": "raw-substring", "id": "inline_raw_substring", "passed": true}, {"derived": "collapsed-only", "expected": "collapsed-only", "id": "markup_collapsed_only", "passed": true}, {"derived": "absent", "expected": "absent", "id": "absent_everywhere", "passed": true}, {"derived": "collapsed-only", "expected": "collapsed-only", "id": "s432_real", "passed": true}], "ok": true, "passed": 4, "total": 4}
derived=collapsed-only
```

No tool was installed or updated. No lane-repository files other than this assigned report were written; the lane repository was treated as read-only.
