#!/bin/sh
# PRIVATE: score the reference and every ablation with the frozen counter (--tool-file).
cd /fast/scratch/hyaku/kake-r36/<private> || exit 2
C=/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-36/sealed_count.py
rm -rf abl && mkdir abl
for a in none a_none a_410err a_204ok b_none b_anywhere b_noresolve b_firstonly b_final c_raw c_nohead c_keepcomment c_keepscript c_keepstyle c_keeptemplate c_noentity d_exact d_casefold d_collapse d_nonfkc e_allhtml e_alltext e_casesens e_noxhtml f_utf8only f_nobom f_pylatin f_nounsupported f_noquote f_labelcase g_abort g_skip g_nourlcheck g_noloc g_noescape s_ctkey s_unsure; do
  if [ $a = none ]; then cp ref.py abl/$a.py; else { echo "import os; os.environ['KAKE_ABLATE']='$a'"; cat ref.py; } > abl/$a.py; fi
  python3 -B $C --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file abl/$a.py --key-file cases.json > abl/$a.json
  echo "$a exit=$? $(python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print(d["passed"],d["met"],[r["id"] for r in d["perCase"] if not r["passed"]])' abl/$a.json)"
done
