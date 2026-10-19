# Latência e Performance em Modelos de Dados Não Estruturados

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red.svg)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-teal.svg)](https://fastapi.tiangolo.com/)

---

## 📋 Sobre

Esta disciplina de pós-graduação (mestrado) em Engenharia de Machine Learning aborda de forma rigorosa os fundamentos teóricos e práticos de **latência e performance** aplicados a modelos que operam sobre **dados não estruturados** — textos, imagens, áudio e vídeo. O curso parte das definições formais de métricas de latência (P50, P95, P99, TTFT) e complexidade computacional (FLOPs, MACs), avançando até técnicas de ponta para otimização, aceleração de hardware e orquestração de pipelines multimodais em ambientes de produção.

O programa é orientado a engenheiros de ML e cientistas de dados que necessitam projetar, otimizar e implantar sistemas de inferência de alta performance em cenários reais de negócio. Cada aula combina **teoria formal** com **implementações práticas**, utilizando frameworks de referência da indústria (TensorFlow, PyTorch, scikit-learn) e infraestrutura moderna de deploy (FastAPI, Docker, Kubernetes, Microsoft Azure). Os tópicos cobrem desde mecanismos de atenção eficiente (Flash Attention, Sparse Attention) e arquiteturas leves (MobileNet, EfficientViT) até serving distribuído com Triton Inference Server e vLLM.

Ao longo de 8 aulas, os alunos progridem de uma compreensão sólida dos gargalos de latência em pipelines de inferência, passando por técnicas avançadas de pruning, quantização (PTQ/QAT), knowledge distillation e PEFT (LoRA, QLoRA), até a implementação de sistemas distribuídos com tensor parallelism e orquestração multimodal em escala de produção com KServe e Azure ML Endpoints. O foco permanente é a **redução de latência com preservação de acurácia**, preparando os alunos para enfrentar os desafios reais de MLOps em sistemas que processam dados não estruturados.

O repositório serve como material de apoio completo, contendo notebooks, código-fonte, documentação de arquitetura, business cases reais e Architecture Decision Records (ADRs) que fundamentam cada escolha técnica.

---

## 🎯 Objetivos de Aprendizagem

Ao concluir esta disciplina, o aluno será capaz de:

1. **Diagnosticar gargalos** de latência e throughput em pipelines de inferência para dados não estruturados, utilizando profiling avançado (NVIDIA Nsight, PyTorch Profiler) e métricas formais (P50/P95/P99, FLOPs, MACs)
2. **Analisar trade-offs** entre mecanismos de atenção (quadrática vs. Flash Attention vs. Linear Attention) e arquiteturas (CNN vs. ViT, autoregressive vs. non-autoregressive) em termos de latência, acurácia e custo
3. **Aplicar técnicas de compressão** de modelos (pruning estruturado/não-estruturado, quantização PTQ/QAT, knowledge distillation) para reduzir latência de inferência com degradação controlada de acurácia
4. **Projetar pipelines de fine-tuning eficiente** com PEFT (LoRA, QLoRA, Adapters, Prefix Tuning) e otimização de grafos computacionais (ONNX, TorchScript, torch.compile)
5. **Selecionar e otimizar aceleradores de hardware** (GPU Tensor Cores, TPU systolic arrays, NPUs) com mixed precision (FP16, BF16, TF32, INT8) e gerenciamento de memória GPU
6. **Implementar sistemas de inferência distribuída** com paralelismo de dados, modelo e pipeline, utilizando Triton Inference Server, vLLM e continuous batching com PagedAttention
7. **Orquestrar pipelines multimodais** (NLP + Visão + Áudio) em produção com Kubernetes (KServe, Seldon Core), Azure ML Endpoints, monitoramento de SLIs/SLOs e estratégias de canary deployment
8. **Avaliar quantitativamente** o impacto de cada técnica de otimização em cenários reais, combinando métricas de ML (acurácia, F1) com métricas de sistema (latência, throughput, custo/inferência)

---

## 📚 Conteúdo das Aulas

### Aula 1 — Fundamentos de Latência e Performance em ML
> **Objetivo:** Estabelecer as definições formais de latência, throughput e complexidade computacional em sistemas de inferência de ML, incluindo profiling de pipelines end-to-end.

Introdução às métricas formais de performance (latência P50/P95/P99, throughput, TTFT), complexidade computacional de modelos (FLOPs, MACs, contagem de parâmetros) e decomposição do pipeline de inferência end-to-end (pré-processamento, inferência, pós-processamento). Análise dos trade-offs fundamentais entre acurácia, latência e custo computacional com benchmarks sintéticos.

**Tecnologias:** Python, NumPy, scikit-learn, cProfile, line_profiler, timeit, PyTorch Profiler
📂 [Acessar material](01_fundamentos_latencia_performance_ml/)

---

### Aula 2 — Desafios de Performance em NLP e Áudio
> **Objetivo:** Identificar e mitigar gargalos de performance específicos de modelos Transformer para NLP e processamento de áudio em cenários de tempo real.

Análise da complexidade quadrática do mecanismo de atenção em Transformers e alternativas eficientes (Sparse Attention, Linear Attention, Flash Attention). Impacto da tokenização na latência, gargalo da geração autoregressiva sequencial, processamento de áudio (espectrogramas Mel/MFCC) e estratégias de batching para sequências de comprimento variável (padding vs. packing).

**Tecnologias:** PyTorch, Hugging Face Transformers, Flash Attention, librosa, Whisper, wav2vec 2.0, ONNX Runtime
📂 [Acessar material](02_desafios_performance_nlp_audio/)

---

### Aula 3 — Desafios de Performance em Visão Computacional
> **Objetivo:** Otimizar pipelines de visão computacional para inferência em tempo real, comparando CNNs e Vision Transformers em cenários com restrições de latência.

Trade-offs de latência e acurácia entre CNNs e Vision Transformers (ViT), impacto da resolução de entrada nos FLOPs, arquiteturas eficientes (MobileNet, EfficientNet, EfficientViT) e detecção de objetos em tempo real (YOLO v8/v11, RT-DETR). Pipelines de streaming de vídeo com keyframe extraction e pré-processamento otimizado com NVIDIA DALI.

**Tecnologias:** PyTorch, TensorFlow/Keras, OpenCV, TensorRT, ONNX, torchvision, NVIDIA DALI, Ultralytics
📂 [Acessar material](03_desafios_performance_visao_computacional/)

---

### Aula 4 — Otimização de Modelos: Pruning e Quantização
> **Objetivo:** Aplicar técnicas de compressão de redes neurais (pruning, quantização, knowledge distillation) para reduzir latência e consumo de memória com degradação controlada de acurácia.

Teoria de compressão baseada na hipótese da Lottery Ticket, pruning estruturado vs. não-estruturado com critérios de importância, quantização pós-treinamento (PTQ: INT8, FP16, INT4), quantização consciente de treinamento (QAT), framework teacher-student para knowledge distillation e combinação sinérgica de técnicas de compressão.

**Tecnologias:** PyTorch (torch.quantization, torch.nn.utils.prune), TensorFlow Lite, ONNX Runtime, Neural Network Intelligence (NNI), TensorRT
📂 [Acessar material](04_otimizacao_modelos_pruning_quantizacao/)

---

### Aula 5 — Transfer Learning Eficiente e Adaptação de Modelos
> **Objetivo:** Dominar técnicas de Parameter-Efficient Fine-Tuning (PEFT) e otimização de grafos computacionais para adaptação de modelos de larga escala com recursos limitados.

Comparação entre fine-tuning completo e PEFT (LoRA, QLoRA, Adapters, Prompt Tuning, Prefix Tuning), otimização de grafos computacionais com ONNX, TorchScript e torch.compile, exportação e conversão de modelos, compilação JIT e ahead-of-time para redução de overhead e estratégias de caching e warm-up.

**Tecnologias:** Hugging Face PEFT, bitsandbytes, LoRA/QLoRA, PyTorch, TorchScript, torch.compile, ONNX, Transformers
📂 [Acessar material](05_transfer_learning_eficiente/)

---

### Aula 6 — Aceleração com Hardware: GPU, TPU e Aceleradores
> **Objetivo:** Compreender a arquitetura de aceleradores de hardware e otimizar o uso de GPU Tensor Cores, TPUs e NPUs para maximizar performance de inferência e treinamento.

Arquitetura de GPUs (CUDA cores, Tensor Cores, hierarquia de memória), modelo de execução SIMT, operações de baixa precisão (FP16, BF16, TF32, INT8) em Tensor Cores, otimização de memória (gradient checkpointing, mixed precision), TPUs e aceleradores especializados (NPUs, AWS Inferentia) e profiling avançado com NVIDIA Nsight e PyTorch Profiler.

**Tecnologias:** CUDA, cuDNN, NVIDIA TensorRT, PyTorch (torch.cuda, AMP), TensorFlow (mixed precision), NVIDIA Nsight, PyTorch Profiler
📂 [Acessar material](06_aceleracao_hardware_gpu_tpu/)

---

### Aula 7 — Inferência Distribuída e Paralelismo de Modelos
> **Objetivo:** Projetar e implementar sistemas de inferência distribuída com tensor parallelism, continuous batching e gerenciamento eficiente de KV-Cache para modelos de larga escala.

Data parallelism vs. model parallelism vs. pipeline parallelism, tensor parallelism para LLMs (Megatron-LM, DeepSpeed), serving distribuído com Triton Inference Server, vLLM e TGI, continuous batching, PagedAttention para gerenciamento eficiente de KV-Cache, protocolos de comunicação (NCCL, gRPC) e auto-scaling baseado em latência.

**Tecnologias:** PyTorch Distributed (DDP, FSDP), Ray Serve, Triton Inference Server, vLLM, TGI, DeepSpeed, Kubernetes
📂 [Acessar material](07_inferencia_distribuida_paralelismo/)

---

### Aula 8 — Escalabilidade e Orquestração Multimodal em Produção
> **Objetivo:** Integrar e orquestrar pipelines multimodais em ambientes de produção com monitoramento de SLIs/SLOs, canary deployments e auto-scaling gerenciado no Azure.

Arquiteturas de serving (microserviços vs. monolito para ML), orquestração com Kubernetes (KServe, Seldon Core, BentoML), Azure ML Managed Online Endpoints com auto-scaling, monitoramento de latência (SLIs, SLOs, error budgets), orquestração de pipelines multimodais (texto + imagem + áudio), A/B testing e canary deployments, e revisão integrativa da teoria à produção em escala.

**Tecnologias:** FastAPI, Docker, Kubernetes, KServe, Seldon Core, BentoML, Azure ML Endpoints, Prometheus, Grafana, Apache Kafka
📂 [Acessar material](08_escalabilidade_orquestracao_multimodal/)

---

## 🚀 Como Usar Este Repositório

### Pré-requisitos

| Requisito | Versão Mínima |
|-----------|---------------|
| Python | 3.10+ |
| pip | 23.0+ |
| Git | 2.30+ |
| Docker | 24.0+ |
| NVIDIA Driver (opcional) | 525+ |
| CUDA Toolkit (opcional) | 12.0+ |

### Instalação

```bash
# 1. Clonar o repositório
git clone https://github.com/fiap/latencia-performance-dados-nao-estruturados.git
cd latencia-performance-dados-nao-estruturados

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
.\venv\Scripts\activate   # Windows

# 3. Instalar dependências gerais
pip install -r requirements.txt

# 4. (Opcional) Instalar dependências específicas de uma aula
pip install -r 01_fundamentos_latencia_performance_ml/requirements.txt
```

### Execução

Cada aula possui sua própria pasta com um `README.md` contendo instruções específicas. O fluxo geral é:

```bash
# Navegar para a aula desejada
cd 04_otimizacao_modelos_pruning_quantizacao/

# Executar notebooks (Jupyter)
jupyter notebook notebooks/

# Ou executar scripts diretamente
python src/main.py
```

---

## 📂 Estrutura do Repositório

```
.
├── README.md                                       # Este arquivo
├── requirements.txt                                # Dependências Python gerais
├── .gitignore                                      # Regras de exclusão Git
├── LICENSE                                         # Licença MIT
│
├── docs/
│   ├── architecture/
│   │   ├── overview.md                             # Visão geral da arquitetura
│   │   ├── diagrams/
│   │   │   ├── system-architecture.md              # Arquitetura de sistema E2E
│   │   │   ├── data-flow.md                        # Fluxo de dados
│   │   │   └── deployment.md                       # Diagrama de deployment
│   │   └── adr/
│   │       ├── template.md                         # Template padrão de ADR
│   │       ├── 0001-escolha-framework-ml.md        # ADR: Frameworks de ML
│   │       ├── 0002-estrategia-armazenamento.md    # ADR: Armazenamento de dados
│   │       ├── 0003-arquitetura-api-modelos.md     # ADR: API de modelos
│   │       ├── 0004-versionamento-modelos.md       # ADR: Versionamento de modelos
│   │       └── 0005-infraestrutura-deployment.md   # ADR: Infra de deployment
│   ├── business/
│   │   ├── README.md                               # Índice de business cases
│   │   ├── use-cases.md                            # Use cases por aula
│   │   ├── process-diagrams/
│   │   │   ├── business-process.md                 # Processo E2E de ML
│   │   │   └── user-journey.md                     # Jornada do usuário
│   │   ├── business-case-voice-assistant-ecommerce.md
│   │   ├── business-case-visual-inspection.md
│   │   └── business-case-multimodal-assistant.md
│   └── contributing.md                             # Guia de contribuição
│
├── 01_fundamentos_latencia_performance_ml/         # Aula 1
├── 02_desafios_performance_nlp_audio/              # Aula 2
├── 03_desafios_performance_visao_computacional/    # Aula 3
├── 04_otimizacao_modelos_pruning_quantizacao/      # Aula 4
├── 05_transfer_learning_eficiente/                 # Aula 5
├── 06_aceleracao_hardware_gpu_tpu/                 # Aula 6
├── 07_inferencia_distribuida_paralelismo/          # Aula 7
└── 08_escalabilidade_orquestracao_multimodal/      # Aula 8
```

---

## 📖 Documentação

| Documento | Descrição |
|-----------|-----------|
| [Arquitetura](docs/architecture/overview.md) | Visão geral da arquitetura das soluções |
| [Diagramas](docs/architecture/diagrams/) | Diagramas de sistema, fluxo de dados e deployment |
| [ADRs](docs/architecture/adr/) | Architecture Decision Records |
| [Business Cases](docs/business/) | Casos de uso e business cases reais |
| [Processos](docs/business/process-diagrams/) | Diagramas de processo de negócio |
| [Contribuição](docs/contributing.md) | Guia para contribuir com o repositório |

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Consulte o [Guia de Contribuição](docs/contributing.md) para detalhes sobre:

- Como reportar issues
- Como submeter pull requests
- Padrões de código e estilo
- Como adicionar conteúdo de novas aulas

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** — veja o arquivo [LICENSE](LICENSE) para detalhes.

---

<p align="center">
  <strong>FIAP — Pós-Graduação em Engenharia de Machine Learning</strong><br/>
  Disciplina: Latência e Performance em Modelos de Dados Não Estruturados
</p>
