#!/usr/bin/env python3
"""ReviewC1 round-96 attack driver. Writes ONLY under /fast/scratch/hyaku/kake-r96/ReviewC1.

Fixture recipe per route: restore all touched paths to base bytes, apply one
defect overlay, commit in the ONE fixture repo (toplevel asserted), score the
defect rev with the FROZEN lane counters (bytes digest-verified) via CLI.

This is the exact script that produced receipts/runs/*.txt (45-file receipt
set): base source plus the two recorded fixes (lazy corrected_entry via
callable overlay values; fixture populated with the full base tree via
copytree before the first commit) plus the full-mode control reproductions.
"""
import hashlib, json, os, shutil, subprocess, sys, traceback

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
S    = "/fast/scratch/hyaku/kake-r96/ReviewC1"
FX   = S + "/fx"
BASETREE = S + "/base-tree"
RUNS = S + "/runs"
C96  = LANE + "/.ufo/waves/round-96/c96_selfassess.py"
C95  = LANE + "/.ufo/waves/round-95/c95_selfassess.py"
SURF96 = LANE + "/.ufo/waves/round-96/frozen/c1-surfaces.json"
SURF95 = LANE + "/.ufo/waves/round-95/frozen/c1-surfaces.json"
BASE = "bde9869144f69c5a459c0d2c93f5135922fe3a8d"

def log(msg):
    print(msg, flush=True)

def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()

def git(*args, cwd=None):
    return subprocess.run(["git"] + list(args), capture_output=True, cwd=cwd or FX)

def base_bytes(rel):
    p = os.path.join(BASETREE, rel)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8", errors="surrogateescape") as fh:
            return fh.read()
    return None

MIST = "\n## Mistakes\n\n| # | Class |\n|---|---|\n| 1 | a |\n"

def lesson(gate_heading, body_lines):
    return "# r96\n\n" + gate_heading + "\n\n" + "\n".join(body_lines) + "\n" + MIST

ENTRY = "corpus/knowledge/conditional-list-membership.md"

def corrected_entry():
    txt = base_bytes(ENTRY)
    marker = "correction: [r96-correction 2026-11-05] head repaired in place; presence-pinned surface (R95-1 route).\n"
    assert "recheck: 180d\n" in txt
    return txt.replace("recheck: 180d\n", "recheck: 180d\n" + marker, 1)

ROUTES = [
    ("NG01r-heading-over-junk-body",
     {"corpus/lessons/round-96.md":
      lesson("## Gate — admit X, reject Y", ["Junk line one.", "Junk line two."])},
     ("E1", "no whole-word"), "pred_admits"),
    ("NG08r-heading-decision-summary",
     {"corpus/lessons/round-96.md":
      lesson("## Gate — admits A; rejects B; summary", ["Prose line alpha.", "Prose line beta."])},
     ("E1", "no whole-word"), "pred_admits"),
    ("NG11a-substring-admittta-rejectable",
     {"corpus/lessons/round-96.md":
      lesson("## Gate", ["We admitta nothing; this is a rejectable item.", "Another junk line."])},
     ("E1", "no whole-word"), "pred_admits"),
    ("NG11b-substring-admin-rejector",
     {"corpus/lessons/round-96.md":
      lesson("## Gate", ["The admin recorded nothing; the rejector script ran idle.",
                         "Another junk line."])},
     ("E1", "no whole-word"), "pred_admits"),
    ("NG11c-substring-codespan-no-wholeword",
     {"corpus/lessons/round-96.md":
      lesson("## Gate", ["Dry-run `admits_more` and `auto_rejected` flags only.",
                         "Another junk line."])},
     ("E1", "no whole-word"), "pred_admits"),
    ("RX01-decisions-only-in-html-comment",
     {"corpus/lessons/round-96.md":
      lesson("## Gate", ["<!-- decisions recorded here: admit X, reject Y -->",
                         "No decisions recorded in prose."])},
     None, "pred_admits"),
    ("RX02-decisions-only-in-fenced-code",
     {"corpus/lessons/round-96.md":
      lesson("## Gate", ["```", "admit: sample output line one",
                         "reject: sample output line two", "```",
                         "Trailing junk line."])},
     None, "pred_admits"),
    ("RX03a-phantom-gate-heading-in-fence",
     {"corpus/lessons/round-96.md":
      "# r96\n\nExample template quoted verbatim:\n\n```\n"
      "## Gate — admit X, reject Y\nJunk line one.\nJunk line two.\n```\n" + MIST},
     ("E1", "no whole-word"), "pred_admits"),
    ("RX03b-entire-gate-inside-fence",
     {"corpus/lessons/round-96.md":
      "# r96\n\nExample template quoted verbatim:\n\n```\n"
      "## Gate\nadmit: template admission line.\nreject: template rejection line.\n"
      "Junk fence line.\n```\n" + MIST},
     None, "pred_admits"),
    ("RX04-entry-deleted-after-base",
     {ENTRY: None},
     ("IDENT", "entry:" + ENTRY), "pred_refuses"),
    ("RX05-entry-head-correction-must-not-fire",
     {ENTRY: lambda: corrected_entry()},
     None, "pred_refuses_diff"),
    ("RX07-tokens-only-in-mistakes-section",
     {"corpus/lessons/round-96.md":
      "# r96\n\n## Gate\n\nJunk line one.\nJunk line two.\n"
      "\n## Mistakes\n\n| # | Class |\n|---|---|\n"
      "| 1 | the gate admits X and rejects Y (tokens live in this row) |\n"},
     ("E1", "no whole-word"), "pred_refuses"),
    ("RX09-subdir-roundno-hijack",
     {"corpus/lessons/round-95/round-96.md":
      "# r96 (misfiled one level deep)\n\n## Gate\n\nlorem ipsum dolor sit amet.\n"
      "consectetur adipiscing elit sed do.\n" + MIST},
     None, "pred_refuses"),
]

ALL_TOUCHED = sorted({p for _, ov, _, _ in ROUTES for p in ov})

def restore_all():
    for rel in ALL_TOUCHED:
        dest = os.path.join(FX, rel)
        content = base_bytes(rel)
        if content is None:
            if os.path.exists(dest) or os.path.islink(dest):
                os.remove(dest)
        else:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8", errors="surrogateescape") as fh:
                fh.write(content)

def commit_overlay(overlay, msg):
    restore_all()
    for rel, content in overlay.items():
        if callable(content):
            content = content()
        dest = os.path.join(FX, rel)
        if content is None:
            if os.path.exists(dest):
                os.remove(dest)
        else:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "w", encoding="utf-8", errors="surrogateescape") as fh:
                fh.write(content)
    top = git("rev-parse", "--show-toplevel").stdout.decode().strip()
    assert top == FX, "toplevel %r != fixture %r" % (top, FX)
    assert git("add", "-A").returncode == 0
    assert git("-c", "user.email=reviewc1@example.invalid",
               "-c", "user.name=reviewc1", "commit", "-q", "-m", msg).returncode == 0
    return git("rev-parse", "HEAD").stdout.decode().strip()

ENV = None

def run_counter(counter, rev, extra=()):
    cmd = ["python3", "-B", counter, "--root", FX, "--revision", rev,
           "--verdict-only"] + list(extra)
    p = subprocess.run(cmd, capture_output=True, timeout=900, env=ENV, cwd=S)
    out = p.stdout.decode("utf-8", "replace")
    err = p.stderr.decode("utf-8", "replace")
    lines = out.splitlines()
    line1 = lines[0] if lines else ""
    detail = {}
    if len(lines) > 1:
        try:
            detail = json.loads(lines[1])
        except Exception:
            detail = {"raw": lines[1][:400]}
    return {"cmd": cmd, "rc": p.returncode, "line1": line1, "detail": detail,
            "stderr": err[:400], "stdout": out}

def write_receipt(name, res, expect, classification, note=""):
    path = os.path.join(RUNS, name + ".txt")
    findings = res["detail"].get("mismatches", [])
    ident = res["detail"].get("identity_missing", [])
    with open(path, "w") as fh:
        fh.write("# route: %s\n" % name)
        fh.write("# command: %s\n" % " ".join(res["cmd"]))
        fh.write("rc=%d\n" % res["rc"])
        fh.write("line1: %s\n" % res["line1"])
        fh.write("findings: %s\n" % json.dumps(
            [{"class": f.get("class"), "detail": f.get("detail")} for f in findings]))
        fh.write("identity: %s\n" % json.dumps(ident[:12]))
        if res["stderr"]:
            fh.write("stderr: %s\n" % res["stderr"])
        fh.write("expect: %s\n" % json.dumps(expect))
        fh.write("classification: %s\n" % classification)
        if note:
            fh.write("note: %s\n" % note)
    return path

def classify(c96res, c95res, expect, pred_expect):
    verdict = "clean" if "verdict=clean" in c96res["line1"] else "failed"
    findings = c96res["detail"].get("mismatches", [])
    ident = c96res["detail"].get("identity_missing", [])
    if expect is None:
        cls96 = "clean-expected"
        ok96 = verdict == "clean"
    elif expect[0] == "IDENT":
        hit = any(expect[1] in x for x in ident)
        cls96 = "refused-identity" if hit else "MISS"
        ok96 = (verdict == "failed") and hit
    else:
        hit = any(f.get("class") == expect[0] and expect[1] in f.get("detail", "")
                  for f in findings)
        cls96 = "refused-named" if hit else "MISS"
        ok96 = (verdict == "failed") and hit
    mm95 = c95res["detail"].get("mismatches", [])
    ident95 = c95res["detail"].get("identity_missing", [])
    if pred_expect == "pred_admits":
        ok95 = len(mm95) == 0
        cls95 = "pred-admits(mismatches=0)" if ok95 else "PRED-REFUSES(FINDING)"
    elif pred_expect in ("pred_refuses", "pred_refuses_diff"):
        ok95 = (len(mm95) > 0) or len(ident95) > 0
        cls95 = "pred-refuses" if ok95 else "pred-admits"
    else:
        ok95, cls95 = True, "n/a"
    return cls96, cls95, ok96, ok95, verdict, "clean" if "verdict=clean" in c95res["line1"] else "failed"

def main():
    global ENV
    os.makedirs(RUNS, exist_ok=True)
    os.makedirs(S + "/tmp", exist_ok=True)
    summary = {"digests": {}, "harness": {}, "routes": {}, "process": {}}

    pins = {"c96": (C96, "a282da654d5ee6af923abb2cae4bd0a4fd6e4309db81de5a67999ed7b25ad134"),
            "c95": (C95, "8fd27d626883f2b6852ea2ee425706a77a72eeaee10ef740b8e0fc15ac03b193"),
            "surf96": (SURF96, "c1caa585b6e752a4fd1ea8597af65db393556db45e47a5007deb2c66ab062249"),
            "surf95": (SURF95, "00a04c9a68f00de1561d70822a8ff3cab718583de4cd2cbf6ebd06e87b5d47b8")}
    for k, (p, want) in pins.items():
        got = sha(p)
        summary["digests"][k] = {"want": want, "got": got, "ok": got == want}
        assert got == want, "digest drift on %s" % k
    log("[digests] all four pins verified OK")

    ENV = dict(os.environ)
    ENV["PYTHONPATH"] = ""
    ENV["TMPDIR"] = S + "/tmp"
    ENV.pop("GIT_DIR", None); ENV.pop("GIT_WORK_TREE", None)

    if not os.path.exists(os.path.join(FX, ".git")):
        os.makedirs(FX)
        assert git("init", "-q").returncode == 0
        git("config", "user.email", "reviewc1@example.invalid")
        git("config", "user.name", "reviewc1")
    if not os.path.exists(BASETREE):
        os.makedirs(BASETREE)
        with open(os.path.join(BASETREE, "..", "base.tar"), "wb") as out:
            r = subprocess.run(["git", "-C", LANE, "archive", BASE], stdout=out)
        assert r.returncode == 0
        r = subprocess.run(["tar", "-x", "-C", BASETREE, "-f", S + "/base.tar"])
        assert r.returncode == 0
        os.remove(S + "/base.tar")
    if git("rev-parse", "HEAD").returncode != 0:
        shutil.copytree(BASETREE, FX, dirs_exist_ok=True)
        restore_all()
        top = git("rev-parse", "--show-toplevel").stdout.decode().strip()
        assert top == FX, top
        assert git("add", "-A").returncode == 0
        assert git("commit", "-q", "-m", "base bde98691 extract").returncode == 0
    base_rev = git("rev-parse", "HEAD").stdout.decode().strip()
    log("[fixture] base committed at %s" % base_rev[:12])

    r96 = run_counter(C96, base_rev)
    r95 = run_counter(C95, base_rev)
    ok96 = r96["rc"] == 0 and "verdict=clean" in r96["line1"]
    ok95 = r95["rc"] == 1 and r95["detail"].get("mismatches") == []
    summary["harness"] = {"c96_base": {"rc": r96["rc"], "line1": r96["line1"], "ok": ok96},
                          "c95_base": {"rc": r95["rc"], "line1": r95["line1"], "ok": ok95}}
    write_receipt("_harness-c96-base-clean", r96, ["verdict=clean", "pins=ok"],
                  "harness-validation" if ok96 else "HARNESS-FAIL")
    write_receipt("_harness-c95-base-predstate", r95,
                  ["mismatches=0", "pins=identity expected"],
                  "harness-validation" if ok95 else "HARNESS-FAIL")
    log("[harness] c96@base rc=%d %s | c95@base rc=%d mismatches=%d"
        % (r96["rc"], r96["line1"][-60:], r95["rc"], len(r95["detail"].get("mismatches", []))))

    for tag, counter, ctrl_path, ctrl_mark in (
            ("succ", C96, LANE + "/.ufo/waves/round-96/controls/c1-successor-at-base.txt", "C1v96"),
            ("pred", C95, LANE + "/.ufo/waves/round-96/controls/base-c1-predecessor.txt", "C1v95")):
        cmd = ["python3", "-B", counter, "--root", FX, "--revision", base_rev,
               "--work", S + "/work-" + tag]
        p = subprocess.run(cmd, capture_output=True, timeout=1200, env=ENV, cwd=S)
        out = p.stdout.decode("utf-8", "replace")
        line1 = out.splitlines()[0] if out.splitlines() else ""
        ctrl_line = ""
        with open(ctrl_path) as fh:
            for ln in fh:
                if ln.startswith(ctrl_mark):
                    ctrl_line = ln.rstrip("\n")
                    break
        match = line1 == ctrl_line
        with open(os.path.join(RUNS, "_repro-%s-full-base.txt" % tag), "w") as fh:
            fh.write("# command: %s\nrc=%d\nline1: %s\ncontrol: %s\nline1==control: %s\n"
                     % (" ".join(cmd), p.returncode, line1, ctrl_path, match))
        summary["harness"]["repro_" + tag] = {"rc": p.returncode, "match": match,
                                              "line1": line1, "ctrl_line": ctrl_line}
        log("[repro-%s] rc=%d line1==control: %s" % (tag, p.returncode, match))

    fg, refused, unexpected = [], [], []
    for name, overlay, expect, pred in ROUTES:
        try:
            rev = commit_overlay(overlay, name)
            c96res = run_counter(C96, rev)
            c95res = run_counter(C95, rev)
            cls96, cls95, ok96, ok95, verdict, v95 = classify(
                c96res, c95res, expect, pred)
            if expect is None and name != "RX05-entry-head-correction-must-not-fire":
                if verdict == "clean" and c96res["rc"] == 0:
                    cls96 = "FALSE-GREEN"
                    fg.append(name)
                else:
                    cls96 = "refused-cleancheck"
                    refused.append(name)
            elif expect is not None and ok96:
                refused.append(name)
            elif expect is not None and not ok96:
                unexpected.append(name)
            if not ok95:
                unexpected.append(name + " [PRED:" + cls95 + "]")
            write_receipt(name, c96res, {"96": expect, "pred": pred},
                          cls96 + " | " + cls95)
            write_receipt(name + "__pred", c95res,
                          {"95": "mismatches=0" if pred == "pred_admits" else "refusal"},
                          cls95)
            summary["routes"][name] = {"rev": rev, "c96": cls96, "c95": cls95,
                                       "line1_96": c96res["line1"],
                                       "line1_95": c95res["line1"], "ok": ok96 and ok95}
            log("[route] %-46s rev=%s c96=%s c95=%s" % (name, rev[:8], cls96, cls95))
        except Exception:
            unexpected.append(name + " [EXC]")
            summary["routes"][name] = {"error": traceback.format_exc()[-800:]}
            log("[route] %s EXCEPTION" % name)
        restore_all()
        git("add", "-A")
        git("-c", "user.email=reviewc1@example.invalid", "-c", "user.name=reviewc1",
            "commit", "-q", "-m", "restore-base")

    summary["tally"] = {"refused": sorted(refused), "false_greens": sorted(fg),
                        "unexpected": unexpected}
    with open(os.path.join(RUNS, "_summary_routes.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    log("[tally] refused=%d false_greens=%s unexpected=%s"
        % (len(refused), fg, unexpected))

if __name__ == "__main__":
    main()
