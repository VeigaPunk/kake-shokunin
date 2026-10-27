import importlib.util, os, shutil, json
S="/fast/scratch/hyaku/kake-r59/MutResolverSelftest"
spec=importlib.util.spec_from_file_location("c59","/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-59/c59_resolver_cases.py")
c59=importlib.util.module_from_spec(spec); spec.loader.exec_module(c59)
LANE="/home/vgpnk/Projects/shokunin/kake-shokunin"; REV="fd6303ce5c14b3f892dec586297a942ab6e4193b"
W=S+"/work/cross2"; shutil.rmtree(W,ignore_errors=True); os.makedirs(W)
DISCRIM={"K1_fenced_heading_before_registry","K2_backtick_fence_inside_registry","K3_tilde_fence_inside_registry",
"K4_non_ascii_path_at_revision","K5_git_quoted_path_at_revision","K6_fenced_low_id_dangles_registered_high_id_resolves",
"K7_newline_path_at_revision","P1_three_space_row_resolves","P2_row_after_closed_fence_resolves",
"P3_four_space_line_is_code","P4_committed_sibling_owns","P5_absent_fleet_is_unevaluable","P7_real_lane_green"}
BASE_FAIL={"K8_html_comment_row_is_not_registered","K9_setext_heading_ends_registry","K10_in_lane_symlinked_dir_is_read",
"K11_revision_symlink_resolved_in_tree","K12_registry_outside_lane_is_unevaluable","K13_non_utf8_path_at_revision",
"K14_non_toplevel_root_is_unevaluable","P6_tool_selftest"}
SRC_TOOL="/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py"
pristine={n:ok for n,ok,_ in c59.case_results(SRC_TOOL,LANE,REV,W)}
print("pristine discriminating results:", {k:v for k,v in pristine.items() if k in DISCRIM})
data=json.load(open(S+"/mutants.json"))
summary={}
for m in data["mutants"]:
    mid=m["id"]; tool=os.path.join(S,"work",f"{mid}.py")
    if not os.path.exists(tool): continue
    res=dict((n,ok) for n,ok,_ in c59.case_results(tool,LANE,REV,W))
    newly=[n for n in DISCRIM if res[n] is False and pristine.get(n) is True]
    fixed=[n for n in BASE_FAIL if res[n] is True and pristine.get(n) is False]
    summary[mid]={"selftest_killed":m["killed"],"counter_discriminating_kills":newly,"counter_fixed_base_failures":fixed}
    print(mid, "selftest:", "KILL" if m["killed"] else "SURVIVE", "| counter discriminates:", newly or "-", "| counter fixes base-fails:", fixed or "-")
json.dump(summary, open(S+"/crosscheck2.json","w"), indent=1)
