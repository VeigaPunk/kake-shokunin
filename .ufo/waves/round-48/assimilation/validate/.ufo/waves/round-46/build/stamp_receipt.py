#!/usr/bin/env python3
"""Run a command and record a small, content-addressed execution receipt."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def parse_args(argv: list[str]) -> tuple[argparse.Namespace, list[str]]:
    try:
        separator = argv.index("--")
    except ValueError:
        separator = len(argv)

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", required=True, help="measured repository revision")
    parser.add_argument("--tool-path", required=True, help="path identifying the measured tool")
    parser.add_argument("--root", default=".", help="working root and relative tool-path base")
    parser.add_argument("--receipt", required=True, help="JSON receipt output path")
    parser.add_argument("--tail-bytes", type=int, default=8192, help="maximum captured stdout suffix")
    options = parser.parse_args(argv[:separator])
    command = argv[separator + 1 :] if separator < len(argv) else []
    if not command:
        parser.error("a command is required after --")
    if options.tail_bytes < 0:
        parser.error("--tail-bytes must be non-negative")
    return options, command


def main(argv: list[str] | None = None) -> int:
    options, command = parse_args(sys.argv[1:] if argv is None else argv)
    root = Path(options.root).resolve(strict=True)
    supplied_tool_path = Path(options.tool_path)
    tool_file = supplied_tool_path if supplied_tool_path.is_absolute() else root / supplied_tool_path
    try:
        tool_sha256 = hashlib.sha256(tool_file.read_bytes()).hexdigest()
    except OSError as error:
        print(f"stamp_receipt.py: cannot read tool {options.tool_path!r}: {error}", file=sys.stderr)
        return 2

    started_at = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    start = time.monotonic()
    tail = bytearray()
    try:
        with subprocess.Popen(command, cwd=root, stdout=subprocess.PIPE) as process:
            assert process.stdout is not None
            while True:
                chunk = process.stdout.read(65536)
                if not chunk:
                    break
                limit = options.tail_bytes
                if limit:
                    if len(chunk) >= limit:
                        tail[:] = chunk[-limit:]
                    else:
                        tail.extend(chunk)
                        excess = len(tail) - limit
                        if excess > 0:
                            del tail[:excess]
            exit_code = process.wait()
    except OSError as error:
        print(f"stamp_receipt.py: cannot start command {command[0]!r}: {error}", file=sys.stderr)
        exit_code = 127

    wall_s = round(time.monotonic() - start, 6)
    receipt = {
        "measured_revision": options.revision,
        "tool_path": options.tool_path,
        "tool_sha256": tool_sha256,
        "argv": command,
        "exit": exit_code,
        "stdout_tail": tail.decode("utf-8", errors="replace"),
        "started_at": started_at,
        "wall_s": wall_s,
    }
    rendered = json.dumps(receipt, indent=2, ensure_ascii=False) + "\n"
    receipt_path = Path(options.receipt)
    try:
        with receipt_path.open("w", encoding="utf-8", newline="\n") as output:
            output.write(rendered)
    except OSError as error:
        print(f"stamp_receipt.py: cannot write receipt {options.receipt!r}: {error}", file=sys.stderr)
        return 2
    sys.stdout.write(rendered)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
