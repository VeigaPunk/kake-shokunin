#!/usr/bin/env python3
"""MutC1: build single-conjunct mutants of the frozen C1 counter c90_defects.py.

Each mutant is one exact textual replacement that must match exactly once in the
frozen bytes (sha256 462224f6...). Output: mutants/<id>.py plus mutants/manifest.tsv.
"""
import hashlib, os, sys

SRC = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-90/c90_defects.py"
FROZEN = "462224f630d4369138af1bf38783b16695b712b85bb46b7b9d2d3c35f05d519b"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mutants")

M = [
 ("M01", "D2 drop base-prefix (append-only) check",
  "        if not cur.startswith(base):\n",
  "        if False:\n"),
 ("M02", "D2 drop frozen c89 re-run",
  "            if got != (n_open, n_closed):\n",
  "            if False:\n"),
 ("M03", "D2 drop receipt first-line agreement check",
  "            if (\"revision=%s\" % hexrev) not in first or (\"open=%d closed=%d\" % (n_open, n_closed)) not in first:\n",
  "            if False:\n"),
 ("M04", "D3 drop S463 byte-identity check",
  "    if c.get(\"S463\") != b.get(\"S463\"):\n",
  "    if False:\n"),
 ("M05", "D3 drop quote-in-retained-body check",
  "            if 3 <= n <= 25 and norm(q) in nbody:\n",
  "            if 3 <= n <= 25:\n"),
 ("M06", "D3 accept any 'supersedes' wording (substring S463 anywhere in teaches)",
  "cs[6].startswith(\"supersedes S463 —\")",
  "(\"S463\" in cs[6])"),
 ("M07", "D1 drop live untracked lane-root check",
  "        if \"/\" not in path or (path.endswith(\"/\") and path.count(\"/\") == 1):\n",
  "        if False:\n"),
 ("M08", "D1 drop relocated-copy sha check",
  "    elif hashlib.sha256(data).hexdigest() != INHERITED_SHA:\n",
  "    elif False:\n"),
 ("M09", "D2 accept either SCORECARD or LOG (one verified file suffices)",
  "    return why\n\n\ndef cells(line):",
  "    return [] if len(why) < 2 else why\n\n\ndef cells(line):"),
 ("M10", "D1 drop 'baseclean.out not tracked at lane root' check",
  "    if tracked(root, rev, \"baseclean.out\"):\n",
  "    if False:\n"),
 ("M11", "D3 drop rfc9111 URL in source cell",
  " and \"rfc9111\" in cs[1].lower()", ""),
 ("M12", "D3 drop status == mined",
  " and cs[7] == \"mined\"", ""),
 ("M13", "D3 drop new-row scope excludes 'not cache-key construction'",
  "\n                    and \"not cache-key construction\" not in cs[4]", ""),
 ("M14", "D3 drop retained RFC body digest check",
  "    if body is None or hashlib.sha256(body).hexdigest() != RFC9111_SHA:\n",
  "    if body is None:\n"),
 ("M15", "D3 drop quote word-count bounds 3..25",
  "            if 3 <= n <= 25 and norm(q) in nbody:\n",
  "            if norm(q) in nbody:\n"),
 ("M16", "D3 drop ## Gate section restriction (whole lesson)",
  "    gate = m.group(1) if m else \"\"\n",
  "    gate = text\n"),
 ("M17", "D3 drop row-id naming on the quote line",
  "        if not any(re.search(r\"\\b%s\\b\" % s, line) for s in sup):\n",
  "        if False:\n"),
 ("M19", "D2 drop receipt-tracked requirement (untracked receipt skips first-line check)",
  "            if data is None:\n                notes.append(\"receipt %s not tracked\" % rec.group(1))\n                continue\n            first = data",
  "            if data is None:\n                data = (\"revision=%s open=%d closed=%d\" % (hexrev, n_open, n_closed)).encode()\n            first = data"),
 ("M20", "D2 reading = first open/closed on whole line (pre-freeze v0 parse)",
  "            ocs = OC_RE.findall(line.split(\"f62e7954\", 1)[1])",
  "            ocs = OC_RE.findall(line)[:1]"),
 ("M21", "D3 drop 'new row' requirement (an existing row may supersede)",
  "        if sid in b:\n            continue\n        for line in lines:",
  "        for line in lines:"),
 ("M22", "D1 live check counts only root files, not root directories",
  "        if \"/\" not in path or (path.endswith(\"/\") and path.count(\"/\") == 1):\n",
  "        if \"/\" not in path:\n"),
 ("M18", "D2 drop f62e7954 requirement on the correction line (reading after f62e7954 if present, else whole line)",
  "            if not CORR_RE.search(line) or \"f62e7954\" not in line:\n                continue\n            rec = REC_RE.search(line)\n            hx = [h for h in HEX_RE.findall(line) if not h.startswith(\"f62e7954\")] or HEX_RE.findall(line)\n            ocs = OC_RE.findall(line.split(\"f62e7954\", 1)[1])",
  "            if not CORR_RE.search(line):\n                continue\n            rec = REC_RE.search(line)\n            hx = [h for h in HEX_RE.findall(line) if not h.startswith(\"f62e7954\")] or HEX_RE.findall(line)\n            ocs = OC_RE.findall(line.split(\"f62e7954\", 1)[-1])"),
]

def main():
    src = open(SRC, "rb").read()
    h = hashlib.sha256(src).hexdigest()
    if h != FROZEN:
        sys.exit("frozen counter sha mismatch: %s" % h)
    s = src.decode()
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "manifest.tsv"), "w") as mf:
        mf.write("id\tsha256\tdescription\n")
        for mid, desc, a, b in M:
            n = s.count(a)
            if n != 1:
                sys.exit("%s: anchor matches %d times" % (mid, n))
            t = s.replace(a, b, 1).encode()
            p = os.path.join(OUT, mid + ".py")
            open(p, "wb").write(t)
            mf.write("%s\t%s\t%s\n" % (mid, hashlib.sha256(t).hexdigest(), desc))
    print("built %d mutants from %s" % (len(M), h))

main()
