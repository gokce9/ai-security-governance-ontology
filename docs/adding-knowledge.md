# Adding knowledge to ASGO

This guide shows the patterns for extending the ontology. Run `python scripts/asgo.py validate` after every change. It runs SHACL and also reports any reference to an undefined ID.

## Where does it go?

| You want to add… | File |
|---|---|
| A control (new or changed), incl. the requirements it implements, threats it mitigates, scopes and ATLAS mitigations | `ontology/modules/ai-controls.ttl` – the only place controls live |
| A mapping between frameworks (closeMatch / relatedMatch / addresses) | `ontology/mappings/framework-crosswalk.ttl` – the only mapping file |
| An evidence document or requirement → evidence link | `ontology/modules/evidence.ttl` |
| A threat or attack technique | `ontology/modules/ai-threats.ttl` |
| Framework text (NIST, CSF, EU AI Act, OECD) | the framework's file in `ontology/modules/` |
| **Your own case, lesson learned or interpretation** | `ontology/modules/practitioner-knowledge.ttl` |
| A new framework (NIST SP 800-53, GDPR, NIS2, CRA…) | new file in `ontology/modules/`, add it to `ontology/asgo.ttl`, run `python scripts/asgo.py catalog` |

See [how-to-read.md](how-to-read.md) for the core model and the meaning of each relation.

## Pattern 1 – guidance on an existing framework element

All 72 AI RMF subcategories and 106 CSF subcategories already exist. Do not edit their official text; attach your guidance in the practitioner module:

```turtle
pk:Guide-MS-2.7 a skos:Concept ;
    rdfs:label "How we evaluate AI security and resilience (MEASURE 2.7)"@en ;
    skos:note "Quarterly LLM red-team covering OWASP LLM01/LLM06; results feed MANAGE 1.3."@en ;
    dcterms:subject nist:MS-2.7 ;
    asgo:authorityLevel asgo:PractitionerInsight ;
    dcterms:creator "Gokcenur Yazici" ;
    dcterms:created "2026-10-01"^^xsd:date .
```

For copyrighted standards (e.g. ISO/IEC), write guidance **in your own words**. Never copy text from the standard.

## Pattern 2 – an EU AI Act paragraph

```turtle
euaia:Art26-6 a euaia:Article ;
    asgo:identifier "Art. 26(6)" ;
    asgo:parentElement euaia:Art26 ;
    asgo:partOfFramework euaia:EUAIAct ;
    rdfs:label "Deployers keep automatically generated logs"@en ;
    asgo:appliesToRole euaia:Deployer ;
    asgo:appliesToTier euaia:HighRisk .
```

## Pattern 3 – a new control (in `ai-controls.ttl`)

```turtle
ctl:RAGSourceTrustScoring a asgo:TechnicalControl ;
    rdfs:label "Trust scoring of RAG sources"@en ;
    asgo:controlDomain "Application security" ;
    asgo:applicableToScope ctl:Scope3 , ctl:Scope4 , ctl:Scope5 ;
    skos:definition "…"@en ;
    asgo:mitigates threat:IndirectPromptInjection ;
    asgo:implements euaia:Art15-5 , nist:MS-2 ;
    asgo:inLifecycleStage asgo:OperateAndMonitor ;
    asgo:authorityLevel asgo:PractitionerInsight ;
    dcterms:creator "Gokcenur Yazici" ;
    dcterms:created "2026-10-01"^^xsd:date .
```

## Pattern 4 – an interpretation or lesson learned

Attach notes to existing elements without changing the authoritative text:

```turtle
pk:Note-Art15-AgentScope a skos:Concept ;
    rdfs:label "Art. 15 and agentic tool use"@en ;
    skos:note "In practice, auditors read Art. 15(5) as covering tool-call abuse in agents…"@en ;
    dcterms:subject euaia:Art15-5 ;
    asgo:authorityLevel asgo:PractitionerInsight ;
    dcterms:creator "Gokcenur Yazici" ;
    dcterms:created "2026-10-01"^^xsd:date .
```

## Pattern 5 – a mapping

Add it to `ontology/mappings/framework-crosswalk.ttl` together with an `asgo:mappingRationale` on the subject explaining why. To have mappings reviewed: `python scripts/mapping_review.py export` → reviewer fills the Decision column → `python scripts/mapping_review.py import <file> --reviewer "Name"`. Use `skos:closeMatch` for substantially overlapping intent and `skos:relatedMatch` for partial overlap. Avoid `skos:exactMatch` between different frameworks.

## Conventions

- Language: English, with `@en` tags on labels and definitions.
- Local names: `Art15-5`, `GV-1`, `MG-4.1` style for framework elements; `UpperCamelCase` for classes and controls.
- Quote official text only in `skos:definition`; put your interpretation in `skos:note` or `skos:scopeNote`.
- Add a competency question to `queries/` when you add a new kind of relationship.
