#!/bin/bash
set -e
echo "======================================"
echo " Construindo pacote NRPP DEMO"
echo "======================================"

# diretório base
BASE_DIR="/home/osvaldo/Área de Trabalho/CAIXA/nrpp"

# pasta do pacote
PACKAGE_NAME="NRPP_AD020_DEMO"
PACKAGE_DIR="$BASE_DIR/$PACKAGE_NAME"

# remove pacote anterior
echo "Limpando versão anterior..."
rm -rf "$PACKAGE_DIR"
rm -f "$BASE_DIR/$PACKAGE_NAME.zip"

# cria estrutura
echo "Criando estrutura..."
mkdir -p "$PACKAGE_DIR/pipeline"
mkdir -p "$PACKAGE_DIR/resources"
mkdir -p "$PACKAGE_DIR/pdfs"
mkdir -p "$PACKAGE_DIR/output"

# copia arquivos principais
echo "Copiando arquivos principais..."
cp "$BASE_DIR/orchestrator.py" "$PACKAGE_DIR/"
cp "$BASE_DIR/nrpp_pipeline.py" "$PACKAGE_DIR/"
cp "$BASE_DIR/cli.py" "$PACKAGE_DIR/"
cp "$BASE_DIR/requirements.txt" "$PACKAGE_DIR/"

# copia pipeline
echo "Copiando módulos do pipeline..."
cp "$BASE_DIR/pipeline/"*.py "$PACKAGE_DIR/pipeline/"

# copia glossário
echo "Copiando glossário..."
cp "$BASE_DIR/resources/glossario_canonico.json" "$PACKAGE_DIR/resources/"

# copia PDFs de teste
echo "Copiando PDFs..."
cp "$BASE_DIR/pdfs/"*.pdf "$PACKAGE_DIR/pdfs/" 2>/dev/null

# cria script de execução
echo "Criando script run_demo.sh..."

cat << 'EOF' > "$PACKAGE_DIR/run_demo.sh"
#!/bin/bash

echo "======================================"
echo " NRPP – DEMONSTRAÇÃO"
echo "======================================"

echo "Instalando dependências..."
pip install -r requirements.txt

echo ""
echo "Executando pipeline..."
python orchestrator.py pdfs/

echo ""
echo "Processamento concluído."
echo "Resultados na pasta output/"
EOF

chmod +x "$PACKAGE_DIR/run_demo.sh"

# cria README
echo "Criando README..."

cat << 'EOF' > "$PACKAGE_DIR/README.txt"

NRPP – Normative-to-Record Preprocessing Pipeline
Demonstração Técnica – CAIXA

Este pacote demonstra a transformação de normas PDF
em registros estruturados arquivísticos.

Etapas do pipeline:

A1 – Extração de texto do PDF
A2 – Segmentação normativa
A3 – Construção de registros
A4 – Normalização semântica via glossário
A5 – Exportação estruturada

Para executar a demonstração:

1) Instalar Python 3.9+
2) Executar:

bash run_demo.sh

Os resultados serão gerados na pasta:

output/

EOF

cat << 'EOF' > "$PACKAGE_DIR/run_demo.bat"
@echo off

echo ======================================
echo NRPP - DEMONSTRACAO CAIXA
echo ======================================

python --version
IF %ERRORLEVEL% NEQ 0 (
    echo Python nao encontrado.
    pause
    exit
)

pip install -r requirements.txt

python orchestrator.py pdfs

echo.
echo Processamento concluido.
echo Veja os resultados na pasta output.

pause
EOF


# cria zip
echo "Gerando ZIP..."

cd "$BASE_DIR"
zip -r "$PACKAGE_NAME.zip" "$PACKAGE_NAME"

echo ""
echo "======================================"
echo " Pacote criado com sucesso"
echo "======================================"

echo "Arquivo:"
echo "$BASE_DIR/$PACKAGE_NAME.zip"
