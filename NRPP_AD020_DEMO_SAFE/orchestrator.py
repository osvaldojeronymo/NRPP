# orchestrator.py

from pathlib import Path
import shutil
from multiprocessing import Pool, cpu_count
import pandas as pd
from pathlib import Path

pdf_dir = Path("pdfs")
from pipeline.a1_text_normalization import run_pipeline as a1
from pipeline.a2_structural_segmentation import run as a2
from pipeline.a3_semantic_cues import run_pipeline as a3
from pipeline.a4_glossary_guided_normalization import run_pipeline as a4
from pipeline.a5_human_guided_structuring import run_pipeline as a5


# --------------------------------------------------
# gerar README automático
# --------------------------------------------------

def gerar_readme(pasta_resultado, nome_pdf):

    texto = f"""
# NRPP – Dossiê de processamento normativo

Arquivo analisado: {nome_pdf}

Este diretório contém os resultados produzidos pelo NRPP
(Normative-to-Record Preprocessing Pipeline).

## ENTRADA
Documento normativo original utilizado na análise.

## EXTRACAO_TEXTO
Texto bruto extraído do PDF.

## INTERMEDIARIOS
Arquivos intermediários do pipeline:
- segmentos_texto.csv
- evidencias_semanticas.csv
- evidencias_normalizadas.csv

## AUDITORIA_PIPELINE
termos_fora_do_glossario.csv
Termos detectados no texto que não possuem correspondência no glossário.

## PRODUTO_FINAL
tabela_validacao_nrpp.xlsx
Tabela analítica para validação humana.
"""

    (pasta_resultado / "README.md").write_text(texto)


# --------------------------------------------------
# processar um único PDF
# --------------------------------------------------

def processar_pdf(pdf_path):

    pdf_path = Path(pdf_path)
    base = pdf_path.parent
    nome = pdf_path.stem

    pasta_resultado = base / "NRPP_RESULTADOS" / nome

    entrada = pasta_resultado / "ENTRADA"
    texto_dir = pasta_resultado / "EXTRACAO_TEXTO"
    inter = pasta_resultado / "INTERMEDIARIOS"
    audit = pasta_resultado / "AUDITORIA_PIPELINE"
    produto = pasta_resultado / "PRODUTO_FINAL"

    entrada.mkdir(parents=True, exist_ok=True)
    texto_dir.mkdir(parents=True, exist_ok=True)
    inter.mkdir(parents=True, exist_ok=True)
    audit.mkdir(parents=True, exist_ok=True)
    produto.mkdir(parents=True, exist_ok=True)

    try:

        print(f"\nProcessando: {pdf_path.name}")

        # copiar PDF original
        shutil.copy(pdf_path, entrada / pdf_path.name)

        # -------------------
        # pipeline NRPP
        # -------------------

        text_file = a1(pdf_path)

        segments = a2(text_file)

        cues = a3(segments)

        normalized = a4(cues)

        tabela = a5(normalized)

        # -------------------
        # mover arquivos
        # -------------------

        shutil.move(text_file, texto_dir / f"{nome}.txt")

        shutil.move(segments, inter / "segmentos_texto.csv")

        shutil.move(cues, inter / "evidencias_semanticas.csv")

        shutil.move(normalized, inter / "evidencias_normalizadas.csv")

        # mover auditoria A4 automaticamente
        for f in base.glob("*_audit.csv"):
            shutil.move(
                f,
                audit / "termos_fora_do_glossario.csv"
            )

        shutil.move(tabela, produto / "tabela_validacao_nrpp.xlsx")

        # gerar README
        gerar_readme(pasta_resultado, pdf_path.name)

        # -------------------
        # estatísticas
        # -------------------

        seg = pd.read_csv(inter / "segmentos_texto.csv", sep=";")
        cues_df = pd.read_csv(inter / "evidencias_semanticas.csv", sep=";")
        norm = pd.read_csv(inter / "evidencias_normalizadas.csv", sep=";")

        return {
            "arquivo": pdf_path.name,
            "segmentos": len(seg),
            "evidencias": len(cues_df),
            "normalizadas": len(norm)
        }

    except Exception as e:

        print(f"Erro em {pdf_path.name}: {e}")

        return None


# --------------------------------------------------
# pipeline principal
# --------------------------------------------------

def run_pipeline(pdf_dir, clean=False):

    pdf_dir = Path(pdf_dir)

    result_dir = pdf_dir / "NRPP_RESULTADOS"

    if clean and result_dir.exists():

        print("Removendo resultados anteriores...")
        shutil.rmtree(result_dir)

    pdf_files = list(pdf_dir.glob("*.pdf"))

    if not pdf_files:

        print("Nenhum PDF encontrado.")
        return

    print(f"{len(pdf_files)} PDF(s) encontrados.")

    # paralelismo inteligente
    workers = min(cpu_count() - 1, len(pdf_files))

    print(f"Executando com {workers} processos em paralelo.\n")

    with Pool(workers) as p:

        stats = p.map(processar_pdf, pdf_files)

    stats = [s for s in stats if s]

    if stats:

        resumo = pd.DataFrame(stats)

        resumo_path = result_dir / "resumo_pipeline.csv"

        resumo.to_csv(resumo_path, index=False)

        print("\nResumo geral gerado:")
        print(resumo_path)