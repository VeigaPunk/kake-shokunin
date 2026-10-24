# Round 27 input-safety review

## Scope and evidence
Static review only: `fetch_group.py`, its imported round-26 `fetch_sources.py` and `source_text.py`, and the frozen `contract.json` gateInterface. No network request was made; no source-index URLs or fetched source bodies were opened. No source edits were made. The observed `scripts/` listing did not contain `scripts/citing_set.py`, so gate implementation behavior is **UNVERIFIABLE** at this snapshot; the interface is assessed as a contract, not a demonstrated implementation.

Reviewed-file SHA-256:

- `.ufo/waves/round-27/fetch_group.py` — `0e039f20a45d4ae7234fcca72bfddd9f56525bbdde5e2cd7205734bb60e58fad`
- `.ufo/waves/round-26/fetch_sources.py` — `de43a2a814cfb8a85348a2641d0d91ef7b3756a1319b247ba5b85218288c7820`
- `.ufo/waves/round-26/source_text.py` — `55ae7abc52a5acfd95a86d96c27f12898c30e33ab63cfa7f383640120f57b7d6`
- `.ufo/waves/round-27/contract.json` — `6d2d7f51371650c2d7535c401ead613355135d18b44762c41f385d05ee7582da`

## Findings

### 1. Conditional high — root-controlled Python execution and symlink-following output writes

**Verdict:** Confirmed unsafe boundary if `--root` is an untrusted or concurrently mutable tree. The script executes helper modules loaded from that root, then writes under the lexical `fetched/` path without checking any path component or output file for symlinks. A pre-existing `fetched`, `text`, output-file, or manifest symlink can redirect writes outside the intended tree; a symlinked helper can execute code outside it.

**Exploit path (not exercised):** Run the tool against a tree where `.ufo/waves/round-26/fetch_sources.py` resolves to attacker-controlled Python, or where `.ufo/waves/round-27/fetched` / `text` / a destination file points elsewhere. Execution is as the invoking user; writes can truncate or replace external destinations.

**Evidence:**

- `fetch_group.py:8` — “`spec.loader.exec_module(m)`”
- `fetch_group.py:9` — “`(out/'text').mkdir(parents=True,exist_ok=True)`”
- `fetch_group.py:16` — “`(out/file).write_bytes(gzip.compress(body,mtime=0))`”
- `fetch_group.py:18` — “`(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')`”

**Impact:** Local code execution through dependency substitution and out-of-root file clobbering are possible when the root/worktree is not trusted. No evidence shows either condition occurred in this review.

**Smallest remediation:** Do not dynamically execute helper files from a caller-selected tree; import vetted code from the trusted tool package. Before writing, reject symlinked root/output components and destination files, and write through a verified directory handle without following symlinks. Fail closed rather than following an existing output symlink.

### 2. Medium — URL and response retention are not restricted to public, non-account sources

**Verdict:** Confirmed capability, not an observed sensitive source. `fetch_group.py` limits row IDs to S001–S006, but the parser accepts any HTTP(S) URL in those rows. The fetch path has no host, URL-userinfo, query, or redirect-destination allowlist. It records the original and returned URL and retains both raw response bytes and extracted text. No network activity or actual URL values were inspected, so whether any current row contains credentials, a private URL, or account content is **UNVERIFIABLE**.

**Exploit path (not exercised):** If one of the selected source rows contains a URL with userinfo or sensitive query values, or points/redirects to a private or account-bearing endpoint, running the fetcher sends a request to the URL accepted by `urllib` and stores the URL/final URL plus response body in the fetched directory. A URL can therefore retain credential-like URL data, and a response can retain account/private content. This is not evidence that current sources do so.

**Evidence:**

- `fetch_group.py:10–11` — “`if row not in {f'S{i:03d}' for i in range(1,7)}:continue`”
- `fetch_sources.py:31` — “`urls = re.findall(r'https?://[^\s;|]+', cells[1])`”
- `fetch_sources.py:38` — “`urllib.request.urlopen(request, timeout=60)`”
- `fetch_group.py:16` — “`(out/file).write_bytes(gzip.compress(body,mtime=0))`”
- `fetch_group.py:17` — “`manifest.append(dict(row=row,index=index,url=url,finalUrl=final,`”

**Impact:** Outbound access is broader than the stated public-document scope, and the retained manifest/body/text can contain data outside that scope. The wrapper itself supplies only a User-Agent and does not persist response headers; that does not validate the URL or sanitize the content it does retain.

**Smallest remediation:** Pin the allowed public URL set (or exact allowed hosts and paths) for S001–S006; reject URL userinfo and unapproved query values; validate every redirect destination before following it; and omit/redact sensitive URL components in the manifest. Do not fetch or retain an input that fails those checks.

### 3. Medium / UNVERIFIABLE — gate path, symlink, and Git access policy is underspecified

**Verdict:** The frozen interface states useful constraints but does not define how the future implementation enforces them. The implementation was not present in the observed `scripts/` listing, so no claim is made that the eventual gate has these defects.

**Exploit path (implementation risk, not exercised):** A relative path containing `..` is still relative; a symlink under `corpus/knowledge` can resolve outside `--root`. If the gate follows such paths while reading the full tree, it can read outside files or silently omit/alter the census. In revision mode, an unsafe Git invocation or unvalidated revision/path could read an unintended object or diverge from working-tree behavior. The interface requires blob reads but does not define local-only Git commands, revision normalization, Git symlink mode handling, or whether symlinks are rejected.

**Evidence:**

- `contract.json:27` — “`--root <dir> [--revision <commit>] --population <relative-json> --ledger <relative-json>`”
- `contract.json:28` — “`Relative paths only; no network/execution; avoid external writes.`”
- `contract.json:28` — “`Read every regular corpus/knowledge file.`”
- `contract.json:28` — “`read blobs when --revision set, working files otherwise.`”

**Impact:** Until implemented and independently checked, path confinement, symlink behavior, Git read-only behavior, and equivalent revision/working-tree coverage are not established. In particular, “relative” alone is not a traversal or symlink defense.

**Smallest remediation before implementation:** Normalize and validate `--population`/`--ledger` paths as root-relative (reject absolute paths, `..`, and symlink components); enumerate corpus entries without following symlinks and reject or explicitly report non-regular entries. In revision mode, validate the selector to a full local commit ID and use fixed-argument local tree/blob reads only—no fetch, checkout, shell, or external filters. Treat invalid paths, symlinks, and unsupported Git entries as `input_invalid` / could-not-evaluate rather than silently skipping them.
