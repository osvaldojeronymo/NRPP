
# NRPP – Dossiê de processamento normativo

Arquivo analisado: AD020122.pdf

Este diretório contém os resultados produzidos pelo NRPP
(Normative-to-Record Preprocessing Pipeline).

## EXTRACAO_TEXTO
Texto bruto extraído do PDF.

## INTERMEDIARIOS
Arquivos intermediários do pipeline:
- segmentos_texto.csv
- evidencias_semanticas.csv
- evidencias_normalizadas.csv, com normalização terminológica e metadados ISDF

## AUDITORIA_PIPELINE
termos_fora_do_glossario.csv
Termos detectados no texto que não possuem correspondência no glossário.

## PRODUTO_FINAL
tabela_validacao_nrpp.xlsx
Tabela analítica para validação humana, incluindo abas de descrição e
relacionamentos ISDF.
