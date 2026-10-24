#!/usr/bin/env python3
"""L1 private sealed cases for kake round-37 C1. Truths are written by hand per check; the
generator asserts the private reference agrees and that every listed ablation fails every case
of its bullet. Output: cases.json (the sealed key)."""
from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REF = HERE / "ref.py"
UAS = ["Kbot", "ZetaCrawler", "lumen_spider", "Hare-Bot"]
HOSTS = ["https://example.com", "http://www.example.org", "https://shop.example.net", "http://docs.example.test"]
WORDS = ["qa", "lm", "rt", "vx"]

BULLET_ABL = {
    "a": ["a_4xx", "a_5xx", "a_2xx"],
    "b": ["b_limit", "b_bom", "b_cr", "b_comment", "b_keycase", "b_orphan", "b_other"],
    "c": ["c_uacase", "c_merge", "c_star", "c_consecutive"],
    "d": ["d_longest", "d_tie", "d_star", "d_dollar", "d_empty"],
    "e": ["e_nonascii", "e_unreserved", "e_hexcase", "f_emptypath", "f_query", "f_fragment", "f_robots"],
    "f": ["f_dup", "f_3xx", "f_ua", "f_escape", "f_expect", "f_scheme"],
    "g": ["g_version", "g_checklist"],
}


def b64(b: bytes) -> dict:
    return {"b64": base64.b64encode(b).decode()}


class Run:
    def __init__(self):
        self.files: dict[str, bytes] = {}
        self.checks: list = []
        self.truth: list = []  # per check: ("ok", truth, flip) or ("invalid",)
        self.n = 0

    def file(self, data, name=None):
        name = name or f"r{len(self.files)}.txt"
        self.files[name] = data if isinstance(data, bytes) else data.encode("utf-8")
        return name

    def check(self, robots, ua, url, truth, flip, status=200, **over):
        self.n += 1
        cid = over.pop("cid", f"k{self.n}")
        c = {"id": cid, "robotsStatus": status, "userAgent": ua, "url": url,
             "expect": (("disallow" if truth == "allow" else "allow") if flip else truth)}
        if robots is not None:
            c["robots"] = robots
        invalid = over.pop("invalid", False)
        c.update(over)
        for k in [k for k, v in c.items() if v is DROP]:
            del c[k]
        self.checks.append(c)
        self.truth.append(("invalid", cid) if invalid else ("ok", cid, truth, flip))

    def expect(self):
        findings = []
        for t in self.truth:
            if t[0] == "invalid":
                findings.append({"check": t[1], "reason": "check_invalid"})
            elif t[3]:
                findings.append({"check": t[1], "reason": "blocked" if t[2] == "disallow" else "exposed"})
        if any(f["reason"] == "check_invalid" for f in findings):
            v = "could-not-evaluate"
        elif findings:
            v = "failed-policy"
        else:
            v = "clean"
        return {"exit": {"clean": 0, "failed-policy": 1, "could-not-evaluate": 2}[v], "verdict": v,
                "findings": findings}

    def dump(self, manifest=None, raw=None, expect=None):
        out = {"files": {k: b64(v) for k, v in self.files.items()}}
        if raw is not None:
            out["raw"] = b64(raw)
        else:
            out["manifest"] = manifest if manifest is not None else {"version": 1, "checks": self.checks}
        out["expect"] = expect or self.expect()
        return out


DROP = object()


def case_a(k):
    r = Run()
    ua, h, w = UAS[k], HOSTS[k], WORDS[k]
    dis_all = r.file(f"user-agent: *\ndisallow: /\n")
    allow_all = r.file(f"user-agent: *\nallow: /\n")
    part = r.file(f"user-agent: {ua}\ndisallow: /{w}/\n")
    s4 = [404, 403, 410, 429][k]
    s5 = [503, 500, 502, 599][k]
    s2 = [203, 206, 299, 204][k]
    r.check(dis_all, ua, f"{h}/{w}/one", "allow", flip=k in (1, 3), status=s4)       # a_4xx
    r.check(allow_all, ua, f"{h}/{w}/two", "disallow", flip=k in (0, 2), status=s5)  # a_5xx
    r.check(part, ua, f"{h}/{w}/three", "disallow", flip=k in (1, 2), status=s2)     # a_2xx
    r.check(part, ua, f"{h}/x{w}/four", "allow", flip=k in (0, 3))                   # plain
    r.check(part, ua, f"{h}/{w}/five", "disallow", flip=False)
    return [r.dump()]


def case_b(k):
    r = Run()
    ua, h, w = UAS[k], HOSTS[k], WORDS[k]
    nl = ["\n", "\r\n", "\n", "\r\n"][k]
    bom = r.file(b"\xef\xbb\xbf" + f"user-agent: {ua}{nl}disallow: /{w}1{nl}".encode())
    cr = r.file(f"user-agent: {ua}\rdisallow: /{w}2\r")
    com = r.file(f"user-agent: {ua}{nl}disallow: /{w}3#note{nl}" if k % 2 == 0 else
                 f"# head{nl}user-agent: {ua} # crawler{nl}disallow: /{w}3 # legacy: /zz{nl}")
    keycase = r.file(["USER-AGENT", "User-Agent", "uSeR-aGeNt", "User-agent"][k] + f": {ua}{nl}" +
                     ["DISALLOW", "Disallow", "DisAllow", "DISallow"][k] + f": /{w}4{nl}")
    orphan = r.file(f"disallow: /{w}5{nl}{nl}user-agent: {ua}{nl}allow: /other{nl}")
    other = r.file(f"user-agent: {ua}{nl}" + ["sitemap: https://example.com/s.xml", "crawl-delay: 10",
                   "Sitemap: https://example.com/map.xml", "host: example.com"][k] + f"{nl}disallow: /{w}6{nl}")
    head = f"user-agent: {ua}\n".encode()
    filler_line = b"# " + b"x" * 97 + b"\n"   # 100 bytes
    need = 512000 - len(head)
    filler = filler_line * (need // 100) + b"#" * (need % 100 - 1) + b"\n" if need % 100 else filler_line * (need // 100)
    body = head + filler
    assert len(body) == 512000, len(body)
    lim = r.file(body + f"disallow: /{w}7\n".encode())
    fl = [k % 2 == 0, k % 2 == 1]
    r.check(bom, ua, f"{h}/{w}1/a", "disallow", flip=fl[0])
    r.check(cr, ua, f"{h}/{w}2/b", "disallow", flip=fl[1])
    r.check(com, ua, f"{h}/{w}3/c", "disallow", flip=fl[0])
    r.check(keycase, ua, f"{h}/{w}4/d", "disallow", flip=fl[1])
    r.check(orphan, "Nobody", f"{h}/{w}5/e", "allow", flip=fl[0])
    r.check(other, ua, f"{h}/{w}6/f", "disallow", flip=fl[1])
    r.check(lim, ua, f"{h}/{w}7/g", "allow", flip=fl[0])
    return [r.dump()]


def case_c(k):
    r = Run()
    ua, h, w = UAS[k], HOSTS[k], WORDS[k]
    sep = ["\n", "\n\n", "\n", "\n\n"][k]
    variants = [ua.upper(), ua.lower(), ua.swapcase(), ua[0].lower() + ua[1:].upper()]
    uacase = r.file(f"user-agent: {variants[k]}\ndisallow: /{w}1\n")
    merge = r.file(f"user-agent: {ua}\ndisallow: /{w}2a\n{sep}user-agent: Other\ndisallow: /\n{sep}"
                   f"user-agent: {ua}\ndisallow: /{w}2b\n")
    star = r.file(f"user-agent: *\ndisallow: /{w}3\n{sep}user-agent: Other\nallow: /\n")
    named_over_star = r.file(f"user-agent: *\ndisallow: /{w}3\n{sep}user-agent: {ua}\nallow: /zz\n")
    consec = r.file(f"user-agent: Abot{sep}user-agent: {ua}\ndisallow: /{w}4\n")
    nogroup = r.file(f"user-agent: Other\ndisallow: /\n")
    fl = [k % 2 == 0, k % 2 == 1]
    r.check(uacase, ua, f"{h}/{w}1/a", "disallow", flip=fl[0])
    r.check(merge, ua, f"{h}/{w}2b/b", "disallow", flip=fl[1])
    r.check(merge, ua, f"{h}/{w}2a/b", "disallow", flip=False)
    r.check(star, ua, f"{h}/{w}3/c", "disallow", flip=fl[0])
    r.check(named_over_star, ua, f"{h}/{w}3/c", "allow", flip=fl[1])
    r.check(consec, "Abot", f"{h}/{w}4/d", "disallow", flip=fl[1])
    r.check(nogroup, ua, f"{h}/{w}5/e", "allow", flip=fl[0])
    return [r.dump()]


def case_d(k):
    r = Run()
    ua, h, w = UAS[k], HOSTS[k], WORDS[k]
    longest = r.file(f"user-agent: *\ndisallow: /{w}1\nallow: /{w}1/open\n" if k % 2 == 0 else
                     f"user-agent: *\nallow: /{w}1\ndisallow: /{w}1/shut\n")
    tie = r.file(f"user-agent: *\ndisallow: /{w}2\nallow: /{w}2\n" if k % 2 == 0 else
                 f"user-agent: *\nallow: /{w}2/*\ndisallow: /{w}2/x\n")
    star = r.file(f"user-agent: *\ndisallow: /{w}3/*/edit\n")
    dollar = r.file(f"user-agent: *\ndisallow: /{w}4.php$\n")
    empty = r.file(f"user-agent: *\ndisallow:\n")
    fl = [k % 2 == 0, k % 2 == 1]
    if k % 2 == 0:
        r.check(longest, ua, f"{h}/{w}1/open/x", "allow", flip=fl[0])
        r.check(tie, ua, f"{h}/{w}2x", "allow", flip=fl[1])
    else:
        r.check(longest, ua, f"{h}/{w}1/shut/x", "disallow", flip=fl[0])
        r.check(tie, ua, f"{h}/{w}2/xy", "allow", flip=fl[1])
    r.check(star, ua, f"{h}/{w}3/a{k}b/edit", "disallow", flip=fl[0])
    r.check(dollar, ua, f"{h}/{w}4.php", "disallow", flip=fl[1])
    r.check(dollar, ua, f"{h}/{w}4.php?x=1", "allow", flip=False)
    r.check(empty, ua, f"{h}/{w}5", "allow", flip=fl[0])
    return [r.dump()]


def case_e(k):
    r = Run()
    ua, h, w = UAS[k], HOSTS[k], WORDS[k]
    na = ["ü", "é", "ツ", "ß"][k]
    enc = "".join("%%%02X" % b for b in na.encode())
    if k % 2 == 0:
        nonascii = r.file(f"user-agent: *\ndisallow: /{w}1/{na}\n")
        na_url = f"{h}/{w}1/{enc}x"
    else:
        nonascii = r.file(f"user-agent: *\ndisallow: /{w}1/{enc}\n")
        na_url = f"{h}/{w}1/{na}x"
    unres = r.file(f"user-agent: *\ndisallow: /{w}2/%61b%7E\n" if k % 2 == 0 else
                   f"user-agent: *\ndisallow: /{w}2/ab~\n")
    unres_url = f"{h}/{w}2/ab~/z" if k % 2 == 0 else f"{h}/{w}2/%61%62%7e/z"
    hexc = r.file(f"user-agent: *\ndisallow: /{w}3/a%2fb\n" if k % 2 == 0 else
                  f"user-agent: *\ndisallow: /{w}3/a%2Fb\n")
    hex_url = f"{h}/{w}3/a%2Fb" if k % 2 == 0 else f"{h}/{w}3/a%2fb"
    reserved = r.file(f"user-agent: *\ndisallow: /{w}3/a%2Fb\n")
    root = r.file(f"user-agent: *\ndisallow: /$\n" if k % 2 == 0 else f"user-agent: *\ndisallow: /\nallow: /{w}\n")
    query = r.file(f"user-agent: *\ndisallow: /{w}5?print=\n")
    frag = r.file(f"user-agent: *\ndisallow: /{w}6$\n")
    robots = r.file(f"user-agent: *\ndisallow: /\n")
    fl = [k % 2 == 0, k % 2 == 1]
    r.check(nonascii, ua, na_url, "disallow", flip=fl[0])
    r.check(unres, ua, unres_url, "disallow", flip=fl[1])
    r.check(hexc, ua, hex_url, "disallow", flip=fl[0])
    r.check(reserved, ua, f"{h}/{w}3/a/b", "allow", flip=False)
    r.check(root, ua, h, "disallow", flip=fl[1])
    r.check(query, ua, f"{h}/{w}5?print=1", "disallow", flip=fl[0])
    r.check(frag, ua, f"{h}/{w}6#top", "disallow", flip=fl[1])
    r.check(robots, ua, f"{h}/robots.txt", "allow", flip=fl[0])
    return [r.dump()]


def case_f(k):
    r = Run()
    ua, h, w = UAS[k], HOSTS[k], WORDS[k]
    part = r.file(f"user-agent: {ua}\ndisallow: /{w}/\n")
    r.check(part, ua, f"{h}/{w}/a", "disallow", flip=k % 2 == 0, cid="dupid")
    r.check(part, ua, f"{h}/{w}/b", "allow", flip=False, cid="dupid", invalid=True)           # f_dup
    r.check(part, ua, f"{h}/{w}/c", "allow", flip=False, status=[301, 302, 304, 399][k], invalid=True)  # f_3xx
    r.check(part, [f"{ua}/1.0", "Bot 2", "bot.v2", "Ünibot"][k], f"{h}/{w}/d", "allow", flip=False, invalid=True)  # f_ua
    esc = ["../outside.txt", "sub/../../outside.txt", "./../outside.txt", "../outside.txt"][k]
    r.check(esc, ua, f"{h}/x/e", "allow", flip=False, invalid=True)                          # f_escape
    r.check(part, ua, f"{h}/x/f", "allow", flip=False, invalid=True, expect=["Allow", "deny", "yes", "allowed"][k])  # f_expect
    r.check(part, ua, ["ftp://example.com/x", "ws://example.com/x", "gopher://example.com/x", "httpx://example.com/x"][k],
            "allow", flip=False, invalid=True)                                              # f_scheme
    r.check(part, ua, f"{h}/x{w}/g", "allow", flip=k % 2 == 1)
    r.files["../outside.txt"] = f"user-agent: *\nallow: /\n".encode()
    return [r.dump()]


def case_g(k):
    runs = []
    r = Run()
    ua, h, w = UAS[k], HOSTS[k], WORDS[k]
    part = r.file(f"user-agent: {ua}\ndisallow: /{w}/\n")
    r.check(part, ua, f"{h}/{w}/a", "disallow", flip=True)
    bad = {"exit": 2, "verdict": "could-not-evaluate", "findings": [{"check": None, "reason": "input_invalid"}]}
    ver = [2, "1", 1.0, True][k]
    runs.append(r.dump(manifest={"version": ver, "checks": r.checks}, expect=bad))
    lst = [{"k1": r.checks[0]}, None, "k1", 7][k]
    runs.append(r.dump(manifest={"version": 1, "checks": lst}, expect=bad))
    runs.append(r.dump(raw=[b"{version: 1}", b"", b"{\"version\": 1, \"checks\": [", b"\xff\xfe{}"][k], expect=bad))
    runs.append(r.dump(raw=b"null", expect=bad) if k == 1 else r.dump(manifest=[[r.checks], None, "manifest", 1][k], expect=bad))
    runs.append(r.dump())  # the same check under a valid manifest: one finding
    return runs


BUILDERS = {"a": case_a, "b": case_b, "c": case_c, "d": case_d, "e": case_e, "f": case_f, "g": case_g}


def run_ref(run: dict, ablate: str) -> tuple[int, dict | None]:
    with tempfile.TemporaryDirectory() as td:
        work = Path(td) / "w"
        work.mkdir()
        for name, body in run["files"].items():
            (work / name).parent.mkdir(parents=True, exist_ok=True)
            (work / name).write_bytes(base64.b64decode(body["b64"]))
        m = work / "manifest.json"
        if "raw" in run:
            m.write_bytes(base64.b64decode(run["raw"]["b64"]))
        else:
            m.write_text(json.dumps(run["manifest"]))
        env = dict(os.environ, KAKE_ABLATE=ablate)
        p = subprocess.run([sys.executable, "-B", str(REF), "--manifest", str(m)], capture_output=True, env=env, timeout=30)
        try:
            return p.returncode, json.loads(p.stdout)
        except ValueError:
            return p.returncode, None


def proj(fs):
    return sorted((json.dumps(f.get("check")), f.get("reason")) for f in fs)


def run_ok(run, ablate):
    code, rep = run_ref(run, ablate)
    e = run["expect"]
    return rep is not None and code == e["exit"] and rep.get("verdict") == e["verdict"] and proj(rep["findings"]) == proj(e["findings"])


def main():
    cases = []
    for bullet, fn in BUILDERS.items():
        for k in range(4):
            cases.append({"id": f"{bullet}{k + 1}", "bullet": bullet, "runs": fn(k)})
    bad = 0
    for c in cases:
        for i, run in enumerate(c["runs"]):
            if not run_ok(run, ""):
                bad += 1
                code, rep = run_ref(run, "")
                print("REFERENCE DISAGREES", c["id"], i, code, json.dumps(rep)[:400], json.dumps(run["expect"])[:400])
    for bullet, abls in BUILDERS.items():
        pass
    abl_report = {}
    for bullet, abls in BULLET_ABL.items():
        for a in abls:
            fails = [c["id"] for c in cases if not all(run_ok(run, a) for run in c["runs"])]
            own = [c["id"] for c in cases if c["bullet"] == bullet]
            abl_report[a] = {"bullet": bullet, "failed": fails, "passed": 28 - len(fails),
                             "allOwnFailed": all(x in fails for x in own)}
            if not abl_report[a]["allOwnFailed"]:
                print("ABLATION MISSES OWN CASES", a, [x for x in own if x not in fails])
    key = {"version": 1, "claim": "kake r37 C1", "cases": cases}
    data = json.dumps(key, sort_keys=True).encode()
    (HERE / "cases.json").write_bytes(data)
    (HERE / "ablation-pre.json").write_text(json.dumps(abl_report, indent=1))
    print("reference disagreements:", bad, "cases:", len(cases), "bytes:", len(data))
    print("max ablation passed:", max(v["passed"] for v in abl_report.values()))


if __name__ == "__main__":
    main()
