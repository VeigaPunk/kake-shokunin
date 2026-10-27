#!/usr/bin/env python3
"""Round-58 C1 candidate ledger builder — emit `.ufo/waves/round-58/receipt-rewrites.json` from git.

Mechanical source of truth: the counter `c58_receipt_rewrites.py` itself (imported by path with importlib), so the
ledger's events and kinds are exactly what the counter will re-derive — no hand-typed hashes, no transcription.

    build_ledger.py --root <lane> --revision <base|tip> [--note TEMPLATE] [--out FILE] [--verify]

Every emitted entry carries all seven counter FIELDS (path, commit, status, fromBlob, toBlob, kind, note). `note`
defaults to the literal `TODO` (the L1 merges the scribes' disclosure notes): the ledger is then structurally
complete but fails the counter's `unpointed` clause on purpose, because a note is a human statement, not a
derivable value. `--note 'see {path}'` writes the mechanical self-pointing variant used for the proof run.
`{path}` in the template is replaced with the entry's receipt path.

Exit codes: 0 ledger written, 1 --verify found the counter not met, 2 evidence unevaluable (revision unresolved),
64 usage.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys

SCHEMA = "kake-r58-receipt-rewrites-v1"
COUNTER = ".ufo/waves/round-58/c58_receipt_rewrites.py"
FIELDS = ("path", "commit", "status", "fromBlob", "toBlob", "kind", "note")


def load_counter(lane: str):
    """Import the counter module by path so a missing/moved counter fails loudly instead of drifting."""
    path = os.path.join(lane, COUNTER)
    if not os.path.isfile(path):
        raise SystemExit(f"unevaluable: counter not found at {path}")
    spec = importlib.util.spec_from_file_location("c58_receipt_rewrites", path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"unevaluable: cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def blob_text(counter, root: str, blob: str | None) -> str:
    if not blob:
        return ""
    return counter.git(root, "cat-file", "blob", blob, check=False)


def build(counter, root: str, tip: str, note_template: str) -> dict:
    entries = []
    for ev in counter.events(root, tip):
        entry = {
            "path": ev["path"],
            "commit": ev["commit"],
            "status": ev["status"],
            "fromBlob": ev["fromBlob"],
            "toBlob": ev["toBlob"],
            "kind": counter.classify(ev["status"], blob_text(counter, root, ev["fromBlob"]),
                                     blob_text(counter, root, ev["toBlob"])),
            "note": note_template.replace("{path}", ev["path"]) if "{path}" in note_template else note_template,
        }
        missing = [f for f in FIELDS if f not in entry]
        if missing:
            raise SystemExit(f"internal: entry for {ev['path']} missing {missing}")
        entries.append(entry)
    return {"schema": SCHEMA, "events": entries}


def main() -> int:
    class _P(argparse.ArgumentParser):
        def error(self, message):
            print(f"usage error: {message}", file=sys.stderr)
            raise SystemExit(64)

    ap = _P(description="Round-58 C1 candidate ledger builder (events and kinds from the counter itself)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision", required=True)
    ap.add_argument("--note", default="TODO", help="note template; `{path}` expands to the receipt path")
    ap.add_argument("--out", help="write the ledger here (default: stdout)")
    ap.add_argument("--verify", action="store_true", help="also run the counter's measure() on the same revision")
    a = ap.parse_args()

    root = os.path.abspath(a.root)
    counter = load_counter(root)
    tip = counter.git(root, "rev-parse", "--verify", "-q", f"{a.revision}^{{commit}}", check=False).strip()
    if not tip:
        print(f"unevaluable: revision {a.revision!r} does not resolve in {root!r}\nEXIT=2")
        return 2
    doc = build(counter, root, tip, a.note)
    text = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {a.out}: {len(doc['events'])} events ({tip})", file=sys.stderr)
    else:
        sys.stdout.write(text)
    if a.verify:
        v = counter.measure(root, tip)
        print("verify: " + counter.report(v, tip, False), file=sys.stderr)
        return 0 if v["met"] else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
