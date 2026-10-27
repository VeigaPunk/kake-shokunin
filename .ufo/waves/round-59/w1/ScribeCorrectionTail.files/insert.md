  **[r59-correction 2026-10-27]** The claim in the bullet above is wrong as stated: a server log
  records the requesting IP address as well as the user-agent, and Google's crawler overview gives
  three identification signals, not one [S425] — the HTTP user-agent request header,
  "The source IP address of the request." and "The reverse DNS hostname of the source IP." Its
  technical-properties section adds that the clients are distributed across many datacenters, so
  "your logs may show visits from several IP addresses" [S425]. What the bullet gets right
  survives: the user-agent header is what separates the Smartphone and Desktop subtypes quoted
  above, so a log line reading Googlebot still does not say which viewport the fetched HTML was
  produced for. What does not survive is the word *only* — verifying a claim to be Googlebot is an
  IP check (reverse DNS, then forward DNS), set out in `googlebot-verification.md` (S426); the
  fuller reading of the three signals, with the datacenter spread, is
  `crawler-identity-signals.md` (S425). The sentence above stays as historical text; this
  correction supersedes it.
