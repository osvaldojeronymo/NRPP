# a5_human_guided_structuring.py
# -*- coding: utf-8 -*-

import pandas as pd
from pathlib import Path


def _valores(g, coluna, filtro_coluna=None, filtro_valor=None):

    if coluna not in g.columns:
        return []

    dados = g

    if filtro_coluna and filtro_coluna in g.columns:
        dados = dados[dados[filtro_coluna] == filtro_valor]

    return sorted(dados[coluna].dropna().astype(str).unique())


def montar_validacao_nrpp(df):

    rows = []

    for seg_id, g in df.groupby("id"):

        texto = g["texto"].iloc[0]

        docs = _valores(g, "termo_norm", "classe", "documento")
        procs = _valores(g, "termo_norm", "classe", "processo")
        entidades = _valores(g, "entidade_coletiva_detectada")
        tipos = _valores(g, "tipo_funcional")
        rels = _valores(g, "categoria_relacionamento")

        rows.append({

            "Fonte (item normativo)": seg_id,

            "Trecho da norma":
                texto,

            "Ação normativa detectada":
                " / ".join(procs),

            "Documento / artefato requerido":
                " / ".join(docs),

            "Tipo funcional ISDF":
                " / ".join(tipos),

            "Entidade coletiva detectada":
                " / ".join(entidades),

            "Categoria de relacionamento ISDF":
                " / ".join(rels),

            "Número de evidências":
                len(g),

            "Conceitos detectados":
                " / ".join(_valores(g, "termo_norm")),

            "Validação pesquisador":
                "",

            "Ator responsável":
                "",

            "Sistema envolvido":
                "",

            "Observações":
                ""

        })

    return pd.DataFrame(rows)


def montar_descricao_isdf(df):

    rows = []

    if "isdf_elemento" not in df.columns:
        return pd.DataFrame()

    for seg_id, g in df.groupby("id"):

        texto = g["texto"].iloc[0]

        for elemento, item in g.groupby("isdf_elemento", dropna=True):
            if not elemento:
                continue

            rows.append({
                "Fonte (item normativo)": seg_id,
                "Elemento ISDF": elemento,
                "Área ISDF": " / ".join(_valores(item, "isdf_area")),
                "Tipo funcional": " / ".join(_valores(item, "tipo_funcional")),
                "Termos normalizados": " / ".join(_valores(item, "termo_norm")),
                "Trecho da norma": texto,
                "Validação pesquisador": "",
                "Observações": "",
            })

    return pd.DataFrame(rows)


def montar_relacionamentos_isdf(df):

    if "classe" not in df.columns:
        return pd.DataFrame()

    rel = df[df["classe"].isin(["documento", "entidade_coletiva", "relacionamento"])].copy()

    if rel.empty:
        return pd.DataFrame()

    colunas = [
        "id",
        "texto",
        "classe",
        "termo",
        "termo_norm",
        "entidade_coletiva_detectada",
        "documento_relacionado",
        "categoria_relacionamento",
        "isdf_elemento",
        "necessita_validacao",
    ]

    return rel[[coluna for coluna in colunas if coluna in rel.columns]]


def montar_controle_descricao():

    return pd.DataFrame([{
        "Identificador da descrição da função": "",
        "Instituição responsável": "",
        "Regras e/ou convenções utilizadas": "ISDF - Norma Internacional para Descricao de Funcoes, Conselho Internacional de Arquivos, 2008",
        "Status": "Preliminar",
        "Nível de detalhamento": "Parcial",
        "Datas de criação, revisão ou obsolescência": "",
        "Idioma(s) e forma(s) de escrita": "Português",
        "Fontes": "",
        "Notas de manutenção": "Descrição gerada automaticamente pelo NRPP para validação humana.",
    }])


def run(a4_csv, out_xlsx):

    print("\n[A5] Estruturação analítica das evidências")

    a4_csv = Path(a4_csv)

    df = pd.read_csv(a4_csv, sep=";", dtype=str)

    if df.empty:
        raise ValueError("A4 não produziu evidências.")

    df_out = montar_validacao_nrpp(df)
    df_isdf = montar_descricao_isdf(df)
    df_rels = montar_relacionamentos_isdf(df)
    df_controle = montar_controle_descricao()

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

        df_isdf.to_excel(
            writer,
            sheet_name="descricao_isdf",
            index=False
        )

        df_rels.to_excel(
            writer,
            sheet_name="relacionamentos_isdf",
            index=False
        )

        df_controle.to_excel(
            writer,
            sheet_name="controle_descricao",
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
