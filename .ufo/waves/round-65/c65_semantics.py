#!/usr/bin/env python3
"""Round-65 C1 calibration counter — the routed green classes, counter-enforced.

Implements the frozen round-65 contract (`.ufo/waves/round-65/contract.md`
§C1, predicate v2) against the round-64 survivors. The round-64 counter
(c64_calibration.py) authenticates its four evidence blobs but its prose
gates are block-scoped substring tests; the round-64 wave reproduced three
green classes it cannot see, and the round-64 closure routed exactly these
(corpus/lessons/round-64-verifier-spotcheck.md defect 1):

  A1 marker-only prose    — w1/ReviewerC1Prose.md `minimal`: a Gate of bare
                            frozen tokens (ids, span, class, counter name,
                            author-side label) with no attribution greens.
  A2 contradictory prose  — w1/ReviewerC1Prose.md `contradictory`: a Gate
                            that also denies resolution greens.
  A3 hidden criterion     — w1/MutC1Prose.md Q3x: the QUALITY criterion kept
                            inside an HTML comment greens.
  A4 outside-verdict tamper — w1/ScoutSpotSpan.md A1/fxB: the spot file is
                            not pinned, so a verdict reword or flip greens
                            (A1) or leaves the counter blind (fxB).

This counter keeps the round-64 byte bindings (recipe re-execution, class
re-derivation, located-line range — unchanged semantics, re-implemented
inline) and adds the routed enforcement:

  pins                  — the four evidence blobs PLUS the round-61 spot
                          file, the round-64 lesson and the round-64 QUALITY
                          attack-addendum region are sha256 constants; any
                          drift at the measured revision fails `pins`.
  disagreements         — the spot file carries its S432/Disagree lines; the
                          >=1 input stays live (printed as a count).
  spot_auth             — the Gate quotes the frozen verdict span verbatim,
                          names the spot file as the span's source
                          (attribution, not copied text), and the span is
                          present in the pinned spot bytes themselves.
  criterion_visible     — the round-62 substantive-support criterion exists
                          in QUALITY AFTER HTML comments are stripped, and
                          names its grounding lesson in the same section.
  gate_noncontradictory — the Gate contains the frozen admission span and no
                          frozen contradiction span outside a historical
                          settlement context.
  quote_class           — the ledger class re-derives collapsed-only inline
                          from the pinned blob via the committed extract
                          recipe (never gating on scripts/quote_class.py).
  unresolved            — max(disagreements - (1 if admission block fully
                          green else 0), 0); 0 only when that block is green.

Frozen predicate (identical sentence in contract.md §C1 v2, this docstring
and the receipt labels): at the measured revision this counter prints
met=true (exit 0); against each differential attack fixture A1/A2/A3 it
prints met=false (exit 1) naming the failed component while c64_calibration.py
prints met=true on the same fixtures (the routed green classes reproduced);
against A4 it prints met=false; --selftest prints all checks passing;
`git cat-file -e <base>:.ufo/waves/round-65/c65_semantics.py` fails at the
base (the do-nothing tree has no instrument).

Honest, frozen limitation (contract §C1 do-nothing control): the counter
authenticates BYTES, not tree identity. A tree carrying copied genuine
lesson/QUALITY/knowledge text (the real bytes, no round-64 settlement
context around them) still greens — including the base revision itself,
where the round-64 lesson bytes already exist. The claim's falsifiable
delta is the fixture differential plus instrument existence, not byte
presence.

Contradiction-span scope (documented heuristic, block-scoped, not semantic):
a contradiction span counts only on a Gate line that names no evidence
artifact (`\\.ufo/waves/`, `round-<N>-verifier-spotcheck`, `round-<N>.md`,
`w1/`, `c6<N>_<tool>`). Lines that cite their evidence are historical
settlement records (the round-64 lesson records prior dispositions that
way); a naked denial in prose is a live contradiction. This is not a
semantic-resolution proof — the round-64 QUALITY addendum already rules
block-scoped token presence is not semantic resolution; this counter
enforces the narrower routed classes only.

Usage: c65_semantics.py --root . --revision <rev>
       c65_semantics.py --selftest [--selftest-work <dir>]
Exits: 0 met or selftest green; 1 not met or selftest red;
       2 could-not-evaluate (input/usage fault; never a traceback).
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

BASE = "d3a4e40228c307954fa6ced6cab03654faac1ffa"  # round-64 wrap-up tip
RAW_REL = ".ufo/waves/round-61/sources/S432.html"
TEXT_REL = ".ufo/waves/round-63/quote-class/S432.txt"
LEDGER_REL = ".ufo/waves/round-63/quote-class/quote-classes.json"
RECIPE_REL = ".ufo/waves/round-63/quote-class/extract_text.py"
RAW_SHA = "63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b"
TEXT_SHA = "8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69"
LEDGER_SHA = "5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d"
RECIPE_SHA = "6b0a88cddfa3b712e8fdbe69c4c2803c816490cd43893972dfe0d39d5f362405"
SPOT_REL = "corpus/lessons/round-61-verifier-spotcheck.md"
SPOT_SHA = "b4faa46bb618399b02d8dc52e14a7f785bb87c17697737f5a92c92621203d013"
LESSON_REL = "corpus/lessons/round-64.md"
LESSON_SHA = "c863acc33a3ff6fdfee6781229c90f98695bd8d354bef0d907194335bff7769b"
QUALITY_REL = "corpus/QUALITY.md"
KNOWLEDGE_REL = "corpus/knowledge/response-header-expectations.md"
SOURCES_REL = "corpus/SOURCES.md"
ADDENDUM_HEADING = "Round-64 attack addendum"
ADDENDUM_REGION_SHA = (
    "be2cd47da43a72535fc095be4a078de4f373940401637aa58327de23c11151e2")
PIN_SHAS = {
    "raw": (RAW_REL, RAW_SHA),
    "text": (TEXT_REL, TEXT_SHA),
    "ledger": (LEDGER_REL, LEDGER_SHA),
    "recipe": (RECIPE_REL, RECIPE_SHA),
    "spot": (SPOT_REL, SPOT_SHA),
    "lesson": (LESSON_REL, LESSON_SHA),
    "quality_region": (QUALITY_REL, ADDENDUM_REGION_SHA),  # region rule below
}
SPOT_VERDICT_SPAN = (
    "is only a generic lead-in, not substantive evidence for a "
    "response-header expectation")
SPOT_FILE_TOKEN = SPOT_REL
ADMISSION_SPAN = "round's calibration evidence resolves"
CONTRADICTION_SPANS = (
    "withhold semantic-counter credit",
    "The verdict above is rejected",
    "No disagreement is resolved by this gate",
)
EVIDENCE_POINTER_RE = re.compile(
    r"(?:\.ufo/waves/|round-\d+-verifier-spotcheck|round-\d+\.md|w1/|c6\d_[a-z0-9_]+)")
CRITERION_SENTENCE = (
    "A quoted span must substantively support the proposition attributed "
    "to its source.")
CRITERION_GROUNDING = "round-61-verifier-spotcheck"
FROZEN_QUOTE = (
    "The `X-Content-Type-Options` response header can be used to require "
    "checking of a response\u2019s `Content-Type` header against the "
    "destination of a request.")
EXPECTED_LOCATED = "6150-6154"
LOCATED_WINDOW = (6100, 6200)
LOCATED_SPAN_MAX = 15
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_show(root: str, revision: str, rel: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "-C", root, "show", f"{revision}:{rel}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode:
        return None
    return proc.stdout


def section(text: str, heading: str) -> str:
    """Text under `## <heading>` until the next `## ` heading (or EOF)."""
    m = re.search(rf"(?ms)^## {re.escape(heading)}[^\n]*\n(.*?)(?=^## |\Z)", text)
    return m.group(1) if m else ""


def strip_comments(text: str) -> str:
    return HTML_COMMENT_RE.sub("", text)


def live_contradiction(gate: str) -> str | None:
    """First contradiction span appearing on a Gate line with no evidence
    pointer (historical settlement lines cite their artifacts)."""
    for line in gate.splitlines():
        if EVIDENCE_POINTER_RE.search(line):
            continue
        for span in CONTRADICTION_SPANS:
            if span in line:
                return span
    return None


def classify(quote: str, raw: str, text: str) -> str:
    """Round-50 class semantics, inlined (never gating on scripts/quote_class.py)."""
    if quote in raw:
        return "raw-substring"
    if quote in text:
        return "collapsed-only"
    return "absent"


def load_recipe(recipe_blob: bytes, work: str):
    rpath = os.path.join(work, "extract_text.py")
    with open(rpath, "wb") as f:
        f.write(recipe_blob)
    spec = importlib.util.spec_from_file_location("c65_extract_text", rpath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_ledger(blob: bytes | None):
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


def derive_located(extract, raw_lines: list[str]) -> str:
    """Minimal raw-line range whose recipe rendering contains the frozen span."""
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
    spot_lines = spot.splitlines()
    disagreements = sum("S432" in ln and "Disagree" in ln for ln in spot_lines)

    raw_blob = git_show(root, rev, RAW_REL)
    text_blob = git_show(root, rev, TEXT_REL)
    ledger_blob = git_show(root, rev, LEDGER_REL)
    recipe_blob = git_show(root, rev, RECIPE_REL)
    lesson = (git_show(root, rev, LESSON_REL) or b"").decode("utf-8", errors="replace")
    quality = (git_show(root, rev, QUALITY_REL) or b"").decode("utf-8", errors="replace")

    present = {
        "raw": raw_blob, "text": text_blob, "ledger": ledger_blob,
        "recipe": recipe_blob, "spot": spot_blob, "lesson": git_show(root, rev, LESSON_REL),
    }
    quality_region = section(quality, ADDENDUM_HEADING)
    missing = [k for k, b in present.items() if b is None]
    drift = [k for k, b in present.items()
             if b is not None and sha256(b) != PIN_SHAS[k][1]]
    if quality_region:
        region_blob = ("## " + ADDENDUM_HEADING + quality_region).encode("utf-8")
        if sha256(region_blob) != ADDENDUM_REGION_SHA:
            drift.append("quality_region")
    else:
        missing.append("quality_region")
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
    ledger_state = "unevaluated"
    quote_class = 0
    if pins:
        ledger_row, ledger_state = parse_ledger(ledger_blob)
        work = tempfile.mkdtemp(prefix="c65recipe-")
        try:
            try:
                mod = load_recipe(recipe_blob, work)
                out_text = mod.extract(raw_blob)
                if (out_text.encode("utf-8") == text_blob
                        and sha256(out_text.encode("utf-8")) == TEXT_SHA):
                    recipe_rederive = 1
                else:
                    ledger_state = "recipe_output_differs"
            except Exception as exc:
                ledger_state = f"recipe_exec_failed:{type(exc).__name__}"
            if recipe_rederive and ledger_state == "ok":
                raw_s = raw_blob.decode("utf-8", errors="replace")
                text_s = text_blob.decode("utf-8", errors="replace")
                derived = classify(FROZEN_QUOTE, raw_s, text_s)
                class_match = int(derived == "collapsed-only"
                                  and ledger_row.get("matchClass") == "collapsed-only")
                located = derive_located(mod.extract, raw_s.split("\n"))
                if located != EXPECTED_LOCATED or ledger_row.get("locatedRawLines") != located:
                    located = f"mismatch:{located}"
                    class_match = 0
                quote_class = int(recipe_rederive and class_match == 1)
        finally:
            shutil.rmtree(work, ignore_errors=True)

    gate = section(lesson, "Gate")
    spot_auth = int(
        bool(gate)
        and SPOT_VERDICT_SPAN in gate
        and SPOT_FILE_TOKEN in gate
        and SPOT_VERDICT_SPAN in spot
        and sha256(spot_blob) == SPOT_SHA)
    visible_quality = strip_comments(quality)
    visible_r62 = section(visible_quality, "Round-62 criteria")
    criterion_visible = int(
        bool(visible_r62)
        and CRITERION_SENTENCE in visible_r62
        and CRITERION_GROUNDING in visible_r62)
    contradiction = live_contradiction(gate)
    gate_noncontradictory = int(
        bool(gate)
        and ADMISSION_SPAN in gate
        and contradiction is None)

    admission_green = bool(spot_auth and criterion_visible and gate_noncontradictory)
    unresolved = max(disagreements - (1 if admission_green else 0), 0)
    met = bool(pins and disagreements >= 1 and spot_auth and criterion_visible
               and gate_noncontradictory and quote_class and unresolved == 0)
    out = (f"revision={rev} disagreements={disagreements} pins={pins} "
           f"pin_drift={pin_drift} spot_auth={spot_auth} "
           f"criterion_visible={criterion_visible} "
           f"gate_noncontradictory={gate_noncontradictory} "
           f"contradiction={contradiction or 'none'} "
           f"recipe_rederive={recipe_rederive} ledger_state={ledger_state} "
           f"derived={derived} located={located} quote_class={quote_class} "
           f"unresolved={unresolved} met={str(met).lower()}")
    return (0 if met else 1), out


# ----------------------------- selftest ------------------------------------

def _fixture(work: str, name: str, files: dict[str, bytes]) -> str:
    """Create one deterministic fixture git repo under work; returns its path."""
    d = os.path.join(work, name)
    os.makedirs(d, exist_ok=True)
    for rel, data in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(data)

    def git(*a):
        return subprocess.run(["git", "-C", d, "-c", "core.autocrlf=false", *a],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    git("init", "-q")
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert top.returncode == 0 and os.path.realpath(top.stdout.decode().strip()) == os.path.realpath(d), \
        f"fixture toplevel mismatch for {name}"
    git("config", "core.autocrlf", "false")
    git("config", "user.name", "c65-selftest")
    git("config", "user.email", "c65-selftest@fixture.invalid")
    git("add", "-A")
    c = git("commit", "-q", "--allow-empty", "-m", "fixture")
    assert c.returncode == 0, f"fixture commit failed for {name}"
    return d


def _head(d: str) -> str:
    out = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                         stdout=subprocess.PIPE, check=True)
    return out.stdout.decode().strip()


MARKER_GATE = (
    "## Gate\n\n"
    "S432 / Fetch " + SPOT_VERDICT_SPAN + "\n"
    "collapsed-only c64_calibration.py author-side\n")


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

    work = workdir or tempfile.mkdtemp(prefix="c65-selftest-")
    os.makedirs(work, exist_ok=True)
    rels = [RAW_REL, TEXT_REL, LEDGER_REL, RECIPE_REL, SPOT_REL, LESSON_REL,
            QUALITY_REL, KNOWLEDGE_REL, SOURCES_REL]
    real = {rel: git_show(root, BASE, rel) for rel in rels}
    if any(v is None for v in real.values()):
        print("selftest 0/0: pinned base blobs unavailable at --root", file=sys.stderr)
        return 2
    lesson_s = real[LESSON_REL].decode("utf-8")
    gate_body = section(lesson_s, "Gate")
    real_lesson_nogate = lesson_s.replace("## Gate\n" + gate_body, "")
    quality_s = real[QUALITY_REL].decode("utf-8")
    crit_line = ("- **A quoted span must substantively support the proposition "
                 "attributed to its source.**")
    spot_s = real[SPOT_REL].decode("utf-8")

    try:
        # T1 no spot file -> could-not-evaluate
        d = _fixture(work, "t1-empty", {})
        code, out, err = run_main(d, _head(d))
        expect("t1 exit2", code == 2)
        expect("t1 token", "spot-check absent" in err)

        # T2 spot only -> pins=0 naming absent keys
        d = _fixture(work, "t2-spot", {SPOT_REL: real[SPOT_REL]})
        code, out, err = run_main(d, _head(d))
        expect("t2 exit1", code == 1)
        expect("t2 disagreements", "disagreements=1" in out)
        expect("t2 pins0", "pins=0" in out
               and "absent:raw,text,ledger,recipe,lesson,quality_region" in out)

        # T3 junk blobs -> sha drift named, no crash
        junk = {SPOT_REL: real[SPOT_REL],
                RAW_REL: b"<html>planted</html>\n",
                TEXT_REL: b"planted text\n",
                LEDGER_REL: b'{"classes": "not-a-list"}',
                RECIPE_REL: b"def extract(x):\n    raise RuntimeError('x')\n",
                LESSON_REL: real[LESSON_REL], QUALITY_REL: real[QUALITY_REL]}
        d = _fixture(work, "t3-junk", junk)
        code, out, err = run_main(d, _head(d))
        expect("t3 exit1", code == 1)
        expect("t3 drift", "drift:raw,text,ledger,recipe" in out and "pins=0" in out)
        expect("t3 nocrash", "Traceback" not in err)

        # T4 (A1 shape) real evidence + marker gate with no attribution.
        # Knowledge and SOURCES ride along verbatim so the round-64 counter
        # (c64) prints met=true here — the differential under test is the
        # marker-gate class, not missing-file noise.
        lesson_a1 = real_lesson_nogate + "\n" + MARKER_GATE
        d = _fixture(work, "t4-marker-gate", {
            RAW_REL: real[RAW_REL], TEXT_REL: real[TEXT_REL],
            LEDGER_REL: real[LEDGER_REL], RECIPE_REL: real[RECIPE_REL],
            SPOT_REL: real[SPOT_REL], LESSON_REL: lesson_a1.encode("utf-8"),
            QUALITY_REL: real[QUALITY_REL],
            KNOWLEDGE_REL: real[KNOWLEDGE_REL], SOURCES_REL: real[SOURCES_REL]})
        code, out, err = run_main(d, _head(d))
        expect("t4 exit1", code == 1)
        expect("t4 spotauth0", "spot_auth=0" in out)
        expect("t4 metfalse", "met=false" in out)
        # The gate mutation necessarily trips the lesson byte pin too; the
        # named failed component for the A1 class is spot_auth (no attribution).
        expect("t4 pin-drift-lesson", "drift:lesson" in out)

        # T5 (A2 shape) real tree + Gate extended with a naked contradiction
        lesson_a2 = real[LESSON_REL].decode("utf-8").replace(
            "## Sources census",
            "Resolution withheld per taste: withhold semantic-counter credit. "
            "The verdict above is rejected. No disagreement is resolved by this "
            "gate.\n\n## Sources census", 1)
        expect("t5 edit-applied", lesson_a2 != real[LESSON_REL].decode("utf-8"))
        d = _fixture(work, "t5-contradictory", {
            RAW_REL: real[RAW_REL], TEXT_REL: real[TEXT_REL],
            LEDGER_REL: real[LEDGER_REL], RECIPE_REL: real[RECIPE_REL],
            SPOT_REL: real[SPOT_REL], LESSON_REL: lesson_a2.encode("utf-8"),
            QUALITY_REL: real[QUALITY_REL],
            KNOWLEDGE_REL: real[KNOWLEDGE_REL], SOURCES_REL: real[SOURCES_REL]})
        code, out, err = run_main(d, _head(d))
        expect("t5 exit1", code == 1)
        expect("t5 gatenc0", "gate_noncontradictory=0" in out)
        expect("t5 span-named", "contradiction=withhold semantic-counter credit" in out)
        expect("t5 metfalse", "met=false" in out)

        # T6 (A3 shape / MutC1Prose Q3x) criterion hidden in an HTML comment
        quality_a3 = quality_s.replace(crit_line, "<!-- " + crit_line + " -->", 1)
        expect("t6 edit-applied", quality_a3 != quality_s)
        d = _fixture(work, "t6-hidden-criterion", {
            RAW_REL: real[RAW_REL], TEXT_REL: real[TEXT_REL],
            LEDGER_REL: real[LEDGER_REL], RECIPE_REL: real[RECIPE_REL],
            SPOT_REL: real[SPOT_REL], LESSON_REL: real[LESSON_REL],
            QUALITY_REL: quality_a3.encode("utf-8"),
            KNOWLEDGE_REL: real[KNOWLEDGE_REL], SOURCES_REL: real[SOURCES_REL]})
        code, out, err = run_main(d, _head(d))
        expect("t6 exit1", code == 1)
        expect("t6 critvis0", "criterion_visible=0" in out)
        expect("t6 metfalse", "met=false" in out)

        # T7 the real base tree greens (frozen do-nothing limitation, documented)
        code, out, err = run_main(root, BASE)
        expect("t7 exit0", code == 0)
        expect("t7 mettrue", "met=true" in out)
        expect("t7 allgreen", "spot_auth=1" in out and "criterion_visible=1" in out
               and "gate_noncontradictory=1" in out and "quote_class=1" in out)

        # T8 (ScoutSpotSpan A1) spot verdict reworded, lesson unchanged -> pins red
        reworded = spot_s.replace(SPOT_VERDICT_SPAN,
                                  "merely introduces a value list, not a rule", 1)
        expect("t8 edit-applied", reworded != spot_s)
        d = _fixture(work, "t8-spot-reword", {
            RAW_REL: real[RAW_REL], TEXT_REL: real[TEXT_REL],
            LEDGER_REL: real[LEDGER_REL], RECIPE_REL: real[RECIPE_REL],
            SPOT_REL: reworded.encode("utf-8"), LESSON_REL: real[LESSON_REL],
            QUALITY_REL: real[QUALITY_REL],
            KNOWLEDGE_REL: real[KNOWLEDGE_REL], SOURCES_REL: real[SOURCES_REL]})
        code, out, err = run_main(d, _head(d))
        expect("t8 exit1", code == 1)
        expect("t8 pins0", "pins=0" in out and "drift:spot" in out)
        expect("t8 metfalse", "met=false" in out)

        # T9 (A4 shape / ScoutSpotSpan fxB) Disagree->Agree flip
        flipped = spot_s.replace("Disagree", "Agree", 1)
        d = _fixture(work, "t9-flip", {
            RAW_REL: real[RAW_REL], TEXT_REL: real[TEXT_REL],
            LEDGER_REL: real[LEDGER_REL], RECIPE_REL: real[RECIPE_REL],
            SPOT_REL: flipped.encode("utf-8"), LESSON_REL: real[LESSON_REL],
            QUALITY_REL: real[QUALITY_REL],
            KNOWLEDGE_REL: real[KNOWLEDGE_REL], SOURCES_REL: real[SOURCES_REL]})
        code, out, err = run_main(d, _head(d))
        expect("t9 exit1", code == 1)
        expect("t9 pins0", "pins=0" in out)
        expect("t9 disagreements0", "disagreements=0" in out)
        expect("t9 metfalse", "met=false" in out)

        # T10 unit: historical settlement lines (evidence pointer) are excluded
        gate_hist = ("Admission stays bounded: per "
                     ".ufo/waves/round-64/w1/ReviewerC1Prose.md the frozen kill "
                     "rule withholds semantic-counter credit.\n")
        expect("t10 excluded", live_contradiction(gate_hist) is None)
        gate_live = ("Resolution withheld per taste: withhold semantic-counter "
                     "credit.\n")
        expect("t10 counted", live_contradiction(gate_live) is not None)

        # T11 unit: HTML-comment stripping
        expect("t11 stripped", CRITERION_SENTENCE not in strip_comments(
            "<!-- " + CRITERION_SENTENCE + " --> tail"))
        expect("t11 visible", CRITERION_SENTENCE in strip_comments(
            "head " + CRITERION_SENTENCE + " tail"))

        # T12 unit: bad revision -> exit 2
        d = _fixture(work, "t12-spot", {SPOT_REL: real[SPOT_REL]})
        code, out, err = run_main(d, "bogus-revision")
        expect("t12 exit2", code == 2)
        expect("t12 token", "unreadable" in err)
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
    try:
        code, out = evaluate(args.root, args.revision)
    except Exception as exc:
        print(f"could-not-evaluate: internal fault: {type(exc).__name__}",
              file=sys.stderr)
        return 2
    if out:
        print(out)
    return code


if __name__ == "__main__":
    sys.exit(main())
