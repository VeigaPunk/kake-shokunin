#!/usr/bin/env python3
"""ScoutRecon: base tool vs amendment-1-predicted tool over frozen + probe + round-80 cases."""
import json
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
HERE = Path("/fast/scratch/hyaku/kake-r80/ScoutRecon")
BASE_REV = "9998dc7a586b9fe76379014c8123aa3606f2d8b9"

# ---------------------------------------------------------------- patch
ASCTIME_ANCHOR = """RFC850_RE = re.compile(
    r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), [0-9]{2}-"
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-[0-9]{2} "
    r"[0-9]{2}:[0-9]{2}:[0-9]{2} GMT$")
"""
ASCTIME_ADD = ASCTIME_ANCHOR + '''ASCTIME_RE = re.compile(
    r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun) "
    r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
    r" {1,2}[0-9]{1,2} [0-9]{2}:[0-9]{2}:[0-9]{2} [0-9]{4}$")
WEEKDAY_TOKENS = {
    "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun",
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
}
'''

VALUE_LINE = '''    if value is None or not (ISO_RE.match(value) or RFC822_RE.match(value) or RFC850_RE.match(value)):'''
VALUE_NEW = '''    if value is None or not (ISO_RE.match(value) or RFC822_RE.match(value)
                             or RFC850_RE.match(value) or ASCTIME_RE.match(value)):'''

SPLIT_LINE = '''    for raw in value.split(","):'''
SPLIT_NEW = '''    for raw in _segments(value):'''

HELPER_ANCHOR = '''def parse_field(value: str, findings: set[str]) -> tuple[list[str], dict[str, list[str]]]:'''
HELPER_ADD = '''def _opens_weekday_date(segment: str) -> bool:
    """True iff this segment is `[bot:] unavailable_after` carrying only a weekday token."""
    head, sep, rest = segment.strip().partition(":")
    if sep and BOT_RE.match(head.strip()) and head.strip().lower() not in KNOWN:
        head, sep, rest = rest.partition(":")
    return bool(sep) and head.strip().lower() == "unavailable_after" and rest.strip() in WEEKDAY_TOKENS


def _segments(value: str) -> list[str]:
    """Split on ASCII comma, keeping the comma that follows a leading weekday token."""
    parts = value.split(",")
    out: list[str] = []
    index = 0
    while index < len(parts):
        raw = parts[index]
        if index + 1 < len(parts) and _opens_weekday_date(raw):
            out.append(raw + "," + parts[index + 1])
            index += 2
        else:
            out.append(raw)
            index += 1
    return out


''' + HELPER_ANCHOR


def patched_source(base: str) -> str:
    for old, new in ((ASCTIME_ANCHOR, ASCTIME_ADD), (VALUE_LINE, VALUE_NEW),
                     (SPLIT_LINE, SPLIT_NEW), (HELPER_ANCHOR, HELPER_ADD)):
        assert base.count(old) == 1, ("anchor not unique", old[:60])
        base = base.replace(old, new)
    return base


# ---------------------------------------------------------------- run
def run(tool: Path, manifest: Path) -> tuple[int, str, str]:
    p = subprocess.run([sys.executable, "-B", str(tool), "--manifest", str(manifest), "--json"],
                       capture_output=True, text=True, timeout=120)
    return p.returncode, p.stdout, p.stderr


def norm(rc: int, out: str) -> str:
    try:
        doc = json.loads(out)
    except json.JSONDecodeError:
        return f"UNPARSEABLE exit={rc} out={out!r}"
    return f"exit={rc} " + json.dumps(doc, sort_keys=True)


def main() -> int:
    base_src = subprocess.run(
        ["git", "-C", str(LANE), "show", f"{BASE_REV}:scripts/x_robots_tag_audit.py"],
        capture_output=True, text=True, check=True).stdout
    (HERE / "tool_base.py").write_text(base_src)
    (HERE / "tool_patched.py").write_text(patched_source(base_src))
    base_tool, new_tool = HERE / "tool_base.py", HERE / "tool_patched.py"

    print("== selftest ==")
    for name, tool in (("base", base_tool), ("patched", new_tool)):
        p = subprocess.run([sys.executable, "-B", str(tool), "--selftest"],
                           capture_output=True, text=True)
        print(f"{name}: {p.stdout.strip()} exit={p.returncode}")

    # frozen 31
    frozen = sorted((LANE / ".ufo/waves/round-79/cases").glob("c*/manifest.json"))
    print(f"\n== frozen round-79 set ({len(frozen)}) ==")
    diffs = 0
    for m in frozen:
        rb, ob, _ = run(base_tool, m)
        rn, on, _ = run(new_tool, m)
        same = norm(rb, ob) == norm(rn, on)
        if not same:
            diffs += 1
            print(f"DIFF {m.parent.name}\n  base: {norm(rb, ob)[:300]}\n  new : {norm(rn, on)[:300]}")
    print(f"frozen_identical={len(frozen)-diffs}/{len(frozen)} diffs={diffs}")

    # probes
    probes = sorted((HERE / "probes").glob("*.json"))
    print(f"\n== probes ({len(probes)}) ==")
    for m in probes:
        rb, ob, _ = run(base_tool, m)
        rn, on, _ = run(new_tool, m)
        db = json.loads(ob) if ob.strip().startswith("{") else {"raw": ob}
        dn = json.loads(on) if on.strip().startswith("{") else {"raw": on}
        print(f"\n-- {m.stem}")
        for line in json.dumps(db, indent=None, sort_keys=True).splitlines():
            print(f"   base[{rb}] {line[:400]}")
        for line in json.dumps(dn, indent=None, sort_keys=True).splitlines():
            print(f"   new [{rn}] {line[:400]}")

    # round-80 set vs oracle
    expect = json.loads((LANE / ".ufo/waves/round-80/expect/expect.json").read_text())
    cases = sorted((LANE / ".ufo/waves/round-80/cases").glob("c*/manifest.json"))
    print(f"\n== round-80 set under predicted patch ({len(cases)}) ==")
    ok = 0
    for m in cases:
        rc, out, _ = run(new_tool, m)
        cid = m.parent.name
        exp = expect["cases"][cid]
        try:
            rep = json.loads(out)
        except json.JSONDecodeError:
            print(f"  {cid}: UNPARSEABLE")
            continue
        got = rep.get("checks", [{}])[0]
        good = (rc == exp["exit"]
                and sorted(rep.get("findings") or []) == exp["findings"]
                and sorted(got.get("directives") or []) == sorted(
                    exp["checks"][cid]["directives"])
                and sorted(got.get("effective") or []) == sorted(
                    exp["checks"][cid]["effective"])
                and {k: sorted(v) for k, v in (got.get("bots") or {}).items()}
                == exp["checks"][cid]["bots"])
        ok += good
        if not good:
            print(f"  WRONG {cid}: exit={rc} findings={rep.get('findings')} "
                  f"directives={got.get('directives')} exp={exp}")
    print(f"a2_predicted_correct={ok}/{len(cases)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
