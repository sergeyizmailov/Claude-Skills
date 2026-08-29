# 05 — Automation channels (which pipe, when)

Agent-first ranking. The agent's write path is ALWAYS the API; every other channel
exists for the human layer or as a fallback. Composing rule: `validate_only` →
PAUSED → human enable, regardless of channel (meta-ads/13 §10, google-ads/10).

| Channel | Agent use | Human use | Documented in |
|---|---|---|---|
| **Meta Marketing API** | Primary write path. System User token, PAUSED-first launch sequence, failure map | Reviews IDs before enable; owns token/asset assignment | meta-ads/13, meta-grey-ops/04 (mass launch) |
| **Google Ads API** | Primary write path. GAQL reads, atomic Mutate graphs, BatchJobService for mass launch | Owns developer token (MCC-level), RMF/Standard access | google-ads/10 |
| **Meta Ads MCP** | Analysis and bounded writes — start read-only, enable write categories per task, budget ceiling on | Toggles the controls (Business Suite → Integrations → Ads MCP Server); controls are rollout-dependent [unverified] | meta-ads/13 §7 |
| **Google Ads MCP** | Reporting only — strictly read-only at release; write-capable claims are unverified | — | google-ads/10 |
| **Automated rules (Meta API)** | Arm the kill/alert ladder (count-form rungs, cents units, dry-run via adrules_history) | Sets confidence levels and verdicts | senior-buyer-ops/04 |
| **Google Ads Scripts** | In-account reporting/logging (QS history, pacing alerts); 30-min runtime cap | In-account guardrails where no API infra exists | google-ads/10 |
| **CSV / bulk files** | Fallback only — human-mediated, no atomicity, no validate_only. Google: Editor CSV for one-off migrations/pre-API. Meta: Ads Manager import lands as paused drafts, and is **blocked on fresh accounts** (error 3738001 → build via API/UI) | The right tool when a human must review thousands of rows first | google-ads/10, meta-ads/02 §10, meta-ads/14 |
| **Google Sheets** | Feeds only (near-real-time small catalogs) + script outputs | Dashboards/leaderboards the TL actually reads | google-feed-ops/01, google-ads/10 |
| **n8n / Zapier / Make** | Orchestration glue (lead → OCI upload, alerts). No no-code connector matches direct API for atomic multi-entity creation; n8n self-hosted = no per-execution ceiling | Alert routing to chat | google-ads/10 |
| **BigQuery Data Transfer** | Reporting warehouse; fixed schemas, 7-day refresh | BI layer | google-ads/10 |

Decision rules:

1. **Agent writes → API, full stop.** MCP only where its governance matches the task
   (read-heavy analysis, bounded writes); never route a launch through CSV/UI
   import — no validate_only equivalent, and Meta blocks fresh accounts.
2. **One spec format, two adapters:** campaign spec as validated JSON →
   deterministic code emits MutateOperation (Google) or API objects (Meta). The
   LLM never emits API calls directly (google-ads/10 AI pipelines).
3. **Human layer sees**: draft IDs before enable, the daily spend→cost sync sheet
   (tracker-ops/03), and the rule history — nothing else needs a human channel.
4. **Reads are cheap everywhere**: GAQL SearchStream (Google) and Insights edge
   (Meta) feed the same daily routine; exports → `meta-ads/scripts/analyze_ads_export.py`
   (meta-ads/12) only when a human asks for a file.
