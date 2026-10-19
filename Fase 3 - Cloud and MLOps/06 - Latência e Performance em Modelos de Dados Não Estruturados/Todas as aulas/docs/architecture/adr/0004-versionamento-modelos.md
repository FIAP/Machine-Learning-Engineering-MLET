# ADR-0004: Estrategia de Versionamento de Modelos

## Status

Aceito

## Data

2026-03-01

## Contexto

A disciplina envolve multiplos ciclos de treinamento, otimizacao (pruning, quantizacao, distillation) e fine-tuning (PEFT). Cada iteracao gera artefatos distintos (pesos FP32, ONNX, TensorRT engine, LoRA adapters) que precisam ser rastreados com:

- Versionamento de modelos e artefatos (pesos, configs, metricas)
- Rastreamento de experimentos (hiperparametros, metricas de acuracia E latencia)
- Linhagem completa (dataset versao X → modelo versao Y → deploy Z)
- Suporte a multiplos formatos de artefato (PyTorch, ONNX, TensorRT, TFLite)
- Integracao com pipeline de CI/CD para deployment automatizado

## Decisao

Adotar **MLflow** como plataforma principal de experiment tracking e model registry, complementado por **DVC** para versionamento de datasets.

1. **MLflow Tracking** — Registro de experimentos (hiperparametros, metricas de acuracia, metricas de latencia P50/P95/P99)
2. **MLflow Model Registry** — Versionamento de modelos com stages (Staging → Production → Archived) e metadados de latencia
3. **DVC** — Versionamento de datasets integrado ao Git (data lineage)
4. **Azure ML** — Integracao para deployment de modelos registrados em Managed Online Endpoints

## Consequencias

### Positivas

- MLflow e open-source, framework-agnostico e integra-se com PyTorch, TensorFlow e scikit-learn
- Tracking de metricas de latencia (P50/P95/P99) junto com metricas de ML permite decisoes baseadas no trade-off acuracia-latencia
- Model Registry com stages facilita o workflow de promotion (Staging → Production)
- DVC oferece versionamento de datasets sem armazenar dados no Git (pointers em Git, dados em remote storage)
- Integracao nativa MLflow → Azure ML para deployment gerenciado
- Suporte a logging de artefatos em multiplos formatos (PyTorch .pth, ONNX .onnx, TensorRT .engine)

### Negativas

- MLflow Tracking Server requer infraestrutura dedicada (ou Azure ML workspace)
- DVC + MLflow sao duas ferramentas com overlap parcial em tracking de artefatos
- MLflow Model Registry nao tem suporte nativo a diff de modelos (comparacao de pesos)
- Storage de artefatos grandes (modelos > 10GB) requer backend storage configurado (S3/Blob)

## Alternativas Consideradas

1. **DVC como solucao unica (tracking + registry)** — Rejeitada. DVC e excelente para versionamento de dados mas seu experiment tracking (DVC Experiments) e menos maduro que MLflow, especialmente para comparacao de metricas de latencia.
2. **Weights & Biases (W&B)** — Considerada. Superior em visualizacao e colaboracao, mas e SaaS proprietario com custos que escalam com volume. MLflow obedece ao principio de portabilidade open-source.
3. **Neptune.ai** — Rejeitada. Similar ao W&B em funcionalidade, mas com adocao menor e menor integracao com o ecossistema Azure.
4. **Custom (Git tags + scripts)** — Rejeitada. Nao escala para dezenas de experimentos com multiplas variantes de otimizacao. Falta de UI para comparacao e linhagem.

## Criterios de Avaliacao

| Criterio | Peso | MLflow + DVC | W&B | DVC only | Custom |
|----------|------|-------------|-----|----------|--------|
| Experiment Tracking | Alto | Excelente | Excelente | Bom | Basico |
| Model Registry | Alto | Nativo | Nativo | Parcial | Manual |
| Data Versioning | Alto | DVC (excelente) | Artifacts (bom) | Excelente | Manual |
| Open-source | Medio | Sim | Nao (SaaS) | Sim | Sim |
| Integracao Azure ML | Medio | Nativa | Plugin | Limitada | Manual |
| Metricas de Latencia | Medio | Custom logging | Custom logging | Limitado | Manual |

## Referencias

- [MLflow — Experiment Tracking & Model Registry](https://mlflow.org/docs/latest/index.html)
- [DVC — Data Version Control](https://dvc.org/doc)
- [Azure ML + MLflow Integration](https://learn.microsoft.com/en-us/azure/machine-learning/concept-mlflow)
- [ML Model Management Best Practices (Google)](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
