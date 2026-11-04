#!/usr/bin/env python3
"""Generate the ExecAuditRealRun receipts by running each command and capturing
its verbatim stdout/stderr/exit. Nothing is hand-transcribed.

argv[1] = wave receipts dir. Writes only there plus its own scratch.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/kake-r76/ExecAuditRealRun"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
LIVE = os.path.join(LANE, ".ufo/waves/round-23/live")
WAVE = os.path.join(LANE, ".ufo/waves/round-76/w1/ExecAuditRealRun")
RECEIPTS = sys.argv[1]
TOOL = os.environ.get("KAKE_TOOL", os.path.join(LANE, ".ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py"))
REF = os.path.join(S, "ref/hreflang_audit.py")
MANIFEST = os.path.join(WAVE, "real-manifest.json")
CANON_MANIFEST = os.path.join(S, "mirror/canon-manifest.json")
MIRROR = os.path.join(S, "mirror")
WORK = os.path.join(S, "work")
WORK_TOOL = os.path.join(S, "work-tool")
TMP = os.path.join(S, "tmp")
ENV = dict(os.environ, TMPDIR=TMP, PYTHONDONTWRITEBYTECODE="1")
PY = sys.executable

SURFACES = [
    "burnerchrome-kimi",
    "charter-ghp",
    "ds4cc-kimi",
    "ds4cc-primary",
    "lucario-ghp",
    "plazir15-ghp",
    "ufo-fsd-kimi-pro",
    "vault-index-kimi",
]
NOT_RETAINED = ["charter-kimi", "lucario-kimi", "plazir15-kimi", "plazir27-kimi"]

PROBES = [
    {
        "name": "p1_relative_href_not_resolved",
        "files": {"a.html": '<html><head><link rel="canonical" href="/p/">'
                            '<link rel="alternate" hreflang="en" href="/p/"></head></html>'},
        "version": 1,
        "pages": [{"id": "a", "file": "a.html", "url": "https://a.test/p/"}],
    },
    {
        "name": "p2_missing_hreflang_value",
        "files": {"a.html": '<html><head><link rel="alternate" href="https://a.test/p/"></head></html>'},
        "version": 1,
        "pages": [{"id": "a", "file": "a.html", "url": "https://a.test/p/"}],
    },
    {
        "name": "p3_two_xdefault_same_href",
        "files": {"a.html": '<html><head><link rel="alternate" hreflang="x-default" href="https://a.test/p/">'
                            '<link rel="alternate" hreflang="X-Default" href="https://a.test/p/"></head></html>'},
        "version": 1,
        "pages": [{"id": "a", "file": "a.html", "url": "https://a.test/p/"}],
    },
    {
        "name": "p4_canonical_not_self",
        "files": {"a.html": '<html><head><link rel="canonical" href="https://a.test/other/">'
                            '<link rel="alternate" hreflang="en" href="https://a.test/p/"></head></html>'},
        "version": 1,
        "pages": [{"id": "a", "file": "a.html", "url": "https://a.test/p/"}],
    },
    {
        "name": "p5_absent_canonical_is_self",
        "files": {"a.html": '<html><head><link rel="alternate" hreflang="en" href="https://b.test/"></head></html>',
                  "b.html": '<html><head><link rel="alternate" hreflang="en" href="https://a.test/p/"></head></html>'},
        "version": 1,
        "pages": [{"id": "a", "file": "a.html", "url": "https://a.test/p/"},
                  {"id": "b", "file": "b.html", "url": "https://b.test/"}],
    },
    {
        "name": "p6_first_canonical_wins",
        "files": {"a.html": '<html><head><link rel="canonical" href="https://a.test/p/">'
                            '<link rel="canonical" href="https://a.test/other/">'
                            '<link rel="alternate" hreflang="en" href="https://a.test/p/"></head></html>'},
        "version": 1,
        "pages": [{"id": "a", "file": "a.html", "url": "https://a.test/p/"}],
    },
    {
        "name": "p7_link_without_href",
        "files": {"a.html": '<html><head><link rel="alternate" hreflang="en"></head></html>'},
        "version": 1,
        "pages": [{"id": "a", "file": "a.html", "url": "https://a.test/p/"}],
    },
    {
        "name": "p8_stylesheet_alternate_pair",
        "files": {"a.html": '<html><head><link rel="stylesheet alternate" hreflang="en_US" href="/x"></head></html>'},
        "version": 1,
        "pages": [{"id": "a", "file": "a.html", "url": "https://a.test/p/"}],
    },
    {
        "name": "p9_noscript_scanned",
        "files": {"a.html": '<html><head><noscript><link rel="alternate" hreflang="en_US" '
                            'href="https://a.test/p/"></noscript></head></html>'},
        "version": 1,
        "pages": [{"id": "a", "file": "a.html", "url": "https://a.test/p/"}],
    },
    {
        "name": "p10_manifest_version_2",
        "files": {"a.html": '<html><head></head></html>'},
        "version": 2,
        "pages": [{"id": "a", "file": "a.html", "url": "https://a.test/p/"}],
    },
    {
        "name": "p11_duplicate_file_two_pages",
        "files": {"a.html": '<html><head></head></html>'},
        "version": 1,
        "pages": [{"id": "a", "file": "a.html", "url": "https://a.test/p/"},
                  {"id": "b", "file": "a.html", "url": "https://b.test/"}],
    },
]


def emit(name: str, header: str, out: str, err: str, code: int) -> None:
    path = os.path.join(RECEIPTS, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"$ {header}\n")
        fh.write(f"exit={code}\n")
        if out:
            fh.write("--- stdout\n")
            fh.write(out if out.endswith("\n") else out + "\n")
        if err:
            fh.write("--- stderr\n")
            fh.write(err if err.endswith("\n") else err + "\n")


def call(name: str, argv: list[str], cwd: str | None = None) -> tuple[int, str, str]:
    proc = subprocess.run(argv, cwd=cwd, env=ENV, capture_output=True, text=True)
    header = " ".join(argv)
    if cwd:
        header = f"(cd {cwd} && {header})"
    emit(name, header, proc.stdout, proc.stderr, proc.returncode)
    return proc.returncode, proc.stdout, proc.stderr


def sha_check() -> str:
    rows = ["# retained-byte verification: page.html sha256 vs round-23 fetch.json sha256"]
    rows.append("id                   bytes  status  match  fetch_sha256")
    for d in SURFACES:
        page = os.path.join(LIVE, d, "page.html")
        fetch = json.load(open(os.path.join(LIVE, d, "fetch.json")))
        raw = open(page, "rb").read()
        got = hashlib.sha256(raw).hexdigest()
        rows.append(
            f"{d:20s} {len(raw):6d} {fetch['status']:6d} {str(got == fetch['sha256']).lower():5s} {fetch['sha256']}"
        )
    for d in NOT_RETAINED:
        fetch = json.load(open(os.path.join(LIVE, d, "fetch.json")))
        has = os.path.isfile(os.path.join(LIVE, d, "page.html"))
        rows.append(
            f"{d:20s} {'-':>6s} {fetch['status']:6d} {'n/a':5s} {fetch['sha256']}  page_html_present={str(has).lower()}"
        )
    return "\n".join(rows) + "\n"


def load_ref():
    spec = importlib.util.spec_from_file_location("hrefref", REF)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def declarations(module) -> str:
    out = [
        "# per-page declarations read from retained bytes (reference scanner == the",
        "# same parse the reference auditor uses; raw-regex counts in raw-scan.txt",
        "# are an independent check of these totals)",
    ]
    alts = 0
    canons = 0
    for d in SURFACES:
        raw = open(os.path.join(LIVE, d, "page.html"), "rb").read()
        decl = module.Declarations(raw)
        out.append(f"{d} link_declarations={len(decl.alternates) + len(decl.canonicals)}")
        for alt in decl.alternates:
            tag = alt.get("hreflang")
            href = alt.get("href")
            alts += 1
            verdict = "valid_tag" if tag is not None and module.valid_tag(module.tidy(tag)) else "invalid_or_absent_tag"
            out.append(f"{d} alternate hreflang={json.dumps(tag)} href={json.dumps(href)} {verdict}")
        for href in decl.canonicals:
            canons += 1
            out.append(f"{d} canonical href={json.dumps(href)}")
    out.append(f"TOTAL alternate_declarations={alts} canonical_declarations={canons}")
    return "\n".join(out) + "\n"


def crosscheck(href_stdout: str, canon_stdout: str, module) -> str:
    href = json.loads(href_stdout)
    canon = json.loads(canon_stdout)
    pages = json.load(open(MANIFEST))["pages"]
    canon_missing = {f["page"] for f in canon["findings"] if f["id"] == "canonical_missing"}
    canon_flagged = {f["page"] for f in canon["findings"]}
    rows = ["page                 scanner.says  canonical_audit.says  agree"]
    agree = 0
    for p in pages:
        raw = open(os.path.join(LIVE, p["id"], "page.html"), "rb").read()
        decl = module.Declarations(raw)
        mine = "declared" if decl.canonicals else "absent"
        theirs = "absent" if p["url"] in canon_missing else "declared"
        agree += int(mine == theirs)
        rows.append(f"{p['id']:20s} {mine:12s} {theirs:20s} {str(mine == theirs).lower()}")
    rows.append(f"AGREEMENT {agree}/{len(pages)} pages on whether rel=canonical is declared")
    rows.append(
        f"canonical_audit: pagesChecked={canon['pagesChecked']} verdict={canon['verdict']} "
        f"findings={len(canon['findings'])}"
    )
    rows.append(f"hreflang audit: pages={href['pages']} verdict={href['exit']} (exit) findings={len(href['findings'])}")
    rows.append(f"canonical_audit pages with any finding: {len(canon_flagged)}")
    return "\n".join(rows) + "\n"


def differential() -> str:
    base = os.path.join(S, "probe")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base, exist_ok=True)
    rows = ["# advisory differential probe (not a matrix case): inputs aimed at the",
            "# Amendment-2 decisions, run through both builds. No verdict is asserted."]
    agree = 0
    for probe in PROBES:
        for name, html in probe["files"].items():
            with open(os.path.join(base, name), "w", encoding="utf-8") as fh:
                fh.write(html)
        manifest = {"version": probe["version"], "pages": probe["pages"]}
        mpath = os.path.join(base, "manifest.json")
        with open(mpath, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh)
        runs = {}
        for label, tool_path, work in (("tool", TOOL, WORK_TOOL), ("ref", REF, WORK)):
            proc = subprocess.run(
                [PY, "-B", tool_path, "--manifest", mpath, "--root", base, "--json", "--work", work],
                env=ENV, capture_output=True, text=True,
            )
            ids = []
            try:
                payload = json.loads(proc.stdout)
                ids = sorted(f["id"] for f in payload.get("findings", []))
            except json.JSONDecodeError:
                ids = ["<unparseable>"]
            runs[label] = (proc.returncode, ids)
        same = runs["tool"] == runs["ref"]
        agree += int(same)
        rows.append(f"[{probe['name']}] agree={str(same).lower()}")
        rows.append(f"  tool exit={runs['tool'][0]} ids={runs['tool'][1]}")
        rows.append(f"  ref  exit={runs['ref'][0]} ids={runs['ref'][1]}")
    rows.append(f"AGREEMENT {agree}/{len(PROBES)} probes (exit code and id multiset)")
    return "\n".join(rows) + "\n"



def prepare_mirror() -> None:
    """canonical_audit.py resolves page files strictly relative to the manifest
    directory (no traversal, no symlinks, no absolute paths), so the retained
    pages are copied byte-for-byte into a scratch mirror and every copy is
    sha256-checked against its original before use."""
    shutil.rmtree(MIRROR, ignore_errors=True)
    for d in SURFACES:
        os.makedirs(os.path.join(MIRROR, "live", d), exist_ok=True)
        src = os.path.join(LIVE, d, "page.html")
        dst = os.path.join(MIRROR, "live", d, "page.html")
        shutil.copy2(src, dst)
        same = hashlib.sha256(open(src, "rb").read()).digest() == hashlib.sha256(open(dst, "rb").read()).digest()
        assert same, f"mirror copy differs for {d}"
    canon, href = [], []
    for d in SURFACES:
        first = json.load(open(os.path.join(LIVE, d, "manifest.json")))["pages"][0]
        canon.append({"url": first["url"], "file": f"live/{d}/page.html", "expectedCanonical": first["expectedCanonical"]})
        href.append({"id": d, "file": f"live/{d}/page.html", "url": first["url"]})
    with open(os.path.join(MIRROR, "canon-manifest.json"), "w", encoding="utf-8") as fh:
        json.dump({"version": 1, "pages": canon}, fh, indent=1, sort_keys=True)
    with open(os.path.join(MIRROR, "hreflang-mirror-manifest.json"), "w", encoding="utf-8") as fh:
        json.dump({"version": 1, "pages": href}, fh, indent=1, sort_keys=True)


def absent_surfaces() -> None:
    """Supplementary run over the four directories that retained no bytes, so the
    fault path is exercised on real paths instead of proving a silent skip."""
    pages = [dict(p) for p in json.load(open(MANIFEST))["pages"]]
    for d in NOT_RETAINED:
        fetch = json.load(open(os.path.join(LIVE, d, "fetch.json")))
        pages.append({"id": d, "file": f".ufo/waves/round-23/live/{d}/page.html", "url": fetch["finalUrl"]})
    manifest_path = os.path.join(WAVE, "absent-surfaces-manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump({"version": 1, "pages": pages}, fh, indent=1, sort_keys=True)
    call("absent-surfaces-run.txt",
         [PY, "-B", TOOL, "--manifest", manifest_path, "--root", LANE, "--json", "--work", WORK_TOOL])



def census() -> str:
    rows = [
        "# round-23 live/ census: every directory, whether bytes were retained, and the",
        "# declaration counts read from those bytes. No network is used or required.",
    ]
    dirs = sorted(d for d in os.listdir(LIVE) if os.path.isdir(os.path.join(LIVE, d)))
    retained = 0
    for d in dirs:
        base = os.path.join(LIVE, d)
        page = os.path.join(base, "page.html")
        man = os.path.join(base, "manifest.json")
        fetch = json.load(open(os.path.join(base, "fetch.json")))
        rows.append(
            f"[{d}] status={fetch['status']} bytes={fetch['bytes']} sha256={fetch['sha256']} "
            f"finalUrl={fetch['finalUrl']} fetchedAt={fetch['fetchedAt']}"
        )
        if os.path.isfile(man):
            first = json.load(open(man))["pages"][0]
            rows.append(f"  manifest.json url={first['url']} expectedCanonical={first['expectedCanonical']}")
        else:
            rows.append("  manifest.json ABSENT")
        if not os.path.isfile(page):
            rows.append("  page.html ABSENT (no retained bytes; not-served; excluded from the audit manifest)")
            continue
        retained += 1
        raw = open(page, "rb").read()
        low = raw.decode("utf-8", "replace").lower()
        canon_hits = low.count('rel="canonical"') + low.count("rel='canonical'")
        rows.append(
            f"  page.html bytes={len(raw)} sha256={hashlib.sha256(raw).hexdigest()} "
            f"fetch_match={str(hashlib.sha256(raw).hexdigest() == fetch['sha256']).lower()} "
            f"hreflang_occurrences={low.count('hreflang')} canonical_occurrences={canon_hits}"
        )
    rows.append(f"directories={len(dirs)} with_retained_page_html={retained} not_served={len(dirs) - retained}")
    return "\n".join(rows) + "\n"


def main() -> int:
    os.makedirs(RECEIPTS, exist_ok=True)
    for d in (TMP, WORK, WORK_TOOL):
        os.makedirs(d, exist_ok=True)
    prepare_mirror()
    with open(os.path.join(RECEIPTS, "sha256-check.txt"), "w", encoding="utf-8") as fh:
        fh.write(sha_check())
    with open(os.path.join(RECEIPTS, "census.txt"), "w", encoding="utf-8") as fh:
        fh.write(census())
    module = load_ref()
    with open(os.path.join(RECEIPTS, "declarations.txt"), "w", encoding="utf-8") as fh:
        fh.write(declarations(module))

    scan = subprocess.run([PY, "-B", os.path.join(S, "ref/scan.py")], env=ENV, capture_output=True, text=True)
    with open(os.path.join(RECEIPTS, "raw-scan.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"$ python3 -B ref/scan.py\nexit={scan.returncode}\n--- stdout\n{scan.stdout}")

    call("tool-selftest.txt", [PY, "-B", TOOL, "--selftest", "--work", WORK_TOOL])
    code, tool_out, _ = call(
        "real-input-run.txt",
        [PY, "-B", TOOL, "--manifest", MANIFEST, "--root", LANE, "--json", "--work", WORK_TOOL],
    )
    with open(os.path.join(RECEIPTS, "real-input-run.exit"), "w", encoding="utf-8") as fh:
        fh.write(f"{code}\n")

    call("ref-selftest.txt", [PY, "-B", REF, "--selftest", "--work", WORK])
    call(
        "ref-real-input-run.txt",
        [PY, "-B", REF, "--manifest", MANIFEST, "--root", LANE, "--json", "--work", WORK],
    )

    per = []
    for d in SURFACES:
        single = os.path.join(WORK, f"single-{d}.json")
        manifest = json.load(open(MANIFEST))
        manifest["pages"] = [p for p in manifest["pages"] if p["id"] == d]
        with open(single, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=1, sort_keys=True)
        proc = subprocess.run(
            [PY, "-B", TOOL, "--manifest", single, "--root", LANE, "--json", "--work", WORK_TOOL],
            env=ENV,
            capture_output=True,
            text=True,
        )
        per.append(f"{d} exit={proc.returncode} stdout={proc.stdout.strip()}")
    emit(
        "per-page.txt",
        "python3 -B ExecAuditTool/hreflang_audit.py --manifest <single-page manifest> --root <lane> --json  (one run per surface)",
        "\n".join(per),
        "",
        0,
    )

    call(
        "root-invariance.txt",
        [
            PY,
            "-B",
            TOOL,
            "--manifest",
            os.path.join(MIRROR, "hreflang-mirror-manifest.json"),
            "--root",
            MIRROR,
            "--json",
            "--work",
            WORK_TOOL,
        ],
    )
    _, canon_out, _ = call(
        "canonical-audit.txt",
        [PY, "-B", os.path.join(LANE, "scripts/canonical_audit.py"), "--manifest", CANON_MANIFEST, "--json"],
        cwd=MIRROR,
    )
    with open(os.path.join(RECEIPTS, "canonical-crosscheck.txt"), "w", encoding="utf-8") as fh:
        fh.write(crosscheck(tool_out, canon_out, module))
    absent_surfaces()
    with open(os.path.join(RECEIPTS, "differential-probe.txt"), "w", encoding="utf-8") as fh:
        fh.write(differential())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
