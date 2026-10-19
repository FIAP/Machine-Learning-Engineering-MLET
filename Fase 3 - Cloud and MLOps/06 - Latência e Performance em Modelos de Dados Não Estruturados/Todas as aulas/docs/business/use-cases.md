# Use Cases da Disciplina

## Visao Geral

Cada aula da disciplina e acompanhada de um **caso de uso real** que contextualiza os conceitos tecnicos apresentados. Os use cases estao ordenados por complexidade crescente, acompanhando a progressao pedagogica do curso.

---

## Aula 1 — Fundamentos de Latencia e Performance em ML

**Use Case nao especifico** — A Aula 1 estabelece os fundamentos teoricos (metricas P50/P95/P99, FLOPs, MACs, profiling) que serao aplicados em todos os use cases subsequentes.

---

## Aula 2 — Desafios de Performance em NLP e Audio

### Caso de Uso: Assistente de Voz no E-commerce

| Aspecto | Detalhe |
|---------|---------|
| **Cenario** | Cliente faz pergunta por voz sobre produtos em plataforma de e-commerce |
| **Fluxo** | Fala → ASR (Speech-to-Text) → NLP (Intent + Resposta) → TTS (Text-to-Speech) |
| **Requisitos de latencia** | Resposta imediata — UX exige minimo atraso perceptivel |
| **Carga estimada** | ~100 consultas/minuto em horario de pico |
| **Meta de SLO** | 95% das respostas < 2s (end-to-end, incluindo ASR + NLP + TTS) |
| **Impacto de negocio** | Atraso > 3s → usuario desiste → perda direta de vendas |

**Desafios tecnicos:**
- Complexidade quadratica do mecanismo de atencao no modelo de NLP (Transformer)
- Geracao autoregressiva sequencial no TTS (gargalo de latencia)
- Batching de sequencias de comprimento variavel (padding overhead)
- Necessidade de Flash Attention para reduzir latencia do Transformer

**Tecnicas abordadas na aula:**
- Sparse Attention e Flash Attention para reduzir O(n²) para O(n)
- Batching estrategico (padding vs. packing)
- Modelos de audio otimizados (Whisper, wav2vec 2.0)

📋 **Business Case detalhado:** [Assistente de Voz para E-commerce](business-case-voice-assistant-ecommerce.md)

📄 **Use Case detalhado:** [Use Case — Aula 2: Assistente de Voz no E-commerce](use-case-aula02-assistente-voz-ecommerce.md)

---

## Aula 3 — Desafios de Performance em Visao Computacional

### Caso de Uso: Classificacao de Imagens de Produtos

| Aspecto | Detalhe |
|---------|---------|
| **Cenario** | Classificacao automatica de imagens de produtos (ex: camera vs. smartphone) |
| **Fluxo** | Upload de imagem → Pre-processamento → CNN/ViT inference → Label + Score |
| **Modelos** | Modelos pre-treinados (ImageNet) — MobileNet, EfficientNet, ViT |
| **Requisitos** | Apps moveis exigem inferencia rapida para boa UX (< 100ms) |
| **Impacto** | Classificacao automatica reduz custo de catalogacao manual |

**Desafios tecnicos:**
- Trade-off entre resolucao de entrada e FLOPs/latencia
- CNNs vs. Vision Transformers: quando usar cada abordagem
- Inferencia on-device (mobile) com restricoes de hardware

**Tecnicas abordadas na aula:**
- Arquiteturas eficientes (MobileNet, EfficientNet, EfficientViT)
- Impacto da resolucao nos FLOPs
- Pre-processamento otimizado com NVIDIA DALI e torchvision.transforms.v2

📄 **Use Case detalhado:** [Use Case — Aula 3: Classificacao de Imagens de Produtos](use-case-aula03-classificacao-imagens.md)

---

## Aula 4 — Otimizacao de Modelos: Pruning e Quantizacao

### Caso de Uso: Inspecao Visual em Linha de Producao

| Aspecto | Detalhe |
|---------|---------|
| **Cenario** | Fabrica usa deep learning para detectar defeitos visuais em produtos na linha de producao |
| **Modelo atual** | ResNet-50 com alta acuracia na identificacao de falhas |
| **Problema** | Latencia ~200ms/imagem, insuficiente para throughput de ~30 itens/segundo |
| **Restricao** | Hardware industrial limitado (sem GPU datacenter, apenas edge devices) |
| **Meta** | Latencia < 33ms/imagem mantendo acuracia > 95% |

**Desafios tecnicos:**
- ResNet-50 FP32 e muito pesado para hardware industrial
- Necessidade de reducao de 6x em latencia sem perda significativa de acuracia
- Hardware edge limita opcoes de computacao

**Tecnicas abordadas na aula:**
- Pruning estruturado para remover filtros redundantes
- Quantizacao PTQ INT8 para reducao de 2-4x em latencia
- QAT para recuperar acuracia apos quantizacao agressiva
- Knowledge Distillation (ResNet-50 teacher → MobileNet student)
- Combinacao sinergica: pruning + quantizacao + distillation

📋 **Business Case detalhado:** [Inspecao Visual em Linha de Producao](business-case-visual-inspection.md)

📄 **Use Case detalhado:** [Use Case — Aula 4: Inspecao Visual em Linha de Producao](use-case-aula04-inspecao-visual-producao.md)

---

## Aula 5 — Transfer Learning Eficiente e Adaptacao de Modelos

### Caso de Uso: AdvogAI — Resumo de Documentos Juridicos com IA

| Aspecto | Detalhe |
|---------|---------|
| **Cenario** | Startup AdvogAI desenvolve sistema para resumir documentos juridicos automaticamente |
| **Abordagem** | Fine-tuning eficiente em vez de completo — custo proibitivo para startup |
| **Modelo base** | LLM com ~7B parametros |
| **Tecnica** | LoRA + quantizacao 4-bit (QLoRA) |
| **Resultado** | Treinamento em poucos dias com 1 GPU (viavel para startup) |
| **Acuracia** | Modelo especializado em linguagem juridica com acuracia proxima do fine-tuning completo |

**Desafios tecnicos:**
- Fine-tuning completo de LLM 7B requer multiplas GPUs A100 (custo > $10k/run)
- Memoria GPU insuficiente para carregar modelo completo em FP32
- Adaptacao de dominio (juridico) requer dados especializados em portugues

**Tecnicas abordadas na aula:**
- LoRA: treinar apenas low-rank adapters (~0.1% dos parametros)
- QLoRA: quantizacao 4-bit do modelo base + LoRA adapters em FP16
- Comparacao com Prompt Tuning e Prefix Tuning
- Exportacao do modelo otimizado para ONNX/TorchScript

📄 **Use Case detalhado:** [Use Case — Aula 5: AdvogAI — Documentos Juridicos](use-case-aula05-advogai-documentos-juridicos.md)

---

## Aula 6 — Aceleracao com Hardware: GPU, TPU e Aceleradores

### Caso de Uso: Veiculo Autonomo em Tempo Real

| Aspecto | Detalhe |
|---------|---------|
| **Cenario** | Veiculo autonomo processa streaming de cameras e sensores LIDAR |
| **Problema** | Prototipo inicial com CPU: processamento lento impede reacao em milissegundos |
| **Restricao** | Latencia alta da CPU para deep learning (>500ms/frame) impede uso seguro |
| **Meta** | Latencia < 50ms por frame para reacao em tempo real |
| **Hardware alvo** | NVIDIA Jetson Orin (edge GPU) ou NVIDIA Drive |

**Desafios tecnicos:**
- Processamento simultaneo de multiplos sensores (cameras + LIDAR)
- Restricoes de potencia e calor em hardware embarcado
- Necessidade de mixed precision para maximizar throughput dos Tensor Cores

**Tecnicas abordadas na aula:**
- Tensor Cores com FP16/INT8 para aceleracao 2-8x vs FP32
- Mixed precision training e inference (AMP)
- Profiling com NVIDIA Nsight para identification de gargalos
- Selecao de hardware: GPU datacenter vs. edge vs. TPU

📄 **Use Case detalhado:** [Use Case — Aula 6: Veiculo Autonomo em Tempo Real](use-case-aula06-veiculo-autonomo.md)

---

## Aula 7 — Inferencia Distribuida e Paralelismo de Modelos

### Caso de Uso: Plataforma de Recomendacoes em Escala

| Aspecto | Detalhe |
|---------|---------|
| **Cenario** | Plataforma de streaming de video com milhoes de usuarios simultaneos |
| **Funcionalidade** | Sistema recomenda videos em tempo real (rede neural de recomendacao) |
| **Problema** | Picos de trafego com milhares de requisicoes de inferencia por segundo |
| **Restricao** | Um servidor com GPU nao atende a demanda de pico |
| **Meta** | Throughput > 10.000 req/s com latencia P95 < 50ms |

**Desafios tecnicos:**
- Modelo de recomendacao requer feature lookup + DNN inference
- Picos de trafego (noite/fins de semana) com variacao de 10x
- Modelo embedding table pode exceder memoria de uma unica GPU

**Tecnicas abordadas na aula:**
- Data parallelism para replicar modelo em multiplas GPUs
- Tensor parallelism para particionar embedding tables
- Continuous batching para maximizar utilizacao de GPU
- vLLM/Triton com dynamic batching e auto-scaling

📄 **Use Case detalhado:** [Use Case — Aula 7: Plataforma de Recomendacoes em Escala](use-case-aula07-plataforma-recomendacoes.md)

---

## Aula 8 — Escalabilidade e Orquestracao Multimodal em Producao

### Caso de Uso: Assistente Virtual Multimodal

| Aspecto | Detalhe |
|---------|---------|
| **Cenario** | Usuario interage por voz e envia imagem simultaneamente |
| **Pipeline** | ASR (fala→texto) + NLP (interpretacao) + CV (analise imagem) + TTS (resposta em voz) |
| **Complexidade** | 4 modelos distintos orquestrados em pipeline com dependencias |
| **Meta de SLO** | Latencia E2E < 3s para experiencia fluida |
| **Escala** | Auto-scaling por modalidade (NLP pode ter mais carga que CV) |

**Desafios tecnicos:**
- Orquestracao de 4 modelos com dependencias (ASR → NLP, CV → merge → TTS)
- Cada modelo tem requisitos de hardware e latencia distintos
- Failure em um componente nao deve derrubar o pipeline inteiro (circuit breaker)
- Auto-scaling independente por modalidade

**Tecnicas abordadas na aula:**
- Microservicos com KServe InferenceService por modelo
- Azure ML Managed Online Endpoints com auto-scaling por endpoint
- Monitoramento de SLIs/SLOs por componente do pipeline
- A/B testing e canary deployment para atualizacao de modelos individuais
- Graceful degradation: fallback para modelo mais leve se latencia exceder SLO

📋 **Business Case detalhado:** [Assistente Virtual Multimodal](business-case-multimodal-assistant.md)

📄 **Use Case detalhado:** [Use Case — Aula 8: Assistente Virtual Multimodal](use-case-aula08-assistente-virtual-multimodal.md)

---

## Matriz de Relacao: Use Cases × Tecnicas

| Use Case | Profiling | Atencao Eficiente | Arch Leves | Pruning | Quantizacao | PEFT | GPU/HW | Distribuido | Multimodal |
|----------|-----------|-------------------|------------|---------|-------------|------|--------|-------------|------------|
| Assistente Voz E-commerce | ✓ | ✓ | | | | | | ✓ | ✓ |
| Classificacao Imagens | ✓ | | ✓ | | | | | | |
| Inspecao Visual Industrial | ✓ | | ✓ | ✓ | ✓ | | ✓ | | |
| AdvogAI (Juridico) | ✓ | | | | ✓ | ✓ | | | |
| Veiculo Autonomo | ✓ | | ✓ | ✓ | ✓ | | ✓ | | |
| Recomendacoes em Escala | ✓ | | | | | | ✓ | ✓ | |
| Assistente Multimodal | ✓ | ✓ | | | ✓ | ✓ | ✓ | ✓ | ✓ |
