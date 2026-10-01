# Opening ASGO in Protégé

1. Install [Protégé](https://protege.stanford.edu/) (5.6 or later).
2. *File → Open…* and choose `ontology/asgo.ttl`.
   Protégé finds `ontology/catalog-v001.xml` next to it and loads all modules
   from local files. The `https://w3id.org/asgo/...` IRIs do not need to resolve.
3. *Reasoner → HermiT → Start reasoner*. The ontology is consistent and within
   OWL 2 DL.
4. To include the example systems, also open `examples/*.ttl` via
   *File → Open…* in the same workspace, or merge them with ROBOT (below).

After adding a new module, run `python scripts/asgo.py catalog` so the catalog
lists it.

## Command-line checks (same engine as Protégé)

Requires Java 17+ and [ROBOT](http://robot.obolibrary.org/):

```bash
java -jar robot.jar merge --catalog ontology/catalog-v001.xml --input ontology/asgo.ttl --output merged.owl
java -jar robot.jar validate-profile --profile DL --input merged.owl --output dl-profile.txt
java -jar robot.jar reason --reasoner hermit --equivalent-classes-allowed all --input merged.owl
java -jar robot.jar report --input merged.owl --fail-on ERROR --output report.tsv
```

These also run in CI (`.github/workflows/validate.yml`, job `owl`).

## Modelling notes

- **Punning is intentional and valid OWL 2 DL.** Threat types such as
  `threat:PromptInjection` are classes (for the hierarchy) and are also used as
  individuals in assertions like `threat:InputOutputGuardrails asgo:mitigates threat:PromptInjection`.
- **`asgo:applicableFrom` is an annotation property** because `xsd:date` is not
  in the OWL 2 datatype map; as a data property it would break DL reasoning.
- **Labels are unique.** Framework elements carry their identifier in the label
  (e.g. "LLM01:2026 Prompt Injection") so they can be told apart in Protégé.
