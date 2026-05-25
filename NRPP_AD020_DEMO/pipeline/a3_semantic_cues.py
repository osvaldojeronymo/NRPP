## a3_controlled_semantic_anchoring.py
# -*- coding: utf-8 -*-

import csv
import re
from pathlib import Path


DOC_PATTERNS = [
    (r"\banexo(?:s)?\b", "anexo"),
    (r"\bformulario(?:s)?\b", "formulario"),
    (r"\brelatorio(?:s)?\b", "relatorio"),
    (r"\bdeclaracao(?:s)?\b", "declaracao"),
    (r"\btermo(?:s)?\b", "termo"),
    (r"\bplanilha(?:s)?\b", "planilha"),
    (r"\bcomprovante(?:s)?\b", "comprovante"),
]

PROC_PATTERNS = [
    (r"\bcompete\b", "compete"),
    (r"\bdeve(?:m)?\b", "deve"),
    (r"\brealiza(?:r|da|do|das|dos)?\b", "realizar"),
    (r"\bregistrar(?:\w*)\b", "registrar"),
    (r"\banexar(?:\w*)\b", "anexar"),
]


def detect_terms(text):

    terms = []

    for pat, label in DOC_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            terms.append((label, "documento"))

    for pat, label in PROC_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            terms.append((label, "processo"))

    return terms


def run(a2_csv, out_csv):

    a2_csv = Path(a2_csv)
    out_csv = Path(out_csv)

    print(f"\n[A3] Ancoragem semântica: {a2_csv.name}")

    rows = []

    with open(a2_csv, encoding="utf-8") as f:

        reader = csv.DictReader(f, delimiter=";")

        for row in reader:

            texto = row["texto"]
            seg_id = row["id"]

            terms = detect_terms(texto)

            for termo, classe in terms:

                rows.append({
                    "id": seg_id,
                    "texto": texto,
                    "termo": termo,
                    "classe": classe
                })

    out_csv.parent.mkdir(parents=True, exist_ok=True)

    with open(out_csv, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=["id", "texto", "termo", "classe"],
            delimiter=";"
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"[A3] Evidências detectadas: {len(rows)}")
    print(f"[A3] Arquivo gerado: {out_csv}\n")


def run_pipeline(a2_csv):

    a2_csv = Path(a2_csv)
    out_csv = a2_csv.parent / f"{a2_csv.stem}_cues.csv"

    run(a2_csv, out_csv)

    return out_csv