#!/usr/bin/env python3
"""Round-44 single-class probe (design-phase tool; not the claim's counting command).

Runs ONE class run of the round-44 counter against the round-41 reference tool and one
candidate tool, and prints whether their exit code and stdout bytes are equal. The counter
itself (`c44_count_v5.py`) is the frozen instrument; this harness only reuses its generators,
`layout_f`, its sandbox and its runner so a class module can be iterated without paying for
the other twenty runs.

Usage:
  python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G5 --tool-file <control.py> \
      [--seed N] [--keep DIR]

Exit 0 when the candidate's judgement equals the round-41 tool's (no witness), 1 when the
candidate diverges (witness), 2 when the probe cannot evaluate.

A witness must be a *semantic* difference: exit code or stdout bytes differ because the two
tools judge a generated value differently. The probe prints the first differing line of each
output (truncated) and the unit count so a report can quote it.
"""
import argparse
import importlib.util
import json
import os
import random
import sys
import tempfile

COUNTER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c44_count_v5.py")


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--class", dest="klass", required=True)
    ap.add_argument("--tool-file", required=True)
    ap.add_argument("--seed", type=int)
    ap.add_argument("--keep", help="copy the generated directory here before exiting")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    c = load(COUNTER, "kake44_counter")
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(6), "big")
    rng = random.Random(seed)
    try:
        fname = dict(c.CLASS_MODULES).get(a.klass)
        if fname is None:
            raise c.CannotEvaluate("unknown class %s" % a.klass)
        cpath = os.path.join(root, c.CLASS_DIR, fname)
        if not os.path.isfile(cpath):
            raise c.CannotEvaluate("class module missing: %s" % fname)
        mod = load(cpath, "kake44_%s" % a.klass.lower())
        classes = {a.klass: mod}
        ref41 = c.git(root, "show", "%s:%s" % (c.REF41_REV, c.TOOL_PATH))
        import hashlib
        if hashlib.sha256(ref41).hexdigest() != c.REF41_SHA:
            raise c.CannotEvaluate("ref41 tool sha256 mismatch")
        cand = open(a.tool_file, "rb").read()
    except (OSError, c.CannotEvaluate, Exception) as exc:  # noqa: BLE001 - probe reports, never traces
        print(json.dumps({"probe": a.klass, "error": "%s: %s" % (type(exc).__name__, exc)}))
        return 2
    td = tempfile.mkdtemp(prefix="kake44-probe-")
    try:
        paths = {}
        for key, data in (("ref41", ref41), ("cand", cand)):
            paths[key] = os.path.join(td, "%s.py" % key)
            with open(paths[key], "wb") as fh:
                fh.write(data)
        cd = os.path.join(td, "cases")
        os.makedirs(cd)
        units, n = classes[a.klass].cases(rng, c)
        mname = c.layout_f(rng, units, cd)
        box = c.Sandbox(rng, td)
        rcode, rout, rcpu = box.run(paths["ref41"], cd, mname)
        ccode, cout, ccpu = box.run(paths["cand"], cd, mname)
        equal = (rcode == ccode and rout == cout)
        out = {"probe": a.klass, "seed": seed, "units": len(units), "values": n,
               "ref41Exit": rcode, "candExit": ccode,
               "ref41OutSha256": __import__("hashlib").sha256(rout).hexdigest(),
               "candOutSha256": __import__("hashlib").sha256(cout).hexdigest(),
               "equal": equal,
               "ref41Tail": rout.decode("utf-8", "replace")[-400:],
               "candTail": cout.decode("utf-8", "replace")[-400:]}
        if a.keep:
            import shutil
            shutil.copytree(cd, a.keep, dirs_exist_ok=True)
            with open(os.path.join(a.keep, "manifest.json"), "w", encoding="utf-8") as fh:
                with open(os.path.join(cd, mname), encoding="utf-8") as src:
                    fh.write(src.read())
        print(json.dumps(out, indent=1))
        return 0 if equal else 1
    finally:
        import shutil
        shutil.rmtree(td, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
