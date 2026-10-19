# ADR-0005: Infraestrutura de Deployment

## Status

Aceito

## Data

2026-03-01

## Contexto

Os modelos otimizados precisam ser implantados em ambientes de producao com **requisitos rigorosos de latencia** (P95 < 100ms para CV/Audio, TTFT < 300ms para LLMs) e **escalabilidade elastica** para lidar com picos de trafego. A infraestrutura precisa:

- Suportar GPU nodes para inferencia com TensorRT e vLLM
- Oferecer autoscaling horizontol baseado em metricas de latencia
- Permitir canary deployments e A/B testing de modelos
- Integrar-se com o ecossistema Azure (AKS, Azure ML, Monitor)
- Suportar multiplos model serving engines (Triton, vLLM, FastAPI)

## Decisao

Adotar **Kubernetes (Azure AKS)** como plataforma principal de orquestracao, complementado por **Azure ML Managed Online Endpoints** para cenarios mais simples:

1. **Azure AKS** — Cluster Kubernetes gerenciado com GPU node pools (NVIDIA T4/A100)
2. **KServe** — Framework de serving de ML no Kubernetes com InferenceService, canary rollouts e autoscaling
3. **KEDA** — Event-driven autoscaling baseado em metricas customizadas (latencia P95, GPU utilization, queue depth)
4. **Azure ML Managed Online Endpoints** — Alternativa gerenciada para modelos que nao requerem controle fino sobre batching/KV-Cache

**Deployment strategy:** Canary releases com 5% → 25% → 100% de trafego, rollback automatico baseado em SLO de latencia.

## Consequencias

### Positivas

- AKS oferece GPU node pools gerenciados com autoscaling (0 a N nodes) — pagamento apenas por uso
- KServe fornece primitivas de ML serving (InferenceService, Transformer, Router) com canary nativo
- KEDA permite autoscaling baseado em metricas de latencia (nao apenas CPU/memoria) — crucial para workloads de inferencia
- AKS + Azure ML integracao permite usar Model Registry do MLflow para deployment direto
- Suporte a multi-model serving (Triton) e modelos especializados (vLLM) no mesmo cluster
- Canary com rollback automatico baseado em SLO reduz risco de deployment de modelo regressivo

### Negativas

- Kubernetes tem curva de aprendizado significativa (networking, RBAC, resource quotas)
- GPU nodes no AKS tem custo elevado (T4 ~$0.35/h, A100 ~$3.67/h — precos Azure)
- KServe + KEDA adicionam complexidade ao stack de orquestracao
- Manter dois paths de deployment (AKS + Azure ML Endpoints) requer documentacao e testes duplicados

## Alternativas Consideradas

1. **Serverless (Azure Functions / AWS Lambda)** — Rejeitada. Cold start de 5-30s e inaceitavel para requisitos de latencia < 100ms. Sem suporte a GPU. Inadequado para modelos de deep learning.
2. **Azure Container Instances (ACI)** — Rejeitada para producao. Util para desenvolvimento e testes, mas sem autoscaling sofisticado, sem GPU scheduling, e sem orquestracao de multiplos modelos.
3. **Azure ML Managed Online Endpoints apenas** — Rejeitada como solucao unica. Embora mais simples operacionalmente, nao oferece controle sobre batching strategy, KV-Cache management, ou multi-model serving que Triton e vLLM requerem.
4. **Self-hosted Kubernetes (kubeadm/k3s)** — Rejeitada. Overhead operacional de manter control plane, etcd, networking, e GPU drivers nao justifica a economia vs. AKS gerenciado.
5. **Docker Compose em VM** — Rejeitada. Sem autoscaling, sem canary deployments, sem health checks sofisticados. Aceitavel apenas para demos e desenvolvimento local.

## Criterios de Avaliacao

| Criterio | Peso | AKS + KServe | Serverless | ACI | Azure ML Endpoints | Docker Compose |
|----------|------|-------------|------------|-----|---------------------|----------------|
| Latencia P95 | Alto | < 100ms | 5-30s cold | ~100ms | ~100ms | ~100ms |
| GPU Support | Alto | Nativo (T4/A100) | Nao | Limitado | Nativo | Manual |
| Autoscaling | Alto | KEDA (latency-based) | Nativo (req-based) | Manual | Nativo (basic) | Nao |
| Canary Deploy | Alto | KServe nativo | Nao | Nao | Nativo | Manual |
| Complexidade Ops | Medio | Alta | Muito baixa | Baixa | Baixa | Muito baixa |
| Custo | Medio | Moderado-Alto | Pay-per-invocation | Moderado | Moderado | Baixo |

## Referencias

- [Azure AKS — GPU Node Pools](https://learn.microsoft.com/en-us/azure/aks/gpu-cluster)
- [KServe — ML Serving on Kubernetes](https://kserve.github.io/website/)
- [KEDA — Event-Driven Autoscaling](https://keda.sh/docs/)
- [Azure ML Managed Online Endpoints](https://learn.microsoft.com/en-us/azure/machine-learning/concept-endpoints)
- [Canary Deployments for ML Models (Google)](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
