# a2_structural_segmentation.py

import re
import sys
import csv
from pathlib import Path


def segment_text(input_path: str | Path, output_csv: str | Path):
    """
    A2 — Segmentação estrutural do documento normativo.

    Identifica unidades hierárquicas do tipo:

    1 Texto
    1.1 Texto
    1.1.1 Texto

    Cada unidade se torna um segmento.
    """

    input_path = Path(input_path)
    output_csv = Path(output_csv)

    print(f"\n[A2] Segmentando estrutura: {input_path.name}")

    lines = input_path.read_text(encoding="utf-8").splitlines()

    segments = []
    current_id = None
    current_text = []

    # Padrão hierárquico
    pattern = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.*)")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        match = pattern.match(line)

        if match:

            # salva segmento anterior
            if current_id:
                segments.append(
                    (current_id, " ".join(current_text).strip())
                )

            current_id = match.group(1)
            current_text = [match.group(2)]

        else:

            if current_id:
                current_text.append(line)

    # salva último segmento
    if current_id:
        segments.append(
            (current_id, " ".join(current_text).strip())
        )

    # cria diretório
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    # grava CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:

        writer = csv.writer(csvfile, delimiter=";")

        writer.writerow(["id", "texto"])

        for seg in segments:
            writer.writerow(seg)

    print(f"[A2] Segmentos identificados: {len(segments)}")
    print(f"[A2] Arquivo gerado: {output_csv}\n")

def run(input_txt: str | Path):
    """
    Interface padrão do pipeline NRPP.
    Recebe arquivo txt e gera CSV de segmentos.
    """

    input_txt = Path(input_txt)

    output_csv = input_txt.parent / f"{input_txt.stem}_segments.csv"

    segment_text(input_txt, output_csv)

    return output_csv

if __name__ == "__main__":

    if len(sys.argv) != 3:

        print("Uso:")
        print("python a2_structural_segmentation.py input.txt output.csv")
        sys.exit(1)

    segment_text(sys.argv[1], sys.argv[2])