Verdict: valid control — M03 breaks contract sentence 4; the reference obeys it.

Target: w1a3-MutUrlAuthority__M03 (receipt: passed 24/24, met=true, toolSha256 f867398e…b886).
Mutant: /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/mutants/M03.py, sha256 f867398ec86b38fe9c4941ff7aa11d71541028287b5a6a0bf3156ad2fbebb886 (matches receipt + mutants.json).

Diff vs /fast/scratch/hyaku/kake-r39a3w1/shared/reference.py (sha256 663e051e…f8): exactly one changed line, M03.py:215 —
    -  or absurl(c["sitemapUrl"]) is None:
    +  or absurl(c["sitemapUrl"]) is None or urlsplit(c["sitemapUrl"]).netloc.endswith(":"):
i.e. the mutant additionally marks a check check_invalid when the sitemapUrl authority ends with a bare ':' (empty port). Confirmed `changed_line_count: 1`.

Commands (cwd /fast/scratch/hyaku/kake-r39a3w1/MutUrlAuthority/witnesses/M03; manifest sitemapUrl = "https://example.test:/s.xml"):
    timeout 60 python3 -B .../shared/reference.py --manifest manifest.json   → exit 0
    {"version": 1, "verdict": "clean", "checks": [{"id": "w", "status": "clean", "error": null, "findings": []}]}
    timeout 60 python3 -B .../mutants/M03.py --manifest manifest.json        → exit 2
    {"version": 1, "verdict": "could-not-evaluate", "checks": [{"id": "w", "status": "error", "error": "check_invalid", "findings": []}]}
Outputs match mutants.json reference_output / mutant_output byte-for-byte.

Sentence 4 (c1-contract.md:22-25): "Each check is an object with string members `id`, `file`, `sitemapUrl`. A check that is not an object, lacks one of them, has a non-string one, repeats an earlier check's `id`, has a `file` that is absolute or has a `..` path segment, or has a `sitemapUrl` that is not an absolute `http`/`https` URL with a host, is an error check with error `check_invalid`."

Reasoning: the witness sitemapUrl `https://example.test:/s.xml` IS an absolute https URL with a host — RFC 3986 grammar permits an empty port (`port = *DIGIT`), and urlsplit parses it as hostname='example.test', port=None (verified). None of sentence 4's exhaustive invalidity conditions apply, so the contract requires this check to be evaluated, not errored. The reference does so (audit proceeds; loc https://example.test/a is in scope since the missing/empty port defaults to 443 per sentence 24 → clean, exit 0). The mutant rejects the check (check_invalid, exit 2) — a plainly observable contract violation on this witness, and likewise on any input with an empty-port authority (e.g. http://h:/x, userinfo variants). Not equivalent, not contract-silent. The mutant only ever adds rejections, so its other outputs are unchanged; the divergence is real and sentence-4-determined.

Attacked statement: sentence 4 — holds for the reference; the mutant breaks it. Consistent with kill rule (1) firing correctly (mutant observable-behavior-differs from reference on a contract-decided input, and the reference's behavior is the contract-correct one). Consistent with the 24/24 kill receipt.

Residual risk: none identified; single-line mutation, witness divergence reproduced independently of the seat's recorded outputs.
