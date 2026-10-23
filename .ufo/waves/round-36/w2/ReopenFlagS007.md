# S007 re-opened by hand — verdict: paraphrase (documented schema transcription)

Finding attacked: `realrun/audit.json` entry `{"check":"S007","reason":"quote_missing"}`;
input quote `` `cname`: required, string or null `` (`realrun/input.json`, `from: round-20.md`).

## Commands and observed output (sandbox /fast/scratch/hyaku/kake-r36w2/ReopenFlagS007/)

1. `curl -sS --http1.1 -o s007-live.html -D s007-noredirect.hdr https://docs.github.com/en/rest/pages/pages`
   exit 0; `HTTP/1.1 200 OK`, `Content-Length: 453447`, `Content-Type: text/html; charset=utf-8`,
   no `Location` header. sha256 `5154fabe8e530e9097ad4934c93b37bdcd296e4f8ba2bb5e71c9f7bf5b7bf4fd`.
2. `curl -sS -L -o s007-live-follow.html -w '%{http_code} %{num_redirects}' ...`
   exit 0; `status=200 redirects=0`; same sha256.
3. `tar -xJf .../realrun/snap-bodies.tar.xz ./S007.body` exit 0; `S007.body` sha256 is the same
   `5154fabe...` and byte-identical to the live body (`same bytes: True`). The page has not changed
   since the recorded fetch, so this is not a freshness signal.
4. Repro with the landed tool's own functions (`source_recheck.py` at `4d5b3d55`), live bytes:
   normalized quote in extracted text `False`; in raw HTML `False`; raw text contains
   `cname: required` `False`.
5. `python3 -B scripts/source_recheck.py --manifest <repro>.json`:
   - quote = the Gate string -> `{"verdict":"failed-policy","checksEvaluated":1,"findings":[{"check":"S007","reason":"quote_missing"}]}` exit 1;
   - quote = `cname string or null` -> `{"verdict":"clean","checksEvaluated":1,"findings":[]}` exit 0;
   - quote = `"cname": "developer.github.com"` -> `{"verdict":"clean",...,"findings":[]}` exit 0.

## Live text found (quoted from the saved body)

Visible rendered table: `Body parametersName, Type, Descriptioncname string or null Specify a custom
domain for the repository. Sending a null value will remove the custom domain.`
Response example: `"cname": "developer.github.com",`.
Embedded page data inside `<script>` (removed by contract bullet (c), so never visible text):
`"cname":{"description":"The Pages site's custom domain","type":["string","null"]}` and
`"required":["url","status","cname","custom_404","public"]`.
Update-body parameter: `{"type":"string or null","name":"cname",...}` with no `required` flag — so
"required" is a property of the **response schema**, not of the update body.

## Verdict and reasoning

**Paraphrase**, with the finding literal-true but freshness-empty.
- The Gate quote is a schema transcription: `required` exists only as a key/array in the
  script-embedded OpenAPI document, and `string or null` is a JSON type array, never printed as the
  sentence "`` `cname`: required, string or null ``". No normalization (NFKC, whitespace deletion,
  case-sensitive, bullet (d)) can make it a substring, in raw or extracted bytes.
- Therefore the tool did not miss an existing literal; there is no extraction-rule bug and no
  JS-rendered-content loss for this string. `quote_missing` is the contract-correct answer for a
  non-verbatim citation.
- The underlying claim is supported on the live page: response schema lists `cname` in `required`
  and types it `["string","null"]`.
- The row URL is correct as written: HTTP 200 on the first hop, no redirect, `text/html` is a
  supported type, so no `moved`, no `gone`, no `unsupported_type`.
- This is already documented by the lane: `corpus/knowledge/ghp-custom-domain.md:50-57` (round-20
  erratum, "a schema transcription, not a verbatim quotation ... which reads 'cname string or
  null'"), yet `corpus/lessons/round-20.md:209` still carries the notation quote and is the source
  the real-run input was built from. The finding will recur until that Gate quote is replaced with a
  rendered literal (e.g. `cname string or null`, or the response-example line), or until the audit
  records known transcription quotes as expected misses rather than findings.

## Artifacts (all under /fast/scratch/hyaku/kake-r36w2/ReopenFlagS007/)

- `s007-live.html`, `s007-live-follow.html` — sha256 `5154fabe8e530e9097ad4934c93b37bdcd296e4f8ba2bb5e71c9f7bf5b7bf4fd` (453447 bytes)
- `S007.body` — extracted recorded body, same sha256
- `repro-gatequote.json`, `repro-rendered.json`, `repro-example.json` — manifests used in step 5
- `s007-noredirect.hdr`, `repro-body.html`

## Not verified

No API request was made; the retired L1 Markdown representation the erratum mentions is not
retained, so I did not test it. I did not re-run the sealed counter, and I say nothing about the
other 13 real-run findings. No tools were installed or upgraded.
