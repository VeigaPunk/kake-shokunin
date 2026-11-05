#!/bin/bash
# SentinelScope (2): attack the C2 counter SANDBOX (extracted verbatim from c95_conditional.py, sha256 64cffb79...).
set -u
L=/home/vgpnk/Projects/shokunin/kake-shokunin
S=/fast/scratch/hyaku/kake-r95/SentinelScope
SB=$S/sbx
SUBJ=$SB/subj
WORK=$SB/work
rm -rf "$SUBJ" "$WORK"; mkdir -p "$SUBJ" "$WORK" "$WORK/tmp"
CNT=$L/.ufo/waves/round-95/c95_conditional.py
MARKDIR=$WORK
LIBDIR=$(python3 -c 'import sys,os; print(os.path.join(sys.prefix,"lib","python%d.%d"%sys.version_info[:2]))')

w() { printf '%s\n' "$2" > "$SUBJ/$1"; }

# benign happy path
w b00_ok.py 'import json,sys; sys.stdout.write(json.dumps({"ok":1}))'
# (1) direct denials the counter promises
w p01_open_outside.py 'open("/etc/hostname").read()'
w p02_import_nonallow.py 'import shutil'
w p03_os_system.py 'import os; os.system("true")'
w p04_popen.py 'import subprocess; subprocess.Popen(["true"])'
w p05_read_counter.py "open('$CNT').read()"
# (2) bypass candidates
w x01_symlink_outside.py "import os; root=os.path.dirname(os.path.abspath(__file__)); os.symlink('/etc/hostname', os.path.join(root,'lnk1')); print(open(os.path.join(root,'lnk1')).read()[:40])"
w x02_symlink_counter.py "import os; root=os.path.dirname(os.path.abspath(__file__)); os.symlink('$CNT', os.path.join(root,'lnk2')); print(open(os.path.join(root,'lnk2')).read()[:40])"
w x03_execv_sh.py "import os; os.execv('/bin/sh', ['sh','-c','echo EXEC > $MARKDIR/exec_marker'])"
w x04_os_open_write.py "import os; fd=os.open('$MARKDIR/osopen_marker', os.O_CREAT|os.O_WRONLY); os.write(fd,b'x'); os.close(fd)"
w x05_spec_stdlib_shutil.py "import importlib.util as u,sys; s=u.spec_from_file_location('shutil','$LIBDIR/shutil.py'); m=u.module_from_spec(s); s.loader.exec_module(m); print('LOADED', m.__name__, hasattr(m,'which'))"
w x06_spec_posixsubprocess.py "import importlib.util as u,glob,sys,os; c=glob.glob(os.path.join(sys.prefix,'lib','python*','lib-dynload','_posixsubprocess*.so'))+glob.glob(os.path.join(sys.base_prefix,'lib','python*','lib-dynload','_posixsubprocess*.so')); print('so', c[:1]); 
if c:
  s=u.spec_from_file_location('_posixsubprocess', c[0]); m=u.module_from_spec(s); s.loader.exec_module(m); print('LOADED', m.__name__, [x for x in dir(m) if 'fork' in x])
else:
  print('no-so-found')"
w x07_spec_then_fork_exec.py "import importlib.util as u,glob,sys,os
c=glob.glob(os.path.join(sys.prefix,'lib','python*','lib-dynload','_posixsubprocess*.so'))+glob.glob(os.path.join(sys.base_prefix,'lib','python*','lib-dynload','_posixsubprocess*.so'))
if not c: print('no-so'); raise SystemExit(0)
s=u.spec_from_file_location('_posixsubprocess', c[0]); m=u.module_from_spec(s); s.loader.exec_module(m)
args=(['sh','-c','echo FORKEXEC > $MARKDIR/forkexec_marker'], None, None, None, None, None)
print('fork_exec present', hasattr(m,'fork_exec'))
"

# run every subject exactly as the counter does: python3 -B SANDBOX subject, cwd=work, minimal env
for f in "$SUBJ"/*.py; do
  n=$(basename "$f" .py)
  out=$(cd "$WORK" && env -i PATH=/usr/bin:/bin HOME="$WORK" TMPDIR="$WORK/tmp" python3 -B "$SB/sandbox.py" "$f" < /dev/null 2> "$SB/$n.err" ; echo "RC=$?")
  rc=${out##*RC=}; body=$(echo "$out" | sed '$d' | head -c 160 | tr '\n' ' ')
  err=$(tail -n 1 "$SB/$n.err" | head -c 200)
  mk=absent; ls "$MARKDIR"/*_marker >/dev/null 2>&1 && mk=present
  echo "SUBJ $n rc=$rc stdout=[${body}] stderr_last=[${err:-<none>}]"
done
echo "--- markers present in sandbox work:"
ls -la "$MARKDIR" | grep -E '_marker' || echo "none"
echo "--- symlinks created in subject tree:"
ls -la "$SUBJ" | grep -- '->' || echo none
