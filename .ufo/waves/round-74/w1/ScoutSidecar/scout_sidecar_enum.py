import json, os, re, hashlib, sys, collections

BASE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REV  = "ced2878a1e77f57afb4ee3baebf1021e5130399b"
SC   = "/fast/scratch/hyaku/kake-r74/ScoutSidecar"
HOME = os.environ["HOME"]

PATH_RE = re.compile(r"(?:~|/home/vgpnk)/[A-Za-z0-9._@%+{},*-]*(?:/[A-Za-z0-9._@%+{},*-]*)*")
ABSENT_RE = re.compile(r"absent|gone|vanished|emptied|no longer|dangling|no such file|never published|missing", re.I)

def expand_braces(tok, cap=64):
    out=[tok]
    for _ in range(6):
        nxt=[]; changed=False
        for t in out:
            m=re.search(r"\{([^{}]*)\}", t)
            if not m: nxt.append(t); continue
            body=m.group(1)
            rng=re.match(r"^\s*(-?\d+)\s*\.\.\s*(-?\d+)\s*$", body)
            if rng:
                a,b=int(rng.group(1)),int(rng.group(2)); step=1 if a<=b else -1
                alts=[str(v) for v in range(a, b+step, step)]
            else:
                alts=[re.sub(r"\s+","",s) for s in body.split(",")]
            if any(not re.match(r"^[A-Za-z0-9._@%+*/-]*$", x) for x in alts): nxt.append(t); continue
            changed=True
            for a in alts: nxt.append(t[:m.start()]+a+t[m.end():])
        out=nxt
        if not changed: break
        if len(out)>cap: return [tok]
    return out

def normalize(tok):
    t=tok
    while len(t)>1 and t[-1] in '.,;)*': t=t[:-1]
    while len(t)>1 and t.endswith('/'): t=t[:-1]
    res=[]
    for e in expand_braces(t):
        if '{' in e or '}' in e: continue
        res.append(e)
    return res

def canon_home(t):
    return "~"+t[len("/home/vgpnk"):] if t.startswith("/home/vgpnk/") else t

def line_tokens(line):
    toks=set()
    for m in PATH_RE.finditer(line):
        for nt in normalize(m.group(0)):
            toks.add(canon_home(nt))
    return toks

def git_show(path):
    import subprocess
    r=subprocess.run(["git","-C",BASE,"show",f"{REV}:{path}"],capture_output=True)
    if r.returncode!=0: return None
    return r.stdout  # bytes

def stat_token(tok):
    p = HOME + tok[1:] if tok.startswith("~/") else tok
    try:
        os.stat(p)
        return "present", None
    except FileNotFoundError:
        return "absent", "FileNotFoundError"
    except NotADirectoryError:
        return "absent", "NotADirectoryError"
    except OSError as e:
        return "unevaluable", f"{type(e).__name__}: {e.strerror}"

raw = open(f"{SC}/base-sidecar.json","rb").read()
data = json.loads(raw.decode("utf-8"))
entries = data["entries"]
print("schema:", data["schema"])
print("top-level keys:", list(data.keys()))
print("total entries:", len(entries))
kinds = collections.Counter(e["kind"] for e in entries)
print("kind counts:", dict(kinds))
print("field sets:", collections.Counter(tuple(e.keys()) for e in entries))
print("dates:", dict(collections.Counter(e["date"] for e in entries)))
print("entries with history field:", sum(1 for e in entries if "history" in e))

# per-entry stat + binding
cache={}
def file_lines(f):
    if f not in cache:
        b=git_show(f)
        cache[f]=(b, b.decode("utf-8").split("\n") if b is not None else None)
    return cache[f]

rows=[]
for i,e in enumerate(entries):
    state,why = stat_token(e["token"])
    b,lines = file_lines(e["file"])
    row={"i":i, **e, "state":state, "why":why}
    if lines is None:
        row["file_missing"]=True; row["sha_ok"]=None; row["tok_on_line"]=None; row["dup"]=None
    else:
        line = lines[e["line"]-1] if e["line"]-1 < len(lines) else None
        row["file_missing"]=False
        row["line_exists"]= line is not None
        row["sha_ok"] = (line is not None and hashlib.sha256(line.encode()).hexdigest()==e["lineSha256"])
        if line is None:
            row["tok_on_line"]=False; row["dup"]=None
        else:
            toks=line_tokens(line)
            row["tok_on_line"] = e["token"] in toks
            # duplicate token occurrences on the same cited line
            occ=0
            for m in PATH_RE.finditer(line):
                if any(canon_home(nt)==e["token"] for nt in normalize(m.group(0))): occ+=1
            row["dup"]=occ
            row["line_text"]=line
    rows.append(row)

def agg(kind):
    c=collections.Counter(r["state"] for r in rows if r["kind"]==kind)
    return c
print()
print("STAT SUMMARY")
for k in ("absent","restored"):
    c=agg(k); print(f"  {k}: total={sum(c.values())} " + " ".join(f"{s}={c[s]}" for s in ("present","absent","unevaluable")))
# matrix
mat=collections.Counter((r["kind"],r["state"]) for r in rows)
print("  matrix:", dict(mat))
contradictions=[r for r in rows if (r["kind"]=="absent" and r["state"]=="present")]
print("  contradictions(kind=absent,state=present):", len(contradictions))

# disagreements
print()
print("DISAGREEMENTS (kind vs host state):")
for r in rows:
    if (r["kind"]=="absent" and r["state"]!="absent") or (r["kind"]=="restored" and r["state"]!="present"):
        print(f"  {r['file']}:{r['line']} {r['token']} kind={r['kind']} state={r['state']}")
print("  count:", sum(1 for r in rows if (r["kind"]=="absent" and r["state"]!="absent") or (r["kind"]=="restored" and r["state"]!="present")))

# genuinely absent
ga=[r for r in rows if r["kind"]=="absent" and r["state"]=="absent"]
print()
print("GENUINELY ABSENT (kind=absent, state=absent):", len(ga))
for r in ga:
    print(f"  file={r['file']} line={r['line']} token={r['token']} why={r['why']}")
    print(f"    note={r['note']}")
print("  distinct tokens:", sorted({r["token"] for r in ga}), "n=",len({r["token"] for r in ga}))

# binding integrity
print()
print("BINDING (sha256 / token-on-line / duplicate occurrences):")
bad_sha=[r for r in rows if r["sha_ok"] is False]
bad_tok=[r for r in rows if r["tok_on_line"] is False]
dup=[r for r in rows if r["dup"] and r["dup"]>1]
print("  sha256 mismatch:", len(bad_sha))
for r in bad_sha: print(f"    {r['file']}:{r['line']} {r['token']} kind={r['kind']} state={r['state']}")
print("  token not found on cited line (PATH_RE-normalized):", len(bad_tok))
for r in bad_tok[:20]: print(f"    {r['file']}:{r['line']} {r['token']}")
print("  cited line carries token >1 time:", len(dup))
for r in dup: print(f"    {r['file']}:{r['line']} {r['token']} occurrences={r['dup']}")
print("  missing files:", sum(1 for r in rows if r["file_missing"]))

# restored entries detail
print()
print("RESTORED ENTRIES:", sum(1 for r in rows if r["kind"]=="restored"))
for r in rows:
    if r["kind"]=="restored":
        dated = re.search(r"\d{4}-\d{2}-\d{2}", r["note"])
        print(f"  {r['file']}:{r['line']} {r['token']} state={r['state']} date={r['date']} note_has_date={bool(dated)} sha_ok={r['sha_ok']} dup={r['dup']} note_len={len(r['note'])}")

# notes vocabulary
print()
print("ABSENCE VOCAB in notes by kind:")
for k in ("absent","restored"):
    hits=[r for r in rows if r["kind"]==k and ABSENT_RE.search(r["note"])]
    print(f"  kind={k}: notes matching ABSENT_RE={len(hits)}/{sum(1 for r in rows if r['kind']==k)}")
print("  restored notes matching ABSENT_RE:", [f"{r['file']}:{r['line']}" for r in rows if r["kind"]=="restored" and ABSENT_RE.search(r["note"])])

# note template uniformity
print()
print("NOTE PREFIX TEMPLATE (first 40 chars) counts:")
print(collections.Counter(r["note"][:60] for r in rows).most_common(6))
print()
print("has 'historical record, not an executable instruction':", sum(1 for r in rows if "historical record, not an executable instruction" in r["note"]), "/", len(rows))
