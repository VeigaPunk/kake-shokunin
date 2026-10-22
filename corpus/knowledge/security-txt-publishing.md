source: S078 RFC 9116; S079 securitytxt.org; S080 Jekyll Configuration Options; S082 RFC 8615; S083 IANA Well-Known URIs registry; S084 https://github.com/.well-known/security.txt; S085 https://www.google.com/.well-known/security.txt; S006 GitHub Docs “About GitHub Pages and Jekyll”; S086 GitHub Docs “Creating a GitHub Pages site”; S001, S002 actions/upload-pages-artifact (ids in corpus/SOURCES.md). S081 (Wikipedia) and S087 (404) were opened this round and rejected.
verified-at: 2026-10-22, eleven public GETs 22:00:48Z–22:27:55Z, all HTTP 200 except S087's 404; retained text and receipts in .ufo/waves/round-35/sources/ (text sha256 S078 4954ddcda4ca…, S079 667229665b5c…, S080 24054b1af50f…, S082 0746e9da9c24…, S083 aceda87b1290…, S084 35cf4b7ba43d…, S085 c7a10ffa520a…, S006 9ddf8eb28670…, S086 710f4781d32f…); no request to an operator-owned host.
recheck: 90d, or on an RFC 9116/8615 revision (S083's security.txt row is the cheap check), a GitHub Pages Jekyll default change (S006), or an upload-pages-artifact hidden-file change (S001, S002); re-run fetch_sources.py in a sandbox and compare receipts.json.
scope: How a publisher serves one valid security.txt from GitHub Pages — a Jekyll branch build and an Actions artifact build — plus what S084 and S085 show against the RFC. Nothing here says what an operator-owned property serves.
ground: The retained texts and receipts.json above; each factual sentence carries its text's id, and lane reasoning is marked [INFERENCE].
coverage: Location and the duplicate rule, serving and encoding, every registered field with cardinality, Expires horizon, contact order, encryption and signing, scope, both live examples, dot-directory handling per build path.
falsifier: A fresh fetch of a cited page that contradicts a sentence below, an IANA registry read that moves the security.txt row, or a C2 run on this text reporting copiedShare above 0.25.
counter: python3 -B .ufo/waves/round-35/sealed_count.py c2 --root . --revision <commit> --key-revision <reveal commit> — entry present, ≤ 1500 words, copiedShare ≤ 0.25, ≥ 3 good cites of S078–S099, ≥ 9 of 12 sealed probes. Not run by this seat; the probes are sealed and were not read.

# Publishing a security.txt from GitHub Pages

Coverage-map ground: operability and freshness of the web properties — a
researcher must find a reporting channel and be able to trust it.
`ghp-served-set.md` owns what the Pages tar and Jekyll build emit;
`publish-channels.md` owns branch versus workflow publication; this entry treats
`/.well-known/security.txt` as the resource those layers must deliver unchanged.

## Where the file lives

- A website's file belongs under `/.well-known/` (S078). The prefix is reserved
  only at the top of the path, so `/foo/.well-known/security.txt` is not a
  well-known URI (S082).
- IANA lists `security.txt` as permanent, controlled by IETF, referencing RFC
  9116, registered 2021-07-13 (S083); a site cannot mint its own well-known name
  (S082).
- A root copy is tolerated for legacy clients and may redirect (S078);
  securitytxt.org calls it a fallback and allows both copies at once (S079).
- With both present, the well-known copy must be used (S078), so the root file is
  a redirect or byte copy, never a second source of truth [INFERENCE].
- Reserve the namespace so no third party can claim either name (S078); write
  access to a well-known location is an origin-wide capability (S082).

## How it is served

- HTTPS only, HTTP/1.0 or later, `Content-Type: text/plain` with default charset
  `utf-8` (S078). securitytxt.org repeats the plain media type and HTTPS (S079).
- Bytes are UTF-8 in Net-Unicode form and must match the RFC's ABNF; lines end
  in CRLF or LF; `#` starts a comment; field names are case-insensitive (S078).
- Retrieval and referenced resources may redirect, and a redirect should be
  recorded (S078).

## The fields

- `Contact` is mandatory (S078, S079). Each value is a URI, so an address needs
  `mailto:`, a number `tel:`, a web contact `https://` (S078) — the three
  prefixes securitytxt.org's validator enforces (S079).
- Several `Contact` lines are ordered by preference, first line preferred (S078).
- `Expires` is mandatory, exactly once, an RFC 3339 date-time; a horizon shorter
  than a year is recommended (S078). securitytxt.org says ISO 8601 and marks it
  single-use (S079).
- `Preferred-Languages` is optional, at most once, a comma list of equally
  weighted tags; if absent, English may be assumed (S078, S079).
- `Canonical`, `Encryption`, `Policy`, `Hiring` and `Acknowledgments` are
  optional, repeatable, and any web URI among them needs `https://` (S078).
- `Canonical` states where the file lives; if it is present and the served URI
  is not listed, the contents should not be trusted (S078).
- `Encryption` is a URI to a key, never the key itself (S078), and should be
  `https://` (S079).
- An OpenPGP cleartext signature is recommended, with Canonical alongside so the
  location is signed too (S078); securitytxt.org frames signing as evidence the
  file was not planted (S079).
- New fields are IANA-registered, optional by definition, and unknown ones must
  be ignored (S078); securitytxt.org already lists one extension, `CSAF` (S079).

## What the file covers

- It applies to the host actually used to fetch it, not its parents or
  subdomains; it may also cover the organization's products, and the policy
  should spell out the scope (S078).
- RFC 8615 leaves scope to the application that registers the suffix (S082), so
  coverage is answered by the publisher's deployment and Policy link.
- Publication grants no permission to test (S078), and stale content is worse
  than no file (S078).

## GitHub Pages: branch build versus artifact build

- Branch build: paths starting with `_`, `.` or `#` are skipped by default, and
  `include` is the documented way to process them (S006). Jekyll's options page
  says dotfiles are excluded by default and that Jekyll 4 `include` entries
  override `exclude` entries (S080).
- [INFERENCE] A branch-published site therefore needs `include: [".well-known"]`
  or an equivalent glob; the retained texts give the mechanism, not that value.
- Branch publishing can skip Jekyll altogether: an empty `.nojekyll` file at the
  root of the publishing source disables the Jekyll build (S086), which is the
  lever when `include` cannot express the path.
- Artifact build: packaging decides dotfiles. v4.0.0 of upload-pages-artifact
  drops hidden paths by default; v5.0.0 adds an `include-hidden-files` input
  (S002).
- Even with that input on, `.git` and `.github` are excluded unconditionally
  (S001), so another dot-directory is includable [INFERENCE]; a pipeline that
  never sets the input ships no `/.well-known/` (S001, S002).
- For an Actions publishing source the artifact must carry the entry file at its
  top level (S086); dot-directory survival there is decided at packaging
  (S001, S002), while the branch path is decided by `include` (S006, S080)
  [INFERENCE: one switch does not cover the other].

## The two live files

- GitHub's retained body has one `Contact` (`https://hackerone.com/github`),
  `Acknowledgments`, `Preferred-Languages: en`, `Canonical`, `Policy`, `Hiring`
  and `Expires: 2026-11-21T22:02:20z` — about a month out at 2026-10-22, inside
  the year (S078, S084) [INFERENCE: subtraction].
- Google's body has two `Contact` lines, `https://` first and `mailto:` second,
  plus `Encryption`, `Acknowledgments`, `Policy`, `Hiring` and
  `Expires: 2030-04-01T00:00:00z` (S085); the first line is preferred (S078).
- That Expires is roughly three and a half years out, past the recommendation
  (S078, S085) [INFERENCE: arithmetic].
- Google's file has no `Canonical` and no `Preferred-Languages` (S085); both are
  optional (S078). GitHub's has no `Encryption` (S084), also optional (S078).
- Neither retained body opens with `-----BEGIN PGP SIGNED MESSAGE-----`; both
  begin with `Contact:` (S084, S085), while signing is only recommended (S078).
  This describes the retained bytes, not what a signature check would find.

## Decisions before publishing

1. One canonical location under `/.well-known/`; the root copy is a redirect or
   mirror (S078).
2. `Contact` first, in preference order, with `mailto:`, `tel:` or `https:`
   (S078, S079).
3. `Expires` under a year out, with a recheck date that keeps it true (S078).
4. `Policy` naming host and product scope, plus `Canonical` and a signature, or
   neither (S078).
5. A build path that ships the dot-directory: `include` for a branch build,
   `include-hidden-files` for a v5 artifact build (S006, S080, S001, S002).
6. A post-deploy read of the published URL as plain text over HTTPS, the only
   observation showing the file survived the build (S078).
