# Aula 01 — Fundamentos de Latência e Performance em ML

## 💼 Caso de Uso: Detecção de Fraude Bancária em Tempo Real

Toda a aula é construída em torno de **um único cenário aplicado**: um sistema
antifraude que analisa transações de cartão à medida que acontecem. Se uma
transação fraudulenta demora a ser sinalizada — ou seja, se a latência da
decisão é alta — o débito já caiu, o banco perde dinheiro e o cliente perde
confiança. O objetivo do produto é direto: **reduzir o tempo de resposta a
praticamente zero do ponto de vista do usuário**, mantendo qualidade de
detecção compatível com SLAs do mercado de pagamentos (tipicamente
P99 ≤ 50 ms ponta-a-ponta, com a inferência do modelo respondendo em poucos
milissegundos).

O notebook da aula usa um **dataset sintético de transações** e responde a
uma pergunta central sob vários ângulos: *quanto tempo o nosso modelo leva
para decidir, onde estão os gargalos e qual configuração aceita o SLA
real-time?*

## 🎯 Objetivos de Aprendizagem

Ao final desta aula, o aluno será capaz de:

1. **Compreender** os conceitos fundamentais de latência e throughput em sistemas de ML
2. **Medir** e **perfilar** o tempo de execução de cada etapa do pipeline de ML (pré-processamento, inferência, pós-processamento)
3. **Analisar** percentis de latência (P50, P95, P99) e sua importância em ambientes de produção
4. **Comparar** a complexidade computacional de diferentes algoritmos de ML e seu impacto na latência
5. **Avaliar** o efeito do tamanho de batch na relação latência-throughput
6. **Implementar** benchmarks reproduzíveis para pipelines de ML
7. **Identificar** gargalos de performance usando técnicas de profiling

## 📖 Teoria-Chave

### Latência em Sistemas de ML

A **latência** é o tempo total decorrido desde que uma requisição é recebida até que a resposta seja
entregue. Em sistemas de ML em produção, a latência end-to-end é composta por:

$$L_{total} = L_{rede} + L_{pre} + L_{inferencia} + L_{pos} + L_{serializacao}$$

Onde cada componente contribui para o tempo total de resposta. Conforme Crankshaw et al. (2017),
a latência de inferência é frequentemente o componente dominante, mas otimizações no
pré-processamento podem render ganhos significativos.

### Throughput vs. Latência

O **throughput** (vazão) mede o número de predições por unidade de tempo. Existe um trade-off
fundamental entre latência e throughput:

- **Batching** aumenta throughput mas pode aumentar latência individual
- **Paralelismo** pode melhorar ambos, mas com retornos decrescentes
- O **ponto ótimo** depende dos SLAs (Service Level Agreements) da aplicação

### Percentis de Latência

Em produção, a **latência média** é insuficiente. Métricas críticas incluem:

| Métrica | Descrição | Uso típico |
|---------|-----------|------------|
| P50 | Mediana | Experiência típica do usuário |
| P95 | 95º percentil | Performance sob carga |
| P99 | 99º percentil | Worst-case para SLAs |
| P99.9 | 99.9º percentil | Tail latency |

Conforme Dean & Barroso (2013), "The Tail at Scale", tail latencies são particularmente
problemáticas em sistemas distribuídos devido ao efeito de amplificação.

### Complexidade de Modelos

A complexidade computacional de diferentes algoritmos impacta diretamente a latência:

| Algoritmo | Complexidade de Inferência | Observação |
|-----------|---------------------------|------------|
| Regressão Logística | O(d) | Linear no nº de features |
| Random Forest | O(t · log n) | t = nº árvores |
| Gradient Boosting | O(t · profundidade) | Sequencial por natureza |
| SVM (kernel RBF) | O(n_sv · d) | n_sv = support vectors |

## 🛠️ Tecnologias Utilizadas

| Biblioteca | Versão | Uso |
|-----------|--------|-----|
| Python | ≥3.10 | Linguagem base |
| NumPy | ≥1.24.0 | Computação numérica |
| Pandas | ≥2.0.0 | Manipulação de dados |
| scikit-learn | ≥1.3.0 | Modelos de ML |
| Matplotlib | ≥3.7.0 | Visualizações |
| Seaborn | ≥0.12.0 | Gráficos estatísticos |
| psutil | ≥5.9.0 | Monitoramento de recursos |
| pytest | ≥7.4.0 | Testes unitários |

## 📂 Estrutura de Arquivos

```
01_fundamentos_latencia_performance_ml/
├── README.md                        # Este arquivo
├── requirements.txt                 # Dependências da aula
├── notebooks/
│   └── 01_fundamentos_latencia_inferencia.ipynb  # Notebook principal da aula
├── src/
│   ├── __init__.py                  # Inicialização do pacote
│   ├── data_preprocessing.py        # Pré-processamento e geração de dados
│   └── utils.py                     # Utilitários (save/load, configs)
├── data/
│   ├── raw/
│   │   └── dataset.csv              # Dataset sintético de classificação
│   ├── processed/                   # Dados processados (gerado em runtime)
│   └── README.md                    # Documentação do dataset
├── tests/
│   ├── __init__.py
│   └── test_preprocessing.py        # Testes do pré-processamento
└── outputs/
    ├── models/                      # Modelos serializados
    ├── figures/                     # Gráficos gerados
    └── logs/                        # Logs de benchmark
```

## 🚀 Como Executar

### 1. Instalação de Dependências

```bash
cd 01_fundamentos_latencia_performance_ml
pip install -r requirements.txt
```

### 2. Gerar Dataset (se necessário)

```bash
python -c "from src.data_preprocessing import DataPreprocessor; DataPreprocessor.generate_synthetic_dataset('data/raw/dataset.csv')"
```

### 3. Executar Notebook

```bash
jupyter notebook notebooks/01_fundamentos_latencia_inferencia.ipynb
```

### 4. Executar via Scripts Python

```bash
# Pipeline completo
python -m src.training
```

## 📊 Datasets

O dataset utilizado é **sintético** e simula um stream de transações de cartão
para um sistema de detecção de fraude em tempo real (consulte
[data/README.md](data/README.md) para detalhes completos das colunas).

- **Transações:** 10.000
- **Features:** 15 numéricas (valor, hora, distância, velocidade, scores de risco…)
- **Target:** Binário (`0` = legítima, `1` = fraude), desbalanceado (~95% / ~5%)

## 🧪 Testes

```bash
# Executar todos os testes
pytest tests/ -v

# Executar com cobertura
pytest tests/ -v --tb=short
```

## 📚 Referências

1. **Crankshaw, D. et al.** (2017). "Clipper: A Low-Latency Online Prediction Serving System."
   *NSDI '17*.
2. **Dean, J. & Barroso, L. A.** (2013). "The Tail at Scale."
   *Communications of the ACM*, 56(2), 74–80.
3. **Reddi, V. J. et al.** (2020). "MLPerf Inference Benchmark."
   *ISCA '20*.
4. **Sculley, D. et al.** (2015). "Hidden Technical Debt in Machine Learning Systems."
   *NeurIPS '15*.
5. **Li, M. et al.** (2014). "Scaling Distributed Machine Learning with the Parameter Server."
   *OSDI '14*.

## 🔗 Links Úteis

- [scikit-learn: Model Complexity & Performance](https://scikit-learn.org/stable/auto_examples/applications/plot_prediction_latency.html)
- [MLPerf Inference Benchmark](https://mlcommons.org/en/inference-datacenter-11/)
- [Google Cloud: ML Latency Best Practices](https://cloud.google.com/architecture/minimizing-predictive-serving-latency-in-machine-learning)
- [Python Profiling Tools](https://docs.python.org/3/library/profile.html)
