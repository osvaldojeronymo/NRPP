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
