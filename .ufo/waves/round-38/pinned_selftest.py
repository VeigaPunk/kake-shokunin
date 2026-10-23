#!/usr/bin/env python3
"""Run a selftest against the tool bytes at a Git revision and write a pinned receipt.

Repairs round-37 closure routed defect 5 (corpus/lessons/round-37-verifier-spotcheck.md, defects):
`verification/postfix/robots-selftest-137-on-postfix-tool.json` named the tool it measured by
filesystem path only (`tool: ".../scripts/robots_audit.py"`), so the receipt could not say which
tool bytes it measured and the round-37 tip tool sha256 (`944d2f51...d3e5`) was unpinned. This
runner reads both the tool and the selftest out of the lane repository with
`git cat-file blob REV:PATH` (never the working tree), writes them into a private temporary
directory, runs the selftest against that copy, and writes a receipt carrying the selftest's JSON
summary plus the revision, Git object id and sha256 of each file.

Usage:
  python3 -B pinned_selftest.py --root ROOT --revision REV \\
      --tool scripts/robots_audit.py --selftest scripts/robots_audit_selftest.py \\
      --out RECEIPT.json

  --tool-revision PATH      override --revision for the tool (default: --revision)
  --selftest-revision PATH  override --revision for the selftest (default: --revision)
  --exit-file PATH          also write the exit code as decimal text (lane receipt convention)
  --timeout SECONDS         cap on the selftest run (default 900); on expiry the selftest's
                            process group is killed and the run is exit 2

Exit: the selftest's own exit code. For scripts/robots_audit_selftest.py that is 0 (every fixture
passed), 1 (at least one failed) or 2 (could not evaluate). 2 is also returned on a usage error, an
unreadable revision or blob, an unwritable receipt, a selftest killed by a signal, a timeout, a
selftest that prints no readable JSON summary (a run whose summary cannot be read is never
reported as a pass) and any internal error. In every one of those cases the receipt is still
written, carrying `error`, `timedOut` or `summaryError`, so a failed run is pinned too. One line on
stderr, never a traceback.

Reads are `git cat-file blob`, which returns blobs only and never a tree, with every `GIT_*`
environment variable dropped (a caller's GIT_DIR/GIT_WORK_TREE cannot redirect the read), the
system and global Git config ignored and hooks disabled -- the same Git access as
scripts/receipt_replay.py. The temporary copies are removed before returning, in every path; the
selftest runs with TMPDIR set inside that directory, so its own temporary fixtures are removed
with it, including after a timeout kill.

Receipt shape: the selftest's stdout JSON summary is the receipt's top level, with the summary's
`tool` member re-pointed from the (deleted) temporary copy to `toolPath` (the temporary paths the
selftest saw are in `command`). Pin fields are written after the summary, so a summary cannot
forge them: `toolPath`, `toolRevision`, `toolObjectId`, `toolSha256`, `selftestPath`,
`selftestRevision`, `selftestObjectId`, `selftestSha256`, `revision`,
`revisionRequested`, `selftestExit`, `command`, `root`, `time` (UTC, seconds: YYYY-MM-DDTHH:MM:SSZ).
When the selftest prints no JSON object, the receipt carries `summary`: null, `summaryError` and a
bounded `selftestStdoutHead`, and the exit is 2.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile

RUNNER = "pinned_selftest"
DEFAULT_TIMEOUT = 900


class Unreadable(Exception):
    """An input the runner cannot read at all: exit 2, receipt carries the message."""


def show(value: object) -> str:
    """Bounded ASCII rendering of an untrusted value for a message."""
    text = ascii(value)
    return text if len(text) <= 80 else text[:77] + "..."


def one_line(exc: BaseException | str) -> str:
    text = " ".join(str(exc).split())
    return text.encode("ascii", "backslashreplace").decode("ascii")[:400]


def utc_now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_hex(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


# --- Git access ----------------------------------------------------------------

class GitStore:
    """Blob reads at a revision. `cat-file blob` returns blobs only, never trees."""

    def __init__(self, root: str) -> None:
        self.root = root

    def git(self, *args: str) -> subprocess.CompletedProcess[bytes]:
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                   GIT_OPTIONAL_LOCKS="0")
        try:
            return subprocess.run(
                ["git", "-c", "core.hooksPath=/dev/null", "-C", self.root, *args],
                env=env, capture_output=True, check=False, timeout=60)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise Unreadable(f"git {args[0]} could not run: {one_line(exc)}") from None

    def resolve(self, revision: str) -> str:
        if not revision or revision.startswith("-"):
            raise Unreadable("revision must be non-empty and must not start with '-'")
        done = self.git("rev-parse", "--verify", "--end-of-options", revision + "^{commit}")
        if done.returncode != 0:
            raise Unreadable(f"revision {show(revision)} does not resolve to a commit in {show(self.root)}")
        return done.stdout.decode("ascii").strip()

    def blob(self, rev: str, path: str) -> tuple[bytes, str]:
        """Return (bytes, Git blob object id) for `rev:path`, or raise Unreadable."""
        if (not path or path.startswith("-") or path.startswith("/") or path.endswith("/")
                or ":" in path or "\x00" in path or "\n" in path or path == ".."):
            raise Unreadable(
                f"path {show(path)} must be a repository-relative file path without ':'")
        spec = f"{rev}:{path}"
        ident = self.git("rev-parse", "--verify", spec)
        if ident.returncode != 0:
            raise Unreadable(f"{show(path)} is not present at {rev[:12]}")
        object_id = ident.stdout.decode("ascii").strip()
        done = self.git("cat-file", "blob", spec)
        if done.returncode != 0:
            raise Unreadable(f"{show(path)} at {rev[:12]} is not a readable blob "
                             f"({one_line(done.stderr.decode('utf-8', 'replace'))})")
        return done.stdout, object_id


# --- the run -------------------------------------------------------------------

def run_capped(command: list[str], cwd: str, timeout: int,
               env: dict[str, str]) -> tuple[int | None, bytes, bytes, bool]:
    """Run `command` in its own session; on timeout kill the group. Returns (exit, out, err, timed_out)."""
    proc = subprocess.Popen(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, start_new_session=True)
    try:
        out, err = proc.communicate(timeout=timeout)
        return proc.returncode, out, err, False
    except subprocess.TimeoutExpired:
        for target in (lambda: os.killpg(proc.pid, signal.SIGKILL), lambda: proc.kill()):
            try:
                target()
            except OSError:
                pass
        try:
            out, err = proc.communicate(timeout=30)
        except subprocess.TimeoutExpired:
            out, err = b"", b""
        return None, out, err, True


def parse_summary(stdout: bytes) -> dict:
    """The selftest's JSON summary: the whole stdout, else its last JSON object line."""
    text = stdout.decode("utf-8", "replace").strip()
    if not text:
        raise ValueError("stdout is empty")
    try:
        value = json.loads(text)
    except ValueError:
        value = None
        for line in reversed(text.splitlines()):
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                value = json.loads(line)
            except ValueError:
                continue
            break
        if value is None:
            raise ValueError("stdout holds no JSON object") from None
    if not isinstance(value, dict):
        raise ValueError("stdout JSON is not an object")
    return value


def write_receipt(path: str, payload: dict, exit_code: int | None,
                  exit_file: str | None) -> None:
    directory = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(directory, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    handle_fd, temporary = tempfile.mkstemp(prefix=".pinned-receipt-", dir=directory)
    try:
        with os.fdopen(handle_fd, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise
    if exit_file is not None:
        exit_directory = os.path.dirname(os.path.abspath(exit_file)) or "."
        os.makedirs(exit_directory, exist_ok=True)
        with open(exit_file, "w", encoding="utf-8") as handle:
            handle.write("%s\n" % ("" if exit_code is None else exit_code))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run a selftest against the tool bytes at a Git revision; pin both by sha256.")
    parser.add_argument("--root", default=".", help="lane repository (default: .)")
    parser.add_argument("--revision", required=True, help="commit the tool and selftest come from")
    parser.add_argument("--tool", required=True, help="repository-relative path of the tool under test")
    parser.add_argument("--selftest", required=True, help="repository-relative path of the selftest")
    parser.add_argument("--tool-revision", help="override --revision for the tool")
    parser.add_argument("--selftest-revision", help="override --revision for the selftest")
    parser.add_argument("--out", required=True, help="receipt path to write")
    parser.add_argument("--exit-file", help="also write the exit code here as decimal text")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help=f"selftest run cap in seconds (default: {DEFAULT_TIMEOUT})")
    args = parser.parse_args(argv)

    receipt: dict = {
        "runner": RUNNER,
        "root": os.path.abspath(args.root),
        "revisionRequested": args.revision,
        "toolPath": args.tool,
        "selftestPath": args.selftest,
        "time": utc_now(),
    }
    work: str | None = None
    try:
        if args.timeout <= 0:
            raise Unreadable("--timeout must be positive")
        store = GitStore(args.root)
        revision = store.resolve(args.revision)
        tool_revision = store.resolve(args.tool_revision or args.revision)
        selftest_revision = store.resolve(args.selftest_revision or args.revision)

        tool_bytes, tool_id = store.blob(tool_revision, args.tool)
        selftest_bytes, selftest_id = store.blob(selftest_revision, args.selftest)
        receipt.update({
            "revision": revision,
            "toolRevision": tool_revision,
            "toolObjectId": tool_id,
            "toolSha256": sha256_hex(tool_bytes),
            "selftestRevision": selftest_revision,
            "selftestObjectId": selftest_id,
            "selftestSha256": sha256_hex(selftest_bytes),
        })

        work = tempfile.mkdtemp(prefix="kake-pinned-selftest-")
        tool_file = os.path.join(work, "tool", os.path.basename(args.tool))
        selftest_file = os.path.join(work, "selftest", os.path.basename(args.selftest))
        for target, data in ((tool_file, tool_bytes), (selftest_file, selftest_bytes)):
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as handle:
                handle.write(data)
            os.chmod(target, 0o500)

        command = [sys.executable, "-B", selftest_file, "--tool", tool_file]
        env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
        env.setdefault("LC_ALL", "C.UTF-8")
        # The selftest's own temporary files live under `work`, so a killed run leaves nothing
        # behind: its TMPDIR is a directory this runner removes.
        env["TMPDIR"] = env["TMP"] = env["TEMP"] = os.path.join(work, "temp")
        os.makedirs(env["TMPDIR"], exist_ok=True)
        receipt.update({"command": command})
        exit_code, stdout, _stderr, timed_out = run_capped(
            command, cwd=work, timeout=args.timeout, env=env)
        receipt.update({
            "selftestExit": exit_code,
            "timedOut": timed_out,
            "selftestStdoutBytes": len(stdout),
        })
        if timed_out:
            receipt["error"] = f"selftest exceeded {args.timeout} s and was killed"
            write_receipt(args.out, receipt, None, args.exit_file)
            print(f"{RUNNER}: selftest exceeded {args.timeout} s", file=sys.stderr)
            return 2
        try:
            summary = parse_summary(stdout)
        except (ValueError, UnicodeError) as exc:
            head = stdout.decode("utf-8", "replace")[:400]
            receipt.update({"summary": None, "summaryError": one_line(exc),
                            "selftestStdoutHead": one_line(head)})
            write_receipt(args.out, receipt, 2, args.exit_file)
            print(f"{RUNNER}: no JSON summary from the selftest: {one_line(exc)}", file=sys.stderr)
            return 2
        receipt.update(summary)
        # Pin fields last: a summary cannot forge them. The summary's own `tool` named a
        # temporary copy that no longer exists; the pin is `toolPath`.
        receipt.update({
            "toolPath": args.tool,
            "toolRevision": tool_revision,
            "toolObjectId": tool_id,
            "toolSha256": sha256_hex(tool_bytes),
            "selftestPath": args.selftest,
            "selftestRevision": selftest_revision,
            "selftestObjectId": selftest_id,
            "selftestSha256": sha256_hex(selftest_bytes),
            "revision": revision,
            "revisionRequested": args.revision,
            "command": command,
            "selftestExit": exit_code,
            "timedOut": timed_out,
            "root": os.path.abspath(args.root),
            "time": utc_now(),
        })
        if "tool" in summary:
            receipt["tool"] = args.tool
        write_receipt(args.out, receipt, exit_code, args.exit_file)
        if exit_code is None or exit_code < 0:
            print(f"{RUNNER}: selftest was killed by a signal", file=sys.stderr)
            return 2
        return exit_code
    except (Unreadable, OSError, ValueError) as exc:
        receipt["error"] = one_line(exc)
        try:
            write_receipt(args.out, receipt, None, args.exit_file)
        except OSError as write_exc:
            print(f"{RUNNER}: {one_line(exc)}; receipt unwritable: {one_line(write_exc)}",
                  file=sys.stderr)
            return 2
        print(f"{RUNNER}: {one_line(exc)}", file=sys.stderr)
        return 2
    except BaseException as exc:  # never a traceback; a broken run is still pinned
        receipt["error"] = "internal error: " + one_line(exc)
        try:
            write_receipt(args.out, receipt, None, args.exit_file)
        except OSError:
            pass
        print(f"{RUNNER}: internal error: {one_line(exc)}", file=sys.stderr)
        return 2
    finally:
        if work is not None:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
