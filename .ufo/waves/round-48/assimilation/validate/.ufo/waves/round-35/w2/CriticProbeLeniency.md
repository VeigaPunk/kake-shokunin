# CriticProbeLeniency — attacks the C2 sealed probe regexes (.ufo/waves/round-35/sealed/c2-probes.json): would false statements pass?

Result: CONFIRMED DEFECT. Every one of the 12 probes accepts a false or opposite sentence, and every one rejects a true paraphrase.
On a 201-word entry made only of false statements, the real counter returns `met: true`, exit 0, `probesPassed` 12.
The landed entry (95abec21) earns its 12/12 on true-looking spans, so the round's C2 number is not wrong. What is overstated is the disclosed limit
(SCORECARD.md:1425-1427, "C2 probes test that stated facts are present"). The probes test that keywords co-occur. They cannot tell a fact from its negation.

## Setup
- Lane HEAD seen: 0d52173c. The key sha256 is 111bceea…d61d and matches the pin at sealed_count.py:57. The counter sha256 is 1b4d9d59…469b.
- Sandbox: /fast/scratch/hyaku/kake-r35/w2/CriticProbeLeniency/ (clone at clone/, TMPDIR=tmp/). I did not write anything to the lane except this report.
- Normalization is the counter's own: probe_leniency.py imports sealed_count.py and applies `clean()`, then `re.sub(r"\s+"," ",text.lower())`, then `re.search` (sealed_count.py:272-273).

## Commands (all exit 0)
1. `timeout 60 python3 -B probe_leniency.py` gives output probe_leniency.out, with false sentences passing 12/12 and true paraphrases failing 12/12.
2. `cp wrong-entry.md clone/corpus/knowledge/security-txt-publishing.md` on 95abec21, then a sandbox commit dc8e1adf, then
   `python3 -B <lane>/.ufo/waves/round-35/sealed_count.py c2 --root clone --revision dc8e1adf --key-revision 4c6be2bd…63cc` gives exit 0 →
   counter-wrong.json: met true; conditions entry/size/copied/cites/probes all true; words 201; copiedShare 0.0; goodCites S078,S079,S080,S082; probesPassed 12.
3. The same counter at 95abec21 gives exit 0, met true, probesPassed 12, words 1388 (counter-landed.json), which matches the claim.
4. `python3 -B spans.py landed-entry.md` and `spans.py wrong-entry.md` print the first matched span per probe, along with a negation-guard experiment (spans-landed.out, spans-wrong.out).

## Per-probe results (exact lines from probe_leniency.out; "regex[i]" is the matching alternative)
| Probe | False sentence that PASSES | True paraphrase that FAILS |
|---|---|---|
| P01 | Never publish the file at /.well-known/security.txt; only the site root is read. [0] | Place security.txt inside the .well-known directory at the web root. |
| P02 | If a file is at both locations, the well-known copy never takes precedence; the root file wins. [0,1] | If the file exists at both paths, clients should prefer the one under .well-known. |
| P03 | Do not serve it as text/plain or declare utf-8; use text/html with latin-1. [0] | Serve it with the plain-text media type and the UTF-8 character set. |
| P04 | Contact is not required. [0] | Every security.txt file must include a Contact field. |
| P05 | Expires may appear more than once, and the last value counts. [0] | The Expires field has to be present and must not be repeated. |
| P06 | Expires should never be less than a year ahead; set it two years out. [0] | Keep the Expires date no further than 365 days in the future. |
| P07 | Expires is not an RFC 3339 date; write it as a Unix timestamp. [0] | Expires uses the internet date-time format, for example 2027-01-01T00:00:00Z. |
| P08 | Contact lines are not in order of preference; clients pick one at random. [0] | When several Contact lines appear, the first is the one a researcher should try before the others. |
| P09 | Paste the key itself into the Encryption field as an armored block. [0] | Encryption holds a URI pointing to the public key; the armored block does not belong in the file. |
| P10 | Do not sign with an OpenPGP cleartext signature; ship a detached .sig file instead. [0] | The whole file may carry an inline GnuPG signature made with gpg --clearsign. |
| P11 | A file on the apex covers every subdomain, so subdomains do not need anything. [1] | A security.txt applies only to the exact host it was fetched from; www.example.com and api.example.com are separate hosts. |
| P12 | GitHub Pages serves .well-known automatically; no include line in _config.yml is ever needed. [0] | Jekyll skips folders whose names start with a dot unless the site configuration lists them for inclusion. |

Count: a confidently wrong entry can pass **12 of 12** probes, as shown end to end in command 2 (the target is 9).
- Pure keyword probes, which carry no claim at all: P01 (a path literal), P07 ("rfc 3339"/"iso 8601"), P06 (no Expires anchor, so any "within a year" passes), and P12 alternatives 3-4 (bare `include-hidden-files` / `.nojekyll`).
- Polarity-blind probes: all 12. No regex excludes not/never/may/optional. P04, P05 and P11 even list the wrong-polarity phrase as a match token ("more than once" in P05 and "do not" in P11 are alternatives).
- P03 uses `[^\n]{0,120}`, and after whitespace collapse that crosses sentences. The landed span runs "…`utf-8` (s078). securitytxt.org repeats…".
- Leniency on the true side: the retained `reworded` control (control-v2-c2-reworded.json) has cites and copied both true but scores only 6/12. A faithful rewording misses the target.

## Landed entry check (spans-landed.out, landed-entry.md sha256 0b5ac7e8…c397)
All 12 first spans read as correct statements, for example "well-known copy must be used (s078)", "`contact` is mandatory", "`expires` is mandatory, exactly once", "shorter than a year", "never the key", and "not its parents or subdomains".
I did not compare these spans to the source texts; ReviewProbeMatchesTruth owns that.

## Counterexample against the control set
The pre-build C2 controls (verification/control-v2-c2-*.json) score base 0, junk 0, keyword 3, reworded 6, transcript 8, hollow 0 and both critic shapes 8.
None of them is a negated-fact entry. My fixture is the missing control, and it scores met true.

## Impacted axes
- Freshness, through claim provenance: "C2 met true" alone certifies coverage of the topics, not correct content. Truth rests entirely on the closure's read.
- No operability impact.

## Smallest safe correction (advisory; I edited nothing)
1. Now, without touching the sealed key or the counter: reword SCORECARD.md:1425-1427 to say the probes test that topic keywords co-occur, and that a polarity-inverted entry scores 12/12 (fixture wrong-entry.md, sha256 0e86d3a8…b250).
   The non-author closure's truth check should then read all 12 matched spans in spans-landed.out against S078/S079/S080/S082. A skim of the entry is not enough.
2. In future rounds, add a negated-fact entry as a mandatory pre-build control that must score met false.
   A negation guard alone is only partial. I tested a rule that rejects a match when not|never|no|do not|may|optional|instead appears in the span or the 30 characters before it.
   It cut the wrong entry to 1/12 (P09's "paste the key itself" still passes) and the landed entry to 10/12, because the true P09 and P11 statements are themselves negative.
   It also falls to rewording without negation words. Changing the sealed key after measurement would be post hoc, so this belongs to the next declaration.

## Not verified
- I did not check the guard against the other retained controls.
- I did not check the truth of the landed entry against the source texts.
- I did not run any live fetch; no network was used.
- Tools installed or updated: none.
- Deliverables: /fast/scratch/hyaku/kake-r35/w2/CriticProbeLeniency/{probe_leniency.py (ed75c8df…), spans.py (703e1616…), wrong-entry.md, landed-entry.md, probe_leniency.out, spans-landed.out, spans-wrong.out, counter-wrong.json, counter-landed.json}, plus sandbox commit dc8e1adf in clone/.
