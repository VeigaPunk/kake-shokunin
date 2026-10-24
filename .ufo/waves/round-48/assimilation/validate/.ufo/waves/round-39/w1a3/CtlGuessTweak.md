PARTIAL: L1-authorized critic fallback: materialize this diff over the committed base as `/fast/scratch/hyaku/kake-r39a3w1/CtlGuessTweak/control.py`; no implementation or interpreter was run by this seat.
Axes: operability (contract-correct findings, bounded exact-decimal handling); freshness unchanged (offline only).
Base: `.ufo/waves/round-39/a3-controls/dead-w1/CtlCodeGuess.py` at `72edf2123f92b9dc546494cbffcc777ed3c3cd3a`, SHA256 `1d0a5d9f1ff859b1b7ba403b4ee4e5e775306de24103902bb27c10b590958448`.
[INFERENCE] Counterexamples: base:54–74 accepts `&#0;` and crashes expanding `&#1114112;`; base:213,405 wrongly expands literal CDATA; base:259 treats escaped namespace URIs literally; base:327 converts unrestricted decimal digits to integers. Contract:38–43,60–61,84–86 requires different behavior.
Smallest proposed corrections below: 24 changed lines by static count, no new parser/tree/import. These are fixable defects, not evidence of 24/24 or saturation; only the canonical scorer can establish the score.
Executed, exit 0: `timeout 30s sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-39/a3-controls/dead-w1/CtlCodeGuess.py` (base hash above).
Executed, exit 0: `timeout 30s git -C /home/vgpnk/Projects/shokunin/kake-shokunin log -1 --format=%H -- .ufo/waves/round-39/a3-controls/dead-w1/CtlCodeGuess.py` (commit above).
Executed, exit 0: `timeout 30s git -C /home/vgpnk/Projects/shokunin/kake-shokunin cat-file -e 72edf2123f92b9dc546494cbffcc777ed3c3cd3a:.ufo/waves/round-39/a3-controls/dead-w1/CtlCodeGuess.py`.
Executed, exit 0: `timeout 30s git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 72edf2123f92b9dc546494cbffcc777ed3c3cd3a:.ufo/waves/round-39/a3-controls/dead-w1/CtlCodeGuess.py | sha256sum` (same base hash).
```diff
--- a/control.py
+++ b/control.py
@@ -30 +30 @@
-_ENT_RE = re.compile(r"&(#\d+|#[xX][0-9a-fA-F]+|amp|lt|gt|quot|apos);")
+_ENT_RE = re.compile(r"&(#[0-9]+|#x[0-9a-fA-F]+|amp|lt|gt|quot|apos);")
@@ -58,0 +59,4 @@
+    try:
+        _check_chars(_expand(s))
+    except (ValueError, OverflowError):
+        raise Malformed("invalid character reference")
@@ -71 +75 @@
-            return chr(int(ent[1:]))
+            return chr(int(ent[1:].lstrip("0") or "0"))
@@ -170 +174,2 @@
-        attrs.append((aname, text[j:end]))
+        _check_text(text[j:end])
+        attrs.append((aname, _expand(text[j:end])))
@@ -213 +218 @@
-                yield ("text", text[pos + 9 : end])
+                yield ("literal", text[pos + 9 : end])
@@ -327,4 +332,3 @@
-    num = int(ip or "0") * (10 ** len(fp)) + int(fp or "0")
-    if neg:
-        num = -num
-    return 0 <= num <= 10 ** len(fp)
+    ip = ip.lstrip("0") or "0"
+    zero = ip == "0" and not fp.strip("0")
+    return (not neg or zero) and (ip == "0" or (ip == "1" and not fp.strip("0")))
@@ -402 +406 @@
-        if kind == "text":
+        if kind in ("text", "literal"):
@@ -405 +409 @@
-                    fr["capture"].append(_expand(ev[1]))
+                    fr["capture"].append(_expand(ev[1]) if kind == "text" else ev[1])
```
Materialize `/fast/scratch/hyaku/kake-r39a3w1/CtlGuessTweak/NOTE.md` with these three lines:
```text
Shape: inherited streaming text scanner and keyword checks; no XML/HTML library or tag tree.
Tweak: validate references/attributes, preserve CDATA, compare decimal priorities lexically.
Deliberately skips complete XML namespace/name/declaration/comment grammar; no network or freshness inference.
```
Five self-test specifications, NOT RUN or written: under `t/<name>/`, use `manifest.json` = `{"version":1,"checks":[{"id":"t","file":"s.xml","sitemapUrl":"https://e.test/s.xml"}]}`; default XML is `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://e.test/</loc></url></urlset>`.
1. `namespace`: replace namespace suffix `0.9` with `0.&#57;`; expected clean, exit 0.
2. `zero-ref`: replace loc value with `https://e.test/&#0;`; expected only file-level `xml_malformed`, exit 1.
3. `range-ref`: replace loc value with `https://e.test/&#1114112;`; expected only file-level `xml_malformed`, exit 1.
4. `literal-cdata`: loc value `<![CDATA[https://e.test/&#1114112;]]>`; expected clean, exit 0.
5. `exact-priority`: insert `<priority>0.` followed by 5000 ASCII zeroes and `</priority>` before `</url>`; expected clean, exit 0.
L1 must materialize, hash and self-test the proposal; no runnable-file SHA256 or test pass is claimed. The role prohibition on editing/invoking another runtime prevented those steps here.
No sealed key, receipt rows, reference implementation, counter, network, installs or other lane writes accessed; no started processes remain. Report is the sole written deliverable.
