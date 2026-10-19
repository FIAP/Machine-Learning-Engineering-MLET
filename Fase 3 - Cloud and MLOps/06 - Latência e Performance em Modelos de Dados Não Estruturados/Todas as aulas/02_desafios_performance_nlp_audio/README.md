# Aula 02 — Desafios de Performance em NLP e Áudio

> Disciplina: Engenharia de Machine Learning — FIAP PosTech

---

## 🎯 Objetivos de Aprendizagem

Ao final desta aula o aluno será capaz de:

1. **Compreender** o pipeline de um assistente virtual de voz: ASR → NLP/LLM → busca → TTS.
2. **Explicar** de forma simples por que o mecanismo de self-attention tem complexidade **O(n²)**.
3. **Implementar** uma self-attention mínima (scaled dot-product) em NumPy.
4. **Medir** na prática como a latência da atenção cresce conforme o tamanho da pergunta.
5. **Interpretar** o impacto do gargalo O(n²) na experiência de tempo real.
6. **Reconhecer** alternativas eficientes (Sparse, Linear e Flash Attention) como caminhos para reduzir esse custo.

---

## � Caso de Uso

Um **assistente virtual de compras por voz**. O usuário pergunta em voz alta:

> 🗣️ *"Quais tênis de corrida leves custam menos de 500 reais?"*

Para responder **em poucos segundos**, o sistema executa o pipeline:

```
🎤 Voz → [ASR] → texto → [NLP/LLM] → intenção → [Busca] → resposta → [TTS] → 🔊 Fala
```

O maior gargalo costuma estar na etapa de **NLP/LLM**, por causa do mecanismo de atenção. É nele que a aula foca.

---

## 📖 Teoria-Chave

### Self-Attention — Complexidade Quadrática

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

A matriz de atenção $QK^T$ possui dimensões $n \times n$: cada token é comparado com **todos** os outros. Isso implica complexidade de tempo $O(n^2 \cdot d)$ e **memória** $O(n^2)$. Na prática, **dobrar** o tamanho da pergunta **quadruplica** o trabalho. (Vaswani et al., 2017)

### Alternativas eficientes

| Técnica | Ideia central | Ganho |
|---|---|---|
| **Sparse Attention** | cada token olha só para alguns tokens, não todos | menos comparações |
| **Linear Attention** | reorganiza a matemática para custo O(n) | escala linear |
| **Flash Attention** | otimiza o uso da memória da GPU (IO-awareness) | 2–4× mais rápido |

---

## 🛠️ Tecnologias Utilizadas

| Biblioteca        | Versão   | Uso                                  |
|-------------------|----------|--------------------------------------|
| Python            | ≥ 3.10   | Linguagem base                       |
| NumPy             | ≥ 1.24   | Álgebra linear, atenção em NumPy     |
| Matplotlib        | ≥ 3.7    | Visualizações                        |
| Jupyter           | ≥ 1.0    | Notebook interativo                  |

> O notebook desta aula é **leve e autocontido**: usa apenas `numpy` e `matplotlib`, sem GPU, internet ou datasets externos.

---

## 📂 Estrutura de Arquivos

```
02_desafios_performance_nlp_audio/
├── README.md                        # ← Você está aqui
├── requirements.txt                 # Dependências da aula (numpy, matplotlib, jupyter)
├── notebooks/
│   └── 00_assistente_virtual_latencia.ipynb  # Notebook único: latência da atenção O(n²)
└── outputs/
    └── figures/                     # (opcional) figuras exportadas
```

---

## 🚀 Como Executar

### 1. Instalar dependências

```bash
cd 02_desafios_performance_nlp_audio
pip install -r requirements.txt
```

O notebook usa apenas `numpy` e `matplotlib`; para rodá-lo você também precisa do `jupyter`.

### 2. Executar o notebook

```bash
jupyter notebook notebooks/00_assistente_virtual_latencia.ipynb
```

O notebook é autocontido e executa de ponta a ponta, cobrindo:

1. Contexto do assistente virtual de voz.
2. Explicação simples da complexidade O(n²) da atenção.
3. Implementação de uma self-attention mínima em NumPy.
4. Hands-on medindo a latência conforme a pergunta cresce.
5. Interpretação dos resultados e alternativas eficientes.

---

## 📊 Datasets

Esta versão simplificada **não depende de dataset externo**: os tensores usados na atenção são gerados sinteticamente com NumPy dentro do próprio notebook.

---

## 📚 Referências

Referências principais relacionadas aos conceitos da aula:

1. **Vaswani, A. et al.** (2017). Attention Is All You Need. *NeurIPS*, v. 30, p. 5998-6008.
2. **Dao, T. et al.** (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness. *NeurIPS*, v. 35.
3. **Dao, T.** (2023). FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning. *arXiv:2307.08691*.
4. **Tay, Y. et al.** (2022). Efficient Transformers: A Survey. *ACM Computing Surveys*, v. 55, n. 6.
5. **Radford, A. et al.** (2023). Robust Speech Recognition via Large-Scale Weak Supervision. *ICML*.
6. **Baevski, A. et al.** (2020). wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations. *NeurIPS*, v. 33.
7. **Shazeer, N.** (2019). Fast Transformer Decoding: One Write-Head is All You Need. *arXiv:1911.02150*.
8. **Katharopoulos, A. et al.** (2020). Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention. *ICML*.

---

## 🔗 Links Úteis

- [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/)
- [Flash Attention — GitHub](https://github.com/Dao-AILab/flash-attention)
- [Hugging Face Transformers — Documentação](https://huggingface.co/docs/transformers/)
- [Librosa — Documentação](https://librosa.org/doc/latest/)
- [faster-whisper — GitHub](https://github.com/SYSTRAN/faster-whisper)
- [PyTorch SDPA](https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)

---

*Material elaborado para a disciplina de Engenharia de Machine Learning — FIAP PósTech.*
*Última atualização: Março de 2026.*
