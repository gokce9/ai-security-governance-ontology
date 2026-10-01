# How to read ASGO in five minutes

## 1. The core chain

Almost everything in ASGO hangs off one chain:

```
                     deploymentScope (1-5)
   AI system ─────────────────────────────▶ Deployment scope
     │  │                                          ▲
     │  │ classifiedAs                             │ applicableToScope
     │  ▼                                          │
     │  Risk tier ◀── appliesToTier ── Requirement ◀── implements ── Control
     │                                  │                             │
     │ exposedTo                        │ demonstratedBy              │ mitigates
     ▼                                  ▼                             ▼
    Risk ──── arisesFrom ─────────▶ Threat ◀──────────────────────────┘
     │
     │ measuredBy
     ▼
   Metric
                                     Evidence type (document)
```

Read it as sentences:

- An **AI system** is *classified as* an EU AI Act **risk tier** and has a **deployment scope** (consumer app … self-trained model).
- It is *exposed to* **risks**; a risk *arises from* a **threat** (prompt injection, poisoning …) and is *measured by* **metrics**.
- A **control** *mitigates* threats, *implements* **requirements** of frameworks and *applies to* certain deployment scopes.
- A **requirement** (AI Act article, NIST subcategory, CSF outcome) *applies to* a risk tier and is *demonstrated by* an **evidence type** (risk register, model card, logs …).

## 2. The relations you need

| Relation | From → To | Use it when |
|---|---|---|
| `asgo:exposedTo` | AI system → Risk | recording a risk of a system |
| `asgo:arisesFrom` | Risk → Threat | the risk is caused by a known attack or weakness |
| `asgo:mitigates` | Control → Threat | a control reduces a threat |
| `asgo:mitigatedBy` | Risk → Control | a specific system risk is covered by a control |
| `asgo:implements` | Control → Requirement | doing the control (partly) satisfies a requirement |
| `asgo:demonstratedBy` | Requirement → Evidence type | this document proves the requirement is met |
| `asgo:measuredBy` | Risk / Requirement → Metric | this metric tests it |
| `asgo:applicableToScope` | Control → Deployment scope | the control is expected in that scope |

Between frameworks only three relations are used:

| Relation | Meaning |
|---|---|
| `skos:closeMatch` | substantially the same intent (e.g. AI Act Art. 14 ↔ NIST MAP 3.5) |
| `skos:relatedMatch` | partial or supporting overlap |
| `asgo:addresses` | a requirement addresses a threat or trustworthiness characteristic |

## 3. Where things live

| You want to … | File |
|---|---|
| understand or extend the vocabulary | `ontology/asgo-core.ttl` |
| look up a framework's text | `ontology/modules/` – `eu-ai-act`, `nist-ai-rmf(-subcategories)`, `nist-csf`, `oecd-ai-principles` |
| look up threats (OWASP, ATLAS techniques, NIST AML) | `ontology/modules/ai-threats.ttl` |
| add or change a **control** | `ontology/modules/ai-controls.ttl` (the only place controls are defined and linked) |
| add a **mapping between frameworks** | `ontology/mappings/framework-crosswalk.ttl` (the only mapping file) |
| add an **evidence document** or link one to a requirement | `ontology/modules/evidence.ttl` |
| add audit questions, metrics, assessment steps | `ontology/modules/trustworthy-ai-assessment.ttl` |
| add **your own cases and lessons learned** | `ontology/modules/practitioner-knowledge.ttl` |
| describe your own AI systems | Turtle files in `data/` (pattern: `examples/`) |

## 4. How much to trust a statement

Every framework, mapping or insight carries provenance:

- `asgo:authorityLevel` – **Normative** (law) · **Voluntary** (NIST, OECD) · **Informative** (OWASP, ATLAS, AWS) · **PractitionerInsight** (author interpretation).
- `asgo:verificationStatus` – checked against the primary source, corroborated by a secondary source, or unverified. Run `queries/cq15-verification-backlog.rq`.
- `asgo:publicationStatus` – final, under revision, draft, superseded. Run `queries/cq09-framework-status.rq`.

## 5. Prefixes

`asgo:` core · `euaia:` EU AI Act · `nist:` AI RMF · `csf:` CSF 2.0 · `oecd:` OECD · `threat:` threats, OWASP, ATLAS · `ctl:` controls and deployment scopes · `ev:` evidence · `tai:` assessment · `pk:` practitioner knowledge · `src:` sources
