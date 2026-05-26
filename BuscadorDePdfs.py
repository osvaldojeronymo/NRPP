from pathlib import Path
from datetime import datetime
import csv
import hashlib
import os
import shutil
import sqlite3


PASTAS_IGNORADAS = {"NRPP_RESULTADOS", "__pycache__"}
PASTA_SHAREPOINT_RELATIVA = (
    Path("Caixa Economica Federal") / "O365GRP-Projects - NRPP"
)
PASTA_SCRIPTS = "scripts"
PASTA_PDFS = "pdfs"
BANCO_SQLITE = "controle_pdfs.db"
CSV_LOG = "processamento_pdfs.csv"
EXCEL_RELATORIO = "relatorio_processamento.xlsx"
CHECKPOINT_FILE = "checkpoint.txt"


def montar_pasta_sharepoint(matricula: str | None = None) -> Path:
    """
    Monta a pasta raiz sincronizada do SharePoint a partir da matrícula.

    Exemplo no Windows:
    C:/Users/c088576/Caixa Economica Federal/O365GRP-Projects - NRPP
    """

    if matricula is None:
        matricula = os.environ.get("USERNAME") or os.environ.get("USER")

    if not matricula:
        raise ValueError(
            "Informe a matrícula do usuário ou configure a variável USERNAME."
        )

    return Path("C:/Users") / matricula / PASTA_SHAREPOINT_RELATIVA


def resolver_origens(
    origens: list[str] | None = None,
    matricula: str | None = None,
    pasta_raiz: str | Path | None = None,
) -> list[Path]:
    """
    Resolve as pastas/arquivos de origem.
    Prioridade:
    1. pasta_raiz informada diretamente;
    2. origens informadas no comando;
    3. pasta SharePoint montada pela matrícula.
    """

    if pasta_raiz:
        return [Path(pasta_raiz).expanduser()]

    if origens:
        return [Path(origem).expanduser() for origem in origens]

    return [montar_pasta_sharepoint(matricula)]


def resolver_destino(
    destino: str | Path | None = None,
    pasta_raiz: str | Path | None = None,
    matricula: str | None = None,
) -> Path:
    """
    Resolve a pasta central onde o pipeline NRPP lê os PDFs.
    Se uma pasta raiz SharePoint ou matrícula for informada, usa:
    PASTA_RAIZ/scripts/pdfs.
    Caso contrário, usa a pasta local pdfs.
    """

    if destino:
        return Path(destino).expanduser()

    if pasta_raiz:
        return Path(pasta_raiz).expanduser() / PASTA_SCRIPTS / PASTA_PDFS

    if matricula:
        return montar_pasta_sharepoint(matricula) / PASTA_SCRIPTS / PASTA_PDFS

    return Path(PASTA_PDFS)


def _deve_ignorar(caminho: Path) -> bool:
    return any(parte in PASTAS_IGNORADAS or parte == PASTA_SCRIPTS for parte in caminho.parts)


def calcular_hash(arquivo: str | Path) -> str:
    sha256 = hashlib.sha256()

    with open(arquivo, "rb") as f:
        for bloco in iter(lambda: f.read(4096), b""):
            sha256.update(bloco)

    return sha256.hexdigest()


def conectar_banco(caminho_banco: str | Path):
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS arquivos_processados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_arquivo TEXT,
        caminho_origem TEXT,
        caminho_destino TEXT,
        hash_arquivo TEXT UNIQUE,
        data_processamento TEXT
    )
    """)

    conn.commit()

    return conn


def arquivo_ja_processado(conn, hash_arquivo: str) -> bool:
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1
        FROM arquivos_processados
        WHERE hash_arquivo = ?
    """, (hash_arquivo,))

    return cursor.fetchone() is not None


def registrar_arquivo(conn, nome, origem, destino, hash_arquivo):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO arquivos_processados (
            nome_arquivo,
            caminho_origem,
            caminho_destino,
            hash_arquivo,
            data_processamento
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        nome,
        str(origem),
        str(destino),
        hash_arquivo,
        datetime.now().isoformat()
    ))

    conn.commit()


def registrar_csv(csv_log, nome, origem, destino, hash_arquivo, status):
    csv_log = Path(csv_log)
    arquivo_existe = csv_log.exists()

    csv_log.parent.mkdir(parents=True, exist_ok=True)

    with open(csv_log, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        if not arquivo_existe:
            writer.writerow([
                "data",
                "arquivo",
                "origem",
                "destino",
                "hash",
                "status"
            ])

        writer.writerow([
            datetime.now().isoformat(),
            nome,
            str(origem),
            str(destino),
            hash_arquivo,
            status
        ])


def atualizar_checkpoint(checkpoint_file, arquivo):
    checkpoint_file = Path(checkpoint_file)
    checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
    checkpoint_file.write_text(str(arquivo), encoding="utf-8")


def gerar_relatorio_excel(excel_relatorio, processados, ignorados, erros):
    import pandas as pd

    excel_relatorio = Path(excel_relatorio)
    excel_relatorio.parent.mkdir(parents=True, exist_ok=True)

    df_processados = pd.DataFrame({"processados": processados})
    df_ignorados = pd.DataFrame({"ignorados": ignorados})
    df_erros = pd.DataFrame(erros)

    with pd.ExcelWriter(excel_relatorio) as writer:
        df_processados.to_excel(writer, sheet_name="processados", index=False)
        df_ignorados.to_excel(writer, sheet_name="ignorados", index=False)
        df_erros.to_excel(writer, sheet_name="erros", index=False)


def buscar_pdfs(origem: str | Path) -> list[Path]:
    """
    Busca PDFs em uma pasta e em todas as suas subpastas.
    Se a origem for um PDF, retorna apenas esse arquivo.
    """

    origem = Path(origem).expanduser().resolve()

    if not origem.exists():
        raise FileNotFoundError(f"Origem não encontrada: {origem}")

    if origem.is_file():
        if origem.suffix.lower() != ".pdf":
            raise ValueError(f"O arquivo informado não é PDF: {origem}")
        return [origem]

    return sorted(
        pdf
        for pdf in origem.rglob("*")
        if pdf.is_file()
        and pdf.suffix.lower() == ".pdf"
        and not _deve_ignorar(pdf.relative_to(origem))
    )


def copiar_pdfs_para_processamento(
    origem: str | Path,
    destino: str | Path = "pdfs",
    limpar_destino: bool = False,
    conn=None,
    csv_log: str | Path | None = None,
    checkpoint_file: str | Path | None = None,
    processados: list[str] | None = None,
    ignorados: list[str] | None = None,
    erros: list[dict] | None = None,
) -> list[Path]:
    """
    Copia PDFs encontrados em origem para destino mantendo a organização
    relativa de pastas.
    """

    origem = Path(origem).expanduser().resolve()
    destino = Path(destino).expanduser().resolve()

    if limpar_destino and (origem == destino or destino in origem.parents):
        raise ValueError(
            "Não é seguro limpar o destino quando a origem está dentro dele."
        )

    if origem.is_dir():
        pdfs = [
            pdf
            for pdf in buscar_pdfs(origem)
            if not (pdf == destino or destino in pdf.parents)
        ]
    else:
        pdfs = buscar_pdfs(origem)

    if limpar_destino and destino.exists():
        shutil.rmtree(destino)

    destino.mkdir(parents=True, exist_ok=True)

    copiados = []

    for pdf in pdfs:
        try:
            if origem.is_file():
                relativo = Path(pdf.name)
            else:
                relativo = pdf.relative_to(origem)

            destino_pdf = destino / relativo

            if pdf.resolve() == destino_pdf.resolve():
                copiados.append(destino_pdf)
                if processados is not None:
                    processados.append(str(pdf))
                continue

            hash_arquivo = calcular_hash(pdf)

            if conn is not None and arquivo_ja_processado(conn, hash_arquivo):
                print("[IGNORADO] DUPLICADO")
                print(f"Arquivo: {pdf}")

                if ignorados is not None:
                    ignorados.append(str(pdf))

                if csv_log:
                    registrar_csv(
                        csv_log,
                        pdf.name,
                        pdf,
                        destino_pdf,
                        hash_arquivo,
                        "IGNORADO_DUPLICADO",
                    )

                continue

            print("\n[ENCONTRADO]")
            print(f"Arquivo: {pdf}")
            print(f"Destino: {destino_pdf}")

            destino_pdf.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(pdf, destino_pdf)

            print("[COPIADO]")

            if conn is not None:
                registrar_arquivo(
                    conn,
                    nome=pdf.name,
                    origem=pdf,
                    destino=destino_pdf,
                    hash_arquivo=hash_arquivo,
                )

            if csv_log:
                registrar_csv(
                    csv_log,
                    pdf.name,
                    pdf,
                    destino_pdf,
                    hash_arquivo,
                    "COPIADO",
                )

            if checkpoint_file:
                atualizar_checkpoint(checkpoint_file, pdf)

            if processados is not None:
                processados.append(str(pdf))

            copiados.append(destino_pdf)

        except Exception as e:
            print(f"[ERRO] {pdf}")
            print(e)

            if erros is not None:
                erros.append({
                    "arquivo": str(pdf),
                    "erro": str(e)
                })

            if csv_log:
                registrar_csv(
                    csv_log,
                    pdf.name,
                    pdf,
                    destino / pdf.name,
                    "",
                    "ERRO",
                )

    return copiados


def copiar_pdfs_de_origens(
    origens: list[str | Path],
    destino: str | Path = "pdfs",
    limpar_destino: bool = False,
    banco_sqlite: str | Path | None = BANCO_SQLITE,
    csv_log: str | Path | None = CSV_LOG,
    excel_relatorio: str | Path | None = EXCEL_RELATORIO,
    checkpoint_file: str | Path | None = CHECKPOINT_FILE,
) -> list[Path]:
    """
    Copia PDFs de uma ou mais origens para a pasta de processamento.
    Quando há mais de uma pasta de origem, cada uma ganha uma subpasta
    com o nome da origem para evitar colisões de nomes.
    """

    destino = Path(destino).expanduser().resolve()

    if limpar_destino and destino.exists():
        shutil.rmtree(destino)

    destino.mkdir(parents=True, exist_ok=True)

    copiados = []
    processados = []
    ignorados = []
    erros = []
    varias_origens = len(origens) > 1
    conn = conectar_banco(banco_sqlite) if banco_sqlite else None

    print("\n===================================")
    print("INICIANDO PROCESSAMENTO")
    print("===================================\n")

    try:
        for origem in origens:
            origem = Path(origem).expanduser().resolve()
            destino_origem = destino / origem.name if varias_origens and origem.is_dir() else destino

            copiados.extend(
                copiar_pdfs_para_processamento(
                    origem,
                    destino=destino_origem,
                    limpar_destino=False,
                    conn=conn,
                    csv_log=csv_log,
                    checkpoint_file=checkpoint_file,
                    processados=processados,
                    ignorados=ignorados,
                    erros=erros,
                )
            )
    finally:
        if conn is not None:
            conn.close()

    if excel_relatorio:
        gerar_relatorio_excel(
            excel_relatorio,
            processados=processados,
            ignorados=ignorados,
            erros=erros,
        )

    print("\n===================================")
    print("PROCESSAMENTO FINALIZADO")
    print("===================================")
    print(f"Processados: {len(processados)}")
    print(f"Ignorados: {len(ignorados)}")
    print(f"Erros: {len(erros)}")

    return copiados


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Busca PDFs recursivamente e copia para a pasta de processamento."
    )
    parser.add_argument(
        "origem",
        nargs="*",
        help="Arquivo PDF ou pasta onde os PDFs serão buscados recursivamente.",
    )
    parser.add_argument(
        "--matricula",
        help="Matrícula do usuário para montar a pasta sincronizada do SharePoint.",
    )
    parser.add_argument(
        "--pasta-raiz",
        help=(
            "Pasta raiz do SharePoint informada manualmente. "
            "Ex.: C:/Users/c088576/Caixa Economica Federal/O365GRP-Projects - NRPP"
        ),
    )
    parser.add_argument(
        "--destino",
        help=(
            "Pasta onde os PDFs serão copiados. "
            "Se omitida com --matricula ou --pasta-raiz, usa PASTA_RAIZ/scripts/pdfs. "
            "Caso contrário, usa pdfs."
        ),
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Limpa a pasta de destino antes de copiar os PDFs.",
    )
    parser.add_argument(
        "--banco-sqlite",
        default=BANCO_SQLITE,
        help=f"Banco SQLite de controle. Padrão: {BANCO_SQLITE}",
    )
    parser.add_argument(
        "--csv-log",
        default=CSV_LOG,
        help=f"Arquivo CSV de log. Padrão: {CSV_LOG}",
    )
    parser.add_argument(
        "--excel-relatorio",
        default=EXCEL_RELATORIO,
        help=f"Relatório Excel. Padrão: {EXCEL_RELATORIO}",
    )
    parser.add_argument(
        "--checkpoint",
        default=CHECKPOINT_FILE,
        help=f"Arquivo de checkpoint. Padrão: {CHECKPOINT_FILE}",
    )

    args = parser.parse_args()

    origens = resolver_origens(
        origens=args.origem,
        matricula=args.matricula,
        pasta_raiz=args.pasta_raiz,
    )
    destino = resolver_destino(
        destino=args.destino,
        pasta_raiz=args.pasta_raiz,
        matricula=args.matricula,
    )

    copiados = copiar_pdfs_de_origens(
        origens,
        destino=destino,
        limpar_destino=args.clean,
        banco_sqlite=args.banco_sqlite,
        csv_log=args.csv_log,
        excel_relatorio=args.excel_relatorio,
        checkpoint_file=args.checkpoint,
    )

    print(f"{len(copiados)} PDF(s) preparado(s) em {destino.resolve()}")

    for pdf in copiados:
        print(pdf)


if __name__ == "__main__":
    main()
