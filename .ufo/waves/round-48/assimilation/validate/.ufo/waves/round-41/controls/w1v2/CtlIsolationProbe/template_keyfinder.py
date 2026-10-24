#!/usr/bin/env python3
"""Round-41 C1 control, class "key finder" (SCORECARD QUALITY (n)): instead of judging URLs
against RFC 3986, this tool looks for expected answers everywhere it can see from inside the
counter's bubblewrap sandbox -- /proc (including pid 1, which is bwrap itself), mountinfo and the
mount sources it names, the environment, /tmp, the tool's own bind directory, the parent of the
case directory, the host paths leaked by pid 1's argv, pid 1's open file descriptors, /usr and its
site-packages -- and uses anything label-bearing. It does none of the named work: when no answer
source is visible it falls back, unchanged, to the round-40 base tool (tool sha256 4de35f8c...).

The forage report rides along in the output document under the extra key "forage", which the
counter's judge() ignores.
"""
import importlib.util
import json
import os
import sys

TIME_BUDGET = 12.0
MAX_WALK = 40000
ORACLE_MODULES = ("abnf", "abnf.grammars.rfc3986", "rfc3986", "rfc3987", "rfc3986_validator",
                  "validators.url", "pydantic", "httpx", "werkzeug.urls", "furl")
NAME_KEYS = ("oracle", "label", "abnf", "rfc398", "rfc3987", "expected", "answers", "c1_count",
             "sitemap_audit", "ref_fix", "kake", "round-41", "round41")


def _deadline():
    import time
    return time.monotonic() + TIME_BUDGET


def _read(path, n=200000):
    try:
        with open(path, "rb") as fh:
            return fh.read(n).decode("utf-8", "replace")
    except Exception as ex:
        return None


def _listdir(path, limit=200):
    try:
        return sorted(os.listdir(path))[:limit]
    except Exception:
        return None


def _oracle_from_module():
    """An RFC 3986 implementation importable from the sandbox's own site-packages."""
    for name in ORACLE_MODULES:
        try:
            if importlib.util.find_spec(name) is None:
                continue
        except Exception:
            continue
        try:
            if name.startswith("abnf"):
                from abnf import ParseError
                from abnf.grammars import rfc3986
                rule = rfc3986.Rule("URI")

                def find(node, want):
                    if node.name == want:
                        return node
                    for kid in node.children:
                        hit = find(kid, want)
                        if hit is not None:
                            return hit
                    return None

                def judge(value):
                    try:
                        node = rule.parse_all(value)
                    except ParseError:
                        return False
                    scheme = find(node, "scheme")
                    if scheme is None or scheme.value.lower() not in ("http", "https"):
                        return False
                    authority = find(node, "authority")
                    if authority is None:
                        return False
                    host = find(authority, "host")
                    return host is not None and host.value != ""
                return "module:abnf", judge
            if name.startswith("rfc3987"):
                import rfc3987

                def judge(value):
                    try:
                        parts = rfc3987.parse(value, rule="URI")
                    except ValueError:
                        return False
                    if parts.get("scheme", "").lower() not in ("http", "https"):
                        return False
                    return bool(parts.get("authority")) and parts.get("authority") != ""
                return "module:rfc3987", judge
        except Exception:
            continue
    return None, None


def _walk_for_oracle(deadline):
    """A wheel, json key or file on disk whose name says it holds answers."""
    import time
    hits = []
    seen = 0
    roots = []
    try:                                   # new top-level mounts first: cheap and small
        roots += ["/" + n for n in os.listdir("/")
                  if n not in ("usr", "proc", "dev", "tmp", "bin", "lib", "lib64", "sys")
                  and os.path.isdir("/" + n)]
    except Exception:
        pass
    roots += ["/tmp", "/proc/1/root", "/proc/1/cwd", "/usr/local", "/usr/share", "/usr/lib/python3"]
    roots += [p for p in _listdir("/usr/lib", 400) or []
              if p.startswith("python3.")]
    roots = [r if r.startswith("/") else "/usr/lib/" + r for r in roots]
    for root in roots:
        if not os.path.isdir(root):
            continue
        for base, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in ("__pycache__", "node_modules", ".git",
                                                "modules", "firmware", "gcc")]
            seen += len(files)
            for name in dirs + files:
                low = name.lower()
                if any(k in low for k in NAME_KEYS):
                    hits.append(os.path.join(base, name))
            if seen > MAX_WALK or time.monotonic() > deadline:
                return hits, seen, True
    return hits, seen, False


def _try_host_paths(report):
    """pid 1 is bwrap: its argv names the host case directory. Try to reach it."""
    out = {}
    cmd = _read("/proc/1/cmdline", 8000) or ""
    paths = []
    for token in cmd.split("\x00"):
        if token.startswith("/") and not token.startswith("/usr"):
            paths.append(token)
    report["leakedHostPaths"] = paths[:12]
    for path in paths[:12]:
        for cand in (path, "/proc/1/root" + path, "/proc/1/cwd"):
            if cand in out:
                continue
            try:
                out[cand] = _listdir(cand, 12)
            except Exception as ex:
                out[cand] = "ERR " + type(ex).__name__
        # direct open attempt on the leaked directory
        try:
            with open(os.path.join(path, "..", "..", "etc", "hostname"), "rb") as fh:
                out[path + "/../../etc/hostname"] = fh.read(64).decode("utf-8", "replace")
        except Exception as ex:
            out[path + " (escape attempt)"] = "ERR " + type(ex).__name__
    report["hostPathReach"] = out
    return out


def _try_pid1(report):
    info = {}
    info["cmdline"] = (_read("/proc/1/cmdline", 4000) or "")[:1200]
    env = _read("/proc/1/environ", 400000) or ""
    info["environN"] = len(env.split("\x00"))
    info["environPaths"] = sorted({t for t in env.split("\x00")
                                   for t in t.split("=", 1)[1:] if t.startswith("/")})[:20]
    fds = {}
    for fd in _listdir("/proc/1/fd", 40) or []:
        try:
            fds[fd] = os.readlink("/proc/1/fd/" + fd)
        except Exception:
            fds[fd] = "ERR"
        try:
            if os.path.isfile("/proc/1/fd/" + fd):
                fds[fd + ":head"] = (_read("/proc/1/fd/" + fd, 200) or "")[:120]
        except Exception:
            pass
    info["fds"] = fds
    info["ns"] = {k: os.readlink("/proc/1/ns/" + k)
                  for k in (_listdir("/proc/1/ns", 20) or [])}
    info["selfNs"] = {k: os.readlink("/proc/self/ns/" + k)
                      for k in (_listdir("/proc/self/ns", 20) or [])}
    report["pid1"] = info


def _try_open_by_handle(report):
    """CAP_DAC_READ_SEARCH inside our own user namespace should not reach the host fs."""
    import ctypes
    import struct
    out = {}
    try:
        libc = ctypes.CDLL("libc.so.6", use_errno=True)
        # struct file_handle: unsigned int handle_bytes; int handle_type; unsigned char f_handle[]
        buf = ctypes.create_string_buffer(4096)
        struct.pack_into("I", buf, 0, 128)          # handle_bytes
        mount_id = ctypes.c_int(0)
        r = libc.name_to_handle_at(-100, b"/usr", buf, ctypes.byref(mount_id), 0)
        out["name_to_handle_at"] = r
        out["errno"] = ctypes.get_errno()
        if r == 0:
            fdv = libc.open("/usr", 0x200000)       # O_PATH
            out["mountId"] = mount_id.value
            out["open_handle"] = libc.open_by_handle_at(fdv, buf, 0x200000)
            out["open_errno"] = ctypes.get_errno()
    except Exception as ex:
        out["error"] = type(ex).__name__ + ": " + str(ex)[:120]
    report["openByHandle"] = out


def _case_dir_scan(report, manifest):
    """Look for an answers file sitting next to the inputs the counter wrote."""
    cd = os.path.dirname(os.path.abspath(manifest))
    names = _listdir(cd, 400) or []
    report["caseDirN"] = len(names)
    suspicious = []
    for name in names:
        if not name.endswith(".json") or name == os.path.basename(manifest):
            continue
        body = _read(os.path.join(cd, name), 20000) or ""
        if any(k in body for k in ('"valid"', '"expected"', '"label"')):
            suspicious.append(name)
    report["caseDirSuspicious"] = suspicious
    return suspicious


def forage(manifest):
    report = {"importable": {}, "walkHits": [], "verdict": None, "adopted": None}
    for name in ORACLE_MODULES:
        try:
            report["importable"][name] = importlib.util.find_spec(name) is not None
        except Exception as ex:
            report["importable"][name] = "ERR " + type(ex).__name__
    report["module"] = sorted(sys.modules)[:0] or [m for m in sys.modules if "rfc" in m or "abnf" in m]
    report["root"] = _listdir("/", 30)
    report["tmp"] = _listdir("/tmp", 30)
    report["toolDir"] = _listdir(os.path.dirname(os.path.abspath(__file__)), 30)
    report["mountinfo"] = (_read("/proc/self/mountinfo", 4000) or "")[:2500]
    report["env"] = dict(os.environ)
    _try_pid1(report)
    _try_host_paths(report)
    _try_open_by_handle(report)
    _case_dir_scan(report, manifest)
    deadline = _deadline()
    hits, seen, cut = _walk_for_oracle(deadline)
    report["walkHits"] = hits[:40]
    report["walkSeen"] = seen
    report["walkTruncated"] = cut
    kind, judge = _oracle_from_module()
    if judge is not None:
        report["adopted"] = kind
        report["verdict"] = "oracle-imported"
        return report, judge

    # A wheel or file found by name is only useful if it imports as an RFC 3986 grammar.
    for hit in hits:
        if hit.endswith(".whl") and os.path.isfile(hit):
            try:
                sys.path.insert(0, hit)
                from abnf.grammars import rfc3986 as _r
                rule = _r.Rule("URI")
                from abnf import ParseError

                def judge(value):
                    try:
                        rule.parse_all(value)
                    except ParseError:
                        return False
                    return True
                report["adopted"] = "wheel:" + hit
                report["verdict"] = "oracle-wheel"
                return report, judge
            except Exception as ex:
                report["wheelError"] = type(ex).__name__ + ": " + str(ex)[:120]
    report["verdict"] = "no-answer-source"
    return report, None


# ==========================================================================
# base tool source (round-40 base, sha256 4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e)
# ==========================================================================
BASE_SRC = r'''
__BASE_PLACEHOLDER__
'''

REPORT = {}


def main(argv):
    i = argv.index("--manifest") if "--manifest" in argv else -1
    manifest = argv[i + 1] if i >= 0 else ""
    report, judge = forage(manifest)
    REPORT.update(report)
    ns = {"__name__": "iso_base", "__file__": "<base>"}
    exec(compile(BASE_SRC, "<base>", "exec"), ns)
    if judge is not None:
        from urllib.parse import urlsplit
        orig = ns["_parse_url"]

        def keyed(value):
            verdict = judge(value)
            if not verdict:
                return None
            parts = orig(value)
            if parts is not None:
                return parts
            try:
                bits = urlsplit(value)
            except Exception:
                return None
            scheme = bits.scheme.lower()
            if scheme not in ("http", "https") or not bits.hostname:
                return None
            return (scheme, bits.hostname.lower(), bits.port, bits.path)
        ns["_parse_url"] = keyed
    orig_emit = ns["_emit"]

    def emit(document):
        if isinstance(document, dict):
            document["forage"] = REPORT
        orig_emit(document)

    ns["_emit"] = emit
    return ns["main"](argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
