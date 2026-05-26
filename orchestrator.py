# orchestrator.py

from pathlib import Path
import shutil
from multiprocessing import Pool, cpu_count
import pandas as pd

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

def _encontrar_pdfs(pdf_dir):

    return sorted(
        pdf
        for pdf in pdf_dir.rglob("*")
        if pdf.is_file()
        and pdf.suffix.lower() == ".pdf"
        and "NRPP_RESULTADOS" not in pdf.parts
    )


def processar_pdf(args):

    pdf_path, raiz_processamento = args

    pdf_path = Path(pdf_path)
    raiz_processamento = Path(raiz_processamento)
    nome = pdf_path.stem

    rel_parent = pdf_path.parent.relative_to(raiz_processamento)
    pasta_resultado = raiz_processamento / "NRPP_RESULTADOS" / rel_parent / nome

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

        rel_pdf = pdf_path.relative_to(raiz_processamento)

        print(f"\nProcessando: {rel_pdf}")

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
        audit_file = normalized.with_name(
            normalized.name.replace("_normalized.csv", "_audit.csv")
        )

        if audit_file.exists():
            shutil.move(
                audit_file,
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
            "arquivo": str(rel_pdf),
            "resultado": str(pasta_resultado.relative_to(raiz_processamento)),
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

    pdf_files = _encontrar_pdfs(pdf_dir)

    if not pdf_files:

        print("Nenhum PDF encontrado.")
        return

    print(f"{len(pdf_files)} PDF(s) encontrados.")

    # paralelismo inteligente
    workers = min(max(cpu_count() - 1, 1), len(pdf_files))

    print(f"Executando com {workers} processos em paralelo.\n")

    with Pool(workers) as p:

        stats = p.map(
            processar_pdf,
            [(pdf, pdf_dir) for pdf in pdf_files]
        )

    stats = [s for s in stats if s]

    if stats:

        resumo = pd.DataFrame(stats)

        resumo_path = result_dir / "resumo_pipeline.csv"

        resumo.to_csv(resumo_path, index=False)

        print("\nResumo geral gerado:")
        print(resumo_path)


def main():

    import argparse
    from BuscadorDePdfs import copiar_pdfs_de_origens, resolver_destino, resolver_origens

    parser = argparse.ArgumentParser(
        description="Executa o pipeline NRPP em PDFs diretos ou organizados em subpastas."
    )

    parser.add_argument(
        "pdf_dir",
        nargs="?",
        help=(
            "Pasta de processamento. "
            "Se omitida com --matricula ou --pasta-raiz, usa PASTA_RAIZ/scripts/pdfs. "
            "Caso contrário, usa pdfs."
        )
    )

    parser.add_argument(
        "--origem",
        nargs="*",
        help="Arquivo(s) PDF ou pasta(s) de origem para buscar PDFs recursivamente antes de executar."
    )

    parser.add_argument(
        "--matricula",
        help="Matrícula do usuário para montar a pasta sincronizada do SharePoint."
    )

    parser.add_argument(
        "--pasta-raiz",
        help="Pasta raiz do SharePoint informada manualmente."
    )

    parser.add_argument(
        "--clean-pdfs",
        action="store_true",
        help="Limpa a pasta de processamento antes de copiar PDFs da origem."
    )

    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove resultados anteriores antes de executar."
    )

    args = parser.parse_args()

    pdf_dir = resolver_destino(
        destino=args.pdf_dir,
        pasta_raiz=args.pasta_raiz,
        matricula=args.matricula,
    )

    if args.origem or args.matricula or args.pasta_raiz:

        origens = resolver_origens(
            origens=args.origem,
            matricula=args.matricula,
            pasta_raiz=args.pasta_raiz,
        )

        copiados = copiar_pdfs_de_origens(
            origens,
            destino=pdf_dir,
            limpar_destino=args.clean_pdfs,
        )

        print(f"{len(copiados)} PDF(s) preparado(s) em {pdf_dir.resolve()}")

    run_pipeline(pdf_dir, clean=args.clean)


if __name__ == "__main__":
    main()
