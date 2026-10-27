# ReviewerCorrection

ATTACKS: Checked the B1 correction against the retained S426 cell and S428 article text; evaluated inferential wording; rendered B1 Markdown with Marked and inspected the correction's DOM ancestry.

SENTENCES:
- The correction faithfully attributes S426's categorical wording and date to its source; the retained S426 article text at lines 1125–1126 prints “these fetchers ignore robots.txt rules.” S428's article intro (retained S428.html:1086–1089) says “generally ignore,” and its footer prints 2026-08-19 UTC (1461–1462). The quoted revisions and contrast are accurate.
- “the later page no longer says that every such fetch ignores it” is an accurate contrast in wording, but does not establish an exception. The next clause explicitly says neither page names one, consistent with S428's entry and article.
- “a publisher still cannot count on robots.txt to hold a user-triggered fetch back” goes beyond the source text: “generally ignore” does not specify which cases are exceptions or establish a universal operational guarantee. It is framed as an inference, but stated categorically (“cannot count”) rather than marked [INFERENCE] or explicitly scoped as a conservative implication. This overstates what S428 alone establishes.

RENDER:
- Ran `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 8b33fd248d126b48d838af5c38bc175850f41a09:corpus/knowledge/googlebot-verification.md | npx --yes marked > /fast/scratch/hyaku/kake-r60/ReviewerCorrection-2/rendered.html`, then parsed it with Python BeautifulSoup.
- Output: correction paragraph parent is `li`, its parent is `ul`; `blockquote` ancestor is `False`. So it renders inside the user-triggered-fetchers list item, outside the preceding blockquote. The subsequent explanatory paragraph also remains in that list item until the next unindented paragraph closes the list.

FINDINGS:
| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| medium | corpus/knowledge/googlebot-verification.md:41 | Categorical publisher assurance is not entailed by S428's “generally ignore”; the page explicitly leaves exceptions unspecified. | `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 8b33fd248d126b48d838af5c38bc175850f41a09:corpus/knowledge/google-user-triggered-fetchers.md` (robots posture and “No exception set”); retained `.ufo/waves/round-60/sources/S428.html:1086-1089` | Mark the sentence as an inference and qualify as a prudent assumption, not a demonstrated guarantee; or remove it. |

VERDICT: One semantic overreach in the publisher-advice sentence; source dates and cited wording are accurate, and the correction renders in the intended list-item position outside the blockquote.
