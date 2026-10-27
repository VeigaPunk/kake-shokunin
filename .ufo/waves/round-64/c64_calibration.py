#!/usr/bin/env python3
"""Round-64 C1 calibration counter — the repaired semantics-binding family.

Repairs routed to round 64 by the round-63 wave settlement and non-author
closure (corpus/lessons/round-63.md §Wave settlement,
round-63-verifier-spotcheck.md routed defect 1). Against the round-63 frozen
counter (c63_calibration.py) this counter:

  pins   — the retained raw blob, committed flat text, ledger, recipe and the
           located-line span are sha256/value constants below; any drift at
           the measured revision fails `pins` (kill rule: a pinned sha
           differing at the measured revision means the claim is unprovable).
  recipe — re-executes the committed extract_text.py over the retained raw
           blob inside this counter (recipe module loaded from the pinned
           revision blob, never from the worktree) and requires its output
           to equal the pinned flat text sha and the committed S432.txt blob
           byte-for-byte. Kills the round-63 circular text blob: a
           self-authored flat text cannot green the counter.
  class  — re-derives the match class inline from the recipe output and the
           raw blob (round-50 semantics; never gates on
           scripts/quote_class.py, keeping C1 verifiable without C2).
  located— re-derives the minimal raw-line range whose committed-recipe
           rendering contains the frozen span and requires it to equal the
           ledger's locatedRawLines and the pinned constant. Kills the
           round-63 M5 survivor (a mutated ledger fails both via the ledger
           sha pin and via this re-derivation).
  prose  — the round-64 lesson Gate must quote the round-61 spot-check's
           actual verdict reason span (block-level binding), name this
           counter, the derived class, and label its own assessment
           author-side; the QUALITY round-62 criterion block must name the
           located proposition; the knowledge [r63-correction] block must
           quote the frozen span and cite the ledger. Marker prose without
           those exact committed-byte spans cannot green the counter.
  unresolved — gated, not masked: `met` requires >=1 recorded S432
           disagreement, the lesson resolution above, and unresolved == 0.

Frozen predicate (identical sentence in contract.md, this code and the
receipts): at the measured revision this counter prints met=true (exit 0);
on each committed control fixture (marker-only, digest-consistent
fabrication, junk, ledger-mutation) it prints met=false (exit 1); at the
round-63 base it prints met=false (exit 1).

Usage: c64_calibration.py --root . --revision <rev>
       c64_calibration.py --selftest [--selftest-work <dir>]
Exits: 0 met or selftest green; 1 not met or selftest red;
       2 could-not-evaluate (input/usage fault).
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = "1a48131577ba82c967650561be34e8dba909432a"  # round-63 tip
RAW_REL = ".ufo/waves/round-61/sources/S432.html"
TEXT_REL = ".ufo/waves/round-63/quote-class/S432.txt"
LEDGER_REL = ".ufo/waves/round-63/quote-class/quote-classes.json"
RECIPE_REL = ".ufo/waves/round-63/quote-class/extract_text.py"
RAW_SHA = "63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b"
TEXT_SHA = "8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69"
LEDGER_SHA = "5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d"
RECIPE_SHA = "6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405"
EXPECTED_LOCATED = "6150-6154"
FROZEN_QUOTE = (
    "The `X-Content-Type-Options` response header can be used to require "
    "checking of a response\u2019s `Content-Type` header against the "
    "destination of a request."
)
PURPOSE_TERMS = ("X-Content-Type-Options", "Content-Type", "destination")
SPOT_REL = "corpus/lessons/round-61-verifier-spotcheck.md"
SPOT_VERDICT_SPAN = (
    "is only a generic lead-in, not substantive evidence for a "
    "response-header expectation"
)
CRITERION_SENTENCE = (
    "A quoted span must substantively support the proposition attributed "
    "to its source."
)
LESSON_REL = "corpus/lessons/round-64.md"
KNOWLEDGE_REL = "corpus/knowledge/response-header-expectations.md"
QUALITY_REL = "corpus/QUALITY.md"
SOURCES_REL = "corpus/SOURCES.md"
PIN_SHAS = {
    "raw": (RAW_REL, RAW_SHA),
    "text": (TEXT_REL, TEXT_SHA),
    "ledger": (LEDGER_REL, LEDGER_SHA),
    "recipe": (RECIPE_REL, RECIPE_SHA),
}
LOCATED_WINDOW = (6100, 6200)
LOCATED_SPAN_MAX = 15


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_show(root: str, revision: str, rel: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "-C", root, "show", f"{revision}:{rel}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode:
        return None
    return proc.stdout


def classify(quote: str, raw: str, text: str) -> str:
    """Round-50 class semantics, inlined (never gating on scripts/quote_class.py)."""
    if quote in raw:
        return "raw-substring"
    if quote in text:
        return "collapsed-only"
    return "absent"


def load_recipe(recipe_blob: bytes, work: str):
    """Materialize the committed recipe at a revision and import its extract()."""
    rpath = os.path.join(work, "extract_text.py")
    with open(rpath, "wb") as f:
        f.write(recipe_blob)
    spec = importlib.util.spec_from_file_location("c64_extract_text", rpath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_ledger(blob: bytes | None):
    """Parse the pinned ledger; returns (row, state). Never raises."""
    if blob is None:
        return None, "ledger_absent"
    try:
        parsed = json.loads(blob.decode("utf-8"))
        rows = parsed.get("classes")
        if not isinstance(rows, list):
            return None, "ledger_classes_not_list"
        row = next((r for r in rows
                    if isinstance(r, dict) and r.get("id") == "S432"), None)
        if row is None:
            return None, "no_s432_row"
        return row, "ok"
    except Exception as exc:
        return None, f"ledger_unreadable:{type(exc).__name__}"


def section(text: str, heading: str) -> str:
    """Text under `## <heading>` until the next `## ` heading (or EOF)."""
    m = re.search(rf"(?ms)^## {re.escape(heading)}[^\n]*\n(.*?)(?=^## |\Z)", text)
    return m.group(1) if m else ""


def correction_block(knowledge: str) -> str:
    m = re.search(r"(?ms)^\[r63-correction[^\n]*\n(.*?)(?=^\[r\d+-correction|^## |\Z)",
                  knowledge)
    return m.group(1) if m else ""


def derive_located(extract, raw_lines: list[str]) -> str:
    """Minimal raw-line range whose recipe rendering contains the frozen span.

    For each start a the first containing end b is minimal (renders grow
    monotonically with b); the global minimum span over the window is the
    located range. Window and max span are pinned constants.
    """
    best = None
    lo, hi = LOCATED_WINDOW
    for a in range(lo, hi + 1):
        for b in range(a, min(a + LOCATED_SPAN_MAX, len(raw_lines)) + 1):
            rendered = extract("\n".join(raw_lines[a - 1:b]).encode("utf-8"))
            if FROZEN_QUOTE in rendered:
                span = b - a
                if best is None or span < best[0]:
                    best = (span, a, b)
                break
    if best is None:
        return "unevaluable"
    return f"{best[1]}-{best[2]}"


def evaluate(root: str, rev: str) -> tuple[int, str]:
    probe = subprocess.run(
        ["git", "-C", root, "rev-parse", "--verify", rev],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if probe.returncode:
        print(f"could-not-evaluate: revision {rev} unreadable", file=sys.stderr)
        return 2, ""

    spot_blob = git_show(root, rev, SPOT_REL)
    if spot_blob is None:
        print("could-not-evaluate: round-61 verifier spot-check absent", file=sys.stderr)
        return 2, ""
    spot = spot_blob.decode("utf-8", errors="replace")
    disagreements = sum("S432" in ln and "Disagree" in ln for ln in spot.splitlines())

    blobs = {k: git_show(root, rev, rel) for k, (rel, _) in PIN_SHAS.items()}
    knowledge = (git_show(root, rev, KNOWLEDGE_REL) or b"").decode("utf-8", errors="replace")
    quality = (git_show(root, rev, QUALITY_REL) or b"").decode("utf-8", errors="replace")
    lesson = (git_show(root, rev, LESSON_REL) or b"").decode("utf-8", errors="replace")
    sources = (git_show(root, rev, SOURCES_REL) or b"").decode("utf-8", errors="replace")

    missing = [k for k, b in blobs.items() if b is None]
    drift = [k for k, b in blobs.items() if b is not None and sha256(b) != PIN_SHAS[k][1]]
    pins = int(not missing and not drift)
    if missing:
        pin_drift = "absent:" + ",".join(missing)
    elif drift:
        pin_drift = "drift:" + ",".join(drift)
    else:
        pin_drift = "none"

    recipe_rederive = 0
    derived = "unevaluable"
    class_match = 0
    located = "unevaluable"
    ledger_row, ledger_state = parse_ledger(blobs["ledger"] if pins else None)
    if pins and ledger_state == "ok":
        work = tempfile.mkdtemp(prefix="c64recipe-")
        try:
            try:
                mod = load_recipe(blobs["recipe"], work)
                out_text = mod.extract(blobs["raw"])
                if (out_text.encode("utf-8") == blobs["text"]
                        and sha256(out_text.encode("utf-8")) == TEXT_SHA):
                    recipe_rederive = 1
                else:
                    ledger_state = "recipe_output_differs"
            except Exception as exc:
                ledger_state = f"recipe_exec_failed:{type(exc).__name__}"
            if recipe_rederive:
                raw_s = blobs["raw"].decode("utf-8", errors="replace")
                text_s = blobs["text"].decode("utf-8", errors="replace")
                derived = classify(FROZEN_QUOTE, raw_s, text_s)
                class_match = int(derived == "collapsed-only"
                                  and ledger_row.get("matchClass") == "collapsed-only")
                located = derive_located(mod.extract, raw_s.split("\n"))
                if located != EXPECTED_LOCATED or ledger_row.get("locatedRawLines") != located:
                    located = f"mismatch:{located}"
                    class_match = 0
        finally:
            shutil.rmtree(work, ignore_errors=True)

    qblock = correction_block(knowledge)
    quote_correction = int(bool(qblock) and FROZEN_QUOTE in qblock and LEDGER_REL in qblock)
    r62 = section(quality, "Round-62 criteria")
    criterion = int(bool(r62) and CRITERION_SENTENCE in r62
                    and all(t in r62 for t in PURPOSE_TERMS))
    gate = section(lesson, "Gate")
    lesson_gate = int(
        bool(gate)
        and "S432 / Fetch" in gate
        and SPOT_VERDICT_SPAN in gate
        and "collapsed-only" in gate
        and "c64_calibration.py" in gate
        and ("author-side" in gate or "self-assessment" in gate))
    row_m = re.search(r"^\|\s*S432\s*\|", sources, re.M)
    source_row = 0
    if row_m:
        end = sources.find("\n", row_m.start())
        cells = [c.strip() for c in sources[row_m.start():end].split("|")]
        source_row = int(len(cells) >= 12 and cells[8] == "mined")

    unresolved = max(disagreements - (1 if lesson_gate else 0), 0)
    met = bool(pins and recipe_rederive and class_match and quote_correction
               and criterion and lesson_gate and source_row
               and disagreements >= 1 and unresolved == 0)
    out = (f"revision={rev} disagreements={disagreements} pins={pins} "
           f"pin_drift={pin_drift} recipe_rederive={recipe_rederive} "
           f"ledger_state={ledger_state} derived={derived} "
           f"class_match={class_match} located={located} "
           f"quote_correction={quote_correction} criterion={criterion} "
           f"lesson_gate={lesson_gate} source_row={source_row} "
           f"unresolved={unresolved} met={str(met).lower()}")
    return (0 if met else 1), out


# ----------------------------- selftest ------------------------------------

def _fixture(work: str, name: str, files: dict[str, bytes]) -> str:
    """Create one fixture git repo under work; returns its absolute path."""
    d = os.path.join(work, name)
    os.makedirs(d, exist_ok=True)
    for rel, data in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(data)
    def git(*a):
        return subprocess.run(["git", "-C", d, *a],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    git("init", "-q")
    top = git("rev-parse", "--show-toplevel")
    assert top.returncode == 0 and os.path.realpath(top.stdout.decode().strip()) == os.path.realpath(d), \
        f"fixture toplevel mismatch for {name}"
    git("config", "user.name", "c64-selftest")
    git("config", "user.email", "c64-selftest@fixture.invalid")
    git("add", "-A")
    c = git("commit", "-q", "--allow-empty", "-m", "fixture")
    assert c.returncode == 0, f"fixture commit failed for {name}"
    return d


def _head(d: str) -> str:
    out = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                         stdout=subprocess.PIPE, check=True)
    return out.stdout.decode().strip()


MARKER_SPOT = (
    "# spot\n\n| Item | Decision | Re-opened source | Agreement | Reason |\n"
    "|---|---|---|---|---|\n"
    "| S432 / Fetch | Admit | x | Disagree | planted marker reason |\n"
)
MARKER_KNOWLEDGE = (
    "# k\n\n[r63-correction 2026-10-30] planted correction marker.\n"
    "quote-classes ledger cited: .ufo/waves/round-63/quote-class/quote-classes.json\n"
)
MARKER_QUALITY = "# q\n\n## Round-62 criteria\n\nplanted criterion marker with X-Content-Type-Options Content-Type destination\n"
MARKER_LESSON = "# l\n\n## Gate\n\nplanted gate marker: S432 / Fetch resolved collapsed-only by c64_calibration.py author-side\n"
MARKER_SOURCES = "| S432 | t | docs | A | scope | anchor | teaches | mined | 2026-10-27 | 90d | — |\n"


def run_selftest(root: str, workdir: str | None) -> int:
    checks: list[tuple[str, bool]] = []

    def run_main(d: str, rev: str) -> tuple[int, str, str]:
        proc = subprocess.run(
            [sys.executable, "-B", os.path.abspath(__file__),
             "--root", d, "--revision", rev],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=dict(os.environ))
        return proc.returncode, proc.stdout.decode(), proc.stderr.decode()

    def expect(name: str, cond: bool):
        checks.append((name, bool(cond)))

    work = workdir or tempfile.mkdtemp(prefix="c64-selftest-")
    os.makedirs(work, exist_ok=True)
    real = {k: git_show(root, BASE, rel) for k, (rel, _) in PIN_SHAS.items()}
    if any(v is None for v in real.values()) or git_show(root, BASE, SPOT_REL) is None:
        print("selftest 0/0: pinned base blobs unavailable at --root", file=sys.stderr)
        return 2
    real_spot = git_show(root, BASE, SPOT_REL)

    try:
        # T1 no spot file -> could-not-evaluate
        d = _fixture(work, "t1-empty", {})
        code, out, err = run_main(d, _head(d))
        expect("t1 exit2", code == 2)
        expect("t1 token", "spot-check absent" in err)

        # T2 spot only -> pins=0
        d = _fixture(work, "t2-spot", {SPOT_REL: real_spot})
        code, out, err = run_main(d, _head(d))
        expect("t2 exit1", code == 1)
        expect("t2 disagreements", "disagreements=1" in out)
        expect("t2 pins0", "pins=0" in out and "absent:raw,text,ledger,recipe" in out)

        # T3 junk blobs -> sha drift named
        junk = {SPOT_REL: real_spot,
                RAW_REL: b"<html>planted</html>\n",
                TEXT_REL: b"planted text\n",
                LEDGER_REL: b'{"classes": "not-a-list"}',
                RECIPE_REL: b"def extract(x):\n    raise RuntimeError('x')\n"}
        d = _fixture(work, "t3-junk", junk)
        code, out, err = run_main(d, _head(d))
        expect("t3 exit1", code == 1)
        expect("t3 drift", "drift:raw,text,ledger,recipe" in out and "pins=0" in out)
        expect("t3 nocrash", "Traceback" not in err)

        # T4 digest-consistent fabrication: real blobs + marker prose
        fab = {SPOT_REL: real_spot, RAW_REL: real["raw"], TEXT_REL: real["text"],
               LEDGER_REL: real["ledger"], RECIPE_REL: real["recipe"],
               KNOWLEDGE_REL: MARKER_KNOWLEDGE.encode(), QUALITY_REL: MARKER_QUALITY.encode(),
               LESSON_REL: MARKER_LESSON.encode(), SOURCES_REL: MARKER_SOURCES.encode()}
        d = _fixture(work, "t4-fabrication", fab)
        code, out, err = run_main(d, _head(d))
        expect("t4 exit1", code == 1)
        expect("t4 pins1", "pins=1" in out)
        expect("t4 recipe1", "recipe_rederive=1" in out)
        expect("t4 class1", "class_match=1" in out)
        expect("t4 located", "located=6150-6154" in out)
        expect("t4 qcorr0", "quote_correction=0" in out)
        expect("t4 gate0", "lesson_gate=0" in out)
        expect("t4 unresolved", "unresolved=1" in out)
        expect("t4 metfalse", "met=false" in out)

        # T5 marker lesson quoting the real verdict span -> gate component isolates
        lesson5 = MARKER_LESSON.replace(
            "planted gate marker: ",
            "outside verdict: S432 / Fetch " + SPOT_VERDICT_SPAN + " — ")
        fab5 = dict(fab)
        fab5[LESSON_REL] = lesson5.encode()
        d = _fixture(work, "t5-gate-span", fab5)
        code, out, err = run_main(d, _head(d))
        expect("t5 exit1", code == 1)
        expect("t5 gate1", "lesson_gate=1" in out)
        expect("t5 unresolved0", "unresolved=0" in out)
        expect("t5 metfalse", "met=false" in out)

        # T6 unit: parse_ledger guards adversarial bytes without raising
        row, state = parse_ledger(b"{not json")
        expect("t6 guard", row is None and state.startswith("ledger_unreadable"))
        row, state = parse_ledger(b'{"classes": 3}')
        expect("t6 notlist", row is None and state == "ledger_classes_not_list")

        # T7 unit: derive_located pins the located span
        mod = load_recipe(real["recipe"], tempfile.mkdtemp(prefix="c64-t7-"))
        raw_lines = real["raw"].decode("utf-8", errors="replace").split("\n")
        expect("t7 located", derive_located(mod.extract, raw_lines) == EXPECTED_LOCATED)

        # T8 unit: bad revision -> exit 2
        d = _fixture(work, "t8-spot", {SPOT_REL: real_spot})
        code, out, err = run_main(d, "bogus-revision")
        expect("t8 exit2", code == 2)
        expect("t8 token", "unreadable" in err)
    finally:
        if workdir is None:
            shutil.rmtree(work, ignore_errors=True)

    total = len(checks)
    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print(f"check {name}: {'pass' if ok else 'FAIL'}")
    print(f"selftest {passed}/{total}")
    return 0 if passed == total else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision", default=BASE)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--selftest-work", default=None,
                    help="scratch dir for selftest fixtures (default: TMPDIR)")
    args = ap.parse_args()
    if args.selftest:
        return run_selftest(args.root, args.selftest_work)
    code, out = evaluate(args.root, args.revision)
    if out:
        print(out)
    return code


if __name__ == "__main__":
    sys.exit(main())
