source: S458 — W3C Referrer Policy, Editor’s Draft — https://w3c.github.io/webappsec-referrer-policy/ — §8.1, https://w3c.github.io/webappsec-referrer-policy/#parse-referrer-policy-from-header; independently fetched GET-only by ScribeKnowledge, retained at `.ufo/waves/round-85/w1/ScribeKnowledge/s458-referrer-policy.html` (HTTP 200, 246577 bytes, sha256 339bdd20be241c9eca2f47a18d35368af460edfc708288d90c51e094393743a6).
verified-at: 2026-11-04 — source algorithm located at retained HTML lines 1596–1621; quote at 1612–1614. Contract: base bdabc6bc8f762a16c6c19c524c4ac84528eb4bf7, frozen round-85 contract designated revision 2f042c370b5f11b84d4f8c9e5d066517aef646b8. This seat verified source text, not decoder execution or C2 acceptance.
recheck: Before relying on this living Editor’s Draft after a source change, reopen the S458 URL GET-only and relocate §8.1; compare the retained source fingerprint. Recheck candidate behavior against the frozen ten-case counter only through the assigned integrator; examples below are contract-derived expectations, not run receipts.
ground: freshness — round-85 C2, bounded field-specific decoding.
scope: Offline selection of a Referrer-Policy token from ordered response field values; not arbitrary-header equivalence, browser referrer generation, or publishing approval.

# Referrer-Policy effective token

## Source rule

S458 §8.1 initializes policy to the empty string, walks extracted header-list values, updates policy for recognized nonempty tokens, and returns policy. Located quote (23 whitespace-separated words, HTML markup removed and line whitespace normalized):

> For each token in policy-tokens, if token is a referrer policy and token is not the empty string, then set policy to token.

Location: retained HTML lines 1612–1614, §8.1 step 3. The update is repeated, so the **last recognized nonempty token wins**, not the first token, a sorted token, or a set. §11.1, retained lines 1866–1870, separately explains that unknown policy values are ignored. The source is a work-in-progress Editor’s Draft, not evidence of W3C endorsement.

## Offline command and interface

After L1 integrates the candidate, the planned command is:

```sh
printf '%s\n' '["no-referrer", "strict-origin, unknown"]' | python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/referrer_policy_effective.py
```

Expected stdout: `{"effective":"strict-origin"}` (JSON whitespace is immaterial). This command has **not** been executed by this seat.

Input is a stdin JSON list of strings containing Referrer-Policy field values, in response field order. Within each string, process comma-separated tokens left to right, stripping surrounding whitespace. Preserve both field order and token order; never sort, deduplicate as a set, or lowercase values. Recognized tokens compare case-sensitively:

- `no-referrer`
- `no-referrer-when-downgrade`
- `same-origin`
- `origin`
- `strict-origin`
- `origin-when-cross-origin`
- `strict-origin-when-cross-origin`
- `unsafe-url`

The contract requires exactly one JSON output object with only `effective`, whose value is the selected token or `""` if none is recognized. Valid decoded input exits 0 even when the selected value is empty. Invalid JSON or unsupported input shape (for example, an object or a non-string list member) fails nonzero, normally exit 1; usage errors exit 64. `--selftest` is a separate interface requiring isolated fixtures and exit-code assertions; its success alone is not publication authority.

Unknown tokens are ignored, not rejected input and not a reason to clear a previously selected token. Empty comma components likewise do not select a policy. An uppercase token is not made recognized by lowercasing. These are contract examples, not execution evidence:

| Ordered JSON field values | Expected effective token | Reason |
|---|---|---|
| `["unknown, same-origin"]` | `same-origin` | Ignore unknown, accept later known token. |
| `["origin", "unknown, unsafe-url"]` | `unsafe-url` | Continue across multiple fields in response order. |
| `["no-referrer", "strict-origin, unknown"]` | `strict-origin` | Trailing unknown does not erase selection. |
| `["NO-REFERRER"]` | `""` | Case-sensitive recognition. |
| `["unknown,"]` or `[]` | `""` | No recognized token; not a browser default assertion. |
| `[" no-referrer , strict-origin "]` | `strict-origin` | Strip surrounding whitespace, retain order. |

## Order-sensitive counterexample

`["no-referrer, strict-origin"]` selects `strict-origin`; reversing the list to `["strict-origin, no-referrer"]` selects `no-referrer`. The same distinction holds for separate fields `["no-referrer", "strict-origin"]` versus `["strict-origin", "no-referrer"]`. These pairs contain the same tokens but have different results. A blanket multiset-based `reordered` label therefore cannot establish Referrer-Policy semantic equivalence.

The existing round-84 `policy_value_class.py` remains experimental. Its frozen `policy-rewritten-equivalent` label and historical selftest receipts must not be upgraded into a field-independent semantic guarantee. This new decoder is a separate capability; it does not rewrite the old classifier or close its other defects.

## Admission and boundaries

Admit: a bounded, source-grounded claim that this field’s effective token is selected by the ordered last-recognized rule, subject to actual candidate measurement by L1. Reject: arbitrary-header reorder equivalence, a claim that all D84 defects are closed, or publication approval derived from decoder output.

The JSON adapter is the round-85 contract, not a claim to implement all HTTP header extraction or browser processing. It accepts already-isolated field values, not full header lines, raw responses, URLs, captures, or network requests. It does not calculate outgoing Referer URLs, origin relationships, redirect effects, meta/element policy precedence, or user-agent privacy overrides. An empty result means no recognized nonempty token in this input, not proof of no referrer leakage or a browser’s final default behavior. Equal selected tokens do not prove entire responses equivalent or a policy safe.

The frozen counter has ten cases; the retained r84 control-pair trial is separate from that numerator. This seat ran neither. C1 registry completion is separate from C2 decoder correctness. D84-2..4 remain explicitly open except procedural mitigations, and there is no full D84-queue closure claim. No live property request or publish/deploy authorization is granted.
