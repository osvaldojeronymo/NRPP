# Lições Aprendidas

## Mudança de perspectiva do NRPP com a incorporação da ISDF

Este documento registra as principais lições aprendidas na evolução do Normative-to-Record Preprocessing Pipeline (NRPP), especialmente na passagem de uma abordagem centrada na identificação de evidências documentais para uma abordagem orientada pela Norma Internacional para Descrição de Funções (ISDF).

O objetivo é explicitar o que mudou, o que permaneceu válido e quais cuidados devem orientar as próximas evoluções metodológicas e técnicas do pipeline.

## 1 Perspectiva original

Na primeira versão operacional, o NRPP foi concebido como um pipeline de apoio à extração estruturada de informações a partir de normativos institucionais.

A preocupação principal era identificar, nos textos normativos:

- documentos explicitamente mencionados;
- artefatos informacionais requeridos;
- ações normativas que sugerissem produção, uso ou guarda de registros;
- segmentos textuais relevantes para posterior validação humana.

Essa abordagem era adequada para iniciar a organização de evidências documentais, pois reduzia a complexidade dos normativos e produzia uma planilha de validação baseada em trechos rastreáveis.

Entretanto, a perspectiva original ainda tratava os documentos como o principal ponto de chegada da análise. A função institucional aparecia de forma indireta, como contexto do documento ou do processo.

## 2 Limite identificado

A leitura orientada apenas por documentos revelou um limite metodológico importante: a produção documental não pode ser compreendida de forma suficiente quando separada das funções institucionais que a originam.

Nos normativos da CAIXA, muitos registros não aparecem apenas como documentos isolados. Eles estão associados a:

- responsabilidades de unidades organizacionais;
- competências formais;
- atividades e tarefas;
- procedimentos de controle;
- bases legais;
- sistemas de informação;
- relações entre áreas, processos e recursos arquivísticos.

Assim, uma evidência documental extraída automaticamente só ganha significado arquivístico mais robusto quando situada no contexto funcional que explica sua produção, uso e manutenção.

## 3 Contribuição da ISDF

A ISDF desloca o foco metodológico para a descrição de funções de entidades coletivas associadas à produção e manutenção de arquivos.

Essa mudança é relevante para o NRPP porque permite organizar as evidências extraídas dos normativos em torno de elementos como:

- tipo funcional: função, subfunção, atividade, tarefa ou transação;
- forma de descrição da função;
- datas e períodos de vigência;
- base legal;
- relacionamentos entre funções;
- relacionamentos entre funções, entidades coletivas e recursos arquivísticos;
- controle da descrição produzida.

Com isso, o NRPP deixa de ser apenas um pre-processador de documentos citados e passa a ser um instrumento de preparação de descrições funcionais validáveis.

## 4 Comparação entre as duas abordagens

| Aspecto                   | Perspectiva original                                 | Perspectiva com ISDF                                                                         |
| ------------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Foco principal            | Evidências documentais em normativos                 | Funções institucionais e seus relacionamentos                                                |
| Pergunta orientadora      | Que documentos ou artefatos aparecem na norma?       | Que função, atividade ou responsabilidade explica a produção e manutenção desses documentos? |
| Produto esperado          | Planilha de evidências para validação                | Planilha de validação com abas de descrição funcional ISDF                                   |
| Papel do glossário        | Normalizar termos documentais                        | Apoiar a normalização terminológica dentro de uma estrutura descritiva                       |
| Papel da validação humana | Confirmar evidências extraídas                       | Validar evidências, relações funcionais e enquadramento ISDF                                 |
| Limite principal          | Risco de tratar documento fora do contexto funcional | Requer maior cuidado interpretativo e validação especializada                                |

### 4.1 Comparação empírica com o PDF AD020122

Para tornar a diferença entre as versões mais visível, foi executado um teste comparativo com o arquivo `AD020122.pdf`.

A versão v1 corresponde ao estado do NRPP antes da incorporação da ISDF. A versão v2 corresponde ao NRPP com detecção ampliada no A3, enriquecimento ISDF no A4 e novas abas de validação no A5.

| Critério observado                         |             NRPP v1 |                                                      NRPP v2 orientado pela ISDF | Leitura da diferença                                                                                                          |
| ------------------------------------------ | ------------------: | -------------------------------------------------------------------------------: | ----------------------------------------------------------------------------------------------------------------------------- |
| Segmentos textuais A2                      |                 684 |                                                                              684 | A segmentação estrutural permaneceu estável; a mudança ocorreu nas etapas semânticas e de estruturação.                       |
| Evidências semânticas A3                   |                 350 |                                                                              663 | A v2 ampliou a detecção de pistas, incluindo função, entidade coletiva, legislação, datas e relacionamentos.                  |
| Classes detectadas no A3                   | documento; processo | documento; processo; função; entidade coletiva; legislação; data; relacionamento | A v1 separava basicamente documentos e processos; a v2 aproxima a leitura do modelo funcional da ISDF.                        |
| Linhas preservadas no A4                   |                  28 |                                                                              663 | A v1 mantinha apenas evidências normalizadas pelo glossário; a v2 preserva todas as evidências e marca o que exige validação. |
| Termos normalizados por glossário          |                  28 |                                                                               60 | A v2 aumentou a cobertura terminológica, mas seu principal ganho é preservar também evidências ainda não normalizadas.        |
| Evidências classificadas com elemento ISDF |       não aplicável |                                                                              663 | Todas as evidências da v2 recebem enquadramento preliminar em área ou elemento ISDF.                                          |
| Itens marcados como `necessita_validacao`  |       não aplicável |                                                                              603 | A v2 explicita o que precisa de revisão humana, reduzindo o risco de falsa decisão automática.                                |
| Linhas na aba `validacao_nrpp`             |                  28 |                                                                              408 | A planilha final deixa de ser um recorte restrito aos termos normalizados e passa a apoiar revisão funcional mais ampla.      |
| Abas do Excel final                        |                   5 |                                                                                8 | A v2 acrescenta `descricao_isdf`, `relacionamentos_isdf` e `controle_descricao`.                                              |
| Cópia do PDF original no dossiê            |                 sim |                                                                              não | A v2 elimina a pasta `ENTRADA/`, evitando duplicação desnecessária do PDF original.                                           |

Distribuição das classes detectadas no A3 para o arquivo `AD020122.pdf`:

| Classe            | NRPP v1 | NRPP v2 orientado pela ISDF |
| ----------------- | ------: | --------------------------: |
| processo          |     248 |                         272 |
| documento         |     102 |                         219 |
| entidade coletiva |       0 |                          71 |
| legislação        |       0 |                          41 |
| relacionamento    |       0 |                          34 |
| função            |       0 |                          13 |
| data              |       0 |                          13 |

Essa comparação mostra que a v2 não é apenas uma versão com mais colunas. Ela altera a finalidade do produto: a saída deixa de ser uma lista reduzida de documentos normalizados e passa a ser uma matriz de evidências para validação funcional e arquivística.

## 5 O que permaneceu válido

A mudança de perspectiva não invalida a versão inicial do NRPP. Ao contrário, vários princípios continuam corretos:

- preservação do texto de origem e dos segmentos normativos;
- separação entre processamento automatizado e decisão arquivística;
- rastreabilidade entre evidência extraída e trecho normativo;
- geração de artefatos intermediários auditáveis;
- necessidade de validação humana;
- uso de glossários e vocabulários controlados;
- execução reprodutível em ambiente local.

A principal mudança está na interpretação do produto final. Antes, a planilha era vista como um inventário preliminar de evidências documentais. Agora, ela deve ser vista como uma base de apoio para descrição funcional e análise arquivística orientada pela ISDF.

## 6 Aprendizados técnicos

A evolução do pipeline mostrou que uma única etapa não deve concentrar toda a inteligência metodológica.

O desenho mais adequado é distribuir responsabilidades:

- A1 extrai e normaliza o texto;
- A2 segmenta a estrutura normativa;
- A3 detecta pistas semânticas;
- A4 normaliza termos e acrescenta metadados ISDF;
- A5 consolida resultados em planilhas de validação humana.

Essa separação permite evoluir cada etapa sem comprometer o conjunto. Também facilita auditoria, testes e manutenção.

## 7 Aprendizados sobre o A4

A ideia inicial era melhorar o A4 com as diretrizes da ISDF. A conclusão foi que isso é correto, desde que o A4 não seja transformado em uma etapa decisória.

O A4 deve:

- normalizar termos detectados pelo A3;
- consultar glossários e diretrizes estruturadas;
- atribuir campos ISDF preliminares;
- indicar itens que exigem validação;
- produzir uma trilha de auditoria para termos fora do glossário.

O A4 não deve:

- declarar de forma definitiva que uma função está descrita corretamente;
- substituir a análise arquivística;
- inferir sozinho relações institucionais complexas;
- decidir classificação, temporalidade ou destinação documental.

## 8 Aprendizados sobre o produto final

O produto final não deve ser uma única tabela plana. A incorporação da ISDF exige uma saída mais rica, com abas separadas para diferentes necessidades de revisão.

A estrutura atual do Excel final é mais adequada porque inclui:

- `validacao_nrpp`: visão consolidada para revisão humana;
- `evidencias_normalizadas`: saída completa do A4;
- `descricao_isdf`: agrupamento dos elementos ISDF detectados;
- `relacionamentos_isdf`: relações entre documentos, entidades coletivas e funções;
- `controle_descricao`: campos de controle inspirados na área de controle da ISDF;
- `evidencias_semanticas`: saída do A3;
- `segmentos_texto`: saída do A2;
- `termos_fora_do_glossario`: trilha de auditoria terminológica.

## 9 Risco de falsa precisão

Um dos principais riscos da nova abordagem é a aparência de precisão excessiva. Como a ISDF possui uma estrutura normativa formal, há risco de o usuário interpretar campos preenchidos automaticamente como descrições arquivísticas finalizadas.

Para mitigar esse risco, o NRPP deve manter linguagem clara de apoio à validação:

- resultados são preliminares;
- campos ISDF são sugestões estruturadas;
- itens marcados como `necessita_validacao` exigem revisão humana;
- decisões arquivísticas permanecem sob responsabilidade profissional.

## 10 Importância da rastreabilidade

A incorporação da ISDF aumenta a necessidade de rastreabilidade. Cada classificação ou sugestão deve permanecer vinculada ao trecho normativo que a originou.

Isso é essencial porque a validação humana precisa responder a perguntas como:

- qual trecho normativo sustenta esta evidência?
- qual termo foi detectado automaticamente?
- qual classe foi atribuída?
- qual elemento ISDF foi sugerido?
- o termo foi normalizado por glossário ou apenas transportado para validação?

Sem essa rastreabilidade, a automação se torna pouco confiável para uso institucional.

## 11 Impacto sobre a validação humana

A validação humana deixa de ser apenas uma revisão de documentos detectados e passa a incluir verificação funcional.

O validador deve observar:

- se o trecho realmente descreve uma função, atividade, tarefa ou transação;
- se a entidade coletiva detectada é pertinente;
- se a relação entre função e documento está corretamente caracterizada;
- se há base legal ou temporalidade funcional associada;
- se o termo detectado deve ser incorporado ao glossário;
- se a descrição precisa de complementação manual.

## 12 Implicações para governança arquivística

A nova perspectiva aproxima o NRPP de uma função institucional mais ampla: apoiar a compreensão da proveniência documental.

Ao relacionar documentos a funções e entidades coletivas, o pipeline passa a produzir insumos mais relevantes para:

- descrição arquivística;
- análise de proveniência;
- entendimento de responsabilidades institucionais;
- mapeamento de registros produzidos por atividades;
- preparação de instrumentos de controle e validação documental.

## 13 Cuidados para próximas evoluções

As próximas melhorias devem priorizar qualidade metodológica, não apenas aumento de detecções.

Recomendações:

- ampliar gradualmente o arquivo `resources/isdf_diretrizes.json`;
- separar padrões genéricos de padrões específicos da CAIXA;
- criar exemplos validados manualmente para calibração;
- registrar falsos positivos e falsos negativos;
- evitar que regras simples de regex sejam tratadas como interpretação semântica completa;
- manter os resultados gerados fora do Git quando forem produtos de execução;
- versionar diretrizes, glossários e código usados em cada processamento.

## 14 Síntese

A principal lição aprendida é que o NRPP deve ser entendido como um instrumento de preparação, não de decisão.

Sua contribuição está em transformar normativos extensos em evidências estruturadas, rastreáveis e organizadas segundo uma matriz funcional inspirada na ISDF.

Com a nova perspectiva, o pipeline passa a apoiar uma pergunta arquivística mais qualificada:

> que funções institucionais explicam a produção, uso e manutenção dos documentos mencionados ou implicados nos normativos?

Essa pergunta é mais robusta do que a simples identificação de documentos, porque conecta o registro ao contexto funcional que lhe confere significado arquivístico.
