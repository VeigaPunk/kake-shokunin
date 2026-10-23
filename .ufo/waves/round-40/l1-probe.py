import json, os, subprocess, sys, tempfile
TOOL = sys.argv[1]
NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
def us(loc, decl='<?xml version="1.0" encoding="UTF-8"?>\n'):
    return decl + '<urlset xmlns="%s"><url><loc>%s</loc></url></urlset>' % (NS, loc)
def run(files, checks):
    with tempfile.TemporaryDirectory() as d:
        for n, b in files.items():
            open(os.path.join(d, n), "wb").write(b)
        json.dump({"version": 1, "checks": checks}, open(os.path.join(d, "m.json"), "w"))
        p = subprocess.run([sys.executable, "-B", TOOL, "--manifest", os.path.join(d, "m.json")], capture_output=True)
        return p.returncode, p.stdout.decode()[:300]
SU = "http://example.com/dir/sitemap.xml"
ok = us("http://example.com/dir/a")
cases = {
 "v11": us("http://example.com/dir/a", '<?xml version="1.1" encoding="UTF-8"?>\n').encode(),
 "v20": us("http://example.com/dir/a", '<?xml version="2.0" encoding="UTF-8"?>\n').encode(),
 "u16le": ok.encode("utf-16-le"), "u16be": ok.encode("utf-16-be"), "u32le": ok.encode("utf-32-le"),
 "u16le_nodecl": us("http://example.com/dir/a", "").encode("utf-16-le"),
 "nul_raw": us("http://example.com/dir/a\x00b").encode(),
 "tab_mid": us("http://example.com/di\tr/a").encode(), "lf_mid": us("http://example.com/di\nr/a").encode(),
 "cr_ref": us("http://example.com/di&#13;r/a").encode(), "tab_ref": us("http://example.com/di&#9;r/a").encode(),
 "tab_host": us("http://exa\tmple.com/dir/a").encode(),
 "tab_lead": us("\thttp://example.com/dir/a\n").encode(), "sp_mid": us("http://example.com/di r/a").encode(),
 "pct09": us("http://example.com/di%09r/a").encode(),
}
for k, b in cases.items():
    print(k, *run({"s.xml": b}, [{"id": "x", "file": "s.xml", "sitemapUrl": SU}]))
okb = ok.encode()
for k, su in {"su_tab": "http://example.com/d\tir/sitemap.xml", "su_lead_sp": " http://example.com/dir/sitemap.xml",
              "su_lead_c0": "\x01http://example.com/dir/sitemap.xml", "su_trail_sp": "http://example.com/dir/sitemap.xml ",
              "su_lf_host": "http://exam\nple.com/dir/sitemap.xml"}.items():
    print(k, *run({"s.xml": okb}, [{"id": "x", "file": "s.xml", "sitemapUrl": su}]))
for k, first in {"d5_nofile": {"id": "x", "sitemapUrl": SU}, "d5_nourl": {"id": "x", "file": "s.xml"},
                 "d5_inturl": {"id": "x", "file": "s.xml", "sitemapUrl": 5}, "d5_absfile": {"id": "x", "file": "/s.xml", "sitemapUrl": SU},
                 "d5_intid": {"id": 5, "file": "s.xml", "sitemapUrl": SU}}.items():
    print(k, *run({"s.xml": okb}, [first, {"id": "x" if k != "d5_intid" else "5", "file": "s.xml", "sitemapUrl": SU}]))
