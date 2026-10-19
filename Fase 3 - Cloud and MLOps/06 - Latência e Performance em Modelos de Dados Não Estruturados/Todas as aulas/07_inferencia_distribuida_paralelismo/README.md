# Aula 07 — Inferência Distribuída e Paralelismo

> Disciplina: Engenharia de Machine Learning — FIAP PosTech

---

## 🎯 Objetivos de Aprendizagem

Ao final desta aula o aluno será capaz de:

1. **Compreender** por que um único servidor vira gargalo sob alta carga de inferência.
2. **Explicar** de forma simples o que são **paralelismo de dados**, **paralelismo de modelos**, **batching** e **balanceamento de carga**.
3. **Medir** na prática a latência média e o throughput (req/s) de um sistema de inferência.
4. **Comparar** uma arquitetura monolítica (1 servidor) com um cluster distribuído (N servidores).
5. **Avaliar** se o sistema aguenta um pico de carga de milhares de requisições por segundo.
6. **Reconhecer** tecnologias reais (Triton, TensorFlow Serving, TorchServe, BentoML, NVIDIA Dynamo) e seus trade-offs.

---

## 🧩 Caso de Uso

Uma **plataforma de streaming de vídeos** (pense em um "YouTube" ou "Netflix") usa modelos de ML para
**recomendar vídeos em tempo real**. A cada abertura do app ou fim de vídeo, um modelo de deep learning gera
uma nova lista personalizada de recomendações.

```
👥 Usuários → [balanceador de carga] → [servidor 1 | servidor 2 | ... | servidor N] → 🎬 recomendações
```

Com poucos usuários, **1 servidor com GPU** bastava. Com **milhões de usuários** e **picos de tráfego**
(~5.000 req/s), um servidor sozinho (~500 req/s) **satura**, formando **filas** e aumentando a latência. A
solução foi **escalar horizontalmente**: um **cluster de 10 servidores** com **balanceador de carga**, que
elevou o throughput em ~**10x**, manteve a latência baixa e trouxe **alta disponibilidade**. É nesse desafio
que a aula foca.

---

## 📖 Teoria-Chave

### Paralelismo de dados x paralelismo de modelos

- **Paralelismo de dados:** várias **cópias do modelo** em paralelo; o balanceador distribui as requisições.
  Escala o **throughput** (mais usuários ao mesmo tempo).
- **Paralelismo de modelos:** uma **única inferência** dividida entre vários dispositivos. Necessário para
  modelos **gigantes** (LLMs 70B+), com maior complexidade de comunicação.

| Cenário | Arquitetura | Servidores | Throughput | Atende ao pico (5.000 req/s)? |
|---|---|---|---|---|
| Original | Monolítica | 1 | ~500 req/s | ❌ Não |
| Solução  | Distribuída | 10 | ~5.000 req/s | ✅ Sim |

### Tecnologias de inferência distribuída (referência)

| Ferramenta / Técnica | Ideia central | Ganho |
|---|---|---|
| **Balanceador de carga** | distribui requisições entre servidores | evita filas e sobrecarga |
| **Batching dinâmico** | agrupa requisições em lotes | máximo throughput por GPU |
| **NVIDIA Triton** | servidor de inferência multi-framework | múltiplas instâncias + monitoramento |
| **TF Serving / TorchServe / BentoML** | servir modelos em produção | escalonamento e versionamento |
| **NVIDIA Dynamo / NeMo Megatron** | inferência desagregada para LLMs enormes | ~30x mais inferências/s (70B+) |
| **Auto-scaling / tolerância a falhas** | ajusta instâncias e cobre falhas | alta disponibilidade |

---

## 🛠️ Tecnologias Utilizadas

| Biblioteca | Versão | Uso |
|-----------|--------|-----|
| Python     | ≥ 3.10 | Linguagem base |
| NumPy      | ≥ 1.24 | Geração de tempos e estatísticas |
| Pandas     | ≥ 2.0  | Tabela comparativa |
| Matplotlib | ≥ 3.7  | Visualizações |
| Jupyter    | ≥ 1.0  | Notebook interativo |

> O notebook desta aula é **leve e autocontido**: usa apenas `numpy`, `pandas` e `matplotlib`, **sem GPU**,
> internet ou datasets externos.

---

## 📂 Estrutura de Arquivos

```
07_inferencia_distribuida_paralelismo/
├── README.md                                         # ← Você está aqui
├── requirements.txt                                  # Dependências da aula
├── notebooks/
│   └── 00_recomendacoes_inferencia_distribuida.ipynb # Notebook único: monolítico x cluster distribuído
└── outputs/
    └── figures/                                      # (opcional) figuras exportadas
```

---

## 🚀 Como Executar

### 1. Instalar dependências

```bash
cd 07_inferencia_distribuida_paralelismo
pip install -r requirements.txt

# ou, o mínimo para este notebook:
pip install numpy pandas matplotlib jupyter
```

### 2. Executar o notebook

```bash
jupyter notebook notebooks/00_recomendacoes_inferencia_distribuida.ipynb
```

O notebook é autocontido e executa de ponta a ponta, cobrindo:

1. Contexto da plataforma de streaming e a necessidade de recomendações em tempo real.
2. Conceitos de inferência distribuída, paralelismo de dados/modelos, batching e balanceamento.
3. Hands-on simulando dois cenários (1 servidor × cluster de 10 servidores).
4. Comparação dos resultados em tabela e gráfico (latência, throughput, escalabilidade).
5. Discussão de tecnologias reais (Triton, TF Serving, TorchServe, BentoML, Dynamo) e trade-offs.
6. Conclusão sobre atender (ou não) ao pico de carga com alta disponibilidade.

---

## 📊 Datasets

Esta versão simplificada **não depende de dataset externo**: as requisições e os tempos de inferência são
simulados sinteticamente dentro do próprio notebook, permitindo medir latência e throughput sem GPU.

---

## 📚 Referências

Referências principais relacionadas aos conceitos da aula:

1. **Crankshaw, D. et al.** (2017). Clipper: A Low-Latency Online Prediction Serving System. *NSDI 2017.*
2. **Olston, C. et al.** (2017). TensorFlow-Serving: Flexible, High-Performance ML Serving. *arXiv:1712.06139.*
3. **Shoeybi, M. et al.** (2019). Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism. *arXiv:1909.08053.*
4. **NVIDIA** (2021). Triton Inference Server: Architecture and Best Practices. *Documentação técnica.*
5. **Reddi, V. J. et al.** (2020). MLPerf Inference Benchmark. *ISCA 2020.*

---

## 🔗 Links Úteis

- [NVIDIA Triton Inference Server](https://developer.nvidia.com/triton-inference-server)
- [TensorFlow Serving](https://www.tensorflow.org/tfx/guide/serving)
- [TorchServe](https://pytorch.org/serve/)
- [BentoML](https://www.bentoml.com/)
- [NVIDIA Dynamo](https://developer.nvidia.com/dynamo)

---

*Material elaborado para a disciplina de Engenharia de Machine Learning — FIAP PosTech.*
