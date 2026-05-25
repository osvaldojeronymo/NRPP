# a1_text_normalization.py

import re
import sys
from pathlib import Path
from pdfminer.high_level import extract_text


def normalize_text(text: str) -> str:
    """
    A1 — Normalização conservadora do texto normativo

    Objetivo:
    - Remover artefatos editoriais comuns
    - Preservar hierarquia normativa
    - Manter rastreabilidade do conteúdo

    Esta etapa NÃO altera estrutura lógica do documento.
    """

    lines = text.splitlines()
    cleaned = []

    for line in lines:
        line = line.rstrip()

        # Remove padrões editoriais específicos
        if re.match(r"^Vigência:\s*\d{2}/\d{2}/\d{4}$", line):
            continue

        if re.match(r"^#PUBLICO$", line):
            continue

        if re.match(r"^\d+\s*/\s*\d+\s*#PUBLICO$", line):
            continue

        if re.match(r"^AD\s*\d{3}\s*\d+$", line):
            continue

        cleaned.append(line)

    # Remove linhas vazias duplicadas
    normalized = []
    previous_blank = False

    for line in cleaned:

        if line.strip() == "":
            if not previous_blank:
                normalized.append("")
            previous_blank = True

        else:
            normalized.append(line)
            previous_blank = False

    return "\n".join(normalized)


def run(pdf_path: str | Path, output_path: str | Path, page_start=None, page_end=None):
    """
    Executa a etapa A1 do pipeline.

    Parâmetros
    ----------
    pdf_path : caminho do PDF de entrada
    output_path : caminho do arquivo TXT de saída
    page_start : página inicial (opcional)
    page_end : página final (opcional)
    """

    pdf_path = Path(pdf_path)
    output_path = Path(output_path)

    print(f"\n[A1] Extraindo texto de: {pdf_path.name}")

    if page_start and page_end:
        pages = range(page_start - 1, page_end)
    else:
        pages = None

    text = extract_text(pdf_path, page_numbers=pages)

    normalized = normalize_text(text)

    # Cria diretório se necessário
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(normalized, encoding="utf-8")

    print(f"[A1] Linhas originais: {len(text.splitlines())}")
    print(f"[A1] Linhas normalizadas: {len(normalized.splitlines())}")
    print(f"[A1] Arquivo gerado: {output_path}\n")

def run_pipeline(pdf_path: str | Path):
    """
    Interface simplificada usada pelo orchestrator.
    """

    pdf_path = Path(pdf_path)

    output_txt = pdf_path.parent / f"{pdf_path.stem}.txt"

    run(pdf_path, output_txt)

    return output_txt

# Execução direta via terminal
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Uso:")
        print("python a1_text_normalization.py input.pdf output.txt [page_start] [page_end]")
        sys.exit(1)

    pdf = sys.argv[1]
    out = sys.argv[2]

    start = int(sys.argv[3]) if len(sys.argv) > 3 else None
    end = int(sys.argv[4]) if len(sys.argv) > 4 else None

    run(pdf, out, start, end)