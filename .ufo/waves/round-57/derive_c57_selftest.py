#!/usr/bin/env python3
"""Install the ported selftest into c57_quote_truth.py (run AFTER derive_c57_quote_truth.py; idempotent on its output).

The block is `w1/ExecC3Selftest.files/c57_quote_truth_selftest.py` (wave-1 seat ExecC3Selftest, 93/93 against counter version 1) with the version-2 fixtures
(sidebar markup span, style-block CSS span, a body swapped together with its receipt, a substring-only row title, a sidebar heading as anchor, the page's
own fullwidth-colon date form, a long URL span in the Gate line, an unrelated extra source body) and the version-2.1 fixtures (the wave-2 mutation survivors
of `w2/MutC3Counter.md`, the anchor with a parenthetical, every Gate-line span, the Gate line's typed fields, the topic anchor, the source URL, an unreadable
base revision, the CLI usage exit) with their kill-matrix rows."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "w1/ExecC3Selftest.files/c57_quote_truth_selftest.py"), encoding="utf-8").read()
a = src.index("# --------------------------------------------------------------------------- selftest")
b = src.index("def main() -> int:")
block = src[a:b]

# the fixture Gate lines carry the typed fields the version-2.1 counter reads (sha256 and byte count of the retained body)
block = block.replace("(9 units; raw substring of the retained body, HTTP 200)", "(9 units; raw substring of the retained body, sha256 @H421@, @B421@ bytes, HTTP 200)")
block = block.replace("(12 units; raw substring of the retained body, HTTP 200)", "(12 units; raw substring of the retained body, sha256 @H422@, @B422@ bytes, HTTP 200)")
assert '@case("pass_gate_extra_short_quote", 0)' in block
block = block.replace('@case("pass_gate_extra_short_quote", 0)', '@case("fail_gate_extra_short_quote_not_in_body", note="not a raw substring of the retained body")')
assert "LESSON: _FX_LESSON," in block
block = block.replace("LESSON: _FX_LESSON,", """LESSON: _FX_LESSON.replace("@H421@", hashlib.sha256(bodies["S421"].encode("utf-8")).hexdigest()).replace("@B421@", str(len(bodies["S421"].encode("utf-8")))).replace("@H422@", hashlib.sha256(bodies["S422"].encode("utf-8")).hexdigest()).replace("@B422@", str(len(bodies["S422"].encode("utf-8")))),""")

new_cases = '''
    # --- version 2 (after wave 1): counter attacks w1/CriticC3Counter A1-A5, W1; w1/CritCheatC3

    @case("fail_sidebar_markup_span", note="outside the page's content block")
    def _(f): add_entry_line(f, "S421", '\\n> "搜索内容选题技巧</a>"\\n')  # recommended-reading markup, page-unique, was inside the version-1 window

    @case("fail_style_css_span", note="outside the page's content block")
    def _(f): add_entry_line(f, "S422", '\\n> "{ margin: 0cm 0cm 0.0001pt; text-align:"\\n')  # the in-window <style> block

    @case("fail_body_swapped_with_receipt", note="frozen at the contract commit")
    def _(f):
        raw = f[f"{SOURCES_DIR}/S421.html"] + "<!-- edited -->"
        f[f"{SOURCES_DIR}/S421.html"] = raw
        r = jload(f, RECEIPTS)
        r["sources"]["S421"]["sha256"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        r["sources"]["S421"]["bytes"] = len(raw.encode("utf-8"))
        f[RECEIPTS] = jdump(r)

    @case("fail_row_title_substring_only", note="is not the page's <title> text")
    def _(f): dual(f, REGISTRY, row(f, "S421"), row(f, "S421").replace(_FX_TITLE["S421"], "死链"))

    @case("fail_anchor_sidebar_heading", note="is not 4+ units, page-unique and inside an article text node")
    def _(f): dual(f, REGISTRY, row(f, "S421"), row(f, "S421").replace("§ 一、了解死链", "§ 推荐阅读"))

    @case("pass_anchor_fullwidth_colon_date", 0)
    def _(f):
        dual(f, REGISTRY, row(f, "S421"), row(f, "S421").replace("(发布日期 2022-09-09)", "(发布日期：2022-09-09)"))
        g = gate_line_of(f, "S421")
        f[LESSON] = f[LESSON].replace(g, g.replace("(发布日期 2022-09-09)", "(发布日期：2022-09-09)"))

    @case("fail_gate_long_url_span", note="character ceiling")
    def _(f):
        g = gate_line_of(f, "S421")
        f[LESSON] = f[LESSON].replace(g, g + ' "https://ziyuan.baidu.com/college/articleinfo?id=3458&x=1"')

    @case("pass_unrelated_source_body_present", 0)
    def _(f): f[f"{SOURCES_DIR}/S999.html"] = f[f"{SOURCES_DIR}/S421.html"]  # a later body must not flip a committed entry's verdict

    # --- version 2.1 (after wave 2): w2/ReviewerC3CounterCode F1/F4, w2/MutC3Counter survivors, w2/CritCheatC3V2 E8/E9

    @case("fail_anchor_with_parenthetical_absent_from_page", note="is not 4+ units, page-unique and inside an article text node")
    def _(f): dual(f, REGISTRY, row(f, "S421"), row(f, "S421").replace("§ 一、了解死链 (发布日期", "§ 一、了解死链 (附注：页面并未印出) (发布日期"))

    @case("fail_anchor_cell_not_the_declared_shape", note="is not `§ <heading> (发布日期 YYYY-MM-DD)`")
    def _(f): dual(f, REGISTRY, row(f, "S421"), row(f, "S421").replace("§ 一、了解死链 (发布日期 2022-09-09)", "一、了解死链 发布日期 2022-09-09"))

    @case("fail_gate_line_extra_nonsubstring_spans", note="not a raw substring of the retained body")
    def _(f):
        g = gate_line_of(f, "S421")
        f[LESSON] = f[LESSON].replace(g, g + ' "QQQ" "ZZZ"')

    @case("fail_gate_line_wrong_sha256", note="does not carry the retained body's sha256")
    def _(f):
        g = gate_line_of(f, "S421")
        f[LESSON] = f[LESSON].replace(g, re.sub(r"sha256 [0-9a-f]{64}", "sha256 " + "0" * 64, g))

    @case("fail_gate_line_wrong_byte_count", note="does not carry the retained body's sha256 and byte count")
    def _(f):
        g = gate_line_of(f, "S422")
        f[LESSON] = f[LESSON].replace(g, re.sub(r"\\d+ bytes", "1 bytes", g))

    @case("fail_gate_line_wrong_units", note="does not state 9 units for its quote")
    def _(f):
        g = gate_line_of(f, "S421")
        f[LESSON] = f[LESSON].replace(g, g.replace("(9 units;", "(5 units;"))

    @case("fail_gate_line_other_anchor", note="does not carry the registry row's anchor cell")
    def _(f):
        g = gate_line_of(f, "S421")
        f[LESSON] = f[LESSON].replace(g, g.replace("§ 一、了解死链", "§ 二、死链处理"))

    @case("fail_gate_quote_off_topic", note="no Gate quote carries the page-named subject")
    def _(f):
        g = gate_line_of(f, "S422")
        q = re.findall(r'"([^"]+)"', g)[-1]
        f[LESSON] = f[LESSON].replace(g, g.replace(q, "近期百度搜索最大的动作应该就是百度").replace("(12 units;", "(17 units;"))

    @case("fail_entry_without_topic_span", note="no page-unique span of the entry carries the page-named subject")
    def _(f):
        head = _FX_ENTRY["S422"].split("# The crawler upgrade")[0]
        set_entry(f, "S422", head + "# The crawler upgrade\\n\\nOff-topic spans only [S422].\\n\\n> \\"近期百度搜索最大的动作应该就是百度\\"\\n> \\"此次升级是把当前离线、\\"\\n> \\"全量计算为主的系统，改造成实时、\\"\\n")

    @case("fail_entry_source_url_other", note="does not carry the row URL")
    def _(f): set_entry(f, "S421", f[ADOPTED["S421"]].replace(ROW_URL["S421"], "https://ziyuan.baidu.com/college/articleinfo?id=1", 1))

    # the mutation survivors of w2/MutC3Counter (validated by that seat against the named mutants)
    @case("fail_m408_anchor_floor_three_units", note="is not 4+ units, page-unique and inside an article text node")
    def _(f): dual(f, REGISTRY, row(f, "S421"), row(f, "S421").replace("§ 一、了解死链", "§ 一定是"))

    @case("pass_m408_gate_span_floor_five_units", 0)
    def _(f):
        g = gate_line_of(f, "S421")
        f[LESSON] = f[LESSON].replace(g, g + ' and "不支持目录"')

    @case("pass_m408_char_ceiling_boundary_40", 0)
    def _(f): add_entry_line(f, "S421", '\\n> "面URL时，因为URL中有不规则字符，或者URL与后边的文字链接起来，导致URL"\\n')

    @case("fail_m408_unit_ceiling_26_units", note="26 units, ceiling 25")
    def _(f): add_entry_line(f, "S422", '\\n> "在这我们不得不再提一下百度站长平台链接提交中的主动推"\\n')

    @case("fail_m408_promo_span_outside_content", note="outside the page's content block")
    def _(f): add_entry_line(f, "S421", '\\n> "推荐阅读"\\n')

    @case("fail_m408_gate_own_duplicate", note="more than once in its own body")
    def _(f):
        g = gate_line_of(f, "S421")
        f[LESSON] = f[LESSON].replace(g, g + ' and "学习如何快速处理网站死链"')

    @case("fail_m408_char_ceiling_41_chars", note="character ceiling")
    def _(f): add_entry_line(f, "S421", '\\n> "，比如您的网站为example.com，您已制作了一个silian_ exampl"\\n')
'''
marker = "    # Kill matrix:"
assert marker in block
block = block.replace(marker, new_cases + "\n" + marker, 1)
kills_add = """        "fail_gate_extra_short_quote_not_in_body": "C5_quote_truth",
        "fail_sidebar_markup_span": "C5_quote_truth",
        "fail_style_css_span": "C5_quote_truth",
        "fail_body_swapped_with_receipt": "C5_quote_truth",
        "fail_row_title_substring_only": "C5_quote_truth",
        "fail_anchor_sidebar_heading": "C5_quote_truth",
        "fail_gate_long_url_span": "C5_quote_truth",
        "fail_anchor_with_parenthetical_absent_from_page": "C5_quote_truth",
        "fail_anchor_cell_not_the_declared_shape": "C5_quote_truth",
        "fail_gate_line_extra_nonsubstring_spans": "C5_quote_truth",
        "fail_gate_line_wrong_sha256": "C5_quote_truth",
        "fail_gate_line_wrong_byte_count": "C5_quote_truth",
        "fail_gate_line_wrong_units": "C5_quote_truth",
        "fail_gate_line_other_anchor": "C5_quote_truth",
        "fail_gate_quote_off_topic": "C5_quote_truth",
        "fail_entry_without_topic_span": "C5_quote_truth",
        "fail_entry_source_url_other": "C2_entry_provenance",
        "fail_m408_anchor_floor_three_units": "C5_quote_truth",
        "fail_m408_unit_ceiling_26_units": "C5_quote_truth",
        "fail_m408_promo_span_outside_content": "C5_quote_truth",
        "fail_m408_gate_own_duplicate": "C5_quote_truth",
        "fail_m408_char_ceiling_41_chars": "C5_quote_truth",
"""
k = "    kills = {\n"
assert k in block
block = block.replace(k, k + kills_add, 1)

# extra checks outside the sandbox cases: an unreadable base revision is unevaluable (exit 2) and an argparse error exits 64
extra_checks = '''
    unreadable_ok = False
    sb_files = dict(real)
    d_u, tip_u, base_u = _build(sb_files, pre)
    try:
        code_u, res_u = run_checks(d_u, tip_u, "0" * 40)
        unreadable_ok = code_u == 2 and any(r["state"] == "unevaluable" for r in res_u)
    finally:
        shutil.rmtree(d_u, ignore_errors=True)
    p_u = subprocess.run([sys.executable, "-B", os.path.abspath(__file__), "--revisionn", "x"], capture_output=True, text=True)
    usage_ok = p_u.returncode == 64
    unit_checks["an unreadable base revision is unevaluable, not 'mirror differs' (exit 2)"] = unreadable_ok
    unit_checks["an argparse usage error exits 64, not 2"] = usage_ok
'''
anchor = "    baseline_conditions = 0\n"
assert anchor in block
block = block.replace(anchor, extra_checks + anchor, 1)
block = block.replace("def selftest() -> int:\n", "def selftest() -> int:\n    for _k in [k for k in os.environ if k.startswith('GIT_')]:\n        os.environ.pop(_k)  # an inherited GIT_DIR would redirect the sandbox commits (w2/SentinelRound F2)\n", 1)

cur = open(os.path.join(HERE, "c57_quote_truth.py"), encoding="utf-8").read()
i = cur.index("# --------------------------------------------------------------------------- selftest")
j = cur.index("def main() -> int:")
cur = cur[:i] + block + cur[j:]
cur = cur.replace("Version 1 (frozen before any seat scored).", "Version 1 was frozen at `b9a5d012f7fd`; version 2 (after wave 1, before any claim was measured; attacks `w1/CriticC3Counter.md`, `w1/CritCheatC3.md`,\n`w1/CriticControlsSizing.md`): bodies pinned by sha256 in code, article block narrowed to text nodes between a start and an end marker (no style, no\nsidebar, no promo), row title equal to the page `<title>` text, anchor heading 4+ units and page-unique inside the block, the page's own printed date\nread in a text node, every Gate-line span checked against both ceilings, the sibling set frozen to the two adopted bodies, and the ported selftest\n(`derive_c57_selftest.py`). Version 2.1 (after wave 2, before any claim was measured; attacks `w2/ReviewerC3CounterCode.md`, `w2/MutC3Counter.md`, `w2/CritCheatC3V2.md`):\nthe anchor cell is parsed whole, the Gate line carries the body's sha256, byte count, unit count and the row's anchor, the page-named subject (死链) must appear in a\nGate quote and in a page-unique entry span, the entry's `source:` line carries the row URL, an unreadable base revision is unevaluable (exit 2), a usage error exits 64,\nand the wave-2 mutation survivors are fixtures. Predicate unchanged.", 1)
open(os.path.join(HERE, "c57_quote_truth.py"), "w", encoding="utf-8").write(cur)
