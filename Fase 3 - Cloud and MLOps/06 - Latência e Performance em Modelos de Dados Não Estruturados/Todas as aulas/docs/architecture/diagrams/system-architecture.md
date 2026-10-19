# Diagrama de Arquitetura de Sistema End-to-End

## Visão Geral

Este diagrama representa a arquitetura completa do sistema de ML para dados não estruturados, desde a ingestão de dados brutos até a entrega de predições ao usuário final, com foco nos componentes que impactam latência em cada etapa.

## Arquitetura de Sistema

```mermaid
graph TB
    subgraph "Fontes de Dados"
        IMG[Imagens<br/>Cameras/Upload]
        AUD[Audio<br/>Microfone/Stream]
        TXT[Texto<br/>APIs/Formularios]
        VID[Video<br/>Streaming/Arquivos]
    end

    subgraph "Ingestao e Validacao"
        GW[API Gateway<br/>Azure API Management]
        VAL[Validacao de Input<br/>Schema + Limites]
        RATE[Rate Limiting<br/>Token Bucket]
    end

    subgraph "Pre-processamento"
        ROUTE{Tipo de Dado}
        RESIZE[Image Pipeline<br/>Resize + Normalize<br/>NVIDIA DALI]
        TOK[Text Pipeline<br/>Tokenizer + Padding<br/>SentencePiece/BPE]
        MFCC[Audio Pipeline<br/>Mel Spectrogram<br/>MFCC Extraction]
        VID_P[Video Pipeline<br/>Keyframe Extract<br/>Temporal Downsample]
    end

    subgraph "Cache Layer"
        REDIS[(Redis Cache<br/>Predicoes Frequentes)]
        EMB_CACHE[(Embedding Cache<br/>Vetores Pre-computados)]
    end

    subgraph "Inference Engine"
        LB[Load Balancer<br/>Latency-based Routing]
        BATCH[Dynamic Batcher<br/>Continuous Batching]
        INF_GPU[GPU Workers<br/>TensorRT/CUDA<br/>Tensor Cores FP16]
        INF_TRITON[Triton Server<br/>Model Ensemble]
        INF_VLLM[vLLM Server<br/>PagedAttention<br/>KV-Cache]
    end

    subgraph "Model Management"
        REG[Model Registry<br/>MLflow]
        OPT[Model Optimizer<br/>ONNX + TensorRT]
        QUANT[Quantization<br/>PTQ INT8/QAT]
        PRUNE[Pruning<br/>Structured/Unstructured]
        AB[A/B Testing<br/>Canary Deploy]
    end

    subgraph "Observabilidade"
        PROM[Prometheus<br/>Latency P50/P95/P99]
        GRAF[Grafana<br/>SLI/SLO Dashboards]
        ALERT[Alertmanager<br/>SLA Breach]
        TRACE[Distributed Tracing<br/>Jaeger]
    end

    subgraph "Orquestracao"
        K8S[Kubernetes - AKS]
        KSERVE[KServe<br/>Inference Service]
        HPA[Autoscaler<br/>Latency-based]
    end

    IMG --> GW
    AUD --> GW
    TXT --> GW
    VID --> GW

    GW --> VAL
    VAL --> RATE
    RATE --> ROUTE

    ROUTE -->|Imagem| RESIZE
    ROUTE -->|Texto| TOK
    ROUTE -->|Audio| MFCC
    ROUTE -->|Video| VID_P

    RESIZE --> REDIS
    TOK --> REDIS
    MFCC --> REDIS
    VID_P --> REDIS
    REDIS --> EMB_CACHE

    EMB_CACHE -->|Cache Miss| LB
    LB --> BATCH
    BATCH --> INF_GPU
    BATCH --> INF_TRITON
    BATCH --> INF_VLLM

    REG --> INF_TRITON
    OPT --> REG
    QUANT --> OPT
    PRUNE --> OPT
    AB --> LB

    INF_TRITON --> PROM
    INF_VLLM --> PROM
    LB --> PROM
    GW --> PROM
    PROM --> GRAF
    PROM --> ALERT
    GW --> TRACE
    INF_TRITON --> TRACE

    K8S --> KSERVE
    KSERVE --> INF_TRITON
    KSERVE --> INF_VLLM
    HPA --> K8S
    PROM --> HPA
```

## Budget de Latencia por Componente

| Camada | Componente | Latencia Alvo | SLA |
|--------|-----------|---------------|-----|
| API Gateway | Azure API Management + WAF | < 5ms | 99.99% |
| Validacao | Schema validation + rate limiting | < 2ms | 99.99% |
| Pre-processamento | Resize/Tokenize/MFCC (GPU DALI) | < 20ms | 99.95% |
| Cache | Redis lookup | < 1ms | 99.99% |
| Load Balancer | Latency-based routing | < 1ms | 99.99% |
| Inferencia (GPU) | TensorRT FP16/INT8 | < 50ms | 99.9% |
| Inferencia (LLM) | vLLM PagedAttention | < 200ms | 99.5% |
| Pos-processamento | Decode + format | < 5ms | 99.95% |
| **Total E2E (CV/Audio)** | **Request to Response** | **< 100ms** | **99.9%** |
| **Total E2E (LLM)** | **Request to First Token** | **< 300ms** | **99.5%** |
