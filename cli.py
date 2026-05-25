import argparse
from pathlib import Path
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
        help="Diretório contendo PDFs"
    )

    run_cmd.add_argument(
        "--clean",
        action="store_true",
        help="Remove resultados anteriores antes de executar"
    )

    args = parser.parse_args()

    if args.command == "run":

        pdf_dir = Path(args.pdf_dir)

        run_pipeline(pdf_dir, clean=args.clean)


if __name__ == "__main__":
    main()