# CriticQuoteOverclaim — quote-support attack

Axes: **operability**, **freshness**. No round verdict, no admission, no edit of the entry or the lesson.

Attacked: `corpus/knowledge/crawl-budget-consequences.md` at `1c846ed2d67b1692ea966be064f0fc04542763c6` (worktree bytes match that blob, 1243 bytes). Support test: a sentence stands only if the two Gate quotes entail it.

Gate quotes, `corpus/lessons/round-49.md:9-10`:

- S273 (21 words): "Google won't shift this newly available crawl budget to other pages unless Google is already hitting your site's crawl capacity limit."
- S274 (10 words): "It reduces your site's crawl rate across the whole hostname"

Neither quote contains: robots, block, free, spared, fetches, emergency, backoff, status, 500, 503, 429, significant.

## Verdict

The status-code disclosure is **not enough**.

It is enough for one narrow fence: the checked S274 quote string does not name the codes, and the entry says so (`crawl-budget-consequences.md:13`). That fence is already what C2 R3/R4 measure (quote span is 6–25 words and a substring). Restating it does not keep the entry inside the two admitted sentences.

A reader who is told to admit only those two sentences still walks away with three claims the quotes do not state: robots blocking is the cause; blocking does not free budget (no capacity-limit exception); status codes trigger the backoff.

## Why the disclosure fails

`crawl-budget-consequences.md:13`: "The checked S274 quote does not itself name the status codes that trigger that backoff. Those words sit in the same retained paragraph and are not the admitted quote."

- The negative half is true of the quote string. The words "are not the admitted quote" hold.
- The same sentence presupposes the excluded claim: "status codes that trigger that backoff." "Backoff" is not in the S274 quote. The quote's subject is "It", with no antecedent inside the quote.
- "Same retained paragraph" is weaker than the blob. In `git show 1c846ed2d67b1692ea966be064f0fc04542763c6:.ufo/waves/round-49/sources/S274.txt` the quote starts at index 3385. The sentence that contains it starts at index 3213 and already includes the codes: "When Google's crawling infrastructure encounters a significant number of URLs with 500, 503, or 429 HTTP response status codes (for example, if you disabled your website): It reduces your site's crawl rate across the whole hostname". The codes are the grammatical antecedent of "It", not a neighboring remark. The entry drops "a significant number of URLs".
- The ground line above the disclosure still states the unadmitted cause as the entry's ground (`:5`: "budget consequence of robots and status codes"). A later "not the admitted quote" does not retract that line.

The parallel S273 antecedent is used harder and is not disclosed at all. Committed `S273.txt` index 7259, the sentence immediately before the quote: "Don't use robots.txt to temporarily reallocate crawl budget for other pages; use robots.txt to block pages or resources that you don't want Google to crawl at all." The heading and the lead clause treat that antecedent as what the page says. The entry never says those words are outside the admitted quote.

## Flagged sentences

Not supported by the two Gate quotes. Cleared spans are noted so a supported fragment is not scored as a miss.

| Loc | Sentence | Class |
|---|---|---|
| `:5` | ground: per-host crawl hygiene — budget consequence of robots and status codes | **Overclaim.** "Across the whole hostname" supports a per-host rate cut for whatever "It" is. "Robots" and "status codes" are not in either quote. |
| `:7` | Robots blocking does not free crawl budget | **Overclaim.** "Robots" and "blocking" are the undisclosed S273 antecedent. "Does not free" is not the quote. The quote is conditional: won't shift unless already hitting the site's crawl capacity limit. The heading drops that exception. An operator who follows the heading gets a stricter rule than the admitted sentence. |
| `:9` | The lane's held robots rows stop at what a directive means. | Not quote-supported. Lane-meta, not a Google-fact overclaim. Not checked against other entries. |
| `:9` | They do not say what blocking costs. | Same. |
| `:9` | Two Google documents opened this round, and only these two sentences are admitted. | Admission bound, not entailed by the quotes. The heading, `:5`, and the lead clauses cross it in the same file. |
| `:11` | Google's crawl-budget page says a block does not hand the spared fetches to other pages: [S273 quote] (S273). | **Overclaim on the lead clause.** "Says" attributes "a block", "spared fetches", and an absolute "does not hand" to the page. None of those words are in the quote. The span after the colon is the S273 quote and is a substring of the committed blob at index 7430. That span is cleared. The unless is present only there, not in the attributed gloss. |
| `:13` | Google's emergency crawl-rate page says the backoff reduces your site's crawl rate across the whole hostname (S274). | **Overclaim on the subject.** "Emergency" and "backoff" are not in the quote. The predicate "reduces your site's crawl rate across the whole hostname" is the S274 quote minus "It", substring at index 3385. That predicate is cleared. "Says" still attributes the substituted subject. |
| `:13` | The checked S274 quote does not itself name the status codes that trigger that backoff. | Split. "Does not itself name the status codes" is true of the quote string and is cleared. "That trigger that backoff" is not supported by the quote, and it is stronger than the retained sentence (significant number of such URLs, not the codes bare). |
| `:13` | Those words sit in the same retained paragraph and are not the admitted quote. | Split. "Are not the admitted quote" is cleared. "Same retained paragraph" is not entailed by the Gate quotes. It is true of the blob and too weak: same sentence, as the antecedent of "It". |
| `:17` | No lane property was fetched or measured. | Not quote-supported. Disclaimer, not a Google overclaim. |
| `:17` | Search Console crawl stats stay operator-gated. | Same. |
| `:17` | Publishing stays operator-owned. | Same. |
| `:17` | Bing and Baidu budget models are not claimed. | Same. |

Identity lines `:1-4` (URLs, verified-at, recheck) are not sentences of the quotes. The URLs match the Gate lines beside the quotes. They are not flagged as overclaims.

## What this does not falsify

C2's frozen predicate can still pass. R4 checks that each Gate span is a substring of its own committed blob. Both spans are. A dirty reading of the entry is outside that counter. This finding does not say the quotes are mistyped, mis-pinned, or absent from the retained text.

## Smallest correction that stays inside the quotes

Do not widen the admitted spans. Three cuts, no new Google claim:

1. Heading and `:11` lead clause: either quote the S273 sentence including "unless", or say the admitted sentence does not name robots or a block.
2. Disclose the S273 robots.txt antecedent the same way as the status codes, and do not teach it.
3. Replace "status codes that trigger that backoff" with a non-causal fence: the quote does not name 500, 503, or 429; those words are the antecedent of "It" in the retained sentence, including "a significant number of URLs", and they are not admitted. Drop "robots and status codes" from `:5`.

That improves freshness of what the entry teaches and operability of the rule a reader would apply. It does not harm either admitted quote.

Report: .ufo/waves/round-49/w1/CriticQuoteOverclaim.md
