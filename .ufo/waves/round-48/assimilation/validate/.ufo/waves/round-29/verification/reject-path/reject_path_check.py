#!/usr/bin/env python3
"""Reject-path check for the round-29 source gate.

Reads committed bytes (registry, lesson, entry) and checks that each
candidate rejected this round is recorded as a checkable rejection:

  q  the quote the lesson carries for the candidate is an exact substring of
     that candidate's own retained visible text and has at most 25 words
  f  the registry row's teaches cell opens "REJECTED:" and names a flip
     condition ("flip:")
  g  every primary id the teaches cell cites is a tier-A mined row that has
     retained visible text, so the contradiction rests on an openable source
  n  the candidate is not admitted: its URL appears in neither the entry body
     nor an admitting Gate line ("- S0NN - " for a mined id)

Exit 0 when every rejected row passes every check; 1 otherwise; 2 on unusable
input.
"""
import argparse, json, pathlib, re, sys

def collapse(s):
    return re.sub(r"\s+", " ", s).strip()

def registry_rows(text):
    out = {}
    for line in text.splitlines():
        m = re.match(r"^\|\s*(S\d{3,})\s*\|", line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 11:
            out[cells[0]] = cells
    return out

def lesson_bullets(text):
    """Screening bullets: '- S044 (C1) - url - ... **rejected**: ... quote "..."'"""
    out = {}
    for line in text.splitlines():
        m = re.match(r"^-\s+(S\d{3,})\s+\(C(\d)\)\s+—\s+(\S+)\s+—(.*)$", line)
        if not m:
            continue
        sid, cid, url, rest = m.groups()
        out[sid] = {"cid": cid, "url": url,
                    "quotes": re.findall(r"“([^”]+)”", rest),
                    "rejected": "rejected" in rest.lower()}
    return out

def admitting_gate_lines(text):
    """Gate lines that admit a mined source: '- S040 - url - ...'."""
    if "## Gate" not in text:
        return []
    gate = text.split("## Gate", 1)[1].split("\n## ", 1)[0]
    return [l for l in gate.splitlines() if re.match(r"^-\s+S\d{3,}\s+—\s+https?://", l)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--lesson", required=True)
    ap.add_argument("--entry", required=True)
    ap.add_argument("--screened-dir", required=True)
    ap.add_argument("--primary-dir", required=True)
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    try:
        reg_text = pathlib.Path(a.registry).read_text(encoding="utf-8")
        les_text = pathlib.Path(a.lesson).read_text(encoding="utf-8")
        ent_text = pathlib.Path(a.entry).read_text(encoding="utf-8")
    except OSError as exc:
        print(json.dumps({"error": "input unusable", "detail": str(exc)}))
        return 2
    rows = registry_rows(reg_text)
    bullets = lesson_bullets(les_text)
    admitted = "\n".join(admitting_gate_lines(les_text))
    results = []
    for sid, b in sorted(bullets.items()):
        cells = rows.get(sid)
        if cells is None:
            results.append({"id": sid, "passed": False, "problems": ["no registry row"]})
            continue
        problems = []
        teaches = cells[6]
        if b["rejected"]:
            if cells[7] != "rejected":
                problems.append(f"registry status is {cells[7]!r}, not 'rejected'")
            if not teaches.startswith("REJECTED:"):
                problems.append("teaches does not open REJECTED:")
            if "flip:" not in teaches:
                problems.append("teaches names no flip condition")
        else:
            if cells[7] == "rejected":
                problems.append("registry rejects a candidate the lesson does not mark rejected")
            if teaches.startswith("REJECTED:"):
                problems.append("teaches opens REJECTED: for a candidate the lesson does not mark rejected")
        ctext = ""
        cpath = pathlib.Path(a.screened_dir) / f"C{b['cid']}.txt"
        if cpath.exists():
            ctext = collapse(cpath.read_text(encoding="utf-8"))
        else:
            problems.append(f"no retained text for candidate C{b['cid']}")
        if not b["quotes"]:
            problems.append("lesson carries no quote for the candidate")
        for q in b["quotes"]:
            if ctext and q not in ctext:
                problems.append(f"quote not an exact substring of the candidate text: {q!r}")
            if len(q.split()) > 25:
                problems.append(f"quote over 25 words: {q!r}")
        for pid in sorted(set(re.findall(r"\bS0\d{2}\b", teaches))) if b["rejected"] else []:
            pcells = rows.get(pid)
            if pcells is None:
                problems.append(f"cited primary {pid} has no registry row")
                continue
            if pcells[7] != "mined" or pcells[3] != "A":
                problems.append(f"cited primary {pid} is tier {pcells[3]} status {pcells[7]}, not tier A mined")
            if not (pathlib.Path(a.primary_dir) / f"{pid}.txt").exists():
                problems.append(f"cited primary {pid} has no retained visible text")
        if b["url"] and (b["url"] in ent_text or b["url"] in admitted):
            problems.append("rejected candidate URL appears in the entry or an admitting Gate line")
        results.append({"id": sid, "url": b["url"], "candidate": f"C{b['cid']}",
                        "quotes": b["quotes"], "passed": not problems, "problems": problems})
    rejected_rows = sum(1 for c in rows.values() if c[7] == "rejected")
    rejected_screened = sum(1 for sid, b in bullets.items()
                            if b["rejected"] and rows.get(sid) is not None and rows[sid][7] == "rejected")
    passed = sum(r["passed"] for r in results)
    out = {"check": "kake-r29-reject-path", "screenedCandidates": len(results),
           "rejectedRowsInRegistry": rejected_rows, "rejectedScreenedCandidates": rejected_screened,
           "passed": passed, "rows": results}
    print(json.dumps(out, indent=1, ensure_ascii=False))
    if a.out:
        pathlib.Path(a.out).write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    # Round-29 wave-2 MistakesRowsCheck: a screen with zero rejections must fail.
    return 0 if results and passed == len(results) and rejected_screened >= 1 else 1

if __name__ == "__main__":
    sys.exit(main())
