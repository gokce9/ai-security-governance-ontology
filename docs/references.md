# References

Sources used to build and update ASGO. Primary sources are authoritative; secondary sources were used only to track changes and are cross-checked against each other. Run `queries/cq09-framework-status.rq` to see each framework's status and the date it was last verified.

Last status check: **2026-10-01**

**GokceINFO** denotes materials shared as PDF by the project author, modelled as a single `asgo:SourceDocument` in `ontology/sources.ttl` (reference material, not a framework).

## EU AI Act

### Primary
- Regulation (EU) 2024/1689 (Artificial Intelligence Act) – <https://eur-lex.europa.eu/eli/reg/2024/1689/oj>
- European Parliament Legislative Train – Digital Omnibus on AI – <https://www.europarl.europa.eu/legislative-train/package-digital-package/file-digital-omnibus-on-ai>

### Secondary (Digital Omnibus on AI, Regulation (EU) 2026/1744)
- K&L Gates – EU Digital Omnibus on AI Enters Into Force – <https://www.klgates.com/EU-Digital-Omnibus-on-AI-Enters-Into-Force-7-31-2026>
- Gibson Dunn – EU AI Act Omnibus Agreement: Postponed High-Risk Deadlines and Other Key Changes – <https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/>
- Usercentrics – EU AI Act Deal: Digital Omnibus Now in Force – <https://usercentrics.com/knowledge-hub/eu-ai-act-high-risk-delay-article-50-transparency-consent/>
- Jones Walker – Yes, August 2 Still Matters – <https://www.joneswalker.com/en/insights/blogs/ai-law-blog/yes-august-2-still-matters-the-eu-approved-a-high-risk-ai-delay-but-most-trans.html?id=102nbon>

> TODO: verify the amended Art. 4 wording and the point number of the new Art. 5 prohibition against the Official Journal text of Regulation (EU) 2026/1744.

## NIST

### Primary
- NIST AI 100-1, AI Risk Management Framework 1.0 (Jan 2023) – <https://doi.org/10.6028/NIST.AI.100-1> (source of the 72 subcategory texts)
- NIST AI RMF page (revision status, profiles) – <https://www.nist.gov/itl/ai-risk-management-framework>
- NIST AI 600-1, Generative AI Profile (Jul 2024) – <https://doi.org/10.6028/NIST.AI.600-1>
- NIST AI 100-2 E2025, Adversarial Machine Learning taxonomy (Mar 2025) – <https://csrc.nist.gov/pubs/ai/100/2/e2025/final>
- NIST CSWP 29, Cybersecurity Framework 2.0 (Feb 2024) – <https://doi.org/10.6028/NIST.CSWP.29> (source of the 106 subcategory texts)
- NIST IR 8596 (preliminary draft), Cyber AI Profile (Dec 2025) – <https://csrc.nist.gov/pubs/ir/8596/iprd>
- COSAiS – SP 800-53 Control Overlays for Securing AI Systems – <https://csrc.nist.gov/projects/cosais>

### Secondary
- I.S. Partners – NIST AI RMF 2025–2026 Updates – <https://www.ispartnersllc.com/blog/nist-ai-rmf-2025-2026-updates-what-you-need-to-know-about-the-latest-framework-changes/>
- Crowell & Moring – NIST Releases Draft Framework for AI Cybersecurity – <https://www.crowell.com/en/insights/client-alerts/nist-releases-draft-framework-for-ai-cybersecurity-solicits-public-comment-what-organizations-using-or-deploying-ai-should-know>


## Assessment methodology

- **GokceINFO** – used for `trustworthy-ai-assessment.ttl` (paraphrased), the recruitment risks in `examples/hiring-assistant.ttl`, the evidence catalogue (`evidence.ttl`).
  - Note: some EU AI Act article references in this source follow the 2021 Commission proposal numbering. ASGO uses the final Regulation (EU) 2024/1689 numbering and records the source references in `skos:editorialNote`.
- EU AI Act Art. 42 (final text) – AI Act Service Desk – <https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-42>
- Art. 48 CE marking / Art. 49 registration – <https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-48> · <https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-49>

## OECD

### Primary
- OECD AI Principles – <https://oecd.ai/en/ai-principles>
- Recommendation of the Council on Artificial Intelligence, OECD/LEGAL/0449 – <https://legalinstruments.oecd.org/en/instruments/OECD-LEGAL-0449>

### Secondary
- Digital Policy Alert – The 2024 update to the OECD AI Principles – <https://digitalpolicyalert.org/ai-rules/2024-update-OECD-principles>
- ANSI – OECD Updates AI Principles – <https://www.ansi.org/standards-news/all-news/5-9-24-oecd-updates-ai-principles>

## Threat catalogues

### Primary
- OWASP GenAI LLM Top 10 2026 (4 Aug 2026) – <https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/> · source files: <https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/tree/main/2026/final> (entry IDs and titles verified here)
- OWASP Top 10 for LLM Applications 2025 (superseded) – <https://genai.owasp.org/llm-top-10/>
- OWASP Top 10 for Agentic Applications 2026 (9 Dec 2025) – <https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/>
- MITRE ATLAS – <https://atlas.mitre.org/> · data release v2026.09 (15 Sep 2026): <https://github.com/mitre-atlas/atlas-data/releases/tag/v2026.09> (all technique IDs in `ai-threats.ttl` verified against `ATLAS-2026.09.yaml`)

- MITRE ATLAS mitigations AML.M0000–M0039 – verified against `ATLAS-2026.09.yaml` (same release)
- AWS – Generative AI Security Scoping Matrix – <https://aws.amazon.com/ai/security/generative-ai-scoping-matrix/> · introduction: <https://aws.amazon.com/blogs/security/securing-generative-ai-an-introduction-to-the-generative-ai-security-scoping-matrix/>

### Secondary
- Imperva – OWASP LLM Top 10 2026: What Changed – <https://www.imperva.com/blog/owasp-llm-top-10-2026-what-changed/>
- Help Net Security – OWASP 2026 LLM Top 10 released – <https://www.helpnetsecurity.com/2026/08/06/owasp-2026-llm-top-10-released/>
- Teleport – OWASP Top 10 for Agentic Applications 2026 – <https://goteleport.com/blog/owasp-top-10-agentic-applications/>
- Modulos – OWASP Top 10 for Agentic Applications – <https://docs.modulos.ai/frameworks/owasp-top-10-agentic>

> Note: the ASI01–ASI10 titles come from two consistent secondary sources; the official list is inside the OWASP PDF. One secondary source (cybersecuritynews.com) published an incorrect LLM 2026 ranking and was not used.
