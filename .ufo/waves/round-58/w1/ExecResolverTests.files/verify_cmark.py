import os, subprocess, xml.etree.ElementTree as ET
CASES = {
 "01-four-backtick-not-closed-by-three": ({"S901","S902"}, {"S101"}, 1),
 "02-tilde-fence-not-closed-by-backticks": ({"S903","S904"}, {"S102"}, 1),
 "03-four-space-fence-line-is-code": (set(), {"S103","S905"}, 2),
 "04-fence-with-info-string": ({"S906"}, {"S104","S907"}, 2),
 "05-unclosed-fence-to-eof": ({"S908","S909"}, {"S105"}, 1),
 "06-heading-after-fenced-heading": ({"S910"}, {"S106","S911"}, 2),
 "07-three-space-row-after-fence": ({"S912"}, {"S107","S913"}, 1),
 "08-crlf-around-fence": ({"S914"}, {"S108","S915"}, 2),
}
ok_all = True
for case,(code_want, real_want, heads_want) in CASES.items():
    path = os.path.join("cases", case, "demo-shokunin", "corpus", "SOURCES.md")
    p = subprocess.run(["cmark","--to","xml",path], capture_output=True, text=True)
    if p.returncode != 0:
        print(f"CMARK-ERR {case}: {p.stderr.strip()[:120]}"); ok_all=False; continue
    root = ET.fromstring(p.stdout)
    code_text = "\n".join("".join(n.itertext()) for n in root.iter("{http://commonmark.org/xml/1.0}code_block"))
    heads = ["".join(n.itertext()).strip() for n in root.iter("{http://commonmark.org/xml/1.0}heading")]
    import re
    in_code = set(re.findall(r"S\d{3,}", code_text))
    all_ids = set(re.findall(r"S\d{3,}", open(path, encoding="utf-8", newline="").read()))
    not_code = all_ids - in_code
    registries = sum(1 for h in heads if h == "Registry")
    ok = in_code == code_want and not_code == real_want and registries == heads_want
    ok_all &= ok
    print(("CMARK-OK   " if ok else "CMARK-FAIL ") + case +
          f": code={sorted(in_code)} not-code={sorted(not_code)} registry-headings={registries}")
print("cmark oracle:", "all fixture expectations match the CommonMark reference parser" if ok_all else "MISMATCH")
