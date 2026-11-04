#!/usr/bin/env python3
"""One-shot: byte-splice two round-80 disclosure entries into the receipt-rewrites ledger.

Preserves every prior byte: the new text is inserted immediately before the array's closing `]`,
the base bytes up to that offset are kept verbatim. Used once in round 80; kept as the record of
how the append was made (the ledger itself is the evidence).
"""
import json
import sys
from pathlib import Path

LEDGER = Path("/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/receipt-rewrites.json")

ENTRIES = [
    {
        "path": ".ufo/waves/round-80/controls/base-c80-defect-queue.txt",
        "commit": "de65ec210e8c4015f27d487fb03ea1e9618bb785",
        "status": "M",
        "fromBlob": "d46bd610bed7b050336c501c2b79c8010d6e7691",
        "toBlob": "dad8fb81bbdc6be4a247aeed74a741e10a50debf",
        "kind": "content",
        "note": "Round-80 amendment 2 re-ran the C1 base receipt on the corrected counter (used-by cell index) before any after-state: one added exit line, the same open=6 met=false verdict. Disclosed in corpus/lessons/round-80.md (Corrections, receipt-rewrite row).",
    },
    {
        "path": ".ufo/waves/round-80/controls/ctl-c80-junk-queue.txt",
        "commit": "de65ec210e8c4015f27d487fb03ea1e9618bb785",
        "status": "M",
        "fromBlob": "a265d23ab29e93002f1dccb42af10c478203f0d2",
        "toBlob": "b72e4af008ab745b186d9270ffff872ca1078863",
        "kind": "content",
        "note": "Round-80 amendment 2 re-ran the junk control on the corrected counter before any after-state: one added exit line, the same met=false verdict and the same open=5 closed=1 reading. Disclosed in corpus/lessons/round-80.md (Corrections, receipt-rewrite row).",
    },
]


def main() -> int:
    base = LEDGER.read_bytes()
    idx = base.rindex(b"]")
    if b'"path": ".ufo/waves/round-80/controls/base-c80-defect-queue.txt"' in base:
        print("already spliced", file=sys.stderr)
        return 1
    block = "".join(",\n" + json.dumps(e, indent=2, ensure_ascii=False) for e in ENTRIES)
    out = base[:idx] + block.encode("utf-8") + base[idx:]
    parsed = json.loads(out)
    assert len(parsed["events"]) == json.loads(base)["events"].__len__() + 2
    LEDGER.write_bytes(out)
    print(f"events {len(json.loads(base)['events'])} -> {len(parsed['events'])}; "
          f"prefix_preserved={out.startswith(base[:idx])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
