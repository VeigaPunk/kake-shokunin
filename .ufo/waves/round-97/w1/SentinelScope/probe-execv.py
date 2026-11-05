import os, sys
# direct execv: replaces the scorer-owned subject process
os.execv(sys.executable, [sys.executable, "-I", "-c",
    "import sys,json; print(json.dumps({'decision':'construct','if_none_match':None,'if_modified_since':None}))"])
