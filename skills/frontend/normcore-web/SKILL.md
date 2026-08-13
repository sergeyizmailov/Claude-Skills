---
name: normcore-web
description: >-
  Use when building or restyling a website that should look like ordinary, long-running
  commercial web rather than a freshly art-directed product — B2B and professional services,
  online shops and catalogues, news and publishing, corporate and institutional sites,
  directories and portals. Covers the plain 2012–2020 commercial register — default fonts,
  dense functional layout, no motion, real photographs. Trigger on explicit requests for a
  conventional corporate, page-builder, legacy-agency, retail, or "real company website"
  appearance. Do not trigger merely because a design should look less AI-generated. Not for
  product UI, SaaS app shells, dashboards, portfolios, or editorial brand sites.
---

# Normcore Web

Ordinary commercial web of the 2010s — roughly 2012–2020. Plain, dense, static, functional: a
site that looks **operationally evolved rather than freshly art-directed.**

That target era is fixed and does not move. What moves is the thing you are avoiding — the
current fashion in product design. Read every "modern" and "contemporary" below as *now*,
whenever now is, and the skill stays correct without edits.

## Who you are

Before the rules: **take the role, and answer every unlisted question from inside it.** The
rules below cover maybe a hundred decisions. A page has thousands. What you default to on the
rest is what decides whether this works — and a model in compliance mode defaults to whatever
year it is being run in.

You build websites for local firms. You have done it for years and you are good at the parts
the client notices. Your working situation:

**What you reach for.** Whatever the project already has. Then an established library for
genuinely non-trivial functionality — carousel, form, cookie notice, phone-prefix field —
because writing it yourself is billable time nobody approved. A block copied from the last site
you built and recoloured.

**What you have never seen.** The list below is what current product design looked like when
these notes were written. **Whenever you are reading this, substitute what is fashionable in
product and app design now** — that is the thing you have never seen. The rule is structural:
you are decades behind whatever "current" means today, and the specifics only ever illustrate it.

Dark-mode toggles. Design tokens. A component library. Figma
handoff. `clamp()`. Container queries. Bento grids. Glassmorphism. Inter at negative tracking.
Hairline `rgba(255,255,255,.08)` borders. Noise or grid overlays. A radial-gradient spotlight
behind a hero. Monospace accents and terminal blocks. Oversized rounded cards on a slightly
different background. A badge pill above a headline. Gradient-stroke borders. A logo strip at
40% opacity. A right-aligned "Sign in / Get started" pair. You are not avoiding these — **they
are outside your visual vocabulary.** If your hand moves toward one, that is not your hand.

This constrains **taste, not competence.** You recognise modern technique when the project
already uses it and you keep it — you simply would never have chosen to *look* like that. Never
add a dependency, and never bypass a component the project already has, in the name of the
role.

Shorthand at the time of writing: nothing that would sit on Vercel, Linear, Supabase or Stripe.
If those names mean nothing to you, the shorthand still holds — **whatever the four most
admired developer-product sites are when you read this, you have never opened them.**

**What you would never do.** Spend an afternoon on a hover state. Argue that the phone number
should come out of the header — the client wants it there and the client is right. Cut the
paragraph the client wrote to make a section breathe. Redesign the footer because the header
changed. Unify the corner radii across the site; you set each one once, in a panel, and moved
on.

**How you judge finished.** The client can find their phone number, the sections the brief
listed are all there, it does not break on the office iPad, and the invoice can go out. Not
"is it beautiful".

**Where you do not take the role:** accessibility, contrast, focus states, honest content, and
maintained dependencies are held to today's standard. You inhabit the era's *taste*, never its
carelessness — see "Defects are evidence, not instructions".

## How to run this

1. Pick the archetype (table below) and read that one file. Do not read the others.
1. Roll the build's history — year, platform, bolt-ons, maintainer — and roll a point on each of
   the archetype's variation axes, using the seed method below. Do this **before** laying
   anything out; it decides the shape. Show the arithmetic in your report.
2. Confirm the genre fits — if the brief is only "less AI-looking", stop and use
   `design-taste-frontend` or `impeccable` instead.
3. Gather real assets first: photographs, logos, an icon font. Nothing is drawn or generated,
   nothing is a placeholder box. What you cannot source, ask for.
4. Build against the core register below plus the archetype's skeleton and density model.
5. Run `node scripts/checks.mjs <url>` — ornament, wordmark, assets, contrast, focus rings
   and the 14-width sweep in one pass. Then the tables in `references/verification.md` and the
   checklist at the end of your archetype file.
6. Run `references/visual-check.md` — screenshot beside two real sites and look at it. This
   is the step that catches "still looks too modern"; the checklists cannot.

## What this actually is

Not "WordPress style" — of the sites measured for these notes, most are not WordPress at all;
an electronics chain, two newspapers, a hospital trust and a directory all sit squarely in the
register, and the one WordPress build among them was a university. What they share is **trust
through unfashionableness**: the site is not treated as a product, so it
accumulated rather than being designed.

The mechanism differs by genre, and the mechanism determines the layout:

| genre | what generates the look |
|---|---|
| professional services | a page builder and an operator who is not a designer |
| shop | a product catalogue and a merchandiser filling promo slots |
| news | a CMS, an editor, and ad inventory |
| corporate / institutional | ten departments each owning a page, over ten years |
| directory | a database with a search form on it |

Pick **one primary archetype**. Real sites are sometimes hybrids — a shop with a newsroom, a
directory with checkout — so borrow the single module you need from a second file rather than
running two grammars at once.

**Do not carry one genre's grammar into another wholesale.** Long SEO prose and photo bands belong to
professional services and are wrong in a shop, where trust comes from catalogue density,
visible prices, stock and delivery terms.

## The success criterion

**Not** "are the tokens right". The values in these files are measurements, not a design system,
and the recurring failure is treating them as one — applying each perfectly yields a *systematic
modern imitation of an unsystematic site*.

The test: **does this look like a site that has been running and accreting for eight years?** If
it reads as composed — every section one clear job, tidy rhythm, coordinated palette — you have
failed regardless of the audit. Both recorded failures passed their token audits, so judge by
eye: `references/visual-check.md` is mandatory before finishing.

**Scale the comparison to the business, not the reference's size.** A national chain runs five
overlapping promo campaigns because it has a marketing department; a single-branch merchant does
not, and inventing that clutter is as false as over-polishing. Match the reference's *register*,
never its headcount.

## Pick an archetype

Read the core below, then exactly one archetype file. They carry the block vocabulary, the
density model, and the core rules they are permitted to override.

**Their page skeletons are menus, not templates.** Every one is a numbered list because order
matters where it matters — but you pick which blocks exist. Drop at least two the brief has no
content for, and let the history you fixed above decide the rest.

| archetype | file | for |
|---|---|---|
| Professional services | `references/archetypes/professional-services.md` | legal, licensing, formation, immigration, accounting, logistics, trades, industrial services. Lead-gen |
| Shop / catalogue | `references/archetypes/ecommerce.md` | retail, wholesale, parts, any priced inventory |
| News / publishing | `references/archetypes/news-media.md` | newspapers, trade press, magazines, company newsrooms |
| Corporate / institutional | `references/archetypes/corporate-institutional.md` | banks, insurers, utilities, universities, hospitals, government, large multi-department firms |
| Directory / portal | `references/archetypes/directory-portal.md` | listings, member registers, search-first sites |

## Roll the build — do not choose it

**Measured failure:** two runs of one brief, given free choice, picked the same point on six of
eight axes and even collided on the invented brand name. Free choice converges. So derive the
choices arithmetically instead — deterministic per project, but different across projects,
which is the property that matters.

**The seed** is the client's or publication's name with spaces and punctuation stripped. Call
that string of letters `N`.

For the list or axis numbered `k` — top to bottom, the first is `k=0` — take **letter number
`k` of `N`**, wrapping back to the start if `N` runs out. Convert that letter to its position
in the alphabet (a=1 … z=26) and take it `mod n` for a list of `n` options, counting options
from 0. Work top to bottom and write the arithmetic into your report.

Worked example, `Thornmere Water` → `ThornmereWater`, against eight binary axes:

```
letter     T    h    o    r    n    m    e    r
alphabet  20    8   15   18   14   13    5   18
mod 2      0    0    1    0    0    1    1    0
```

**Use the letters, not the name's length.** Every axis table is binary, so a length-based
`(S + k) mod 2` just alternates as `k` increments — which collapses every project in the world
onto one of two profiles that are exact inverses of each other. Spelling the name out moves the
axes independently.

If a rolled option is genuinely impossible for the brief — a shop with no promo banners cannot
roll "carousel" — step to the next option and say why. Do not re-roll until you like it, and do
not quietly land on the option you would have picked anyway.

The seed also breaks name collisions: if the invented name is the first one that comes to mind,
it is the one every other run will also produce. Take the brief's own specifics — the region,
the trade, the founder's surname, the street — and build the name from those instead.

## Fix the build's history before you start

You are not designing a site. You are **the person who has been maintaining this one since it
was built** — so decide when that was and what has happened to it since. State your four
choices in your report; they are what stop every build coming out identical.

**1. Year it was first built** — each has different bones:

| | consequences |
|---|---|
| 2012–14 | narrower container (~960–1140), left sidebar rails on inner pages, smaller type (H1 30–40), visible 1px borders everywhere, boxed widgets, breadcrumbs on every page |
| 2015–17 | full-width bands arrive, container ~1170–1200, H1 40–50, flat colour sections, first carousels, icon fonts everywhere |
| 2018–20 | container 1240–1300, H1 50–110, full-bleed photo bands, sticky header, a rounded corner or two creeping in |

**2. What it was built on** — a bought ThemeForest theme (strong opinions you worked around, its
own H-scale and button shape) · a page builder on a starter theme (panel-styled widgets, spacers,
per-element CSS) · a local agency's own theme (tidier, fewer widgets, one consistent grid) · a
platform's stock theme lightly recoloured (shops especially).

**3. What was bolted on since** — pick one or two. A header redesigned two years ago while the
footer never was · a new section built in the newer style, sitting next to old ones · a plugin
whose CSS never matched (its own font-size, its own radius) · a page nobody has touched since
launch · a second brand colour introduced for one campaign and never removed.

**4. Who maintains it** — an agency on retainer (competent, consistent) · the owner's marketing
person (content current, layout untouched since launch) · nobody since 2019 (dated but coherent)
· a succession of freelancers (the most heterogeneous, and the most authentic).

These are not flavour. A 2013 agency-theme build maintained in-house looks materially different
from a 2019 builder site with three bolt-ons, and both are correct. **Two runs of this skill on
the same brief should not produce the same page.**

## Page types

Each archetype's skeleton describes its **front page**. Most briefs are for a secondary page —
an article, a results list, a category, a service page — and the rule is the same everywhere:

**A secondary page keeps the entire outer chrome and replaces only the listing region.** Same
topbar, masthead, navigation, sidebar, footer, ad slots and floating layer; the river or grid
becomes the one thing the page is about, wrapped in a breadcrumb above and related links below.

Resist stripping the chrome for reading comfort — a reduced "reading mode" header is a modern
publishing pattern and instantly dates the page. A CMS of this era does not vary the furniture
per page type.

Density benchmarks in `references/verification.md` are **front-page figures.** A secondary page
typically lands at 30–50% of the front page's link count because the listing is gone while the
chrome remains. Where an archetype has a measured secondary figure it says so.

## Core register — all archetypes

"Banned ornament" is the checkable form of "What you have never seen" — the same thing written
so it can be audited, plus the items that need precise definition.

### Banned ornament

Passes every token check and still marks the page as contemporary:

- **Eyebrow / kicker labels above a heading** — small-caps accent text, with or without a
  rule, dash or icon. The strongest modern tell after icon cards. A heading starts the block.
- **Decorative rules, dashes and divider lines** used as ornament rather than structure.
- **Icons as decoration** — an icon appears only where it labels a thing.
- **Two-tone or multi-colour wordmarks.** One colour, or an image file.
- **◆ Decorative button variants.** Professional services has exactly two: solid accent, solid
  white. Shops, directories and institutions may add one functional tertiary action (compare,
  save, secondary text link). Never a ghost or gradient-outline variant for visual variety.
- **Uppercase or letter-spaced button labels.** Measured: 15px, weight 400, sentence case.
- **◆ Decorative pills** — section-number chips, progress rails, animated counters, and pills
  used as ornament. *Functional* labels are fine and genre-correct: a news section tag, a
  directory status chip (Open now, Verified), a shop badge. Those are solid rectangles that
  carry information, not rounded decoration.

### Motion: none

```
transition: color .3s, background-color .3s, border-color .3s
```

Hover changes colour. Nothing moves — no scale, lift, slide, underline sweep, colour wipe,
growing pseudo-element. No scroll-linked motion, stagger, parallax, counters, intersection
reveal, spring, marquee.

**`transform` is banned as animation, not as a tool.** Never in a `transition` or
`@keyframes` you write. Static positioning (`translate(-50%,-50%)` to centre something) and a
component library's internals are fine — they change nothing on screen.

Measured `transform` transitions per page: two regional dailies **0** and **0**, a university
**0**, a hospital trust **2**, an in-register electronics chain **3**. Every button hover on
the professional-services reference is a flat swap to a pale tint of the accent
(`background:#DAE3FF; color:#0F2E93`) — not one scales. This holds across every genre.

### Typography

One workhorse family, three weights — 700 / 500 / 400. **Open Sans, Arial, Lato, Roboto,
Noto Sans, Source Sans, Work Sans, Montserrat.** Measured most-used face: a university Open
Sans, a hospital trust Arial, a regional electronics chain, in register Lato, a national business directory Open Sans.

Fixed px sizes with full re-declaration at 1024 and 767. **No `clamp()` on type** — the ban is
visual, not stylistic: fluid type scales smoothly as the window moves, stepped type snaps at
breakpoints, and that snap is a visible period signal. Container queries are permitted where
the rendered result is identical. No negative tracking, no display+body pairing. Mixing `bold`/`normal`/`400`/`500` in one
stylesheet is authentic — do not normalise.

**Exception, news only:** a serif headline face over a sans body is correct and measured
(an English regional daily Merriweather + Open Sans, a Scottish daily Source Serif + Libre
Franklin). Nowhere else.

### Responsive — era-correct, and required in the first pass

Ship adaptive on the first build; never as a second pass. The *method* is itself a period
signal, so do not reach for a modern fluid system:

```
breakpoints   1024 and 767/768 — the two the era used. Add an intermediate one only where a
              real grid breaks between them (a percentage float grid with fixed margins
              overflows at ~768 long before the declared breakpoint)
type          re-declare every heading size in px at each breakpoint
columns       side-by-side percentages collapse to 100% at 767. Two-up on tablet is fine
container     min(100%, 1240px) with 15-25px side padding below 1024
images        max-width:100%, height:auto, width/height attributes always set
tables        wrap in overflow-x:auto — never restyle a table into stacked cards
nav           collapses to a hamburger with a plain stacked panel, no slide-in animation
touch         44px minimum on primary controls — nav items, buttons, form fields, icon
              buttons. Not on links inside a dense text list or a headline river, which no
              real site of this kind sizes up. Phone numbers are real tel: links
```

Verify by sweeping every width in `references/verification.md`, not four breakpoints —
overflow hides between them. For rescuing an existing non-responsive page, hand off to the
`responsive-adapter` skill; this section is for building it right the first time.

### Sharp over round

Measured button radii across five professional-services sites: **2 · 4 · 6 · 10 · 25**.
Shops: a regional electronics chain, in register 2px dominant, a second electronics chain, drifted modern 4px. Institutional: a university 2px,
a hospital trust 2/10px. **Default to the sharp end.** Rounding everything is the fastest way
back into a modern landing page. Fix one radius per element *type* and refuse to reconcile
across types — button and photo disagreeing is correct.

### Shadows

**Professional services: none in content.** the professional-services reference ships zero; the two on screen
come from the sticky header and floating plugins.

Other genres do carry them, measured: a regional electronics chain, in register 28, a large international chain 39,
a Scottish daily 46, a hospital trust 42, a university 14, a national business directory 1. Where an archetype
permits shadows they are **one crude value reused**, never a layered designed set. Check your
archetype file.

### Inconsistency is placed, not random

Fix one value per element type, then refuse to reconcile across types. Never derive spacing
from a scale. Never normalise third-party artwork. Leave one or two of the builder's or
theme's stock greys in the palette — a perfectly coordinated palette is a designer's artefact.

Randomness reads as broken. The bones stay square: do not misalign the grid or break the
container.

### Spacing is front-loaded

Real builds reuse three or four values for almost everything, with a thin tail of one-offs.
Measured distributions live in the archetype files.

The rule is **do not enforce a scale**, not "insert random numbers". Where a block genuinely
needed 17px because of what was in it, leave 17px rather than rounding it into the system.
Scattering values to look handmade reads as broken. Exempt: percentages, breakpoints, library
internals.

### Cosmetic only, never functional

Contrast, focus, hit targets, keyboard order and alt text hold to the **current** standard,
whatever it is when you read this — not the era's. **This
survives a brief that says "nothing needs to function" or "appearance only"** — a static
mockup still gets real contrast, real focus rings, 44px targets, real `alt`, and carets that
actually open their submenus. Those are the floor, not features to defer. Three traps
this register produces every time:

- `a { color: accent-deep }` is dark and leaks onto photo or dark bands → set white there
- that rule then out-specifies `.btn-2 { color: accent-deep }` → white-on-white. Pin it
- **picking an accent off a variants table and assuming white text works.** Three of the five
  in `references/archetypes/professional-services.md` fail — gold 2.47, yellow 1.51, green
    3.21 — and a mid-tone teal like `#0B8FA8` measures 3.81. Compute before choosing the label
    colour

A caret must open a real submenu — keyboard reachable, `aria-expanded`, Escape closes.

### Never generate an asset — source it, or ask

Do not **design or hand-author** icons, illustrations, patterns, dividers or decorative
graphics — no CSS-drawn stand-in, gradient rectangle as photo,
letter-in-a-circle avatar, drawn seal, **no AI-generated image**.

The ban is on invention, not on the SVG format. An official brand logo in SVG, an icon set's
own SVG sprite, or a project's existing icon component are all correct and stay as they are —
never downgrade a real vector logo to text or a bitmap to satisfy the rule. Resolve in order: project
folder → real artwork of a known brand or body → a real photograph downloaded → **ask the
user**.

**No placeholder boxes, and no reserved voids.** A grey "LOGO" rectangle, a dashed outline, a
"VIDEO PLACEHOLDER" slot turns the page into a wireframe — and so does a large empty band left
standing where something was meant to go. If a slot cannot be filled with something real,
collapse it and keep the markup with a comment; never ship visible emptiness. Every logo is a real logo file; every photo
slot holds a real photograph. Cannot source it → put a real photograph there and say to swap
it, or drop the slot and ask.

| need | source |
|---|---|
| icons, social glyphs | an established icon font, current stable major — Font Awesome Free, Bootstrap Icons, Material Icons |
| photography | Unsplash · Pexels · Pixabay · Wikimedia Commons |
| brand, partner, press logos | client's own files; for public companies, Wikimedia Commons (`commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch=filetype:drawing <brand> logo&gsrnamespace=6&prop=imageinfo&iiprop=url&iiurlwidth=330&format=json`) |
| review badges, seals, certification marks | the issuing platform's or body's own asset file |
| own logo when no file exists | the company name set as a real wordmark in the page font, one colour. A finished lockup, not a stand-in |
| video | a real embed or platform poster frame. None available → a real photograph, never an empty player |

**Check the logo variant you downloaded.** Brands ship monochrome and reversed versions
alongside the full-colour one, and an SVG with no `fill` declared inherits `currentColor` and
renders flat black — which looks wrong beside full-colour siblings in the same row. Open each
logo on its own before shipping it: it must carry its own brand colours. If it does not, fetch
the colour variant rather than tinting it yourself.

Download locally, never hotlink. Always set `width`/`height` and `max-width:100%`. Optimise
to delivered size. Keep proportions; let displayed sizes differ. Record attribution where the
licence requires.

Subject guidance per vertical, including retail and news: `references/photo-subjects.md`.

### Prefer existing components

The rendered artefact reads as real: Swiper's arrow-and-dot furniture, an icon font's glyph
metrics, a country-prefix phone select. Font Awesome · Swiper · the project's own
grid/accordion, else Bootstrap · intl-tel-input · flatpickr · GLightbox. Keep the project's
stack. **One dependency rule, and it overrides anything that reads otherwise:** reuse the
project's existing components and its pinned versions; add a dependency only for functionality
genuinely required, at the latest version compatible with the project — not reflexively the
newest major; never add one for period accuracy or to serve the role.

### Defects are evidence, not instructions

References ship typos, trailing spaces in labels, stray colons, an unbalanced `}` killing a
media query, dead font declarations, untouched factory colours. Those show the process — one
operator, no review. Reproduce the *process*: awkward composition, unreconciled tokens,
repeated blocks. Never the output errors.

### Content mode

State which one you are in before writing copy.

**Production** — a real client's site. Never invent prices, discounts, stock levels, reviews,
warranties, credentials, article authors or datelines, client names, or institutional
notices. Never invent the entity's own facts: legal name, address, registration numbers,
headcount. Missing copy is marked placeholder text plus a list of what to supply.

**Fixture / demo** — a style test or template. Fictional content is allowed, must be
recognisable as fictional, and must not imply affiliation with a real organisation. Say in
your report that it is a fixture.

Either way: placeholder *copy* is fine; placeholder *images* do not exist.

## Keeping this current

Nothing here needs rewriting as time passes, by design:

- **The target era is fixed.** The 2010s commercial register does not move.
- **What you avoid is defined relatively** — "current product-design fashion" resolves itself
  whenever this is read. Named companies and specific effects are illustrations with a
  shelf life; the structural rule outlives them.
- **Version numbers are evidence, not recommendations.** Where a file records
  `Elementor Pro 3.29.2`, that documents what was measured. Install current stable majors.
- **Reference URLs rot.** `visual-check.md` carries a test for whether a candidate site is
  still in register, so a dead link means substitute, never skip.
- **Measurements can be refreshed** without touching the rules: the mining recipe at the end of
  `archetypes/professional-services.md` regenerates the distributions from any live reference.

If a section ever reads as dated, it is the illustrations, not the method. Replace the examples
and leave the structure alone.

## Files

| | |
|---|---|
| `references/archetypes/*.md` | one per genre — block vocabulary, density model, permitted overrides |
| `references/photo-subjects.md` | what to photograph, per vertical |
| `scripts/checks.mjs` | runnable: everything a machine can see, in one pass |
| `references/verification.md` | the regression tables a machine cannot check |
| `references/visual-check.md` | **mandatory before finishing** — screenshot beside real sites and score |
