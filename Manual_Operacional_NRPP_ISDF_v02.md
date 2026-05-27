# Manual Operacional

## Normative-to-Record Preprocessing Pipeline (NRPP)

### Versão orientada pela ISDF

Autor: Osvaldo Jeronymo Neto  
Versão: v02  
Data: 2026-05-27

## 1 Apresentação

O Normative-to-Record Preprocessing Pipeline (NRPP) é um pipeline metodológico e computacional destinado a apoiar a preparação de evidências arquivísticas a partir de normativos institucionais.

Na sua versão inicial, o NRPP foi concebido para extrair e organizar evidências documentais presentes em textos normativos. Com a incorporação da Norma Internacional para Descrição de Funções (ISDF), o pipeline passa a adotar uma perspectiva funcional: os documentos e registros identificados são tratados em relação às funções, atividades, entidades coletivas e recursos arquivísticos associados à sua produção e manutenção.

Esta versão do manual descreve o uso operacional do NRPP considerando essa nova perspectiva.

O NRPP não substitui a análise arquivística profissional. Ele produz insumos estruturados, rastreáveis e auditáveis para validação humana.

## 2 Objetivo

Estabelecer o procedimento operacional para executar o NRPP em normativos institucionais, gerando artefatos intermediários e uma planilha final de validação humana com apoio da ISDF.

O procedimento busca garantir:

- reprodutibilidade técnica;
- rastreabilidade entre resultados e trechos normativos;
- padronização da extração inicial;
- apoio à descrição funcional;
- separação entre automação e decisão arquivística;
- preservação de trilha de auditoria.

## 3 Mudança metodológica introduzida pela ISDF

A perspectiva anterior do NRPP tinha como foco principal a pergunta:

> que documentos, artefatos ou registros aparecem no normativo?

A perspectiva atual, orientada pela ISDF, amplia a pergunta:

> que funções, atividades, entidades coletivas e relacionamentos explicam a produção e manutenção desses documentos?

Essa mudança desloca o produto final de uma simples tabela de evidências documentais para uma base de validação funcional, capaz de apoiar descrições arquivísticas mais consistentes.

## 4 Base conceitual

Para fins operacionais, o NRPP utiliza a ISDF como referência para estruturar informações relacionadas à descrição de funções.

Os elementos incorporados ao pipeline incluem:

- tipo funcional: função, subfunção, atividade, tarefa ou transação;
- descrição de processos e ações normativas;
- identificação preliminar de entidades coletivas;
- identificação de documentos e recursos relacionados;
- identificação de legislação ou base normativa;
- identificação de datas ou períodos;
- categorização preliminar de relacionamentos;
- campos de controle da descrição.

Esses elementos são sugestões estruturadas para validação. Eles não constituem descrição arquivística definitiva.

## 5 Escopo de aplicação

O NRPP pode ser aplicado a arquivos PDF contendo normativos institucionais com camada textual extraível.

O pipeline é adequado para:

- manuais normativos;
- instruções internas;
- procedimentos administrativos;
- regulamentos;
- normas operacionais;
- documentos institucionais que descrevam responsabilidades, atividades, fluxos ou produção documental.

O NRPP não é adequado, sem preparação adicional, para:

- PDFs exclusivamente digitalizados sem OCR;
- documentos sem estrutura textual reconhecível;
- arquivos corrompidos;
- documentos cujo acesso não esteja formalmente autorizado;
- análises que exijam decisão arquivística automática.

## 6 Estrutura do repositório

A estrutura atual do repositório é:

```text
nrpp/
|-- BuscadorDePdfs.py
|-- orchestrator.py
|-- requirements.txt
|-- README
|-- pipeline/
|   |-- a1_text_normalization.py
|   |-- a2_structural_segmentation.py
|   |-- a3_semantic_cues.py
|   |-- a4_glossary_guided_normalization.py
|   `-- a5_human_guided_structuring.py
|-- resources/
|   |-- glossario_arquivistico_limpo.json
|   |-- glossario_canonico.json
|   `-- isdf_diretrizes.json
`-- pdfs/
```

Os principais componentes são:

- `orchestrator.py`: ponto de entrada principal para executar o pipeline;
- `BuscadorDePdfs.py`: utilitário para localizar e copiar PDFs de uma ou mais origens;
- `pipeline/`: etapas A1 a A5;
- `resources/glossario_arquivistico_limpo.json`: glossário usado na normalização terminológica;
- `resources/isdf_diretrizes.json`: mapeamento das diretrizes ISDF usadas no enriquecimento do A4;
- `pdfs/`: pasta local de entrada para PDFs.

## 7 Arquitetura operacional do pipeline

O NRPP é executado em cinco etapas principais.

### A1 - Extração e normalização textual

Entrada:

- arquivo PDF.

Processamento:

- extrai texto do PDF;
- remove artefatos editoriais simples;
- preserva a estrutura textual necessária para segmentação.

Saída:

- arquivo `.txt` com texto extraído e normalizado.

### A2 - Segmentação estrutural

Entrada:

- arquivo `.txt` produzido no A1.

Processamento:

- identifica segmentos normativos com base em padrões estruturais;
- organiza cada segmento com identificador e texto.

Saída:

- CSV de segmentos textuais.

### A3 - Identificação de pistas semânticas

Entrada:

- CSV de segmentos produzido no A2.

Processamento:

- detecta termos e padrões relacionados a documentos;
- detecta ações normativas;
- detecta pistas de função, atividade, tarefa ou transação;
- detecta entidades coletivas;
- detecta legislação;
- detecta datas;
- detecta relacionamentos.

Saída:

- CSV de evidências semânticas com as colunas:

```text
id
texto
termo
classe
```

### A4 - Normalização terminológica e enriquecimento ISDF

Entrada:

- CSV de evidências semânticas produzido no A3;
- glossário arquivístico;
- diretrizes ISDF estruturadas em JSON.

Processamento:

- normaliza termos usando o glossário;
- associa classes detectadas a áreas e elementos ISDF;
- identifica tipo funcional preliminar;
- registra entidade coletiva detectada;
- registra documento relacionado;
- categoriza relacionamentos quando houver pistas;
- marca itens que exigem validação.

Saída:

- CSV de evidências normalizadas e enriquecidas;
- CSV de auditoria com termos fora do glossário.

Colunas principais do CSV normalizado:

```text
id
texto
termo
classe
termo_norm
isdf_area
isdf_elemento
tipo_funcional
entidade_coletiva_detectada
documento_relacionado
categoria_relacionamento
necessita_validacao
```

### A5 - Estruturação para validação humana

Entrada:

- CSV normalizado produzido no A4.

Processamento:

- consolida evidências por segmento;
- organiza a planilha final de validação;
- cria abas específicas para descrição funcional e relacionamentos ISDF;
- preserva evidências intermediárias para auditoria.

Saída:

- arquivo Excel `tabela_validacao_nrpp.xlsx`.

## 8. Requisitos de ambiente

Requisitos recomendados:

- Python 3.10 ou superior;
- ambiente virtual Python;
- acesso ao repositório NRPP;
- permissão de leitura aos PDFs de origem;
- dependências instaladas por `requirements.txt`.

Dependências principais:

- `pdfminer.six`: extração de texto de PDFs;
- `pandas`: manipulação de dados tabulares;
- `numpy`: suporte computacional;
- `tqdm`: progresso de processamento;
- `regex`: expressões regulares;
- `python-dateutil`: apoio a datas;
- `openpyxl`: escrita de planilhas Excel.

## 9. Instalação

Clone o repositório:

```bash
git clone https://github.com/osvaldojeronymo/NRPP.git
cd NRPP
```

Crie e ative o ambiente virtual.

Linux ou macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Verifique a instalação:

```bash
python orchestrator.py --help
```

## 10. Preparação dos PDFs

O pipeline pode processar PDFs já colocados na pasta `pdfs/` ou pode copiar PDFs de uma origem externa usando o próprio comando de execução.

### Opção 1: PDFs já preparados

Coloque os arquivos PDF na pasta:

```text
pdfs/
```

Depois execute:

```bash
python orchestrator.py pdfs --clean
```

### Opção 2: buscar PDFs em uma pasta de origem

Execute:

```bash
python orchestrator.py pdfs --origem /caminho/da/pasta --clean-pdfs --clean
```

Esse comando:

- busca PDFs recursivamente na origem;
- copia os arquivos para `pdfs/`;
- preserva subpastas relativas;
- remove resultados anteriores quando `--clean` for informado;
- executa o pipeline.

### Opção 3: buscar pela pasta sincronizada do SharePoint

Quando aplicável, informe a matrícula:

```bash
python orchestrator.py pdfs --matricula c000000 --clean-pdfs --clean
```

Ou informe a pasta raiz manualmente:

```bash
python orchestrator.py pdfs --pasta-raiz "C:/Users/c000000/Caixa Economica Federal/O365GRP-Projects - NRPP" --clean-pdfs --clean
```

## 11. Execução padrão

Com os PDFs em `pdfs/`, execute:

```bash
python orchestrator.py pdfs --clean
```

Durante a execução, o terminal exibirá mensagens semelhantes a:

```text
1 PDF(s) encontrados.
Executando com 1 processos em paralelo.

[A1] Extraindo texto
[A2] Segmentando estrutura
[A3] Ancoragem semântica
[A4] Normalização terminológica e enriquecimento ISDF
[A5] Estruturação analítica das evidências
```

## 12. Estrutura de saída

Os resultados são gravados em:

```text
pdfs/NRPP_RESULTADOS/
```

Para cada PDF, o pipeline cria um dossiê:

```text
pdfs/NRPP_RESULTADOS/<subpasta>/<nome_pdf>/
|-- ENTRADA/
|-- EXTRACAO_TEXTO/
|-- INTERMEDIARIOS/
|-- AUDITORIA_PIPELINE/
|-- PRODUTO_FINAL/
`-- README.md
```

Conteúdo esperado:

- `ENTRADA/`: cópia do PDF original;
- `EXTRACAO_TEXTO/`: texto extraído;
- `INTERMEDIARIOS/`: CSVs das etapas A2, A3 e A4;
- `AUDITORIA_PIPELINE/`: termos fora do glossário;
- `PRODUTO_FINAL/`: planilha final de validação;
- `README.md`: descrição do dossiê.

Também é gerado:

```text
pdfs/NRPP_RESULTADOS/resumo_pipeline.csv
```

## 13. Produto final

O principal produto do NRPP é:

```text
tabela_validacao_nrpp.xlsx
```

A planilha contém as seguintes abas.

### validacao_nrpp

Aba principal para revisão humana.

Contém:

- fonte do segmento normativo;
- trecho da norma;
- ação normativa detectada;
- documento ou artefato requerido;
- tipo funcional ISDF;
- entidade coletiva detectada;
- categoria de relacionamento ISDF;
- número de evidências;
- conceitos detectados;
- campos para validação e observações.

### evidencias_normalizadas

Contém a saída completa do A4.

Essa aba deve ser usada para auditoria detalhada das evidências e dos metadados ISDF atribuídos automaticamente.

### descricao_isdf

Agrupa os elementos ISDF sugeridos a partir dos segmentos normativos.

Deve ser usada como apoio à construção ou revisão de descrições funcionais.

### relacionamentos_isdf

Apresenta evidências relacionadas a:

- documentos;
- entidades coletivas;
- relacionamentos entre função, entidade e recurso arquivístico.

Essa aba apoia a validação dos relacionamentos previstos no Capítulo 6 da ISDF.

### controle_descricao

Contém campos de controle inspirados na área de controle da ISDF.

Inclui:

- identificador da descrição da função;
- instituição responsável;
- regras e convenções utilizadas;
- status;
- nível de detalhamento;
- datas de criação, revisão ou obsolescência;
- idioma;
- fontes;
- notas de manutenção.

### evidencias_semanticas

Contém a saída do A3 antes da normalização.

### segmentos_texto

Contém a saída do A2 com os segmentos normativos.

### termos_fora_do_glossario

Contém termos detectados que não tiveram correspondência no glossário.

Essa aba deve orientar a manutenção do vocabulário controlado.

## 14. Como validar os resultados

A validação deve ser feita por pessoa autorizada e com conhecimento do contexto normativo e arquivístico.

Procedimento recomendado:

1. Abrir `tabela_validacao_nrpp.xlsx`.
2. Revisar a aba `validacao_nrpp`.
3. Conferir se o trecho normativo sustenta a evidência detectada.
4. Verificar se o documento ou artefato requerido está corretamente identificado.
5. Conferir se o tipo funcional ISDF é pertinente.
6. Revisar entidade coletiva detectada.
7. Validar categoria de relacionamento, quando houver.
8. Consultar `descricao_isdf` e `relacionamentos_isdf` para revisão arquivística.
9. Registrar observações, ajustes e decisões nos campos de validação.
10. Consultar `termos_fora_do_glossario` para propor atualizações ao glossário.

## 15. Critérios de aceitação da execução

Uma execução será considerada tecnicamente válida quando:

- todos os PDFs esperados forem processados;
- não houver erro crítico no terminal;
- cada PDF possuir dossiê em `NRPP_RESULTADOS`;
- os CSVs intermediários forem gerados;
- a planilha final existir em `PRODUTO_FINAL`;
- a aba `validacao_nrpp` estiver preenchida;
- as abas ISDF estiverem presentes;
- o resumo geral for gerado.

## 16. Rastreabilidade e auditoria

Para cada execução, devem ser preservados:

- commit ou versão do código usado;
- versão do glossário;
- versão de `resources/isdf_diretrizes.json`;
- PDFs de origem;
- CSVs intermediários;
- planilha final;
- resumo da execução;
- data, executor e escopo do processamento.

Os resultados em `pdfs/NRPP_RESULTADOS/` são artefatos de execução e normalmente não devem ser versionados no Git.

## 17. Responsabilidades

### Executor técnico

Responsável por:

- preparar ambiente;
- atualizar repositório;
- instalar dependências;
- organizar PDFs;
- executar pipeline;
- registrar erros e resultados.

### Validador humano

Responsável por:

- revisar evidências;
- confirmar ou rejeitar sugestões;
- preencher campos de validação;
- registrar dúvidas e inconsistências.

### Arquivista ou especialista em gestão documental

Responsável por:

- avaliar pertinência funcional;
- validar uso da ISDF;
- revisar relações entre funções, entidades coletivas e recursos;
- orientar atualização de glossários e diretrizes;
- tomar decisões arquivísticas fora do escopo automatizado.

## 18. Problemas frequentes

### PDF sem texto extraível

Sintoma:

- A1 gera texto vazio ou incompleto.

Ação:

- verificar se o PDF é escaneado;
- substituir por versão com texto;
- aplicar OCR fora do NRPP, se autorizado.

### Segmentação insuficiente

Sintoma:

- A2 gera poucos segmentos ou segmentos muito extensos.

Ação:

- verificar estrutura de numeração do normativo;
- registrar exceção;
- avaliar ajuste futuro dos padrões de segmentação.

### Muitos termos fora do glossário

Sintoma:

- A4 gera muitos registros em `termos_fora_do_glossario`.

Ação:

- revisar termos;
- identificar termos relevantes;
- propor atualização do glossário.

### Muitos falsos positivos ISDF

Sintoma:

- campos ISDF são preenchidos em trechos pouco relevantes.

Ação:

- revisar padrões do A3;
- ajustar `resources/isdf_diretrizes.json`;
- registrar exemplos para calibração.

## 19. Limites do NRPP

O NRPP não:

- interpreta definitivamente o conteúdo normativo;
- conclui descrição arquivística;
- substitui avaliação humana;
- define temporalidade;
- define destinação documental;
- resolve conflitos de competência institucional;
- confirma validade jurídica de normas;
- executa OCR automaticamente.

O NRPP faz:

- extração textual;
- segmentação;
- detecção preliminar de pistas;
- normalização terminológica;
- enriquecimento preliminar com metadados ISDF;
- estruturação de planilha para validação.

## 20. Boas práticas

- Executar o pipeline sempre a partir de uma cópia controlada dos PDFs.
- Usar `--clean` para evitar mistura de resultados antigos e novos.
- Registrar o commit do repositório usado na execução.
- Não editar manualmente arquivos intermediários sem registrar a alteração.
- Validar os resultados no Excel antes de qualquer uso analítico.
- Manter glossários e diretrizes ISDF versionados.
- Tratar campos ISDF como apoio preliminar, não como decisão final.

## 21. Comandos rápidos

Atualizar repositório:

```bash
git pull origin main
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

Executar PDFs locais:

```bash
python orchestrator.py pdfs --clean
```

Buscar PDFs de uma pasta e executar:

```bash
python orchestrator.py pdfs --origem /caminho/da/pasta --clean-pdfs --clean
```

Executar apenas o buscador:

```bash
python BuscadorDePdfs.py /caminho/da/pasta --destino pdfs --clean
```

Ver ajuda:

```bash
python orchestrator.py --help
python BuscadorDePdfs.py --help
```

## 22. Encerramento

Esta versão do manual estabelece o uso operacional do NRPP como ferramenta de preparação de evidências para validação arquivística orientada pela ISDF.

A principal mudança em relação à versão anterior é que o documento ou registro deixou de ser tratado como ponto final isolado da extração. Ele passa a ser analisado como recurso relacionado a funções, atividades, entidades coletivas e responsabilidades institucionais.

Essa mudança amplia a utilidade do NRPP para análise de proveniência, descrição funcional e governança arquivística, mantendo o princípio fundamental do projeto: automação para organizar evidências, validação humana para interpretar e decidir.
