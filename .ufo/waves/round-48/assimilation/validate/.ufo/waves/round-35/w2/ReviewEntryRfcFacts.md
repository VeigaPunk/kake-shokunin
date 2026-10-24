# ReviewEntryRfcFacts — wave 2 falsify report

Attacks: the C2 entry corpus/knowledge/security-txt-publishing.md at 95abec21 (= master 7deacc4, same sha256 0b5ac7e8…) — every sentence citing S078/S079/S082/S083, checked against retained texts.

## Method / commands
- Sandbox: /fast/scratch/hyaku/kake-r35/w2/ReviewEntryRfcFacts/clone (clone of lane, checkout -q 95abec21; exit 0).
- `sha256sum` retained texts = receipts.json textSha256 exactly (S078 4954ddcda4ca…, S079 667229665b5c…, S082 0746e9da9c24…, S083 aceda87b1290…, S084 35cf4b7ba43d…, S085 c7a10ffa520a…; exit 0).
- `git show 7deacc4:corpus/knowledge/security-txt-publishing.md | sha256sum` = 0b5ac7e83a622… = file at 95abec21 → reviewed text is exactly the landed entry.
- No live network; no tool installs (none needed). Errata DB not consulted (no named public URL authorized).

## Verdicts (entry line numbers from the file; cited id in parens)
All 27 sentences citing S078/S079/S082/S083: SUPPORTED by the retained texts (quotes below key ones).

- L20 S078: "organizations MUST place the 'security.txt' file under the '/.well-known/' path" (§3). OK.
- L21-22 S082: "Well-known URIs are rooted in the top of the path's hierarchy… '/.well-known/example' is a well-known URI, whereas '/foo/.well-known/example' is not" (§3). OK.
- L23-25 S083+S082: IANA row "security.txt | RFC 9116 | permanent | IETF | 2021-07-13" (S083, exact); "Applications that wish to mint new well-known URIs MUST register them" (§3). OK.
- L26-27 S078+S079: §3 "For legacy compatibility… might be placed at the top-level path or redirect…"; S079 "or simply as a fallback. The file can be placed in both locations… at the same time." OK.
- L28 S078: "If a 'security.txt' file is present in both locations, the one in the '/.well-known/' path MUST be used" (§3). OK (marked [INFERENCE] tail).
- L30-31 S078+S082: §5.6 "should reserve the 'security.txt' namespace at the root to ensure no third party can create a page with the 'security.txt' AND '/.well-known/security.txt' names"; §4.1 "well-known locations effectively represent the entire origin… control the ability to write to them" (paraphrase "origin-wide capability" — substance exact). OK.
- L35-36 S078+S079: §3 "MUST be accessed via HTTP 1.0 or a higher version… MUST use the 'https' scheme… Content-Type of 'text/plain' with the default charset parameter set to 'utf-8'"; S079 "Internet Media Type of text/plain and must be served over HTTPS". OK.
- L37-38 S078: §4 "encoded using UTF-8… in Net-Unicode form… MUST follow the ABNF"; §2.2 CRLF/LF; §2.1 "#" comment; §2 "Field names are case insensitive". OK.
- L39-40 S078: §3 "may result in a redirect"; §5.2 "should record any redirects". OK.
- L44-46 S078+S079: §2.5.3 "MUST always be present… 'mailto' and 'tel' URI schemes must be used… web URI… MUST begin with 'https://'"; S079 "ensure it starts with mailto:… tel:… or https://". OK.
- L47 S078: "SHOULD be listed in order of preference, with the first occurrence being the preferred method". OK.
- L48-50 S078+S079: §2.5.5 "MUST always be present and MUST NOT appear more than once… as defined in [RFC3339]… RECOMMENDED… less than a year"; S079 "date format for Expires has changed to ISO 8601" + "Only 1 allowed". OK.
- L51-52 S078+S079: §2.5.8 "MUST NOT appear more than once… separated by commas… equal priority… if absent… English… to be used"; S079 "Optional Only 1 allowed… comma-separated". OK.
- L53-54 S078: §2.5 "Unless otherwise stated, all fields MUST be considered optional"; §2 "a field MAY appear multiple times" (IANA §6.2 registry: Multiple Appearances yes for all five); each field "web URI… MUST begin with 'https://'". OK.
- L55-56 S078: §2.5.2 "canonical URIs where the 'security.txt' file is located… not listed within any canonical fields, then the contents… SHOULD NOT be trusted". OK.
- L57-58 S078+S079: §2.5.4 "Keys MUST NOT appear… MUST be a URI pointing to…"; S079 "Remember to include 'https://'". OK.
- L59-61 S078+S079: §2.3 OpenPGP cleartext RECOMMENDED + Canonical "allowing the digital signature to authenticate the location"; S079 "authentic, and not planted by an attacker". OK.
- L62-63 S078+S079: §2.4 "IANA registry… MUST be considered optional… MUST ignore any fields they do not explicitly support"; S079 lists CSAF Optional. OK.
- L67-69 S078: §3.1 "MUST only apply to the domain or IP address in the URI used to retrieve it, not to any of its subdomains or parent domains… MAY also apply to products and services… SHOULD use the policy directive". OK.
- L70-71 S082: §3 "defines neither… the scope… both should be defined by the application itself". OK.
- L72-73 S078: §5.5 (heading "No Implied Permission for Testing": "shouldn't assume that the presence or absence… grants or denies permission"); §5.3 "Not having a 'security.txt' file may be preferable to having stale information". OK (see nuance 1).
- L99-102 S078+S084: S084 bytes exactly match (one Contact hackerone.com/github, Acknowledgments, Preferred-Languages en, Canonical, Policy, Hiring, Expires 2026-11-21T22:02:20z); 2026-11-21 − 2026-10-22 = 30 d ≈ "about a month", < 1 y (marked inference). OK.
- L103-105 S085+S078: S085 bytes exactly match (two Contacts https:// then mailto:, Encryption, Acknowledgments, Policy, Hiring, Expires 2030-04-01T00:00:00z); §2.5.3 first-line-preferred. OK.
- L106-107 S078+S085: 2030-04-01 − 2026-10-22 ≈ 3.44 y ≈ "three and a half", past §2.5.5 recommendation (marked inference). OK.
- L108-109 S085+S078+S084: bytes confirm no Canonical/no Preferred-Languages (Google), no Encryption (GitHub); both optional per §2.5. OK.
- L110-112 S084+S085+S078: bytes begin "Contact:", no "-----BEGIN PGP SIGNED MESSAGE-----"; §2.3 signing only RECOMMENDED. OK.
- L116-126 decisions: S078/S079 restatements all supported (Contact first + prefixes; Expires < 1y; Policy/Canonical/signature; post-deploy plain-text HTTPS read). OK.

## Count
False: 0. Unsupported: 0. Wrong ids: 0. (Borderline paraphrases, not findings: "grants no permission to test" vs §5.5 "shouldn't assume" wording; "origin-wide capability" vs §4.1 "effectively represent the entire origin"; "cannot mint its own" vs §3 MUST-register.)

## Erratum note
The entry cites no errata and relies on none. Every checked claim matches the retained RFC/IANA/securitytxt.org bodies directly; no sentence depends on a Reported-but-not-Verified erratum (I could not consult the errata databases — not fetched, per bounds).

## Not verified
- Live re-fetch of any cited page (network bound; retained texts are ground truth by design).
- RFC 9116/8615 errata databases (unopened).
- C2 counter run / probes (other seats' scope).
