#!/usr/bin/env python3
"""Round-31 C2 strict supplement (declared before any C2 after-measurement).

Wave-1 critic CriticC2Sizing built a hollow commit that the declared counter
(c2_quote_truth.py, frozen) scores 4/4: navigation or code quotes, rows
outside the Registry table, an entry whose only body line is a comment.  The
declared counter stays the measure; this supplement must also pass at the
landed commit.  Its quote-location rule follows the critic's prototype
(.ufo/waves/round-31/w1/CriticC2Sizing.md).  It reads committed bytes only.

  S1 quote located: for each id S057-S060 the lesson Gate quote lies in the
     page body (between the first and last "Copy page" markers of the
     retained text), appears in no other retained page (S057-S061), and has
     at least 4 words containing a letter.
  S2 registry row: the id's row lies inside the `## Registry` section of
     corpus/SOURCES.md and its source cell contains the receipt URL.
  S3 entry use: corpus/knowledge/render-web-services.md, with HTML comments
     removed, has at least 2 lines that cite the id and carry a curly-quoted
     span of 6 or more words that is an exact substring of that id's
     retained page body.
  S4 render.yaml check: the entry has a `## ` section whose heading names
     render.yaml; that section names the blob `d17ab7e5` and, for each key
     type, runtime, dockerfilePath, dockerContext, healthCheckPath, envVars
     and sync, has a line naming the key in backticks and carrying a
     curly-quoted span of 6 or more words that is an exact substring of the
     body of one of S057-S060.
  S5 retained bytes: for S057-S061 the gunzipped .html.gz body sha256 and the
     .txt sha256 equal receipts.json, and the visible text re-derived from
     the body with the fetcher's rule equals the .txt bytes.

Usage: python3 -B c2_strict_checks.py --root <lane> --revision <commit>
Exit 0 when S1-S5 all pass; 1 otherwise; 2 on bad input.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import html
import json
import os
import re
import subprocess
import sys

IDS = ["S057", "S058", "S059", "S060"]
ALL = IDS + ["S061"]
SRC = ".ufo/waves/round-31/sources"
ENTRY = "corpus/knowledge/render-web-services.md"
LESSON = "corpus/lessons/round-31.md"
REGISTRY = "corpus/SOURCES.md"
KEYS = ["type", "runtime", "dockerfilePath", "dockerContext", "healthCheckPath", "envVars", "sync"]
QUOTE = re.compile(r"\u201c([^\u201c\u201d]+)\u201d")


def show(root, rev, path):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    p = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"], capture_output=True, env=env)
    return p.stdout if p.returncode == 0 else None


def collapse(s):
    return re.sub(r"\s+", " ", s).strip()


def visible_text(body: str) -> str:
    t = re.sub(r"(?is)<(script|style)\b.*?</\1\s*>", " ", body)
    t = re.sub(r"(?s)<!--.*?-->", " ", t)
    t = re.sub(r"(?s)<[^>]+>", " ", t)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip() + "\n"


def section(text, pred):
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = pred(line)
            continue
        if inside:
            out.append(line)
    return out


def body_of(text):
    marks = [m.start() for m in re.finditer("Copy page", text)]
    return text[marks[0]:marks[-1]] if len(marks) >= 2 else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision", required=True)
    a = ap.parse_args()
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    rp = subprocess.run(["git", "-C", a.root, "rev-parse", "--verify", "--quiet", f"{a.revision}^{{commit}}"],
                        capture_output=True, env=env)
    if rp.returncode != 0:
        print(json.dumps({"error": "revision not found", "revision": a.revision}))
        return 2
    rev = rp.stdout.decode().strip()
    try:
        receipts = json.loads(show(a.root, rev, f"{SRC}/receipts.json") or b"{}")
    except ValueError:
        receipts = {}
    texts, bodies, s5 = {}, {}, {}
    for sid in ALL:
        raw = show(a.root, rev, f"{SRC}/{sid}.txt")
        gz = show(a.root, rev, f"{SRC}/{sid}.html.gz")
        rec = receipts.get(sid, {}) if isinstance(receipts, dict) else {}
        ok = False
        if raw is not None and gz is not None:
            try:
                body = gzip.decompress(gz)
                ok = (hashlib.sha256(body).hexdigest() == rec.get("bodySha256")
                      and hashlib.sha256(raw).hexdigest() == rec.get("textSha256")
                      and visible_text(body.decode("utf-8", "replace")).encode("utf-8") == raw)
            except OSError:
                ok = False
        s5[sid] = ok
        texts[sid] = collapse(raw.decode("utf-8", "replace")) if raw is not None else ""
        bodies[sid] = body_of(texts[sid])
    lesson = (show(a.root, rev, LESSON) or b"").decode("utf-8", "replace")
    registry = (show(a.root, rev, REGISTRY) or b"").decode("utf-8", "replace")
    entry = (show(a.root, rev, ENTRY) or b"").decode("utf-8", "replace")
    entry = re.sub(r"(?s)<!--.*?-->", " ", entry)
    gate = section(lesson, lambda l: l.strip() == "## Gate")
    reg_lines = section(registry, lambda l: l.strip() == "## Registry")

    def verified(span, ids):
        q = collapse(span)
        return len(q.split()) >= 6 and any(q in bodies[i] for i in ids)

    per_id = []
    for sid in IDS:
        url = (receipts.get(sid) or {}).get("url") if isinstance(receipts, dict) else None
        gl = [l for l in gate if l.startswith(f"- {sid} \u2014 ")]
        qs = QUOTE.findall(gl[0]) if len(gl) == 1 else []
        q = collapse(qs[0]) if len(qs) == 1 else ""
        s1 = (bool(q) and q in bodies[sid] and not any(q in texts[o] for o in ALL if o != sid)
              and sum(1 for w in q.split() if re.search(r"[A-Za-z]", w)) >= 4)
        row = [l for l in reg_lines if re.match(rf"^\s{{0,3}}\|\s*{sid}\s*\|", l)]
        cells = [c.strip() for c in row[0].strip().strip("|").split("|")] if len(row) == 1 else []
        s2 = bool(url and len(cells) >= 2 and url in cells[1])
        uses = [l for l in entry.splitlines()
                if re.search(rf"\b{sid}\b", l) and any(verified(s, [sid]) for s in QUOTE.findall(l))]
        s3 = len(uses) >= 2
        per_id.append({"id": sid, "S1": s1, "S2": s2, "S3": s3, "S3lines": len(uses), "quote": q})
    yaml_sec = section(entry, lambda l: "render.yaml" in l)
    keys = {}
    for key in KEYS:
        keys[key] = any(f"`{key}" in l and any(verified(s, IDS) for s in QUOTE.findall(l)) for l in yaml_sec)
    s4 = bool(yaml_sec) and any("d17ab7e5" in l for l in yaml_sec) and all(keys.values())
    checks = {
        "S1": all(r["S1"] for r in per_id),
        "S2": all(r["S2"] for r in per_id),
        "S3": all(r["S3"] for r in per_id),
        "S4": s4,
        "S5": all(s5.values()),
    }
    passed = sum(checks.values())
    print(json.dumps({"checker": "kake-r31-c2-strict",
                      "checkerSha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
                      "revision": rev, "passed": passed, "total": len(checks), "checks": checks,
                      "ids": per_id, "renderYamlKeys": keys, "retainedBytes": s5}, indent=1, ensure_ascii=False))
    print(f"C2 strict {passed}/{len(checks)} at {rev}", file=sys.stderr)
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
