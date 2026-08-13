# Visual check

The token checklist cannot detect "still looks too modern" — both recorded failures passed
their audits. **Look at the page next to a real one before calling it done.** This step is
not optional and cannot be replaced by reading the CSS.

## Capture

Pick the two or three references matching **your archetype**, never a generic sample.

**These URLs will rot.** Sites get redesigned, go behind bot challenges, or disappear. The
named ones are a starting point, not the method. If one fails, find a replacement by class —
and verify the candidate is still in register before comparing against it:

> **Is this candidate usable?** Open it and check: one workhorse sans (or a serif headline face
> for news), corners at or near square, nothing that moves on hover, dense text or dense
> listings, real photographs, no ornament above headings. If it fails those, it has been
> redesigned — find another. Any long-running firm, county newspaper, utility, university,
> regional retailer or listings site in the target genre will do.

Never skip the comparison because a URL broke. Substitute.

**No named URLs here on purpose** — they rot, and a list of them ages worse than a method.
Find two live references per build with these searches, then qualify them:

| archetype | search for |
|---|---|
| professional services | `"company formation" OR "licensing consultancy" site:*.com` · a law or accountancy firm that has traded for 15+ years |
| shop | a national electronics or tool retailer in a mid-size European market — not the global flagship brands, whose sites are designed |
| news | a county or regional daily, or a trade weekly · `"est. 18.." newspaper` |
| corporate / institutional | a regional water or energy utility, an NHS-equivalent hospital trust, a public university |
| directory | a national business directory, a trades register, a classifieds portal |

> **Qualify the candidate before comparing.** Open it: one workhorse sans (or a serif headline
> face for news), corners at or near square, nothing that moves on hover, dense text or dense
> listings, real photographs, no ornament above headings. Fails those → it has been redesigned;
> search again. A large chain with a commissioned typeface will *feel* dated and still be a real
> design system — not a target.

Never skip the comparison because you could not find a reference. Search again.

```bash
cat > /tmp/board.mjs <<'EOF'
import { chromium } from 'playwright-core';   // or an absolute path to it
const SHOTS = [
  ['ref-a', 'https://REFERENCE-ONE'],
  ['ref-b', 'https://REFERENCE-TWO'],
  ['mine',  'file:///ABSOLUTE/PATH/index.html'],
];
const b = await chromium.launch({ executablePath: process.env.CHROME_PATH });
for (const [name, url] of SHOTS) {
  const p = await b.newPage({ viewport: { width: 1440, height: 1000 } });
  try {
    await p.goto(url, { waitUntil: 'load', timeout: 45000 });
    await p.waitForTimeout(2500);
    for (let i = 0; i < 3; i++) {
      await p.evaluate(y => window.scrollTo(0, y), i * 1900);
      await p.waitForTimeout(400);
      await p.screenshot({ path: `${name}-${i}.png` });
    }
  } catch (e) { console.log(name, 'failed:', e.message); }
  await p.close();
}
await b.close();
EOF
CHROME_PATH=<chrome-headless-shell> node /tmp/board.mjs
```

No headless browser available? Open your page and one reference side by side in a real
browser at the same window width and compare them by eye. The comparison is mandatory; the
automation is not.

Then **open the images and look at them.** Reading the HTML back is not this step.

## Score against the board

Answer each out loud. Any "mine" answer that is the tidier one is a failure.

**Universal — every archetype:**

| | reference | yours |
|---|---|---|
| Corners | how sharp? | sharper or equal, never rounder |
| Hover | what actually moves? | nothing moves; colour only |
| Ornament above headings | none | none |
| Is the palette coordinated? | no, stock greys sit in it | no |
| Does it look art-directed? | no | no |
| Could you tell which is the newer build? | — | **it should not be obvious** |

**Then the genre question — one only, yours:**

| archetype | ask |
|---|---|
| professional services | Is every band full of prose, or does it breathe? Does a CTA row close each photo band? |
| shop | Is the price the loudest thing in the tile? Is the grid crowded enough to scroll past? Do tiles stay still on hover? |
| news | Can you count 250+ links? Are river items headline-and-timestamp with no summaries? Are unfilled ad slots collapsed rather than left as blank bands? |
| corporate / institutional | Does the nav go deep? Is there a notices strip and a dated news list? Is the hero signage rather than a sales pitch? |
| directory | Is it rows with hairlines rather than cards? Is the search block loud and slightly crude? Numbered pagination? |

Text volume, section repetition and image count are **not** universal criteria — a directory
has almost no text and a shop has almost no prose. Use the density table in
`verification.md`.

That last row is the whole test. If yours is instantly identifiable as the modern one, the
token audit passing means nothing.

## Controls — optional, not shipped with the skill

**These are workspace artefacts, not part of this skill.** They exist only in the project they
were built in. If the paths below are absent, skip this section entirely and use the live
references above — nothing here is required.

| | verdict | what it shows |
|---|---|---|
| `references/skill-test-2/` (industrial refrigeration) | **user-approved** | what "right" looks like for this skill |
| `references/forward-test-sonnet-safety/` (safety training) | close, one flaw | correct except a wireframe placeholder box in the hero — since banned |
| `references/normcore-forward-test-pumpworks/` (pumps) | **rejected** | token-compliant and visually wrong: kickers, animated nav underline, scale hovers, uppercase buttons, rounded everything, too composed |

Paths are relative to the project those were built in. The negative control is the more
useful of the three — compare against it and ask which of its faults you have repeated.

## The two failures on record, and what fooled the audit

- **Rounded + polished.** Every radius at the top of its range, hover scale on every button,
  perfectly ranged headings. Each value individually within the skill's stated bounds; the
  sum read as a modern landing page. Default to the sharp end.
- **Wireframe furniture.** A dashed grey "VIDEO PLACEHOLDER" box in the hero. It satisfied
  the then-current asset rule and made the page look unfinished rather than ordinary.
