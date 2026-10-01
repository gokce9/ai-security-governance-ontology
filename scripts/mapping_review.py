#!/usr/bin/env python3
"""Expert review of framework mappings via Excel.

Usage:
    python scripts/mapping_review.py export [out.xlsx]        # review workbook
    python scripts/mapping_review.py import reviewed.xlsx --reviewer "Name"
"""
import argparse
import datetime as dt
import re
import sys
from collections import Counter
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation
from rdflib import RDFS, Namespace
from rdflib.namespace import SKOS

sys.path.insert(0, str(Path(__file__).resolve().parent))
from asgo import ROOT, load_graph  # noqa: E402

ASGO = Namespace("https://w3id.org/asgo/core#")
RELATIONS = {SKOS.closeMatch: "close match", SKOS.relatedMatch: "related match",
             SKOS.exactMatch: "exact match", SKOS.broadMatch: "broader (2026 covers more)"}
DECISIONS = ["Approve", "Reject", "Change to close match", "Change to related match"]
CROSSWALK = ROOT / "ontology" / "mappings" / "framework-crosswalk.ttl"
CORRECTED = {"https://w3id.org/asgo/eu-ai-act#Art14|https://w3id.org/asgo/nist-ai-rmf#GV-3":
             "Corrected from close match to related match while drafting the rationale"}


def unverified_framework(g, x):
    fw = g.value(x, ASGO.partOfFramework)
    return fw is not None and str(g.value(fw, ASGO.verificationStatus) or "").endswith("#Unverified")


def mappings(g):
    """Mappings to review. Mappings touching an unverified framework (work in progress) are left out until that framework has been verified."""
    rows = []
    for p, rel in RELATIONS.items():
        for s, o in g.subject_objects(p):
            if (s, ASGO.partOfFramework, None) not in g or unverified_framework(g, s) or unverified_framework(g, o):
                continue
            fw = lambda x: str(g.value(g.value(x, ASGO.partOfFramework), RDFS.label) or "")
            text = lambda x: str(g.value(x, SKOS.definition) or g.value(x, SKOS.scopeNote) or "")
            rows.append({
                "s": str(s), "o": str(o), "rel": rel,
                "s_fw": fw(s), "s_id": str(g.value(s, ASGO.identifier) or ""), "s_label": str(g.value(s, RDFS.label) or ""),
                "s_text": text(s), "o_fw": fw(o), "o_id": str(g.value(o, ASGO.identifier) or ""),
                "o_label": str(g.value(o, RDFS.label) or ""), "o_text": text(o),
                "why": str(g.value(s, ASGO.mappingRationale) or ""),
                "note": CORRECTED.get(f"{s}|{o}", ""),
            })
    return sorted(rows, key=lambda r: (r["s_fw"], r["s_id"], r["rel"], r["o_id"]))


def cmd_export(args):
    rows = mappings(load_graph())
    wb = Workbook()
    info = wb.active
    info.title = "Instructions"
    for line in [
        "ASGO framework mapping review",
        "",
        "TR: Her satır bir eşleştirme. 'Decision' sütununda bir seçenek seçin; gerekirse 'Comment' yazın.",
        "    close match = büyük ölçüde aynı amaç · related match = kısmi/destekleyici örtüşme.",
        "    Bitirince dosyayı kaydedip bana gönderin ya da: python scripts/mapping_review.py import <dosya> --reviewer \"Ad Soyad\"",
        "",
        "EN: One row per mapping. Choose a Decision; add a Comment where useful.",
        "    close match = substantially the same intent · related match = partial / supporting overlap.",
        "    Then run: python scripts/mapping_review.py import <file> --reviewer \"Name\"",
        "",
        f"{len(rows)} mappings · rows marked in yellow were already corrected by the author.",
    ]:
        info.append([line])
    info["A1"].font = Font(bold=True, size=14)
    info.column_dimensions["A"].width = 120

    ws = wb.create_sheet("Mappings")
    head = ["#", "From framework", "From", "From - text", "Relation", "To framework", "To", "To - text",
            "Rationale (author)", "Decision", "Comment", "Author note", "_s", "_o", "_rel"]
    ws.append(head)
    widths = [5, 18, 30, 50, 16, 18, 30, 50, 60, 22, 40, 30, 2, 2, 2]
    for i, w in enumerate(widths, 1):
        c = ws.cell(row=1, column=i)
        c.font, c.fill = Font(bold=True, color="FFFFFF"), PatternFill("solid", fgColor="2F5BD3")
        ws.column_dimensions[c.column_letter].width = w
    for n, r in enumerate(rows, 1):
        ws.append([n, r["s_fw"], f'{r["s_id"]} {r["s_label"]}'.strip(), r["s_text"], r["rel"], r["o_fw"],
                   f'{r["o_id"]} {r["o_label"]}'.strip(), r["o_text"], r["why"], "", "", r["note"],
                   r["s"], r["o"], r["rel"]])
        if r["note"]:
            for c in ws[ws.max_row]:
                c.fill = PatternFill("solid", fgColor="FDF1DC")
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    for col in ("M", "N", "O"):
        ws.column_dimensions[col].hidden = True
    dv = DataValidation(type="list", formula1='"' + ",".join(DECISIONS) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"J2:J{len(rows) + 1}")
    ws.freeze_panes = "D2"
    ws.auto_filter.ref = ws.dimensions

    out = Path(args.out or ROOT / "build" / "mapping-review.xlsx")
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    print(f"Wrote {out} ({len(rows)} mappings)")
    return 0


def cmd_import(args):
    ws = load_workbook(args.file, data_only=True)["Mappings"]
    decided, changes = Counter(), []
    total = 0
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row[0]:
            continue
        total += 1
        decision, comment, s, o, rel = row[9], row[10], row[12], row[13], row[14]
        decided[decision or "(empty)"] += 1
        if decision and decision != "Approve":
            changes.append((decision, s, rel, o, comment or ""))
    print(f"{total} mappings: " + ", ".join(f"{k}: {v}" for k, v in decided.items()))
    if decided["(empty)"]:
        print("Review incomplete - fill every Decision before importing.")
        return 1
    if changes:
        print("Changes requested (apply them to framework-crosswalk.ttl, then import again):")
        for d, s, rel, o, c in changes:
            print(f"  - {d}: {s.split('/')[-1]} [{rel}] {o.split('/')[-1]}  {c}")
        return 1
    today = dt.date.today().isoformat()
    ttl = CROSSWALK.read_text()
    reviewer = args.reviewer.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    for prop, value in (("reviewedBy", f'"{reviewer}"'), ("reviewedOn", f'"{today}"^^xsd:date'),
                        ("reviewScope", f'"All {total} framework mappings approved"@en')):
        ttl, n = re.subn(rf'(    asgo:{prop} ).*? ;\n', lambda m: f"{m.group(1)}{value} ;\n", ttl, count=1)
        if not n:
            sys.exit(f"asgo:{prop} not found in the crosswalk header")
    CROSSWALK.write_text(ttl)
    print(f"All {total} mappings approved - review recorded in {CROSSWALK.relative_to(ROOT)}")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("export")
    e.add_argument("out", nargs="?")
    e.set_defaults(fn=cmd_export)
    i = sub.add_parser("import")
    i.add_argument("file")
    i.add_argument("--reviewer", required=True)
    i.set_defaults(fn=cmd_import)
    a = p.parse_args()
    sys.exit(a.fn(a) or 0)


if __name__ == "__main__":
    main()
