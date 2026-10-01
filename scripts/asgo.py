#!/usr/bin/env python3
"""ASGO toolkit: load, validate, query and export the ontology.

Usage:
    python scripts/asgo.py validate              # syntax + SHACL
    python scripts/asgo.py query queries/cq01-obligations-for-system.rq
    python scripts/asgo.py query-all             # run every competency question
    python scripts/asgo.py export build/asgo.owl --format xml
    python scripts/asgo.py maturity              # rule-based maturity scorecard
    python scripts/asgo.py catalog               # refresh the Protege import catalog
"""
import argparse
import sys
from pathlib import Path

from rdflib import OWL, RDF, Graph, URIRef

ASGO_BASE = "https://w3id.org/asgo/"
ROOT = Path(__file__).resolve().parent.parent
ONTOLOGY_DIRS = [ROOT / "ontology", ROOT / "examples", ROOT / "data"]
SHAPES = ROOT / "shapes" / "asgo-shapes.ttl"
QUERIES = ROOT / "queries"


def load_graph(include_examples=True):
    g = Graph()
    dirs = ONTOLOGY_DIRS if include_examples else ONTOLOGY_DIRS[:1]
    for d in dirs:
        if not d.exists():
            continue
        for f in sorted(d.rglob("*.ttl")):
            try:
                g.parse(f, format="turtle")
            except Exception as e:  # report the file that broke
                sys.exit(f"Syntax error in {f.relative_to(ROOT)}:\n{e}")
    return g


def dangling_references(g):
    """ASGO IRIs used as objects but never declared with rdf:type (typos in IDs)."""
    declared = set(g.subjects(RDF.type, None))
    return sorted(
        {(p, o) for _, p, o in g
         if isinstance(o, URIRef) and str(o).startswith(ASGO_BASE)
         and p not in (RDF.type, OWL.imports) and o not in declared}
    )


def cmd_validate(_args):
    from pyshacl import validate

    g = load_graph()
    print(f"Loaded {len(g)} triples.")
    conforms, _, text = validate(
        g, shacl_graph=str(SHAPES), inference="rdfs", advanced=True
    )
    print(text)
    dangling = dangling_references(g)
    for p, o in dangling:
        print(f"Undefined reference: {g.qname(o)} (via {g.qname(p)})")
    return 0 if conforms and not dangling else 1


def run_query(g, path):
    print(f"\n### {path.name}")
    res = g.query(path.read_text())
    cols = [str(v) for v in res.vars]
    print(" | ".join(cols))
    print("-" * 60)
    for row in res:
        print(" | ".join("" if v is None else str(v) for v in row))


def cmd_query(args):
    run_query(load_graph(), Path(args.file))
    return 0


def cmd_query_all(_args):
    g = load_graph()
    for q in sorted(QUERIES.glob("*.rq")):
        run_query(g, q)
    return 0


def cmd_export(args):
    g = load_graph(include_examples=False)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(out, format=args.format)
    print(f"Wrote {len(g)} triples to {out}")
    return 0


def cmd_catalog(_args):
    """Regenerate ontology/catalog-v001.xml so Protege resolves imports offline."""
    root = ROOT / "ontology"
    entries = []
    for f in sorted(root.rglob("*.ttl")):
        g = Graph()
        g.parse(f, format="turtle")
        entries += [(str(o), f.relative_to(root).as_posix()) for o in g.subjects(RDF.type, OWL.Ontology)]
    lines = ['<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
             "<!-- Maps ASGO ontology IRIs to local files so Protege and OWL tools resolve imports offline. -->",
             '<catalog prefer="public" xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">']
    lines += [f'    <uri id="{Path(p).stem}" name="{iri}" uri="{p}"/>' for iri, p in entries]
    lines.append("</catalog>")
    (root / "catalog-v001.xml").write_text("\n".join(lines) + "\n")
    print(f"Mapped {len(entries)} ontologies in ontology/catalog-v001.xml")
    return 0


def cmd_maturity(_args):
    """Print the rule-based maturity scorecard."""
    from pyshacl import validate
    from maturity import compute

    g = load_graph()
    conforms, _, _ = validate(g, shacl_graph=str(SHAPES), inference="rdfs", advanced=True)
    m = compute(g, ROOT, shacl_ok=conforms, undefined_refs=len(dangling_references(g)))
    print(f"Overall maturity: {m['overall']} / 5\n")
    for d in m["dimensions"]:
        print(f"{d['name']:<24} {'#' * d['score']}{'.' * (5 - d['score'])}  {d['score']}/5")
        for c in d["checks"]:
            mark = "x" if c["ok"] else " "
            print(f"    [{mark}] {c['label']}" + (f"  ({c['detail']})" if c["detail"] else ""))
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("validate").set_defaults(fn=cmd_validate)
    q = sub.add_parser("query")
    q.add_argument("file")
    q.set_defaults(fn=cmd_query)
    sub.add_parser("query-all").set_defaults(fn=cmd_query_all)
    sub.add_parser("catalog").set_defaults(fn=cmd_catalog)
    sub.add_parser("maturity").set_defaults(fn=cmd_maturity)
    e = sub.add_parser("export")
    e.add_argument("out")
    e.add_argument("--format", default="xml", help="xml | turtle | json-ld | nt")
    e.set_defaults(fn=cmd_export)
    args = p.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
