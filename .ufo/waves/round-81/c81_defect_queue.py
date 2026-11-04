#!/usr/bin/env python3
"""Round-81 C1 counter — the round-80 routed-defect queue (kake, calibration).

Population (frozen in `.ufo/waves/round-81/contract.md`): the six defects the
non-author round-80 closure filed in `corpus/lessons/round-80-verifier-spotcheck.md`
§6 — R80-1 … R80-6.

Frozen predicate (contract §C1):

    met <=> open == 0

Every item is decided from bytes, never from a token that merely says "closed":
a registry line number is re-derived, a receipt is re-parsed and its arithmetic
recomputed, a control receipt is produced by re-running the round-80 counter over
a rebuilt tree, and a seat record is compared canonically against its own
re-derivation.

Exit: 0 met, 1 not met, 2 unevaluable, 64 usage. Read-only outside --work.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ITEMS = ["R80-1", "R80-2", "R80-3", "R80-4", "R80-5", "R80-6"]
ATTACK_ROLES = ["reviewer", "critic", "mutation-tester", "labrat"]

EXPORT_PATHS = [
    "corpus/SOURCES.md",
    "corpus/lessons/round-80.md",
    "corpus/lessons/round-81.md",
    "corpus/knowledge/response-header-expectations.md",
    "LOG.md", "SCORECARD.md", "SKILL.md", "PROVINCE.md", "SHONEN.md",
    ".ufo/waves/round-80/controls/ctl-c80-constants.txt",
    ".ufo/waves/round-80/c80_defect_queue.py",
    ".ufo/waves/round-80/defect-queue.json",
    ".ufo/waves/round-81/junk_tree_build.py",
    ".ufo/waves/round-81/junk-tree.json",
    ".ufo/waves/round-81/w1-spec.json",
    ".ufo/waves/round-81/w1-results.json",
    ".ufo/waves/round-81/w1-accounting.json",
    ".ufo/waves/round-81/seat-failures.json",
    ".ufo/waves/round-81/capture/manifest.json",
    ".ufo/waves/round-81/controls/after-c2-audit.txt",
    "scripts/wave_seat_record.py",
]

CONST_RE = re.compile(r"^const (\S+) failures=(\d+) undecided=(\d+) total=(\d+)")
SUMMARY_RE = re.compile(r"^ctl constants_failed=(\d+)/(\d+) cases=(\d+)", re.M)
SURFACE_RE = re.compile(r"^\| *S(\d{3,}) *\|")


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def run(argv: list[str], cwd: Path, timeout: int = 240) -> tuple[int, str, str]:
    try:
        p = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        return 127, "", f"{type(exc).__name__}: {exc}"
    return p.returncode, p.stdout, p.stderr


def registry_rows(text: str) -> list[tuple[int, str, list[str]]]:
    """(line number, id, cells) for every registry row, whitespace-tolerant."""
    rows = []
    for lineno, line in enumerate(text.splitlines(), 1):
        m = SURFACE_RE.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append((lineno, f"S{m.group(1)}", cells))
    return rows


def materialise(root: Path, revision: str, work: Path) -> tuple[Path, list[str]]:
    tree = work / "tree"
    tree.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    for rel in EXPORT_PATHS:
        show = subprocess.run(["git", "-C", str(root), "show", f"{revision}:{rel}"],
                              capture_output=True)
        if show.returncode != 0:
            continue
        dst = tree / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(show.stdout)
    listing = subprocess.run(["git", "-C", str(root), "ls-tree", "-r", "--name-only", revision,
                              "--", "corpus/knowledge"], capture_output=True, text=True)
    if listing.returncode != 0:
        errors.append(f"ls-tree corpus/knowledge rc={listing.returncode}")
    return tree, errors


# --- items -------------------------------------------------------------------------

def p_r80_1(tree: Path) -> tuple[bool, str]:
    rows = registry_rows(read(tree / "corpus/SOURCES.md"))
    s453 = [ln for ln, rid, _ in rows if rid == "S453"]
    if not s453:
        return False, "no S453 row at the measured revision"
    line = s453[0]
    lesson = read(tree / "corpus/lessons/round-81.md")
    hits = [ln for ln in lesson.splitlines()
            if "R80-1" in ln and f"corpus/SOURCES.md:{line}" in ln and "S453" in ln]
    if not hits:
        return False, f"no R80-1 correction row names corpus/SOURCES.md:{line} for S453"
    return True, f"R80-1 correction names corpus/SOURCES.md:{line}; S453 is on that line"


def parse_constants(text: str) -> tuple[dict[str, tuple[int, int]], int, int]:
    per: dict[str, tuple[int, int]] = {}
    failed = total = 0
    cases = slots = 0
    for line in text.splitlines():
        m = CONST_RE.match(line)
        if m:
            name, failures, und, tot = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
            per[name] = (failures, tot)
            failed += failures
            total += und
            slots += tot
        s = SUMMARY_RE.match(line)
        if s:
            cases = int(s.group(3))
    return per, failed, slots


def p_r80_2(tree: Path) -> tuple[bool, str]:
    text = read(tree / ".ufo/waves/round-80/controls/ctl-c80-constants.txt")
    if not text.strip():
        return False, "round-80 constants receipt absent at the measured revision"
    per, failed, slots = parse_constants(text)
    m = SUMMARY_RE.search(text)
    if not m or len(per) < 1:
        return False, "round-80 constants receipt carries no parseable constant lines"
    echo = per.get("const_echo.py")
    if not echo:
        return False, "round-80 constants receipt names no const_echo.py line"
    wanted = [f"constants_failed={m.group(1)}/{m.group(2)}", f"{failed}/{slots}",
              f"{echo[0]}/{echo[1]}"]
    lesson = read(tree / "corpus/lessons/round-81.md")
    hits = [ln for ln in lesson.splitlines() if "R80-2" in ln and all(w in ln for w in wanted)]
    if not hits:
        return False, ("no R80-2 correction row carries all of " + ", ".join(wanted))
    return True, ("R80-2 correction re-derives " + ", ".join(wanted)
                  + f" over {len(per)} constants")


def p_r80_3(tree: Path) -> tuple[bool, str]:
    rows = registry_rows(read(tree / "corpus/SOURCES.md"))
    if not rows:
        return False, "registry unreadable at the measured revision"
    counts = {}
    for token in ("rfc9110.txt", "rfc9110.html"):
        ids = [rid for _, rid, cells in rows if len(cells) > 1 and token in cells[1]]
        counts[token] = (len(ids), ids)
    lesson = read(tree / "corpus/lessons/round-81.md")
    wanted = [f"rfc9110.txt rows={counts['rfc9110.txt'][0]}",
              f"rfc9110.html rows={counts['rfc9110.html'][0]}"]
    hits = [ln for ln in lesson.splitlines() if "R80-3" in ln and all(w in ln for w in wanted)]
    if not hits:
        return False, "no R80-3 correction row carries " + " and ".join(wanted)
    return True, ("R80-3 correction re-derives " + " and ".join(wanted)
                  + f" ({', '.join(counts['rfc9110.txt'][1])} / {', '.join(counts['rfc9110.html'][1])})")


def load_json(path: Path):
    try:
        return json.loads(read(path)), ""
    except json.JSONDecodeError as exc:
        return None, f"{path.name}: {exc}"


def p_r80_4(tree: Path) -> tuple[bool, str]:
    spec, err = load_json(tree / ".ufo/waves/round-81/w1-spec.json")
    if spec is None:
        return False, f"round-81 spec unreadable: {err}"
    results, err = load_json(tree / ".ufo/waves/round-81/w1-results.json")
    if results is None:
        return False, f"round-81 results unreadable: {err}"
    items = spec.get("items") or []
    if not isinstance(items, list) or not items:
        return False, "round-81 spec carries no items"
    role_of = {i.get("name"): i.get("role") for i in items if isinstance(i, dict)}
    requested_attack = sum(1 for r in role_of.values() if r in ATTACK_ROLES)
    settled = [r.get("name") for r in (results.get("results") or []) if isinstance(r, dict)]
    settled_attack = sum(1 for name in settled if role_of.get(name) in ATTACK_ROLES)
    total = len(settled)
    if total == 0:
        return False, "round-81 results carry no settled seat"
    share = settled_attack / total
    if share < 0.25:
        return False, f"settled attack share {share:.3f} below 0.25 ({settled_attack}/{total})"
    record, err = load_json(tree / ".ufo/waves/round-81/w1-accounting.json")
    if record is None:
        return False, f"round-81 accounting record unreadable: {err}"
    spec_bytes = read(tree / ".ufo/waves/round-81/w1-spec.json").encode("utf-8")
    checks = [
        (record.get("attack_roles") == ATTACK_ROLES, "attack_roles"),
        (record.get("requested_total") == len(items), "requested_total"),
        (record.get("requested_attack") == requested_attack, "requested_attack"),
        (record.get("settled_total") == total, "settled_total"),
        (record.get("settled_attack") == settled_attack, "settled_attack"),
        (abs(float(record.get("share") or 0) - share) < 1e-9, "share"),
        (record.get("spec_sha256") == hashlib.sha256(spec_bytes).hexdigest(), "spec_sha256"),
    ]
    bad = [name for ok, name in checks if not ok]
    if bad:
        return False, "accounting record disagrees with re-derivation: " + ", ".join(bad)
    return True, (f"settled attack share {share:.3f} ({settled_attack}/{total}); requested "
                  f"{requested_attack}/{len(items)}; accounting record re-derives")


def tree_digest(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    files = sorted(p for p in path.rglob("*") if p.is_file())
    for p in files:
        h.update(str(p.relative_to(path)).encode("utf-8") + b"\0")
        h.update(p.read_bytes() + b"\0")
    return h.hexdigest(), len(files)


def p_r80_5(tree: Path, work: Path) -> tuple[bool, str]:
    work.mkdir(parents=True, exist_ok=True)
    builder = tree / ".ufo/waves/round-81/junk_tree_build.py"
    spec = tree / ".ufo/waves/round-81/junk-tree.json"
    counter = tree / ".ufo/waves/round-80/c80_defect_queue.py"
    for path in (builder, spec, counter):
        if not path.is_file():
            return False, f"{path.relative_to(tree)} absent at the measured revision"
    digests = []
    for run_index in (1, 2):
        out = work / f"junk-{run_index}"
        if out.exists():
            shutil.rmtree(out)
        rc, stdout, stderr = run([sys.executable, "-B", str(builder), "--spec", str(spec),
                                  "--out", str(out)], work)
        if rc != 0:
            return False, f"junk builder rc={rc}: {(stdout + stderr).strip()[-160:]}"
        digests.append(tree_digest(out))
    if digests[0] != digests[1]:
        return False, f"junk builder is not deterministic: {digests[0]} != {digests[1]}"
    junk = work / "junk-1"
    verdict_work = work / "junk-work"
    verdict_work.mkdir(parents=True, exist_ok=True)
    rc, stdout, stderr = run([sys.executable, "-B", str(counter), "--root", str(junk),
                              "--work", str(verdict_work)], work)
    lines = [ln for ln in stdout.splitlines() if ln.startswith("C1v1 ")]
    if rc != 1 or not lines:
        return False, f"round-80 counter over the rebuilt junk tree rc={rc} lines={lines[:1]}"
    line = lines[-1]
    wanted = ("open=5", "closed=1", "met=false")
    missing = [w for w in wanted if w not in line]
    if missing:
        return False, f"rebuilt junk tree reads {line!r}; missing {missing}"
    return True, f"junk tree rebuilt deterministically ({digests[0][1]} files); {line}"


def p_r80_6(tree: Path, work: Path) -> tuple[bool, str]:
    work.mkdir(parents=True, exist_ok=True)
    recorder = tree / "scripts/wave_seat_record.py"
    if not recorder.is_file():
        return False, "scripts/wave_seat_record.py absent at the measured revision"
    committed, err = load_json(tree / ".ufo/waves/round-81/seat-failures.json")
    if committed is None:
        return False, f"seat-failures.json unreadable: {err}"
    out = work / "seat-failures.json"
    rc, stdout, stderr = run([sys.executable, "-B", str(recorder),
                              "--results", str(tree / ".ufo/waves/round-81/w1-results.json"),
                              "--spec", str(tree / ".ufo/waves/round-81/w1-spec.json"),
                              "--out", str(out)], work)
    if rc != 0:
        return False, f"recorder rc={rc}: {(stdout + stderr).strip()[-160:]}"
    derived, err = load_json(out)
    if derived is None:
        return False, f"recorder wrote no record: {err}"
    if derived != committed:
        keys = sorted(set(derived) | set(committed))
        bad = [k for k in keys if derived.get(k) != committed.get(k)]
        return False, "committed seat record differs from re-derivation: " + ", ".join(bad)
    seats = derived.get("seats") or {}
    if not seats:
        return False, "seat record lists no seat"
    for name, entry in seats.items():
        if not isinstance(entry, dict):
            return False, f"{name}: entry is not an object"
        for field in ("role", "status", "exit", "error"):
            if field not in entry:
                return False, f"{name}: missing field {field}"
        if entry["status"] not in {"reported", "empty", "unknown"}:
            return False, f"{name}: status {entry['status']!r} outside the enum"
    limit = derived.get("schema_limit")
    if not isinstance(limit, str) or "status" not in limit.lower():
        return False, "record names no results-schema limit"
    empty = sorted(n for n, e in seats.items() if e.get("status") == "empty")
    return True, (f"{len(seats)} seats recorded ({len(empty)} empty: {', '.join(empty) or 'none'}); "
                  f"record equals re-derivation")


# --- selftest ----------------------------------------------------------------------

def _write(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def _base_tree(base: Path) -> Path:
    t = base / "green"
    _write(t / "corpus/SOURCES.md",
           "# SOURCES\n\n| id | source | kind | tier | scope | anchor | teaches | status | opened "
           "| recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
           "| S010 | RFC 9110 html — https://www.rfc-editor.org/rfc/rfc9110.html | spec | A | x | a "
           "| t | mined | 2026-10-19 | 365d | corpus/knowledge/x.md |\n"
           "| S453 | RFC 9110 txt — https://www.rfc-editor.org/rfc/rfc9110.txt | spec | A | x | a "
           "| t | mined | 2026-11-04 | 365d | corpus/knowledge/x.md |\n")
    _write(t / "corpus/knowledge/x.md", "source: S453, S010\n")
    return t


def selftest(work: Path) -> int:
    base = work / "selftest"
    checks: list[tuple[str, bool, str]] = []

    # R80-1: green names :5 (the S453 row), mutant names :6.
    t = _base_tree(base)
    _write(t / "corpus/lessons/round-81.md",
           "| R80-1 | citation | fix | names corpus/SOURCES.md:6 for S453 |\n")
    ok, detail = p_r80_1(t)
    checks.append(("r80-1-green", ok, detail))
    _write(t / "corpus/lessons/round-81.md",
           "| R80-1 | citation | fix | names corpus/SOURCES.md:7 for S453 |\n")
    ok, detail = p_r80_1(t)
    checks.append(("r80-1-wrong-line-opens", not ok, detail))

    # R80-2: green carries the numbers the receipt yields; mutant drops 47/48.
    t = _base_tree(base / "b2")
    _write(t / ".ufo/waves/round-80/controls/ctl-c80-constants.txt",
           "const const_echo.py failures=11 undecided=0 total=12 failed\n"
           "const const_all.py failures=12 undecided=0 total=12 failed\n"
           "const const_clean.py failures=12 undecided=0 total=12 failed\n"
           "const const_regex.py failures=12 undecided=0 total=12 failed\n"
           "ctl constants_failed=4/4 cases=12\n")
    _write(t / "corpus/lessons/round-81.md",
           "| R80-2 | numbers | fix | constants_failed=4/4, 47/48, 11/12 |\n")
    ok, detail = p_r80_2(t)
    checks.append(("r80-2-green", ok, detail))
    _write(t / "corpus/lessons/round-81.md",
           "| R80-2 | numbers | fix | constants_failed=4/4, 48/48, 12/12 |\n")
    ok, detail = p_r80_2(t)
    checks.append(("r80-2-wrong-arithmetic-opens", not ok, detail))

    # R80-3: green counts rows; mutant claims another count.
    t = _base_tree(base / "b3")
    _write(t / "corpus/lessons/round-81.md",
           "| R80-3 | scope | fix | rfc9110.txt rows=1; rfc9110.html rows=1 |\n")
    ok, detail = p_r80_3(t)
    checks.append(("r80-3-green", ok, detail))
    _write(t / "corpus/lessons/round-81.md",
           "| R80-3 | scope | fix | rfc9110.txt rows=3; rfc9110.html rows=1 |\n")
    ok, detail = p_r80_3(t)
    checks.append(("r80-3-wrong-count-opens", not ok, detail))

    # R80-4: green 1 attack of 3 (0.333); mutant 1 of 5 (0.2) with a matching
    # record so only the floor decides; third mutant drifts the record.
    def spec_results(tree: Path, roles: list[str], settled: int, record_share: float | None):
        spec = {"items": [{"name": f"S{i}", "role": r, "item": "x"} for i, r in enumerate(roles)]}
        _write(tree / ".ufo/waves/round-81/w1-spec.json", json.dumps(spec))
        results = {"results": [{"name": f"S{i}", "output": "x"} for i in range(settled)]}
        _write(tree / ".ufo/waves/round-81/w1-results.json", json.dumps(results))

    t = _base_tree(base / "b4")
    spec_results(t, ["reviewer", "executor", "scribe"], 3, None)
    attack = sum(1 for r in ["reviewer", "executor", "scribe"] if r in ATTACK_ROLES)
    share = attack / 3
    _write(t / ".ufo/waves/round-81/w1-accounting.json", json.dumps({
        "attack_roles": ATTACK_ROLES, "requested_total": 3, "requested_attack": attack,
        "settled_total": 3, "settled_attack": attack, "share": share,
        "spec_sha256": hashlib.sha256((t / ".ufo/waves/round-81/w1-spec.json").read_bytes()).hexdigest()}))
    ok, detail = p_r80_4(t)
    checks.append(("r80-4-green", ok, detail))
    spec_results(t, ["reviewer", "executor", "executor", "executor", "executor"], 5, None)
    share = 1 / 5
    _write(t / ".ufo/waves/round-81/w1-accounting.json", json.dumps({
        "attack_roles": ATTACK_ROLES, "requested_total": 5, "requested_attack": 1,
        "settled_total": 5, "settled_attack": 1, "share": share,
        "spec_sha256": hashlib.sha256((t / ".ufo/waves/round-81/w1-spec.json").read_bytes()).hexdigest()}))
    ok, detail = p_r80_4(t)
    checks.append(("r80-4-floor-opens", not ok, detail))
    spec_results(t, ["reviewer", "executor", "scribe"], 3, None)
    _write(t / ".ufo/waves/round-81/w1-accounting.json", json.dumps({
        "attack_roles": ["reviewer", "sentinel"], "requested_total": 3, "requested_attack": 1,
        "settled_total": 3, "settled_attack": 1, "share": 1 / 3, "spec_sha256": "0" * 64}))
    ok, detail = p_r80_4(t)
    checks.append(("r80-4-drifted-record-opens", not ok, detail))

    # R80-5: green reproduces open=5 closed=1; mutant tree that also closes R79-1.
    t = _base_tree(base / "b5")
    junk_lesson = ("R79-5 withdrawal: passed 31/31 before the tool existed\n")
    _write(t / ".ufo/waves/round-81/junk-tree.json", json.dumps({
        "files": {"corpus/lessons/round-80.md": junk_lesson}}))
    _write(t / ".ufo/waves/round-81/junk_tree_build.py", JUNK_BUILDER)
    (t / ".ufo/waves/round-80").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__).resolve().parent / ".." / "round-80" / "c80_defect_queue.py",
                    t / ".ufo/waves/round-80/c80_defect_queue.py")
    ok, detail = p_r80_5(t, base / "w5-green")
    checks.append(("r80-5-green", ok, detail))
    _write(t / ".ufo/waves/round-81/junk-tree.json", json.dumps({
        "files": {"corpus/lessons/round-80.md": junk_lesson + "R79-1 erratum: S453 was never the RFC 9309 row.\n",
                  "corpus/SOURCES.md": (t / "corpus/SOURCES.md").read_text(encoding="utf-8"),
                  "corpus/knowledge/x.md": "cites S453\n"}}))
    ok, detail = p_r80_5(t, base / "w5-mutant")
    checks.append(("r80-5-overbuilt-junk-opens", not ok, detail))

    # R80-6: green equality; mutant tampers the committed record.
    t = _base_tree(base / "b6")
    _write(t / "scripts/wave_seat_record.py", RECORDER)
    _write(t / ".ufo/waves/round-81/w1-spec.json", json.dumps(
        {"items": [{"name": "SeatA", "role": "reviewer", "item": "x"}]}))
    _write(t / ".ufo/waves/round-81/w1-results.json", json.dumps(
        {"results": [{"name": "SeatA", "output": ""}, {"name": "SeatB", "output": "ok"}]}))
    rc, _, _ = run([sys.executable, "-B", str(t / "scripts/wave_seat_record.py"),
                    "--results", str(t / ".ufo/waves/round-81/w1-results.json"),
                    "--spec", str(t / ".ufo/waves/round-81/w1-spec.json"),
                    "--out", str(t / ".ufo/waves/round-81/seat-failures.json")], base)
    ok, detail = p_r80_6(t, base / "w6-green")
    checks.append((f"r80-6-green (recorder rc={rc})", ok, detail))
    doc = json.loads((t / ".ufo/waves/round-81/seat-failures.json").read_text(encoding="utf-8"))
    doc["seats"]["SeatB"]["status"] = "reported" if doc["seats"]["SeatB"]["status"] != "reported" else "empty"
    _write(t / ".ufo/waves/round-81/seat-failures.json", json.dumps(doc))
    ok, detail = p_r80_6(t, base / "w6-mutant")
    checks.append(("r80-6-tampered-record-opens", not ok, detail))

    for name, ok, detail in checks:
        print(f"  {'ok' if ok else 'FAIL'} {name} :: {detail}")
    passed = sum(1 for _, ok, _ in checks if ok)
    print(f"selftest: {passed}/{len(checks)} passed")
    return 0 if passed == len(checks) else 1


# --- main --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--work")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    work = Path(a.work) if a.work else Path(tempfile.mkdtemp(prefix="kake-c81-dq-"))
    work.mkdir(parents=True, exist_ok=True)
    try:
        if a.selftest:
            return selftest(work)
        errors: list[str] = []
        if a.revision:
            tree, errors = materialise(root, a.revision, work)
            label = a.revision
        else:
            tree, label = root, "worktree"
        if errors:
            print(f"unevaluable: {errors}")
            return 2
        verdicts = {
            "R80-1": p_r80_1(tree),
            "R80-2": p_r80_2(tree),
            "R80-3": p_r80_3(tree),
            "R80-4": p_r80_4(tree),
            "R80-5": p_r80_5(tree, work),
            "R80-6": p_r80_6(tree, work),
        }
        open_items = [k for k in ITEMS if not verdicts[k][0]]
        closed = [k for k in ITEMS if verdicts[k][0]]
        for item in ITEMS:
            ok, detail = verdicts[item]
            print(f"{item} {'closed' if ok else 'open'} {detail}")
        met = not open_items
        print(f"C1v1 revision={label} items={len(ITEMS)} open={len(open_items)} "
              f"closed={len(closed)} met={'true' if met else 'false'}")
        print(f"exit={0 if met else 1}")
        return 0 if met else 1
    finally:
        if a.work is None:
            shutil.rmtree(work, ignore_errors=True)


JUNK_BUILDER = '''#!/usr/bin/env python3
"""Materialise a junk control tree from a JSON file map (round-81 R80-5 builder)."""
import argparse, json, sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    try:
        spec = json.loads(Path(a.spec).read_text(encoding="utf-8"))
        files = spec["files"]
    except (OSError, ValueError, KeyError) as exc:
        print(f"bad spec: {exc}", file=sys.stderr)
        return 2
    out = Path(a.out)
    for rel, body in files.items():
        if rel.startswith("/") or ".." in Path(rel).parts:
            print(f"unsafe path: {rel}", file=sys.stderr)
            return 2
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(body, encoding="utf-8")
    print(f"wrote {len(files)} files to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

RECORDER = '''#!/usr/bin/env python3
"""Record per-seat outcome from a wave results file (round-81 R80-6).

The orchestrator's `<wave>-results.json` carries per seat only `name`, `agent`
and `output`. It records no status, exit or error text, so a dead seat's cause
cannot be cited from it. This recorder writes the lane-owned record that makes
the outcome decidable: it joins the spec's roles, classifies each settling seat
(`reported` / `empty` / `unknown`), re-derives output bytes and digest, and
names the schema limit instead of inventing an error message.
"""
import argparse, hashlib, json, sys
from pathlib import Path

SCHEMA_LIMIT = ("w1-results.json records only name, agent and output; it carries no status, "
                "exit code or error text, so a seat's failure cause is not recoverable from "
                "committed bytes and every exit/error here is declared unknown")


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--results", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    try:
        results = load(a.results)
        spec = load(a.spec)
    except (OSError, ValueError) as exc:
        print(f"unreadable input: {exc}", file=sys.stderr)
        return 2
    roles = {i.get("name"): i.get("role") for i in (spec.get("items") or []) if isinstance(i, dict)}
    seats = {}
    for row in (results.get("results") or []):
        if not isinstance(row, dict) or not isinstance(row.get("name"), str):
            continue
        name = row["name"]
        output = row.get("output") or ""
        raw = output.encode("utf-8")
        status = "reported" if raw.strip() else "empty"
        seats[name] = {
            "role": roles.get(name, "unknown"),
            "status": status,
            "exit": "unknown",
            "error": "not recorded in w1-results.json",
            "output_bytes": len(raw),
            "output_sha256": hashlib.sha256(raw).hexdigest(),
        }
    unattributed = sorted(n for n in roles if n not in seats)
    record = {
        "wave": results.get("wave") or spec.get("wave"),
        "round": results.get("round"),
        "seats": seats,
        "empty_output": sorted(n for n, e in seats.items() if e["status"] == "empty"),
        "not_settled": unattributed,
        "schema_limit": SCHEMA_LIMIT,
    }
    Path(a.out).write_text(json.dumps(record, indent=1, sort_keys=True) + "\\n", encoding="utf-8")
    print(f"seats={len(seats)} empty={len(record['empty_output'])} not_settled={len(unattributed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


if __name__ == "__main__":
    raise SystemExit(main())
