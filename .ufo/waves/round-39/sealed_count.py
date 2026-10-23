#!/usr/bin/env python3
"""Round-39 C1 sealed counter (frozen at declaration).

Scores one sitemap-audit tool against the sealed key. Exit 0 met, 1 not met, 2 cannot evaluate.

  python3 -B sealed_count.py --root <lane> --revision <rev> (--key-file <cases.json> | --key-revision <rev>)
  python3 -B sealed_count.py --root <lane> --tool-file <path> --label <name> (--key-file ... | --key-revision ...)

Each case runs the tool inside bubblewrap (no network, no lane, no key; only /usr, the case files
and the tool). The tool under test is `scripts/sitemap_audit.py` at --revision (read with `git show`), or the file
given by --tool-file (controls, mutants). A revision whose tree holds KEY_PATH is refused (exit 2)
unless it is only used with --key-revision as the key source.
"""
import argparse, base64, hashlib, json, os, subprocess, sys, tempfile

PREDICATE = "met: passed >= 24 of 24 sealed cases"
CASES = 24
TARGET = 24
KEY_SHA256 = "16440f62803e25fee5e17e77bae88636fa0c711b0fa26024ec78d4134767c10b"
KEY_PATH = ".ufo/waves/round-39/sealed/cases.json"
TOOL_PATH = "scripts/sitemap_audit.py"
CASE_TIMEOUT = 180


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, check=True).stdout


def materialize(case, d):
    for name, spec in case["files"].items():
        p = os.path.join(d, name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if "text" in spec:
            data = spec["text"].encode("utf-8")
        elif "b64" in spec:
            data = base64.b64decode(spec["b64"])
        else:
            g = spec["gen"]
            if g["kind"] == "entries":
                ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
                body = "".join(f"<url><loc>{g['base']}{i}</loc></url>" for i in range(g["n"]))
                data = (f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="{ns}">' + body + "</urlset>\n").encode()
            elif g["kind"] == "padded":
                body = g["body"].encode()
                pad = g["bytes"] - len(body) - len("<!---->")
                data = body + b"<!--" + b" " * pad + b"-->"
                assert len(data) == g["bytes"]
            else:
                raise ValueError(g["kind"])
        with open(p, "wb") as fh:
            fh.write(data)
    mp = os.path.join(d, "manifest.json")
    with open(mp, "w", encoding="utf-8") as fh:
        fh.write(case["manifestRaw"] if "manifestRaw" in case else json.dumps(case["manifest"]))
    return mp


def norm_checks(lst):
    out = []
    for c in lst:
        fs = sorted({(f[0], f[1]) if isinstance(f, list) else (f.get("code"), f.get("entry")) for f in c.get("findings") or []},
                    key=lambda t: (str(t[0]), -1 if t[1] is None else t[1]))
        out.append({"id": c.get("id"), "status": c.get("status"), "error": c.get("error"), "findings": fs})
    return out


def judge(case, rc, stdout):
    exp = case["expect"]
    if rc != exp["exit"]:
        return False, f"exit {rc} != {exp['exit']}"
    if "verdict" not in exp:
        return True, "exit matches"
    try:
        doc = json.loads(stdout)
    except Exception:
        return False, "stdout not JSON"
    if not isinstance(doc, dict):
        return False, "stdout not an object"
    if doc.get("version") != 1 or doc.get("verdict") != exp["verdict"]:
        return False, f"verdict {doc.get('verdict')!r} != {exp['verdict']!r}"
    if "error" in exp and doc.get("error") != exp["error"]:
        return False, f"error {doc.get('error')!r} != {exp['error']!r}"
    got = doc.get("checks")
    if not isinstance(got, list):
        return False, "checks not a list"
    try:
        g, e = norm_checks(got), norm_checks(exp["checks"])
    except Exception as ex:
        return False, f"checks unreadable: {type(ex).__name__}"
    if g != e:
        for i, (a, b) in enumerate(zip(g, e)):
            if a != b:
                return False, f"check {i} {b['id']}: got {a['status']}/{a['error']}/{a['findings']} want {b['status']}/{b['error']}/{b['findings']}"
        return False, f"check count {len(g)} != {len(e)}"
    return True, "match"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--revision")
    src.add_argument("--tool-file")
    ap.add_argument("--label", default="")
    k = ap.add_mutually_exclusive_group(required=True)
    k.add_argument("--key-file")
    k.add_argument("--key-revision")
    ap.add_argument("--out")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    rec = {"predicate": PREDICATE, "cases": CASES, "target": TARGET, "passed": None, "met": False,
           "revision": None, "toolFile": a.tool_file, "label": a.label, "keySha256": KEY_SHA256,
           "counterSha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(), "toolSha256": None,
           "rows": [], "note": None}

    def finish(code):
        s = json.dumps(rec, indent=1)
        if a.out:
            with open(a.out, "w") as fh:
                fh.write(s + "\n")
            with open(a.out[:-5] + ".exit" if a.out.endswith(".json") else a.out + ".exit", "w") as fh:
                fh.write(f"{code}\n")
        print(json.dumps({k: rec[k] for k in ("label", "revision", "passed", "cases", "met", "note")}))
        sys.exit(code)

    try:
        key = open(a.key_file, "rb").read() if a.key_file else git(root, "show", f"{a.key_revision}:{KEY_PATH}")
    except Exception as ex:
        rec["note"] = f"key unreadable: {ex}"
        finish(2)
    if hashlib.sha256(key).hexdigest() != KEY_SHA256:
        rec["note"] = "key sha256 mismatch"
        finish(2)
    cases = json.loads(key)["cases"]
    if len(cases) != CASES:
        rec["note"] = "case count mismatch"
        finish(2)
    with tempfile.TemporaryDirectory(prefix="kake-r39-count-") as td:
        tool = os.path.join(td, "tool.py")
        if a.revision:
            rev = git(root, "rev-parse", "--verify", f"{a.revision}^{{commit}}").decode().strip()
            rec["revision"] = rev
            if git(root, "ls-tree", "-r", "--name-only", rev, "--", KEY_PATH).strip():
                rec["note"] = "revision holds the sealed key; refused"
                finish(2)
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
            rec["rows"] = [{"id": c["id"], "pass": False, "why": "tool absent"} for c in cases]
            finish(1)
        rec["toolSha256"] = hashlib.sha256(data).hexdigest()
        with open(tool, "wb") as fh:
            fh.write(data)
        passed = 0
        for c in cases:
            cd = os.path.join(td, c["id"])
            os.makedirs(cd)
            mp = materialize(c, cd)
            # The tool runs in a bubblewrap sandbox: read-only /usr, the case directory at /work
            # (read-only), the tool at /tool, a private /tmp, no network, no lane, no key.
            argv = ["bwrap", "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib",
                    "--symlink", "usr/lib64", "/lib64", "--symlink", "usr/bin", "/bin",
                    "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
                    "--ro-bind", cd, "/work", "--ro-bind", tool, "/tool/tool.py", "--chdir", "/work",
                    "--unshare-all", "--die-with-parent", "--clearenv",
                    "--setenv", "PATH", "/usr/bin", "--setenv", "LANG", "C.UTF-8", "--setenv", "PYTHONHASHSEED", "0",
                    "/usr/bin/python3", "-B", "/tool/tool.py"] + (c["argv"] if "argv" in c else ["--manifest", "/work/manifest.json"])
            try:
                p = subprocess.run(argv, cwd=cd, capture_output=True, timeout=CASE_TIMEOUT)
                ok, why = judge(c, p.returncode, p.stdout.decode("utf-8", "replace"))
            except subprocess.TimeoutExpired:
                ok, why = False, "timeout"
            passed += ok
            rec["rows"].append({"id": c["id"], "pass": ok, "why": why[:400]})
    rec["passed"] = passed
    rec["met"] = len(rec["rows"]) == CASES and passed >= TARGET
    finish(0 if rec["met"] else 1)


if __name__ == "__main__":
    main()
