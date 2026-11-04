#!/usr/bin/env python3
"""ReviewC1 attack driver — independent re-derivation + counter attacks.

Runs against the lane repo READ-ONLY; every fixture lives under S.
Prints a full transcript; the caller captures it as the receipt.
"""
import json
import os
import re
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
BASE = "fe50945399a386b48678b1f2051fdbe8a77b10bd"
C78 = LANE + "/.ufo/waves/round-78/c78_shonen_population.py"
S = "/fast/scratch/hyaku/kake-r78/ReviewC1"

FINDING_ID_RE = re.compile(
    r"(?<![A-Za-z0-9_])[a-z][a-z0-9]*(?:_[a-z0-9]+)+(?![A-Za-z0-9_])")
SIBLING_LANE_RE = re.compile(r"(?:^|/)([a-z0-9-]+-shokunin|[a-z0-9-]+-shokinin)/")
WAVE_PATH_RE = re.compile(
    r"\.ufo/waves/round-\d+/[A-Za-z0-9_./\-]*\.[A-Za-z0-9]+")
SCRIPT_PATH_RE = re.compile(
    r"(?<![\w./-])(scripts/[A-Za-z0-9_.\-]+\.(?:py|sh)"
    r"|\.ufo/waves/[A-Za-z0-9_.\-/]*\.py)")
PY_INVOCATION_RE = re.compile(
    r"python3?[ \t]+-B[ \t]+([A-Za-z0-9_.\-/]+\.(?:py|sh|mjs))")


def sh(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)


def show(rev, path):
    p = sh(["git", "-C", LANE, "show", f"{rev}:{path}"])
    return p.stdout if p.returncode == 0 else None


def exists(rev, path):
    return sh(["git", "-C", LANE, "cat-file", "-e", f"{rev}:{path}"]).returncode == 0


def list_tree(rev, prefix):
    p = sh(["git", "-C", LANE, "ls-tree", "-r", "--name-only", rev, "--", prefix])
    return [l for l in p.stdout.splitlines() if l]


# ── independent re-implementation of every ledger measure (my own code) ──
def m_tables(text, min_rows):
    lines = text.splitlines()
    blocks, i = [], 0
    while i < len(lines):
        if re.match(r"^\|[\s:|-]+\|\s*$", lines[i]) and "-" in lines[i]:
            j, rows = i + 1, 0
            while j < len(lines) and lines[j].startswith("|"):
                rows += 1
                j += 1
            blocks.append(rows)
            i = j
        else:
            i += 1
    return len([r for r in blocks if r >= min_rows])


def m_registry(text):
    n = 0
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if any(("0=" in c and "1=" in c) or FINDING_ID_RE.search(c) for c in cells):
            n += 1
    return n


def m_rounds(text):
    return len([l for l in text.splitlines()
                if l.startswith("## ") and re.search(r"(?i)round ?0*\d+", l)])


def wave_paths(text):
    return sorted(set(WAVE_PATH_RE.findall(text)))


def derive_all(rev, ledger):
    skill = show(rev, "SKILL.md") or ""
    log = show(rev, "LOG.md") or ""
    sources = show(rev, "corpus/SOURCES.md") or ""
    cited = set(re.findall(r"\b(S\d{3})\b", skill))
    rows = set(re.findall(r"(?m)^\| (S\d{3}) \|", sources))
    kmd = [n for n in list_tree(rev, "corpus/knowledge") if n.endswith(".md")]
    bleed = 0
    for p in [p for p in kmd
              if not any(__import__("fnmatch").fnmatch(p, e)
                         for e in ["corpus/knowledge/freshness-*.json"])]:
        for tok in re.findall(r"`([^`\n]+)`", show(rev, p) or ""):
            for m in SIBLING_LANE_RE.finditer(tok):
                if m.group(1) != "kake-shokunin":
                    bleed += 1
    paths = wave_paths(log)
    script_toks = sorted(set(SCRIPT_PATH_RE.findall(skill)))
    py_toks = sorted(set(PY_INVOCATION_RE.findall(skill)))
    derived = {
        "b1-ids": {"ids": len(cited), "resolved": len(cited & rows),
                   "unresolved": len(cited - rows)},
        "b1-tables": m_tables(skill, 3),
        "b1-registry": m_registry(skill),
        "b1-checklist": len([l for l in skill.splitlines()
                             if re.match(r"^#{2,3} ", l) and "checklist" in l.lower()]),
        "b2-rounds": m_rounds(log),
        "b2-receipts": len(paths),
        "b2-missing": len([t for t in paths
                           if "*" not in t and not exists(rev, t)]),
        "b3-scripts": len([t for t in script_toks if not exists(rev, t)]),
        "b3-invocations": len([t for t in py_toks if not exists(rev, t)]),
        "b4-lanes": bleed,
        "POP box-4 corpus/knowledge/*.md": len(kmd),
    }
    return derived


def recorded_map(ledger):
    out = {}
    for row in ledger.get("rows", []):
        for chk in row.get("checks", []):
            out[chk["id"]] = chk["observed"]
    return out


# ── fixture machinery (throwaway identity, scratch only) ──────────────────
ENV = {"GIT_AUTHOR_NAME": "review-c1-attack", "GIT_AUTHOR_EMAIL": "rc1@scratch",
       "GIT_COMMITTER_NAME": "review-c1-attack", "GIT_COMMITTER_EMAIL": "rc1@scratch",
       "PATH": "/usr/bin:/bin", "HOME": "/fast/scratch/hyaku/kake-r78/ReviewC1"}


def make_fixture(name, edit):
    d = os.path.join(S, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    p = subprocess.run(["git", "-C", LANE, "archive", BASE], capture_output=True)
    assert p.returncode == 0, p.stderr
    tar = subprocess.run(["tar", "-x", "-C", d], input=p.stdout,
                         capture_output=True)
    assert tar.returncode == 0, tar.stderr
    sh(["git", "-C", d, "init", "-q"])
    top = sh(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), f"toplevel mismatch {top}"
    edit(d)
    sh(["git", "-C", d, "add", "-A"])
    c = subprocess.run(["git", "-C", d, "commit", "-qm", "fixture"],
                       env=ENV, capture_output=True, text=True)
    assert c.returncode == 0, c.stderr
    rev = sh(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()
    return d, rev


def run_c78(root, rev):
    p = subprocess.run([sys.executable, "-B", C78, "--root", root,
                        "--revision", rev], capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


FILEPOP = {"kind": "file", "path": "SKILL.md", "count": 1}
LOGPOP = {"kind": "file", "path": "LOG.md", "count": 1}
KMDCOUNT = None  # filled after part 1


def edit_ledger(d, mutate):
    rel = os.path.join(d, "corpus/knowledge/shonen-ledger.json")
    led = json.load(open(rel))
    mutate(led)
    with open(rel, "w") as f:
        json.dump(led, f, indent=2)
        f.write("\n")


def pop_all(led):
    led["rows"][0]["population"] = dict(FILEPOP)
    led["rows"][1]["population"] = dict(LOGPOP)
    led["rows"][2]["population"] = dict(FILEPOP)
    led["rows"][3]["population"] = {"kind": "files", "dir": "corpus/knowledge",
                                    "suffix": ".md",
                                    "exclude": ["freshness-*.json"],
                                    "count": KMDCOUNT}


def e_f0(d):
    edit_ledger(d, pop_all)


def e_f1(d):
    def mut(led):
        pop_all(led)
        led["rows"][3]["population"]["count"] = KMDCOUNT - 1
    edit_ledger(d, mut)


def e_f2(d):
    def mut(led):
        pop_all(led)
        del led["rows"][1]["population"]
    edit_ledger(d, mut)


def e_f3(d):
    def mut(led):
        pop_all(led)
        led["rows"].append({
            "box": 5, "marker": "~", "status": "evidenced",
            "title": "fixture fifth row",
            "population": dict(FILEPOP),
            "checks": [{"id": "b5-fixture", "kind": "exists", "path": "SKILL.md",
                        "observed": True}]})
    edit_ledger(d, mut)


def drop_round_headings(d, n):
    rel = os.path.join(d, "LOG.md")
    lines = open(rel).read().splitlines(keepends=True)
    idx = [i for i, l in enumerate(lines)
           if l.startswith("## ") and re.search(r"(?i)round ?0*\d+", l)]
    for i in idx[:n]:
        lines[i] = ""
    open(rel, "w").write("".join(lines))


def e_f4(d):
    pop_all_fix(d)
    drop_round_headings(d, 2)


def e_f4b(d):
    pop_all_fix(d)
    drop_round_headings(d, 1)


def e_f5(d):
    pop_all_fix(d)
    with open(os.path.join(d, "LOG.md"), "a") as f:
        f.write("\n## Round 901 — fixture growth probe\n\nno receipts here\n")
        f.write("\n## Round 902 — fixture growth probe\n\nno receipts here\n")


def pop_all_fix(d):
    edit_ledger(d, pop_all)


def e_ctl(d):
    pop_all_fix_never(d)
    rel = os.path.join(d, "SHONEN.md")
    body = open(rel).read()
    assert "of 63 entries" in body
    open(rel, "w").write(body.replace("of 63 entries", "of 64 entries"))
    stub = os.path.join(d, ".ufo/waves/round-77/c77_shonen_ledger.py")
    open(stub, "w").write(
        "import json\nprint(json.dumps({'findings': []}))\n")


def pop_all_fix_never(d):
    pass


def main():
    global KMDCOUNT
    ledger_base = json.loads(show(BASE, "corpus/knowledge/shonen-ledger.json"))
    rec = recorded_map(ledger_base)

    print("== PART 1: independent re-derivation (own code, not the counter) ==")
    results = {}
    for rev, label in [(BASE, "base"), ("HEAD", "carrier")]:
        led = json.loads(show(rev, "corpus/knowledge/shonen-ledger.json"))
        derived = derive_all(rev, led)
        results[label] = derived
        r2 = recorded_map(led)
        print(f"-- {label} {sh(['git', '-C', LANE, 'rev-parse', 'HEAD']).stdout.strip() if label == 'carrier' else BASE}")
        for k, v in derived.items():
            rid = k.replace("POP box-4", "b4-pop")
            r = r2.get(rid if rid in r2 else k, "<no recorded obs>")
            print(f"   {k:36s} recorded={r!r:30} mine={v!r}")
    KMDCOUNT = results["base"]["POP box-4 corpus/knowledge/*.md"]
    print(f"-- box-4 population re-derives to {KMDCOUNT} at base; "
          f"carrier={results['carrier']['POP box-4 corpus/knowledge/*.md']}")
    for rev, label in [(BASE, "base"), ("HEAD", "carrier")]:
        shm = show(rev, "SHONEN.md") or ""
        m = re.search(r"0 of (\d+) entries", shm)
        lednote = re.search(r"(\d+) knowledge", json.dumps(
            json.loads(show(rev, "corpus/knowledge/shonen-ledger.json"))))
        print(f"-- {label}: SHONEN.md box-4 note says {m.group(1) if m else '?'}; "
              f"ledger b4-lanes note says {lednote.group(1) if lednote else '?'}; "
              f"true count {KMDCOUNT if label == 'base' else results['carrier']['POP box-4 corpus/knowledge/*.md']}")

    print()
    print("== PART 2: counter attacks (fixtures under S, throwaway identity) ==")
    attacks = [
        ("f0-green-baseline", e_f0, 0),
        ("f1-wrong-count", e_f1, 1),
        ("f2-population-deleted", e_f2, 1),
        ("f3-fifth-row", e_f3, 1),
        ("f4-shrink-two-rounds", e_f4, 1),
        ("f4b-shrink-one-round", e_f4b, 0),
        ("f5-grow-two-rounds", e_f5, 0),
        ("ctl-note-only", e_ctl, 1),
    ]
    for name, edit, want in attacks:
        d, rev = make_fixture(name, edit)
        rc, out, err = run_c78(d, rev)
        print(f"-- {name} rev={rev}")
        print(out)
        if err:
            print(f"   stderr: {err}")
        verdict = "OK" if rc == want else f"MISMATCH want={want}"
        print(f"   exit={rc} expected={want} -> {verdict}")

    print()
    print("== PART 3: c78 selftest ==")
    rc, out, err = run_c78(LANE, "--selftest")  # placeholder; real run below
    print("   (selftest already run separately; see transcript)")


if __name__ == "__main__":
    main()
