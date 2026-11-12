# Kake: certificate wildcard scope

[RFC6125](https://www.rfc-editor.org/rfc/rfc6125.html), March 2011, section 6.4.3, permits clients to match partial-label wildcards, while discouraging wildcards embedded in internationalized labels.

[RFC9525](https://www.rfc-editor.org/rfc/rfc9525.html), November 2023, section 6.3 and Appendix A, replaces that specification. A presented name may contain one wildcard, occupying the entire leftmost label. A nonconforming presented identifier is ignored; other identifiers remain independently checkable.

For custom-domain diagnosis, separate certificate-name matching from DNS wildcard expansion. Where the application protocol permits wildcard support, `*.studio.example` can match `mix.studio.example`, but neither `studio.example` nor `a.mix.studio.example`. The partial label `m*.studio.example` is invalid under the newer rule. These names are invented.

This is a standards transition, not a browser-implementation measurement. Application protocols may prohibit wildcards; certification-path validation remains separate. See RFC9525 sections 1.2 and 7.1.

Both RFCs carry IETF Trust/BCP78 notices. Unrestricted reuse is not asserted; this note supplies original commentary and links only.

Proposed destination: `VeigaPunk/kake-shokunin` → `considerthese/2026-11-12-certificate-wildcard-scope.md`. No repository change, training or assimilation.
