---
name: deep-research
description: Use when the user asks to deeply research, compare technologies/vendors/options, verify or fact-check a claim, investigate an unfamiliar topic, prepare a report or briefing, build a skill / knowledge base / reference document, or trace a claim to its primary source. Guides source selection, search strategy, quality filtering, verification, and structured output.
---

# Deep Research Methodology

How to find high-quality information and produce a defensible, traceable
write-up. Prioritizes primary sources over blog rewrites and SEO noise.
Output is structured (executive summary, findings by confidence, claim
ledger, gaps) so the result can be audited later instead of trusted blindly.

## Research Workflow

```
1.  SCOPE    — define question, audience, depth, deadline
2.  OUTLINE  — list items/subtopics, fields per item, success criteria
3.  PRIMARY  — official specs/docs/source code, vendor docs, RFC/W3C
4.  ACADEMIC — arXiv + Semantic Scholar + Google Scholar for foundations
5.  VENDOR   — threat intel reports, whitepapers, vendor research blogs
6.  COMMUNITY — awesome-* lists, GitHub trending, HN/Reddit (for leads, not as ground truth)
7.  VERIFY   — apply tiered verification (see Verification Protocol)
8.  TRACE    — follow every cited claim back to its primary source
9.  DATE     — flag anything stale for fast-moving topics; tag volatile sources
10. GAPS     — explicitly enumerate what you could NOT find
11. STOP?    — apply Stop Criteria before doing another loop
12. COMPILE  — produce output in the format below
```

## Stop Criteria (when to stop researching)

Stop when ALL of the below are true — do not keep grinding for marginal sources:

- Every item in the outline has at least one Tier 1 or Tier 2 source.
- Last 1-2 source loops produced no new substantive claims (diminishing returns).
- Critical/high-impact claims meet the verification tier requirements below.
- Remaining gaps are documented in the Gaps section (not silently skipped).
- You have spent the agreed iteration / time budget for the task.

If after the budget you still have critical unanswered questions, surface them
as Gaps rather than fabricating an answer. "I could not find X" is a valid result.

## Verification Protocol (tiered)

| Claim type | Required evidence |
|------------|-------------------|
| Defined by a single canonical authority (RFC, W3C/WHATWG spec, vendor docs for that vendor's own product, source code for that project) | 1 primary source is enough — cite it |
| High-impact / decision-driving claim (security, cost, breaking change, "recommended approach", numerical performance) | 2+ independent sources, at least one Tier 1 or Tier 2; if only 1 → mark Tentative |
| Conflicting claims across sources | Show both, note the conflict, do NOT silently pick one |
| Routine metadata (release date, version number, default port) | 1 primary source enough; double-check if it drives a decision |
| Community opinion / "best practice" attribution | Trace to where it originated; if origin is a single blog post, present as opinion, not fact |

Additional rules:
- **Trace to origin**: blog says X? Find the paper/RFC/commit/changelog that proves X.
- **Date check**: when was this written? Is there a newer authoritative version?
- **Version match**: does this info apply to the version under discussion?
- **Code test**: if a code snippet is load-bearing for a recommendation, confirm it runs.
- **Author check**: who wrote this? What's their track record / affiliation?

## Output Format

Structure every research deliverable like this. Adapt depth to scope but keep
the section order.

```
# <Topic>

## 1. Executive Summary
3–6 bullets: what the answer is, the main tradeoffs, the main uncertainties.

## 2. Scope
- Question(s) answered
- Out of scope
- Assumptions / constraints
- Date of research

## 3. Findings by Confidence
### Confirmed (Tier 1 primary, or multi-source agreement)
- Claim — [src]
### High confidence (Tier 1 + Tier 2 / 3, no contradictions)
- Claim — [src1], [src2]
### Tentative (single non-primary source, or partial evidence)
- Claim — [src] — why tentative
### Disputed (sources disagree)
- Claim A — [src]; Claim B — [src]; conflict description
### Unknown
- Question and why it couldn't be answered

## 4. Claim Ledger
| # | Claim | Source(s) | Date | Tier | Confidence | Notes |
|---|-------|-----------|------|------|------------|-------|
| 1 | ...   | URL       | YYYY-MM-DD | 1 | Confirmed | ... |

## 5. Sources
Numbered list with full URLs and access date. Mark Tier (1–4) and
mark volatile sources with [V] (see Volatile Sources below).

## 6. Gaps
What was not found, what was contradictory, what needs follow-up.

## 7. Stale-Risk Notes
Which findings are likely to go stale soon (vendor pricing, leaderboards,
benchmark numbers, API rate limits, deprecation timelines).
```

For short factual queries, collapse sections 3–5 into a single short table.
The structure is the contract; the length is not.

## Volatile Source Handling

Some sources go stale fast or move/disappear without redirect. Tag them
explicitly so future readers know not to trust the snapshot blindly.

Volatile by default:
- AI/ML leaderboards (LMArena, HF Open LLM Leaderboard, MTEB, etc.) — re-rank
  weekly, get retired, models replaced; HF Open LLM Leaderboard in particular
  has been deprecated/reshuffled multiple times.
- Vendor pricing pages, free-tier limits, rate limits.
- "State of X 2025/2026" survey reports — annual, often replaced.
- News aggregator front pages (HN, Reddit, Twitter) — by definition transient.
- Live dashboards, status pages, threat-intel feeds (URLhaus, abuse.ch lists).
- GitHub trending pages, "awesome-" list ordering.
- LLM model names, context windows, knowledge cutoffs (move every few months).

Handling rules:
1. Cite the volatile source AND the date you accessed it.
2. Cross-reference with at least one non-volatile source for any high-impact claim.
3. If the source moved (e.g. LMSYS → lmarena.ai), prefer the current canonical URL.
4. In the Stale-Risk Notes section, list every volatile claim with expected half-life.
5. Prefer permanent identifiers (DOI, arXiv ID, RFC number, git SHA) over URLs
   when both exist.

## Parallel Research Pattern (optional)

For large topics with **10+ independent items** (e.g. surveying 30 libraries
across same fields) AND when the environment supports subagent dispatch,
the work can be parallelized. Skip this pattern for small topics or in
environments without parallel agent support — sequential research is fine.

```
1. Define items list (what to research)
2. Define fields per item (what to collect for each)
3. Launch parallel web-search agents (3-5 at a time)
4. Each agent researches 1-3 items independently
5. Collect results, check for gaps
6. Second pass: fill gaps, verify uncertain claims
```

Key rules:
- Each agent gets a self-contained prompt with item + fields + output schema
- Agents write results directly to disk (don't hold in main context)
- Resume support: skip already-completed items on retry
- After each batch — review results, adjust strategy for next batch
- Mark uncertain findings with `[uncertain]` for second-pass verification

## Source Quality Tiers

| Tier | Sources | Trust level |
|------|---------|-------------|
| 1 — Primary | Specs (RFC, W3C, WHATWG), source code, official docs, original papers, changelogs | Highest |
| 2 — Secondary | Peer-reviewed papers, vendor threat intel (Unit42, Mandiant, Sekoia), audit reports, MITRE ATT&CK | High |
| 3 — Tertiary | Technical books (O'Reilly, No Starch), curated guides (awesome-*, OWASP Cheat Sheets), conference talks | Moderate |
| 4 — Community | Stack Overflow, Reddit (r/netsec, r/programming), Hacker News, dev.to/Medium | Verify first |
| 5 — Avoid | SEO farms (GeeksforGeeks, tutorialspoint), AI-generated slop, "Top 10 X in 2026", marketing blogs | Skip |

**Always go Tier 1 → Tier 2 → Tier 3 → Tier 4. Never start from Tier 4.**

## Search Strategy

Start with Google dorks to cut through noise. Details in `search-techniques.md`.

Key patterns:
- `filetype:pdf site:edu "topic"` — academic papers
- `site:github.com "awesome-" "topic"` — curated lists
- `site:attack.mitre.org "technique"` — ATT&CK techniques
- `"topic" after:2025-01-01 filetype:pdf` — recent whitepapers

## Red Flags (Skip These Sources)

- No author name or credentials
- No dates or version numbers
- Code examples with syntax errors or deprecated APIs
- "Updated for 2026!" with 2021 content
- Generic stock photos, excessive ads
- Reads like "compilation of page-one search results" (AI slop)
- Hedging: "In the ever-evolving landscape...", "It's important to note..."
- Answers every question with same product recommendation

## Coverage Checklist (run before declaring done)

- [ ] Every outline item is addressed in Findings (Confirmed / Tentative / Unknown)
- [ ] Verification tier requirements met (see Verification Protocol)
- [ ] Tentative / Disputed / Unknown items are explicit, not silently dropped
- [ ] Date relevance confirmed; volatile sources tagged with `[V]` + access date
- [ ] Source list attached with URLs and tier markings
- [ ] Gaps section is non-empty or explicitly states "no known gaps"
- [ ] Stop Criteria satisfied (or budget exhausted with gaps reported)

## When to Read Which Reference File

- Need to find something specific → `search-techniques.md`
- Need sources for a specific domain → `sources-by-domain.md`
- Need a database or API → `sources-and-apis.md`

## Reference Files

- `search-techniques.md` — Google dorks, Scholar techniques, finding original sources, Wayback Machine
- `sources-by-domain.md` — domain-specific source lists (cybersecurity, web, cloud, AI/ML, crypto)
- `sources-and-apis.md` — all databases, APIs, tools organized by type (docs, academic, security, code, books, patents)
