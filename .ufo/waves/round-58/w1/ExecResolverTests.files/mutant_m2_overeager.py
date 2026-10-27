# junk control M2: correct -z paths + over-eager fence toggle (any indent, any char, any length)
import importlib.util, re, sys
spec = importlib.util.spec_from_file_location("ref", "/fast/scratch/hyaku/kake-r58/ExecResolverTests/ref_id_resolver.py")
ref = importlib.util.module_from_spec(spec); spec.loader.exec_module(ref)
TOGGLE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
def parse_registry(text):
    rows, inside, fence = {}, False, False
    for raw in text.splitlines():
        line = raw.rstrip("\r")
        if TOGGLE_RE.match(line):
            fence = not fence
            continue
        if fence:
            continue
        if ref.REGISTRY_HEADING_RE.match(line):
            inside = True
            continue
        if not inside:
            continue
        if ref.SECTION_END_RE.match(line):
            inside = False
            continue
        m = ref.ROW_RE.match(line)
        if not m:
            continue
        sid = m.group(1).strip()
        if not ref.ID_CELL_RE.match(sid):
            continue
        source_cell = (m.group(2) or "").split("|", 1)[0]
        for url in ref.URL_RE.findall(source_cell):
            url = url.rstrip(".,;:")
            bucket = rows.setdefault(sid, [])
            if url not in bucket:
                bucket.append(url)
    return rows
ref.parse_registry = parse_registry
sys.exit(ref.main(sys.argv[1:]))
