#!/bin/bash
# usage: drive.sh candidate.py  -> runs under the gate's exact sandbox argv/env, prints rc, stdout, stderr
W=/fast/scratch/hyaku/kake-r90/ExecSandbox
payload=${2:-'{"uri":"u","request_headers":{}}'}
cd $W/cwd && printf '%s' "$payload" | env -i PATH=/usr/bin:/bin LC_ALL=C.UTF-8 PYTHONIOENCODING=utf-8 /usr/bin/python3 -I -S -B $W/sandbox.py "$1"
echo "rc=$?"
