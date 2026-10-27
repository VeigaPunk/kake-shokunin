"""Scratch integration driver: build a synthetic round-61 after-state on a clone of the real lane registry
(read-only clone; nothing outside the scratch dir is touched) and run c61_recheck_pins.py against it.
This is a fixture, not the lane after-state: bodies are synthetic, no network fetch happens.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

S = "/fast/scratch/hyaku/kake-r61/ExecC3Counter"
CLONE = os.path.join(S, "integ")
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
COUNTER = os.path.join(LANE, ".ufo/waves/round-61/c61_recheck_pins.py")
DUE = [f"S{i:03d}" for i in range(1, 11)]
PINS = {sid: ("2027-01-17" if sid <= "S007" else "2027-10-19") for sid in DUE}
REGISTRY = os.path.join(CLONE, "corpus/SOURCES.md")
LESSON = os.path.join(CLONE, "corpus/lessons/round-61.md")
RECHECK = os.path.join(CLONE, ".ufo/waves/round-61/recheck")


def git(*args, **kw):
    return subprocess.run(["git", "-C", CLONE, *args], check=kw.pop("check", True),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def cell_line(line, index, value):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    cells[index] = value
    return "| " + " | ".join(cells) + " |"


def row_urls(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    out = []
    for token in cells[1].split():
        token = token.strip(".,;:)]}\"'")
        if token.startswith(("http://", "https://")) and token not in out:
            out.append(token)
    return out


def commit(message, at="HEAD"):
    if at:
        git("reset", "-q", "--hard", at)
    git("add", "-A")
    git("-c", "user.name=selftest", "-c", "user.email=selftest@local", "commit", "-q", "-m", message)
    return git("rev-parse", "HEAD").stdout.strip()


def build_green(at="eaa9177"):
    """Ten pins + ten bodies + ten receipts + ten Gate lines, on the real 167-row registry."""
    if at:
        git("reset", "-q", "--hard", at)
    text = open(REGISTRY, encoding="utf-8").read()
    lines = text.split("\n")
    bodies, gates, receipts = {}, [], []
    for i, line in enumerate(lines):
        m = re.match(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|", line)
        if not m or m.group(1) not in DUE:
            continue
        sid = m.group(1)
        lines[i] = cell_line(line, 9, PINS[sid])
        quote = f"Fresh {sid} synthetic body states the recheck pin rule holds"
        blob = (f"<html><head><title>Synthetic {sid}</title></head><body><h1>Synthetic {sid}</h1>"
                f"<p>{quote}.</p></body></html>\n").encode("utf-8")
        bodies[sid] = blob
        urls = row_urls(line)
        assert urls, sid
        gates.append(f"- {sid} — {urls[0]} — accessed 2026-10-27 — § Synthetic anchor — quote: \"{quote}\" "
                     f"({len(quote.split())} units; sha256 {hashlib.sha256(blob).hexdigest()}, {len(blob)} bytes, HTTP 200)")
        receipts.append({"url": urls[0], "effectiveUrl": urls[0], "status": 200,
                         "sha256": hashlib.sha256(blob).hexdigest(), "bytes": len(blob),
                         "fetchedAt": f"2026-10-27T05:0{sid[-1]}:00+00:00", "userAgent": "kake-shokunin-round61"})
    assert len(bodies) == 10, len(bodies)
    open(REGISTRY, "w", encoding="utf-8").write("\n".join(lines))
    os.makedirs(RECHECK, exist_ok=True)
    for sid, blob in bodies.items():
        with open(os.path.join(RECHECK, f"{sid}.html"), "wb") as handle:
            handle.write(blob)
    with open(os.path.join(RECHECK, "receipts.json"), "w", encoding="utf-8") as handle:
        json.dump({"receipts": receipts}, handle, indent=1)
        handle.write("\n")
    with open(LESSON, "w", encoding="utf-8") as handle:
        handle.write("# Round 61 — lessons (synthetic fixture)\n\n## Gate\n\n"
                     "Synthetic rows re-verified; quote spans follow the C3 rules.\n\n"
                     + "\n".join(gates) + "\n")
    return commit("synthetic after-state", at=None)


def run(rev):
    env = dict(os.environ, TMPDIR=os.path.join(S, "tmp"))
    return subprocess.run([sys.executable, "-B", COUNTER, "--root", CLONE, "--revision", rev],
                          capture_output=True, text=True, env=env)


def main():
    rev = build_green()
    print("clone toplevel:", git("rev-parse", "--show-toplevel").stdout.strip())
    print("synthetic revision:", rev)
    out = run(rev)
    print(out.stdout)
    print("counter exit:", out.returncode, "stderr:", out.stderr.strip())
    # negative: a non-due row rewritten
    lines = open(REGISTRY, encoding="utf-8").read().split("\n")
    for i, line in enumerate(lines):
        m = re.match(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|", line)
        if m and m.group(1) == "S050":
            lines[i] = cell_line(line, 6, "rewritten teaches cell for S050")
    open(REGISTRY, "w", encoding="utf-8").write("\n".join(lines))
    rev2 = commit("mutate non-due row S050", at=None)
    out = run(rev2)
    print("\n".join(line for line in out.stdout.splitlines() if "C6" in line or "conditions_passed" in line
                    or "EXIT" in line or "outside the due set" in line))
    print("mutant exit:", out.returncode)


if __name__ == "__main__":
    main()
