## a3_controlled_semantic_anchoring.py
# -*- coding: utf-8 -*-

import csv
import re
from pathlib import Path


DOC_PATTERNS = [
    (r"\banexo(?:s)?\b", "anexo"),
    (r"\bformul[aá]rio(?:s)?\b", "formulario"),
    (r"\brelat[oó]rio(?:s)?\b", "relatorio"),
    (r"\bdeclara[cç][aã]o(?:es|ões)?\b", "declaracao"),
    (r"\btermo(?:s)?\b", "termo"),
    (r"\bplanilha(?:s)?\b", "planilha"),
    (r"\bcomprovante(?:s)?\b", "comprovante"),
    (r"\bprocesso(?:s)?\b", "processo administrativo"),
    (r"\bdossi[eê](?:s)?\b", "dossie"),
    (r"\bregistro(?:s)?\b", "registro"),
]

PROC_PATTERNS = [
    (r"\bcompete(?:m)?\b", "compete"),
    (r"\bdeve(?:m)?\b", "deve"),
    (r"\brealiza(?:r|da|do|das|dos)?\b", "realizar"),
    (r"\bregistrar(?:\w*)\b", "registrar"),
    (r"\banexar(?:\w*)\b", "anexar"),
    (r"\belaborar(?:\w*)\b", "elaborar"),
    (r"\baprovar(?:\w*)\b", "aprovar"),
    (r"\bencaminhar(?:\w*)\b", "encaminhar"),
    (r"\b(?:manter|mant[eé]m|manuten[cç][aã]o)\b", "manter"),
    (r"\b(?:guardar|guarda|custodiar(?:\w*))\b", "custodiar"),
    (r"\bpreservar(?:\w*)\b", "preservar"),
    (r"\bclassificar(?:\w*)\b", "classificar"),
    (r"\bavaliar(?:\w*)\b", "avaliar"),
]

FUNCTION_PATTERNS = [
    (r"\bfun[cç][aã]o(?:es|ões)?\b", "funcao"),
    (r"\bsubfun[cç][aã]o(?:es|ões)?\b", "subfuncao"),
    (r"\batividade(?:s)?\b", "atividade"),
    (r"\btarefa(?:s)?\b", "tarefa"),
    (r"\btransa[cç][aã]o(?:es|ões)?\b", "transacao"),
]

ENTITY_PATTERNS = [
    (r"\bentidade(?:s)? coletiva(?:s)?\b", "entidade coletiva"),
    (r"\bunidade(?:s)?\b", "unidade"),
    (r"\bdepartamento(?:s)?\b", "departamento"),
    (r"\bdiretoria(?:s)?\b", "diretoria"),
    (r"\bger[eê]ncia(?:s)?\b", "gerencia"),
    (r"\bcoordena[cç][aã]o(?:es|ões)?\b", "coordenacao"),
    (r"\bcomiss[aã]o(?:es|ões)?\b", "comissao"),
    (r"\bconselho(?:s)?\b", "conselho"),
    (r"\b[oó]rg[aã]o(?:s)?\b", "orgao"),
    (r"\brespons[aá]vel(?:eis|éis)?\b", "responsavel"),
]

LEGAL_PATTERNS = [
    (r"\blei(?:s)?\b", "lei"),
    (r"\bdecreto(?:s)?\b", "decreto"),
    (r"\bresolu[cç][aã]o(?:es|ões)?\b", "resolucao"),
    (r"\bportaria(?:s)?\b", "portaria"),
    (r"\binstru[cç][aã]o normativa(?:s)?\b", "instrucao normativa"),
    (r"\bnorma(?:s)?\b", "norma"),
    (r"\bregulamento(?:s)?\b", "regulamento"),
]

RELATIONSHIP_PATTERNS = [
    (r"\bproduz(?:ir|ido|ida|em)?\b", "produz"),
    (r"\butiliza(?:r|do|da|m)?\b", "utiliza"),
    (r"\bexecuta(?:r|do|da|m)?\b", "executa"),
    (r"\bapoia(?:r|do|da|m)?\b", "apoia"),
    (r"\bvinculad[ao]s?\b", "vinculado"),
    (r"\bsubordinad[ao]s?\b", "subordinado"),
    (r"\bsucede(?:r|u|m)?\b", "sucede"),
    (r"\bsubstitui(?:r|u|do|da)?\b", "substitui"),
]

DATE_PATTERNS = [
    (r"\b\d{2}/\d{2}/\d{4}\b", "data completa"),
    (r"\b\d{4}\b", "ano"),
]


def detect_terms(text):

    terms = []

    for pat, label in DOC_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            terms.append((label, "documento"))

    for pat, label in PROC_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            terms.append((label, "processo"))

    for pat, label in FUNCTION_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            terms.append((label, "funcao"))

    for pat, label in ENTITY_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            terms.append((label, "entidade_coletiva"))

    for pat, label in LEGAL_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            terms.append((label, "legislacao"))

    for pat, label in RELATIONSHIP_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            terms.append((label, "relacionamento"))

    for pat, label in DATE_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            terms.append((label, "data"))

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
