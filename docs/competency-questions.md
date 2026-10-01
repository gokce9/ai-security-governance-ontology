# Competency questions

Competency questions define what the ontology must be able to answer. Implemented questions have a SPARQL file in `queries/`.

| ID | Question | Status |
|---|---|---|
| CQ1 | Which EU AI Act obligations apply to a given AI system, for which role, and from when? | `cq01-obligations-for-system.rq` |
| CQ2 | Which NIST AI RMF categories support compliance with each EU AI Act article? | `cq02-nist-for-eu-article.rq` |
| CQ3 | Which controls mitigate a given threat, and which requirements do they help implement? | `cq03-controls-for-threat.rq` |
| CQ4 | Which risks of an AI system have no mitigating control? | `cq04-unmitigated-risks.rq` |
| CQ5 | Which statements are practitioner insights, and who authored them? | `cq05-practitioner-insights.rq` |
| CQ6 | For each control, which requirements does it satisfy in every framework (coverage matrix)? | `cq06-control-coverage-matrix.rq` |
| CQ7 | For each EU AI Act article, which NIST AI RMF subcategories can be reused? | `cq07-eu-article-to-nist.rq` |
| CQ8 | Which EU AI Act obligations are in force or become applicable within 12 months? | `cq08-upcoming-obligations.rq` |
| CQ9 | What is the publication status of every framework, and when was it last verified? | `cq09-framework-status.rq` |
| CQ10 | Which trustworthiness characteristics does a given attack degrade? | planned |
| CQ11 | Which evidence types demonstrate which requirements across frameworks? | `cq11-evidence-per-artefact.rq` |
| CQ12 | Which third-party components introduce supply-chain risk (GOVERN 6 / Art. 25)? | planned |
| CQ13 | What is the maximum penalty exposure for a given non-compliance? | planned |
| CQ14 | For a given AI system, which evidence must exist for the EU AI Act obligations of its risk tier? | `cq14-system-evidence-checklist.rq` |
| CQ15 | Which framework elements are not yet verified against their primary source (work-in-progress backlog)? | `cq15-verification-backlog.rq` |
| CQ16 | Which consequence-scanning questions should an auditor ask, and which requirements does each answer? | `cq16-assessment-questionnaire.rq` |
| CQ17 | What are the steps of the Annex VI conformity assessment, with articles and evidence per step? | `cq17-conformity-roadmap.rq` |
| CQ18 | Which metrics (formula, threshold) test each risk of an AI system? | `cq18-metrics-for-risks.rq` |
| CQ19 | For each practitioner case: threats, applied controls, requirements satisfied and lesson learned | `cq19-practitioner-cases.rq` |
