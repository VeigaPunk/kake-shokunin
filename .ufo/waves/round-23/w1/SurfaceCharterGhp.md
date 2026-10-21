## Verdict

`charter-ghp` is live and its captured head passes the frozen round-22 local canonical policy: one canonical link in the explicit head, equal to the expected GHP URL; the auditor returned `clean` with no findings. The expected canonical is the right local policy for this surface: the `SKILL.md` property-map row names the GHP front as the canonical charter document, and the live page self-declares that same URL. Freshness is only partially resolved: the mapped local source directory is confirmed absent as the map's inline historical note says; branch-publishing configuration and the separate Kimi-variant canonical tags were not verified. This is a surface report, not independent admission.

## Findings

- **No C2 canonical-policy finding.** Before running the audit, I read the captured head by eye: explicit `<head>` open at line 3, one `<link rel="canonical" href="https://veigapunk.github.io/charter-ufo-fsd/">` at line 8, and `</head>` at line 23. Given the frozen policy's one-supported-head-canonical-equals-expected rule, I predicted `clean`, `findings: []`, exit 0. The run matched.
- **P2 — Freshness verification gap: publish mechanism.** Exact command: `curl -sS -L --max-redirs 5 -A 'kake-r23-readonly' -D /tmp/kake-r23-SurfaceCharterGhp-Vq6g/h -o /tmp/kake-r23-SurfaceCharterGhp-Vq6g/b -w 'status=%{http_code}\nfinal_url=%{url_effective}\ncontent_type=%{content_type}\n' 'https://veigapunk.github.io/charter-ufo-fsd/'`. Exact observed response summary: `status=200`, `final_url=https://veigapunk.github.io/charter-ufo-fsd/`, `content_type=text/html; charset=utf-8`, body SHA-256 `7c243a1d81357cdee71520034a05d540bfe8f69c702a7a1c95f8a0bfa5237aba`, `content_bytes=53660`. Impacted claim/axis: `SKILL.md`'s `Pages deploy from branch (no workflow file)` / freshness. A rendered HTML GET does not identify the Pages publishing configuration, and the mapped source tree is absent. Smallest verification/fix: read authoritative public Pages/repository configuration; correct the map only if that contradicts it. No configuration was changed.
- **P2 — Freshness verification gap: Kimi-variant canonicals.** The same exact GET above is the only web request made; it establishes the GHP page's own canonical but not the `<head>` declarations on each Kimi variant. Impacted claim/axis: `SKILL.md`'s `all kimi variants rel=canonical here` / freshness. Smallest verification/fix: inspect each variant head in its separately scoped read-only surface pass; if one disagrees, fix that variant's upstream source canonical and leave publishing operator-gated. No variant was fetched or changed here.

The corresponding audit command was `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --manifest /tmp/kake-r23-SurfaceCharterGhp-Vq6g/manifest.json --json`; the manifest was `{"version":1,"pages":[{"url":"https://veigapunk.github.io/charter-ufo-fsd/","file":"b","expectedCanonical":"https://veigapunk.github.io/charter-ufo-fsd/"}]}`. Exact stdout: `{"findings":[],"pagesChecked":1,"verdict":"clean"}`; exact exit: `0`.

**Upstream fix named (documented only, not applied):** commit `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`, `round-23: evaluate body-only SVG/MathML and void self-closing tags; read-only live snapshot tool`. Its auditor change evaluates SVG/MathML and self-closed HTML void tags after an explicitly closed head. No canonical-source correction is indicated for this GHP snapshot; this parser change is the upstream tool fix, not a live-site edit.

## Checked and held

- Frozen policy: `.ufo/waves/round-22/contract.json` specifies exactly one canonical link in the explicit head and comparison against `expectedCanonical`; the finding IDs include `canonical_missing`, `canonical_multiple`, `canonical_outside_head`, and `canonical_mismatch`. `SKILL.md` says a matching supported head canonical means local policy clean, not complete publication readiness.
- One public GET only: `curl -sS -L --max-redirs 5 -A 'kake-r23-readonly' -D /tmp/kake-r23-SurfaceCharterGhp-Vq6g/h -o /tmp/kake-r23-SurfaceCharterGhp-Vq6g/b -w 'status=%{http_code}\nfinal_url=%{url_effective}\ncontent_type=%{content_type}\n' 'https://veigapunk.github.io/charter-ufo-fsd/'`. Captured summary: `status=200`; final URL `https://veigapunk.github.io/charter-ufo-fsd/`; content type `text/html; charset=utf-8`; SHA-256 `7c243a1d81357cdee71520034a05d540bfe8f69c702a7a1c95f8a0bfa5237aba`; 53,660 bytes.
- By-eye head: lines 3–23 explicitly bracket the head; line 8 declares the same expected URL. The fetched HTML also has title `PLAZIR-27 — the ufo-fsd charter` at line 6. Audit command/output/exit are recorded above.
- Local source-path check: `if test -e /home/vgpnk/Projects/origin-work/charter-ufo-fsd; then printf 'present\n'; else code=$?; printf 'absent (test -e exit=%s)\n' "$code"; fi` → exact output `absent (test -e exit=1)`. The map's inline comment already records this path as absent and retained as historical, so that state remains consistent.
- The upstream commit identity/subject was read with `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show --format='%H %s' --no-patch 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc` → `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc round-23: evaluate body-only SVG/MathML and void self-closing tags; read-only live snapshot tool`.

```json
{
  "unit": "property-map",
  "path": "SKILL.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "| charter GHP front | `https://veigapunk.github.io/charter-ufo-fsd/` |",
      "claim": "The charter GHP front is live at the mapped URL and the final URL matches it.",
      "surface": "https://veigapunk.github.io/charter-ufo-fsd/",
      "method": "GET",
      "observation": "status=200; final_url=https://veigapunk.github.io/charter-ufo-fsd/; content_type=text/html; charset=utf-8; sha256=7c243a1d81357cdee71520034a05d540bfe8f69c702a7a1c95f8a0bfa5237aba; content_bytes=53660",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "`~/Projects/origin-work/charter-ufo-fsd`",
      "claim": "The mapped local source directory is absent, matching the row's adjacent historical-record annotation.",
      "surface": "/home/vgpnk/Projects/origin-work/charter-ufo-fsd",
      "method": "test -e",
      "observation": "absent (test -e exit=1)",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "canonical doc, all kimi variants `rel=canonical` here",
      "claim": "The GHP page confirms the canonical-document target locally: its explicit head has one canonical equal to the mapped GHP URL.",
      "surface": "https://veigapunk.github.io/charter-ufo-fsd/",
      "method": "GET",
      "observation": "HTML head lines 3-23; line 8: <link rel=\"canonical\" href=\"https://veigapunk.github.io/charter-ufo-fsd/\">; canonical_audit output {\"findings\":[],\"pagesChecked\":1,\"verdict\":\"clean\"}, exit=0",
      "verdict": "HOLD"
    },
    {
      "id": "c1",
      "anchor": "Pages deploy from branch (no workflow file)",
      "claim": "The mapped branch-publishing mechanism is not established by the fetched page or the absent local source directory.",
      "surface": "https://veigapunk.github.io/charter-ufo-fsd/",
      "method": "GET",
      "observation": "GET returned HTML status 200; the response does not expose Pages source configuration; local source-path test returned absent (test -e exit=1)",
      "verdict": "UNVERIFIABLE",
      "reason": "The live HTML does not identify the Pages deployment source, and the mapped source checkout is absent; no authoritative public deployment configuration was queried."
    },
    {
      "id": "c1",
      "anchor": "all kimi variants `rel=canonical` here",
      "claim": "Every Kimi charter variant currently declares the GHP URL as its canonical.",
      "surface": "https://veigapunk.github.io/charter-ufo-fsd/ (variant pages not fetched)",
      "method": "GET",
      "observation": "Only the GHP URL was fetched; its self-canonical is present, but no Kimi variant head was inspected.",
      "verdict": "UNVERIFIABLE",
      "reason": "A GHP response cannot establish canonical declarations on separate Kimi variant pages; those URLs were not fetched in this single-surface check."
    }
  ]
}
```

## Limits

This GET plus the offline audit establishes one live response and the source HTML's declared canonical signal, not Google-selected canonical, duplicate-content treatment, JavaScript behavior, or full publication readiness. The Kimi-variant canonical claim and branch-publishing configuration remain unverified. No Kimi page was fetched, no account/publish action was taken, no production file was edited, and no build, lint, formatter, or test was run.