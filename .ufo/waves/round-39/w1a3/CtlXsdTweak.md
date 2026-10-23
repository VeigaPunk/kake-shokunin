PARTIAL: Static, unapplied proposal only: the critic role prohibits code edits and runtime execution; L1's requested report-diff handoff is used. Axes: operability (assigned), freshness metadata conformance (secondary). No tests, counter, score, or changed-line command was run; no control.py or NOTE.md was created. Command: `timeout 5s sha256sum /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-39/a3-controls/dead-w1/CtlXsdDelegate.py` exited 0; SHA256=72a614fc9adf992877cd40f24ee8d59e8bd46f4a4071ae968d5250dfaa5bfa14. No tools installed. No receipt rows, key, or reference implementation accessed.
Evidence: B=/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-39/a3-controls/dead-w1/CtlXsdDelegate.py; C=/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-39/c1-contract.md. B:395 misses ValueError: manifest {"version":1,"checks":[{"id":"nul","file":"a\u0000.xml","sitemapUrl":"https://example.invalid/sitemap.xml"}]} reaches open(), rather than C:26-27's file_unreadable JSON. B:407 trims an encoding declaration value, so `encoding=" UTF-8 "` can reach xml_malformed instead of C:34-37's encoding_invalid. These are static traces, not exercised results. Strongest remaining shape counterexample: a matching-host urlset with loc=https://example.invalid/a and lastmod=2026-10-23T12:34:56 has an XSD-valid timezone-less dateTime (B:94-101,474), while C:74-80 requires lastmod_invalid; adding that profile restriction or scope would violate the control assignment. B:4 overstates provenance: B:299-317 constructs synthetic one-field documents, not full-input schema validation. B:350-351,369-370 retain fail-open behavior when the schema engine is unavailable; do not call that successful validation.
Smallest proposed correction: the zero-context unified diff below removes optional third-party Python imports and fixes the two existing error paths, with 46 nonblank added/deleted lines by static count (not an exercised diff count); apply against B and materialize at /fast/scratch/hyaku/kake-r39a3w1/CtlXsdTweak/control.py. /usr/bin/xmllint exists by glob, but this remains an external executable dependency, not a proven strictly-stdlib-only runtime. Proposed /fast/scratch/hyaku/kake-r39a3w1/CtlXsdTweak/NOTE.md text (one line): "Shape: stdlib XML envelope checks plus embedded sitemaps.org XSD field validation via /usr/bin/xmllint; not full-document schema validation. Deliberately skips scope and W3C-profile lastmod tightening; retains original fail-open engine fallback." L1 must materialize, record the resulting control SHA256 and actual diff count, and run the requested 3–5 small-manifest self-tests; no unrun check is claimed passed.
```diff
--- a/.ufo/waves/round-39/a3-controls/dead-w1/CtlXsdDelegate.py
+++ b/control.py
@@ -281,11 +280,0 @@
-    try:
-        from lxml import etree
-    except Exception:
-        etree = None
-    if etree is not None:
-        try:
-            parser = etree.XMLParser(resolve_entities=False, no_network=True,
-                                     load_dtd=False, recover=False, huge_tree=False)
-            return etree.fromstring(data, parser)
-        except Exception:
-            return None
@@ -301,10 +289,0 @@
-    try:
-        from lxml import etree
-    except Exception:
-        etree = None
-    if etree is not None:
-        root = etree.Element("{%s}%s" % (NS, rootname), nsmap={None: NS})
-        ent = etree.SubElement(root, "{%s}%s" % (NS, entname))
-        etree.SubElement(ent, "{%s}loc" % NS).text = "http://example.com/a"
-        etree.SubElement(ent, "{%s}%s" % (NS, field)).text = value
-        return etree.tostring(root, encoding="utf-8")
@@ -328,11 +306,0 @@
-        try:
-            from lxml import etree
-        except Exception:
-            etree = None
-        if etree is not None:
-            try:
-                self.schemas["urlset"] = etree.XMLSchema(etree.fromstring(XSD_URLSET.encode("utf-8")))
-                self.schemas["sitemapindex"] = etree.XMLSchema(etree.fromstring(XSD_SITEMAPINDEX.encode("utf-8")))
-                self.mode = "lxml"
-            except Exception:
-                self.schemas = {}
@@ -355,10 +322,0 @@
-        if self.mode == "lxml":
-            from lxml import etree
-            try:
-                parsed = etree.fromstring(doc)
-            except Exception:
-                return False
-            try:
-                return bool(self.schemas[kind].validate(parsed))
-            except Exception:
-                return True
@@ -395 +353 @@
-    except OSError:
+    except (OSError, ValueError):
@@ -407 +365 @@
-    if enc is not None and enc.strip().lower() != "utf-8":
+    if enc is not None and enc.lower() != "utf-8":
```
