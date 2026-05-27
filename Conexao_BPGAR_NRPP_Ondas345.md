# Conexao entre o fluxo BPGAR-UnB e o NRPP

Arquivo de referencia analisado:
`/home/osvaldo/Downloads/BPGAR_UnB_Fluxo_DadosBrutos_Ondas345_v16.pdf`

## Visao geral

O PDF da BPGAR nao deve ser tratado como mais uma norma de entrada do NRPP.
Ele funciona melhor como documento de arquitetura, alinhamento institucional e
ponte conceitual entre:

- a entrega de dados brutos e metadados pela BPGAR;
- o pipeline local NRPP orientado pela ISDF;
- as Ondas 3, 4 e 5 de validacao, curadoria e caracterizacao documental;
- a formacao da prateleira de Tipos Documentais da CAIXA.

A conexao mais importante e esta: a BPGAR fornece ou confirma insumos
rastreaveis; o NRPP transforma esses insumos em evidencias estruturadas; as
ondas distribuem a decisao entre setor CAIXA e UnB.

## Distincao necessaria entre dois usos de A1-A5

O PDF usa `a1 -> a5` para descrever camadas de dados do fluxo BPGAR-UnB.
O NRPP implementado neste repositorio usa `A1 -> A5` para descrever etapas
analiticas do processamento.

Essa diferenca precisa ser explicitada para evitar confusao.

| Camada no PDF BPGAR | Sentido no PDF | Etapa NRPP relacionada | Sentido no NRPP |
|---|---|---|---|
| `a1` | TXT bruto extraido do PDF normativo; fonte de verdade para IA | `A1` | Extracao e normalizacao conservadora do texto |
| `a2` | CSV linha/texto; apoio a rastreabilidade | `A2` | Segmentacao estrutural da norma em itens |
| `a3` | Limpeza inicial de cabecalhos, espacos e OCR | `A3` | Deteccao de pistas semanticas |
| `a4` | Refinamentos pontuais sobre a3 | `A4` | Normalizacao terminologica e enriquecimento ISDF |
| `a5` | CSV/XLSX final com metadados estruturais | `A5` | Planilha final de validacao humana com evidencias e abas ISDF |

Portanto, a equivalencia nao e um-para-um. O correto e dizer que o NRPP
consome e reorganiza logicamente os insumos BPGAR, mas sua semantica interna de
A1-A5 e mais analitica.

## Papel do PDF no pipeline desenvolvido

Minha leitura e que este PDF deve cumprir quatro papeis no projeto:

1. Documento de alinhamento metodologico.
   Ele explica por que o texto bruto e os metadados estruturais sao insumos
   criticos e por que as camadas intermediarias devem permanecer auditaveis.

2. Requisito funcional para evolucao do NRPP.
   Ele deixa claro que a extracao deve caminhar para cinco elementos:
   procedimento, especie documental, acao, objeto e documentos mencionados.

3. Ponte entre NRPP e governanca de dados.
   Ele desloca a saida do pipeline de uma planilha isolada para catalogos
   institucionais reutilizaveis.

4. Justificativa para validacao humana distribuida.
   Ele mostra que UnB, setor CAIXA e bases institucionais como SIICO possuem
   responsabilidades diferentes, evitando que a IA ou a UnB "inventem" contexto.

## Como o NRPP atual se encaixa

O NRPP atual ja cobre uma parte importante da arquitetura descrita no PDF:

- preserva o texto extraido como base auditavel;
- segmenta itens normativos;
- detecta pistas de documentos, processos, funcoes, entidades, legislacao,
  datas e relacionamentos;
- normaliza termos por glossario;
- acrescenta metadados preliminares ISDF;
- gera planilha de validacao humana.

Mas ainda ha uma diferenca de maturidade: o NRPP atual produz evidencias
arquivisticas e funcionais preliminares; o fluxo descrito no PDF mira a
formacao de catalogos institucionais e Tipos Documentais.

## Lacunas para conectar completamente

Para alinhar o NRPP ao fluxo BPGAR-UnB, as proximas evolucoes deveriam criar
uma camada posterior ao A5 atual, voltada a catalogos:

- `catalogo_atividades_normatizadas`
- `catalogo_especies_documentais`
- `catalogo_acoes_documentais`
- `catalogo_objetos_glossario`
- `catalogo_documentos_mencionados`
- `catalogo_tipos_documentais`

Essa camada nao deve substituir o A5. Ela deve nascer a partir do A5 validado.

## Relacao com as Ondas 3, 4 e 5

| Onda | Responsavel principal | Papel no fluxo | Relacao com o NRPP |
|---|---|---|---|
| Onda 3 | Setor CAIXA | Valida atividades, normas, processos, produtos, sistemas e uso real | Usa evidencias do NRPP como ponto de partida |
| Onda 4 | UnB | Padroniza especie, acao e objeto; vincula glossarios e SIICO | Faz curadoria sobre dados validados |
| Onda 5 | Setor CAIXA | Caracteriza o documento real produzido, com metadados tecnicos | Transforma atividade validada em tipo documental caracterizado |

Essa distribuicao confirma uma decisao metodologica importante: o NRPP prepara
evidencias, mas nao decide sozinho o Tipo Documental.

## Interpretacao arquivistica

O ponto forte do PDF e explicitar que Tipo Documental nao deve ser apenas um
nome extraido da norma. Ele deve resultar da combinacao:

```text
Especie + Acao + Objeto = Tipo Documental
```

No NRPP atual, essa logica ainda aparece de forma embrionaria:

- documentos aparecem em `classe=documento`;
- acoes aparecem principalmente em `classe=processo`;
- funcoes aparecem em `classe=funcao`;
- entidades e relacionamentos aparecem como pistas ISDF;
- objetos ainda precisam de extracao mais especializada e cruzamento com SIICO.

Assim, a principal evolucao tecnica e criar campos explicitamente orientados a:

- `procedimento_extraido`;
- `verbo_original`;
- `acao_documental_sugerida`;
- `especie_documental_sugerida`;
- `objeto_sugerido`;
- `documento_mencionado`;
- `fonte_objeto` (`extracao`, `siico`, `processo_negocio`, `manual`);
- `status_curadoria`.

## Decisao recomendada

Minha recomendacao e tratar o PDF da BPGAR como um documento de referencia do
NRPP, nao como entrada operacional comum.

Na pratica:

1. Manter o pipeline A1-A5 atual para normativos.
2. Acrescentar ao manual uma secao explicando a diferenca entre `a1-a5` da
   BPGAR e `A1-A5` do NRPP.
3. Evoluir o A3/A4 para extrair explicitamente os cinco elementos citados no
   PDF: procedimento, especie, acao, objeto e documentos mencionados.
4. Criar uma etapa posterior ao A5, provisoriamente chamada `A6 - Catalogacao
   institucional`, para gerar insumos de catalogos e Tipos Documentais.
5. Preservar a regra metodologica: toda decisao final depende de validacao
   setorial e curadoria UnB.

## Formula sintese

```text
BPGAR fornece PDF, a1 e a5
        |
NRPP estrutura evidencias rastreaveis
        |
Onda 3 confirma realidade operacional
        |
Onda 4 padroniza vocabularios e vincula SIICO
        |
Onda 5 caracteriza o documento produzido
        |
Prateleira CAIXA: Tipo Documental + CCD + TTD + metadados
```

Essa e a conexao mais limpa entre o arquivo analisado e o pipeline desenvolvido.
