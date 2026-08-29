---
name: deep-research
description: Use when asked to research deeply, compare options or vendors, fact-check a claim, investigate an unfamiliar topic, prepare a report or briefing, build a knowledge base or reference doc, or trace a claim to its primary source.
---

# Deep Research

Primary sources over blog rewrites. Output is auditable: every claim traceable, every gap named.

## Workflow

Scope (question, audience, depth, budget) → outline (items, fields, success criteria) → gather tiers 1→4, never start at 4 → verify per protocol → date-check staleness and version → apply stop criteria → compile output format.

## Source Tiers

| Tier | Sources |
|---|---|
| 1 Primary | Specs (RFC, W3C, WHATWG), source code, official docs, original papers, changelogs |
| 2 Secondary | Peer-reviewed papers, vendor threat intel (Unit42, Mandiant, Sekoia), audits, MITRE ATT&CK |
| 3 Tertiary | Technical books, curated guides (awesome-*, OWASP Cheat Sheets), conference talks |
| 4 Community | Stack Overflow, Reddit, HN, dev.to/Medium — leads only, never ground truth |
| 5 Avoid | SEO farms (GeeksforGeeks), AI slop, "Top 10 X in 2026", marketing blogs |

Skip a source: no author, no dates/versions, "Updated for 2026!" over 2021 content, every question resolves to the same product.

## Verification

| Claim type | Required evidence |
|---|---|
| One canonical authority (RFC, spec, vendor's own docs, project source) | 1 primary source |
| High-impact: security, cost, breaking change, "recommended approach", perf numbers | 2+ independent, ≥1 Tier 1–2; if only 1 → Tentative |
| Sources conflict | Present both, name the conflict, never silently pick |
| Routine metadata (release date, version, port) | 1 primary; recheck if it drives a decision |
| Community "best practice" | Trace to origin; single blog post → opinion, not fact |

Trace blog claims to the paper/RFC/commit behind them; match the version under discussion; run load-bearing snippets.

## Volatile by Default

Leaderboards (LMArena, HF Open LLM, MTEB), pricing/rate limits, annual surveys, aggregator front pages, live dashboards/threat feeds (URLhaus, abuse.ch), GitHub trending, LLM model names/context windows/cutoffs. Cite with access date; cross-check high-impact claims against a non-volatile source; prefer permanent IDs (DOI, arXiv, RFC number, git SHA) over URLs.

## Output Format

Structure is the contract; length is not — short factual queries collapse to a ledger plus a summary.

```
# <Topic>
## 1. Executive Summary — the answer, tradeoffs, uncertainties (3–6 bullets)
## 2. Scope — questions answered · out of scope · assumptions · research date
## 3. Findings — prose grouped Confirmed / High confidence / Tentative / Disputed / Unknown; no URLs here
## 4. Claim Ledger — | # | Claim | Source(s) | Date | Tier | Confidence | Notes |
## 5. Sources — numbered, full URLs, access date, tier, [V] for volatile
## 6. Gaps — not found · contradictory · needs follow-up
## 7. Stale-Risk Notes — findings likely to expire, with half-life
```

## Stop When

All hold: every outline item has a Tier 1–2 source or sits in Gaps · last 1–2 loops yielded no new substantive claims · high-impact claims verified · Tentative/Disputed/Unknown explicit, not dropped · budget spent. "Could not find X" is a valid result; never fabricate to close a gap.

## Parallel Pattern (10+ independent items, subagents)

One self-contained prompt per agent (item + fields + output schema), 3–5 concurrent, results to disk, skip completed on retry; review each batch; mark uncertain findings `[uncertain]` for a second pass. Below 10, sequential. Google dorks first — `search-techniques.md`.

## References

- `search-techniques.md` — dorks, Scholar, finding originals, Wayback.
- `sources-by-domain.md` — per-domain source lists (security, web, cloud, AI/ML, crypto).
- `sources-and-apis.md` — databases, APIs, tools by type.
