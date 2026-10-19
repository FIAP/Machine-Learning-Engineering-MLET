# Aula 05 — Transfer Learning Eficiente: PEFT, LoRA e QLoRA

> Disciplina: Engenharia de Machine Learning — FIAP PosTech

---

## 🎯 Objetivos de Aprendizagem

Ao final desta aula o aluno será capaz de:

1. **Compreender** por que treinar um LLM do zero é inviável para uma startup com recursos limitados.
2. **Explicar** de forma simples o que são **transfer learning**, **fine-tuning completo** e **PEFT** (LoRA/QLoRA).
3. **Medir** na prática quantos **parâmetros treináveis** cada estratégia exige.
4. **Comparar** custo computacional e uso de memória entre fine-tuning completo, LoRA e QLoRA.
5. **Avaliar** qual estratégia é **viável** para o hardware disponível (1 GPU).
6. **Reconhecer** técnicas reais de adaptação (adapters, LoRA, QLoRA, prompt tuning) e seus trade-offs.

---

## 🧩 Caso de Uso

A startup **AdvogAI** usa IA para **resumir contratos jurídicos automaticamente**. Em vez de criar um modelo do
zero, ela **reutiliza um LLM pré-treinado** e o adapta ao domínio jurídico.

```
📄 Contrato → [LLM adaptado ao domínio jurídico] → 📝 Resumo das cláusulas
```

Treinar do zero exigiria bilhões de palavras, centenas de GPUs e meses de trabalho. O modelo precisa aprender
**termos jurídicos**, a **estrutura de contratos** e o **contexto legal**, mas a empresa possui apenas **1 ou 2
GPUs**, **orçamento limitado** e **prazos curtos**. A solução é a **adaptação eficiente** com **LoRA** e
**QLoRA** (LoRA + quantização 4 bits), que permite fazer fine-tuning em uma única GPU. É nesse desafio que a
aula foca.

---

## 📖 Teoria-Chave

### Transfer Learning e PEFT

- **Transfer learning:** reutilizar um modelo pré-treinado e ajustá-lo à tarefa alvo, economizando dados e tempo.
- **Fine-tuning completo:** atualiza **todos** os parâmetros — adaptação máxima, custo altíssimo.
- **PEFT:** ajusta apenas uma **pequena fração** dos parâmetros (< 3%), mantendo o modelo base congelado.

### LoRA em uma linha

Uma camada tem uma matriz de pesos `W` (`d × d`). O LoRA congela `W` e aprende duas matrizes pequenas
`A` (`d × r`) e `B` (`r × d`), com rank `r` pequeno (ex.: 8). Treina apenas `2·d·r` valores por camada.

| Estratégia | Parâmetros treinados | Memória | Viável em 1 GPU? |
|---|---|---|---|
| **Fine-tuning completo** | 100% | muito alta | ❌ Não |
| **LoRA** | < 1% | média | ⚠️ Depende |
| **QLoRA** (4 bits + LoRA) | < 1% | baixa | ✅ Sim |

### Técnicas de PEFT (referência)

| Técnica | Ideia central | Ganho |
|---|---|---|
| **Adapters** | camadas pequenas treináveis inseridas no modelo | poucos parâmetros extras |
| **LoRA** | matrizes de baixo rank (A e B) | treina < 1% dos parâmetros |
| **QLoRA** | LoRA + modelo base em 4 bits | cabe em 1 GPU |
| **Prompt/Prefix Tuning** | treinar só vetores de entrada | ajuste ultraleve |

---

## 🛠️ Tecnologias Utilizadas

| Biblioteca | Versão | Uso |
|-----------|--------|-----|
| Python     | ≥ 3.10 | Linguagem base |
| NumPy      | ≥ 1.24 | Cálculos de parâmetros e estatísticas |
| Pandas     | ≥ 2.0  | Tabela comparativa |
| Matplotlib | ≥ 3.7  | Visualizações |
| Jupyter    | ≥ 1.0  | Notebook interativo |

> O notebook desta aula é **leve e autocontido**: usa apenas `numpy`, `pandas` e `matplotlib`, **sem GPU**,
> internet ou datasets externos.

---

## 📂 Estrutura de Arquivos

```
05_transfer_learning_eficiente/
├── README.md                                # ← Você está aqui
├── requirements.txt                         # Dependências da aula
├── notebooks/
│   └── 00_advogai_transfer_learning.ipynb   # Notebook único: transfer learning, LoRA e QLoRA
└── outputs/
    └── figures/                             # (opcional) figuras exportadas
```

---

## 🚀 Como Executar

### 1. Instalar dependências

```bash
cd 05_transfer_learning_eficiente
pip install -r requirements.txt

# ou, o mínimo para este notebook:
pip install numpy pandas matplotlib jupyter
```

### 2. Executar o notebook

```bash
jupyter notebook notebooks/00_advogai_transfer_learning.ipynb
```

O notebook é autocontido e executa de ponta a ponta, cobrindo:

1. Contexto da startup AdvogAI e o desafio de adaptar um LLM com poucos recursos.
2. Conceitos de transfer learning, fine-tuning completo e PEFT (adapters, LoRA, QLoRA, prompt tuning).
3. Hands-on simulando três estratégias (fine-tuning completo × LoRA × QLoRA).
4. Comparação dos resultados em tabela e gráficos (parâmetros treináveis, custo, memória).
5. Discussão de técnicas reais de adaptação e seus trade-offs.
6. Conclusão sobre a viabilidade de cada estratégia para a startup.

---

## 📊 Datasets

Esta versão simplificada **não depende de dataset externo**: os números de parâmetros e a memória são
calculados/simulados dentro do próprio notebook, permitindo comparar estratégias sem GPU.

---

## 📚 Referências

Referências principais relacionadas aos conceitos da aula:

1. **Houlsby, N. et al.** (2019). Parameter-Efficient Transfer Learning for NLP. *ICML 2019.*
2. **Hu, E. et al.** (2021). LoRA: Low-Rank Adaptation of Large Language Models. *arXiv:2106.09685.*
3. **Dettmers, T. et al.** (2023). QLoRA: Efficient Finetuning of Quantized LLMs. *NeurIPS 2023.*
4. **Li, X. L. & Liang, P.** (2021). Prefix-Tuning: Optimizing Continuous Prompts for Generation. *ACL 2021.*
5. **Lester, B. et al.** (2021). The Power of Scale for Parameter-Efficient Prompt Tuning. *EMNLP 2021.*

---

## 🔗 Links Úteis

- [Hugging Face PEFT](https://huggingface.co/docs/peft/)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [QLoRA Paper](https://arxiv.org/abs/2305.14314)
- [bitsandbytes (quantização 4 bits)](https://github.com/TimDettmers/bitsandbytes)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)

---

*Material elaborado para a disciplina de Engenharia de Machine Learning — FIAP PosTech.*
