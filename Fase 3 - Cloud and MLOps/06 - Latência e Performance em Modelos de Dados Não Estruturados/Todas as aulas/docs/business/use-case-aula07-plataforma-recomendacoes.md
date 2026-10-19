# Use Case — Aula 7: Plataforma de Recomendações — Serving Distribuído para Milhões de Usuários

## Contexto da Aula

**Aula 7 — Inferência Distribuída e Serving em Escala**

---

## Cenário

A **StreamFlix** é uma plataforma de streaming de vídeo com **15 milhões de usuários ativos** que opera um sistema de recomendação baseado em deep learning. O modelo de recomendação processa o histórico de visualização, preferências e contexto do usuário para gerar recomendações personalizadas em tempo real. Durante horários de pico (20h-23h), o sistema recebe até **50.000 requisições de inferência por segundo**.

O problema: um **único servidor GPU** (NVIDIA A100) consegue processar no máximo **~3.000 req/s** com latência aceitável (< 100ms P95). Para atender o pico de 50.000 req/s, é necessária uma infraestrutura de **serving distribuído** com auto-scaling inteligente.

---

## O Problema

```mermaid
graph LR
    subgraph "Cenário Atual (1 GPU)"
        USERS["15M Usuários<br/>Pico: 50K req/s"] --> LB["Load Balancer"]
        LB --> GPU1["1x A100<br/>Capacidade: 3K req/s"]
        GPU1 -->|"Overflow: 47K req/s"| DROP["❌ Requests Dropped<br/>Timeout / 503"]
    end

    style DROP fill:#ff6666
```

| Métrica | Requisito | 1 GPU (Atual) | Gap |
|---------|-----------|---------------|-----|
| Throughput | 50.000 req/s | 3.000 req/s | 17x abaixo |
| Latência P95 | < 100 ms | 85 ms (sem carga) | OK isolado, degrada sob carga |
| Latência P95 (pico) | < 100 ms | > 2.000 ms | 20x acima |
| Disponibilidade | 99.9% | ~94% (drops no pico) | Inaceitável |
| Custo/req | Minimizar | — | — |

---

## Solução: Arquitetura de Serving Distribuído

```mermaid
graph TB
    subgraph "Clientes"
        APP["Apps Mobile/Web/Smart TV"]
    end

    subgraph "Ingress"
        APP --> CDN["CDN<br/>(Cache de Recomendações<br/>TTL=5min)"]
        CDN --> GW["API Gateway<br/>Rate Limiting<br/>Auth"]
    end

    subgraph "Serving Layer — Triton + vLLM"
        GW --> LB["L7 Load Balancer<br/>(Round-Robin Weighted)"]
        LB --> T1["Triton Pod 1<br/>2x A10G"]
        LB --> T2["Triton Pod 2<br/>2x A10G"]
        LB --> T3["Triton Pod 3<br/>2x A10G"]
        LB --> TN["Triton Pod N<br/>(Auto-scaled)"]
    end

    subgraph "Otimizações"
        BATCH["Dynamic Batching<br/>max_batch=64<br/>max_delay=10ms"]
        PAGED["PagedAttention<br/>(vLLM)"]
        CB["Continuous Batching<br/>Não espera terminar<br/>batch inteiro"]
    end

    subgraph "Scaling"
        HPA["KEDA Autoscaler<br/>Métrica: GPU Utilization<br/>+ Queue Depth"]
        HPA --> T1
        HPA --> T2
        HPA --> T3
        HPA --> TN
    end

    subgraph "Cache Layer"
        T1 --> REDIS["Redis Cluster<br/>Cache de Embeddings<br/>+ Recomendações Recentes"]
        T2 --> REDIS
        T3 --> REDIS
        TN --> REDIS
    end

    BATCH -.-> T1
    PAGED -.-> T1
    CB -.-> T1
```

---

## Fluxo de uma Requisição

```mermaid
sequenceDiagram
    participant USER as Usuário
    participant CDN as CDN
    participant GW as API Gateway
    participant LB as Load Balancer
    participant TRITON as Triton Pod
    participant CACHE as Redis Cache
    participant MODEL as Modelo RecomendaçãoM

    USER->>CDN: GET /recommendations?user_id=123
    
    alt Cache Hit (CDN)
        CDN-->>USER: Recomendações cached (< 5ms)
    else Cache Miss
        CDN->>GW: Forward request
        GW->>GW: Auth + Rate Limit check
        GW->>LB: Route to serving layer
        LB->>TRITON: Assign to least-loaded pod
        
        TRITON->>CACHE: Check embedding cache
        alt Cache Hit (Redis)
            CACHE-->>TRITON: User embedding cached
        else Cache Miss
            TRITON->>MODEL: Compute user embedding
            MODEL-->>TRITON: Embedding vector
            TRITON->>CACHE: Store embedding (TTL=1h)
        end
        
        TRITON->>MODEL: Dynamic Batch inference
        Note over TRITON,MODEL: Batch acumula até 64 requests<br/>ou timeout 10ms
        MODEL-->>TRITON: Top-K recomendações
        TRITON-->>LB: Response
        LB-->>GW: Response
        GW-->>CDN: Response (cache TTL=5min)
        CDN-->>USER: Recomendações personalizadas
    end
```

---

## Comparação de Estratégias de Serving

| Estratégia | Throughput | Latência P95 | Custo Relativo | Complexidade |
|------------|------------|-------------- |----------------|--------------|
| 1 GPU, sem batching | 1.000 req/s | 50 ms | 1x | Baixa |
| 1 GPU, dynamic batching | 3.000 req/s | 85 ms | 1x | Baixa |
| **4 GPUs, dynamic batching** | 12.000 req/s | 90 ms | 4x | Média |
| **N GPUs + auto-scaling** | **50.000+ req/s** | **75 ms** | **~8x base** | Alta |
| N GPUs + CDN cache | 50.000+ req/s | **< 10 ms (cache hit)** | ~6x base | Alta |
| Continuous Batching (vLLM) | +40% vs. static | -20% vs. static | Mesmo | Média |
| PagedAttention (vLLM) | +2x memória efetiva | Similar | -30% GPUs | Média |

---

## Desafios Técnicos Abordados na Aula

| Desafio | Conceito da Aula 7 |
|---------|---------------------|
| Uma GPU não suporta o pico de requests | Inferência distribuída: model parallelism vs. data parallelism |
| Batching estático desperdiça latência | Dynamic batching: acumular requests até max_batch ou timeout |
| Modelos generativos bloqueiam o batch inteiro | Continuous batching: liberar slots conforme cada request termina |
| Memória GPU fragmentada em KV-cache | PagedAttention (vLLM): paginação virtual para KV-cache |
| Auto-scaling reativo demora para escalar | KEDA: scaling baseado em queue depth + GPU utilization |
| Orquestração de múltiplos modelos | Triton Inference Server: model versioning, ensemble pipelines |
| Deploy multi-cloud/hybrid | KServe: abstração de serving sobre Kubernetes |
| Monitoramento SLI/SLO em escala | Métricas: throughput, latência P50/P95/P99, error rate, GPU util |

---

## Escalonamento Automático

```mermaid
graph LR
    subgraph "Métricas de Entrada"
        M1["GPU Utilization > 70%"]
        M2["Queue Depth > 100"]
        M3["Latência P95 > 80ms"]
    end

    subgraph "KEDA Autoscaler"
        M1 --> KEDA["ScaledObject<br/>minReplicas: 4<br/>maxReplicas: 20<br/>cooldown: 300s"]
        M2 --> KEDA
        M3 --> KEDA
    end

    subgraph "Ação"
        KEDA -->|"Scale Up"| UP["Novo Triton Pod<br/>Tempo: ~60s<br/>(imagem pre-pulled)"]
        KEDA -->|"Scale Down"| DOWN["Graceful Drain<br/>Finish in-flight requests<br/>Remove pod"]
    end
```

---

## Tecnologias Relacionadas

- **Serving:** Triton Inference Server, vLLM, TorchServe, KServe
- **Orquestração:** Kubernetes (AKS), KEDA (autoscaling)
- **Otimizações:** Dynamic Batching, Continuous Batching, PagedAttention
- **Cache:** Redis Cluster, CDN (Azure Front Door)
- **Monitoramento:** Prometheus, Grafana, Azure Monitor
- **Model Parallelism:** Tensor Parallelism, Pipeline Parallelism
- **Load Balancing:** NGINX, Envoy, Azure Application Gateway

---

## Conexões com Outras Aulas

| Aula | Relação |
|------|---------|
| Aula 1 | SLI/SLO: P95 < 100ms, throughput > 50K req/s, error rate < 0.1% |
| Aula 4 | Modelos quantizados (INT8) aumentam throughput por GPU em ~2x |
| Aula 5 | LoRA adapters permitem servir variantes do modelo sem duplicar memória |
| Aula 6 | Tensor Cores + TensorRT maximizam throughput por GPU |
| Aula 8 | Ensemble pipelines no Triton para orquestrar múltiplos modelos |

---

## Referências

- Crankshaw, D. et al. (2017). *Clipper: A Low-Latency Online Prediction Serving System*. NSDI.
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP.
- Yu, G. et al. (2022). *Orca: A Distributed Serving System for Transformer-Based Generative Models*. OSDI.
- NVIDIA (2024). *Triton Inference Server Documentation*.
- [KServe Documentation](https://kserve.github.io/website/)

---

📂 **Material da aula:** [Aula 7 — Inferência Distribuída e Serving em Escala](../../07_inferencia_distribuida/)
