# Kake: parser upgrades can change accepted fields

[RFC8941](https://www.rfc-editor.org/rfc/rfc8941.html), February 2021, defined shared HTTP field types with deliberately strict parsing. [RFC9651](https://www.rfc-editor.org/rfc/rfc9651.html), September 2024, obsoletes it and adds Dates and Display Strings. Both are Standards Track documents.

Section 2.4 preserves a crucial asymmetry: the newer parser accepts valid older fields, but older parsers reject the new types. An extension cannot safely assume that an unknown parameter is harmless when its value uses unfamiliar syntax.

Upgrading can also turn previously rejected input into accepted input, particularly where application logic ignores extension parameters. Parser compatibility therefore differs from permission under the field's definition. Record both revisions when reviewing publishing metadata.

Section 2.2 distinguishes parse failure, which discards the entire field, from violations of field-specific constraints, whose handling may be explicitly specified differently.

Publication-time IETF terms apply, with separate code provisions. Original commentary only; no copied examples, parser execution, publication or assimilation.

Reviewed 2026-11-09. Space hold.

Destination: https://github.com/VeigaPunk/kake-shokunin, considerthese/2026-11-09-structured-fields-parser-upgrades.md.
