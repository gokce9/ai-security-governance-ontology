# Changelog

All notable changes to ASGO are listed here. Versions follow [semantic versioning](https://semver.org/).

## [0.4.0] – 2026-10-02

First public release.

### What's included

- **Frameworks:** EU AI Act (Regulation (EU) 2024/1689 as amended by the Digital Omnibus, Regulation (EU) 2026/1744 – Annex III high-risk obligations from 2 December 2027, Annex I from 2 August 2028); NIST AI RMF 1.0 with all 72 subcategories and the GenAI Profile risks; NIST CSF 2.0 with all 106 subcategories; OECD AI Principles (2024 revision).
- **Threats:** NIST AI 100-2 E2025 adversarial ML taxonomy; OWASP Top 10 for LLM Applications 2026 (with a mapping from the 2025 edition); OWASP Top 10 for Agentic Applications (ASI01–ASI10); MITRE ATLAS v2026.09 technique IDs.
- **Controls:** 56 AI security controls in 10 domains, tagged by AWS Generative AI Security Scoping Matrix scope (1–5) and mapped to all 40 MITRE ATLAS mitigations and to EU AI Act, NIST AI RMF and CSF requirements.
- **Evidence:** 38 evidence types (policies, registers, logs, records) linked to the requirements they demonstrate.
- **Mappings:** 107 framework-to-framework mappings, each with a written rationale, reviewed by the author (100 approved as proposed, 7 raised from related match to close match).
- **Assessment:** trustworthiness assessment cycle, audit questions, fairness and robustness metrics, and a 10-step EU AI Act conformity-assessment roadmap.
- **Practitioner cases:** four anonymised, composite cases from practice (internal RAG assistant, customer-facing chatbot with actions, AI coding assistants and IDE agents, AI in low-code workflows), each with risks, applied controls, outcome and lesson learned.
- **Examples:** two fictional AI systems (hiring pre-screening assistant, customer support chatbot).
- **Quality:** OWL 2 DL, consistent under HermiT, SHACL-validated, 16 SPARQL competency queries, CI on every push.

### Downloads

- `asgo-v0.4.0.owl` – the whole ontology merged into one file (RDF/XML), opens directly in Protégé.
- `asgo-v0.4.0.ttl` – the same in Turtle.
- Source code (zip / tar.gz) – the full repository at this version.

### Licence

CC BY-NC 4.0 – free for non-commercial use with attribution; commercial use by separate licence from the author.

### Known limitations

- Framework mappings are the author's interpretation, not official crosswalks.
- The `w3id.org/asgo` IRIs do not resolve yet.
- Four practitioner cases so far; more are planned.
