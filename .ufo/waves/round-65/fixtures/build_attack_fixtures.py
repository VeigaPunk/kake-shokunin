#!/usr/bin/env python3
"""Build the round-65 attack and control fixture repositories.

Usage: build_attack_fixtures.py <workdir> --lane <lane-root> [--base <rev>]

Creates, under <workdir>, one deterministic git repository per fixture
(init + config + fixed-identity commit; toplevel verified; core.autocrlf
disabled so committed blobs are byte-exact on any host):

  A1-marker    the routed marker-only prose class (ReviewerC1Prose
               `minimal`): the real base bytes for every pinned evidence
               blob plus the spot/QUALITY/knowledge/SOURCES files, with the
               round-64 lesson's Gate section replaced by a bare-token
               marker gate (frozen ids, verdict span as a bare token,
               class, counter name, author-side label) carrying NO
               attribution and NO admission span. c64 greens; c65's
               spot_auth fails.
  A2-contradictory
               the routed contradictory-prose class (ReviewerC1Prose
               `contradictory`): real bytes plus one naked contradiction
               line inside the Gate (no evidence pointer on the line).
               c64 greens; c65's gate_noncontradictory fails.
  A3-hidden-criterion
               the routed hidden-comment class (MutC1Prose Q3x): real
               bytes with the round-62 substantive-support criterion
               wrapped in an HTML comment. c64 greens; c65's
               criterion_visible fails.
  A4-tamper    the routed outside-verdict tamper (ScoutSpotSpan fxB): real
               bytes with the spot file's S432 row flipped Disagree->Agree.
               c65's pins/disagreements fail (c64 goes red too via its
               disagreements>=1 gate — recorded as-is, not a differential).
  donothing-c1-copied
               the contract §C1 do-nothing-copied control: a tree carrying
               only copied genuine prose (the real lesson/QUALITY/knowledge/
               spot bytes, no round-64 settlement context around them) plus
               the real evidence blobs. c65 greens it — the frozen honest
               limitation (byte authentication, not tree identity).
  c2-drift     contract §C2 do-nothing drift control: the round-64
               S432.live.html blob with ONE byte changed, plus a correct
               pin file. check_s432_pin.py: match=0.
  c2-wrongpin  contract §C2 wrong-pin control: the real blob plus a pin
               file naming a different digest. check_s432_pin.py: pin=0.

Every fixture commit uses fixed author/committer identity and date, so two
runs of this builder print identical revisions (the receipts assert this).
Each fixture prints one JSON line:
  {"name", "path", "revision", "provenance": [{"path", "source", "sha256", "note"}]}
Provenance is per-path and honest: "verbatim <base>:<rel>" (byte-equal to
the lane blob) or "mutation of <base>:<rel>" with the exact edit named, or
"synthetic" for built files.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys

BASE_DEFAULT = "d3a4e40228c307954fa6ced6cab03654faac1ffa"
RAW_REL = ".ufo/waves/round-61/sources/S432.html"
TEXT_REL = ".ufo/waves/round-63/quote-class/S432.txt"
LEDGER_REL = ".ufo/waves/round-63/quote-class/quote-classes.json"
RECIPE_REL = ".ufo/waves/round-63/quote-class/extract_text.py"
SPOT_REL = "corpus/lessons/round-61-verifier-spotcheck.md"
LESSON_REL = "corpus/lessons/round-64.md"
QUALITY_REL = "corpus/QUALITY.md"
KNOWLEDGE_REL = "corpus/knowledge/response-header-expectations.md"
SOURCES_REL = "corpus/SOURCES.md"
LIVE_REL = ".ufo/waves/round-64/sources/S432.live.html"
LIVE_SHA = "63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b"
VERDICT_SPAN = ("is only a generic lead-in, not substantive evidence for a "
                "response-header expectation")
CRIT_LINE = ("- **A quoted span must substantively support the proposition "
             "attributed to its source.**")
GATE_HEADING = "## Gate"
MARKER_GATE = (
    "## Gate\n\n"
    "S432 / Fetch " + VERDICT_SPAN + "\n"
    "collapsed-only c64_calibration.py author-side\n")
CONTRADICTION_LINE = (
    "Resolution withheld per taste: withhold semantic-counter credit. "
    "The verdict above is rejected. No disagreement is resolved by this gate.\n")

FIXED_DATE = "2026-11-01T00:00:00+00:00"
FIXED_NAME = "kake-r65-fixture"
FIXED_EMAIL = "kake-r65-fixture@fixture.invalid"


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_show(lane: str, rev: str, rel: str) -> bytes:
    p = subprocess.run(["git", "-C", lane, "show", f"{rev}:{rel}"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise SystemExit(f"cannot read {rev}:{rel} from {lane}")
    return p.stdout


def section(text: str, heading: str) -> str:
    import re
    m = re.search(rf"(?ms)^## {re.escape(heading)}[^\n]*\n(.*?)(?=^## |\Z)", text)
    return m.group(1) if m else ""


def build_fixture(work: str, name: str, files: dict[str, bytes],
                  provenance: list[dict]) -> dict:
    d = os.path.join(work, name)
    os.makedirs(d, exist_ok=True)
    for rel, data in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(data)
    env = dict(os.environ)
    env.update({
        "GIT_AUTHOR_NAME": FIXED_NAME, "GIT_AUTHOR_EMAIL": FIXED_EMAIL,
        "GIT_AUTHOR_DATE": FIXED_DATE,
        "GIT_COMMITTER_NAME": FIXED_NAME, "GIT_COMMITTER_EMAIL": FIXED_EMAIL,
        "GIT_COMMITTER_DATE": FIXED_DATE,
    })

    def git(*a):
        r = subprocess.run(["git", "-C", d, "-c", "core.autocrlf=false", *a],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           env=env)
        if r.returncode:
            raise SystemExit(f"git {a[0]} failed for {name}: "
                             f"{r.stderr.decode(errors='replace')[:300]}")
        return r.stdout

    git("init", "-q")
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    if top.returncode != 0 or os.path.realpath(
            top.stdout.decode().strip()) != os.path.realpath(d):
        raise SystemExit(f"fixture toplevel mismatch for {name}")
    git("config", "core.autocrlf", "false")
    git("add", "-A")
    git("commit", "-q", "--allow-empty", "-m", f"round-65 fixture {name}")
    head = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                          stdout=subprocess.PIPE, env=env, check=True)
    return {"name": name, "path": d,
            "revision": head.stdout.decode().strip(),
            "provenance": provenance}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("workdir")
    ap.add_argument("--lane", required=True)
    ap.add_argument("--base", default=BASE_DEFAULT)
    args = ap.parse_args()
    os.makedirs(args.workdir, exist_ok=True)
    lane, base = args.lane, args.base

    ev = {rel: git_show(lane, base, rel)
          for rel in (RAW_REL, TEXT_REL, LEDGER_REL, RECIPE_REL)}
    spot = git_show(lane, base, SPOT_REL)
    lesson = git_show(lane, base, LESSON_REL)
    quality = git_show(lane, base, QUALITY_REL)
    knowledge = git_show(lane, base, KNOWLEDGE_REL)
    sources = git_show(lane, base, SOURCES_REL)
    live = git_show(lane, base, LIVE_REL)
    if sha256(live) != LIVE_SHA:
        raise SystemExit("round-64 S432.live.html blob does not match the "
                         "frozen digest at --base; refusing to build")

    verbatim = lambda rel: {"path": rel, "source": f"verbatim {base}:{rel}",
                            "sha256": None, "note": "byte-equal to lane blob"}
    out = []

    # ---- A1 marker-only -------------------------------------------------
    lesson_s = lesson.decode("utf-8")
    gate_body = section(lesson_s, "Gate")
    lesson_a1 = lesson_s.replace(GATE_HEADING + "\n" + gate_body, "") + "\n" + MARKER_GATE
    assert lesson_a1 != lesson_s and VERDICT_SPAN in MARKER_GATE
    files = dict(ev)
    files[SPOT_REL] = spot
    files[LESSON_REL] = lesson_a1.encode("utf-8")
    files[QUALITY_REL] = quality
    files[KNOWLEDGE_REL] = knowledge
    files[SOURCES_REL] = sources
    prov = [verbatim(RAW_REL), verbatim(TEXT_REL), verbatim(LEDGER_REL),
            verbatim(RECIPE_REL), verbatim(SPOT_REL), verbatim(QUALITY_REL),
            verbatim(KNOWLEDGE_REL), verbatim(SOURCES_REL),
            {"path": LESSON_REL, "source": f"mutation of {base}:{LESSON_REL}",
             "sha256": sha256(files[LESSON_REL]),
             "note": ("Gate section replaced by the bare-token marker gate "
                      "(ReviewerC1Prose minimal shape): frozen ids and span "
                      "as a bare token, class, counter name, author-side "
                      "label; NO spot-file attribution, NO admission span")}]
    out.append(build_fixture(args.workdir, "A1-marker", files, prov))

    # ---- A2 contradictory -----------------------------------------------
    anchor = "## Sources census"
    assert anchor in lesson_s
    lesson_a2 = lesson_s.replace(anchor, CONTRADICTION_LINE + "\n" + anchor, 1)
    files = dict(ev)
    files[SPOT_REL] = spot
    files[LESSON_REL] = lesson_a2.encode("utf-8")
    files[QUALITY_REL] = quality
    files[KNOWLEDGE_REL] = knowledge
    files[SOURCES_REL] = sources
    prov = [verbatim(RAW_REL), verbatim(TEXT_REL), verbatim(LEDGER_REL),
            verbatim(RECIPE_REL), verbatim(SPOT_REL), verbatim(QUALITY_REL),
            verbatim(KNOWLEDGE_REL), verbatim(SOURCES_REL),
            {"path": LESSON_REL, "source": f"mutation of {base}:{LESSON_REL}",
             "sha256": sha256(files[LESSON_REL]),
             "note": ("one naked contradiction line inserted inside the Gate "
                      "(before the Sources census heading), no evidence "
                      "pointer on the line (ReviewerC1Prose contradictory "
                      "shape on the real tree)")}]
    out.append(build_fixture(args.workdir, "A2-contradictory", files, prov))

    # ---- A3 hidden criterion --------------------------------------------
    quality_s = quality.decode("utf-8")
    assert quality_s.count(CRIT_LINE) == 1, "criterion line not found once"
    quality_a3 = quality_s.replace(CRIT_LINE, "<!-- " + CRIT_LINE + " -->", 1)
    files = dict(ev)
    files[SPOT_REL] = spot
    files[LESSON_REL] = lesson
    files[QUALITY_REL] = quality_a3.encode("utf-8")
    files[KNOWLEDGE_REL] = knowledge
    files[SOURCES_REL] = sources
    prov = [verbatim(RAW_REL), verbatim(TEXT_REL), verbatim(LEDGER_REL),
            verbatim(RECIPE_REL), verbatim(SPOT_REL), verbatim(LESSON_REL),
            verbatim(KNOWLEDGE_REL), verbatim(SOURCES_REL),
            {"path": QUALITY_REL, "source": f"mutation of {base}:{QUALITY_REL}",
             "sha256": sha256(files[QUALITY_REL]),
             "note": ("the round-62 substantive-support criterion sentence "
                      "wrapped in an HTML comment (MutC1Prose Q3x exact edit)")}]
    out.append(build_fixture(args.workdir, "A3-hidden-criterion", files, prov))

    # ---- A4 tamper -------------------------------------------------------
    spot_s = spot.decode("utf-8")
    assert spot_s.count("Disagree") >= 1
    spot_a4 = spot_s.replace("Disagree", "Agree", 1)
    files = dict(ev)
    files[SPOT_REL] = spot_a4.encode("utf-8")
    files[LESSON_REL] = lesson
    files[QUALITY_REL] = quality
    files[KNOWLEDGE_REL] = knowledge
    files[SOURCES_REL] = sources
    prov = [verbatim(RAW_REL), verbatim(TEXT_REL), verbatim(LEDGER_REL),
            verbatim(RECIPE_REL), verbatim(LESSON_REL), verbatim(QUALITY_REL),
            verbatim(KNOWLEDGE_REL), verbatim(SOURCES_REL),
            {"path": SPOT_REL, "source": f"mutation of {base}:{SPOT_REL}",
             "sha256": sha256(files[SPOT_REL]),
             "note": ("the S432 row's first Disagree flipped to Agree "
                      "(ScoutSpotSpan fxB shape)")}]
    out.append(build_fixture(args.workdir, "A4-tamper", files, prov))

    # ---- donothing-c1-copied --------------------------------------------
    files = dict(ev)
    files[SPOT_REL] = spot
    files[LESSON_REL] = lesson
    files[QUALITY_REL] = quality
    files[KNOWLEDGE_REL] = knowledge
    prov = [verbatim(RAW_REL), verbatim(TEXT_REL), verbatim(LEDGER_REL),
            verbatim(RECIPE_REL),
            {"path": SPOT_REL, "source": f"copied bytes of {base}:{SPOT_REL}",
             "sha256": sha256(spot), "note": "copied genuine bytes"},
            {"path": LESSON_REL, "source": f"copied bytes of {base}:{LESSON_REL}",
             "sha256": sha256(lesson), "note": "copied genuine bytes"},
            {"path": QUALITY_REL, "source": f"copied bytes of {base}:{QUALITY_REL}",
             "sha256": sha256(quality), "note": "copied genuine bytes"},
            {"path": KNOWLEDGE_REL,
             "source": f"copied bytes of {base}:{KNOWLEDGE_REL}",
             "sha256": sha256(knowledge), "note": "copied genuine bytes",
             "context": "no SOURCES.md, no other lane files present"}]
    out.append(build_fixture(args.workdir, "donothing-c1-copied", files, prov))

    # ---- c2-drift ---------------------------------------------------------
    drift = bytearray(live)
    drift[-1] ^= 0x01
    files = {LIVE_REL: bytes(drift)}
    out.append(build_fixture(args.workdir, "c2-drift", files, [
        {"path": LIVE_REL, "source": f"mutation of {base}:{LIVE_REL}",
         "sha256": sha256(files[LIVE_REL]),
         "note": "exactly one byte flipped (final byte XOR 0x01)"}]))

    # ---- c2-wrongpin ------------------------------------------------------
    files = {LIVE_REL: live}
    out.append(build_fixture(args.workdir, "c2-wrongpin", files, [
        {"path": LIVE_REL, "source": f"verbatim {base}:{LIVE_REL}",
         "sha256": sha256(live), "note": "byte-equal to lane blob"}]))

    for row in out:
        print(json.dumps(row))
    return 0


if __name__ == "__main__":
    sys.exit(main())
