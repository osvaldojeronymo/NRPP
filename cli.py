import argparse
from pathlib import Path
from BuscadorDePdfs import copiar_pdfs_de_origens, resolver_origens
from orchestrator import run_pipeline


def main():

    parser = argparse.ArgumentParser(
        description="NRPP — Normative-to-Record Preprocessing Pipeline"
    )

    sub = parser.add_subparsers(dest="command")

    run_cmd = sub.add_parser("run", help="Executa o pipeline NRPP")

    run_cmd.add_argument(
        "pdf_dir",
        type=str,
        help="Diretório de processamento contendo PDFs"
    )

    run_cmd.add_argument(
        "--origem",
        nargs="*",
        help="Arquivo(s) PDF ou pasta(s) de origem para buscar PDFs recursivamente antes de executar"
    )

    run_cmd.add_argument(
        "--matricula",
        help="Matrícula do usuário para montar a pasta sincronizada do SharePoint"
    )

    run_cmd.add_argument(
        "--pasta-raiz",
        help="Pasta raiz do SharePoint informada manualmente"
    )

    run_cmd.add_argument(
        "--clean-pdfs",
        action="store_true",
        help="Remove PDFs preparados anteriormente antes de copiar a origem"
    )

    run_cmd.add_argument(
        "--clean",
        action="store_true",
        help="Remove resultados anteriores antes de executar"
    )

    args = parser.parse_args()

    if args.command == "run":

        pdf_dir = Path(args.pdf_dir)

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
