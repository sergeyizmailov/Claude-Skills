# Search Techniques

## Google Dork Operators

```
# Papers and whitepapers
filetype:pdf "buffer overflow" site:edu
filetype:pdf "threat intelligence" site:gov
filetype:pdf site:arxiv.org "topic"

# Vendor whitepapers
site:crowdstrike.com filetype:pdf
site:mandiant.com filetype:pdf "threat"
site:unit42.paloaltonetworks.com "threat research"

# Conference talks and presentations
filetype:pdf site:blackhat.com
filetype:pdf site:defcon.org
filetype:pdf site:usenix.org inurl:sec

# GitHub via Google (note: Google strips GitHub-specific qualifiers
# like `language:` and `stars:` — those work only on GitHub Code Search,
# see the dedicated section below)
site:github.com "awesome-" inurl:readme "topic"
inurl:gist.github.com "topic"
site:github.com "topic" inurl:readme

# Code examples and configs on GitHub (Google-side, full-file content match)
"nginx.conf" "proxy_pass" site:github.com
"docker-compose.yml" "traefik" site:github.com

# Community discussions
site:reddit.com/r/netsec "CVE-2024"
site:news.ycombinator.com "topic"

# Date-restricted
"LLM jailbreak" after:2025-01-01
"supply chain attack" after:2024-06-01 filetype:pdf

# Excluding noise
"smart contract audit" -"hire us" -"contact us" -"get a quote"
"kubernetes security" -pinterest -facebook filetype:pdf

# Documentation and specs
site:datatracker.ietf.org "TLS 1.3"
site:developer.mozilla.org "fetch API"
site:tc39.es "proposal"
```

## Google Scholar Techniques

```
# Exact title search
allintitle: "attention is all you need"

# Author-specific
author:"Goodfellow" "adversarial"

# Date-restricted
"fuzzing" after:2023 -patent

# Survey/review papers (high-level overviews)
"survey" OR "systematic review" "smart contract vulnerabilities"

# Site restriction
site:arxiv.org "diffusion model" "text-to-image"
```

Tips:
- **"Cited by N"** links → find seminal papers, trace research evolution
- **"Related articles"** → adjacent work
- **"All N versions"** → find free copies (preprints, author manuscripts)
- Sort by date for latest, by relevance for foundational

## Finding the Original Source (SIFT Method)

1. **Stop** — pause before trusting
2. **Investigate the source** — who published? What expertise?
3. **Find better coverage** — look for multiple independent sources
4. **Trace claims upstream** — follow citations/links to primary source

Practical steps:
- Scroll to references/bibliography at bottom
- Follow "Source:" or "Via:" links
- For GitHub repos, check README for "inspired by" or "based on"
- For blog claims, find the original paper/RFC/commit
- Use Google Scholar "Cited by" to find first publication of a concept
- Check Wayback Machine if original links are dead

## Using awesome-* Repos as Curated Indexes

1. Search GitHub for `awesome-{topic}`
2. Check: stars, last commit, contribution activity
3. Use as starting point, evaluate each resource independently
4. If a tool appears in multiple awesome lists → real adoption
5. Check Contributing guidelines → well-maintained lists have strict criteria

Key meta-lists:
- https://github.com/sindresorhus/awesome
- https://github.com/topics/awesome-list
- https://github.com/best-of-lists/best-of

Security-specific:
- awesome-hacking, awesome-pentest, awesome-security
- awesome-osint, awesome-threat-intelligence
- awesome-malware-analysis, awesome-reversing
- awesome-web-security, awesome-appsec

## Wayback Machine

```
# Direct URL lookup
https://web.archive.org/web/2024*/https://example.com/docs/api

# Wildcard search
https://web.archive.org/web/20220101*/example.com

# CDX API (programmatic)
https://web.archive.org/cdx/search/cdx?url=example.com&output=json&from=20200101&to=20250101
```

Use for: recovering removed docs, seeing API changes between versions, finding deleted repos, verifying historical claims.

## GitHub Code Search (NOT Google)

Run these inside https://github.com/search — the qualifiers below are
GitHub-only and are ignored by Google even with `site:github.com`.

```
language:python "import torch" path:train symbol:forward
language:go "net/http" repo:kubernetes/kubernetes
language:javascript "evilginx" NOT test
stars:>1000 language:rust topic:cryptography
org:openssl path:apps content:"BIO_new"
```

Common qualifiers:
- `language:` — file language (one per qualifier)
- `repo:owner/name` — specific repo
- `org:` / `user:` — owner scope
- `path:` — directory or file path
- `symbol:` — defined symbol (function, class, etc.)
- `content:` — substring within file
- `stars:>N` — repo star threshold (works on repo search, not code search)
- `topic:` — repo topic tag

Repo-level discovery uses GitHub Repo Search (different endpoint):
```
topic:malware-analysis stars:>500 pushed:>2025-01-01
in:name "evilginx" language:go
```

Also: Sourcegraph (https://sourcegraph.com/search) for cross-repo regex and
structural search; grep.app (https://grep.app) for fast plain-text code search.
