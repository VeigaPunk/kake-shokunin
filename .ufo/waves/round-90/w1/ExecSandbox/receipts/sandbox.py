
import os, sys, sysconfig, runpy
_cand = os.path.realpath(sys.argv[1])
_STD = set(sys.stdlib_module_names) | set(sys.builtin_module_names)
_roots = []
for _k in ("stdlib", "platstdlib"):
    _p = sysconfig.get_paths().get(_k)
    if _p:
        _roots.append(os.path.realpath(_p) + os.sep)
_roots = tuple(_roots)
_DENY = ("subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "os.spawn", "os.fork",
         "os.forkpty", "pty.spawn", "socket.connect", "socket.bind", "socket.__new__", "ctypes.dlopen",
         "ctypes.dlsym", "ctypes.cdata", "glob.glob", "os.chdir",
         "os.startfile", "webbrowser.open", "urllib.Request", "shutil.copyfile", "os.remove",
         "os.rename", "os.mkdir", "os.rmdir", "os.unlink", "os.truncate", "os.chmod", "os.symlink")
def _die(why):
    os.write(2, ("SANDBOX_VIOLATION " + why + "\n").encode("utf-8", "replace"))
    os._exit(97)
def _hook(event, args):
    if event == "import":
        top = str(args[0]).split(".")[0]
        if top not in _STD:
            _die("import " + str(args[0]))
    elif event in ("os.listdir", "os.scandir"):
        p = args[0] if args and args[0] is not None else "."
        if isinstance(p, int):
            _die(event + " fd")
        if isinstance(p, bytes):
            p = os.fsdecode(p)
        rp = os.path.realpath(str(p)) + os.sep
        if not rp.startswith(_roots):
            _die(event + " " + rp)
    elif event == "open":
        p = args[0]
        if isinstance(p, int):
            return
        if isinstance(p, bytes):
            p = os.fsdecode(p)
        rp = os.path.realpath(str(p))
        if rp != _cand and not rp.startswith(_roots):
            _die("open " + rp)
    elif event.startswith(_DENY) or event == "sys.addaudithook":
        _die(event)
sys.argv = [_cand]
sys.addaudithook(_hook)
runpy.run_path(_cand, run_name="__main__")
