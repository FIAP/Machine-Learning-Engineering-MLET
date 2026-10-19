# Aula 08 — Escalabilidade e Orquestração Multimodal

> Disciplina: Engenharia de Machine Learning — FIAP PosTech

---

## 🎯 Objetivos de Aprendizagem

Ao final desta aula o aluno será capaz de:

1. **Compreender** o problema de latência ponta a ponta em um pipeline multimodal com vários modelos.
2. **Explicar** de forma simples o que são **pipeline de inferência**, **orquestração**, **microsserviços** e **execução paralela**.
3. **Medir** na prática o tempo total e a latência de um pipeline multimodal.
4. **Comparar** a execução sequencial com a execução orquestrada (paralela).
5. **Avaliar** se a resposta cabe na meta de poucos segundos (< 1 s).
6. **Reconhecer** ferramentas e práticas reais de orquestração e MLOps (Airflow, Kubeflow, Triton, autoscaling) e seus trade-offs.

---

## 🧩 Caso de Uso

Um **assistente virtual multimodal**: o usuário faz uma pergunta **por voz** e anexa uma **imagem** para dar
mais contexto. O sistema executa um pipeline de vários modelos.

```
🎤 Voz ─► [ASR] ─► texto ─► [NLP] ─┐
                                    ├─► [Lógica] ─► resposta ─► [TTS] ─► 🔊 Fala
🖼️ Imagem ──────────► [Visão] ─────┘
```

Há **múltiplos modelos** e **etapas** que precisam ser coordenados: o ramo de **áudio (ASR+NLP)** e o ramo de
**imagem (Visão)** são **independentes** e podem rodar **em paralelo**. Rodando tudo em série, a latência passa
de 1 s; com **orquestração paralela**, cai para **< 1 s**. Somando otimização de cada modelo, microsserviços com
**autoscaling** e **MLOps** ativo, o sistema fica **rápido, escalável, modular e monitorado**. É nesse desafio
que a aula foca.

---

## 📖 Teoria-Chave

### Sequencial x Orquestrado (paralelo)

- **Sequencial:** cada etapa espera a anterior → tempo total é a **soma** de todas.
- **Orquestrado:** etapas **independentes** rodam ao mesmo tempo → o trecho concorrente custa o do **ramo mais
  lento**, não a soma.

| Cenário | Etapas | Latência total | Atende < 1 s? |
|---|---|---|---|
| Sequencial | 5 | ~1000+ ms | ❌ Depende |
| Orquestrado (paralelo) | 5 | ~700 ms | ✅ Sim |

### Ferramentas e práticas (referência)

| Técnica / Ferramenta | Ideia central | Ganho |
|---|---|---|
| **Airflow / Kubeflow** | orquestrar dependências e paralelismo | dispara ramos independentes juntos |
| **Microsserviços de inferência** | cada modelo como serviço via API | escalar/atualizar isoladamente |
| **Triton / TF Serving / TorchServe / BentoML** | servir modelos em produção | batching, múltiplas instâncias |
| **Autoscaling + balanceamento** | ajustar instâncias conforme a carga | aguenta picos de uso |
| **Monitoramento, CI/CD, feedback loop** | operar e evoluir modelos (MLOps) | qualidade e disponibilidade contínuas |
| **Edge x Cloud (híbrido)** | decidir onde roda cada parte | latência, custo e privacidade |

---

## 🛠️ Tecnologias Utilizadas

| Biblioteca | Versão | Uso |
|-----------|--------|-----|
| Python     | ≥ 3.10 | Linguagem base (inclui `concurrent.futures`) |
| NumPy      | ≥ 1.24 | Geração de ruído e estatísticas |
| Pandas     | ≥ 2.0  | Tabela comparativa |
| Matplotlib | ≥ 3.7  | Visualizações |
| Jupyter    | ≥ 1.0  | Notebook interativo |

> O notebook desta aula é **leve e autocontido**: usa apenas `numpy`, `pandas` e `matplotlib`, **sem GPU**,
> internet ou datasets externos.

---

## 📂 Estrutura de Arquivos

```
08_escalabilidade_orquestracao_multimodal/
├── README.md                                       # ← Você está aqui
├── requirements.txt                                # Dependências da aula
├── notebooks/
│   └── 00_assistente_multimodal_orquestracao.ipynb # Notebook único: sequencial x orquestrado (paralelo)
└── outputs/
    └── figures/                                    # (opcional) figuras exportadas
```

---

## 🚀 Como Executar

### 1. Instalar dependências

```bash
cd 08_escalabilidade_orquestracao_multimodal
pip install -r requirements.txt

# ou, o mínimo para este notebook:
pip install numpy pandas matplotlib jupyter
```

### 2. Executar o notebook

```bash
jupyter notebook notebooks/00_assistente_multimodal_orquestracao.ipynb
```

O notebook é autocontido e executa de ponta a ponta, cobrindo:

1. Contexto do assistente multimodal e a meta de resposta fluida (< 1 s).
2. Conceitos de pipeline, orquestração, microsserviços, execução paralela e MLOps.
3. Hands-on simulando dois cenários (pipeline sequencial × orquestrado/paralelo).
4. Comparação dos resultados em tabela e gráfico (tempo total ponta a ponta).
5. Discussão de ferramentas reais de orquestração/MLOps e seus trade-offs.
6. Conclusão sobre atender (ou não) à meta de latência com um sistema modular.

---

## 📊 Datasets

Esta versão simplificada **não depende de dataset externo**: os tempos de cada etapa são simulados
sinteticamente dentro do próprio notebook, permitindo medir latência ponta a ponta sem GPU.

---

## 📚 Referências

Referências principais relacionadas aos conceitos da aula:

1. **Sculley, D. et al.** (2015). Hidden Technical Debt in Machine Learning Systems. *NeurIPS 2015.*
2. **Baylor, D. et al.** (2017). TFX: A TensorFlow-Based Production-Scale ML Platform. *KDD 2017.*
3. **Baltrušaitis, T. et al.** (2019). Multimodal Machine Learning: A Survey and Taxonomy. *IEEE TPAMI.*
4. **Apache Airflow** (2020). Documentação oficial — DAGs e orquestração de tarefas.
5. **Kubeflow** (2021). Kubeflow Pipelines — orquestração de fluxos de ML em Kubernetes.

---

## 🔗 Links Úteis

- [Apache Airflow](https://airflow.apache.org/)
- [Kubeflow Pipelines](https://www.kubeflow.org/docs/components/pipelines/)
- [NVIDIA Triton Inference Server](https://developer.nvidia.com/triton-inference-server)
- [BentoML](https://www.bentoml.com/)
- [TorchServe](https://pytorch.org/serve/)

---

*Material elaborado para a disciplina de Engenharia de Machine Learning — FIAP PosTech.*
