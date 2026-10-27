import importlib.util, hashlib, os, re, sys
W="/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58"
spec=importlib.util.spec_from_file_location("qt", os.path.join(W,"c58_quote_truth.py"))
qt=importlib.util.module_from_spec(spec); spec.loader.exec_module(qt)
report=open("/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/w1/ScribeRegistryGate.md",encoding="utf-8").read()
gate=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"gate.md"),encoding="utf-8").read()
rowtext="## Registry\n"+"\n".join(l for l in report.splitlines() if re.match(r"^\| S42[34] ", l))
rows=qt.parse_registry(rowtext)
print("parsed ids:", sorted(rows))
bodies={}
for sid in ("S423","S424"):
    bodies[sid]=open(os.path.join(W,"sources",f"{sid}.html"),"rb").read()
notes=[]
for sid in ("S423","S424"):
    row=rows.get(sid)
    if row is None: notes.append(f"{sid}: no row"); continue
    if len(row)!=11: notes.append(f"{sid}: {len(row)} cells")
    if row[7]!="mined": notes.append(f"{sid}: status {row[7]}")
    if row[8]!=qt.ROUND_DATE: notes.append(f"{sid}: opened {row[8]}")
    if not re.fullmatch(r"(\d{4}-\d{2}-\d{2}|\d+d|on-release)", row[9]): notes.append(f"{sid}: recheck {row[9]}")
    if row[2] not in qt.ROW_KINDS or row[3] not in ("A","B","C"): notes.append(f"{sid}: kind/tier")
    if len(row[4])<20 or len(row[6])<20: notes.append(f"{sid}: short scope/teaches")
    if qt.row_url(row)!=qt.ROW_URL[sid]: notes.append(f"{sid}: row_url {qt.row_url(row)}")
    text=bodies[sid].decode("utf-8")
    if hashlib.sha256(bodies[sid]).hexdigest()!=qt.BODY_SHA256.get(sid): notes.append(f"{sid}: body digest != frozen")
    title=" — ".join(row[1].split(" — ")[1:-1]); page_title=(re.search(r"<title>([^<]*)</title>",text) or [None,""])[1].split("_")[0]
    if title!=page_title or qt.units(title)<6: notes.append(f"{sid}: title {title!r} != {page_title!r}")
    am=re.match(r"^§\s*(.*?)\s*\(发布日期[：: ]\s*\d{4}-\d{2}-\d{2}\)\s*$", row[5])
    if not am: notes.append(f"{sid}: anchor form {row[5][:40]!r}")
    else:
        anchor=am.group(1)
        if qt.units(anchor)<4 or text.count(anchor)!=1 or not qt.in_content(text,anchor,sid):
            notes.append(f"{sid}: anchor not 4+units/unique/in-node")
    pub=re.search(r"发布日期[：: ]\s*(\d{4}-\d{2}-\d{2})", row[5])
    if not pub or not qt.in_content(text,f"发布日期：{pub.group(1)}",sid): notes.append(f"{sid}: printed date")
    line=qt.gate_line(gate,sid)
    if line is None: notes.append(f"{sid}: no gate line"); continue
    if qt.CURLY.search(line): notes.append(f"{sid}: curly quotes in gate line")
    allq=re.findall(r'"([^"]+)"',line); spans=[q for q in allq if qt.units(q)>=6]
    if not any(qt.TOPIC in q for q in spans): notes.append(f"{sid}: no quote carries {qt.TOPIC}")
    if hashlib.sha256(bodies[sid]).hexdigest() not in line: notes.append(f"{sid}: digest absent")
    if f"{len(bodies[sid])} bytes" not in line: notes.append(f"{sid}: bytes absent")
    for q in spans:
        if f"{qt.units(q)} units" not in line: notes.append(f"{sid}: units label for {q[:12]}")
        if not 6<=qt.units(q)<=25: notes.append(f"{sid}: quote units {qt.units(q)}")
    if row[5] not in line: notes.append(f"{sid}: gate line lacks anchor cell")
    for q in allq:
        if qt.units(q)>25 or len(q)>40: notes.append(f"{sid}: ceiling {q[:12]}")
        if q not in text: notes.append(f"{sid}: not substring {q[:12]}")
        elif not qt.in_content(text,q,sid): notes.append(f"{sid}: outside block {q[:12]}")
    other=bodies["S424" if sid=="S423" else "S423"].decode("utf-8")
    for q in spans:
        if text.count(q)!=1 or q in other: notes.append(f"{sid}: not page-unique {q[:12]}")
    if qt.ROW_URL[sid] not in line: notes.append(f"{sid}: url absent")
    if qt.ROUND_DATE not in line: notes.append(f"{sid}: date absent")
print("NOTES:", len(notes))
for n in notes: print(" -", n)
