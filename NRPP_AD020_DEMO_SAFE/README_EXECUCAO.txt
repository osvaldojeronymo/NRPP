
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

