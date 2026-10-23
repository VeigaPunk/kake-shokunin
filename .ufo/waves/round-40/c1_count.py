#!/usr/bin/env python3
"""Round-40 C1 counter (frozen at the C1 declaration; never edited after it).

Claim C1 (operability): `scripts/sitemap_audit.py` is repaired on three input classes the
round-39 closure routed (corpus/lessons/round-39-verifier-spotcheck.md, routed defect 2):
  E  UTF-16 without a byte-order mark (bytes decode as UTF-8, U+0000 is not an XML Char)
     -> xml_malformed (contract .ufo/waves/round-39/c1-contract.md sentences 6 and 8);
  U  a `loc` or `sitemapUrl` that urlsplit would alter (TAB, CR or LF anywhere, a leading C0
     control or space) is judged as written: not an absolute URL (sentences 21, 22 and 4);
  R  a check repeating the string `id` of an earlier check that was itself invalid is
     `check_invalid` (sentence 4).
Every class carries witnesses of both polarities. Hosts, directories, file names and check ids
are random per run (`--seed` replays one run), so a tool keyed on ids, names or labels cannot
match. The tool runs in bubblewrap with only /usr, the case directory and the tool visible.

PREDICATE is the frozen sentence; it is the same text in SCORECARD.md and in every receipt.
Exit 0 met, 1 not met, 2 cannot evaluate.

Usage: c1_count.py --root <lane> (--revision <rev> | --tool-file <path>) [--label L]
                   [--seed S] [--out receipt.json]
"""
import argparse
import hashlib
import json
import os
import random
import subprocess
import sys
import tempfile

PREDICATE = "met: passed >= 30 of 30 witnesses and the round-39 selftest passes 150 of 150"
WITNESSES = 30
TARGET = 30
SELFTEST_REV = "f171c58b918f705ca875b6cb42b9e75489cd3589"
SELFTEST_PATH = "scripts/sitemap_audit_selftest.py"
SELFTEST_SHA256 = "99ee9bbfc55f8e3c7a3ce073c0697d0efad573cd6028f44029eb35aac93351db"
SELFTEST_PASS = "PASS 150/150"
TOOL_PATH = "scripts/sitemap_audit.py"
CASE_TIMEOUT = 60
SELFTEST_TIMEOUT = 900
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, check=True).stdout


def witnesses(rng):
    """Return the 30 witnesses for one random draw."""
    def tok(n, alphabet="abcdefghijklmnopqrstuvwxyz0123456789"):
        return "".join(rng.choice(alphabet) for _ in range(n))

    host = "w" + tok(8) + ".example"
    d = "d" + tok(6)
    su = f"http://{host}/{d}/sitemap.xml"
    fname = "f" + tok(7) + ".xml"
    decl = '<?xml version="1.0" encoding="UTF-8"?>\n'

    def urlset(loc, extra="", dcl=decl):
        return dcl + f'<urlset xmlns="{NS}"><url><loc>{loc}</loc>{extra}</url></urlset>\n'

    def index(loc, dcl=decl):
        return dcl + f'<sitemapindex xmlns="{NS}"><sitemap><loc>{loc}</loc></sitemap></sitemapindex>\n'

    good = f"http://{host}/{d}/p{tok(4)}"
    out = []

    def one(cid, cls, data, status, error=None, findings=(), url=su):
        ident = "c" + tok(10)
        exit_code = {"clean": 0, "findings": 1, "error": 2}[status]
        verdict = {"clean": "clean", "findings": "failed-policy", "error": "could-not-evaluate"}[status]
        out.append({
            "id": cid, "class": cls,
            "files": {fname: data},
            "manifest": {"version": 1, "checks": [{"id": ident, "file": fname, "sitemapUrl": url}]},
            "expect": {"exit": exit_code, "verdict": verdict,
                       "checks": [{"id": ident, "status": status, "error": error,
                                   "findings": [list(f) for f in findings]}]},
        })

    # ---- E: UTF-16 without BOM (sentences 6, 8) --------------------------------------
    u8 = urlset(good)
    one("E1", "E", u8.encode("utf-16-le"), "findings", findings=[("xml_malformed", None)])
    one("E2", "E", u8.encode("utf-16-be"), "findings", findings=[("xml_malformed", None)])
    one("E3", "E", urlset(good, dcl="").encode("utf-16-le"), "findings", findings=[("xml_malformed", None)])
    one("E4", "E", urlset(good, dcl="").encode("utf-16-be"), "findings", findings=[("xml_malformed", None)])
    one("E5", "E", urlset(good, dcl='<?xml version="1.0" encoding="UTF-16"?>\n').encode("utf-16-le"),
        "findings", findings=[("xml_malformed", None)])
    one("E6", "E", u8.encode("utf-8"), "clean")
    one("E7", "E", b"\xef\xbb\xbf" + u8.encode("utf-8"), "clean")
    one("E8", "E", b"\xff\xfe" + u8.encode("utf-16-le"), "findings", findings=[("encoding_invalid", None)])
    one("E9", "E", urlset(good + "\u00e9").encode("utf-16-le"), "findings", findings=[("encoding_invalid", None)])

    # ---- U: values urlsplit would alter (sentences 21, 22, 4) --------------------------
    nab = [("loc_not_absolute", 1)]
    one("U1", "U", urlset(f"http://{host}/{d}/a\tb").encode(), "findings", findings=nab)
    one("U2", "U", urlset(f"http://{host}/{d}/a\nb").encode(), "findings", findings=nab)
    one("U3", "U", urlset(f"http://{host}/{d}/a&#13;b").encode(), "findings", findings=nab)
    one("U4", "U", urlset(f"http://{host[:3]}\t{host[3:]}/{d}/a").encode(), "findings", findings=nab)
    one("U5", "U", urlset(f"http:\n//{host}/{d}/a").encode(), "findings", findings=nab)
    one("U6", "U", index(f"http://{host}/x\ny.xml").encode(), "findings", findings=nab)
    one("U7", "U", urlset(good).encode(), "error", error="check_invalid", url=f"http://{host}/{d}\t/sitemap.xml")
    one("U8", "U", urlset(good).encode(), "error", error="check_invalid", url=f"http://{host}/{d}/site\rmap.xml")
    one("U9", "U", urlset(good).encode(), "error", error="check_invalid", url=" " + su)
    one("U10", "U", urlset(good).encode(), "error", error="check_invalid", url="\u0001" + su)
    one("U11", "U", urlset(f"\t{good}\r\n").encode(), "clean")
    one("U12", "U", urlset(f"http://{host}/{d}/a%09b%0Ac").encode(), "clean")
    one("U13", "U", urlset(good, extra=f'<x:note xmlns:x="urn:{tok(5)}">a\tb\nc</x:note>').encode(), "clean")

    # ---- R: repeated id of an earlier invalid check (sentence 4) -----------------------
    page = urlset(good).encode()

    def rep(cid, checks, expect_items):
        exit_code = 2 if any(s == "error" for s, _ in expect_items) else 0
        verdict = "could-not-evaluate" if exit_code == 2 else "clean"
        exp = []
        for raw, (status, error) in zip(checks, expect_items):
            ident = raw.get("id") if isinstance(raw, dict) and isinstance(raw.get("id"), str) else None
            exp.append({"id": ident, "status": status, "error": error, "findings": []})
        out.append({"id": cid, "class": "R", "files": {fname: page},
                    "manifest": {"version": 1, "checks": checks},
                    "expect": {"exit": exit_code, "verdict": verdict, "checks": exp}})

    bad = ("error", "check_invalid")
    ok = ("clean", None)
    i1, i2 = "r" + tok(9), "r" + tok(9)
    rep("R1", [{"id": i1, "sitemapUrl": su}, {"id": i1, "file": fname, "sitemapUrl": su}], [bad, bad])
    rep("R2", [{"id": i1, "file": fname}, {"id": i1, "file": fname, "sitemapUrl": su}], [bad, bad])
    rep("R3", [{"id": i1, "file": 7, "sitemapUrl": su}, {"id": i1, "file": fname, "sitemapUrl": su}], [bad, bad])
    rep("R4", [{"id": i1, "file": fname, "sitemapUrl": None}, {"id": i1, "file": fname, "sitemapUrl": su}],
        [bad, bad])
    rep("R5", [{"id": i1, "file": fname, "sitemapUrl": su}, {"id": i2, "sitemapUrl": su},
               {"id": i2, "file": fname, "sitemapUrl": su}], [ok, bad, bad])
    num = rng.randrange(100, 100000)
    rep("R6", [{"id": num, "file": fname, "sitemapUrl": su}, {"id": str(num), "file": fname, "sitemapUrl": su}],
        [bad, ok])
    rep("R7", [i1, {"id": i1, "file": fname, "sitemapUrl": su}], [bad, ok])
    mixed = "Q" + tok(8, "abcdefghijklmnopqrstuvwxyz")
    rep("R8", [{"id": mixed, "sitemapUrl": su}, {"id": mixed.lower(), "file": fname, "sitemapUrl": su}], [bad, ok])
    assert len(out) == WITNESSES
    return out


def materialize(w, cd):
    for name, data in w["files"].items():
        with open(os.path.join(cd, name), "wb") as fh:
            fh.write(data)
    with open(os.path.join(cd, "manifest.json"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(w["manifest"]))


def norm(lst):
    out = []
    for c in lst:
        fs = sorted({(f[0], f[1]) if isinstance(f, list) else (f.get("code"), f.get("entry"))
                     for f in c.get("findings") or []},
                    key=lambda t: (str(t[0]), -1 if t[1] is None else t[1]))
        out.append({"id": c.get("id"), "status": c.get("status"), "error": c.get("error"), "findings": fs})
    return out


def judge(w, rc, stdout):
    exp = w["expect"]
    if rc != exp["exit"]:
        return False, f"exit {rc} != {exp['exit']}"
    try:
        doc = json.loads(stdout)
    except Exception:
        return False, "stdout not JSON"
    if not isinstance(doc, dict) or doc.get("version") != 1 or doc.get("verdict") != exp["verdict"]:
        return False, "verdict mismatch: %r" % (doc.get("verdict") if isinstance(doc, dict) else None)
    got = doc.get("checks")
    if not isinstance(got, list):
        return False, "checks not a list"
    try:
        g, e = norm(got), norm(exp["checks"])
    except Exception as ex:
        return False, f"checks unreadable: {type(ex).__name__}"
    if g != e:
        for i, (a, b) in enumerate(zip(g, e)):
            if a != b:
                return False, (f"check {i}: got {a['status']}/{a['error']}/{a['findings']} "
                               f"want {b['status']}/{b['error']}/{b['findings']}")
        return False, f"check count {len(g)} != {len(e)}"
    return True, "match"


def sandbox_argv(cd, tool):
    return ["bwrap", "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib",
            "--symlink", "usr/lib64", "/lib64", "--symlink", "usr/bin", "/bin",
            "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
            "--ro-bind", cd, "/work", "--ro-bind", tool, "/tool/tool.py", "--chdir", "/work",
            "--unshare-all", "--die-with-parent", "--clearenv",
            "--setenv", "PATH", "/usr/bin", "--setenv", "LANG", "C.UTF-8", "--setenv", "PYTHONHASHSEED", "0",
            "/usr/bin/python3", "-B", "/tool/tool.py", "--manifest", "/work/manifest.json"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--revision")
    src.add_argument("--tool-file")
    ap.add_argument("--label", default="")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--out")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(6), "big")
    rec = {"predicate": PREDICATE, "witnesses": WITNESSES, "target": TARGET, "passed": None,
           "byClass": {}, "selftest": None, "met": False, "revision": None, "toolFile": a.tool_file,
           "label": a.label, "seed": seed,
           "counterSha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
           "toolSha256": None, "rows": [], "note": None}

    def finish(code):
        s = json.dumps(rec, indent=1)
        if a.out:
            with open(a.out, "w") as fh:
                fh.write(s + "\n")
        print(json.dumps({k: rec[k] for k in ("label", "revision", "passed", "witnesses", "byClass",
                                              "selftest", "met", "note")}))
        sys.exit(code)

    try:
        selftest = git(root, "show", f"{SELFTEST_REV}:{SELFTEST_PATH}")
    except Exception as ex:
        rec["note"] = f"selftest unreadable: {ex}"
        finish(2)
    if hashlib.sha256(selftest).hexdigest() != SELFTEST_SHA256:
        rec["note"] = "selftest sha256 mismatch"
        finish(2)
    ws = witnesses(random.Random(seed))
    with tempfile.TemporaryDirectory(prefix="kake-r40-count-") as td:
        tool = os.path.join(td, "tool.py")
        if a.revision:
            rev = git(root, "rev-parse", "--verify", f"{a.revision}^{{commit}}").decode().strip()
            rec["revision"] = rev
            try:
                data = git(root, "show", f"{rev}:{TOOL_PATH}")
            except subprocess.CalledProcessError:
                data = None
        else:
            try:
                data = open(a.tool_file, "rb").read()
            except OSError:
                data = None
        if data is None:
            rec["note"] = "tool absent"
            rec["passed"] = 0
            rec["rows"] = [{"id": w["id"], "class": w["class"], "pass": False, "why": "tool absent"} for w in ws]
            finish(1)
        rec["toolSha256"] = hashlib.sha256(data).hexdigest()
        with open(tool, "wb") as fh:
            fh.write(data)
        passed = 0
        by = {}
        for w in ws:
            cd = os.path.join(td, "case-" + w["id"])
            os.makedirs(cd)
            materialize(w, cd)
            try:
                p = subprocess.run(sandbox_argv(cd, tool), cwd=cd, capture_output=True, timeout=CASE_TIMEOUT)
                ok, why = judge(w, p.returncode, p.stdout.decode("utf-8", "replace"))
            except subprocess.TimeoutExpired:
                ok, why = False, "timeout"
            passed += ok
            c = by.setdefault(w["class"], [0, 0])
            c[0] += ok
            c[1] += 1
            rec["rows"].append({"id": w["id"], "class": w["class"], "pass": ok, "why": why[:300]})
        rec["passed"] = passed
        rec["byClass"] = {k: f"{v[0]}/{v[1]}" for k, v in sorted(by.items())}
        st = os.path.join(td, "selftest.py")
        with open(st, "wb") as fh:
            fh.write(selftest)
        try:
            p = subprocess.run(["/usr/bin/python3", "-B", st, "--tool", tool], cwd=td, capture_output=True,
                               timeout=SELFTEST_TIMEOUT)
            lines = [ln.strip() for ln in p.stdout.decode("utf-8", "replace").splitlines()
                     if ln.startswith(("PASS ", "FAIL "))]
            last = [ln for ln in lines if ln.startswith("PASS ") and "/" in ln]
            rec["selftest"] = {"exit": p.returncode, "summary": last[-1] if last else (lines[-1] if lines else None)}
        except subprocess.TimeoutExpired:
            rec["selftest"] = {"exit": None, "summary": "timeout"}
    st_ok = rec["selftest"]["exit"] == 0 and rec["selftest"]["summary"] == SELFTEST_PASS
    rec["met"] = len(rec["rows"]) == WITNESSES and passed >= TARGET and st_ok
    finish(0 if rec["met"] else 1)


if __name__ == "__main__":
    main()
