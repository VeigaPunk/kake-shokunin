# ReviewSkillTriageTable — C2 SKILL table "Render web service and Blueprint triage — round 31"

Seat: KakeR31a2.ReviewSkillTriageTable (wave-2 falsify, freshness axis).
Reviewed at fde133ab48086bb9a06911b4ab045e2ad9086347 in sandbox clone
/fast/scratch/hyaku/kake-r31/a2-w2/ReviewSkillTriageTable/clone.
`git diff --stat fde133a 92235a0 -- SKILL.md` = empty (0 lines): table identical at lane tip.

Method: python3 -B heredoc extracted the 8 table rows (SKILL.md:817-826), matched each
curly-quoted span byte-exact against .ufo/waves/round-31/sources/S0NN.txt (sha256
prefixes match entry: S057 ca8179f2, S058 983a792d, S059 f8e60da0, S060 1f934877),
then substring-searched each check-first clause's support inside the cited retained
text. Note: c2_quote_truth.py and c2_strict_checks.py contain no "SKILL" reference;
this table is outside counter coverage, so this review is the only check on it.

## Rows

row | supported | issue

1 deploy-cancelled (SKILL.md:819, S060) | yes | Quote exact. "all new instances pass
the health check together" is supported by adjacent S060 text "Whenever all of the
new instances are passing their health checks at the same time" (not the quoted
sentence, but same source).

2 no-public-traffic (:820, S058) | yes | Quote exact. "the port Render expects
(default 10000)" supported by S058 "The default expected port is 10000 (you can
configure this )."

3 health-check-fails (:821, S060) | yes | Quote exact. Host-header clause supported
by S060 "If your service has any verified custom domains , Render sets one of those
domains as the value of the Host header for all HTTP health checks. Otherwise,
Render uses the service's onrender.com subdomain."

4 instance-drops-out (:822, S060) | yes | Quote exact. "15 seconds stop routing"
supported by S060 "fails consecutive health checks for 15 seconds, Render
temporarily stops routing traffic to it"; 60s restart is the quote.

5 sync:false secret (:823, S057) | yes | Quote exact. "asked for only when the
Blueprint is created" = S057 "Render prompts you for these values only during the
initial Blueprint creation" (prompt happens "in the Render Dashboard"); "set them
in the dashboard" = S057 "Add any new secret credentials to your existing services
manually ." Supported, mildly loose on "dashboard" for the manual step.

6 dockerfilePath (:824, S057) | yes | Quote exact. "default ./Dockerfile" supported
by S057 "If omitted, Render uses ./Dockerfile ."

7 dockerContext (:825, S059) | PARTIAL | Quote exact in S059; ".dockerignore filters
the build context" supported. But "`dockerContext` defaults to the repository root"
is not in S059: S059 contains no "dockerContext"/"repo root" substring (index -1).
The support is S057's field doc "dockerContext The path to the service's Docker
build context, relative to the repo root. … If omitted, Render uses the repo root."
Minor: clause correctly grounded but attributed to the wrong source id (S059 cited,
S057 needed). Fix: cite S057 alongside S059 on this row.

8 secret-in-layers (:826, S059) | yes | Quote exact. "Service variables become build
arguments" = S059 "Render automatically translates those values to Docker build
arguments"; "use secret files" = S059 "If you need to reference sensitive values
during a build, use a secret file instead."

## Findings

- F1 (minor): SKILL.md:825 attributes the dockerContext-default clause to S059; the
  supporting text exists only in S057. All 8 quotes byte-exact; every other
  check-first clause is grounded in the cited retained text.
- F2 (observation): the SKILL table is not covered by either C2 counter; a future
  quote drift in SKILL.md would not trip c2_quote_truth.py or c2_strict_checks.py.

Not verified: live render.com pages (bounds: work from retained snapshots only;
quotes were checked against retained text as assigned, not re-fetched).
No tools installed; no lane mutation besides this report.
