PARTIAL: complete static source handoff under the critic no-edit/no-runtime boundary and L1's materialization instruction; control, NOTE and tests were not written or executed. L1 must materialize the bytes below and run the checks.
Axes: operability (primary), freshness (loose lastmod syntax only); no sealed key, counter execution, reference implementation, or network access.
Source destination: /fast/scratch/hyaku/kake-r39a3w1/CtlEngineLenient/control.py; SHA256 56652e5de6c76be1142d7c385f5baa0b98036c8a3e51c0eb8902cd803b77f0c0 (UTF-8 fenced contents, final LF).
```python
import json,re,sys,xml.etree.ElementTree as ET; from pathlib import Path; from urllib.parse import urlsplit
NS="{http://www.sitemaps.org/schemas/sitemap/0.9}"; WS=" \t\r\n"; ISO=re.compile(r"[0-9]{4}[-0-9Ww]*(?:[Tt ][0-9:.,]+(?:[Zz]|[+-][0-9:]+)?)?")
class Tree(ET.TreeBuilder):
    def __init__(self): super().__init__(); self.doctype_seen=False
    def doctype(self,*args): self.doctype_seen=True
def absolute(value):
    try: parsed=urlsplit(value); return parsed.scheme.lower() in ("http","https") and bool(parsed.hostname)
    except ValueError: return False
def text(node): return "".join(node.itertext()).strip(WS)
def audit(data):
    def finding(code,entry=None): return {"code":code,"entry":entry}
    try: raw=data.decode("utf-8-sig")
    except UnicodeError: return [finding("encoding_invalid")]
    declaration=re.match(r"<\?xml[ \t\r\n][^?]*\?>",raw); encoding=re.search(r"\bencoding[ \t\r\n]*=[ \t\r\n]*([\x22\x27])(.*?)\1",declaration.group(0)) if declaration else None; tree=Tree()
    if encoding and encoding.group(2).lower()!="utf-8": return [finding("encoding_invalid")]
    try: root=ET.fromstring(raw,parser=ET.XMLParser(target=tree))
    except (ET.ParseError,ValueError): return [finding("xml_malformed")]
    if tree.doctype_seen: return [finding("doctype_present")]
    if root.tag not in (NS+"urlset",NS+"sitemapindex"): return [finding("root_invalid")]
    kind="url" if root.tag==NS+"urlset" else "sitemap"; entries=root.findall(NS+kind); out=[] if entries else [finding("no_entries")]; usable=[]
    if any(child.tag.startswith(NS) and child.tag!=NS+kind for child in root): out.append(finding("element_unexpected"))
    allowed=("loc","lastmod","changefreq","priority") if kind=="url" else ("loc","lastmod")
    for index,entry in enumerate(entries,1):
        fields={field:entry.findall(NS+field) for field in allowed}; locs=fields["loc"]
        if len(locs)!=1: out.append(finding("loc_missing" if not locs else "loc_repeated",index))
        else:
            try: usable.append(urlsplit(text(locs[0])))
            except ValueError: pass
        for field in allowed[1:]: out.extend([finding("field_repeated",index)] if len(fields[field])>1 else [])
        if any(child.tag.startswith(NS) and child.tag[len(NS):] not in allowed for child in entry): out.append(finding("element_unexpected",index))
        if len(fields["lastmod"])==1 and not ISO.fullmatch(text(fields["lastmod"][0])): out.append(finding("lastmod_invalid",index))
    return list({(item["code"],item["entry"]):item for item in out}.values())
def reject(value): raise ValueError(value)
def main(argv):
    if len(argv)!=3 or argv[1]!="--manifest": return 64
    try: manifest_path=Path(argv[2]); manifest=json.loads(manifest_path.read_text(encoding="utf-8"),parse_constant=reject); valid=isinstance(manifest,dict) and type(manifest.get("version")) is int and manifest["version"]==1 and isinstance(manifest.get("checks"),list) and bool(manifest["checks"])
    except (OSError,ValueError): valid=False
    if not valid: print(json.dumps({"version":1,"verdict":"could-not-evaluate","error":"input_invalid","checks":[]})); return 2
    checks=[]; seen=set()
    for item in manifest["checks"]:
        ident=item.get("id") if isinstance(item,dict) and isinstance(item.get("id"),str) else None; result={"id":ident,"error":None,"findings":[]}; valid=isinstance(item,dict) and all(isinstance(item.get(field),str) for field in ("id","file","sitemapUrl")) and ident not in seen and not Path(item["file"]).is_absolute() and ".." not in Path(item["file"]).parts and absolute(item["sitemapUrl"])
        if ident is not None: seen.add(ident)
        if not valid: result["error"]="check_invalid"
        else:
            try: result["findings"]=audit((manifest_path.parent/item["file"]).read_bytes())
            except (OSError,ValueError): result["error"]="file_unreadable"
        result["status"]="error" if result["error"] else "findings" if result["findings"] else "clean"; checks.append(result)
    code=2 if any(item["error"] for item in checks) else 1 if any(item["findings"] for item in checks) else 0; print(json.dumps({"version":1,"verdict":("clean","failed-policy","could-not-evaluate")[code],"checks":checks})); return code
if __name__=="__main__": sys.exit(main(sys.argv))
```
NOTE destination: /fast/scratch/hyaku/kake-r39a3w1/CtlEngineLenient/NOTE.md; SHA256 c944e615b15ffa9eed03de304677cc054bb085bf987312eaa72835c61ce80223; exactly one line plus LF: `Lenient crawler control: standard-library XML parsing, namespace/structure and manifest/verdict handling retained; locs accepted whenever urlsplit parses (parse failures silently dropped); priority/changefreq values, strict lastmod/calendar/TZD rules, URL absoluteness/length/scope, and file/entry limits deliberately skipped.`
Four fixture specifications for /fast/scratch/hyaku/kake-r39a3w1/CtlEngineLenient/t/ (NOT written): valid.json, malformed.json and lenient.json each contain {"version":1,"checks":[{"id":"x","file":"NAME.xml","sitemapUrl":"https://example.test/maps/sitemap.xml"}]} with NAME replaced by the matching basename; invalid.json contains {"version":true,"checks":[{}]}. valid.xml contains `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://example.test/maps/a</loc></url></urlset>`; malformed.xml contains `<urlset`; lenient.xml contains `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>ftp://elsewhere.test/a</loc><lastmod>2026-02-30T25:61</lastmod><changefreq>sometimes</changefreq><priority>2</priority></url></urlset>`.
Self-tests NOT RUN: `timeout 60s bash -c 'for n in valid malformed lenient invalid; do timeout 10s prlimit --as=4000000000 /usr/bin/python3 -B "$1/control.py" --manifest "$1/t/$n.json"; printf "fixture=%s exit=%s\n" "$n" "$?"; done' bash /fast/scratch/hyaku/kake-r39a3w1/CtlEngineLenient`; [INFERENCE] exits respectively 0/1/0/2, with clean / xml_malformed finding / clean / input_invalid. Sandbox/bubblewrap behavior remains untested.
Observed commands: `timeout 10s /usr/bin/python3 -B -c 'import sys, pathlib, resource, shutil; print(sys.version.split()[0]); print("sandbox_exists=" + str(pathlib.Path("/fast/scratch/hyaku/kake-r39a3w1/CtlEngineLenient").exists())); print("bwrap=" + str(shutil.which("bwrap"))); print("prlimit=" + str(shutil.which("prlimit")))'` exit 0 (Python 3.14.8, sandbox absent, /usr/bin/bwrap, /usr/bin/prlimit); `timeout 10s sha256sum` twice, exit 0 each, stdin respectively the exact source and NOTE bytes above. No installs/updates; no process left running.
Counterexample/evidence: c1-contract.md:60-86 requires loc_not_absolute, lastmod_invalid, changefreq_invalid and priority_invalid, all entry 1, for lenient.xml; [INFERENCE] this control returns clean. This intentional under-validation tradeoff loses operability, not a control implementation defect to repair into a strict validator. Smallest safe correction: L1 materializes/scores these exact bytes and preserves the collector-versus-auditor distinction; no counter discrimination or round verdict is claimed here.
