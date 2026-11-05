
import importlib.machinery, importlib.util, json, os, pkgutil, runpy, sys

subject = os.path.realpath(sys.argv[1])
root = os.path.dirname(subject)
allowed = set("""json sys os re math collections functools itertools decimal fractions
typing dataclasses enum string unicodedata operator copy bisect heapq array struct textwrap
pprint numbers abc contextlib weakref types warnings traceback linecache tokenize token keyword
builtins codecs encodings io errno stat posixpath genericpath time datetime hashlib random
binascii base64 runpy importlib importlib.machinery importlib.util pkgutil zipimport marshal
_collections_abc _io""".split())
prefixes = tuple(p for p in {os.path.realpath(sys.prefix),
                             os.path.realpath(sys.base_prefix),
                             os.path.dirname(os.path.realpath(os.__file__))}
                 if p)


def hook(event, args):
    if event == "open":
        p = args[0]
        if isinstance(p, (bytes, bytearray)):
            p = p.decode("utf-8", "replace")
        if isinstance(p, int):
            return
        if not isinstance(p, str):
            return
        ap = os.path.realpath(p)
        if ap == subject or ap.startswith(root + os.sep):
            return
        if ap.startswith(prefixes):
            return
        raise PermissionError("sandbox: open outside the subject tree: %s" % ap)
    elif event == "import":
        name = args[0]
        if name.split(".")[0] not in allowed:
            raise PermissionError("sandbox: import denied: %s" % name)
    elif event in ("os.system", "subprocess.Popen", "os.spawn", "os.posix_spawn",
                   "os.exec", "os.fork"):
        raise PermissionError("sandbox: process creation denied: %s" % event)


sys.addaudithook(hook)
sys.argv = [subject]
sys.path[:] = [root]
runpy.run_path(subject, run_name="__main__")
