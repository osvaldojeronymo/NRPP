# a4_glossary_guided_normalization.py
# -*- coding: utf-8 -*-

"""
A4 — Glossary-guided semantic normalization (versão avançada)
"""

import csv
import json
import re
import unicodedata
from pathlib import Path


# --------------------------------------------------
# utilidades
# --------------------------------------------------

def strip_accents(text):

    text = unicodedata.normalize("NFD", text)

    return "".join(
        ch for ch in text
        if not unicodedata.combining(ch)
    )


def normalize_key(s):

    s = str(s).lower().strip()

    s = strip_accents(s)

    s = re.sub(r"[^\w\s]", "", s)

    s = re.sub(r"\s+", " ", s)

    return s


# --------------------------------------------------
# normalização leve de plural
# --------------------------------------------------

def normalize_plural(term):

    if term.endswith("oes"):
        return term[:-3] + "ao"

    if term.endswith("aes"):
        return term[:-3] + "ao"

    if term.endswith("s") and len(term) > 4:
        return term[:-1]

    return term


# --------------------------------------------------
# carregar glossário
# --------------------------------------------------

def load_glossary(glossary_path):

    data = json.loads(Path(glossary_path).read_text(encoding="utf-8"))

    glossary = {}

    for termo, preferencial in data.items():

        key = normalize_key(termo)

        val = normalize_key(preferencial)

        glossary[key] = val

    return glossary


# --------------------------------------------------
# matching semântico robusto
# --------------------------------------------------

def match_term(term, glossary):

    key = normalize_key(term)

    if key in glossary:
        return glossary[key]

    key2 = normalize_plural(key)

    if key2 in glossary:
        return glossary[key2]

    return None


# --------------------------------------------------
# execução principal
# --------------------------------------------------

def run(a3_csv, glossary_path, out_csv, audit_csv):

    print("\n[A4] Normalização terminológica (robusta)")

    glossary = load_glossary(glossary_path)

    total = 0
    ok = 0
    nao = 0

    with open(a3_csv, encoding="utf-8") as f_in, \
         open(out_csv, "w", encoding="utf-8", newline="") as f_out, \
         open(audit_csv, "w", encoding="utf-8", newline="") as f_audit:

        reader = csv.DictReader(f_in, delimiter=";")

        writer = csv.DictWriter(
            f_out,
            fieldnames=[
                "id",
                "texto",
                "termo",
                "classe",
                "termo_norm"
            ],
            delimiter=";"
        )

        audit = csv.DictWriter(
            f_audit,
            fieldnames=[
                "id",
                "texto",
                "termo",
                "motivo"
            ],
            delimiter=";"
        )

        writer.writeheader()
        audit.writeheader()

        for row in reader:

            total += 1

            termo = row.get("termo", "")

            termo_norm = match_term(termo, glossary)

            if termo_norm:

                writer.writerow({
                    "id": row.get("id", ""),
                    "texto": row.get("texto", ""),
                    "termo": termo,
                    "classe": row.get("classe", ""),
                    "termo_norm": termo_norm
                })

                ok += 1

            else:

                audit.writerow({
                    "id": row.get("id", ""),
                    "texto": row.get("texto", ""),
                    "termo": termo,
                    "motivo": "fora_do_glossario"
                })

                nao += 1

    print(f"[A4] Linhas processadas: {total}")
    print(f"[A4] Normalizadas: {ok}")
    print(f"[A4] Fora do glossário: {nao}")
    print(f"[A4] Saída: {out_csv}")
    print(f"[A4] Auditoria: {audit_csv}")


# --------------------------------------------------
# interface do orchestrator
# --------------------------------------------------

def run_pipeline(a3_csv):

    a3_csv = Path(a3_csv)

    base = a3_csv.parent
    stem = a3_csv.stem

    glossary_path = Path("resources/glossario_arquivistico_limpo.json")

    out_csv = base / f"{stem}_normalized.csv"
    audit_csv = base / f"{stem}_audit.csv"

    run(a3_csv, glossary_path, out_csv, audit_csv)

    return out_csv


# --------------------------------------------------
# CLI opcional
# --------------------------------------------------

def main():

    import sys

    if len(sys.argv) < 5:

        print(
            "Uso:\n"
            "python a4_glossary_guided_normalization.py "
            "<A3.csv> <glossario.json> <OUT.csv> <AUDIT.csv>"
        )

        sys.exit(1)

    run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


if __name__ == "__main__":
    main()