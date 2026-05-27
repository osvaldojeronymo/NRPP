# Dossie didatico A1-A5 - AD020122

Este diretorio organiza, em ordem didatica, os produtos gerados a partir de
`AD020122.pdf`. A ideia e permitir que o usuario abra o PDF original e compare,
passo a passo, como o texto normativo foi extraido, segmentado, enriquecido e
consolidado para validacao humana.

## Arquivos

| Etapa | Arquivo | O que observar |
|---|---|---|
| PDF | `00_pdf_original_AD020122.pdf` | Documento de referencia para comparacao visual. |
| A1 | `A1_texto_extraido_normalizado.txt` | Texto extraido do PDF, com remocao conservadora de artefatos editoriais. |
| A2 | `A2_segmentacao_estrutura_normativa.csv` | Itens normativos identificados por numeracao hierarquica. |
| A3 | `A3_pistas_semanticas_detectadas.csv` | Termos e pistas semanticas detectados em cada segmento. |
| A4 | `A4_termos_normalizados_metadados_isdf.csv` | Termos normalizados pelo glossario e enriquecidos com metadados ISDF. |
| A5 | `A5_planilha_validacao_humana.xlsx` | Planilha final para revisao humana, com abas analiticas. |

## Como usar em aula ou validacao

1. Abra `00_pdf_original_AD020122.pdf`.
2. Abra `A1_texto_extraido_normalizado.txt` ao lado do PDF e compare as
   primeiras paginas. Nesta etapa ainda podem aparecer sumario, quebras de
   pagina e residuos de extracao.
3. Abra `A2_segmentacao_estrutura_normativa.csv` e verifique como a numeracao
   da norma virou segmentos (`id` + `texto`).
4. Abra `A3_pistas_semanticas_detectadas.csv` e observe que um mesmo segmento
   pode gerar varias evidencias, por exemplo documento, processo, legislacao,
   entidade coletiva ou relacionamento.
5. Abra `A4_termos_normalizados_metadados_isdf.csv` e compare `termo` com
   `termo_norm`, `isdf_area`, `isdf_elemento` e `necessita_validacao`.
6. Abra `A5_planilha_validacao_humana.xlsx` para a visao consolidada que o
   pesquisador deve revisar.

## Leituras importantes

- A1 nao interpreta a norma; apenas extrai e normaliza texto de forma
  conservadora.
- A2 depende da qualidade do texto extraido. Se o sumario ou cabecalhos ficarem
  no texto, eles tambem podem virar segmentos.
- A3 detecta pistas por padroes lexicais. Portanto, evidencia nao significa
  decisao final.
- A4 aproxima os termos detectados do vocabulario controlado e dos elementos
  ISDF, mas marca casos que exigem validacao.
- A5 e o produto de trabalho humano: organiza as evidencias para conferencia,
  correcao e enriquecimento.

## Estatisticas deste processamento

- Segmentos A2: 684
- Evidencias A3: 663
- Linhas normalizadas A4: 663
- Abas na planilha A5:
  `validacao_nrpp`, `evidencias_normalizadas`, `descricao_isdf`,
  `relacionamentos_isdf`, `controle_descricao`, `evidencias_semanticas`,
  `segmentos_texto`, `termos_fora_do_glossario`.
