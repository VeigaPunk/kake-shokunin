#!/usr/bin/env python3
"""Install the ported selftest into c57_quote_truth.py (run AFTER derive_c57_quote_truth.py; idempotent on its output).

The block is `w1/ExecC3Selftest.files/c57_quote_truth_selftest.py` (wave-1 seat ExecC3Selftest, 93/93 against counter version 1) with
the version-2 edits: the baseline needs no change; version-2 fixtures (sidebar markup span, style-block CSS span, a body swapped
together with its receipt, a substring-only row title, a sidebar heading as anchor, the page's own fullwidth-colon date form, a long
URL span in the Gate line, an unrelated extra source body) and their kill-matrix rows are added."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "w1/ExecC3Selftest.files/c57_quote_truth_selftest.py"), encoding="utf-8").read()
a = src.index("# --------------------------------------------------------------------------- selftest")
b = src.index("def main() -> int:")
block = src[a:b]
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
    def _(f): dual(f, REGISTRY, row(f, "S421"), row(f, "S421").replace("(发布日期 2022-09-09)", "(发布日期：2022-09-09)"))

    @case("fail_gate_long_url_span", note="character ceiling")
    def _(f):
        g = gate_line_of(f, "S421")
        f[LESSON] = f[LESSON].replace(g, g + ' "https://ziyuan.baidu.com/college/articleinfo?id=3458&x=1"')

    @case("pass_unrelated_source_body_present", 0)
    def _(f): f[f"{SOURCES_DIR}/S999.html"] = f[f"{SOURCES_DIR}/S421.html"]  # a later body must not flip a committed entry's verdict
'''
marker = "    # Kill matrix:"
assert marker in block
block = block.replace(marker, new_cases + "\n" + marker, 1)
kills_add = '''        "fail_sidebar_markup_span": "C5_quote_truth",
        "fail_style_css_span": "C5_quote_truth",
        "fail_body_swapped_with_receipt": "C5_quote_truth",
        "fail_row_title_substring_only": "C5_quote_truth",
        "fail_anchor_sidebar_heading": "C5_quote_truth",
        "fail_gate_long_url_span": "C5_quote_truth",
'''
k = "    kills = {\n"
assert k in block
block = block.replace(k, k + kills_add, 1)
cur = open(os.path.join(HERE, "c57_quote_truth.py"), encoding="utf-8").read()
i = cur.index("# --------------------------------------------------------------------------- selftest")
j = cur.index("def main() -> int:")
cur = cur[:i] + block + cur[j:]
cur = cur.replace("Version 1 (frozen before any seat scored).", "Version 1 was frozen at `b9a5d012f7fd`; version 2 (after wave 1, before any claim was measured; attacks `w1/CriticC3Counter.md`, `w1/CritCheatC3.md`,\n`w1/CriticControlsSizing.md`): bodies pinned by sha256 in code, article block narrowed to text nodes between a start and an end marker (no style, no\nsidebar, no promo), row title equal to the page `<title>` text, anchor heading 4+ units and page-unique inside the block, the page's own printed date\nread in a text node, every Gate-line span checked against both ceilings, the sibling set frozen to the two adopted bodies, and the ported selftest\n(`derive_c57_selftest.py`). Predicate unchanged.", 1)
open(os.path.join(HERE, "c57_quote_truth.py"), "w", encoding="utf-8").write(cur)
