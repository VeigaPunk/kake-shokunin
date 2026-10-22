# Wave-2 falsification — C2 entry, "Web services" + "Docker-based services" sections
Seat: KakeR31a2.ReviewEntryWebDocker. Target: `corpus/knowledge/render-web-services.md`
lines 18-31 at fde133ab48086bb9a06911b4ab045e2ad9086347, reviewed in sandbox clone
`/fast/scratch/hyaku/kake-r31/a2-w2/ReviewEntryWebDocker/clone` (HEAD fde133a).

## Method
Own checker `/fast/scratch/hyaku/kake-r31/a2-w2/ReviewEntryWebDocker/check_quotes_clone.py`
replicates the counter's normalization (`re.sub(r"\s+"," ",s).strip()`), slices the entry
from `## Web services` to `## Health checks`, extracts every curly quote + `(S0xx)` cite,
tests literal substring against the collapsed retained text, and prints source context.
Then per-sentence "says no more than the quote" review against that context.

## Result: 11/11 quotes are exact substrings; 1 defect found (false [INFERENCE] claim)

sentence (entry line) | supported | issue
- L20 "rebuilt and redeployed from Git on each push" — "Render builds and deploys your code with every push to your linked Git branch." (S058) | YES | none; "from Git" narrows "linked Git branch" slightly, harmless.
- L21 "listen on all interfaces" — "must bind to a port on host 0.0.0.0 to receive HTTP requests from the public internet." (S058) | YES | none.
- L22 "has a default that can be changed" — "The default expected port is 10000 (you can configure this )." (S058) | YES (head) | DEFECT in trailing note, see below.
- L22 [INFERENCE] "the mechanism (the PORT environment variable) is not stated from a source here" | NO — claim is FALSE | S058's retained text states it verbatim twice: "We recommend binding your HTTP server to the port defined by the PORT environment variable." and "You can override this value by setting the environment variable for your service in the Render Dashboard ." plus "The default value of PORT is 10000 for all Render web services." (S058.txt). S057's example render.yaml also sets `- key : PORT / value : 10000`. The note misstates retained evidence and wrongly marks a sourced fact unsourced; it also contradicts the entry's own Port bullet ("the app follows PORT when Render sets it"). Honest-marking defect, not a substantive overreach.
- L23 "keeps a Render host name beside any custom domain" — "Every Render web service gets a unique onrender.com subdomain, and you can add your own custom domains ." (S058) | YES | pointer "custom-domain and certificate behaviour is in render-static-sites.md (S052, S061)" verified: render-static-sites.md:55-66 covers custom domains/TLS from S052 and :157-160 adds S061.
- L27 "Render can build the image itself from the repository" — "Build their own image at deploy time based on the Dockerfile in your project repo." (S059) | YES | quote subject is "Your services can", one of two options ("Pull and run a prebuilt image ... or Build their own image"); entry's "can" matches the option framing.
- L28 "starts with the Dockerfile's own command unless a Docker Command is set" — "If Render should run a custom command ... specify it in the Docker Command field under Advanced" (S059) | YES | none.
- L29 "env vars reach the build" + "secrets must not be read as build arguments" — both quotes (S059) | YES | "those values" resolves to "environment variables for a Docker-based service" in the retained preceding sentence; the "so" linkage matches the page's own next sentence ("Otherwise, those sensitive values might be included in your generated image").
- L30 "build context filtered by .dockerignore, secret files placed in it" — both quotes (S059) | YES | none.
- L31 "deploy without downtime like native ones" — "support zero-downtime deploys , just like services that use a native language runtime." (S059) | YES | none.

## Commands run (all in sandbox clone at fde133a; TMPDIR inside sandbox)
- `git clone -q <lane> clone && git -C clone checkout -q fde133a` → HEAD fde133a; S058.txt sha256 983a792dc65dbbe9…, S059.txt f8e60da01b3087b3… — match declared header prefixes.
- `python3 -B check_quotes_clone.py` → exit 0, "TOTAL quotes in scope: 11, substring-true: 11" (`clone_check.out`).
- `python3 -B .ufo/waves/round-31/c2_quote_truth.py --root . --revision fde133a…` → exit 0, passed 4/4, controlBroken false.
- `python3 -B .ufo/waves/round-31/c2_strict_checks.py --root . --revision fde133a…` → exit 0, S1-S5 true, renderYamlKeys all true, retainedBytes S057-S061 true.
- `grep` contexts on lane `sources/S058.txt`, `S057.txt` (read-only): PORT evidence quoted above.

## Residual risk / gaps
- Both counters sample one gate quote per source id; the other 10 in-scope quotes are checked only by my script (all pass). Neither counter verifies the truth of [INFERENCE] annotations — that is how the false L22 note lands green.
- Quote whitespace artifacts ("deploys ,", "this )", "domains .", "deploys ,") faithfully mirror the retained visible text where link targets were stripped; verified in the retained bytes, not defects.
- Not verified by me: S052/S061 quote fidelity inside render-static-sites.md (pointer existence only); Health-checks, Blueprint, and lane-render.yaml sections (other seats); live pages (no network per bounds).
- No tools installed; no lane files touched besides this report.
