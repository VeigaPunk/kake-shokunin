PARTIAL: Critic role permits this static proposal, not code edits or Python runs; L1 must materialize the diff at /fast/scratch/hyaku/kake-r39a3w1/CtlRegexTweak/control.py. Axes: operability (affected), freshness (not measured). Counterexample: standard-namespace urlset with <x:meta/> and an entry containing both loc and x:loc (xmlns:x="urn:extension") must be clean, but [INFERENCE] baseline emits element_unexpected/null and loc_repeated/1: CtlRegexOnly.py:59-60,265-268,279-283 versus c1-contract.md:41-55. Smallest proposed semantic correction: inherited namespace tracking, extension filtering, single-pass XML-reference decoding; no score claim. Read only contract and supplied control; no receipt, key, counter, or reference read. Exact executed command: `timeout 10s sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-39/c1-contract.md /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-39/a3-controls/dead-w1/CtlRegexOnly.py` exit 0; hashes respectively 2023d295bb156b6842f69583c201a7359ce5d4d8de2d6432c1dcbba7b0351ff7 and b7667eaf223caf1045f2e5298f8759205dc5703f7a8bfea1cf66930b93d21871. No installs or processes left running.
NOTE.md proposed one-line content: "Regex-only tag scanner with inherited namespace bindings and predefined/numeric XML-reference decoding; deliberately skips full XML 1.0 attribute/name/declaration validation, namespace-reservation rules, and exhaustive well-formedness." Four UNRUN vectors for t/, common manifest {"version":1,"checks":[{"id":"t","file":"map.xml","sitemapUrl":"https://example.test/sitemap.xml"}]}: (1) `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:x="urn:extension"><x:meta/><url><loc>https://example.test/a</loc><x:loc>https://other.test/</x:loc></url></urlset>` => clean/0; (2) `<urlset xmlns="urn:wrong"><url><loc>https://example.test/a</loc></url></urlset>` => root_invalid/null, failed-policy/1; (3) `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://exam&#112;le.test/a</loc><changefreq>d&#97;ily</changefreq><priority>&#x31;</priority></url></urlset>` => clean/0; (4) `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://example.test/&bogus;</loc></url></urlset>` => xml_malformed/null, failed-policy/1. All expectations are contract-derived, not exercised verification; control bytes/hash and changed-line count require L1 materialization.
```diff
--- a/control.py
+++ b/control.py
@@ -4,2 +4,1 @@
-No XML parser at all: no xml.etree, no expat, no namespace resolution, no prefix
-binding, no entity decoding.  Document structure is recovered by scanning
+No XML parser at all. Document structure is recovered by scanning
@@ -11,3 +10,1 @@
-  * namespaces are never resolved -- any element name is judged on its local
-    name, whatever namespace or prefix binds it;
-  * entity references are not decoded (`&amp;` stays `&amp;`);
+  * namespace syntax and general XML 1.0 well-formedness remain approximate;
@@ -36 +33 @@
-    r"|<[A-Za-z_][^>]*>",
+    r"|<[A-Za-z_](?:[^>\"']|\"[^\"]*\"|'[^']*')*>",
@@ -51 +48 @@
-    __slots__ = ("name", "children", "text")
+    __slots__ = ("name", "children", "text", "ns")
@@ -60 +57 @@
-    return name.split(":")[-1]
+    return name.rsplit("}", 1)[-1].split(":")[-1] if name.startswith("http://www.sitemaps.org/schemas/sitemap/0.9}") else None
@@ -65,0 +63,7 @@
+def unescape(value):
+    entities = {"amp": "&", "lt": "<", "gt": ">", "quot": '"', "apos": "'"}
+    def replace(m):
+        if (key := m[1]) is None: raise ValueError("invalid entity")
+        if key in entities: return entities[key]
+        return chr(int(key[2:], 16) if key.startswith("#x") else int(key[1:]))
+    return re.sub(r"&(#x[0-9A-Fa-f]+|#[0-9]+|amp|lt|gt|quot|apos);|&", replace, value)
@@ -69 +73 @@
-def scan(text):
+def scan(text, decode_entities=True):
@@ -75,0 +80 @@
+        chunk = unescape(chunk) if decode_entities else chunk
@@ -93 +98 @@
-            if stack[-1].name != name:
+            if stack[-1].name.rsplit("}", 1)[-1] != name:
@@ -105 +110,6 @@
-        node = Node(name)
+        ns = dict(stack[-1].ns) if stack else {"xml": "http://www.w3.org/XML/1998/namespace"}
+        for attr, quote, value in re.findall(r"""\s+([:\w.-]+)\s*=\s*(["'])(.*?)\2""", body, re.S):
+            if attr == "xmlns" or attr.startswith("xmlns:"): ns[attr.partition(":")[2]] = unescape(value) if decode_entities else value
+        prefix, sep, lname = name.rpartition(":")
+        if decode_entities and sep and not ns.get(prefix): return None, "unbound namespace"
+        node = Node(ns.get(prefix if sep else "", "") + "}" + name); node.ns = ns
@@ -251 +261,2 @@
-    root, _why = scan(text)
+    try: root, _why = scan(text, not has_doctype(text))
+    except (ValueError, OverflowError): root = None
@@ -267 +278 @@
-        if local(c.name) != entry_tag:
+        if local(c.name) not in (None, entry_tag):
@@ -280 +291 @@
-            if local(k.name) not in allowed:
+            if local(k.name) is not None and local(k.name) not in allowed:
```
