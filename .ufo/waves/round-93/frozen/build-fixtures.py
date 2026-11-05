#!/usr/bin/env python3
"""Rebuild the six round-93 C2 forgery fixtures from `pos-good.py`.

Each forgery is the frozen positive control with exactly one documented defect, so
the counter's refusal of it is caused by that defect and not by a broken subject.
Run from this directory; the pins file must then be rebuilt and the counter's
PINS_SHA updated (see `.ufo/waves/round-93/freeze.md`).
"""
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))

PATCHES = {
    "neg-blanket-200": [(
        """    try:
        out = decide(payload)
    except Bad as exc:
        sys.stderr.write("invalid_input: %s\\n" % exc)
        return 1""",
        """    try:
        decide(payload)
    except Bad as exc:
        sys.stderr.write("invalid_input: %s\\n" % exc)
        return 1
    out = {"decision": "200", "precondition": None}""")],
    "neg-blanket-304": [(
        """    try:
        out = decide(payload)
    except Bad as exc:
        sys.stderr.write("invalid_input: %s\\n" % exc)
        return 1""",
        """    try:
        decide(payload)
    except Bad as exc:
        sys.stderr.write("invalid_input: %s\\n" % exc)
        return 1
    out = {"decision": "304", "precondition": "if_none_match"}""")],
    "neg-weak-strong-swap": [
        ("""        if not hit(parsed["if_match"], strong):""",
         """        if not hit(parsed["if_match"], weak):"""),
        ("""        if hit(parsed["if_none_match"], weak):""",
         """        if hit(parsed["if_none_match"], strong):"""),
    ],
    "neg-ignore-precedence": [(
        """    if parsed["if_none_match"] is not None:""",
        """    if (parsed["if_modified_since"] is not None and method in ("GET", "HEAD")
          and stamp is not None and stamp <= parsed["if_modified_since"]):
        return {"decision": "304", "precondition": "if_modified_since"}
    if parsed["if_none_match"] is not None:""")],
    "neg-oracle-import": [(
        """def main():
    raw = sys.stdin.read()""",
        """def main():
    sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-93")
    import c93_conditional  # noqa: F401  (absolute-path import of the scoring oracle)
    raw = sys.stdin.read()""")],
    "neg-pin-reader": [(
        """def main():
    raw = sys.stdin.read()""",
        """def main():
    with open("/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-93/frozen/"
              "c2-population.sha256") as fh:
        fh.read()
    raw = sys.stdin.read()""")],
}


def main():
    base = open(os.path.join(HERE, "pos-good.py"), encoding="utf-8").read()
    rows = []
    for name, patches in PATCHES.items():
        text = base
        for old, new in patches:
            if text.count(old) != 1:
                raise SystemExit("%s: patch anchor count %d" % (name, text.count(old)))
            text = text.replace(old, new)
        path = os.path.join(HERE, name + ".py")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("wrote %s" % name)
    names = ["pos-good"] + sorted(PATCHES)
    for name in names:
        with open(os.path.join(HERE, name + ".py"), "rb") as fh:
            digest = hashlib.sha256(fh.read()).hexdigest()
        rows.append("%s  .ufo/waves/round-93/frozen/%s.py" % (digest, name))
    with open(os.path.join(HERE, "c2-population.sha256"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(rows) + "\n")
    with open(os.path.join(HERE, "c2-population.sha256"), "rb") as fh:
        print("pins sha256 %s" % hashlib.sha256(fh.read()).hexdigest())


if __name__ == "__main__":
    main()
