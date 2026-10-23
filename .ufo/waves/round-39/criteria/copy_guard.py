#!/usr/bin/env python3
"""Copy guard: flag near-duplication between a candidate tool and a corpus.

Normalisation pipeline, per file (stdlib only):

  1. parse the file with :mod:`ast`;
  2. drop every docstring (module, class, function, async function);
  3. rename every identifier in order of first use -- the first distinct name
     seen in source order becomes ``v0``, the next ``v1``, and so on -- so that
     re-naming a variable, function, argument, attribute or import alias does
     not hide a copy;
  4. unparse the rewritten tree and tokenise it; comments, layout and
     INDENT/DEDENT/NEWLINE tokens are already gone, and string literals are
     reduced to their unquoted, whitespace-collapsed text.

Each ``(candidate, against)`` pair is then scored with :mod:`difflib` over the
normalised token sequences.  A pair is a HIT when the sequence ratio is at
least ``--ratio`` (default 0.60) *and* at least ``--min-matched`` tokens are
actually matched (default 40), or when the longest common contiguous token run
is at least ``--run`` tokens (default 200).

The matched-token floor exists because ``difflib`` ratios are unstable on tiny
inputs: ``x = 1`` against ``y = 2`` scores 0.67 and two empty files score 1.0.
Below the floor the pair is reported but cannot decide the verdict.

Exit codes: 0 no hit, 1 at least one hit, 2 could not evaluate (unreadable or
unparsable input, bad arguments).
"""

from __future__ import annotations

import argparse
import ast
import difflib
import glob
import io
import json
import os
import re
import sys
import tokenize

DEFAULT_RATIO = 0.6
DEFAULT_RUN = 200
DEFAULT_MIN_MATCHED = 40

# Layout tokens carry no semantics for copy detection.
SKIP_TOKEN_TYPES = frozenset(
    {
        tokenize.NL,
        tokenize.NEWLINE,
        tokenize.INDENT,
        tokenize.DEDENT,
        tokenize.ENDMARKER,
        getattr(tokenize, "ENCODING", -1),
        tokenize.COMMENT,
    }
)

STRING_TOKEN_NAMES = frozenset({"STRING", "FSTRING_START", "FSTRING_MIDDLE", "FSTRING_END"})

_STRING_OPEN = re.compile(r"^([A-Za-z]{0,3})(\"\"\"|'''|\"|')")
_WHITESPACE = re.compile(r"\s+")


class GuardError(Exception):
    """Input that cannot be normalised."""


# --------------------------------------------------------------------------- #
# normalisation
# --------------------------------------------------------------------------- #
def strip_docstrings(tree: ast.AST) -> None:
    """Remove the leading string statement of every scope that may hold one."""
    owners = (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
    for node in ast.walk(tree):
        if not isinstance(node, owners):
            continue
        body = getattr(node, "body", None)
        if not body:
            continue
        first = body[0]
        if (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        ):
            node.body = body[1:] or [ast.Pass()]


def _identifier_slots(tree: ast.AST) -> list[tuple]:
    """Every identifier occurrence, ordered by source position.

    Each slot is ``(position, name, node, field, index)``; ``index`` addresses a
    list field (``Global.names``) and is ``None`` for a plain attribute.
    """
    slots: list[tuple] = []
    counter = 0

    def add(name, node, field, index=None):
        nonlocal counter
        if not name:
            return
        position = (getattr(node, "lineno", 0) or 0, getattr(node, "col_offset", 0) or 0, counter)
        counter += 1
        slots.append((position, name, node, field, index))

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            add(node.id, node, "id")
        elif isinstance(node, ast.arg):
            add(node.arg, node, "arg")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            add(node.name, node, "name")
        elif isinstance(node, ast.Attribute):
            add(node.attr, node, "attr")
        elif isinstance(node, ast.keyword):
            add(node.arg, node, "arg")
        elif isinstance(node, ast.alias):
            add(node.name, node, "name")
            add(node.asname, node, "asname")
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            for index, name in enumerate(node.names):
                add(name, node, "names", index)
        elif isinstance(node, ast.ExceptHandler):
            add(node.name, node, "name")
        elif isinstance(node, (ast.MatchAs, ast.MatchStar)):
            add(node.name, node, "name")
        elif isinstance(node, ast.MatchMapping):
            add(node.rest, node, "rest")
        else:
            type_param = getattr(ast, "TypeVar", None)
            if type_param is not None and isinstance(node, type_param):
                add(node.name, node, "name")

    slots.sort(key=lambda slot: slot[0])
    return slots


def rename_identifiers(tree: ast.AST) -> dict[str, str]:
    """Rename every identifier to ``vN`` by order of first use (in place)."""
    mapping: dict[str, str] = {}
    for _position, name, node, field, index in _identifier_slots(tree):
        new_name = mapping.get(name)
        if new_name is None:
            new_name = f"v{len(mapping)}"
            mapping[name] = new_name
        if index is None:
            setattr(node, field, new_name)
        else:
            getattr(node, field)[index] = new_name
    return mapping


def normalise_string(text: str) -> str:
    """Unquote a string token and collapse its whitespace."""
    matched = _STRING_OPEN.match(text.strip())
    body = text.strip()[matched.end() :] if matched else text.strip()
    if matched:
        quote = matched.group(2)
        if body.endswith(quote):
            body = body[: -len(quote)]
    return _WHITESPACE.sub(" ", body).strip()


def tokenise(source: str) -> list[tuple[str, str]]:
    tokens: list[tuple[str, str]] = []
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type in SKIP_TOKEN_TYPES:
            continue
        name = tokenize.tok_name.get(token.type, str(token.type))
        if name in STRING_TOKEN_NAMES:
            value = "<fstring>" if name != "STRING" else normalise_string(token.string)
            tokens.append(("STRING", value))
        elif token.type == tokenize.NUMBER:
            tokens.append(("NUMBER", token.string))
        elif token.type == tokenize.NAME:
            tokens.append(("NAME", token.string))
        else:
            tokens.append((name, token.string))
    return tokens


def normalise(path: str) -> list[tuple[str, str]]:
    """Full normalisation of one Python file to a semantic token sequence."""
    try:
        # tokenize.open honours a PEP 263 coding cookie.
        with tokenize.open(path) as handle:
            source = handle.read()
    except OSError as exc:
        raise GuardError(f"{path}: cannot read: {exc}") from exc
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise GuardError(f"{path}: cannot decode: {exc}") from exc

    try:
        tree = ast.parse(source, filename=path)
    except SyntaxError as exc:
        raise GuardError(f"{path}: cannot parse: {exc}") from exc

    strip_docstrings(tree)
    rename_identifiers(tree)

    try:
        rewritten = ast.unparse(tree)
    except Exception as exc:  # unparse should not fail on a parsed tree
        raise GuardError(f"{path}: cannot unparse: {exc}") from exc
    return tokenise(rewritten)


# --------------------------------------------------------------------------- #
# comparison
# --------------------------------------------------------------------------- #
def compare(left: list[tuple[str, str]], right: list[tuple[str, str]]) -> tuple[float, int, int]:
    """Return ``(difflib ratio, longest common contiguous run, matched tokens)``."""
    matcher = difflib.SequenceMatcher(None, left, right, autojunk=False)
    ratio = matcher.ratio()
    blocks = matcher.get_matching_blocks()
    longest_run = max((block.size for block in blocks), default=0)
    matched = sum(block.size for block in blocks)
    return ratio, longest_run, matched


def expand_against(patterns: list[str]) -> list[str]:
    """Expand files, directories (recursive ``*.py``) and globs, de-duplicated."""
    found: list[str] = []
    seen: set[str] = set()
    for pattern in patterns:
        if os.path.isdir(pattern):
            matches = sorted(glob.glob(os.path.join(pattern, "**", "*.py"), recursive=True))
        elif os.path.isfile(pattern):
            matches = [pattern]
        else:
            matches = sorted(glob.glob(pattern, recursive=True))
            if not matches:
                raise GuardError(f"no such file, directory or glob match: {pattern}")
        for match in matches:
            resolved = os.path.realpath(match)
            if resolved in seen:
                continue
            seen.add(resolved)
            found.append(resolved)
    return found


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Flag near-duplication between a candidate file and an 'against' corpus.",
        epilog=(
            "Exit status: 0 = no pair over the thresholds, 1 = at least one hit, "
            "2 = could not evaluate."
        ),
    )
    parser.add_argument("--candidate", required=True, help="Python file under review.")
    parser.add_argument(
        "--against",
        required=True,
        nargs="+",
        help="Corpus: one or more files, directories (recursive *.py) or globs.",
    )
    parser.add_argument("--ratio", type=float, default=DEFAULT_RATIO, help="Ratio threshold.")
    parser.add_argument("--run", type=int, default=DEFAULT_RUN, help="Longest-run threshold, tokens.")
    parser.add_argument(
        "--min-matched",
        type=int,
        default=DEFAULT_MIN_MATCHED,
        help="Matched tokens needed before the ratio rule may fire (0 disables the floor).",
    )
    parser.add_argument("--json", action="store_true", help="Emit one JSON report on stdout.")
    return parser.parse_args(argv)


def build_report(
    candidate: str, against: list[str], ratio_at: float, run_at: int, min_matched: int
) -> dict:
    candidate_tokens = normalise(candidate)
    pairs = []
    hits = 0
    for other in against:
        other_tokens = normalise(other)
        ratio, longest_run, matched = compare(candidate_tokens, other_tokens)
        reasons = []
        if ratio >= ratio_at and matched >= min_matched:
            reasons.append(f"ratio>={ratio_at:g}")
        if longest_run >= run_at:
            reasons.append(f"run>={run_at}")
        if reasons:
            hits += 1
        notes = []
        if ratio >= ratio_at and matched < min_matched:
            notes.append(f"ratio over threshold but only {matched} matched token(s) < {min_matched}: floor")
        pairs.append(
            {
                "against": other,
                "tokens": len(other_tokens),
                "ratio": round(ratio, 6),
                "longest_run": longest_run,
                "matched": matched,
                "hit": bool(reasons),
                "reasons": reasons,
                "notes": notes,
            }
        )
    pairs.sort(key=lambda item: (-item["ratio"], -item["longest_run"], item["against"]))
    return {
        "candidate": candidate,
        "candidate_tokens": len(candidate_tokens),
        "ratio_threshold": ratio_at,
        "run_threshold": run_at,
        "min_matched": min_matched,
        "pairs": pairs,
        "hits": hits,
        "clean": hits == 0,
    }


def print_report(report: dict) -> None:
    print(f"candidate {report['candidate']} (tokens={report['candidate_tokens']})")
    for pair in report["pairs"]:
        status = "HIT" if pair["hit"] else "ok"
        reason = " ".join(pair["reasons"])
        print(
            f"  against {pair['against']} tokens={pair['tokens']} "
            f"ratio={pair['ratio']:.4f} run={pair['longest_run']} "
            f"matched={pair['matched']} {status} {reason}".rstrip()
        )
        for note in pair["notes"]:
            print(f"    note: {note}")
    total = len(report["pairs"])
    verdict = "CLEAN" if report["clean"] else "COPY-SUSPECT"
    print(f"verdict: {verdict} ({report['hits']}/{total} pair(s) over threshold)")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        candidate = os.path.realpath(args.candidate)
        if not os.path.isfile(candidate):
            raise GuardError(f"candidate is not a file: {args.candidate}")
        against = expand_against(args.against)
        if not against:
            raise GuardError("empty 'against' corpus")
        report = build_report(candidate, against, args.ratio, args.run, args.min_matched)
    except GuardError as exc:
        print(f"copy_guard: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_report(report)
    return 0 if report["clean"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
