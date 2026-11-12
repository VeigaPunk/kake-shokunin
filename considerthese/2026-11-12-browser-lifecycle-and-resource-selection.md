# Kake: browser lifecycle and resource-selection evidence

Curation date: 2026-11-12 UTC. Destination: `VeigaPunk/kake-shokunin`, `considerthese/2026-11-12-browser-lifecycle-and-resource-selection.md`.

Status: curated reading and unperformed practice. No browser was driven, site deployed, service worker registered, cache cleared, account used, or production content changed. This is not a completed experiment, training round, assimilation, or a conformance claim.

## Why this batch

Kake already has deep HTTP caching, validators, deployment-source, and crawl evidence. The live registry inspected at blob `0bd37bce0a4489027b0cf9504e0a42b14ada1895` reaches 224 source rows, and its recent training log ends at round 100 on 2026-11-06. The new ground here is state retained inside a browser: service-worker controller versions, back/forward-restored documents, and responsive-image resource choice. A fresh HTTP response is not the only state a returning user can see.

The 412 locally available curation Markdown files, current systems registries, and recent logs were screened. No service-worker, bfcache, or srcset family appeared in the prior curation corpus. Font-display and Early Hints/preload were already present and are not counted as new. This is novelty relative to the inspected material, not an exhaustive history of all branches.

## Sources and timeline

1. [Service Workers Nightly](https://w3c.github.io/ServiceWorker/), fetched 2026-11-12, displayed Editor's Draft date 12 August 2026. Read the status and model before treating any algorithm as a shipped browser promise. The draft explicitly says it may include unimplemented or changing features.
2. [The service worker lifecycle](https://web.dev/articles/service-worker-lifecycle), web.dev, opened 2026-11-12. Read “Updating the service worker,” “Waiting,” “Skip the waiting phase,” and the `clients.claim()` discussion. This is implementation-oriented teaching, not a browser-independent normative contract.
3. [Back/forward cache](https://web.dev/articles/bfcache), web.dev, displayed published date 25 May 2023 and last-updated date 16 October 2026 in the retrieved text. Read `pageshow`, `pagehide`, and the difference between HTTP cache and bfcache.
4. [Chrome: enabling bfcache for Cache-Control: no-store](https://developer.chrome.com/docs/web-platform/bfcache-ccns), published 21 October 2024; displayed update 9 September 2025; a March 2025 note describes completing rollout during March–April 2025. Opened 2026-11-12. This narrower product-specific page supersedes the broad guide's still-present “work underway” wording for that Chrome change.
5. [HTML Living Standard: Images](https://html.spec.whatwg.org/multipage/images.html), retrieved 2026-11-12, displayed last-updated date 11 November 2026. Read §4.8.4.1 examples and §4.8.4.2 srcset/sizes requirements. Introductory resource-selection examples are non-normative; the attribute conformance requirements are separately identified.

These are opened page extracts rather than a byte-preserved web archive. Dates shown above are source metadata, not measured browser availability. Re-open living documents and record installed browser versions before executing a practice report.

## 1. A service-worker update can mix code generations

**Method.** Track installing, waiting, active, and controlling states separately. The lifecycle guide explains that a replacement worker installs alongside the existing worker and ordinarily waits until the old worker controls no clients. Refreshing one tab may leave overlapping clients, so reload is not a reliable “activate new worker” instruction. `skipWaiting()` bypasses waiting, not installation, and can make a new worker handle subsequent fetches from a document loaded under the old version. `clients.claim()` changes who controls existing clients and can similarly produce timing-sensitive behavior.

**Publisher inference.** Retain compatibility between old HTML and the assets/API behavior that a newly activated worker might provide. A versioned cache name alone does not establish compatibility. The acceptance criterion should name the document/controller/asset combination, not simply “the new worker is active.” No universal update policy follows: immediate takeover and deferred takeover each have product trade-offs.

**Proposed exercise, not run:** use an isolated temporary browser profile and a loopback-only origin serving two tiny self-authored versions, A and B. No remote site or user profile. Maximum six cases: fresh A installation; B installed while two A tabs remain open; one-tab refresh; close all controlled tabs and revisit; explicit B skip-waiting while A document remains; failed B install with A retained. Use a stable worker URL and version-marked local assets. Bound each case to 30 seconds and keep browser storage below 20 MB.

**Report requirements.** Log document version, controller script/version, registration states, request/response asset version, tab count, and exact event sequence. Preserve a minimal mismatch trace if A HTML receives an incompatible B asset. Treat timing-dependent differences as observations, not normative violations. The negative control is a checker that declares success from `registration.active` alone; the fixture must show why this misses the mixed-version case. Cleanup removes only the temporary profile and fixture origin's data.

## 2. A restored document is not a new network load

**Method.** Distinguish `pageshow.persisted` from `pagehide.persisted`. The former reports restoration from bfcache; the latter indicates an intention to cache and does not guarantee it happened. A restored page can retain its JavaScript heap and stale application state without performing a fresh main-document request. Update or recheck the state that must be current after restoration, rather than assuming every history traversal runs the initial-load path again.

**Source conflict resolved.** The broad web.dev guide still says a change to no-store behavior is underway. Chrome's dedicated page documents the later rollout and conditions: pages with `Cache-Control: no-store` can enter bfcache in qualifying Chrome cases, with additional safeguards including eviction on cookie/authentication changes and disqualifying API activity. It also describes a shorter timeout for these pages. These are Chrome-specific policy statements, not an all-browser guarantee. Do not remove privacy-related cache directives merely to increase a performance score; first classify the data and its requirements.

**Proposed exercise, not run:** two local synthetic pages, no login and no personal data, with a visible “server revision” and document-instance marker. Test six cases in two installed browser engines if available: ordinary back/forward; main-document no-store; a harmless local cookie changed on the second page; `pageshow` refresh of a synthetic state value; duplicate analytics counting caused by both load and restore handlers; an intentional bfcache blocker. Freeze versions and record any unavailable engine as not run. Do not alter browser flags or enterprise policies merely to force a result.

**Report requirements.** Capture the event timeline, `persisted` flags, main-document request count, JS document marker, visible revision, and browser-provided non-restoration reason when available. A no-store header is not a sufficient observation of whether restoration occurred. The negative control is a test that treats `pagehide.persisted=true` as proof of a later restoration; it must be rejected. Do not equate synthetic cookie behavior with a verified logout/security policy for a real site.

## 3. Responsive-image declarations define candidates, not a universal byte choice

**Method.** Separate width descriptors from density descriptors and separate source size from rendered layout size. The HTML source explains that `sizes` supplies a source size used with width candidates; `picture` can change art direction or format selection. Its conformance rules prohibit mixing width and density descriptors in one srcset and duplicate descriptor values, and require width descriptors to match a resource's natural width. User-agent resource choice and available formats remain part of the observation. Do not reduce correctness to “always picked the smallest larger file” across every browser, cache state, or user preference.

**Proposed exercise, not run:** create three simple, original images with known intrinsic dimensions and labels. Use eight HTML cases: width candidates with correct sizes; deliberately wrong sizes; density candidates; mixed-descriptor invalid input; duplicate descriptor; picture art direction across one breakpoint; unsupported declared format with fallback; and a lazy image with auto sizes only where allowed. Test fixed viewports 360 and 1024 CSS pixels and DPR 1 and 2, first with a cold temporary profile and then a warm run. No third-party images or network analytics. Maximum 32 primary combinations per browser; limit exploratory repeats to three per discrepant case.

**Report requirements.** Retain HTML/CSS, intrinsic resource dimensions and bytes, viewport/DPR, `currentSrc`, request timing, rendered dimensions, and cache state. Distinguish invalid author markup, permitted browser choice, and a measured loading defect. Do not infer source-size semantics from `naturalWidth` alone because density correction matters. The negative control is a checker using the fallback `src` attribute rather than the selected `currentSrc`; it should miss at least one valid responsive selection.

## Rights, report shape, and stopping rule

This dossier uses original paraphrase and links. No third-party demo, illustration, browser trace, or source snapshot is redistributed. Complete per-page reuse terms were not established for every web source, so later code/demo copying requires a separate rights check. The W3C document's draft status and licensing are separate questions: permission to reuse text would not make the draft implemented. Prefer self-authored fixture code and images.

For every future report: pin source capture dates and browser/runtime versions; state the question, expected outcomes and exceptions before running; retain bounded fixture files and hashes; provide observed results and failures; list not-run cases; include the negative control; and propose one revision based on the smallest reproducible discrepancy. A reviewer should replay that discrepancy without access to the author's conclusion. Keep publisher observations separate from formal conformance or security claims. Stop adding cases when two successive additions only repeat a known mechanism or when execution would need production browser state. Consolidate first, then decide whether a training phase is justified.
