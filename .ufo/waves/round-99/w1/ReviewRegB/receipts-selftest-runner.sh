set -u
S=/fast/scratch/hyaku/kake-r99/ReviewRegB
C=$S/clone
W=$S/w
mkdir -p "$S/st" "$W" "$W/tmp" "$W/cit" "$W/hostile" "$W/sidecar"
export TMPDIR=$W/tmp
cd "$C"
run() { name=$1; shift; "$@" >"$S/st/$name.out" 2>"$S/st/$name.err"; echo $? >"$S/st/$name.rc"; echo "$name rc=$(cat $S/st/$name.rc)"; }
run st01_base_path python3 -B scripts/base_path_selftest.py
run st04_citing_set python3 -B scripts/citing_set.py --selftest
run st05_citself python3 -B scripts/citing_set_selftest.py --selftest --tmpdir "$W/cit"
run st06_hostile python3 -B scripts/citing_set_hostile_selftest.py --root . --tmpdir "$W/hostile"
run st07_cond python3 -B scripts/conditional_eval.py --selftest
run st08_hcc python3 -B scripts/header_change_class.py --selftest
run st09_kml python3 -B scripts/knowledge_metatext_lint.py --selftest
run st10_landed python3 -B scripts/landed_check.py --selftest
run st11_ledger python3 -B scripts/ledger_latest_check.py --selftest
run st12_linkprev python3 -B scripts/link_preview_selftest.py
run st15_quote python3 -B scripts/quote_class.py --selftest
run st18_robots python3 -B scripts/robots_audit_selftest.py
run st20_sidecar python3 -B scripts/sidecar_reobserve.py --selftest --work "$W/sidecar"
run st21_sitemap python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py
run st22_srh python3 -B scripts/source_recheck_hardening_selftest.py
run st23_srcchk python3 -B scripts/source_recheck_selftest.py
run st25_stale python3 -B scripts/stale_extensions.py --selftest
echo ALLDONE
