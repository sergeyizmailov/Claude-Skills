# 03 — Domains, redirects, trackers, the review layer

Reviewed 2026-08-27. Tracker metric discipline → `tracker-ops`. Conversion mechanics →
`google-ads/06`.

## What AdsBot actually does

AdsBot **fetches the Final URL chain** as part of ad review and ongoing enforcement. This is the
structural difference from Facebook: the destination is inspected directly, repeatedly, and after
approval.

**Destination requirements** [official]:

- Must "work on common browsers and devices" and must not "return an HTTP error code for Google AdsBot
  web crawlers on common devices globally". **Blocking or erroring the crawler specifically is itself a
  violation surface**, not just a UX problem. AdsBot egress is **primarily US** — geo-blocking the US
  is Destination not accessible even if the buy geo is EU/ASIA. A WAF 429 is the same class as 403.
- **"Redirects from the final URL that take the user to a different domain"** is explicitly prohibited
  language. Same-domain redirects are the tolerated case.
- **"Tracking templates and expanded URLs must lead to the same content as the final URL."** This is
  the operative sentence for the entire tracker layer.
- Display URL domain must match where the user actually lands.
- Pages "solely designed to send users elsewhere", replicated or scraped content, and incomprehensible
  content are named violation patterns.

**Enforcement: destination requirements carry a mandatory 7-day warning before suspension.** They are
not on the egregious track.

## Where the line actually is

Google publishes **no** page distinguishing an allowed tracking redirect from prohibited content
substitution **by protocol**. There is no official "302 is fine, JS is not" statement. The policy text
is intent- and outcome-based, split across two pages:

- **Abusing the ad network** — *Evasive ad content*: "Manipulation of ad components like text, image,
  videos, domain, or subdomains in an attempt to bypass detection or enforcement action is not
  allowed." *Circumventing systems*: **egregious, immediate suspension, no warning step.**
- **Misrepresentation** — carries the destination-mismatch language: "Promotions that are not relevant
  to the destination are not allowed"; promising things in the ad that are "unavailable or aren't
  easily found from the destination" is a violation.

**The enforceable question is whether the destination is relevant and available as advertised, and
whether content differs conditioned on who is requesting it. Not which redirect mechanism was used.**

Serving different content to reviewers than to visitors is Circumventing systems — **no warning,
permanent, propagates**. Filter stacks, white-page requirements, Keitaro/Adspect recipes, and
replacement-after-burn live in `05-review-layer-and-cloaking.md`. This file stays on what AdsBot
fetches and how ValueTrack is supposed to look.

## ValueTrack, tracker wiring and the gclid chain → `tracker-ops/04`

`tracker-ops/references/04-google-lane.md` owns this end to end: the escaping ladder
(`{lpurl}` / `{lpurl+2}` / `{ignore}`, literal `?` vs `%3F`), the Keitaro and RedTrack
configurations, the gclid → OCI chain, backdate windows, the dedup key, and timezone discipline.
Do not restate it here.

What is grey-specific and belongs in this file:

- **The tracker hop is the hop that must satisfy "same content as the final URL."** Every ValueTrack
  fact matters here only because AdsBot re-fetches that chain (`## What AdsBot actually does`, above).
- **Tracking-template changes take 24–48h to propagate.** A chain judged sooner reads as a moderation
  problem when it is a propagation delay. This misdiagnosis burns accounts that were never flagged.
- **Keitaro's own guidance: disable cookie tracking to reduce moderation risk** — a vendor telling you
  its default raises review exposure.
- **Do not use RedTrack funnel filters as a cloak.** The vendor itself says filtering "won't be useful"
  for Google Ads no-redirect campaigns; using it that way is a circumvention attempt with none of the
  function. Cloaking and the review layer → `05`.
- **Uncertified tracker hosts** in the visible chain are a Destination-mismatch surface — see the
  certified-tracker note above and the disapproval codes in `05`.

## Domains

**Safe Browsing / Web Risk** [official]:

- **Malware** — "software or mobile application specifically designed to harm a computer, a mobile
  device, the software it's running, or its users".
- **Unwanted software** — behavior that is "deceptive, unexpected, or that negatively affects the
  user's browsing or computing experience".
- Search Console's Security Issues report splits **Malware** (web-based, no user action) from
  **Harmful downloads** (requires an explicit download).

**Critical tier distinction inside the same Ads policy page:**

- **Malicious software** — egregious. Immediate suspension, no warning, permanent.
- **Compromised site** — "destinations which are hijacked and hacked" — enforced as **ad disapproval**,
  a much lighter tier. **Do not treat a compromised-site flag as a death sentence.**

**The scope clause that explains otherwise inexplicable burns:** the malware ban applies to software the
site "hosts or links to, **regardless of whether the software is promoted through the Google advertising
network**". It is a domain/account-level flag — a domain flagged for something unconnected to the
running campaign still burns the account.

**A Google domain burn has wider blast radius than a Facebook one.** The Safe Browsing flag is a
**cross-Google-product signal** — it surfaces in Search Console Security Issues and can affect organic
visibility, not just Ads. On Facebook a domain block is platform-scoped.

### Rotation discipline

Rotate on **signals, not a timer.** Fixed-timer rotation burns a working domain early and does nothing
for a domain flagged the day after you reset the clock.

Signals that should trigger rotation:

- A Safe Browsing / Web Risk flag in Search Console Security Issues.
- AdsBot fetch errors appearing in the account.
- A mass-disapproval wave hitting ads pointing at **that domain specifically** while other domains in
  the same account stay clean — that isolates the burn to the domain.
- Hosting-side compromise indicators, including a shared-hosting neighbor's known breach. Rotate off
  compromised-adjacent infrastructure **before** the crawler finds it.

**Attribution discipline — change one variable at a time.** If a *fresh domain* on an *existing clean
account* still gets mass-disapproved, the account or its payment/identity signal is implicated, not the
domain. If a *new domain* clears review on the same account that just had another domain
mass-disapproved, the prior domain was the burn.

> 🔺 **Honest gap:** this single-variable discipline is a well-founded borrowing from the Facebook-side
> doctrine in `meta-grey-ops`. It was **not** found in any reachable Google-specific source — every forum
> carrying that discussion (afflift, BlackHatWorld, Reddit) was inaccessible. Treat it as sound method,
> not as observed Google-side practitioner consensus.

🔺 **Second honest gap:** no source connects **expired-domain vetting** (Moz Spam Score, Majestic Trust
Flow, domain-age tooling) to **Google Ads** account safety. All such material is pure organic-SEO/PBN
framing. **Do not assume the SEO practice transfers to Ads risk.**
