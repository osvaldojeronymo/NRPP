# build_nrpp_safe.sh
#!/bin/bash

echo "======================================"
echo " Construindo pacote NRPP SAFE"
echo "======================================"

BASE_DIR="/home/osvaldo/Área de Trabalho/CAIXA/nrpp"

PACKAGE_NAME="NRPP_AD020_DEMO_SAFE"
PACKAGE_DIR="$BASE_DIR/$PACKAGE_NAME"

echo "Limpando versão anterior..."
rm -rf "$PACKAGE_DIR"
rm -f "$BASE_DIR/$PACKAGE_NAME.zip"

echo "Criando estrutura..."
mkdir -p "$PACKAGE_DIR/pipeline"
mkdir -p "$PACKAGE_DIR/resources"
mkdir -p "$PACKAGE_DIR/pdfs"
mkdir -p "$PACKAGE_DIR/output"

echo "Copiando arquivos principais..."
cp "$BASE_DIR/orchestrator.py" "$PACKAGE_DIR/"
cp "$BASE_DIR/nrpp_pipeline.py" "$PACKAGE_DIR/"
cp "$BASE_DIR/cli.py" "$PACKAGE_DIR/"
cp "$BASE_DIR/requirements.txt" "$PACKAGE_DIR/"

echo "Copiando pipeline..."
cp "$BASE_DIR/pipeline/"*.py "$PACKAGE_DIR/pipeline/"

echo "Copiando glossário..."
cp "$BASE_DIR/resources/glossario_canonico.json" "$PACKAGE_DIR/resources/"

echo "Copiando PDFs..."
cp "$BASE_DIR/pdfs/"*.pdf "$PACKAGE_DIR/pdfs/" 2>/dev/null

echo "Criando README..."

cat << 'EOF' > "$PACKAGE_DIR/README_EXECUCAO.txt"

NRPP – Normative-to-Record Preprocessing Pipeline
Demonstração Técnica – CAIXA

EXECUÇÃO DO PIPELINE

1. Instalar Python 3.9 ou superior

2. Instalar dependências

pip install -r requirements.txt

3. Executar o pipeline

python orchestrator.py pdfs

4. Os resultados serão gerados na pasta

output/

Etapas do pipeline:

A1 – Extração de texto de PDFs
A2 – Segmentação normativa
A3 – Construção de registros
A4 – Normalização semântica via glossário
A5 – Exportação estruturada

EOF

echo "Gerando ZIP..."

cd "$BASE_DIR"
zip -r "$PACKAGE_NAME.zip" "$PACKAGE_NAME"

echo ""
echo "Pacote SAFE criado:"
echo "$BASE_DIR/$PACKAGE_NAME.zip"