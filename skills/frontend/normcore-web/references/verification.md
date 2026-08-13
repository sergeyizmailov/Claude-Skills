# Verification

Any left-column item is a regression. **Rows marked ◆ are archetype-dependent — check your
archetype file before treating them as failures.**

## Genre density targets

The density model differs per archetype and is the fastest way to tell you built the wrong
genre. Measured:

**These are front-page figures.** A secondary page — article, results list, category — runs
about 30–50% of the link count with the same chrome. See "Page types" in `SKILL.md`.

**Scale every row to the content that exists.** A single-branch trader with 50 products has
50 images and that is correct; a small newsroom does not reach newspaper link counts. These
detect a *genre mismatch*, not a word count — never pad toward them with invented inventory,
articles or departments.

Shadow figures are **evidence of what the genre tolerates, not a target.** The rule is one
crude value reused where an element needs separating; eight is fine where the reference had
forty. Never add shadows to reach a number — that is the "technically compliant, visually
wrong" trap.

| archetype | links | images | shadows seen | prose |
|---|---|---|---|---|
| professional services | low | ~40 | **0** | 60–90 word paragraphs, 2–3 per band |
| shop | moderate | **121–353** | 9–39 | almost none; one SEO block at the bottom |
| news | **265–424** | 112–151 | 5–46 | headlines and timestamps, no summaries |
| corporate / institutional | 150–261 | **18–34** | 14–42 | short intros, then links |
| directory | ~173 | **~10** | ~1 | near zero |

These are **benchmarks for a complete home page**, not minimums to pad toward. Scale them to
the content actually supplied — a shop with nine products has nine, and you say so in your
report rather than inventing inventory. What they catch is a genre mismatch: a news home page
with thirty links is not a news home page; a shop with twelve images is not a shop.

A small company newsroom does not reach newspaper density. Route it to
`corporate-institutional` and use the news grammar only for its article list.

## Style

These apply to **every** archetype. Genre-specific checks live in the archetype file — run
both.

| wrong | right |
|---|---|
| eyebrow / kicker label above a heading | the heading starts the block |
| decorative rule, dash or icon beside a heading | nothing there |
| two-tone wordmark | one colour, or an image file |
| ◆ a decorative third button variant (ghost, outline, tinted) | two in professional services; elsewhere one functional tertiary action is allowed |
| uppercase or letter-spaced button labels | 15px / 400 / sentence case |
| spatial hover — scale, lift, slide, underline sweep, colour wipe | colour change only |
| `transform` in a transition or keyframes you authored | none. Static positioning (`translate(-50%,-50%)`) is fine; library internals exempt |
| anything reacts to scroll position | static |
| animated counters | plain static numbers |
| all radii equal | one per element type, unreconciled across types |
| radii at the round end of the measured range | default sharp — 2–6 |
| a derived 8pt scale, **or** values scattered on purpose to look handmade | ordinary front-loaded values, with odd ones only where the content actually forced them |
| `clamp()` on type | fixed px, re-declared @1024 / @767 |
| a container query that changes the visual result | none introduced; existing project ones may stay where the rendered layout is the same stepped one |
| negative letter-spacing | normal tracking |
| palette perfectly coordinated | one or two stock greys left in |
| logos normalised to one height or equal tiles | own proportions, uneven |
| a nav caret that opens nothing | real submenu, keyboard reachable, `aria-expanded`, Escape closes |
| every section has one clear distinct job | some overlap and repetition |
| could pass for a currently-admired product site | should pass for an ordinary firm's site that has been running for years |
| ◆ icon cards | banned in professional services; carved out for a retail reassurance strip and institutional text tiles |
| ◆ two text faces | one family — except news, where serif headlines over a sans body are correct and measured |
| ◆ `box-shadow` on content | none in professional services; elsewhere one crude value reused only where something needs separating — count is not a target |
| ◆ density | per the archetype's model — see the table above |
| the build's history was never fixed or stated | year, platform, bolt-ons and maintainer chosen and reported |
| every block in the archetype's skeleton was built, in its listed order | at least two dropped; order reflects the history |
| no point chosen on the archetype's variation axes | one point per axis, stated |
| it looks like the last build from this skill | two runs on one brief must differ structurally |

## Assets

| wrong | right |
|---|---|
| a hand-authored or invented `<svg>` — drawn icon, illustration, divider, seal | icon-set glyph, official brand SVG, or a real `<img>` |
| a real vector logo downgraded to text or bitmap to satisfy the SVG rule | keep the official SVG as supplied |
| a logo rendering flat black beside full-colour siblings — an SVG with no `fill`, inheriting `currentColor` | the colour variant of the same mark |
| an AI-generated or improvised image | a real sourced file |
| a placeholder box, dashed outline or "LOGO / VIDEO" marked slot | a real image — no wireframe furniture anywhere |
| an empty video player frame | a real photograph in that slot |
| hotlinked remote image | downloaded locally |
| icon is CSS shapes, emoji or a drawn path | icon-font class |
| logo is typeset text posing as a mark | real file, or company name as header text |
| "photo" is a gradient or illustration | real photograph |
| hand-written carousel or accordion | Swiper / project component, configured |
| `<img>` without `width`+`height` | both set |
| 1920px source in a 204px slot | optimised to delivered size |
| dependency added for period accuracy | maintained versions only |
| an asset's origin is unrecorded | source known, attribution kept where the licence requires |

Run the automated checks — ornament, two-tone wordmark, assets, contrast, focus rings and the
full width sweep, in one pass:

```bash
CHROME=<chrome-headless-shell> PW=<playwright-core/index.mjs> \
  node scripts/checks.mjs file:///abs/path/index.html
```

It prints image, link and shadow counts to compare against the density band above, then lists
only failures and exits non-zero. It deliberately does **not** assert `svg.length === 0` —
official brand SVGs and icon-set sprites are legitimate; it counts them for you to confirm each
traces to an icon set, a brand file or a project component.

Prose-density checking is archetype-specific and lives in `archetypes/professional-services.md`;
the other four genres have no paragraph-length target.

## Function

- **Contrast.** Every text node ≥4.5:1, or 3:1 at ≥24px / ≥18.66px bold. Check the
  three contrast traps named under "Cosmetic only, never functional" in `SKILL.md`.
- **Widths.** Covered by the script (14 widths, 320–1920). Four breakpoints is not enough —
  two offenders appear only between them: a percentage float grid with fixed margins
  (`width:17%; margin-right:25px` × 5 fits at 1440, overflows at 768 — add an intermediate
  breakpoint), and an unbreakable token in a fixed-width box (`overflow-wrap: anywhere`).
- **Keyboard.** Everything reachable, sensible order, visible focus ring. The era dropped
  focus rings; this skill does not. Every nav caret opens a real submenu: reachable by
  keyboard, `aria-expanded` maintained, Escape closes it.
- **Motion.** Nothing animates, so there is nothing for `prefers-reduced-motion` to silence.
  Confirm that is actually true rather than assuming it.
- **Images.** All load, no layout shift, `alt` real.
- **Console.** No JS errors, no failed requests.
- **Placeholders.** Zero. Every logo is a real file, every photo slot holds a photograph.
  Files the user still owes belong in the report, not on the page.
- **Build history.** The four choices — year, what it was built on, what was bolted on, who
  maintains it — stated in the report, with the variation-axis points picked.
- **Content mode.** Stated explicitly. In production mode: no invented entity names, addresses, registration numbers, dates, headcount or
  prices. Placeholder *copy* is marked as such and listed — placeholder *images* do not exist.

## Then run your archetype's checklist

`archetypes/<yours>.md` ends with the genre-specific regressions. The core table above cannot
catch building the wrong genre.

## Final — the only question that matters

Run `visual-check.md` first: capture your page and two or three real sites at 1440px and
**look at the images**. Everything above can pass on a page that is still visibly modern.
Then ask:

> Does this look like a site that has been running and accreting for eight years?

And the same question from the other side: **would the person described in "Who you are" have
made this?** Not "does it pass" — would they have bothered? Would they have known how? Anything
on the page that answers no is the thing to cut.

Not "are the tokens right" — the tokens can all be right and the answer still no. Specifically:

- Does anything hover-animate beyond a colour change? There must be nothing.
- Is every section doing one clear job with a tidy rhythm? That is a designer's page.
- Is the palette perfectly coordinated? One or two stock greys should be sitting in it.
- Does the density match the genre, or does it read as a landing page wearing a costume?

**If yours looks tidier, more composed, or better art-directed than the reference, you have
failed in the specific way this skill exists to prevent.**
