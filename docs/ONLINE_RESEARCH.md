# Online Research — LogicaSophia 0.8.1

**Built by I2PS Engineering.**

## Internet access is a first-class capability

LogicaSophia is an internet-capable engineering assistant. The native analysis engine is able to work locally, **but the application is not restricted to offline use**. A task explicitly requesting online research can transmit its query over HTTPS, retrieve actual public sources and produce an audited report.

**Current supported providers:** Wikipedia MediaWiki Action API (article search), Crossref REST API (scholarly DOI metadata), and optionally Brave Search (broad-web indexed results with `LOGICASOPHIA_BRAVE_API_KEY`). Without a Brave key, `auto` searches Wikipedia and Crossref. Internet services may have availability, quotas or usage restrictions; a failed service is shown rather than hidden.

## Usage

```bash
bash LogicaSophia_Start_AI.txt research --query 'processor cache-coherence protocols' --provider auto --confirm-network
bash LogicaSophia_Start_AI.txt work --goal 'Search web for thermal management standards'
bash LogicaSophia_Start_AI.txt work --goal 'Search web for thermal management standards' --confirm
```

In Qt Studio choose **Search online** from Assistant, or **Online research** under Create. Both prompt for consent before the network request.

The `research` CLI requires `--confirm-network`. In a general `work` request, `--confirm` authorizes the reviewed task, including transmission of research terms. No network request occurs during a planning preview or by launching the application.

### Outputs

- `sources.json`: title, provider, full source URL, excerpt, UTC retrieval time and provider warnings.
- `research.md`: structured source bibliography and snippets.
- `document.pdf`: genuine generated PDF, based only on retrieved metadata.
- `workbench.json`: execution and evidence hashes.

All results are outside the authorized input workspace. The application does **not** invent successful research when the Internet is unavailable or no provider responds.

### What is not yet claimed

This initial retrieval feature is **not general autonomous web browsing or verified live-news understanding**. It does not fetch arbitrary websites, submit forms, log into users' accounts, or generate independent AI-verified scientific answers. Provider excerpts are external data, and source integrity does not prove source accuracy.

## Verification

Version 0.8.1 passed 104 local tests, including 13 tests for provider formats, API-key handling, explicit confirmation, partial failures, report and actual PDF output. Providers were mocked in these local tests, so first-machine live query verification on Ubuntu is still required.

### Data and credential boundaries

A search query leaves the machine and is sent to the chosen provider. Do not include secrets in research queries. If you use optional Brave Search, set its credential in your process environment as `LOGICASOPHIA_BRAVE_API_KEY`; do not paste it into a public README or commit it to GitHub. Tokens are placed in request headers, never report files or URLs. Reported results include provider attribution and direct links.

Third-party API documentation: https://www.mediawiki.org/wiki/API:Search · https://www.crossref.org/documentation/retrieve-metadata/rest-api/ · https://api-dashboard.search.brave.com/api-reference/web/search/get
