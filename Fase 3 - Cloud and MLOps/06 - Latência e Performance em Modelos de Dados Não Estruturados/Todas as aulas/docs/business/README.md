# Business Cases e Documentacao de Negocio

## Visao Geral

Esta secao contem os business cases, use cases e diagramas de processo que conectam os conceitos tecnicos da disciplina a cenarios reais de negocio. O objetivo e demonstrar como tecnicas de otimizacao de latencia e performance em modelos de dados nao estruturados geram **valor mensuravel** para organizacoes.

---

## Indice

### Use Cases por Aula

- [Use Cases da Disciplina](use-cases.md) — Mapeamento de use cases reais para cada aula

| Use Case Individual | Aula | Cenario |
|---------------------|------|--------|
| [Assistente de Voz no E-commerce](use-case-aula02-assistente-voz-ecommerce.md) | Aula 2 | NLP + Audio para e-commerce |
| [Classificacao de Imagens de Produtos](use-case-aula03-classificacao-imagens.md) | Aula 3 | CNN vs. ViT, mobile vs. servidor |
| [Inspecao Visual em Linha de Producao](use-case-aula04-inspecao-visual-producao.md) | Aula 4 | Pruning + Quantizacao + Distillation |
| [AdvogAI — Documentos Juridicos](use-case-aula05-advogai-documentos-juridicos.md) | Aula 5 | LoRA + QLoRA para LLM 7B |
| [Veiculo Autonomo em Tempo Real](use-case-aula06-veiculo-autonomo.md) | Aula 6 | GPU Tensor Cores + Mixed Precision |
| [Plataforma de Recomendacoes](use-case-aula07-plataforma-recomendacoes.md) | Aula 7 | Triton + vLLM + Auto-scaling |
| [Assistente Virtual Multimodal](use-case-aula08-assistente-virtual-multimodal.md) | Aula 8 | KServe + Orquestracao de 5+ modelos |

### Business Cases Detalhados

| Business Case | Aulas Relacionadas | Setor |
|---------------|-------------------|-------|
| [Assistente de Voz para E-commerce](business-case-voice-assistant-ecommerce.md) | Aulas 2, 7, 8 | Varejo / E-commerce |
| [Inspecao Visual em Linha de Producao](business-case-visual-inspection.md) | Aulas 3, 4, 6 | Manufatura / Industria |
| [Assistente Virtual Multimodal](business-case-multimodal-assistant.md) | Aulas 5, 7, 8 | Tecnologia / Servicos |

### Diagramas de Processo

| Diagrama | Descricao |
|----------|-----------|
| [Processo de ML em Producao](process-diagrams/business-process.md) | Processo end-to-end (BPMN-style) |
| [Jornada do Usuario](process-diagrams/user-journey.md) | Jornada do cientista de dados usando o repositorio |

---

## Como Usar Esta Documentacao

1. **Comece pelos use cases** para entender o contexto de negocio de cada aula
2. **Aprofunde-se nos business cases** para ver ROI, metricas e arquiteturas de solucao
3. **Consulte os diagramas de processo** para visualizar o workflow end-to-end
4. **Conecte com a documentacao tecnica** em [docs/architecture/](../architecture/overview.md) para decisoes de implementacao
