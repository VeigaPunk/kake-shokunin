#!/usr/bin/env python3
"""Round-38 sealed cases v3 for C2 (redesign of withdrawn C1) (written by the L1 KakeR38 by hand from the round-38 contract).
Expectations are written here from the contract text, not recorded from any tool."""
import base64, json, sys

def b64(s):
    if isinstance(s, str):
        s = s.encode("utf-8")
    return {"b64": base64.b64encode(s).decode()}

def chk(i, url, expect, ua="Kbot", status=200, robots="r.txt", **extra):
    c = {"id": i, "robotsStatus": status, "userAgent": ua, "url": url, "expect": expect}
    if robots is not None:
        c["robots"] = robots
    c.update(extra)
    return c

def run(files, checks, findings, extra_top=None):
    exit_, verdict = 0, "clean"
    if any(r == "check_invalid" for _, r in findings):
        exit_, verdict = 2, "could-not-evaluate"
    elif findings:
        exit_, verdict = 1, "failed-policy"
    m = {"version": 1, "checks": checks}
    if extra_top:
        m.update(extra_top)
    return {"files": {k: b64(v) for k, v in files.items()}, "manifest": m,
            "expect": {"exit": exit_, "verdict": verdict,
                       "findings": [{"check": c, "reason": r} for c, r in findings]}}

def raw(files, template, findings, exit_=None, verdict=None):
    if exit_ is None:
        exit_, verdict = 0, "clean"
        if any(r in ("check_invalid", "input_invalid") for _, r in findings):
            exit_, verdict = 2, "could-not-evaluate"
        elif findings:
            exit_, verdict = 1, "failed-policy"
    return {"files": {k: b64(v) for k, v in files.items()}, "rawTemplate": template,
            "expect": {"exit": exit_, "verdict": verdict,
                       "findings": [{"check": c, "reason": r} for c, r in findings]}}

H = "https://site.example"
cases = []
def case(bullet, n, *runs):
    cases.append({"bullet": bullet, "id": f"{bullet}{n}", "runs": list(runs)})

# ---- (c) groups: exact product-token equality, ASCII-only folding, groups split only by user-agent
case("c", 1, run(
    {"r.txt": "User-agent: googlebot\nDisallow: /a\n\nUser-agent: *\nDisallow: /b\n"},
    [chk("a", H + "/a", "allow", ua="googlebot-news"),      # no exact name -> * group -> /a allowed: hold
     chk("b", H + "/b", "allow", ua="googlebot-news"),      # * group disallows /b: blocked
     chk("c", H + "/a", "disallow", ua="Googlebot")],       # exact (case-insensitive) -> disallowed: hold
    [("b", "blocked")]))
case("c", 2, run(
    {"r.txt": "User-agent: *\nDisallow: /admin\n\nUser-agent: Googlebot\nAllow: /\n",
     "r2.txt": "User-agent: *\nDisallow: /x\n\nUser-agent: *\nDisallow: /y\n"},
    [chk("a", H + "/admin", "disallow", ua="Googlebot-Image"),  # * group -> disallowed: hold
     chk("b", H + "/admin", "disallow", ua="Googlebot"),        # Googlebot group allows: exposed
     chk("c", H + "/ok", "allow", ua="Googlebot-Image"),        # hold
     chk("m", H + "/y", "disallow", robots="r2.txt")],           # both * groups combined: hold
    [("b", "exposed")]))
case("c", 3, run(
    {"r.txt": "user-agent: bot\ncrawl-delay: 5\nuser-agent: other\ndisallow: /x\n\nuser-agent: botnet\nallow: /\n"},
    [chk("a", H + "/x", "disallow", ua="bot"),       # one group {bot, other}: disallowed: hold
     chk("b", H + "/x", "allow", ua="other"),        # blocked
     chk("c", H + "/x", "disallow", ua="bo")],       # no group named bo, no * -> allowed: exposed
    [("b", "blocked"), ("c", "exposed")]))
case("c", 4, run(
    {"r.txt": "User-agent: \u212aakebot\nDisallow: /k\n\nUser-agent: kbot\nDisallow: /q\n\nUser-agent: KBOT\nDisallow: /r\n",
     "r3.txt": "User-agent: *\nDisallow: /\n\nUser-agent: kbot\n"},
    [chk("a", H + "/k", "allow", ua="kakebot"),      # Kelvin sign does not fold to k: no group, no * -> allowed: hold
     chk("b", H + "/r", "disallow", ua="kbot"),      # both kbot groups combined: /r disallowed: hold
     chk("c", H + "/q", "allow", ua="Kbot"),         # blocked
     chk("m", H + "/p", "allow", ua="kbot", robots="r3.txt")],  # matching group with no rules: allowed: hold
    [("c", "blocked")]))

# ---- R2 rules: specificity by rule length in octets (* and $ counted), allow wins ties, non-final $ literal
case("d", 1, run(
    {"r.txt": "User-agent: *\nAllow: /abc\nDisallow: /*\n",
     "r2.txt": "User-agent: *\nAllow: /a*\nDisallow: /ab\n"},
    [chk("a", H + "/abcdef", "allow"),     # /abc (4) beats /* (2): allowed: hold
     chk("m", H + "/abc", "allow", robots="r2.txt"),   # /a* (3) ties /ab (3): allow: hold
     chk("b", H + "/xyz", "allow")],       # /* disallows: blocked
    [("b", "blocked")]))
case("d", 2, run(
    {"r.txt": "User-agent: *\nDisallow: /private/\nAllow: /*.html\n",
     "r2.txt": "User-agent: *\nDisallow: /*x\nAllow: /x$\n"},
    [chk("a", H + "/private/a.html", "disallow"),   # /private/ (9) beats /*.html (7): disallowed: hold
     chk("b", H + "/public/a.html", "disallow"),    # only allow matches: exposed
     chk("m", H + "/x", "allow", robots="r2.txt")], # /x$ (3) ties /*x (3): allow: hold
    [("b", "exposed")]))
case("d", 3, run(
    {"r.txt": "User-agent: *\nDisallow: /*.php\nAllow: /index\n",
     "r2.txt": "User-agent: *\nAllow: /p\nDisallow: /p\n",
     "r3.txt": "User-agent: *\nDisallow: /*C\nAllow: /%7C\n"},
    [chk("a", H + "/index.php", "allow"),   # tie 6 = 6, allow wins: hold
     chk("b", H + "/other.php", "allow"),   # blocked
     chk("m", H + "/p", "allow", robots="r2.txt"),     # allow listed first, tie: allow: hold
     chk("n", H + "/%7C", "allow", robots="r3.txt")],  # /%7C (4 octets) beats /*C (3): hold
    [("b", "blocked")]))
case("d", 4, run(
    {"r.txt": "User-agent: *\nDisallow: /a$b\nAllow: /c$\nDisallow: /c\n",
     "r2.txt": "User-agent: *\nDisallow: /a\nAllow: /*.htm\n",
     "r3.txt": "User-agent: *\nDisallow: /a*b\nDisallow: /b\n"},
    [chk("a", H + "/a$b/x", "disallow"),    # literal $ prefix match: disallowed: hold
     chk("b", H + "/c", "allow"),           # /c$ (3) beats /c (2): allowed: hold
     chk("c", H + "/cd", "allow"),          # only /c matches: blocked
     chk("m", H + "/a.htm", "allow", robots="r2.txt"),    # /*.htm (6) beats /a (2): hold
     chk("n", H + "/ab", "disallow", robots="r3.txt"),    # * matches none: disallowed: hold
     chk("o", H + "/x/b", "allow", robots="r3.txt")],     # /b is not a prefix of /x/b: hold
    [("c", "blocked")]))

# ---- R3 JSON numbers (RFC 8259 section 6)
GOOD = '{"id": "@ID:g@", "robotsStatus": 200, "robots": "@FILE:r.txt@", "userAgent": "Kbot", "url": "https://site.example/p", "expect": "allow"}'
RF = {"r.txt": "User-agent: *\nDisallow: /p\n"}
case("j", 1,
     raw(RF, '{"version": 1, "checks": [' + GOOD + ', {"id": "@ID:n@", "robotsStatus": Infinity, "robots": "@FILE:r.txt@", "userAgent": "Kbot", "url": "https://site.example/q", "expect": "allow"}]}',
         [(None, "input_invalid")]),
     run(RF, [chk("a", H + "/p", "allow"), chk("b", H + "/q", "allow")], [("a", "blocked")]))
case("j", 2,
     raw(RF, '{"version": 1, "note": -Infinity, "checks": [' + GOOD + ']}', [(None, "input_invalid")]),
     raw(RF, '{"version": 1, "checks": [' + GOOD + ', {"id": "@ID:z@", "robotsStatus": 404, "userAgent": "Kbot", "url": "https://site.example/z", "expect": "disallow", "weight": NaN}]}',
         [(None, "input_invalid")]))
BIG = "2" + "0" * 4999
case("j", 3, raw(RF,
     '{"version": 1, "checks": [' + GOOD + ', {"id": "@ID:b@", "robotsStatus": ' + BIG + ', "robots": "@FILE:r.txt@", "userAgent": "Kbot", "url": "https://site.example/q", "expect": "allow"}, '
     '{"id": "@ID:c@", "robotsStatus": 200, "robots": "@FILE:r.txt@", "userAgent": "Kbot", "url": "https://site.example/q", "expect": "allow"}, '
     '{"id": "@ID:e@", "robotsStatus": 1e400, "robots": "@FILE:r.txt@", "userAgent": "Kbot", "url": "https://site.example/q", "expect": "allow"}]}',
     [("@ID:g@", "blocked"), ("@ID:b@", "check_invalid"), ("@ID:e@", "check_invalid")]))
case("j", 4, raw(RF,
     '{"version": 1, "size": ' + "9" * 6000 + ', "checks": [' + GOOD + ', {"id": "@ID:c@", "robotsStatus": 200, "robots": "@FILE:r.txt@", "userAgent": "Kbot", "url": "https://site.example/q", "expect": "disallow", "note": "NaN", "rank": -' + "7" * 4400 + '}]}',
     [("@ID:g@", "blocked"), ("@ID:c@", "exposed")]))

# ---- R4 URL characters (RFC 3986 section 2): ASCII outside the URI character set -> check_invalid
RU = {"r.txt": "User-agent: *\nDisallow: /a\n"}
case("u", 1, run(RU,
    [chk("a", H + "/a b", "allow"),           # space: check_invalid
     chk("b", H + "/a", "allow"),             # blocked
     chk("c", H + "/z", "allow"),             # hold
     chk("q", H + '/a"b', "allow")],          # double quote: check_invalid
    [("a", "check_invalid"), ("b", "blocked"), ("q", "check_invalid")]))
case("u", 2, run(RU,
    [chk("a", " " + H + "/z", "allow"),       # leading space: check_invalid
     chk("b", H + "/z\t", "disallow"),        # trailing tab: check_invalid
     chk("c", H + "/a/x", "disallow"),        # hold
     chk("d", H + "/z", "disallow"),          # exposed
     chk("q", H + "/<z>", "disallow")],       # angle brackets: check_invalid
    [("a", "check_invalid"), ("b", "check_invalid"), ("d", "exposed"), ("q", "check_invalid")]))
case("u", 3, run(RU,
    [chk("a", H + "/a\nb", "disallow"),       # newline: check_invalid
     chk("b", "ht\ttps://site.example/a", "disallow"),   # tab inside scheme: check_invalid
     chk("c", H + "/ab", "disallow"),         # hold
     chk("d", H + "/b", "disallow"),          # exposed
     chk("q", H + "/a^b\\c", "allow")],      # caret and backslash: check_invalid
    [("a", "check_invalid"), ("b", "check_invalid"), ("d", "exposed"), ("q", "check_invalid")]))
case("u", 4, run(RU,
    [chk("a", H + "/a|b", "disallow"),        # | not a URI character: check_invalid
     chk("b", H + "/{x}", "allow"),           # { } : check_invalid
     chk("c", H + "/a\x7f`", "disallow"),     # DEL and backtick: check_invalid
     chk("d", H + "/caf\u00e9", "allow"),     # non-ASCII kept (lane reading, rule (e)): hold
     chk("e", H + "/a%7Cb", "allow")],        # percent-encoded |: valid; /a prefix: blocked
    [("a", "check_invalid"), ("b", "check_invalid"), ("c", "check_invalid"), ("e", "blocked")]))

# ---- R5 implicit /robots.txt allow on the normalized path to match
RA = {"r.txt": "User-agent: *\nDisallow: /\n"}
case("r", 1, run(RA,
    [chk("a", H + "/robots%2Etxt", "allow"),     # normalizes to /robots.txt: allowed: hold
     chk("q", H + "/robots.txt?a", "disallow"),  # query: rules decide: hold
     chk("t", H + "/robots.txt/", "disallow"),   # trailing slash: rules decide: hold
     chk("b", H + "/x", "allow")],               # blocked
    [("b", "blocked")]))
case("r", 2, run(RA,
    [chk("a", H + "/%72obots.txt", "allow"),     # %72 = r: hold
     chk("b", H + "/robots.txt?x=1", "disallow"),# path to match has a query: rules decide: hold
     chk("q", H + "/Robots.txt", "disallow"),    # case differs: rules decide: hold
     chk("c", H + "/robots.txt", "disallow")],   # implicitly allowed: exposed
    [("c", "exposed")]))
case("r", 3, run(RA,
    [chk("a", H + "/ROBOTS.TXT", "disallow"),    # case differs: rules decide: hold
     chk("b", H + "/robots%2etxt", "allow"),     # lowercase hex: hold
     chk("c", H + "/robots%2Ftxt", "allow")],    # %2F reserved, kept: not /robots.txt: blocked
    [("c", "blocked")]))
case("r", 4, run(RA,
    [chk("a", H + "/robots.tx%74", "allow"),     # %74 = t: hold
     chk("q", H + "/robots.TXT?z=%2E", "disallow"),  # case and query: rules decide: hold
     chk("b", H + "/robots%2Etxt", "disallow", status=503, robots=None),  # unreachable: disallowed: hold
     chk("c", H + "/robots.txt#top", "disallow")],  # fragment dropped: implicitly allowed: exposed
    [("c", "exposed")]))

EXCL = [chr(c) for c in range(0x00, 0x21)] + ["\x7f", '"', "<", ">", "\\", "^", "`", "{", "|", "}"]
POS = [lambda ch: H + "/a" + ch + "z", lambda ch: H + "/z?q=" + ch, lambda ch: H + "/z#f" + ch,
       lambda ch: ch + H + "/z", lambda ch: H + "/z" + ch, lambda ch: "https://site" + ch + ".example/z"]
for n, ch in enumerate(EXCL):
    c = cases[-8 + n % 4]   # u1..u4 sit at positions -8..-5 (before r1..r4)
    assert c["id"].startswith("u"), c["id"]
    url = POS[n % len(POS)](ch)
    cid = "x%02d" % n
    c["runs"][0]["manifest"]["checks"].append(chk(cid, url, "allow" if n % 2 else "disallow"))
    c["runs"][0]["expect"]["findings"].append({"check": cid, "reason": "check_invalid"})
    c["runs"][0]["expect"].update(exit=2, verdict="could-not-evaluate")

for c in cases:
    for r in c["runs"]:
        e = r["expect"]
        if any(f["reason"] == "input_invalid" for f in e["findings"]):
            e["checksEvaluated"] = 0
        elif "manifest" in r:
            e["checksEvaluated"] = len(r["manifest"]["checks"]) - sum(f["reason"] == "check_invalid" for f in e["findings"])
        else:
            e["checksEvaluated"] = r["rawTemplate"].count('"robotsStatus"') - sum(f["reason"] == "check_invalid" for f in e["findings"])

# raw templates carry @ID:x@ tokens in findings: keep as written; counter maps them.
key = {"version": 1, "claim": "C1", "round": 38, "cases": cases}
json.dump(key, sys.stdout, indent=1, sort_keys=True, ensure_ascii=True)
print()
