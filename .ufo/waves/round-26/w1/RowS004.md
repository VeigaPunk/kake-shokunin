# RowS004 — freshness re-check (round 26)

```json
{"id":"S004","verdict":"HOLD","fetchIndex":1,"quote":"The tar file must be under 10GB in size and should not contain any symbolic or hard links","anchorObserved":"Section heading \"Configuring the upload-pages-artifact action\" (fetched/text/S004-1.txt line 1; text view is one line)","reason":"Living (unpinned) docs re-fetched 2026-10-21, status 200, sha256 5c15ef2d…: the artifact-shape sentence is verbatim unchanged under the same heading (preceded by \"The GitHub Pages artifact should be a compressed gzip archive containing a single tar file.\"), so scope and teaches still hold; the row pins no action version, and the doc's current snippets (upload-pages-artifact@v4, deploy-pages@v4, configure-pages@v5, checkout@v6) do not contradict any row cell.","correction":null}
```

## Caveat

- The 10GB bound attaches to the tar file *inside* the gzip archive, not to the archive as a whole; the row's one-line paraphrase ("gzip-compressed tar files under 10GB") stays compatible but is not literal.
- "should not contain" is advisory in the source, matching the row's "should contain no"; neither is a hard MUST, so no correction needed.
- Anchor text is still present verbatim; only surrounding version snippets drifted (v4/v5/v6 action pins), outside this row's scope.
- used-by corpus/knowledge/ghp-served-set.md:29 uses S004 only for "steps 4-5 upload static files and deploy the artifact", which the re-fetched page still supports.
- No tools installed or updated.
