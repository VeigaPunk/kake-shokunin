#!/usr/bin/env python3
"""Round-35 sealed counters for C1 (link-preview audit repair) and C2 (security.txt entry).

The case set (C1) and the probe set (C2) were written by the L1 before this file and before
any build. Until the reveal commit they live outside the lane; this file pins their sha256, so
neither can change after the declaration. The builder of the tool and the drafter of the entry
never see them. A revision that already contains a key file cannot be measured (exit 2): the
measured bytes must predate the reveal, so nothing measured can be a copy of a key.

Usage:
  python3 -B sealed_count.py c1 --root ROOT --revision REV (--key-revision KREV | --key-file PATH)
  python3 -B sealed_count.py c2 --root ROOT --revision REV (--key-revision KREV | --key-file PATH)

C1: the tool `scripts/link_preview_audit.py` at REV runs on each of the 24 sealed cases,
materialized under a fresh random directory. A case passes when the exit code, the verdict and
the multiset of findings projected on (reason, page, property) all equal the sealed
expectation. Declared target: passed >= 22 of 24 (exit 0 when met, 1 when not).

C2: the entry `corpus/knowledge/security-txt-publishing.md` at REV is judged on five conditions:
  entry      the file exists;
  size       at most 1500 whitespace-separated words;
  copied     the nine retained source texts pinned below are intact at REV, and at most 25% of
             the entry's 8-word shingles occur in the retained round-35 source texts
             (`.ufo/waves/round-35/sources/*.txt` at REV), so a transcription fails;
  cites      it cites at least 3 distinct ids S078-S099 (word boundary), each a single
             `## Registry` row of `corpus/SOURCES.md` at REV with status `mined`, opened
             `2026-10-22` and the entry path in its used-by cell;
  probes     at least 9 of the 12 sealed probes match the normalized entry text.
`met` is all five. Declared target: met true (exit 0 when met, 1 when not).

Exit 2: could not evaluate (unresolved revision, key sha256 mismatch, key visible at REV).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

C1_KEY_PATH = ".ufo/waves/round-35/sealed/c1-cases.json"
C2_KEY_PATH = ".ufo/waves/round-35/sealed/c2-probes.json"
C1_KEY_SHA256 = "a861dccdf63c21b2f731b5845ec016e216bee8bd7ad62df646d5e47e8bc1a391"
C2_KEY_SHA256 = "111bceea7766ea29ee5a31646a455f3a593053a00b4c358e367024d1b458d61d"
TOOL = "scripts/link_preview_audit.py"
ENTRY = "corpus/knowledge/security-txt-publishing.md"
SOURCES_MD = "corpus/SOURCES.md"
SOURCE_TEXT_DIR = ".ufo/waves/round-35/sources/"
C1_TARGET = 22
C2_PROBE_TARGET = 9
C2_MAX_WORDS = 1500
C2_MAX_COPIED = 0.25
C2_MIN_CITES = 3
SHINGLE = 8
# The retained source texts as opened before the declaration; the copied condition fails when any
# is missing or altered at the measured revision (a transcription cannot pass by deleting them).
PINNED_TEXTS = {
    "S006.txt": "9ddf8eb286701b7f567167d56a99163bbabaf9689f7f1423c7f76f4182dd3447",
    "S078.txt": "4954ddcda4caf38985ebc7ea359a9c49fa78c5d9cbe14dde2bda794d39e50e44",
    "S079.txt": "667229665b5cc50a6c107974226d6dd53e75b41c5ea89d56f37c56181331fa67",
    "S080.txt": "24054b1af50fcfd6e508101042f6c8b722e62e2af7c78e42f313959ec985edf4",
    "S081.txt": "1af8954e57eb1da2226a5302f105eb41b42e2b966e9ba730dbdd27a459176b55",
    "S082.txt": "0746e9da9c241660f71be6529b8f175293b85a4e91e9c061ec976ba973e20dc3",
    "S083.txt": "aceda87b1290696ab91c356086b5f4d50d647ecf882fca55c1efccb7bc3f9840",
    "S084.txt": "35cf4b7ba43d9e84afaf5b56e145de6fe10758a82f794d46ac75ab9be043af58",
    "S085.txt": "c7a10ffa520a9d5d344f18464348815482ed0db8f4fb54ebcc5b8c0410e71813",
}
TIMEOUT = 20


def _env() -> dict[str, str]:
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", root, *args], capture_output=True, env=_env())


def resolve(root: str, revision: str) -> str | None:
    proc = git(root, "rev-parse", "--verify", "--quiet", f"{revision}^{{commit}}")
    return proc.stdout.decode().strip() if proc.returncode == 0 else None


def show(root: str, revision: str, path: str) -> bytes | None:
    proc = git(root, "show", f"{revision}:{path}")
    return proc.stdout if proc.returncode == 0 else None


def ls_tree(root: str, revision: str, prefix: str) -> list[str]:
    proc = git(root, "ls-tree", "-r", "--name-only", revision, "--", prefix)
    return [p for p in proc.stdout.decode().splitlines() if p] if proc.returncode == 0 else []


def load_key(args: argparse.Namespace, path: str, pinned: str) -> tuple[dict | None, str]:
    if args.key_file:
        data = Path(args.key_file).read_bytes()
    else:
        krev = resolve(args.root, args.key_revision)
        data = show(args.root, krev, path) if krev else None
        if data is None:
            return None, "key not found at key revision"
    digest = hashlib.sha256(data).hexdigest()
    if digest != pinned:
        return None, f"key sha256 {digest} != pinned {pinned}"
    return json.loads(data), "ok"


def project(expected: list[dict], observed: list) -> tuple[list, list]:
    keys = ("page", "property", "reason")
    exp = sorted(tuple(str(f.get(k)) for k in keys) for f in expected)
    obs = sorted(tuple(str(f.get(k)) for k in keys) if isinstance(f, dict) else ("<non-object>",)
                 for f in observed)
    return exp, obs


def judge(case: dict, proc: subprocess.CompletedProcess | None) -> bool:
    exp = case["expect"]
    if proc is None or proc.returncode != exp["exit"]:
        return False
    try:
        report = json.loads(proc.stdout)
    except (ValueError, RecursionError):
        return False
    if not isinstance(report, dict) or report.get("verdict") != exp["verdict"]:
        return False
    findings = report.get("findings")
    if not isinstance(findings, list):
        return False
    e, o = project(exp["findings"], findings)
    return e == o


def run_c1(args: argparse.Namespace, rev: str) -> tuple[dict, int]:
    key, why = load_key(args, C1_KEY_PATH, C1_KEY_SHA256)
    if key is None:
        return {"error": why}, 2
    tool = show(args.root, rev, TOOL)
    rows = []
    with tempfile.TemporaryDirectory(prefix="kake-r35-c1-") as scratch:
        tool_path = None
        if tool is not None:
            tool_path = Path(scratch) / f"t{uuid.uuid4().hex}.py"
            tool_path.write_bytes(tool)
        for case in key["cases"]:
            proc = None
            if tool_path is not None:
                work = Path(scratch) / uuid.uuid4().hex
                work.mkdir()
                for rel, body in case["files"].items():
                    target = work / rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    if "latin1" in body:
                        target.write_bytes(body["latin1"].encode("latin-1"))
                    else:
                        target.write_text(body["text"], encoding="utf-8")
                manifest = work / f"m{uuid.uuid4().hex[:8]}.json"
                manifest.write_text(json.dumps(case["manifest"]), encoding="utf-8")
                env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": scratch,
                       "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}
                try:
                    proc = subprocess.run([sys.executable, "-B", str(tool_path), "--manifest", str(manifest)],
                                          cwd=work, capture_output=True, text=True, timeout=TIMEOUT, env=env)
                except subprocess.TimeoutExpired:
                    proc = None
            rows.append({"id": case["id"], "passed": judge(case, proc)})
    passed = sum(r["passed"] for r in rows)
    out = {"claim": "C1", "toolPresent": tool is not None,
           "toolSha256": hashlib.sha256(tool).hexdigest() if tool is not None else None,
           "cases": len(rows), "passed": passed, "target": C1_TARGET, "met": passed >= C1_TARGET,
           "perCase": rows}
    return out, 0 if out["met"] else 1


def split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def registry_rows(text: str) -> dict[str, list[list[str]]]:
    rows: dict[str, list[list[str]]] = {}
    in_registry, fence = False, False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        if re.match(r"^##\s", line):
            in_registry = re.match(r"^##\s+Registry\s*$", line) is not None
            continue
        if in_registry and re.match(r"^\|\s*S\d{3}\s*\|", line):
            cells = split_row(line)
            rows.setdefault(cells[0], []).append(cells)
    return rows


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def shingles(ws: list[str]) -> set[tuple[str, ...]]:
    return {tuple(ws[i:i + SHINGLE]) for i in range(len(ws) - SHINGLE + 1)}


def run_c2(args: argparse.Namespace, rev: str) -> tuple[dict, int]:
    key, why = load_key(args, C2_KEY_PATH, C2_KEY_SHA256)
    if key is None:
        return {"error": why}, 2
    raw = show(args.root, rev, ENTRY)
    text = raw.decode("utf-8", "replace") if raw is not None else ""
    cond: dict[str, bool] = {"entry": raw is not None}
    word_count = len(text.split())
    cond["size"] = raw is not None and word_count <= C2_MAX_WORDS
    src_shingles: set[tuple[str, ...]] = set()
    pinned_ok = True
    for name, digest in PINNED_TEXTS.items():
        data = show(args.root, rev, SOURCE_TEXT_DIR + name)
        pinned_ok = pinned_ok and data is not None and hashlib.sha256(data).hexdigest() == digest
    for path in ls_tree(args.root, rev, SOURCE_TEXT_DIR):
        if path.endswith(".txt"):
            src_shingles |= shingles(words((show(args.root, rev, path) or b"").decode("utf-8", "replace")))
    entry_sh = shingles(words(text))
    copied = (len(entry_sh & src_shingles) / len(entry_sh)) if entry_sh else 1.0
    cond["copied"] = raw is not None and pinned_ok and copied <= C2_MAX_COPIED
    reg = registry_rows((show(args.root, rev, SOURCES_MD) or b"").decode("utf-8", "replace"))
    cited = sorted(set(re.findall(r"\b(S0(?:7[89]|8\d|9\d))\b", text)))
    good = []
    for sid in cited:
        rows = reg.get(sid, [])
        if len(rows) == 1 and len(rows[0]) >= 11:
            c = rows[0]
            if c[7] == "mined" and c[8] == "2026-10-22" and ENTRY in c[10]:
                good.append(sid)
    cond["cites"] = len(good) >= C2_MIN_CITES
    norm = re.sub(r"\s+", " ", text.lower())
    probes = [{"id": p["id"], "passed": any(re.search(r, norm) for r in p["regex"])} for p in key["probes"]]
    probes_passed = sum(p["passed"] for p in probes)
    cond["probes"] = probes_passed >= C2_PROBE_TARGET
    met = all(cond.values())
    out = {"claim": "C2", "entrySha256": hashlib.sha256(raw).hexdigest() if raw is not None else None,
           "words": word_count, "pinnedTextsIntact": pinned_ok, "copiedShare": round(copied, 4), "citedIds": cited, "goodCites": good,
           "probes": len(probes), "probesPassed": probes_passed, "probeTarget": C2_PROBE_TARGET,
           "conditions": cond, "met": met, "perProbe": probes}
    return out, 0 if met else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("claim", choices=("c1", "c2"))
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--key-revision")
    g.add_argument("--key-file")
    args = ap.parse_args()
    rev = resolve(args.root, args.revision)
    if rev is None:
        print(json.dumps({"error": "revision does not resolve"}))
        return 2
    key_path = C1_KEY_PATH if args.claim == "c1" else C2_KEY_PATH
    head = {"revision": rev, "counterSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "keyPath": key_path, "keySource": "file" if args.key_file else f"revision {args.key_revision}"}
    if show(args.root, rev, key_path) is not None:
        print(json.dumps({**head, "error": "key visible at the measured revision"}, sort_keys=True))
        return 2
    out, code = (run_c1 if args.claim == "c1" else run_c2)(args, rev)
    print(json.dumps({**head, **out}, indent=1, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
