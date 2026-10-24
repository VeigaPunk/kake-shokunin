#!/usr/bin/env python3
"""Run the round-37 selftest against single-point mutants of the independent implementation.

Each mutant is one edit that breaks the contract sentence the round-37 control mutation pass
(`.ufo/waves/round-37/ctl/MutRefPass.md`) lists. A mutant is killed when the selftest does not
pass every fixture. Mirrors the mutant table's one-line diffs onto this implementation.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "independent_robots_audit.py"
SELFTEST = HERE / "robots_audit_selftest.py"
OUT = HERE / "mutants"

MUTANTS = [
    ("M01", "LIMIT 512000 -> 511999", [('ROBOTS_LIMIT = 512000', 'ROBOTS_LIMIT = 511999')]),
    ("M02", "LIMIT 512000 -> 512001", [('ROBOTS_LIMIT = 512000', 'ROBOTS_LIMIT = 512001')]),
    ("M03", "key SP/TAB trim -> strip()",
     [('key = ascii_lower(trim(line[:colon]))', 'key = ascii_lower(line[:colon].strip())')]),
    ("M04", "value SP/TAB trim -> strip()",
     [('value = trim(line[colon + 1:])', 'value = line[colon + 1:].strip()')]),
    ("M05", "first # -> rfind(#)",
     [('cut = line.find("#")', 'cut = line.rfind("#")')]),
    ("M06", "CR/LF split -> splitlines()",
     [('for line in _LINE_END.split(text):', 'for line in text.splitlines():')]),
    ("M07", "first colon -> last colon",
     [('colon = line.find(":")', 'colon = line.rfind(":")')]),
    ("M08", "ASCII key lower -> casefold",
     [('key = ascii_lower(trim(line[:colon]))', 'key = trim(line[:colon]).casefold()')]),
    ("M09", "ASCII agent compare -> casefold",
     [('if any(ascii_lower(name) == wanted for name in group["names"])]',
       'if any(name.casefold() == wanted for name in group["names"])]')]),
    ("M10", "agent equality -> substring",
     [('if any(ascii_lower(name) == wanted for name in group["names"])]',
       'if any(wanted in ascii_lower(name) for name in group["names"])]')]),
    ("M11", "wildcard fallback inverted", [('    if not matching:\n', '    if matching:\n')]),
    ("M12", "combine groups -> last group only",
     [('    matching = [group for group in groups\n                    if any(name == "*" for name in group["names"])]\n',
       '    matching = [group for group in groups\n                    if any(name == "*" for name in group["names"])]\n    matching = matching[-1:]\n')]),
    ("M13", "agent after rule starts group -> always new group",
     [('if not groups or not previous_was_agent:', 'if True:')]),
    ("M14", "consecutive agents share group -> never",
     [('if not groups or not previous_was_agent:', 'if not groups:')]),
    ("M15", "wildcard .* -> .+", [('".*".join(re.escape(piece)', '".+".join(re.escape(piece)')]),
    ("M16", "anchor endswith($) -> startswith($)",
     [('anchored = rule.endswith("$")', 'anchored = rule.startswith("$")')]),
    ("M17", "prefix re.match -> re.fullmatch",
     [('return re.match(pattern, path, re.DOTALL) is not None',
       'return re.fullmatch(pattern, path, re.DOTALL) is not None')]),
    ("M18", "prefix re.match -> re.search",
     [('return re.match(pattern, path, re.DOTALL) is not None',
       'return re.search(pattern, path, re.DOTALL) is not None')]),
    ("M19", "normalized length -> raw length",
     [('length = len(normalized)', 'length = len(value)')]),
    ("M20", "longest tie: > -> >=",
     [('if length > best_length or (length == best_length and kind == "allow"):',
       'if length >= best_length or (length == best_length and kind == "allow"):')]),
    ("M21", "tie kind allow -> disallow",
     [('(length == best_length and kind == "allow")',
       '(length == best_length and kind == "disallow")')]),
    ("M22", "decode unreserved -> also %2F",
     [('if char in _UNRESERVED:', 'if char in _UNRESERVED or char == "/":')]),
    ("M23", "kept escape hex upper -> lower",
     [('return "%" + match.group(1).upper()', 'return "%" + match.group(1).lower()')]),
    ("M24", "UTF-8 escape hex %02X -> %02x",
     [('out.extend("%%%02X" % byte', 'out.extend("%%%02x" % byte')]),
    ("M25", "empty path default / -> empty",
     [('path = parts.path or "/"', 'path = parts.path')]),
    ("M26", "append ?query -> append empty",
     [('path = path + "?" + parts.query', 'path = path + "?"')]),
    ("M27", "fragment included",
     [('path = parts.path or "/"',
       'path = (parts.path or "/") + ("#" + parts.fragment if parts.fragment else "")')]),
    ("M28", "robots.txt comparison case-insensitive",
     [('if path == "/robots.txt":', 'if path.lower() == "/robots.txt":')]),
    ("M29", "version exact int -> isinstance",
     [('if type(version) is not int or version != 1:', 'if not isinstance(version, int) or version != 1:')]),
    ("M30", "product token anchored -> prefix match",
     [('_PRODUCT_TOKEN = re.compile(r"[A-Za-z_-]+\\Z")',
       '_PRODUCT_TOKEN = re.compile(r"[A-Za-z_-]+")'),
      ('_PRODUCT_TOKEN.fullmatch(agent)', '_PRODUCT_TOKEN.match(agent)')]),
    ("M31", "product token alphabet adds digits",
     [('_PRODUCT_TOKEN = re.compile(r"[A-Za-z_-]+\\Z")',
       '_PRODUCT_TOKEN = re.compile(r"[A-Za-z0-9_-]+\\Z")')]),
    ("M32", "status 300 accepted",
     [('if not (200 <= status <= 299 or 400 <= status <= 499 or 500 <= status <= 599):',
       'if not (200 <= status <= 299 or status == 300 or 400 <= status <= 499 or 500 <= status <= 599):')]),
    ("M33", "status 399 accepted",
     [('if not (200 <= status <= 299 or 400 <= status <= 499 or 500 <= status <= 599):',
       'if not (200 <= status <= 299 or 400 <= status <= 499 or status == 399 or 500 <= status <= 599):')]),
    ("M34", "status accepts floats",
     [('if type(status) is not int:', 'if not isinstance(status, (int, float)):')]),
    ("M35", "status lower bound 200 -> 201",
     [('if not (200 <= status <= 299 or 400 <= status <= 499 or 500 <= status <= 599):',
       'if not (201 <= status <= 299 or 400 <= status <= 499 or 500 <= status <= 599):')]),
    ("M36", "status upper bound 599 -> 598",
     [('if not (200 <= status <= 299 or 400 <= status <= 499 or 500 <= status <= 599):',
       'if not (200 <= status <= 299 or 400 <= status <= 499 or 500 <= status <= 598):')]),
    ("M37", "realpath -> abspath for containment",
     [('resolved = os.path.realpath(os.path.join(manifest_dir, robots))',
       'resolved = os.path.abspath(os.path.join(manifest_dir, robots))')]),
    ("M38", "containment prefix drops separator",
     [('if not resolved.startswith(manifest_dir + os.sep):',
       'if not resolved.startswith(manifest_dir):')]),
    ("M39", "manifest max 64 MiB -> 64 MiB - 1",
     [('if info.st_size > MANIFEST_LIMIT:', 'if info.st_size >= MANIFEST_LIMIT:')]),
    ("M40", "manifest UTF-8 strict -> replacement",
     [('text = data.decode("utf-8")', 'text = data.decode("utf-8", "replace")')]),
    ("M41", "checksEvaluated increment 1 -> 2", [('evaluated += 1', 'evaluated += 2')]),
    ("M42", "report version 1 -> 2", [('"version": 1,', '"version": 2,')]),
]


def main():
    OUT.mkdir(exist_ok=True)
    source = SOURCE.read_text()
    env = dict(os.environ)
    env["TMPDIR"] = str(HERE / "tmp")
    results = []
    for mutant_id, sentence, edits in MUTANTS:
        text = source
        for old, new in edits:
            if text.count(old) != 1:
                results.append({"id": mutant_id, "status": "locator-failed",
                                "sentence": sentence, "count": text.count(old)})
                text = None
                break
            text = text.replace(old, new)
        if text is None:
            continue
        target = OUT / ("%s.py" % mutant_id)
        target.write_text(text)
        proc = subprocess.run(
            [sys.executable, "-B", str(SELFTEST), "--tool", str(target)],
            cwd=str(HERE), capture_output=True, text=True, timeout=900, env=env,
        )
        summary = None
        try:
            summary = json.loads(proc.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            pass
        results.append({
            "id": mutant_id,
            "sentence": sentence,
            "exit": proc.returncode,
            "passedOverTotal": summary.get("passedOverTotal") if summary else None,
            "verdict": summary.get("verdict") if summary else None,
            "killed": proc.returncode != 0,
            "firstFailures": [item["case"] for item in (summary or {}).get("failures", [])][:6],
        })
        print(json.dumps(results[-1], sort_keys=True), flush=True)
        target.unlink()
    (HERE / "mutation-summary.json").write_text(json.dumps(results, indent=2, sort_keys=True))
    killed = sum(1 for item in results if item.get("killed"))
    print("KILLED %d/%d" % (killed, len(results)))


if __name__ == "__main__":
    main()
