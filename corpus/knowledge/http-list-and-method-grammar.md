source: S477, S478 (RFC 9110 sections 9.1 and 5.6.1, see corpus/SOURCES.md)
verified-at: 2026-11-05
recheck: 180d
ground: freshness -- method-token and list-member grammar of conditional requests.
scope: the method-token case rule and the list-member whitespace rule for If-Match and If-None-Match; not entity-tag grammar or contract decisions.

# Method-token case and list whitespace in conditional requests

**The method token is case-sensitive.** RFC 9110 §9.1 (S477, §9.1, plain-text lines 3748-3749):

> The method token is case-sensitive because it might be used as a
> gateway to object-based systems with case-sensitive method names.

So `get` is not the GET method (S477, §9.1). RFC 9110 §13.1.2 (S473, lines 5928-5932) makes a matching If-None-Match answer 304 "if the request method is GET or HEAD" and 412 "for all other request methods" (S473, §13.1.2). So the v2 case `inm/lowercase-method-is-not-get` expects 412 (S473, §13.1.2): the method-token case rule (S477, §9.1) decides it, not taste, and the case kills mutant M37.

**List members are comma-separated with optional whitespace.** RFC 9110 §5.6.1.2 (S478, lines 1699-1702):

> a recipient MUST accept lists
> that satisfy the following syntax:
>
> #element => [ element ] *( OWS "," OWS [ element ] )

so members are comma-separated with optional whitespace (S478, §5.6.1.2). Section 5.6.1 names that whitespace OWS and points to Section 5.6.3 for its definition (S478, §5.6.1, plain-text lines 1670-1672), where OWS is SP or HTAB (plain-text line 1774), so a tab around a member is legal whitespace.

If-Match and If-None-Match are entity-tag lists (S472, §13.1.1, line 5799; S473, §13.1.2, line 5885), so `"9",<TAB>"1"` is two members whose second member matches; the v2 case `inm/htab-around-list-members` expects that match (S478, §5.6.1.2) and kills mutant M40.

## What this entry does not decide

- A comma inside a quoted entity-tag: RFC 9110 §8.8.3 (S455, line 3587) admits it; R93-8 records the positive control refusing it.
- Empty list elements: S478's §5.6.1.2 (lines 1695-1699) requires a recipient to accept and ignore them; the contract refuses them (R93-9).
- obs-text in an entity-tag: the same line 3587 (S455, §8.8.3) admits it; the contract refuses it (R93-9).

Each is a contract-v2 decision, routed by `corpus/lessons/round-93.md` R93-8/R93-9.
