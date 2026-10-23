#!/usr/bin/env python3
"""QUALITY (j) control-consequence check, v2 (round 39; round-38 closure routed defect 4).

Decides by receipt CONTENT, never by file name, label, directory or class text.

  control_consequence_check.py --root <lane> --counter <counter.py> --receipts <dir>
      [--build-revision <rev>] [--oracle-sha <sha256>]...
  control_consequence_check.py --selftest

For every *.json under --receipts (recursive) that carries a `predicate` field:
  * the receipt must carry the frozen counter's sha256 (of the bytes at --counter; give the
    committed counter) and that counter's PREDICATE, CASES, TARGET and KEY_SHA256; a receipt
    with any other predicate, counter, key, cases or target is foreign -> exit 2 (cannot
    evaluate);
  * "meets" is recomputed from the rows: len(rows) == CASES and count(pass is True) >= TARGET.
    The receipt's own `met` field is not trusted (a mismatch is reported and exits 2);
  * the build is identified by BYTES only: sha256 of `git show <build-revision>:scripts/sitemap_audit.py`.
    A receipt meets-and-is-build iff its toolSha256 equals those bytes' sha256.
  * every other receipt that meets is a control meeting the predicate -> exit 1, listed.
    `--oracle-sha` exempts the named tool bytes (reading B of the round-39 drafting defect);
    each exemption is printed so the reading is visible in the receipt.
Exit 0: no control meets. 1: a control meets. 2: cannot evaluate (unreadable or foreign input).
"""
import argparse, hashlib, json, os, re, subprocess, sys, tempfile

TOOL_PATH = "scripts/sitemap_audit.py"


def counter_constants(path):
    src = open(path, "rb").read()
    text = src.decode("utf-8")
    out = {"counterSha256": hashlib.sha256(src).hexdigest()}
    for name in ("PREDICATE", "KEY_SHA256"):
        m = re.search(rf'^{name} = "([^"]*)"$', text, re.M)
        if not m:
            raise ValueError(f"counter lacks {name}")
        out[name] = m.group(1)
    for name in ("CASES", "TARGET"):
        m = re.search(rf"^{name} = (\d+)$", text, re.M)
        if not m:
            raise ValueError(f"counter lacks {name}")
        out[name] = int(m.group(1))
    return out


def build_sha(root, rev):
    data = subprocess.run(["git", "-C", root, "show", f"{rev}:{TOOL_PATH}"], capture_output=True, check=True).stdout
    return hashlib.sha256(data).hexdigest()


def evaluate(receipts_dir, k, bsha, oracles):
    controls, builds, exempt, problems, n = [], [], [], [], 0
    for dp, _, fs in sorted(os.walk(receipts_dir)):
        for f in sorted(fs):
            if not f.endswith(".json"):
                continue
            p = os.path.join(dp, f)
            try:
                rec = json.load(open(p, encoding="utf-8"))
            except Exception as ex:
                problems.append(f"{p}: unreadable ({type(ex).__name__})")
                continue
            if not isinstance(rec, dict) or "predicate" not in rec:
                continue
            n += 1
            if (rec.get("predicate") != k["PREDICATE"] or rec.get("counterSha256") != k["counterSha256"]
                    or rec.get("keySha256") != k["KEY_SHA256"] or rec.get("cases") != k["CASES"]
                    or rec.get("target") != k["TARGET"]):
                problems.append(f"{p}: foreign receipt (predicate/counter/key/cases/target differ)")
                continue
            rows = rec.get("rows")
            if not isinstance(rows, list):
                problems.append(f"{p}: rows missing")
                continue
            passed = sum(1 for r in rows if isinstance(r, dict) and r.get("pass") is True)
            meets = len(rows) == k["CASES"] and passed >= k["TARGET"]
            if bool(rec.get("met")) != meets or (rec.get("passed") is not None and rec.get("passed") != passed):
                problems.append(f"{p}: met/passed fields disagree with rows (rows give {passed}, meets={meets})")
                continue
            if not meets:
                continue
            ts = rec.get("toolSha256")
            if bsha is not None and ts == bsha:
                builds.append(p)
            elif ts in oracles:
                exempt.append(f"{p} (oracle {ts[:12]})")
            else:
                controls.append(f"{p} (tool {str(ts)[:12]}, passed {passed})")
    return n, controls, builds, exempt, problems


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--counter")
    ap.add_argument("--receipts")
    ap.add_argument("--build-revision")
    ap.add_argument("--oracle-sha", action="append", default=[])
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.root and a.counter and a.receipts):
        ap.error("--root, --counter and --receipts are required")
    try:
        k = counter_constants(a.counter)
        bsha = build_sha(a.root, a.build_revision) if a.build_revision else None
    except Exception as ex:
        print(f"cannot evaluate: {ex}")
        return 2
    n, controls, builds, exempt, problems = evaluate(a.receipts, k, bsha, set(a.oracle_sha))
    print(f"counter {k['counterSha256']} predicate {k['PREDICATE']!r}")
    print(f"build revision {a.build_revision} tool sha256 {bsha}")
    print(f"receipts read {n}; build receipts meeting {len(builds)}; oracle-exempt {len(exempt)}; controls meeting {len(controls)}; problems {len(problems)}")
    for tag, lst in (("BUILD", builds), ("EXEMPT", exempt), ("CONTROL-MEETS", controls), ("PROBLEM", problems)):
        for x in lst:
            print(f"{tag} {x}")
    return exit_code(n, controls, problems)


def exit_code(n, controls, problems):
    """The one exit mapping, shared by main and the selftest."""
    if problems or n == 0:
        return 2
    return 1 if controls else 0


def selftest():
    """Negative fixtures: each must give the stated exit; prints PASS n/N."""
    td = tempfile.mkdtemp(prefix="kake-r39-ccc-")
    ctr = os.path.join(td, "counter.py")
    open(ctr, "w").write('PREDICATE = "met: passed >= 3 of 3 sealed cases"\nCASES = 3\nTARGET = 3\nKEY_SHA256 = "ab"\n')
    k = counter_constants(ctr)
    B = "b" * 64

    def rec(ts, passes, label="x", met=None, **kw):
        rows = [{"id": f"c{i}", "pass": bool(v)} for i, v in enumerate(passes)]
        m = len(rows) == 3 and sum(passes) >= 3
        r = {"predicate": k["PREDICATE"], "counterSha256": k["counterSha256"], "keySha256": "ab", "cases": 3,
             "target": 3, "passed": sum(passes), "met": m if met is None else met, "label": label,
             "toolSha256": ts, "rows": rows}
        r.update(kw)
        return r

    cases = [
        ("build only meets", {"a.json": rec(B, [1, 1, 1])}, [], 0),
        ("control named build-*.json meets", {"build-x.json": rec("c" * 64, [1, 1, 1], label="build")}, [], 1),
        ("control one hex digit off the build", {"r.json": rec(B[:-1] + "c", [1, 1, 1])}, [], 1),
        ("control in subdir labelled build", {"sub/build.json": rec("d" * 64, [1, 1, 1], label="build")}, [], 1),
        ("control at 2 of 3", {"b.json": rec(B, [1, 1, 1]), "c.json": rec("e" * 64, [1, 1, 0])}, [], 0),
        ("met field lies false", {"c.json": rec("e" * 64, [1, 1, 1], met=False)}, [], 2),
        ("met field lies true", {"c.json": rec("e" * 64, [1, 1, 0], met=True)}, [], 2),
        ("foreign predicate", {"c.json": rec("e" * 64, [1, 0, 0], predicate="met: passed >= 1 of 3")}, [], 2),
        ("foreign counter sha", {"c.json": rec("e" * 64, [1, 1, 1], counterSha256="0" * 64)}, [], 2),
        ("short rows meet nothing", {"c.json": rec("e" * 64, [1, 1])}, [], 0),
        ("oracle exempt only when named", {"o.json": rec("f" * 64, [1, 1, 1])}, ["f" * 64], 0),
        ("oracle not named", {"o.json": rec("f" * 64, [1, 1, 1])}, [], 1),
        ("no receipts", {}, [], 2),
        ("pass as string 'true' is not a pass", {"c.json": rec("e" * 64, [1, 1, 1], rows=[{"pass": "true"}] * 3, passed=None, met=False)}, [], 0),
        # v2.1 (round 39, MutCcCheckV2 survivors M05, M07, M09-M12, M14):
        ("foreign key sha", {"c.json": rec("e" * 64, [1, 1, 1], keySha256="0" * 64)}, [], 2),
        ("foreign target", {"c.json": rec("e" * 64, [1, 1, 1], target=2)}, [], 2),
        ("passed total contradicts rows", {"c.json": rec("e" * 64, [1, 1, 1], passed=2)}, [], 2),
        ("extra row is not a meet", {"c.json": rec("e" * 64, [1, 1, 1, 0], met=False, passed=3)}, [], 0),
        ("label 'ref' without --oracle-sha is a control", {"ref.json": rec("f" * 64, [1, 1, 1], label="ref")}, [], 1),
        ("oracle exemption covers only the named bytes", {"o.json": rec("f" * 64, [1, 1, 1]), "p.json": rec("a" * 64, [1, 1, 1])}, ["f" * 64], 1),
    ]
    ok = 0
    for name, files, oracles, want in cases:
        d = tempfile.mkdtemp(dir=td)
        for fn, r in files.items():
            os.makedirs(os.path.dirname(os.path.join(d, fn)), exist_ok=True)
            json.dump(r, open(os.path.join(d, fn), "w"))
        n, controls, builds, exempt, problems = evaluate(d, k, B, set(oracles))
        got = exit_code(n, controls, problems)
        ok += got == want
        print(f"{'ok  ' if got == want else 'FAIL'} {name}: exit {got} want {want}")
    print(f"PASS {ok}/{len(cases)}")
    return 0 if ok == len(cases) else 1


if __name__ == "__main__":
    sys.exit(main())
