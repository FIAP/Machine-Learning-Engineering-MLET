# Aula 06 — Aceleração por Hardware: GPU, TPU e ASICs

> Disciplina: Engenharia de Machine Learning — FIAP PosTech

---

## 🎯 Objetivos de Aprendizagem

Ao final desta aula o aluno será capaz de:

1. **Compreender** por que a CPU vira gargalo em cargas pesadas de machine learning.
2. **Explicar** de forma simples por que **GPUs superam CPUs** em ML e o que são **TPUs/ASICs**.
3. **Medir** na prática a latência média e o throughput (FPS) de um pipeline de percepção.
4. **Comparar** o processamento em CPU com o processamento em GPU.
5. **Avaliar** se o sistema atende à meta de segurança de **< 50 ms por frame** (~30 ms ideal).
6. **Reconhecer** tecnologias reais de aceleração (CUDA, cuDNN, TensorRT, XLA, multi-GPU) e seus trade-offs.

---

## 🧩 Caso de Uso

Uma **fabricante de carros autônomos** desenvolve um sistema de **direção automática**. O veículo tem múltiplas
câmeras de alta resolução, **LIDAR** e **radares**, gerando dados não estruturados em tempo real.

```
📷 Câmeras + 🛰️ LIDAR → [percepção / fusão de sensores] → [decisão: virar? frear? desviar?] → 🚗
```

No protótipo inicial, só **CPUs** processavam a visão computacional: **~200 ms por frame** (~5 FPS), muito acima
da meta de **< 50 ms** (~33 ms para 30 FPS). Ao adicionar sensores, formavam-se **filas de imagens**. A solução
foi integrar uma **GPU de alto desempenho**, que derrubou a latência para **~30 ms** (redução de quase 7x),
elevou o throughput para **>30 FPS por sensor** e tornou o sistema **responsivo e confiável**. É nesse desafio
que a aula foca.

---

## 📖 Teoria-Chave

### Por que a CPU vira gargalo?

A CPU tem poucos núcleos potentes, ótimos para tarefas **sequenciais**. Modelos de ML fazem **bilhões de
multiplicações de matrizes** que poderiam rodar **em paralelo** — algo em que a **GPU** (milhares de núcleos)
é imbatível.

| Cenário | Hardware | Latência por frame | FPS aproximado | Atende < 50 ms? |
|---|---|---|---|---|
| Protótipo | CPU tradicional | ~200 ms | ~5 FPS  | ❌ Não |
| Solução  | GPU de alto desempenho | ~30 ms | ~30 FPS | ✅ Sim |

### Tecnologias de aceleração (referência)

| Tecnologia | Ideia central | Ganho |
|---|---|---|
| **GPU** | paralelismo massivo (milhares de núcleos) | processa muitos frames/sensores juntos |
| **TPU** | ASIC do Google para tensores/matrizes | throughput alto, eficiência energética |
| **ASICs** | chip dedicado a IA (Ascend, Habana, Cerebras) | máximo desempenho por watt |
| **CUDA / cuDNN / TensorRT** | programar e otimizar GPUs NVIDIA | menor latência de inferência |
| **XLA** | compilador de grafos (TF/JAX) | otimiza execução, usado em TPUs |
| **Multi-GPU / NVLink** | várias GPUs em paralelo | escala para mais sensores e modelos |

---

## 🛠️ Tecnologias Utilizadas

| Biblioteca | Versão | Uso |
|-----------|--------|-----|
| Python     | ≥ 3.10 | Linguagem base |
| NumPy      | ≥ 1.24 | Geração de ruído e estatísticas |
| Pandas     | ≥ 2.0  | Tabela comparativa |
| Matplotlib | ≥ 3.7  | Visualizações |
| Jupyter    | ≥ 1.0  | Notebook interativo |

> O notebook desta aula é **leve e autocontido**: usa apenas `numpy`, `pandas` e `matplotlib`, **sem GPU real**,
> internet ou datasets externos.

---

## 📂 Estrutura de Arquivos

```
06_aceleracao_hardware_gpu_tpu/
├── README.md                          # ← Você está aqui
├── requirements.txt                   # Dependências da aula
├── notebooks/
│   └── 00_veiculo_autonomo_gpu.ipynb  # Notebook único: CPU vs GPU, latência e throughput
└── outputs/
    └── figures/                       # (opcional) figuras exportadas
```

---

## 🚀 Como Executar

### 1. Instalar dependências

```bash
cd 06_aceleracao_hardware_gpu_tpu
pip install -r requirements.txt

# ou, o mínimo para este notebook:
pip install numpy pandas matplotlib jupyter
```

### 2. Executar o notebook

```bash
jupyter notebook notebooks/00_veiculo_autonomo_gpu.ipynb
```

O notebook é autocontido e executa de ponta a ponta, cobrindo:

1. Contexto do veículo autônomo e a meta de < 50 ms por frame.
2. Conceitos de CPU, GPU, TPU, ASICs e o papel de CUDA/cuDNN/TensorRT/XLA.
3. Hands-on simulando dois cenários (CPU × GPU).
4. Comparação dos resultados em tabela e gráfico (latência e FPS).
5. Discussão de tecnologias reais de aceleração e seus trade-offs.
6. Conclusão sobre atender (ou não) ao requisito de segurança em tempo real.

---

## 📊 Datasets

Esta versão simplificada **não depende de dataset externo**: os tempos de processamento são simulados
sinteticamente dentro do próprio notebook, permitindo medir latência e throughput sem GPU.

---

## 📚 Referências

Referências principais relacionadas aos conceitos da aula:

1. **Jouppi, N. P. et al.** (2017). In-Datacenter Performance Analysis of a Tensor Processing Unit. *ISCA 2017.*
2. **NVIDIA** (2020). NVIDIA A100 Tensor Core GPU Architecture. *Whitepaper.*
3. **Sze, V. et al.** (2017). Efficient Processing of Deep Neural Networks: A Tutorial and Survey. *Proceedings of the IEEE.*
4. **Chetlur, S. et al.** (2014). cuDNN: Efficient Primitives for Deep Learning. *arXiv:1410.0759.*
5. **Reddi, V. J. et al.** (2020). MLPerf Inference Benchmark. *ISCA 2020.*

---

## 🔗 Links Úteis

- [NVIDIA CUDA](https://developer.nvidia.com/cuda-zone)
- [NVIDIA TensorRT](https://developer.nvidia.com/tensorrt)
- [Google Cloud TPU](https://cloud.google.com/tpu)
- [XLA (TensorFlow)](https://www.tensorflow.org/xla)
- [ONNX Runtime](https://onnxruntime.ai/)

---

*Material elaborado para a disciplina de Engenharia de Machine Learning — FIAP PosTech.*
