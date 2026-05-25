# nrpp_pipeline.py

import argparse
from nrpp.orchestrator import run_pipeline, run_folder


def main():

    parser = argparse.ArgumentParser(
        description="NRPP - Normative to Record Preprocessing Pipeline"
    )

    parser.add_argument(
        "input",
        help="PDF ou pasta contendo PDFs"
    )

    parser.add_argument(
        "--output",
        default="runs",
        help="Diretório de saída"
    )

    parser.add_argument(
        "--start",
        default="A1",
        help="Estágio inicial (A1–A5)"
    )

    args = parser.parse_args()

    import os

    if os.path.isdir(args.input):
        run_folder(args.input, args.output, args.start)

    else:
        run_pipeline(args.input, args.output, args.start)


if __name__ == "__main__":
    main()