# Aula 04 — Otimização de Modelos: Pruning e Quantização

> Disciplina: Engenharia de Machine Learning — FIAP PosTech

---

## 🎯 Objetivos de Aprendizagem

Ao final desta aula o aluno será capaz de:

1. **Compreender** o problema de latência na inspeção visual de defeitos em uma linha de produção industrial.
2. **Explicar** de forma simples o que são **pruning** (estruturado/não-estruturado) e **quantização** (PTQ/QAT).
3. **Medir** na prática a latência média e calcular o throughput (itens/segundo) de um pipeline de inferência.
4. **Comparar** um modelo pesado (ResNet-50 FP32) com uma versão otimizada (quantização PTQ INT8).
5. **Avaliar** se o sistema atende à meta de produção de **30 itens por segundo**.
6. **Reconhecer** técnicas reais de otimização (pruning, quantização, fine-tuning, hardware) e seus trade-offs.

---

## 🧩 Caso de Uso

Uma **fábrica** usa deep learning para **detectar defeitos** nos produtos ao longo da **linha de produção**.
Uma câmera fotografa cada item na esteira e um modelo de IA decide se a peça está **OK** ou **defeituosa**.

```
🏭 Esteira → [foto do item] → [modelo de IA] → [decisão: defeito?] → ✅ / ❌ descarte
```

Hoje o sistema usa **ResNet-50** (alta acurácia), mas com **~200 ms por imagem** (~5 itens/s) — insuficiente
para uma esteira que movimenta **~30 itens/s**. Além disso, o **hardware industrial é limitado** e precisa de
uma solução mais **leve**. A meta é atingir **~30 itens/s** (≈ 33 ms por imagem), reduzindo latência, tamanho
do modelo e custo computacional, mantendo acurácia suficiente para separar peças boas de defeituosas. É nesse
desafio que a aula foca.

---

## 📖 Teoria-Chave

### Latência e Throughput

Para um pipeline simples que processa uma imagem de cada vez:

$$\text{throughput} \approx \frac{1000}{\text{latência por imagem (ms)}}$$

| Latência por imagem | Throughput aproximado | Meta (30 itens/s)? |
|---|---|---|
| 200 ms | ~5 itens/s  | ❌ Não |
| 100 ms | ~10 itens/s | ❌ Não |
| 33 ms  | ~30 itens/s | ✅ Sim |
| 16 ms  | ~60 itens/s | ✅ Sim |

Modelos grandes (mais parâmetros e operações) tendem a ter **maior latência**. Pruning reduz o **número** de
operações; quantização reduz o **custo** de cada operação.

### Técnicas de otimização (referência)

| Técnica | Ideia central | Ganho |
|---|---|---|
| **Pruning estruturado** | remove canais/filtros inteiros | modelo menor e mais rápido |
| **Pruning não-estruturado** | zera pesos individuais irrelevantes | alta compressão (esparsidade) |
| **Quantização PTQ** | FP32 → INT8 sem re-treino | até 4x menor, mais rápido |
| **Quantização QAT** | simula INT8 durante o treino | recupera acurácia perdida |
| **Fine-tuning após poda** | re-treina após remover pesos | recupera acurácia perdida |
| **Aceleração por hardware** | NPU / GPU / runtimes otimizados | mais operações por segundo |

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
04_otimizacao_modelos_pruning_quantizacao/
├── README.md                                 # ← Você está aqui
├── requirements.txt                          # Dependências da aula
├── notebooks/
│   └── 00_inspecao_defeitos_latencia.ipynb   # Notebook único: pruning, quantização e latência
└── outputs/
    └── figures/                              # (opcional) figuras exportadas
```

---

## 🚀 Como Executar

### 1. Instalar dependências

```bash
cd 04_otimizacao_modelos_pruning_quantizacao
pip install -r requirements.txt

# ou, o mínimo para este notebook:
pip install numpy pandas matplotlib jupyter
```

### 2. Executar o notebook

```bash
jupyter notebook notebooks/00_inspecao_defeitos_latencia.ipynb
```

O notebook é autocontido e executa de ponta a ponta, cobrindo:

1. Contexto da inspeção visual de defeitos e a meta de 30 itens/s.
2. Conceitos de pruning (estruturado/não-estruturado) e quantização (PTQ/QAT).
3. Hands-on simulando dois cenários (ResNet-50 FP32 × versão quantizada PTQ INT8).
4. Comparação dos resultados em tabela e gráfico (latência, throughput, tamanho).
5. Discussão de técnicas reais de otimização e seus trade-offs.
6. Conclusão sobre atender (ou não) ao requisito de produção.

---

## 📊 Datasets

Esta versão simplificada **não depende de dataset externo**: os tempos de inferência são simulados
sinteticamente dentro do próprio notebook, permitindo medir latência e throughput sem GPU.

---

## 📚 Referências

Referências principais relacionadas aos conceitos da aula:

1. **Han, S. et al.** (2015). Learning both Weights and Connections for Efficient Neural Networks. *NeurIPS 2015.*
2. **Frankle, J. & Carbin, M.** (2019). The Lottery Ticket Hypothesis. *ICLR 2019.*
3. **Jacob, B. et al.** (2018). Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference. *CVPR 2018.*
4. **Molchanov, P. et al.** (2017). Pruning CNNs for Resource Efficient Inference. *ICLR 2017.*
5. **Blalock, D. et al.** (2020). What is the State of Neural Network Pruning? *MLSys 2020.*

---

## 🔗 Links Úteis

- [PyTorch Pruning Tutorial](https://pytorch.org/tutorials/intermediate/pruning_tutorial.html)
- [PyTorch Quantization Docs](https://pytorch.org/docs/stable/quantization.html)
- [ONNX Runtime](https://onnxruntime.ai/)
- [Intel Neural Compressor](https://github.com/intel/neural-compressor)
- [Hugging Face Optimum](https://huggingface.co/docs/optimum/)

---

*Material elaborado para a disciplina de Engenharia de Machine Learning — FIAP PosTech.*
