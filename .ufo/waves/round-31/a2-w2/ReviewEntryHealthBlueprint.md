# ReviewEntryHealthBlueprint — round 31 wave 2 (falsify, C2)

Scope: sentence-by-sentence support review of `corpus/knowledge/render-web-services.md`
sections `## Health checks` (lines 33-39) and `## The Blueprint file` (lines 41-48) at
fde133ab, against retained `.ufo/waves/round-31/sources/S060.txt` (health-checks) and
`S057.txt` (blueprint-spec). Other sections are out of scope (other seats).

## Verdict
All 17 curly-quoted spans are exact substrings of the cited retained source, and every
sentence's claim is supported by the surrounding context. No falsifying defect. Two minor
notes: one unflagged inference (line 39), one omitted precondition (line 48).

## Commands run (sandbox clone; TMPDIR inside sandbox)
- `git clone -q <lane> clone && git -C clone checkout -q fde133a…` — exit 0, HEAD fde133ab.
- `git -C clone diff --stat fde133a 92235a0 -- corpus/knowledge/render-web-services.md` — empty; entry unchanged at attempt-2 tip.
- `sha256sum S057.txt S060.txt` — ca8179f2098b142d… and 1f934877247b6d…; byte-identical to `receipts.json` `textSha256` and the header's stated values.
- `python3 -B check_quotes.py` — exit 0, `FAILS: 0` (script: /fast/scratch/hyaku/kake-r31/a2-w2/ReviewEntryHealthBlueprint/check_quotes.py; extracts “…” spans from lines 33-48 and tests exact substring in the cited S0xx).
- Python context windows around each quote in S057/S060 — printed and judged (below).
- `git -C /home/vgpnk/Projects/ds4cc-marketplace show 1fbdb8ed:render.yaml` — exit 0, 20 lines; `grep -c renderSubdomainPolicy` = 0 (line-48 premise holds).
- `python3 -B clone/.ufo/waves/round-31/c2_quote_truth.py --root clone --revision fde133a` — `C2 4/4`, exit 0.

## Health checks (S060)

| sentence (line) | supported | issue |
|---|---|---|
| L35 "A web service can name an HTTP path for checks" | yes | none; S060 headings "HTTP health checks (web services only)" confirm scope |
| L36 "Success has a status and a time limit" | yes | none; adjacent text adds 4xx/5xx = unhealthy and "all other cases" failed — entry consistent, omits extras |
| L37 "new deploy goes live only when its instances pass together … otherwise is cancelled" | yes | none; both quotes verbatim and adjacent in S060 |
| L38 "fails … first taken out of routing and then restarted" | yes | none; omits (harmlessly) the S060 clause that healthy sibling instances keep receiving traffic |
| L39 "checks carry a Host header the app must accept" | yes | minor: "the app must accept" is an inference beyond the quotes — S060 states what Render sends, not an app-side requirement; the file's own convention marks such steps `[INFERENCE]`. Nearby S060 text ("How should my endpoint verify instance health?") does not state it either. Not a factual error. |

## The Blueprint file (S057)

| sentence (line) | supported | issue |
|---|---|---|
| L43 "one file at the repository root by default" | yes | none; S057 lead: "Every Render Blueprint is backed by a YAML file… By default… render.yaml… repository's root directory (you can customize this during setup)" |
| L44 "can take over a service that already exists" | yes | none |
| L45 "For many omitted fields the file does not reset an existing service" + `[INFERENCE]` plan/region/deploy trigger | yes | note: the quoted "retains the current value for an existing service" appears verbatim for autoDeployTrigger, renderSubdomainPolicy, numInstances (5 occurrences total). `plan`'s row paraphrases it ("retains the current compute plan", @10725). `region` has no retain clause but says "You can't modify this value after creation" (@13437) — the inference holds via immutability, not the quoted retain rule. "many" is an accurate hedge (17 "If you omit this field" rows). |
| L46 env vars preserved when omitted | yes | none |
| L47 secrets via `sync: false`, prompted once, ignored on update | yes | none; S057 adds "add any new secret credentials to your existing services manually" — consistent, omitted |
| L48 onrender.com host can be switched off + `[INFERENCE]` "always" holds unless `renderSubdomainPolicy` is `disabled` | yes | minor: S057 states disabling "requires the service to have at least one custom domain" — the inference's exception is the same exception (a service can only disable via that field), but the precondition is not carried; equivalently, for services without a custom domain "always" holds unconditionally. Lane file verified not to set the field. |

## Residual risk / gaps
- Support judged against retained texts only; a page change after 15:41Z is outside this check (the counter replays retained text — stated in the entry header).
- Sections on web services, Docker, and `## The lane's render.yaml` reviewed by other seats.
- No installs needed; artifacts under /fast/scratch/hyaku/kake-r31/a2-w2/ReviewEntryHealthBlueprint/ (clone/, check_quotes.py).

Report: .ufo/waves/round-31/a2-w2/ReviewEntryHealthBlueprint.md
