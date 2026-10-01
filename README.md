# AI Security Governance Ontology (ASGO)

A modular OWL/RDF ontology that connects **AI systems**, **AI security threats**, **controls**, and **governance requirements** from the **NIST AI Risk Management Framework**, **NIST CSF 2.0**, the **OECD AI Principles** and the **EU AI Act**, extended with curated practitioner knowledge.

It is designed to answer questions such as:

- Which EU AI Act obligations apply to this AI system, for which role, and from when?
- Which NIST AI RMF subcategories can be reused to comply with Article 15?
- Which EU AI Act, NIST AI RMF and CSF requirements does a single control cover?
- Which controls mitigate indirect prompt injection, and which requirements do they help satisfy?
- Which risks in my AI inventory have no mitigating control?
- How do I audit this system: which questions to ask, which fairness and robustness metrics to compute, which conformity-assessment steps to follow?
- Which documents must exist for an auditor or regulator for this AI system, and which single document covers the most frameworks?

## Scope

New here? Read [docs/how-to-read.md](docs/how-to-read.md) first – the core model fits on one page.

| Module | File | Coverage |
|---|---|---|
| Core | `ontology/asgo-core.ttl` | AI system, component, actor/role, risk, threat, vulnerability, harm, control, requirement, evidence, lifecycle stage |
| NIST AI RMF | `ontology/modules/nist-ai-rmf.ttl` | AI 100-1: 4 functions, 19 categories, 7 trustworthiness characteristics; AI 600-1: 12 GenAI risks |
| NIST AI RMF subcategories | `ontology/modules/nist-ai-rmf-subcategories.ttl` | All 72 subcategories with official text (extracted from NIST AI 100-1) |
| NIST CSF 2.0 | `ontology/modules/nist-csf.ttl` | CSF Core: 6 functions, 22 categories, 106 subcategories with official text (extracted from NIST CSWP 29) |
| OECD AI Principles | `ontology/modules/oecd-ai-principles.ttl` | OECD/LEGAL/0449 (2019, revised 2024): 5 values-based principles and 5 policy recommendations, mapped to NIST trustworthiness characteristics and EU AI Act articles |
| EU AI Act | `ontology/modules/eu-ai-act.ttl` | Regulation (EU) 2024/1689 as amended by Regulation (EU) 2026/1744 (Digital Omnibus): operator roles, risk tiers, Art. 5 prohibited practices, Annex III areas, key obligations (Art. 4, 9–17, 25–27, 43, 49, 50, 53, 55, 72, 73), Art. 99 penalties |
| AI threats | `ontology/modules/ai-threats.ttl` | NIST AI 100-2 E2025 adversarial ML taxonomy; OWASP LLM Top 10 2026 (and superseded 2025 edition with version mapping); OWASP Top 10 for Agentic Applications 2026; MITRE ATLAS v2026.09 technique IDs |
| Framework crosswalk | `ontology/mappings/framework-crosswalk.ttl` | All framework-to-framework mappings in one file: EU AI Act ↔ NIST AI RMF (category and subcategory), CSF 2.0 ↔ AI RMF, OECD ↔ NIST / EU AI Act, AI Act articles → threats |
| Evidence catalogue | `ontology/modules/evidence.ttl` | 38 evidence types (policies, procedures, registers, logs) in a four-level document hierarchy, each linked to the EU AI Act, NIST AI RMF and CSF requirements it helps demonstrate |
| Trustworthy AI assessment | `ontology/modules/trustworthy-ai-assessment.ttl` | The auditor's perspective (source: GokceINFO): 5-step trustworthiness cycle, 12 consequence-scanning questions, performance and fairness metrics with formulas, 10-step EU AI Act conformity assessment roadmap (Annex VI), governance operating models and AI-specific risk sources — all mapped to EU AI Act, NIST and OECD |
| AI security controls | `ontology/modules/ai-controls.ttl` | The single control catalogue: 56 controls in 10 domains, each tagged with the deployment scopes it applies to (AWS Generative AI Security Scoping Matrix, Scope 1 consumer app … Scope 5 self-trained model), mapped to all 40 MITRE ATLAS v2026.09 mitigations and to EU AI Act, NIST AI RMF and CSF requirements |
| Practitioner knowledge | `ontology/modules/practitioner-knowledge.ttl` | Anonymised, composite cases from the author's practice (source: GokceINFO): internal RAG assistant, customer-facing chatbot with actions, AI coding assistant and IDE agents, AI in low-code workflows – each with the system, typical risks, recommended controls, target outcome and lesson learned |

`ontology/asgo.ttl` imports every module.

## Design principles

- **Modular.** Each framework lives in its own namespace and file, so it can be updated independently when the source text changes.
- **Provenance is first-class.** Every statement can carry an `asgo:authorityLevel`: `Normative` (law), `Voluntary` (e.g. NIST), `Informative` (e.g. OWASP, ATLAS), or `PractitionerInsight` (author knowledge). Normative text and personal interpretation never blur together.
- **Verification is tracked.** Elements carry `asgo:verificationStatus` (verified against primary source, corroborated by secondary source, unverified), so provisional content is never mistaken for checked content.
- **Citable.** Framework elements carry `asgo:identifier` (e.g. `Art. 15(5)`, `MANAGE 4`) and `asgo:sourceReference`.
- **Validated.** SHACL shapes in `shapes/` enforce quality rules, and the validator flags any reference to an undefined ID (e.g. a mistyped `csf:PR.DS-03`). A GitHub Actions workflow (`.github/workflows/validate.yml`) runs both, plus an OWL 2 DL profile check and a HermiT consistency check.

## Namespaces

| Prefix | IRI |
|---|---|
| `asgo:` | `https://w3id.org/asgo/core#` |
| `nist:` | `https://w3id.org/asgo/nist-ai-rmf#` |
| `euaia:` | `https://w3id.org/asgo/eu-ai-act#` |
| `csf:` | `https://w3id.org/asgo/nist-csf#` |
| `ev:` | `https://w3id.org/asgo/evidence#` |
| `oecd:` | `https://w3id.org/asgo/oecd-ai#` |
| `tai:` | `https://w3id.org/asgo/assessment#` |
| `ctl:` | `https://w3id.org/asgo/controls#` |
| `threat:` | `https://w3id.org/asgo/threats#` |
| `pk:` | `https://w3id.org/asgo/practitioner#` |

> The `w3id.org/asgo` IRIs are reserved for a future persistent-identifier registration and do not resolve yet.

## Using the ontology

**No installation needed:** open `ontology/asgo.ttl` in [Protégé](https://protege.stanford.edu/). The bundled catalog loads every module from local files; the ontology is OWL 2 DL and consistent under HermiT (see [docs/protege.md](docs/protege.md)). You can also load the Turtle files into any triple store or graph database and run the SPARQL queries in `queries/`.

**Command-line tools (optional, Python 3.9+):**

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

.venv/bin/python scripts/asgo.py validate        # Turtle syntax, SHACL, undefined references
.venv/bin/python scripts/asgo.py query-all       # run all competency questions
.venv/bin/python scripts/asgo.py query queries/cq01-obligations-for-system.rq
.venv/bin/python scripts/asgo.py export build/asgo.owl --format xml   # single-file OWL/XML (also json-ld, nt)
.venv/bin/python scripts/asgo.py maturity        # rule-based maturity scorecard
```

To describe your own AI systems, add Turtle files to `data/` following the pattern in `examples/`.

## Repository layout

```
ontology/
  asgo.ttl                      entry point (imports all modules)
  asgo-core.ttl                 upper ontology
  modules/                      framework and knowledge modules
  mappings/framework-crosswalk.ttl  all framework-to-framework mappings
shapes/asgo-shapes.ttl          SHACL validation rules
examples/                       two fictional AI systems (hiring assistant, support chatbot)
queries/                        SPARQL competency questions
scripts/asgo.py                 validate / query / export / maturity / catalog CLI
scripts/mapping_review.py       expert review of framework mappings (Excel round-trip)
data/                           your own AI systems in Turtle (git-ignored)
docs/                           modelling guide, competency questions, references
```

## Examples and practitioner cases

Two fictional AI systems in `examples/` show how to describe your own systems:

- **Hiring pre-screening assistant** (`hiring-assistant.ttl`) – an LLM-based CV screening assistant with a retrieval index and an applicant-tracking write tool. Annex III(4) makes it **high risk**; deployment scope 3 (pre-trained model). Running `query-all` lists its EU AI Act obligations, maps them to NIST, and flags **three bias risks as unmitigated** (discriminatory ranking, reproduced recruiter bias, exclusion of qualified candidates).
- **Customer support chatbot** (`support-chatbot.ttl`) – answers from a help-centre RAG index and opens tickets. **Transparency risk** (Art. 50); deployment scope 3. Covers RAG poisoning, hidden-context extraction and ticket abuse with controls, and flags **confident but wrong answers** as unmitigated.

Four anonymised, composite cases from the author's practice live in `ontology/modules/practitioner-knowledge.ttl`. Each describes a recurring deployment pattern rather than any single organisation – the system, typical risks, recommended controls, target outcome and lesson learned:

| Case | System |
|---|---|
| 1 | Internal knowledge-base RAG assistant |
| 2 | Customer-facing support chatbot with actions (refunds, cancellations) |
| 3 | AI coding assistant and local IDE agents |
| 5 | AI nodes in low-code workflow automation |

Run `queries/cq19-practitioner-cases.rq` to see them end to end.

## Sources and update tracking

All sources are listed in [docs/references.md](docs/references.md). Each framework carries `asgo:publicationStatus` (final, under revision, draft, concept note) and `asgo:statusCheckedOn`; run `queries/cq09-framework-status.rq` to see which ones need re-checking. Drafts currently tracked: NIST Cyber AI Profile (IR 8596), COSAiS (SP 800-53 AI overlays), and the AI RMF Critical Infrastructure Profile.

## Mapping review

All 107 framework-to-framework mappings carry a written rationale (`asgo:mappingRationale`) and were reviewed by Gokcenur Yazici on 1 October 2026: 100 approved as proposed, 7 raised from related match to close match. The review is recorded on the crosswalk (`asgo:reviewedBy`, `asgo:reviewedOn`, `asgo:reviewScope`). Mappings remain the author's interpretation; see the disclaimer.

## Disclaimer

This ontology is a knowledge-engineering resource, not legal advice. The crosswalk and practitioner modules reflect the author's interpretation. Application dates follow the EU AI Act as amended by the Digital Omnibus on AI (Regulation (EU) 2026/1744, in force 27 July 2026): Annex III high-risk obligations apply from 2 December 2027 and Annex I from 2 August 2028. Original dates are preserved in `skos:historyNote`. Check for later amendments before relying on them.

## Licence

[CC BY-NC 4.0](LICENSE) – free to use, share and adapt for **non-commercial** purposes with attribution. For commercial use (e.g. inside a paid product or consulting service), please contact the author for a separate licence.

Source frameworks remain the property of their respective publishers: NIST (AI RMF, CSF 2.0, AI 100-2), the European Union (AI Act), the OECD (AI Principles), the OWASP Foundation (Top 10 for LLM and Agentic Applications, CC BY-SA 4.0 – ASGO uses only their identifiers and titles, with its own definitions), MITRE (ATLAS, Apache 2.0) and Amazon Web Services (Generative AI Security Scoping Matrix).

## Author

**Gokcenur Yazici** – design, sources, practitioner cases and mapping review.

## How to cite

GitHub shows a **“Cite this repository”** button (from `CITATION.cff`). Release notes are in [CHANGELOG.md](CHANGELOG.md).

> Yazici, G. (2026). *AI Security Governance Ontology (ASGO)*, version 0.4. CC BY-NC 4.0. https://github.com/gokce9/ai-security-governance-ontology

---

<p align="center">Made with 💜 by Gökçe — stay curious, stay secure. 🔐</p>
