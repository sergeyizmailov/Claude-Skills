# Sources by Domain

## Cybersecurity

**Techniques and tools:**
- MITRE ATT&CK Navigator: https://mitre-attack.github.io/attack-navigator/
- GitHub topics: `topic:red-team`, `topic:pentest`, `topic:exploit`
- PortSwigger Research: https://portswigger.net/research
- Project Zero: https://googleprojectzero.blogspot.com/
- DEF CON media: https://media.defcon.org/
- Black Hat archives: https://www.blackhat.com/html/archives.html

**CVEs and exploits:**
- NVD API: https://services.nvd.nist.gov/rest/json/cves/2.0
- ExploitDB / searchsploit (ships with Kali)
- Packet Storm: https://packetstormsecurity.com/
- GitHub Advisory DB: https://github.com/advisories
- OSV: https://osv.dev/

**Malware analysis and threat intel:**
- ANY.RUN: https://any.run/ — interactive sandbox
- VirusTotal: https://www.virustotal.com/ — multi-engine scanner
- MalwareBazaar: https://bazaar.abuse.ch/ — malware samples
- URLhaus: https://urlhaus.abuse.ch/ — malicious URLs
- abuse.ch: https://abuse.ch/ — threat intel feeds

**Vendor research (Tier 2 quality):**
- Unit 42 (Palo Alto): https://unit42.paloaltonetworks.com/
- Mandiant (Google): https://www.mandiant.com/
- Talos (Cisco): https://talosintelligence.com/
- CrowdStrike: https://www.crowdstrike.com/blog/
- Securelist (Kaspersky): https://securelist.com/
- Microsoft Threat Intel: https://www.microsoft.com/en-us/security/blog/topic/threat-intelligence/
- Sekoia: https://www.sekoia.io/
- The DFIR Report: https://thedfirreport.com/ — real intrusion case studies
- Krebs on Security: https://krebsonsecurity.com/

## Web Development

**Core references:**
- MDN Web Docs: https://developer.mozilla.org/ — HTML, CSS, JS, Web APIs
- caniuse: https://caniuse.com/ — browser support tables
- TC39 proposals: https://github.com/tc39/proposals — upcoming JS features
- WHATWG: https://spec.whatwg.org/ — HTML, DOM, Fetch living standards
- web.dev (Google): https://web.dev/ — performance, PWAs, Core Web Vitals

**Framework docs:**
- Use Context7 MCP for real-time docs (React, Next.js, Vue, Svelte, etc.)
- Check framework GitHub repos discussions/issues for edge cases

## Cloud / DevOps

**Vendor docs (always start here):**
- AWS: https://docs.aws.amazon.com/
- GCP: https://cloud.google.com/docs
- Azure: https://learn.microsoft.com/en-us/azure/

**Cloud-native ecosystem:**
- CNCF Landscape: https://landscape.cncf.io/
- Artifact Hub: https://artifacthub.io/ — Helm charts, OPA policies, Falco rules
- Terraform Registry: https://registry.terraform.io/
- Kubernetes docs: https://kubernetes.io/docs/
- KEPs: https://github.com/kubernetes/enhancements

## AI / ML

**Models and datasets:**
- Hugging Face Hub: https://huggingface.co/ — 2M+ models, 500K+ datasets
- Hugging Face Papers: https://huggingface.co/papers/trending

**Research:**
- arXiv: cs.AI, cs.CL, cs.CV, cs.LG categories
- Semantic Scholar: https://www.semanticscholar.org/
- Connected Papers: https://www.connectedpapers.com/ — visual citation graph
- Lilian Weng's blog: https://lilianweng.github.io/ — excellent ML summaries

**Benchmarks — [VOLATILE]:**

AI leaderboards re-rank frequently, get deprecated, and move domains.
Always note access date and cross-check with a non-leaderboard source
(model card, paper, vendor blog) for decision-driving claims. If a URL
404s, search for the current canonical home.

- LMArena (formerly LMSYS Chatbot Arena): https://lmarena.ai/
  Old `chat.lmsys.org` redirects but may break; treat the legacy URL as stale.
- Open LLM Leaderboard v2: https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard
  v1 was retired in 2024; v2 has its own scoring methodology — do not
  compare scores across versions.
- MTEB (embedding benchmarks): https://huggingface.co/spaces/mteb/leaderboard
- HELM (Stanford): https://crfm.stanford.edu/helm/
- LiveBench: https://livebench.ai/ — contamination-resistant, refreshed periodically
- Artificial Analysis: https://artificialanalysis.ai/ — vendor-side benchmarks + pricing

For per-task benchmarks, prefer the paper's reported numbers over leaderboard
aggregates; leaderboard runs may use different prompts, decoding settings,
or quantization than the original model.

## Crypto / Blockchain

**Standards:**
- EIPs: https://eips.ethereum.org/
- Solidity docs: https://docs.soliditylang.org/
- Ethereum.org: https://ethereum.org/developers/docs/

**Security and auditing:**
- OpenZeppelin: https://www.openzeppelin.com/security-audits
- Trail of Bits: https://blog.trailofbits.com/
- SWC Registry: https://swcregistry.io/
- Rekt News: https://rekt.news/ — hack post-mortems
- Code4rena: https://code4rena.com/ — audit contests
- Sherlock: https://www.sherlock.xyz/
- Immunefi: https://immunefi.com/ — bug bounties

**Audit tools:**
- Slither: https://github.com/crytic/slither
- Mythril: https://github.com/Consensys/mythril
- Echidna: https://github.com/crytic/echidna
- Foundry: https://github.com/foundry-rs/foundry
