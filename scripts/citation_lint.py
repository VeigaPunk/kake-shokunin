#!/usr/bin/env python3
"""Commit-citation hygiene gate (round 46, C2).

Resolves every lane-commit citation over the frozen population
{SCORECARD.md, LOG.md} and reports each violation with file, line and token.
A violation is a hex token in a commit-citation context that does not resolve
to a git object in the lane repository. Contexts and exclusions are named
classes (each exercised by the selftest); tokens named in the committed
adjudication ledger (corpus/quality/citation-adjudications.md) are reported as
adjudicated, not violations.

Citation context: the token's line names a commit-bearing relation
(commit/base/revision/tip/HEAD/landed/hash/ancestor/parent). Excluded classes:
content digests (sha256/sha/digest on the line), beat/marker pins, external
repositories named on the same line (ufo-fsd-alpha, ds4cc-marketplace,
webzites, charter, lucario, marketplace upstream, fleet repo, sandbox runs),
and tokens glued to alphanumerics/UUID dashes or without a-f letters.

Exit map: 0 clean (no unadjudicated violations), 1 violations found,
2 could-not-evaluate, 64 usage.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

EXIT_CLEAN = 0
EXIT_VIOLATION = 1
EXIT_INPUT = 2
EXIT_USAGE = 64

POPULATION = ("SCORECARD.md", "LOG.md")
DEFAULT_ADJUDICATIONS = "corpus/quality/citation-adjudications.md"

TOKEN_RE = re.compile(r"(?<![0-9A-Za-z_-])([0-9a-f]{7,40})(?:…|\.\.\.)?(?![0-9A-Za-z_-])")
CONTEXT_RE = re.compile(
    r"\b(commit|commits|base|revision|tip|HEAD|landed|hash|ancestor|parent|merge-base)\b")
DIGEST_RE = re.compile(r"sha-?256|\bsha\b|digest", re.I)
PIN_RE = re.compile(r"\bbeat\b|marker|pinned|\bpin\b|sentinel|etag", re.I)
EXTERNAL_RE = re.compile(
    r"ufo-fsd-alpha|ds4cc-marketplace|plazir|webzites|charter|lucario|origin-work|"
    r"burnerchrome|marketplace|upstream|sandbox|fleet repo|spotcheck|render\.yaml", re.I)
ADJUDICATION_ROW_RE = re.compile(r"^\|\s*`([0-9a-f]{7,40})`\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")


class UsageError(Exception):
    pass


class InputError(Exception):
    pass


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


def parse_cli(argv: list[str]) -> argparse.Namespace:
    parser = ArgumentParser(
        prog="citation_lint.py",
        usage="citation_lint.py --root PATH [--revision REV] [--adjudications PATH] [--json [PATH]]",
        allow_abbrev=False,
    )
    parser.add_argument("--root", required=True, metavar="PATH")
    parser.add_argument("--revision", metavar="REV")
    parser.add_argument("--adjudications", default=DEFAULT_ADJUDICATIONS, metavar="PATH")
    parser.add_argument("--json", nargs="?", const="-", metavar="PATH")
    parser.add_argument("--selftest", action="store_true")
    if sum(t == "--root" or t.startswith("--root=") for t in argv) > 1:
        raise UsageError("--root given more than once")
    if "--selftest" in argv and any(t.startswith("--root") for t in argv):
        raise UsageError("--selftest takes no --root")
    return parser.parse_args(argv)


def read_population(root: str, revision: str | None) -> dict[str, list[str]]:
    files: dict[str, list[str]] = {}
    for rel in POPULATION:
        if revision:
            proc = subprocess.run(
                ["git", "-C", root, "show", f"{revision}:{rel}"],
                capture_output=True)
            if proc.returncode != 0:
                raise InputError(f"cannot read {rel} at {revision}")
            text = proc.stdout.decode("utf-8", "replace")
        else:
            try:
                with open(os.path.join(root, rel), "r", encoding="utf-8") as handle:
                    text = handle.read()
            except OSError as exc:
                raise InputError(f"cannot read {rel}: {exc}") from exc
        files[rel] = text.splitlines()
    return files


def load_adjudications(root: str, rel_path: str, revision: str | None) -> dict[tuple[str, str], str]:
    rows: dict[tuple[str, str], str] = {}
    text: str | None
    if revision:
        proc = subprocess.run(
            ["git", "-C", root, "show", f"{revision}:{rel_path}"],
            capture_output=True)
        if proc.returncode != 0:
            return rows  # no ledger at that revision: nothing is adjudicated
        text = proc.stdout.decode("utf-8", "replace")
    else:
        try:
            with open(os.path.join(root, rel_path), "r", encoding="utf-8") as handle:
                text = handle.read()
        except OSError:
            return rows
    for line in text.splitlines():
        match = ADJUDICATION_ROW_RE.match(line)
        if match:
            token, file_part, class_part, _reason = match.groups()
            rows[(token, file_part)] = class_part
    return rows


def resolves(root: str, token: str) -> bool:
    # `rev-parse -q --verify` answers "is this a well-formed object name", not
    # "does this object exist": a full-40-hex token that no object carries is
    # echoed back with exit 0 (git 2.56.0), so a dead 40-hex citation used to
    # pass this gate. A citation claims that a commit exists, so ask for
    # existence. Round-48 C2; the defect is recorded in
    # .ufo/waves/round-46/residual/CriticCitationOverreach.md, Finding 1.
    proc = subprocess.run(
        ["git", "-C", root, "cat-file", "-e", token],
        capture_output=True)
    return proc.returncode == 0


def scan(
    files: dict[str, list[str]],
    root: str,
    adjudications: dict[tuple[str, str], str],
    *,
    use_context: bool = True,
    use_digest_exclusion: bool = True,
    use_ellipsis_digest: bool = True,
    assume_resolves: bool = False,
) -> tuple[list[dict], list[dict]]:
    violations: list[dict] = []
    adjudicated: list[dict] = []
    for rel, lines in files.items():
        prev_line = ""
        for lineno, line in enumerate(lines, 1):
            context_line = line if CONTEXT_RE.search(line) else prev_line
            for match in TOKEN_RE.finditer(line):
                token = match.group(1)
                tail = line[match.end(1):]
                has_ellipsis = tail.startswith("…") or tail.startswith("...")
                if not re.search(r"[a-f]", token):
                    continue  # pure-digit number, not a hash
                if use_digest_exclusion and DIGEST_RE.search(line):
                    continue
                if use_ellipsis_digest and has_ellipsis and len(token) != 40:
                    continue  # content-digest / pin prefix, not a commit citation
                if PIN_RE.search(line):
                    continue
                if EXTERNAL_RE.search(line):
                    continue
                if use_context and not CONTEXT_RE.search(context_line):
                    continue
                key = (token, rel)
                if key in adjudications:
                    adjudicated.append({"file": rel, "line": lineno, "token": token,
                                        "class": adjudications[key]})
                    continue
                if not assume_resolves and resolves(root, token):
                    continue
                if assume_resolves:
                    continue  # mutant F: treats every citation as resolving (false green)
                violations.append({"file": rel, "line": lineno, "token": token,
                                   "reason": "dead_citation"})
            prev_line = line
    return violations, adjudicated


# --------------------------------------------------------------------------
# Selftest (hermetic: temp git repo + fixture population; nothing repo-written)


def selftest() -> int:
    import pathlib

    failures: list[str] = []
    passed: list[str] = []

    with tempfile.TemporaryDirectory(prefix="kake-r46-citelint-") as tmp:
        tmp_path = pathlib.Path(tmp)
        repo = tmp_path / "repo"
        repo.mkdir()
        env = dict(os.environ)
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True, env=env)
        subprocess.run(["git", "config", "user.email", "selftest@example.invalid"],
                       cwd=repo, check=True, env=env)
        subprocess.run(["git", "config", "user.name", "selftest"],
                       cwd=repo, check=True, env=env)
        (repo / "f.txt").write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "add", "f.txt"], cwd=repo, check=True, env=env)
        subprocess.run(["git", "commit", "-q", "-m", "base"], cwd=repo, check=True, env=env)
        good = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, check=True,
                              capture_output=True, env=env).stdout.decode().strip()
        dead = "e5455253"  # matches no object
        dead40 = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"  # full-40 dead token

        population = {
            "SCORECARD.md": [
                f"measured at commit `{good}` resolves",                    # resolving
                f"report cites commit `{dead}` (wave registry) which does not resolve",  # DEAD
                f"report cites commit `{dead40}` (full-40) which does not resolve",     # DEAD 40
                "counter sha256 `5cedaa3b` pins the revision bytes",           # digest exclusion (H)
                "strict check `5111264f…46ad` sets the revision",           # ellipsis digest (E)
                "beat `9c28d29` landed on the scribe remote",               # pin exclusion
                "chat `1a0acf59-4122-87ce` bound to the slot",              # UUID fragment
                "seed `43258815593301` used for the timing run",            # pure digits
                "the baseline6883f1d0 wording is compact",                  # alnum-glued
                "source6cb08's focused35/36 naming",                        # alnum-glued
                "scored 8 of 20 against the seat sandbox",                  # sandbox word, no ctx
                "sandbox commit `489714be` never entered the lane",         # external/sandbox
                "external `1fbdb8ed` named beside ds4cc-marketplace blobs", # external repo line
                "a plain hex token cafe012 sits in prose",                  # no context
            ],
            "LOG.md": [
                f"landed `{good}` on the lane branch",                      # resolving
                f"dead short-hash commit `{dead}` quoted from the closure",  # DEAD
                "gate check `f3c3171b…` observed at the tip",               # ellipsis digest (E)
            ],
        }
        files = {rel: list(lines) for rel, lines in population.items()}
        empty_adj: dict[tuple[str, str], str] = {}

        violations, adjudicated = scan(files, str(repo), empty_adj)
        flagged = {(v["file"], v["token"]) for v in violations}
        if ("SCORECARD.md", dead) not in flagged or ("LOG.md", dead) not in flagged:
            failures.append(f"committed gate missed planted dead citations: {flagged}")
        else:
            passed.append("planted dead citations flagged (2/2)")
        if ("SCORECARD.md", dead40) not in flagged:
            failures.append(f"committed gate missed the planted dead full-40 token: {flagged}")
        else:
            passed.append("planted dead full-40-hex token flagged (1/1)")
        if any(t == good for (_f, t) in flagged):
            failures.append("committed gate flagged the resolving commit")
        else:
            passed.append("resolving commit not flagged")
        false_positives = [t for (_f, t) in flagged if t not in (dead, dead40)]
        if false_positives:
            failures.append(f"committed gate false-positived: {sorted(set(false_positives))}")
        else:
            passed.append("no false positives on the exclusion classes")

        # Mutant F: skip git resolution (treat every token as resolving) -> false green
        mutant_f, _ = scan(files, str(repo), empty_adj, assume_resolves=True)
        if any(v["token"] == dead for v in mutant_f):
            failures.append("mutant F (no resolution) still flags the dead token")
        else:
            passed.append("mutant F (no resolution) false-green on dead token (diverges)")

        # Mutant G: no context filter -> overreach
        mutant_g, _ = scan(files, str(repo), empty_adj, use_context=False)
        g_flagged = {v["token"] for v in mutant_g}
        if "cafe012" not in g_flagged:
            failures.append("mutant G (no context filter) failed to overreach on plain hex")
        else:
            passed.append("mutant G (no context filter) overreaches on plain hex (diverges)")

        # Mutant H: no sha256-digest exclusion -> digest flagged
        mutant_h, _ = scan(files, str(repo), empty_adj, use_digest_exclusion=False)
        h_flagged = {v["token"] for v in mutant_h}
        if "5cedaa3b" not in h_flagged:
            failures.append("mutant H (no digest exclusion) failed to flag the sha256 token")
        else:
            passed.append("mutant H (no digest exclusion) flags the sha256 token (diverges)")

        # Mutant E: no ellipsis-digest rule -> context-carrying digest prefixes flagged
        mutant_e, _ = scan(files, str(repo), empty_adj, use_ellipsis_digest=False)
        e_flagged = {v["token"] for v in mutant_e}
        if "5111264f" not in e_flagged or "f3c3171b" not in e_flagged:
            failures.append(f"mutant E (no ellipsis rule) failed to overreach: {sorted(e_flagged)}")
        else:
            passed.append("mutant E (no ellipsis rule) overreaches on digest prefixes (diverges)")

        # Adjudication ledger suppresses a violation
        adj = {(dead, "LOG.md"): "quoted-dead-token"}
        v2, adj2 = scan(files, str(repo), adj)
        if not any(a["token"] == dead and a["file"] == "LOG.md" for a in adj2) \
                or any(v["file"] == "LOG.md" and v["token"] == dead for v in v2):
            failures.append("adjudication ledger did not suppress the named token/file")
        else:
            passed.append("adjudication ledger suppresses named token/file only")

    print("citation_lint --selftest")
    for name in passed:
        print(f"  PASS  {name}")
    for name in failures:
        print(f"  FAIL  {name}")
    total = len(passed) + len(failures)
    print(f"selftest: {len(passed)}/{total} passed")
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    args_list = sys.argv[1:] if argv is None else argv
    if "--selftest" in args_list:
        return selftest()
    try:
        args = parse_cli(args_list)
    except UsageError as exc:
        print(f"citation_lint.py: {exc}", file=sys.stderr)
        return EXIT_USAGE

    root = os.path.abspath(args.root)
    try:
        files = read_population(root, args.revision)
    except InputError as exc:
        print(f"citation_lint.py: {exc}", file=sys.stderr)
        return EXIT_INPUT
    adjudications = load_adjudications(root, args.adjudications, args.revision)
    violations, adjudicated = scan(files, root, adjudications)

    report = {
        "version": 1,
        "population": list(POPULATION),
        "revision": args.revision,
        "adjudications": args.adjudications,
        "violations": violations,
        "adjudicated": adjudicated,
        "verdict": "clean" if not violations else "failed-policy",
    }
    encoded = json.dumps(report, sort_keys=True, separators=(",", ":"))
    if args.json is None or args.json == "-":
        print(encoded)
    else:
        try:
            with open(args.json, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(encoded + "\n")
        except OSError as exc:
            print(f"citation_lint.py: cannot write JSON output: {exc}", file=sys.stderr)
            return EXIT_INPUT

    for violation in violations:
        print(f"{violation['file']}:{violation['line']}: {violation['token']} ({violation['reason']})")
    return EXIT_VIOLATION if violations else EXIT_CLEAN


if __name__ == "__main__":
    raise SystemExit(main())
