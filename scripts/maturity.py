"""Rule-based maturity scorecard for ASGO (run: python scripts/asgo.py maturity).

Each dimension has four measurable checks; score = 1 + checks passed (max 5).
Thresholds are deliberately simple so the scorecard doubles as a to-do list.
"""
import datetime as dt
import subprocess
from collections import Counter

from rdflib import RDF, RDFS, Namespace, URIRef
from rdflib.namespace import SKOS

ASGO = Namespace("https://w3id.org/asgo/core#")
BASE = "https://w3id.org/asgo/"


def _git(root, *args):
    try:
        return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:
        return ""


def compute(g, root, shacl_ok=None, undefined_refs=None):
    today = dt.date.today()
    fws = list(g.subjects(RDF.type, ASGO.Framework))
    frac = lambda xs: (sum(xs) / len(xs)) if xs else 0.0

    # framework elements and verification
    elements = set(g.subjects(ASGO.partOfFramework, None))
    status = Counter(str(g.value(e, ASGO.verificationStatus) or "").rsplit("#", 1)[-1] for e in elements)
    primary = status["VerifiedPrimary"] / max(1, len(elements))
    any_verified = (status["VerifiedPrimary"] + status["CorroboratedSecondary"]) / max(1, len(elements))
    unverified_fw = [f for f in fws if str(g.value(f, ASGO.verificationStatus) or "").endswith("#Unverified")]

    # entities, definitions, labels
    entities = [s for s in set(g.subjects(RDFS.label, None)) if isinstance(s, URIRef) and str(s).startswith(BASE)]
    defined = frac([bool(g.value(s, SKOS.definition) or g.value(s, SKOS.scopeNote) or g.value(s, SKOS.note)) for s in entities])
    labels = Counter(str(g.value(s, RDFS.label)) for s in entities)
    dup_labels = sum(1 for v in labels.values() if v > 1)

    # mappings
    map_subjects = {s for p in (SKOS.closeMatch, SKOS.relatedMatch) for s in g.subjects(p, None)
                    if (s, ASGO.partOfFramework, None) in g}
    n_mappings = sum(1 for p in (SKOS.closeMatch, SKOS.relatedMatch) for _ in g.triples((None, p, None)))
    with_rationale = frac([bool(g.value(s, ASGO.mappingRationale)) for s in map_subjects])
    crosswalk = URIRef(BASE + "crosswalk")
    reviewed = bool(g.value(crosswalk, ASGO.reviewedBy))

    # checked dates
    checked = [str(g.value(f, ASGO.statusCheckedOn)) for f in fws if g.value(f, ASGO.statusCheckedOn)]
    fresh = bool(checked) and min(dt.date.fromisoformat(c) for c in checked) >= today - dt.timedelta(days=90)

    # cases
    cases = list(g.subjects(RDF.type, ASGO.PractitionerCase))
    case_ctrl = [c for case in cases for c in g.objects(case, ASGO.appliedControl)]

    # repository facts
    has = lambda p: (root / p).exists()
    remote = bool(_git(root, "remote"))
    tags = bool(_git(root, "tag"))
    authors = len(set(_git(root, "log", "--format=%an").splitlines()))

    D = []

    def dim(name, checks):
        passed = sum(ok for _, ok, _ in checks)
        D.append({"name": name, "score": 1 + passed,
                  "checks": [{"label": l, "ok": bool(ok), "detail": d} for l, ok, d in checks]})

    dim("Source transparency", [
        ("Every framework has a publication status", frac([bool(g.value(f, ASGO.publicationStatus)) for f in fws]) == 1, f"{len(fws)} frameworks"),
        ("≥90% of frameworks link to their source", frac([bool(g.value(f, ASGO.sourceURL)) for f in fws]) >= .9,
         f"{sum(bool(g.value(f, ASGO.sourceURL)) for f in fws)}/{len(fws)}"),
        ("Every framework has an authority level", frac([bool(g.value(f, ASGO.authorityLevel)) for f in fws]) == 1, ""),
        ("All statuses checked in the last 90 days", fresh, f"oldest check {min(checked) if checked else '—'}"),
    ])
    dim("Framework content", [
        ("≥50% of framework elements verified against the primary source", primary >= .5, f"{primary:.0%}"),
        ("≥80% verified or corroborated", any_verified >= .8, f"{any_verified:.0%}"),
        ("No core framework marked unverified", not unverified_fw, ", ".join(str(g.value(f, RDFS.label)) for f in unverified_fw) or "none"),
        ("Amendments tracked (amending acts recorded)", bool(list(g.subjects(RDF.type, ASGO.AmendingAct))), ""),
    ])
    dim("Model quality", [
        ("SHACL validation passes", bool(shacl_ok), ""),
        ("No undefined references", undefined_refs == 0, f"{undefined_refs} found" if undefined_refs is not None else "not run"),
        ("Labels are unique", dup_labels == 0, f"{dup_labels} duplicates"),
        ("≥60% of entities have a definition or note", defined >= .6, f"{defined:.0%}"),
    ])
    dim("Mapping reliability", [
        ("≥100 framework mappings", n_mappings >= 100, f"{n_mappings}"),
        ("Mappings flagged as author interpretation", (crosswalk, ASGO.authorityLevel, ASGO.PractitionerInsight) in g, ""),
        ("≥50% of mapped elements carry a rationale", with_rationale >= .5, f"{with_rationale:.0%}"),
        ("Mappings reviewed by a named expert", reviewed, "asgo:reviewedBy on the crosswalk"),
    ])
    dim("Testing & QA", [
        ("SHACL shapes present", has("shapes/asgo-shapes.ttl"), ""),
        ("CI workflow defined", has(".github/workflows/validate.yml"), ""),
        ("CI has run (repository published)", remote, "no git remote" if not remote else "remote configured"),
        ("Automated tests for the tools", has("tests"), "no tests/ folder" if not has("tests") else ""),
    ])
    n_queries = len(list((root / "queries").glob("*.rq")))
    dim("Usability", [
        ("Opens in Protege offline (import catalog)", has("ontology/catalog-v001.xml"), ""),
        ("≥10 ready-made SPARQL queries", n_queries >= 10, f"{n_queries} queries"),
        ("Exportable to other formats (OWL/XML, JSON-LD, N-Triples)", has("scripts/asgo.py"), "python scripts/asgo.py export"),
        ("Browsable online without download", remote, "not published" if not remote else ""),
    ])
    dim("Documentation", [
        ("README", has("README.md"), ""),
        ("Model guide", has("docs/how-to-read.md"), ""),
        ("Contribution guide", has("docs/adding-knowledge.md"), ""),
        ("Changelog", has("CHANGELOG.md"), "no CHANGELOG.md" if not has("CHANGELOG.md") else ""),
    ])
    dim("Practitioner knowledge", [
        ("≥3 practitioner cases", len(cases) >= 3, f"{len(cases)} cases"),
        ("≥10 practitioner cases", len(cases) >= 10, f"{len(cases)} cases"),
        ("Every case has a lesson learned", all(g.value(c, ASGO.lessonLearned) for c in cases) and bool(cases), ""),
        ("Case controls linked to requirements", bool(case_ctrl) and all(g.value(c, ASGO.implements) for c in case_ctrl), ""),
    ])
    dim("Maintenance", [
        ("Version history (git)", bool(_git(root, "log", "-1", "--format=%h")), ""),
        ("Tagged releases", tags, "no git tags" if not tags else ""),
        ("Update routine documented", has("docs/maintenance.md"), "no docs/maintenance.md" if not has("docs/maintenance.md") else ""),
        ("Regeneration commands (catalog, export)", has("scripts/asgo.py"), ""),
    ])
    dim("Publication & adoption", [
        ("Licence file", has("LICENSE"), ""),
        ("Published repository", remote, ""),
        ("Versioned release", tags, ""),
        ("More than one contributor", authors > 1, f"{authors} author(s)"),
    ])
    overall = sum(d["score"] for d in D) / len(D)
    return {"overall": round(overall, 1), "dimensions": D}
