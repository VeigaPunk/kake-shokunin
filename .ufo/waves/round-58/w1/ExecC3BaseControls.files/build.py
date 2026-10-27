#!/usr/bin/env python3
"""Round-58 C3 base controls: build junk fixtures in a scratch clone and score them with the frozen counter."""
import json
import os
import shutil
import subprocess
import sys

CLONE = "/fast/scratch/hyaku/kake-r58/ExecC3BaseControls/freeze"
COUNTER = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/c58_quote_truth.py"
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
PARENT = "fff3eea6aa349c8635fd84a791cc32de350ee1c2"
V_REL = ".ufo/waves/round-58/assimilation/validate"
V = f"{CLONE}/{V_REL}"
NONCORPUS = ["SCORECARD.md", "SKILL.md", "scripts/source_recheck.py",
             ".ufo/waves/round-41/c1_count.py", ".ufo/waves/round-41/oracle_crosscheck.py"]

SHA = {"S423": "8b8aef60bd7e315799e9a97dadfd02a5982f8c7e17b9d4064a6fc3913a0736ec",
       "S424": "3ef1275b730230f2cb9c14b28b1c4bd08dc363dc7941b63d06c507fb2729cad1"}
BYTES = {"S423": 29007, "S424": 22476}
URL = {"S423": "https://ziyuan.baidu.com/college/articleinfo?id=3457",
       "S424": "https://ziyuan.baidu.com/college/articleinfo?id=3028"}
ENTRY = {"S423": "corpus/knowledge/baidu-spider-identification.md",
         "S424": "corpus/knowledge/baidu-spider-unblocking.md"}
ROW = {
    "S423": ("| S423 | 百度搜索资源平台 — 搜索问答剧场 【五】“百度蜘蛛”全面解析 — " + URL["S423"] +
             " | docs | A | **Baidu's two-step crawler identification** — UA strings per channel and reverse then forward DNS "
             "against *.baidu.com / *.baidu.jp | § 方式二：双向DNS解析认证 (发布日期 2022-08-19) | "
             "Baidu's page states the two identification steps and that a hostname outside *.baidu.com / *.baidu.jp is an "
             "impersonation | mined | 2026-10-26 | 180d | {used_by} |"),
    "S424": ("| S424 | 百度搜索资源平台 — 开发者如何解除封禁百度蜘蛛 — " + URL["S424"] +
             " | docs | A | **Three block kinds and their checks** — robots, Baidu UA and Baidu IP blocks with the page's "
             "unblocking steps | § robots文件说明： (发布日期 2020-07-23) | "
             "Baidu's page lists the three block kinds, the robots.txt check and the curl UA check that exposes a UA block | "
             "mined | 2026-10-26 | 180d | {used_by} |"),
}
ANCHOR = {"S423": "§ 方式二：双向DNS解析认证 (发布日期 2022-08-19)",
          "S424": "§ robots文件说明： (发布日期 2020-07-23)"}

# entry bodies: header + prose + quotes
HEAD = {
    "S423": ("source: S423 — {url} — § 方式二：双向DNS解析认证 (发布日期 2022-08-19) — fetched 2026-10-26\n"
             "verified-at: 2026-10-26\nrecheck: 180d\nground: per-engine crawl hygiene — Baidu's own crawler identification\n"),
    "S424": ("source: S424 — {url} — § robots文件说明： (发布日期 2020-07-23) — fetched 2026-10-26\n"
             "verified-at: 2026-10-26\nrecheck: 180d\nground: per-engine crawl hygiene — Baidu's own unblocking steps\n"),
}


def entry_body(sid, quotes, prose):
    head = HEAD[sid].format(url=URL[sid])
    lines = [f"# Control fixture entry for {sid}", "",
             prose, ""]
    for q in quotes:
        lines.append(f"- quoted: \"{q}\"")
    lines.append("")
    lines.append(f"mined {sid} — control fixture, no real assimilation.")
    return head + "\n".join(lines) + "\n"


def gate_line(sid, quotes):
    parts = [f"- {sid} — {URL[sid]} — accessed 2026-10-26 — {ANCHOR[sid]} — quote:"]
    for q in quotes:
        parts.append(f" \"{q}\" ({units(q)} units; raw substring of the retained body)")
    parts.append(f" — sha256 {SHA[sid]}, {BYTES[sid]} bytes, HTTP 200")
    return " ".join(parts)


# unit count exactly as the counter defines it (import it)
def units(text):
    import re
    cjk = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]")
    return len(cjk.findall(text)) + len([t for t in text.split() if not cjk.search(t)])


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def git(*args, cwd=CLONE):
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True)


def build(name, quotes, gates, used_by=None, argv_mode="file", prose="Control fixture.", mirror_rows=False):
    r = git("checkout", "-q", "-f", "-B", f"ctl-{name}", PARENT)
    assert r.returncode == 0, r.stderr
    assert git("rev-parse", "--show-toplevel").stdout.strip() == CLONE
    # registry: insert the two rows right after S422
    reg_path = os.path.join(CLONE, "corpus/SOURCES.md")
    with open(reg_path, encoding="utf-8", newline="") as fh:
        lines = fh.read().split("\n")
    idx = next(i for i, ln in enumerate(lines) if ln.startswith("| S422 |"))
    ub = used_by or {sid: ENTRY[sid] for sid in ("S423", "S424")}
    rows = [ROW["S423"].format(used_by=ub["S423"]), ROW["S424"].format(used_by=ub["S424"])]
    lines[idx + 1:idx + 1] = rows
    write(reg_path, "\n".join(lines))
    if mirror_rows:  # control: the seat edits the pre-append mirror to carry the new rows
        mirror = os.path.join(CLONE, ".ufo/waves/round-58/assimilation/pre-append/corpus/SOURCES.md")
        with open(mirror, encoding="utf-8", newline="") as fh:
            mlines = fh.read().split("\n")
        midx = next(i for i, ln in enumerate(mlines) if ln.startswith("| S422 |"))
        mlines[midx + 1:midx + 1] = rows
        write(mirror, "\n".join(mlines))
    # entries
    for sid in ("S423", "S424"):
        write(os.path.join(CLONE, ENTRY[sid]), entry_body(sid, quotes[sid], prose))
    # lesson
    lesson = ("# Round 58 — kake (control fixture lesson)\n\n## Gate\n\n"
              + "\n".join(gate_line(sid, gates[sid]) for sid in ("S423", "S424")) + "\n")
    write(os.path.join(CLONE, "corpus/lessons/round-58.md"), lesson)
    # validate receipts (real census run)
    shutil.rmtree(V, ignore_errors=True)
    os.makedirs(V)
    shutil.copytree(os.path.join(CLONE, "corpus"), os.path.join(V, "corpus"))
    for f in NONCORPUS:
        dst = os.path.join(V, f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(os.path.join(CLONE, f), dst)
    file_argv = f"{CENSUS} validate --file {V}/corpus/SOURCES.md"
    root_argv = f"{CENSUS} validate --root {V} {V}"
    run_argv = root_argv if argv_mode in ("root", "mislabel") else file_argv
    label_argv = file_argv if argv_mode == "mislabel" else run_argv
    proc = subprocess.run(run_argv.split(), capture_output=True, text=True)
    write(os.path.join(V, "census-argv.txt"), label_argv + "\n")
    write(os.path.join(V, "census-stdout.txt"), proc.stdout)
    write(os.path.join(V, "census-stderr.txt"), proc.stderr)
    write(os.path.join(V, "census-exit.txt"), f"exit={proc.returncode}\n")
    # commit
    git("add", "-A")
    c = subprocess.run(["git", "-C", CLONE, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
                        "commit", "-q", "-m", f"control {name}"], capture_output=True, text=True)
    assert c.returncode == 0, c.stderr + c.stdout
    rev = git("rev-parse", "HEAD").stdout.strip()
    score(name, rev, proc.returncode)
    return rev


def score(name, rev, census_exit):
    out = subprocess.run([sys.executable, "-B", COUNTER, "--root", CLONE, "--revision", rev, "--json"],
                         capture_output=True, text=True)
    try:
        data = json.loads(out.stdout)
    except json.JSONDecodeError:
        print(f"[{name}] counter produced no JSON: rc={out.returncode} {out.stdout[:400]} {out.stderr[:400]}")
        return
    passed = [k for k, v in data["checks"].items() if v["passed"]]
    failed = [k for k, v in data["checks"].items() if not v["passed"]]
    print(f"=== CONTROL {name} rev={rev[:12]} census_exit={census_exit} conditions_passed={data['conditions_passed']}/8 exit={data['exit']}")
    print(f"    pass: {passed}")
    print(f"    fail: {failed}")
    for k in failed:
        for n in data["checks"][k]["notes"][:6]:
            print(f"      {k}: {n[:180]}")
    with open(f"/fast/scratch/hyaku/kake-r58/ExecC3BaseControls/score-{name}.json", "w", encoding="utf-8") as fh:
        fh.write(out.stdout)


REAL = {
    "S423": ["方式二：双向DNS解析认证", "也叫百度蜘蛛", "访问互联网上的网页，建立索引数据库"],
    "S424": ["常见的封禁行为包括robots封禁、封禁百度UA、封禁百度IP等。",
             "如何验证网站和智能小程序是否存在封禁百度蜘蛛的情况？",
             "注：正常返回码是200，其他情况为异常。"],
}
GATE_REAL = {
    "S423": ["方式二：双向DNS解析认证", "也叫百度蜘蛛"],
    "S424": ["如何验证网站和智能小程序是否存在封禁百度蜘蛛的情况？",
             "常见的封禁行为包括robots封禁、封禁百度UA、封禁百度IP等。"],
}
NAV = {"S423": ["搜索学堂", "推荐阅读", "百度蜘蛛"], "S424": ["搜索学堂", "推荐阅读", "百度蜘蛛"]}
GATE_NAV = {"S423": ["百度蜘蛛"], "S424": ["百度蜘蛛"]}
TITLE = {"S423": ["搜索问答剧场 【五】“百度蜘蛛”全面解析"],
         "S424": ["开发者如何解除封禁百度蜘蛛"]}
PROMO = {"S423": ["——什么是【搜索问答剧场】？", "《开发者如何解除封禁百度蜘蛛》",
                  "定期为开发者运营过程中产生的疑惑问题进行梳理解答，"],
         "S424": REAL["S424"]}
GATE_PROMO = {"S423": ["——什么是【搜索问答剧场】？", "《开发者如何解除封禁百度蜘蛛》"],
              "S424": GATE_REAL["S424"]}
CEIL = {"S423": REAL["S423"][:2] + ["，需要查看防火墙配置系统后台，检查是否存在百度蜘蛛的IP级别封禁措施。"],
        "S424": REAL["S424"][:2] + ["Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko)Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)"]}

if __name__ == "__main__":
    for q in (REAL, NAV, TITLE, PROMO):
        for sid in ("S423", "S424"):
            for span in q[sid]:
                assert units(span) <= 25 and len(span) <= 40, (sid, span, units(span), len(span))
    build("scaffold", REAL, GATE_REAL, prose="Scaffold control: shallow prose, three real quotes.")
    build("a-nav", NAV, GATE_NAV, prose="Nav/sidebar text only.")
    build("b-title", TITLE, TITLE, prose="Page title only.")
    build("c-usedby", REAL, GATE_REAL, used_by={"S423": ENTRY["S424"], "S424": ENTRY["S423"]},
          prose="Used-by swapped.")
    build("d-root", REAL, GATE_REAL, argv_mode="root", prose="Validate receipt produced with --root.")
    build("d-mislabel", REAL, GATE_REAL, argv_mode="mislabel",
          prose="Validate run with --root, argv labelled --file.")
    build("e-promo", PROMO, GATE_PROMO, prose="Promo/cross-link boilerplate quotes.")
    build("f-swap", {"S423": REAL["S424"], "S424": REAL["S423"]},
          {"S423": GATE_REAL["S424"], "S424": GATE_REAL["S423"]},
          prose="Entry bodies swapped between the two ids.")
    build("h-mirror", REAL, GATE_REAL, mirror_rows=True,
          prose="Pre-append mirror edited to carry the new rows.")
    build("i-repeat", {"S423": [REAL["S423"][0]] * 3, "S424": [REAL["S424"][0]] * 3}, GATE_REAL,
          prose="One span quoted three times.")
    build("j-ceiling", CEIL, GATE_REAL, prose="Spans over the unit/character ceilings.")
