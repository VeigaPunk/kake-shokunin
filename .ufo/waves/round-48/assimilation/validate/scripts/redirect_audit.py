#!/usr/bin/env python3
"""Offline static-host redirect/rewrite expectation audit (round 46, C1).

Reads a version-1 manifest of static-host redirect/rewrite checks and reports,
read-only and network-free, every check whose decided outcome differs from its
independently authored expectation.

Semantics contract v1 (grounded in corpus/knowledge/redirect-rewrite-rules.md;
S050 Render Docs, S135 Cloudflare Pages docs, opened 2026-10-24):

  decision(host fields, rules, resources, requestPath):
    1. path = percent-decode(requestPath)  (UTF-8; '+' stays literal in paths)
    2. if resourcePrecedence and path in resources -> decided {"action":"serve"}
    3. first rule, in listed order, whose source pattern matches path ->
       decided redirect {"action":"redirect","status":S,"location":dest'}
       or rewrite {"action":"rewrite","destination":dest'}
       (dest' = splat/placeholder substitution; S = rule status or defaultStatus)
    4. else if not resourcePrecedence and path in resources -> {"action":"serve"}
    5. else -> {"action":"none"}  (the host's 404)

  Source pattern: '/' matches '/'; '*', when terminal, matches any suffix;
  ':name' matches one path component. Any other '*' placement or a source not
  starting with '/' is a malformed rule. Redirect status must be one of
  301/302/303/307/308; anything else is a malformed rule.

The manifest supplies both the rules under test and the expectations; the
expectations are authored independently of the rules (a check states the
request and the outcome the publisher intends, not the outcome the rules
happen to produce), which is what keeps the audit from being tautological.

Exit map (lane convention): 0 clean, 1 failed-policy (findings), 2
could-not-evaluate (input), 64 usage. No network, no writes outside an
optional --json report path.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse

EXIT_CLEAN = 0
EXIT_POLICY = 1
EXIT_INPUT = 2
EXIT_USAGE = 64

REDIRECT_STATUSES = {301, 302, 303, 307, 308}


class UsageError(Exception):
    """Invalid command-line shape."""


class InputError(Exception):
    """Manifest population cannot be evaluated."""


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


def parse_cli(argv: list[str]) -> argparse.Namespace:
    parser = ArgumentParser(
        prog="redirect_audit.py",
        usage="redirect_audit.py --manifest PATH [--root PATH] [--json [PATH]]",
        allow_abbrev=False,
        description="Offline static-host redirect/rewrite expectation audit.",
    )
    parser.add_argument("--manifest", required=True, metavar="PATH")
    parser.add_argument("--root", default=".", metavar="PATH")
    parser.add_argument("--json", nargs="?", const="-", metavar="PATH")
    parser.add_argument("--selftest", action="store_true")
    if sum(t == "--manifest" or t.startswith("--manifest=") for t in argv) > 1:
        raise UsageError("--manifest given more than once")
    if "--selftest" in argv and any(t.startswith("--manifest") for t in argv):
        raise UsageError("--selftest takes no --manifest")
    return parser.parse_args(argv)


# --------------------------------------------------------------------------
# Semantics core (pure; mutated by the round-46 selftest as in-memory variants)


class Rule:
    __slots__ = ("source", "destination", "action", "status", "order")

    def __init__(self, raw: dict, order: int) -> None:
        self.order = order
        self.source = raw.get("source")
        self.destination = raw.get("destination")
        self.action = raw.get("action")
        self.status = raw.get("status")

    def malformed_reason(self) -> str | None:
        if not isinstance(self.source, str) or not self.source.startswith("/"):
            return "source_not_path"
        if "*" in self.source and not self.source.endswith("*"):
            return "wildcard_not_terminal"
        if not isinstance(self.destination, str) or not self.destination:
            return "destination_missing"
        if self.action not in ("redirect", "rewrite"):
            return "action_unknown"
        if self.action == "redirect":
            status = self.status
            if status is None:
                return None
            if not isinstance(status, int) or isinstance(status, bool):
                return "status_not_integer"
            if status not in REDIRECT_STATUSES:
                return "status_not_redirect"
        else:
            if self.status is not None:
                return "rewrite_has_status"
        return None


def _match_source(source: str, path: str) -> dict[str, str] | None:
    """Match a v1 source pattern against a decoded path.

    Returns {"splat": str|None, **placeholders} on match, else None.
    """
    if source == "/":
        return {"splat": None} if path == "/" else None
    if "*" in source:
        stem = source[:-1]
        if path.startswith(stem):
            return {"splat": path[len(stem):]}
        return None
    # placeholder/exact matching, component-wise
    s_parts = [p for p in source.split("/") if p != ""]
    p_parts = [p for p in path.split("/") if p != ""]
    if source.endswith("/") and not path.endswith("/"):
        return None
    if len(s_parts) != len(p_parts):
        return None
    captured: dict[str, str] = {"splat": None}
    for s_part, p_part in zip(s_parts, p_parts):
        if s_part.startswith(":"):
            if p_part == "":
                return None
            captured[s_part[1:]] = p_part
        elif s_part != p_part:
            return None
    return captured


def _expand_destination(destination: str, captured: dict[str, str]) -> str:
    out = destination
    splat = captured.get("splat")
    if splat is not None:
        out = out.replace("*", splat).replace(":splat", splat)
    for name, value in captured.items():
        if name != "splat":
            out = out.replace(":" + name, value)
    return out


def decide(
    manifest: dict,
    rules: list[Rule],
    request_path: str,
    *,
    check_status: bool = True,
    first_match: bool = True,
    resource_precedence: bool | None = None,
    reject_malformed: bool = True,
    url_decode: bool = True,
) -> dict:
    """Decide the outcome for one request path under the v1 semantics."""
    path = urllib.parse.unquote(request_path, encoding="utf-8", errors="replace") if url_decode else request_path
    resources = manifest.get("resources") or []
    if resource_precedence is None:
        resource_precedence = bool(manifest.get("resourcePrecedence", True))
    default_status = manifest.get("defaultStatus", 301)

    if resource_precedence and path in resources:
        return {"action": "serve"}

    candidates = rules
    ordered = candidates if first_match else list(reversed(candidates))
    for rule in ordered:
        malformed = rule.malformed_reason()
        if malformed is not None:
            if reject_malformed:
                if _match_source(rule.source if isinstance(rule.source, str) else "", path) is not None:
                    return {"action": "malformed_rule", "reason": malformed, "rule": rule.order}
                continue
        captured = _match_source(rule.source, path) if isinstance(rule.source, str) else None
        if captured is None:
            continue
        destination = _expand_destination(rule.destination, captured)
        if rule.action == "redirect":
            if not check_status:
                status = default_status
            else:
                status = rule.status if rule.status is not None else default_status
            return {"action": "redirect", "status": status, "location": destination}
        return {"action": "rewrite", "destination": destination}

    if not resource_precedence and path in resources:
        return {"action": "serve"}
    return {"action": "none"}


# --------------------------------------------------------------------------
# Manifest handling


def load_manifest(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            manifest = json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise InputError(f"cannot read manifest: {exc}") from exc
    if not isinstance(manifest, dict) or manifest.get("version") != 1:
        raise InputError("manifest must be a version-1 object")
    for key in ("resourcePrecedence", "defaultStatus", "rules", "checks"):
        if key not in manifest:
            raise InputError(f"manifest missing required key: {key}")
    if not isinstance(manifest["rules"], list) or not isinstance(manifest["checks"], list):
        raise InputError("manifest rules/checks must be arrays")
    if manifest.get("resources") is not None and not isinstance(manifest["resources"], list):
        raise InputError("manifest resources must be an array when present")
    if not isinstance(manifest["resourcePrecedence"], bool):
        raise InputError("manifest resourcePrecedence must be a boolean")
    if not isinstance(manifest["defaultStatus"], int) or isinstance(manifest["defaultStatus"], bool) \
            or manifest["defaultStatus"] not in REDIRECT_STATUSES:
        raise InputError("manifest defaultStatus must be one of 301/302/303/307/308")
    return manifest


def evaluate(manifest: dict) -> list[dict]:
    rules = []
    for order, raw in enumerate(manifest["rules"]):
        if not isinstance(raw, dict):
            raise InputError(f"rule {order} is not an object")
        rules.append(Rule(raw, order))
    findings = []
    for check in manifest["checks"]:
        if not isinstance(check, dict) or not isinstance(check.get("id"), str) \
                or not isinstance(check.get("path"), str) or not isinstance(check.get("expect"), dict):
            raise InputError("each check needs id, path, expect")
        decided = decide(manifest, rules, check["path"])
        if decided != check["expect"]:
            findings.append({
                "check": check["id"],
                "path": check["path"],
                "expected": check["expect"],
                "decided": decided,
                "reason": "outcome_mismatch" if decided.get("action") != "malformed_rule" else "malformed_rule",
            })
    return findings


def run_audit(manifest_path: str) -> tuple[int, dict]:
    try:
        manifest = load_manifest(manifest_path)
    except InputError as exc:
        return EXIT_INPUT, {"version": 1, "verdict": "could-not-evaluate",
                            "checksEvaluated": 0, "findings": [{"check": None, "reason": str(exc)}]}
    try:
        findings = evaluate(manifest)
    except InputError as exc:
        return EXIT_INPUT, {"version": 1, "verdict": "could-not-evaluate",
                            "checksEvaluated": 0, "findings": [{"check": None, "reason": str(exc)}]}
    report = {
        "version": 1,
        "verdict": "failed-policy" if findings else "clean",
        "checksEvaluated": len(manifest["checks"]),
        "findings": findings,
    }
    return (EXIT_POLICY if findings else EXIT_CLEAN), report


# --------------------------------------------------------------------------
# Selftest: planted witness classes + differential mutant kills. Hermetic:
# fixtures live in memory and under a temporary directory; nothing is written
# into the repo. Isolation shape (per QUALITY.md shape-only rule): HOME and
# scratch dirs are mktemp-generated; values are never printed.


def _w(case_id: str, source: str, destination: str, action: str = "redirect",
       status: int | None = 301) -> dict:
    rule = {"source": source, "destination": destination, "action": action}
    if status is not None:
        rule["status"] = status
    return rule


def _manifest(rules: list[dict], checks: list[dict], resources: list[str] | None = None,
              precedence: bool = True, default: int = 301) -> dict:
    manifest = {
        "version": 1,
        "resourcePrecedence": precedence,
        "defaultStatus": default,
        "rules": rules,
        "checks": checks,
    }
    if resources is not None:
        manifest["resources"] = resources
    return manifest


def _check(cid: str, path: str, expect: dict) -> dict:
    return {"id": cid, "path": path, "expect": expect}


# Each FLAG witness models a real publisher failure: the manifest's expect is
# the outcome the publisher intends; the rules+resources are the defective
# world; the committed semantics must decide something different (a finding).
# Each CLEAN case is a correct rules+expect pair the committed semantics must
# NOT flag; per-mutant blindness is proven against the paired case.
def _witnesses() -> list[tuple[str, dict, str, str]]:
    flag_cases: list[tuple[str, dict, str, str]] = []

    # W1 shadowed specific redirect: a resource exists at the redirected path,
    # so the rule never fires and visitors keep the old content. The publisher
    # intended the redirect; the resource presence defeats it.
    flag_cases.append((
        "w1_shadowed_redirect", "flag",
        _manifest([_w("r1", "/old", "/new")],
                  [_check("c1", "/old", {"action": "redirect", "status": 301, "location": "/new"})],
                  resources=["/old"]),
        "c1",
    ))

    # W2 SPA fallback rewrite listed before the specific legacy redirect:
    # first match wins, so the legacy redirect never fires.
    flag_cases.append((
        "w2_first_match_shadow", "flag",
        _manifest([_w("r1", "/*", "/index.html", action="rewrite", status=None),
                   _w("r2", "/legacy", "/modern")],
                  [_check("c1", "/legacy",
                          {"action": "redirect", "status": 301, "location": "/modern"})]),
        "c1",
    ))

    # W3 redirect vs rewrite confusion: expectation says redirect to a new
    # URL, rule rewrites internally (browser stays at the wrong URL).
    flag_cases.append((
        "w3_redirect_vs_rewrite", "flag",
        _manifest([_w("r1", "/docs", "/docs/", action="rewrite", status=None)],
                  [_check("c1", "/docs", {"action": "redirect", "status": 301, "location": "/docs/"})]),
        "c1",
    ))

    # W4 wrong destination: splat substituted to the wrong host path.
    flag_cases.append((
        "w4_splat_destination", "flag",
        _manifest([_w("r1", "/blog/*", "https://blog.example.com/:splat")],
                  [_check("c1", "/blog/a/b",
                          {"action": "redirect", "status": 301,
                           "location": "https://blog.example.com/a/b/c"})]),
        "c1",
    ))

    # W5 wrong status: rule says 302, expectation 301.
    flag_cases.append((
        "w5_status_mismatch", "flag",
        _manifest([_w("r1", "/a", "/b", status=302)],
                  [_check("c1", "/a", {"action": "redirect", "status": 301, "location": "/b"})]),
        "c1",
    ))

    # W7 placeholder capture written in the wrong order by the publisher.
    flag_cases.append((
        "w7_placeholders", "flag",
        _manifest([_w("r1", "/updates/:month/:year", "/changelog/:year/:month")],
                  [_check("c1", "/updates/03/2024",
                          {"action": "redirect", "status": 301, "location": "/changelog/03/2024"})]),
        "c1",
    ))

    # W8 no rule and no resource -> none (404); the publisher expected a serve.
    flag_cases.append((
        "w8_unmatched_none", "flag",
        _manifest([_w("r1", "/a", "/b")],
                  [_check("c1", "/missing", {"action": "serve"})],
                  resources=["/index.html"]),
        "c1",
    ))

    # W9 cloudflare semantics: the publisher expected the asset to be served,
    # but a redirect rule fires even though the asset exists.
    flag_cases.append((
        "w9_no_resource_precedence", "flag",
        _manifest([_w("r1", "/home", "/", status=301)],
                  [_check("c1", "/home", {"action": "serve"})],
                  resources=["/home"], precedence=False),
        "c1",
    ))

    # W10 default status: rule omits status, manifest default 302, expectation 301.
    flag_cases.append((
        "w10_default_status", "flag",
        _manifest([_w("r1", "/a", "/b", status=None)],
                  [_check("c1", "/a", {"action": "redirect", "status": 301, "location": "/b"})],
                  default=302),
        "c1",
    ))

    # W11 malformed rule shape (wildcard mid-pattern) matched by the request.
    flag_cases.append((
        "w11_malformed_rule", "flag",
        _manifest([_w("r1", "/a/*/b", "/x")],
                  [_check("c1", "/a/1/b", {"action": "redirect", "status": 301, "location": "/x"})]),
        "c1",
    ))

    # W12 malformed status (200 is not a redirect status).
    flag_cases.append((
        "w12_malformed_status", "flag",
        _manifest([_w("r1", "/a", "/b", status=200)],
                  [_check("c1", "/a", {"action": "redirect", "status": 200, "location": "/b"})]),
        "c1",
    ))

    clean_cases: list[tuple[str, dict, str, str]] = []

    # C6 url-encoded request path must match the decoded source: the rule is
    # correct, so the committed semantics must NOT flag it.
    clean_cases.append((
        "c6_encoded_path", "clean",
        _manifest([_w("r1", "/old page", "/new")],
                  [_check("c1", "/old%20page", {"action": "redirect", "status": 301, "location": "/new"})]),
        "c1",
    ))

    # C7 correct placeholder reorder must not flag.
    clean_cases.append((
        "c7_placeholders_correct", "clean",
        _manifest([_w("r1", "/updates/:month/:year", "/changelog/:year/:month")],
                  [_check("c1", "/updates/03/2024",
                          {"action": "redirect", "status": 301, "location": "/changelog/2024/03"})]),
        "c1",
    ))

    # C8 first match with the specific rule listed first: correct.
    clean_cases.append((
        "c8_first_match_correct", "clean",
        _manifest([_w("r1", "/legacy", "/modern"),
                   _w("r2", "/*", "/index.html", action="rewrite", status=None)],
                  [_check("c1", "/legacy", {"action": "redirect", "status": 301, "location": "/modern"}),
                   _check("c2", "/other", {"action": "rewrite", "destination": "/index.html"})]),
        "c1",
    ))

    return flag_cases + clean_cases


def _mutants() -> dict[str, dict]:
    """In-memory mutant decision-knob settings; each must diverge on its witness."""
    return {
        "drop_status_check": {"check_status": False},
        "drop_first_match": {"first_match": False},
        "drop_resource_precedence": {"resource_precedence": False},
        "accept_malformed_rules": {"reject_malformed": False},
        "always_clean": {},   # special-cased: report no findings regardless
        "skip_url_decoding": {"url_decode": False},
    }


def selftest() -> int:
    import tempfile

    failures: list[str] = []
    passed: list[str] = []

    cases = _witnesses()
    flag_cases = [(n, m, c) for n, kind, m, c in cases if kind == "flag"]
    clean_cases = [(n, m, c) for n, kind, m, c in cases if kind == "clean"]
    by_name = {n: (m, c) for n, _, m, c in cases}

    with tempfile.TemporaryDirectory(prefix="kake-r46-redirect-") as tmp:
        # --- FLAG witnesses: committed semantics must catch every planted case
        for name, manifest, check_id in flag_cases:
            if not _would_flag(manifest, check_id):
                failures.append(f"{name}: committed semantics missed the planted witness")
            else:
                passed.append(f"{name} flagged")

        # --- CLEAN cases: committed semantics must NOT flag a correct world
        for name, manifest, check_id in clean_cases:
            if _would_flag(manifest, check_id):
                failures.append(f"{name}: committed semantics false-positived a correct world")
            else:
                passed.append(f"{name} clean")

        # --- mutants: each must diverge from committed on its paired case.
        # Direction "flag": committed flags the FLAG case, the mutant misses it.
        # Direction "clean": committed passes the CLEAN case, the mutant flags it.
        mutant_pair = {
            "drop_status_check": ("flag", "w5_status_mismatch"),
            "drop_first_match": ("flag", "w2_first_match_shadow"),
            "drop_resource_precedence": ("flag", "w1_shadowed_redirect"),
            "accept_malformed_rules": ("flag", "w12_malformed_status"),
            "skip_url_decoding": ("clean", "c6_encoded_path"),
        }
        for mutant, knobs in _mutants().items():
            if mutant == "always_clean":
                blind = [name for name, _, _ in flag_cases if not _would_flag(*by_name[name])]
                if blind:
                    failures.append(f"mutant always_clean: unexpectedly blind list nonempty {blind}")
                else:
                    passed.append("mutant always_clean blind to all flag witnesses")
                continue
            direction, witness_name = mutant_pair[mutant]
            mutant_flags = _would_flag(*by_name[witness_name], **knobs)
            if direction == "flag" and mutant_flags:
                failures.append(f"mutant {mutant}: still flags {witness_name} (not a kill)")
            elif direction == "clean" and not mutant_flags:
                failures.append(f"mutant {mutant}: passes {witness_name} like committed (not a kill)")
            else:
                passed.append(f"mutant {mutant} killed on {witness_name}")

        # --- end-to-end CLI runs over temp manifests (positive + negative)
        import os
        import subprocess
        import sys as _sys

        audit = os.path.join(os.path.dirname(os.path.abspath(__file__)), "redirect_audit.py")

        def run_cli(manifest: dict) -> tuple[int, dict]:
            path = os.path.join(tmp, "m.json")
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(manifest, handle)
            proc = subprocess.run(
                [_sys.executable, "-B", audit, "--manifest", path],
                capture_output=True, text=True, timeout=60,
            )
            if proc.returncode not in (0, 1, 2):
                raise RuntimeError(f"cli crash exit {proc.returncode}: {proc.stderr[:200]}")
            return proc.returncode, json.loads(proc.stdout)

        dirty = _manifest([_w("r1", "/a", "/b", status=302)],
                          [_check("c1", "/a", {"action": "redirect", "status": 301, "location": "/b"})])
        code, report = run_cli(dirty)
        if code != 1 or report["verdict"] != "failed-policy" or len(report["findings"]) != 1:
            failures.append(f"cli positive control: code={code} verdict={report.get('verdict')}")
        else:
            passed.append("cli positive control (exit 1, one finding)")

        clean_manifest = _manifest([_w("r1", "/a", "/b")],
                                   [_check("c1", "/a", {"action": "redirect", "status": 301, "location": "/b"})])
        code, report = run_cli(clean_manifest)
        if code != 0 or report["verdict"] != "clean":
            failures.append(f"cli negative control: code={code} verdict={report.get('verdict')}")
        else:
            passed.append("cli negative control (exit 0, clean)")

        bad_input = os.path.join(tmp, "bad.json")
        with open(bad_input, "w", encoding="utf-8") as handle:
            handle.write("{not json")
        proc = subprocess.run([_sys.executable, "-B", audit, "--manifest", bad_input],
                              capture_output=True, text=True, timeout=60)
        if proc.returncode != 2:
            failures.append(f"cli bad input: exit {proc.returncode} != 2")
        else:
            passed.append("cli bad input (exit 2)")

    print("redirect_audit --selftest")
    for name in passed:
        print(f"  PASS  {name}")
    if failures:
        for name in failures:
            print(f"  FAIL  {name}")
        print(f"selftest: {len(passed)}/{len(passed) + len(failures)} passed")
        return 1
    print(f"selftest: {len(passed)}/{len(passed)} passed")
    return 0


def _would_flag(manifest: dict, check_id: str, **knobs) -> bool:
    """True if a decide() variant with `knobs` reports the check (finds the witness)."""
    rules = [Rule(raw, i) for i, raw in enumerate(manifest["rules"])]
    check = next(c for c in manifest["checks"] if c["id"] == check_id)
    decided = decide(manifest, rules, check["path"], **knobs)
    return decided != check["expect"]


def main(argv: list[str] | None = None) -> int:
    args_list = sys.argv[1:] if argv is None else argv
    if "--selftest" in args_list:
        return selftest()
    try:
        args = parse_cli(args_list)
    except UsageError as exc:
        print(f"redirect_audit.py: {exc}", file=sys.stderr)
        return EXIT_USAGE

    exit_code, report = run_audit(args.manifest)
    encoded = json.dumps(report, sort_keys=True, separators=(",", ":"))
    if args.json is None or args.json == "-":
        print(encoded)
    else:
        try:
            with open(args.json, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(encoded + "\n")
        except OSError as exc:
            print(f"redirect_audit.py: cannot write JSON output: {exc}", file=sys.stderr)
            return EXIT_INPUT
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
