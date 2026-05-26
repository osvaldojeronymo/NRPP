# a5_human_guided_structuring.py
# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path


def run(a4_csv, out_xlsx):

    print("\n[A5] Estruturação analítica das evidências")

    a4_csv = Path(a4_csv)

    df = pd.read_csv(a4_csv, sep=";", dtype=str)

    if df.empty:
        raise ValueError("A4 não produziu evidências.")

    rows = []

    for seg_id, g in df.groupby("id"):

        texto = g["texto"].iloc[0]

        docs = g[g["classe"] == "documento"]["termo_norm"].dropna().unique()
        procs = g[g["classe"] == "processo"]["termo_norm"].dropna().unique()

        rows.append({

            "Fonte (item normativo)": seg_id,

            "Trecho da norma":
                texto,

            "Ação normativa detectada":
                " / ".join(sorted(procs)),

            "Documento / artefato requerido":
                " / ".join(sorted(docs)),

            "Número de evidências":
                len(g),

            "Conceitos detectados":
                " / ".join(sorted(g["termo_norm"].dropna().unique())),

            "Validação pesquisador":
                "",

            "Ator responsável":
                "",

            "Sistema envolvido":
                "",

            "Observações":
                ""

        })

    df_out = pd.DataFrame(rows)

    out_xlsx = Path(out_xlsx)
    out_xlsx.parent.mkdir(parents=True, exist_ok=True)

    # caminhos dos arquivos anteriores

    a3_csv = a4_csv.parent / a4_csv.name.replace("_normalized", "")
    a2_csv = a3_csv.parent / a3_csv.name.replace("_cues.csv", ".csv")
    audit_csv = a4_csv.parent / a4_csv.name.replace("_normalized.csv", "_audit.csv")

    # Excel com múltiplas abas

    with pd.ExcelWriter(out_xlsx, engine="openpyxl") as writer:

        # produto principal
        df_out.to_excel(
            writer,
            sheet_name="validacao_nrpp",
            index=False
        )

        # A4
        df.to_excel(
            writer,
            sheet_name="evidencias_normalizadas",
            index=False
        )

        # A3
        if a3_csv.exists():
            df_a3 = pd.read_csv(a3_csv, sep=";", dtype=str)
            df_a3.to_excel(
                writer,
                sheet_name="evidencias_semanticas",
                index=False
            )

        # A2
        if a2_csv.exists():
            df_a2 = pd.read_csv(a2_csv, sep=";", dtype=str)
            df_a2.to_excel(
                writer,
                sheet_name="segmentos_texto",
                index=False
            )

        # auditoria
        if audit_csv.exists():
            df_audit = pd.read_csv(audit_csv, sep=";", dtype=str)
            df_audit.to_excel(
                writer,
                sheet_name="termos_fora_do_glossario",
                index=False
            )

    print(f"[A5] Evidências estruturadas: {len(df_out)}")
    print(f"[A5] Arquivo gerado: {out_xlsx}\n")


def run_pipeline(a4_csv):

    a4_csv = Path(a4_csv)

    out_xlsx = a4_csv.parent / f"{a4_csv.stem}_tabela_validacao.xlsx"

    run(a4_csv, out_xlsx)

    return out_xlsx
