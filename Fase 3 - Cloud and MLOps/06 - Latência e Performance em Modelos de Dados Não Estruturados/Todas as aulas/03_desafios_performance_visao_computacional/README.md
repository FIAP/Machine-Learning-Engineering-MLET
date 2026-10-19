# Aula 03 — Desafios de Performance em Visão Computacional

> Disciplina: Engenharia de Machine Learning — FIAP PósTech

---

## 🎯 Objetivos de Aprendizagem

Ao final desta aula o aluno será capaz de:

1. **Compreender** o problema de latência em um sistema de vigilância inteligente em tempo real.
2. **Explicar** de forma simples o que são **latência de inferência**, **throughput** e **FPS**.
3. **Medir** na prática a latência média e calcular os FPS de um pipeline de visão.
4. **Comparar** um modelo pesado (ResNet-50) com um modelo otimizado.
5. **Avaliar** se o sistema atende à meta de tempo real de **30 FPS**.
6. **Reconhecer** técnicas reais de otimização (modelos menores, quantização, GPU, runtimes) e seus trade-offs.

---

## 🧩 Caso de Uso

Um **campus empresarial** possui um sistema de **vigilância inteligente**. Câmeras de segurança usam IA para
detectar intrusos e atividades suspeitas, 24 horas por dia, e precisam identificar ameaças **em tempo real**.

```
📹 Câmera → [captura frame] → [modelo de IA] → [decisão: intruso?] → 🔔 alerta
```

Hoje o sistema usa **ResNet-50** (alta acurácia), mas com **~200 ms por frame** (~5 FPS). Esse atraso é
excessivo para segurança em tempo real. A meta é atingir **~30 FPS** (≈ 33 ms por frame), mantendo precisão
suficiente para diferenciar funcionários autorizados de intrusos. É nesse desafio que a aula foca.

---

## 📖 Teoria-Chave

### Latência, Throughput e FPS

Para um pipeline simples que processa um frame de cada vez:

$$\text{FPS} \approx \frac{1000}{\text{latência por frame (ms)}}$$

| Latência por frame | FPS aproximado | Tempo real (30 FPS)? |
|---|---|---|
| 200 ms | ~5 FPS  | ❌ Não |
| 100 ms | ~10 FPS | ❌ Não |
| 33 ms  | ~30 FPS | ✅ Sim |
| 16 ms  | ~60 FPS | ✅ Sim |

Modelos grandes (mais parâmetros e operações) tendem a ter **maior latência**. Por isso, otimizar a
inferência é essencial em visão computacional em tempo real.

### Técnicas de otimização (referência)

| Técnica | Ideia central | Ganho |
|---|---|---|
| **Modelos menores** | MobileNet / EfficientNet no lugar da ResNet-50 | menos operações |
| **Quantização** | pesos FP32 → INT8 | modelo até 4x menor, mais rápido |
| **Batch inference** | processar vários frames de uma vez | maior throughput |
| **GPU / runtimes** | TensorRT, ONNX Runtime, OpenVINO | melhor uso do hardware |
| **Resolução / frames** | imagens menores, keyframes | menos cálculo total |

---

## 🛠️ Tecnologias Utilizadas

| Biblioteca | Versão | Uso |
|-----------|--------|-----|
| Python     | ≥ 3.10 | Linguagem base |
| NumPy      | ≥ 1.24 | Geração de ruído e estatísticas |
| Pandas     | ≥ 2.0  | Tabela comparativa |
| Matplotlib | ≥ 3.7  | Visualizações |
| Jupyter    | ≥ 1.0  | Notebook interativo |

> O notebook desta aula é **leve e autocontido**: usa apenas `numpy`, `pandas` e `matplotlib`, **sem GPU**,
> internet ou datasets externos.

---

## 📂 Estrutura de Arquivos

```
03_desafios_performance_visao_computacional/
├── README.md                                    # ← Você está aqui
├── requirements.txt                             # Dependências da aula
├── notebooks/
│   └── 00_vigilancia_inteligente_latencia.ipynb # Notebook único: latência, throughput e FPS
└── outputs/
    └── figures/                                 # (opcional) figuras exportadas
```

---

## 🚀 Como Executar

### 1. Instalar dependências

```bash
cd 03_desafios_performance_visao_computacional
pip install -r requirements.txt

# ou, o mínimo para este notebook:
pip install numpy pandas matplotlib jupyter
```

### 2. Executar o notebook

```bash
jupyter notebook notebooks/00_vigilancia_inteligente_latencia.ipynb
```

O notebook é autocontido e executa de ponta a ponta, cobrindo:

1. Contexto do sistema de vigilância inteligente e a meta de 30 FPS.
2. Conceitos de latência de inferência, throughput e FPS.
3. Hands-on simulando dois cenários (modelo pesado × modelo otimizado).
4. Comparação dos resultados em tabela e gráfico.
5. Discussão de técnicas reais de otimização.
6. Conclusão sobre atender (ou não) ao requisito de tempo real.

---

## 📊 Datasets

Esta versão simplificada **não depende de dataset externo**: os tempos de inferência são simulados
sinteticamente dentro do próprio notebook, permitindo medir latência, throughput e FPS sem GPU.

---

## 📚 Referências

Referências principais relacionadas aos conceitos da aula:

1. **He, K. et al.** (2016). Deep Residual Learning for Image Recognition. *CVPR 2016.*
2. **Howard, A. G. et al.** (2017). MobileNets: Efficient CNNs for Mobile Vision Applications. *arXiv:1704.04861.*
3. **Tan, M. & Le, Q. V.** (2019). EfficientNet: Rethinking Model Scaling for CNNs. *ICML 2019.*
4. **Jacob, B. et al.** (2018). Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference. *CVPR 2018.*
5. **Reddi, V. J. et al.** (2020). MLPerf Inference Benchmark. *ISCA 2020.*

---

## 🔗 Links Úteis

- [torchvision — Modelos de visão](https://pytorch.org/vision/stable/models.html)
- [ONNX Runtime](https://onnxruntime.ai/)
- [NVIDIA TensorRT](https://developer.nvidia.com/tensorrt)
- [Intel OpenVINO](https://docs.openvino.ai/)
- [MobileNet Paper](https://arxiv.org/abs/1704.04861)

---

*Material elaborado para a disciplina de Engenharia de Machine Learning — FIAP PosTech.*
