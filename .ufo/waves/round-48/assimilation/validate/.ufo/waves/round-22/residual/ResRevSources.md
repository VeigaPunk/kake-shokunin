## Verdict

**Counterexample found:** the RFC claims match, but the recovery rows’ required source receipts are missing from the round lesson they cite in `used-by`.

## Findings

- **P3 — S028/S029 lack their required round-lesson receipts.** `CORPUS.md:107–115` defines `used-by` as paths citing a row and requires the round lesson’s Gate to record each new row’s URL, access date, and a located quote of at most 25 words. The rows at `corpus/SOURCES.md:36–37` list `corpus/lessons/round-22.md`; its Gate source table at lines 36–57 records S020–S027, not S028 or S029.
  - **Exact check:** `grep` tool, pattern `S028|S029|recipient that processes|When authority is not present`, target `corpus/lessons/round-22.md` → **`No matches found`**. The Gate table read confirms the listed receipts are S020–S027.
  - **Impacted axis:** contract-v1 provenance and `used-by` accuracy; this does not contradict the RFC facts checked below.
  - **Smallest fix:** add S028 and S029’s URL, 2026-10-21 access date, section, and short quote to the round-22 Gate; that also makes the lesson path in `used-by` accurate.

## Checked and held

- **RFC fetch and digest comparison.** In a fresh `/tmp/kake-r22a2-ResRevSources-Kh8z` directory:
  ```
  curl -fsS -o "$probe/rfc9110.txt" https://www.rfc-editor.org/rfc/rfc9110.txt
  curl -fsS -o "$probe/rfc3986.txt" https://www.rfc-editor.org/rfc/rfc3986.txt
  sha256sum "$probe/rfc9110.txt" "$probe/rfc3986.txt"
  ```
  Observed:
  ```
  21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a  rfc9110.txt
  3102dae4b68cebe40337730312fcb612297b8928547267e8b3d1ee6002b2d683  rfc3986.txt
  ```
  **Both row prefixes and displayed suffixes match**: S028 `21c1cdce…7232a`; S029 `3102dae4…b2d683`.

- **S028 — match; no overclaim in the row.** RFC 9110 §§4.2.1–4.2.2 each say: “A recipient that processes such a URI reference MUST reject it as invalid.” This matches the row’s empty-host claim. The rule is for an `http` or `https` URI reference.

- **S029 — match; no overclaim in the row.** RFC 3986 §3, immediately after the `hier-part` ABNF, says: “When authority is not present, the path cannot begin with two slash characters ("//").” The row’s inference that a `//`-prefixed reference has an authority, possibly empty, matches that grammar. Generic syntax permits an empty host: §3.2.2 has `reg-name = *( unreserved / pct-encoded / sub-delims )` and refers to “the registered name [being] empty (zero length).” Scheme rules determine whether that is valid.

- **Knowledge paragraph — no overclaim found.** RFC 9110 does not define HTML canonical-link `href` parsing; its empty-host rule applies when the processed URI is HTTP(S), not to every raw `href` under every base scheme. The paragraph states the HTTP(S) condition and describes rejection as conservative local policy; it also separately notes WHATWG browser parsing. RFC 3986’s generic grammar does allow an empty authority.

- **S010 duplication — not a contract-v1 problem.** S010 and S028 cite different RFC 9110 sections and teach different claims. The contract requires scoped claims and anchors but does not require unique source documents.

- **S020/S027 spot-check — limited by the network restriction.** I did not reopen either URL. The existing round-22 Gate records S020 §3: “Specify a relative IRI (see [RFC3986], Section 4.2).” This matches the relative-target part; the recorded quote alone does not verify the row’s other clauses. For S027 it records the `urlsplit` warning: “urlsplit() does not perform validation.” That matches the no-validation claim; I did not independently recheck the broader browser-equivalence clause. No contrary claim was established from these local records.

- **Census:** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
  ```
  kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
  exit=0
  ```

## Limits

S020 and S027 were not freshly verified against their URLs because network access was limited to the two specified RFC plain-text URLs. No packages were installed; no build, lint, or formatter was run.