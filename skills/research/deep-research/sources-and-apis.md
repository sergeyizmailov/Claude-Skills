# Sources, Databases & APIs

## Documentation Aggregators

| Source | URL | Notes |
|--------|-----|-------|
| DevDocs | https://devdocs.io/ | 100+ doc sets, offline support, fuzzy search |
| Context7 MCP | https://github.com/upstash/context7 | 9000+ libraries, real-time docs for AI agents |
| MDN Web Docs | https://developer.mozilla.org/ | Canonical web reference |
| caniuse | https://caniuse.com/ | Browser feature support tables |
| tldr-pages | https://tldr.sh/ | Simplified man pages |

## Standards Bodies

| Body | URL | Covers |
|------|-----|--------|
| IETF / RFC Editor | https://www.rfc-editor.org/ | TCP/IP, HTTP, TLS, DNS, email |
| W3C | https://www.w3.org/ | HTML, CSS, SVG, WAI-ARIA, WASM |
| WHATWG | https://whatwg.org/ | HTML, DOM, Fetch, URL (living standards) |
| TC39 | https://github.com/tc39/proposals | ECMAScript/JavaScript evolution |
| IEEE | https://ieeexplore.ieee.org/ | Networking, electrical, computing standards |

## Academic Paper Databases

| Database | URL | Access | API |
|----------|-----|--------|-----|
| arXiv | https://arxiv.org/ | Free, open | REST + OAI-PMH, 4 req/s |
| Semantic Scholar | https://www.semanticscholar.org/ | Free | REST JSON. Unauthenticated: 1000 req/s shared across ALL anonymous users (practically ~1 RPS per IP). API key: 1 RPS per key, higher availability. Apply for key at api.semanticscholar.org |
| Google Scholar | https://scholar.google.com/ | Free | No official API |
| DBLP | https://dblp.org/ | Free, CC0 | XML dumps |
| ACM DL | https://dl.acm.org/ | Paywalled | Check arXiv for preprints |
| IEEE Xplore | https://ieeexplore.ieee.org/ | Paywalled | Check author sites for preprints |
| OpenAlex | https://openalex.org/ | Free, open | REST, replacement for MS Academic |
| Hugging Face Papers | https://huggingface.co/papers/trending | Free | Trending ML/AI papers |

## Security Databases

| Database | URL | Purpose |
|----------|-----|---------|
| MITRE ATT&CK | https://attack.mitre.org/ | Adversary TTPs knowledge base |
| NIST NVD | https://nvd.nist.gov/ | Vulnerability database with CVSS |
| CVE | https://cve.mitre.org/ | Vulnerability identifiers |
| CWE | https://cwe.mitre.org/ | Weakness classification taxonomy |
| OWASP | https://owasp.org/ | Web/API/Mobile/LLM Top 10, tools |
| ExploitDB | https://www.exploit-db.com/ | Public exploits + PoC code |
| VulDB | https://vuldb.com/ | Vuln intel with risk scoring |

## Code & Repository Search

| Tool | URL | Notes |
|------|-----|-------|
| GitHub Code Search | https://github.com/search | Regex, symbol, language/path filters |
| GitHub Search API | https://docs.github.com/en/rest/search | 30 req/min |
| GitHub Advisory DB | https://github.com/advisories | Security advisories |
| Sourcegraph | https://sourcegraph.com/search | Cross-repo regex + structural search |

## Infrastructure Research

| Tool | URL | Use Case |
|------|-----|----------|
| Shodan | https://www.shodan.io/ | Internet-wide device/service scanning |
| Censys | https://search.censys.io/ | Internet asset discovery |
| FOFA | https://en.fofa.info/ | Chinese internet scanning |
| ZoomEye | https://www.zoomeye.org/ | Cyberspace search engine |

Use Shodan + Censys together for maximum coverage.

## Books & eBooks

**Commercial (default starting point):**
- O'Reilly: https://www.oreilly.com/ — 50K+ books, subscription
- Manning: https://www.manning.com/ — MEAP early access
- No Starch Press: https://nostarch.com/ — security/hacking focused
- Packt: https://www.packtpub.com/ — free book of the day

**Open / public-domain (always safe):**
- Internet Archive: https://archive.org/ — 44M texts, Controlled Digital Lending
- Project Gutenberg: https://www.gutenberg.org/ — 60K+ public domain
- arXiv / OpenReview / institutional preprint servers — author-deposited
- Author home pages — frequently host free preprint PDFs of paywalled papers

### Shadow libraries (legal risk, jurisdiction-dependent, user-approved only)

The following are unauthorized copies of copyrighted material. Access and
download are illegal in many jurisdictions. Use ONLY when the user has
explicitly approved this source for the current task, the work is
authorized research, and you have first attempted:

1. Author home page / preprint server (arXiv, OpenReview, SSRN)
2. Institutional repository / Google Scholar "All N versions"
3. Direct request to author via email
4. Library access (university, public library digital lending)

- Anna's Archive: https://annas-archive.org/ — metasearch (LibGen, Z-Library, Sci-Hub)
- Sci-Hub: https://sci-hub.se/ — ~85M papers (domains change frequently)

Operational note: never cite shadow libraries in a research output — cite
the canonical DOI or arXiv ID. The shadow source is a delivery channel,
not a citable authority.

## Patent Databases

| Database | URL | Coverage |
|----------|-----|----------|
| Google Patents | https://patents.google.com/ | Global, full-text, free |
| USPTO | https://ppubs.uspto.gov/ | US patents |
| Espacenet | https://worldwide.espacenet.com/ | 140M+ publications, EU |

## Web Archive

Wayback Machine: https://web.archive.org/
- CDX API: `https://web.archive.org/cdx/search/cdx?url=example.com&output=json`
- Use for: removed docs, API change history, deleted repos, historical verification
