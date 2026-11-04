#!/usr/bin/env python3
"""MutC round-83 mutation harness.

Scores mutated *copies* of the two frozen counters against
  (a) the counter's own --selftest, and
  (b) an external fixture built for the property the mutation breaks.

Pristine and mutant runs are handed byte-identical fixture trees (sha256 of the
whole tree is recorded on both sides), so any difference in exit code or output
line is attributable to the mutation, not to the harness.  The committed
counters are never written: only copies under the scratch root are mutated.

Every patch asserts a single textual match before it is applied, and the
mutated source is compiled before it is run, so a mutant that fails for a
harness reason (bad path, syntax error, missing file) is reported as
`harness-error`, never as `killed`.

Usage: mutc.py [c1|c2|all] [--case NAME]
"""
from __future__ import annotations

import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRATCH = Path("/fast/scratch/hyaku/kake-r83/MutC")
LANE = Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
COUNTER_C1 = LANE / ".ufo/waves/round-83/c83_defect_queue.py"
COUNTER_C2 = LANE / ".ufo/waves/round-83/c83_drift_class.py"
TOOL = LANE / "scripts/header_change_class.py"
PY = sys.executable

ATTACK_ROLES = {"reviewer", "critic", "mutation-tester", "labrat"}
KILLER_NAMES = ("C1-m3", "C1-m5", "C2-m2", "C2-m4", "C2-m5")

# C1 paths (mirror the counter, relative to the fixture root)
LESSON = "corpus/lessons/round-83.md"
QUALITY = "corpus/QUALITY.md"
SPEC = ".ufo/waves/round-83/w1-spec.json"
RESULTS = ".ufo/waves/round-83/w1-results.json"
ACCOUNTING = ".ufo/waves/round-83/w1-accounting.json"
INSTRUMENT = ".ufo/waves/round-83/controls/after-c83-instrument-check.txt"
KILLER = ".ufo/waves/round-83/killers/run_killers.py"
FLEET_REPORT = ".ufo/reports/round-81/kake.md"

# C2 paths
BASE_CAPTURE = ".ufo/waves/round-81/capture"
ROUND_CAPTURE = ".ufo/waves/round-82/capture"
CONTROL_A = ".ufo/waves/round-83/capture-control/a"
CONTROL_B = ".ufo/waves/round-83/capture-control/b"
DECLARATION = ".ufo/waves/round-81/capture-expectations.json"
RECORD = ".ufo/waves/round-83/controls/after-c2-classes.txt"
TOOL_REL = "scripts/header_change_class.py"

C2_SURFACES = ("s1", "s2", "s3")
C2_STABLE = {"ETag": '"v1"', "Content-Length": "5", "Content-Type": "text/plain",
             "Cache-Control": "max-age=600", "Vary": "Accept-Encoding"}
C2_A = dict(C2_STABLE, Date="Tue, 04 Nov 2026 10:00:00 GMT", **{"X-Cache": "HIT"})
C2_B = dict(C2_STABLE, Date="Tue, 04 Nov 2026 11:00:00 GMT", **{"X-Cache": "MISS"})

C1_FLEET_LINES = [
    "the lane tip at filing abc is superseded by the amendment commit",
    "the wave bullet said one seat died and was not replaced at all",
    "the claim row measured at the earlier carrier only, not the tip",
    "controls were named without a receipt path anywhere in the section",
    "the population figure was quoted from the draft, not the counter",
]


class HarnessError(RuntimeError):
    pass


# --------------------------------------------------------------------- utils

def env() -> dict:
    merged = dict(os.environ)
    merged["TMPDIR"] = str(SCRATCH / "tmp")
    merged["PYTHONDONTWRITEBYTECODE"] = "1"
    merged.pop("PYTHONPATH", None)
    return merged


def run_cmd(argv: list[str]) -> tuple[int, str, str]:
    proc = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=env(), check=False)
    return (proc.returncode,
            proc.stdout.decode("utf-8", "replace"),
            proc.stderr.decode("utf-8", "replace"))


def sha_tree(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def fresh(path: Path) -> Path:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)
    return path


def apply_patch(text: str, old: str, new: str) -> str:
    hits = text.count(old)
    if hits != 1:
        raise HarnessError(f"patch matched {hits} times, expected 1: {old[:80]!r}")
    return text.replace(old, new)


def compile_check(path: Path) -> None:
    source = path.read_text(encoding="utf-8")
    try:
        compile(source, str(path), "exec")
    except SyntaxError as exc:  # harness defect, not a kill
        raise HarnessError(f"mutant does not compile: {exc}") from exc


def summary_line(stdout: str) -> str:
    """The counter's own verdict line, not a trailing diagnostic line."""
    for line in stdout.splitlines():
        if line.startswith(("C1v1 ", "C2v1 ")):
            return line
    lines = [line for line in stdout.splitlines() if line.strip()]
    return lines[-1] if lines else ""


# ----------------------------------------------------------------- C1 fixtures

def build_c1_fleet(fleet: Path) -> str:
    fresh(fleet)
    run = run_cmd(["git", "-C", str(fleet), "init", "-q"])
    if run[0] != 0:
        raise HarnessError(f"git init failed: {run[2]}")
    top = run_cmd(["git", "-C", str(fleet), "rev-parse", "--show-toplevel"])[1].strip()
    if Path(top).resolve() != fleet.resolve():
        raise HarnessError(f"fixture toplevel {top!r} != {fleet}")
    ident = ["-c", "user.name=mutc", "-c", "user.email=mutc@example.test"]
    report = fleet / FLEET_REPORT
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text("\n".join(C1_FLEET_LINES) + "\n", encoding="utf-8")
    for args in (["add", FLEET_REPORT], [*ident, "commit", "-q", "-m", "filed"]):
        rc, _out, err = run_cmd(["git", "-C", str(fleet), *args])
        if rc != 0:
            raise HarnessError(f"git {args[0]} failed: {err}")
    report.write_text(C1_FLEET_LINES[0] + "\nrevised\n", encoding="utf-8")
    for args in (["add", FLEET_REPORT], [*ident, "commit", "-q", "-m", "amended"]):
        rc, _out, err = run_cmd(["git", "-C", str(fleet), *args])
        if rc != 0:
            raise HarnessError(f"git {args[0]} failed: {err}")
    return run_cmd(["git", "-C", str(fleet), "rev-parse", "HEAD"])[1].strip()


def c1_seats(kind: str) -> list[dict]:
    if kind == "nine":
        names = [("Alfa", "executor"), ("Bravo", "reviewer"), ("Charlie", "scribe"),
                 ("Delta", "critic"), ("Echo", "executor"), ("Foxtrot", "scribe"),
                 ("Golf", "executor"), ("Hotel", "scribe"), ("India", "executor")]
    elif kind == "one-attack":
        names = [("Alfa", "reviewer"), ("Bravo", "executor"),
                 ("Charlie", "scribe"), ("Delta", "executor")]
    else:
        names = [("Alfa", "executor"), ("Bravo", "reviewer"),
                 ("Charlie", "scribe"), ("Delta", "critic")]
    return [{"name": name, "role": role, "output": "a" * 300} for name, role in names]


def build_c1(root: Path, amendment: str, *, seats: list[dict] | None = None,
             quotes: int = 4, basis: str = "utf-8", population: int = 30,
             bound: int | None = None, killer_rows: bool = True) -> None:
    fresh(root)
    seats = seats or c1_seats("four")
    settlement = [row for row in seats if row["output"]]
    attack = [row for row in settlement if row["role"] in ATTACK_ROLES]
    share = round(len(attack) / len(settlement), 4) if settlement else 0.0

    (root / SPEC).parent.mkdir(parents=True, exist_ok=True)
    (root / SPEC).write_text(json.dumps({"items": [
        {"name": row["name"], "role": row["role"]} for row in seats
    ]}), encoding="utf-8")
    (root / RESULTS).write_text(json.dumps({"results": [
        {"name": row["name"], "output": row["output"]} for row in seats
    ]}), encoding="utf-8")
    (root / ACCOUNTING).write_text(json.dumps({
        "bytes_basis": basis,
        "settled": len(settlement),
        "settled_names": sorted(row["name"] for row in settlement),
        "settled_attack": len(attack),
        "settled_share": share,
        "seats": [{"name": row["name"], "role": row["role"],
                   "output_bytes": len(row["output"].encode("utf-8"))} for row in seats],
    }), encoding="utf-8")

    (root / INSTRUMENT).parent.mkdir(parents=True, exist_ok=True)
    (root / INSTRUMENT).write_text(
        "C2v1 revision=" + "a" * 40 + f" population={population} "
        f"bound={population if bound is None else bound} mismatches=0 met=true\n",
        encoding="utf-8")

    (root / KILLER).parent.mkdir(parents=True, exist_ok=True)
    if killer_rows:
        body = "".join(f'print("{name} killed fixture=mutc")\n' for name in KILLER_NAMES)
        body += 'print("distinguished=5/5")\n'
    else:
        body = 'print("distinguished=5/5")\n'
    (root / KILLER).write_text("import sys\n" + body + "raise SystemExit(0)\n",
                               encoding="utf-8")

    (root / QUALITY).parent.mkdir(parents=True, exist_ok=True)
    (root / QUALITY).write_text(
        "# QUALITY (fixture)\n\n"
        "- A Gate summary must cite the lesson it summarises "
        "(`corpus/lessons/round-82.md` §Gate); added `round-83`.\n", encoding="utf-8")

    # only C1_FLEET_LINES[1:] are removed by the amendment commit; quoting the
    # retained first line would score a quote that is not an erratum.
    quote_lines = "\n".join("> " + line for line in C1_FLEET_LINES[1:1 + quotes])
    (root / LESSON).parent.mkdir(parents=True, exist_ok=True)
    (root / LESSON).write_text(
        "# Round 83 (fixture)\n\n"
        f"**D1 — attack floor.** settled_attack={len(attack)} of {len(settlement)}, "
        "superseding 0/7.\n"
        "**D2 — units.** UTF-8 bytes from w1-accounting.json.\n"
        "**D3 — instrument receipt.** controls/after-c83-instrument-check.txt, `--check`.\n"
        f"**D4 — erratum.** commit `{amendment[:8]}` — the superseded statements quoted:\n\n"
        + quote_lines + "\n\n"
        "**D5 — killers.** distinguished=5/5 over C1-m3 C1-m5 C2-m2 C2-m4 C2-m5.\n"
        "**D6 — provenance.** §Gate rule lands in corpus/QUALITY.md.\n", encoding="utf-8")


def build_c1_junk(root: Path) -> None:
    """The contract's junk control: prose says closed, no state carrier."""
    fresh(root)
    (root / LESSON).parent.mkdir(parents=True, exist_ok=True)
    (root / LESSON).write_text(
        "# lessons\n\n"
        + "\n".join(f"**{item} — closed.** The work is done." for item in
                    ("D1", "D2", "D3", "D4", "D5", "D6")) + "\n", encoding="utf-8")
    (root / QUALITY).parent.mkdir(parents=True, exist_ok=True)
    (root / QUALITY).write_text("# QUALITY\n", encoding="utf-8")


C1_VARIANTS = {
    "green": lambda root, amendment: build_c1(root, amendment),
    "share-0.2222": lambda root, amendment: build_c1(
        root, amendment, seats=c1_seats("nine")),
    "bytes-basis-chars": lambda root, amendment: build_c1(
        root, amendment, basis="chars"),
    "erratum-two-quotes": lambda root, amendment: build_c1(
        root, amendment, quotes=2),
    "d3-bound-differs": lambda root, amendment: build_c1(
        root, amendment, bound=29),
    "attack-floor-one": lambda root, amendment: build_c1(
        root, amendment, seats=c1_seats("one-attack")),
    "killer-rows-missing": lambda root, amendment: build_c1(
        root, amendment, killer_rows=False),
    "multibyte-bytes": lambda root, amendment: build_c1(
        root, amendment,
        seats=[{"name": "Alfa", "role": "executor", "output": "é" * 150},
               {"name": "Bravo", "role": "reviewer", "output": "é" * 150},
               {"name": "Charlie", "role": "scribe", "output": "é" * 150},
               {"name": "Delta", "role": "critic", "output": "é" * 150}]),
    "junk-prose-only": lambda root, amendment: build_c1_junk(root),
}

C1_MUTANTS = [
    ("C1-m1-drop-share-conjunct", "share-0.2222",
     'derived["settled_attack"] >= 2 and derived["settled_share"] >= 0.25',
     'derived["settled_attack"] >= 2'),
    ("C1-m2-ignore-bytes-basis", "bytes-basis-chars",
     '    if record.get("bytes_basis") != "utf-8":\n'
     "        return False, f\"bytes_basis={record.get('bytes_basis')!r}\"\n",
     ""),
    ("C1-m3-erratum-threshold-one", "erratum-two-quotes",
     "return len(quoted) >= 4 and log is not None, (",
     "return len(quoted) >= 1 and log is not None, ("),
    ("C1-m4-drop-bound-equals-population", "d3-bound-differs",
     '    ok = (fields.get("bound") == fields.get("population")\n'
     '          and fields.get("mismatches") == "0" and fields.get("met") == "true")',
     '    ok = (fields.get("mismatches") == "0" and fields.get("met") == "true")'),
    ("C1-m5-drop-attack-floor", "attack-floor-one",
     'derived["settled_attack"] >= 2 and derived["settled_share"] >= 0.25',
     'derived["settled_share"] >= 0.25'),
    ("C1-m6-drop-killer-row-check", "killer-rows-missing",
     '    ok = proc.returncode == 0 and "distinguished=5/5" in out and rows_ok',
     '    ok = proc.returncode == 0 and "distinguished=5/5" in out'),
    ("C1-m7-count-chars-not-utf8-bytes", "multibyte-bytes",
     '        size = len(output.encode("utf-8")) if isinstance(output, str) else 0',
     '        size = len(output) if isinstance(output, str) else 0'),
    ("C1-m8-met-always-true", "junk-prose-only",
     "    met = open_items == 0",
     "    met = True"),
    # harness control: a comment-only edit must read `survived` on both axes.
    ("C1-m0-comment-only-control", "green",
     "#!/usr/bin/env python3",
     "#!/usr/bin/env python3\n# mutc harness control: comment only, no behaviour change"),
]


# ----------------------------------------------------------------- C2 fixtures

def write_receipt(directory: Path, body: bytes, headers: dict[str, str],
                  status: int = 200, truncated: bool = False) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "body.bin").write_bytes(body)
    receipt = {
        "bodyFile": "body.bin",
        "bytes": len(body),
        "fetchedAt": "2026-11-04T00:00:00Z",
        "finalUrl": "https://example.test/",
        "headers": [{"name": name, "value": value} for name, value in headers.items()],
        "method": "GET",
        "sha256": hashlib.sha256(body).hexdigest(),
        "status": status,
        "truncated": truncated,
        "url": "https://example.test/",
    }
    (directory / "response.json").write_text(json.dumps(receipt, indent=1), encoding="utf-8")


def c2_record(root: Path) -> bytes:
    rc, out, _err = run_cmd([PY, "-B", str(root / TOOL_REL),
                             "--a", str(root / BASE_CAPTURE),
                             "--b", str(root / ROUND_CAPTURE),
                             "--declared", str(root / DECLARATION)])
    return out.encode("utf-8") if rc == 0 else b""


def build_c2(root: Path, *, captures_identical: bool = False,
             etag_only: bool = False, control_flip: bool = True,
             content_length: bool = False, truncated: bool = False,
             record_override: bytes | None = None,
             tool_append: str = "") -> None:
    fresh(root)
    (root / TOOL_REL).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(TOOL, root / TOOL_REL)
    (root / DECLARATION).parent.mkdir(parents=True, exist_ok=True)
    (root / DECLARATION).write_text(json.dumps(
        {"surfaces": [{"id": s, "url": "https://example.test/"} for s in C2_SURFACES]}),
        encoding="utf-8")

    for surface in C2_SURFACES:
        write_receipt(root / BASE_CAPTURE / surface, b"hello", C2_A)
        b_headers = dict(C2_B)
        b_truncated = False
        if captures_identical:
            b_headers = dict(C2_A)
        if etag_only and surface == "s1":
            b_headers = dict(b_headers, ETag='"v2"')
        if content_length and surface == "s1":
            b_headers = dict(b_headers, **{"Content-Length": "6"})
        if truncated and surface == "s1":
            b_truncated = True
        write_receipt(root / ROUND_CAPTURE / surface, b"hello", b_headers,
                      truncated=b_truncated)

        write_receipt(root / CONTROL_A / surface, b"hello", C2_A)
        if control_flip:
            write_receipt(root / CONTROL_B / surface, b"hellx",
                          dict(C2_B, ETag='"v2"'))
        else:
            write_receipt(root / CONTROL_B / surface, b"hello", C2_A)

    record = c2_record(root) if record_override is None else record_override
    (root / RECORD).parent.mkdir(parents=True, exist_ok=True)
    (root / RECORD).write_bytes(record)
    if tool_append:
        with (root / TOOL_REL).open("a", encoding="utf-8") as handle:
            handle.write(tool_append)


C2_VARIANTS = {
    "green": lambda root: build_c2(root),
    "tool-imports-socket": lambda root: build_c2(
        root, tool_append="\nimport socket\n"),
    "control-pair-identical": lambda root: build_c2(root, control_flip=False),
    "etag-only-change": lambda root: build_c2(root, etag_only=True),
    "captures-identical": lambda root: build_c2(root, captures_identical=True),
    "record-wrong": lambda root: build_c2(
        root, record_override=b"summary surfaces=3 diffs=9 verdict=same-object\n"),
    "content-length-change": lambda root: build_c2(root, content_length=True),
    "receipt-truncated": lambda root: build_c2(root, truncated=True),
}

C2_MUTANTS = [
    ("C2-m1-tool-offline-always-true", "tool-imports-socket",
     "    return NETWORK.search(source) is None",
     "    return True"),
    ("C2-m2-control-ok-hardcoded", "control-pair-identical",
     '    flags["control_ok"] = control_ok',
     '    flags["control_ok"] = 1'),
    ("C2-m3-validator-as-per-request", "etag-only-change",
     '    if lowered in VALIDATOR:\n        return "validator"',
     '    if lowered in VALIDATOR:\n        return "per-request"'),
    ("C2-m4-drop-diffs-positive", "captures-identical",
     '                    and isinstance(flags["diffs"], int) and flags["diffs"] > 0',
     '                    and isinstance(flags["diffs"], int)'),
    ("C2-m5-record-equal-weakened", "record-wrong",
     '    flags["record_equal"] = int(record is not None and rc1 == 0\n'
     '                                and record.rstrip(b"\\n") == out1.rstrip(b"\\n"))',
     '    flags["record_equal"] = int(rc1 == 0)'),
    ("C2-m6-content-length-as-per-request", "content-length-change",
     "    if lowered in PER_REQUEST:\n        return \"per-request\"",
     "    if lowered in PER_REQUEST or lowered == \"content-length\":\n"
     "        return \"per-request\""),
    ("C2-m7-accept-truncated-receipt", "receipt-truncated",
     '    if receipt.get("truncated") is not False:\n'
     '        return None, "truncated or silent"\n',
     ""),
    ("C2-m8-met-always-true", "captures-identical",
     '    flags["met"] = (flags["declared"] == 3 and flags["surfaces_a"] == 3',
     '    flags["met"] = True or (flags["declared"] == 3 and flags["surfaces_a"] == 3'),
    # harness control: a comment-only edit must read `survived` on both axes.
    ("C2-m0-comment-only-control", "green",
     "#!/usr/bin/env python3",
     "#!/usr/bin/env python3\n# mutc harness control: comment only, no behaviour change"),
]


# --------------------------------------------------------------------- scorer

def prepare_cases() -> dict[str, Path]:
    """Build every fixture once; pristine and mutant share exact bytes."""
    roots: dict[str, Path] = {}

    fixtures = fresh(SCRATCH / "fixtures")
    fleet = fixtures / "fleet"
    amendment = build_c1_fleet(fleet)
    for name, builder in C1_VARIANTS.items():
        tree = fixtures / "c1" / name
        builder(tree, amendment)
        roots["c1:" + name] = tree
    roots["c1:fleet"] = fleet

    for name, builder in C2_VARIANTS.items():
        tree = fixtures / "c2" / name
        builder(tree)
        roots["c2:" + name] = tree
    return roots


def case_dir(name: str) -> Path:
    return fresh(SCRATCH / "cases" / name)


def build_case(counter: Path, case: Path, depth: bool) -> Path:
    """Lay a counter copy out so __file__-relative lookups still resolve."""
    if depth:
        target = case / "lane/.ufo/waves/round-83" / counter.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(counter, target)
        (case / "lane/scripts").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(TOOL, case / "lane" / TOOL_REL)
    else:
        target = case / "counter.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(counter, target)
    return target


def selftest_axis(counter_path: Path, case: Path, depth: bool) -> dict:
    work = case / "selftest-work"
    if work.exists():
        shutil.rmtree(work)
    argv = [PY, "-B", str(counter_path), "--selftest"]
    if depth:
        argv += ["--work", str(work)]
    rc, out, err = run_cmd(argv)
    return {"rc": rc, "tail": summary_line(out), "stdout": out,
            "stderr": err, "green": rc == 0}


def fixture_axis(counter_path: Path, case: Path, tree: Path, fleet: Path | None,
                 label: str) -> dict:
    run_tree = case / f"run-{label}"
    if run_tree.exists():
        shutil.rmtree(run_tree)
    shutil.copytree(tree, run_tree)
    digest = sha_tree(run_tree)

    run_fleet = None
    if fleet is not None:
        run_fleet = case / f"run-{label}-fleet"
        if run_fleet.exists():
            shutil.rmtree(run_fleet)
        shutil.copytree(fleet, run_fleet)

    argv = [PY, "-B", str(counter_path), "--root", str(run_tree)]
    if run_fleet is not None:
        argv += ["--fleet", str(run_fleet)]
    if counter_path.name == "c83_drift_class.py":
        work = case / f"work-{label}"
        if work.exists():
            shutil.rmtree(work)
        argv += ["--work", str(work)]
    rc, out, err = run_cmd(argv)
    return {"rc": rc, "tail": summary_line(out), "stdout": out, "stderr": err,
            "tree_sha256": digest}


def score_counter(kind: str, mutants: list[tuple], roots: dict[str, Path]) -> dict:
    counter = COUNTER_C1 if kind == "c1" else COUNTER_C2
    depth = kind == "c2"
    pristine_case = case_dir(f"{kind}-pristine")
    pristine_path = build_case(counter, pristine_case, depth)
    record: dict = {"counter": str(counter), "sha256": hashlib.sha256(
        counter.read_bytes()).hexdigest(), "pristine": {}, "mutants": []}

    st = selftest_axis(pristine_path, pristine_case, depth)
    record["pristine"]["selftest"] = {k: st[k] for k in ("rc", "tail", "green", "stderr")}

    # pristine results on every variant the counter's mutants will use, plus
    # the green control: a counter that cannot read green is not scorable.
    variants = sorted({"green"} | {variant for _n, variant, _o, _new in mutants})
    pristine_fixtures: dict[str, dict] = {}
    for variant in variants:
        tree = roots[f"{kind}:{variant}"]
        fleet = roots.get(f"{kind}:fleet")
        pristine_fixtures[variant] = fixture_axis(
            pristine_path, pristine_case, tree, fleet, f"pristine-{variant}")
    record["pristine"]["fixtures"] = pristine_fixtures

    for name, variant, old, new in mutants:
        case = case_dir(f"{kind}-{name}")
        target = build_case(counter, case, depth)
        entry: dict = {"name": name, "variant": variant, "patch_old": old,
                       "patch_new": new}
        try:
            source = target.read_text(encoding="utf-8")
            patched = apply_patch(source, old, new)
            target.write_text(patched, encoding="utf-8")
            compile_check(target)
            if patched == source:
                raise HarnessError("patch was a no-op")
        except HarnessError as exc:
            entry.update(verdict="harness-error", error=str(exc))
            record["mutants"].append(entry)
            continue

        entry["mutated_sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
        entry["diff"] = "".join(difflib.unified_diff(
            source.splitlines(keepends=True), patched.splitlines(keepends=True),
            fromfile=counter.name, tofile=name))
        st = selftest_axis(target, case, depth)
        tree = roots[f"{kind}:{variant}"]
        fleet = roots.get(f"{kind}:fleet")
        fx = fixture_axis(target, case, tree, fleet, f"mutant-{variant}")

        pristine_fx = pristine_fixtures[variant]
        same_tree = fx["tree_sha256"] == pristine_fx["tree_sha256"]
        selftest_killed = (st["rc"], st["tail"]) != (
            record["pristine"]["selftest"]["rc"], record["pristine"]["selftest"]["tail"])
        fixture_killed = (fx["rc"], fx["tail"]) != (pristine_fx["rc"], pristine_fx["tail"])
        crashed = "Traceback" in fx["stderr"] and "Traceback" not in pristine_fx["stderr"]
        if not same_tree or crashed:
            verdict = "harness-error"
        elif selftest_killed or fixture_killed:
            verdict = "killed"
        else:
            verdict = "survived"
        entry.update({
            "verdict": verdict,
            "tree_identical": same_tree,
            "pristine_selftest": {k: record["pristine"]["selftest"][k]
                                  for k in ("rc", "tail")},
            "mutant_selftest": {"rc": st["rc"], "tail": st["tail"],
                                "stderr_tail": st["stderr"].strip().splitlines()[-1:]},
            "selftest_killed": selftest_killed,
            "pristine_fixture": {k: pristine_fx[k] for k in ("rc", "tail", "stdout")},
            "mutant_fixture": {k: fx[k] for k in ("rc", "tail", "stdout", "stderr")},
            "fixture_killed": fixture_killed,
        })
        record["mutants"].append(entry)
    return record


def main(argv: list[str]) -> int:
    which = argv[1] if len(argv) > 1 and not argv[1].startswith("-") else "all"
    roots = prepare_cases()
    receipts = SCRATCH / "receipts"
    receipts.mkdir(parents=True, exist_ok=True)
    out: dict = {}
    if which in ("c1", "all"):
        out["c1"] = score_counter("c1", C1_MUTANTS, roots)
    if which in ("c2", "all"):
        out["c2"] = score_counter("c2", C2_MUTANTS, roots)
    (receipts / f"matrix-{which}.json").write_text(
        json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")

    rows = ["| mutant | fixture | selftest (pristine -> mutant) | fixture rc | verdict |",
            "|---|---|---|---|---|"]
    for kind, record in out.items():
        for entry in record["mutants"]:
            if "diff" in entry:
                (receipts / f"{kind}-{entry['name']}.diff").write_text(
                    entry["diff"], encoding="utf-8")
            if entry["verdict"] == "harness-error":
                rows.append(f"| {entry['name']} | {entry['variant']} | harness-error | - | "
                            f"{entry['verdict']} |")
                continue
            st = (f"{entry['pristine_selftest']['rc']}/{entry['pristine_selftest']['tail']}"
                  f" -> {entry['mutant_selftest']['rc']}/{entry['mutant_selftest']['tail']}")
            rows.append(f"| {entry['name']} | {entry['variant']} | {st} | "
                        f"{entry['pristine_fixture']['rc']} -> "
                        f"{entry['mutant_fixture']['rc']} | {entry['verdict']} |")
    (receipts / f"summary-{which}.md").write_text("\n".join(rows) + "\n", encoding="utf-8")

    for kind, record in out.items():
        print(f"== {kind} pristine selftest: rc={record['pristine']['selftest']['rc']} "
              f"{record['pristine']['selftest']['tail']}")
        for variant, fx in sorted(record["pristine"]["fixtures"].items()):
            print(f"   pristine[{variant}] rc={fx['rc']} :: {fx['tail'][:150]}")
            for extra in fx["stdout"].splitlines():
                if extra.startswith("# "):
                    print(f"      {extra[:150]}")
        for entry in record["mutants"]:
            print(f"{entry['verdict']:14s} {entry['name']}")
            if entry["verdict"] == "harness-error":
                print(f"               error={entry.get('error')}")
                continue
            print(f"               selftest pristine=({entry['pristine_selftest']['rc']})"
                  f"{entry['pristine_selftest']['tail']} mutant=({entry['mutant_selftest']['rc']})"
                  f"{entry['mutant_selftest']['tail']} killed={entry['selftest_killed']}")
            print(f"               fixture rc {entry['pristine_fixture']['rc']}->"
                  f"{entry['mutant_fixture']['rc']}")
            print(f"               pristine {entry['pristine_fixture']['tail'][:150]}")
            print(f"               mutant   {entry['mutant_fixture']['tail'][:150]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
