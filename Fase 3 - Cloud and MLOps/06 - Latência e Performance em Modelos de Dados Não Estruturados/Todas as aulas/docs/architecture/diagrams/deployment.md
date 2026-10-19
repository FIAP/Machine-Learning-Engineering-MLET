# Diagrama de Deployment

## Visao Geral

Opcoes de deployment para sistemas de inferencia de ML com dados nao estruturados, cobrindo cenarios cloud (Microsoft Azure), on-premises e edge. O foco esta na topologia que minimiza latencia enquanto mantem escalabilidade e resiliencia.

## Deployment em Cloud — Microsoft Azure

```mermaid
graph TB
    subgraph "Internet"
        USER[Usuarios/Clientes<br/>Web/Mobile/API]
    end

    subgraph "Azure Edge"
        FD[Azure Front Door<br/>CDN + WAF + SSL]
        APIM[Azure API Management<br/>Rate Limiting + Auth]
    end

    subgraph "Azure Kubernetes Service - AKS"
        subgraph "Ingress"
            ING[NGINX Ingress Controller]
        end

        subgraph "Application Pods"
            API1[FastAPI Pod 1<br/>Pre/Post Processing]
            API2[FastAPI Pod 2<br/>Pre/Post Processing]
            API3[FastAPI Pod N<br/>Pre/Post Processing]
        end

        subgraph "Inference Pods - GPU Node Pool"
            TRT1[Triton Server<br/>GPU T4 - TensorRT]
            TRT2[vLLM Server<br/>GPU A100 - PagedAttention]
            TRT3[Triton Server<br/>GPU T4 - TensorRT]
        end

        subgraph "Support Services"
            REDIS[(Redis Cache<br/>Azure Cache for Redis)]
            PROM[Prometheus + Grafana<br/>SLI/SLO Monitoring]
            KEDA_S[KEDA Autoscaler<br/>Latency-based]
        end

        HPA[Horizontal Pod Autoscaler]
    end

    subgraph "Azure Data Services"
        BLOB[(Azure Blob Storage<br/>Raw Data + Models)]
        ACR[Azure Container Registry]
        LAKE[(Azure Data Lake Gen2<br/>Training Data)]
        SQLDB[(Azure PostgreSQL<br/>Metadata + Logs)]
    end

    subgraph "Azure ML Services"
        AML[Azure Machine Learning<br/>Training + Registry]
        AMLEP[Azure ML Managed<br/>Online Endpoints]
    end

    subgraph "Observabilidade"
        APPINS[Application Insights<br/>Distributed Tracing]
        MONITOR[Azure Monitor<br/>Alerts + Dashboards]
    end

    USER --> FD
    FD --> APIM
    APIM --> ING
    ING --> API1
    ING --> API2
    ING --> API3
    API1 --> TRT1
    API2 --> TRT2
    API3 --> TRT3
    API1 --> REDIS
    API2 --> REDIS
    TRT1 --> BLOB
    TRT2 --> BLOB
    ACR --> API1
    ACR --> TRT1
    LAKE --> AML
    AML --> BLOB
    AML --> AMLEP
    HPA --> API1
    KEDA_S --> TRT1
    API1 --> APPINS
    TRT1 --> APPINS
    APPINS --> MONITOR
    PROM --> MONITOR
    API1 --> SQLDB
```

## Deployment On-Premises / Edge

```mermaid
graph TB
    subgraph "Edge Devices"
        CAM[Camera Industrial<br/>IP Camera]
        MIC[Microfone<br/>Audio Capture]
        SENSOR[Sensores IoT]
    end

    subgraph "Edge Server"
        EDGE_GW[Edge Gateway<br/>NVIDIA Jetson Orin]
        EDGE_INF[Inference Engine<br/>TensorRT INT8]
        EDGE_PRE[Pre-processing<br/>NVIDIA DALI]
        LOCAL_CACHE[(Local Cache<br/>SQLite)]
    end

    subgraph "On-Premises Data Center"
        LB_ON[Load Balancer<br/>HAProxy]
        APP_ON[Application Servers<br/>FastAPI x 3]
        GPU_ON[GPU Servers<br/>NVIDIA DGX/RTX]
        TRITON_ON[Triton Inference<br/>Server Cluster]
        NAS[(NAS Storage<br/>Models + Data)]
        MONITOR_ON[Prometheus + Grafana]
    end

    subgraph "Sync com Cloud"
        SYNC[Azure IoT Hub<br/>Data Sync]
        CLOUD_TRAIN[Azure ML<br/>Cloud Training]
        MODEL_PULL[Model Pull<br/>Periodic Update]
    end

    CAM --> EDGE_GW
    MIC --> EDGE_GW
    SENSOR --> EDGE_GW
    EDGE_GW --> EDGE_PRE
    EDGE_PRE --> EDGE_INF
    EDGE_INF --> LOCAL_CACHE
    EDGE_INF --> LB_ON

    LB_ON --> APP_ON
    APP_ON --> TRITON_ON
    TRITON_ON --> GPU_ON
    TRITON_ON --> NAS
    APP_ON --> MONITOR_ON

    LOCAL_CACHE --> SYNC
    SYNC --> CLOUD_TRAIN
    CLOUD_TRAIN --> MODEL_PULL
    MODEL_PULL --> NAS
    MODEL_PULL --> EDGE_INF
```

## Comparacao de Ambientes

| Aspecto | Cloud (Azure AKS) | On-Premises | Edge (Jetson/NPU) |
|---------|-------------------|-------------|---------------------|
| **Latencia de rede** | 10-50ms (com CDN) | < 5ms (LAN) | < 1ms (local) |
| **Latencia de inferencia** | 20-50ms (GPU T4/A100) | 20-50ms (GPU dedicada) | 30-100ms (TensorRT INT8) |
| **Escalabilidade** | Elastica (KEDA/HPA) | Limitada (capacidade fixa) | Fixa (por device) |
| **Custo** | Pay-as-you-go (OpEx) | CAPEX alto, OpEx baixo | CAPEX moderado |
| **Disponibilidade** | 99.95% (SLA Azure AKS) | Depende de infra local | Offline-first |
| **Modelos suportados** | Qualquer tamanho | Qualquer tamanho | Otimizados (INT8/INT4) |
| **Manutencao** | Gerenciada (PaaS) | Equipe interna | Atualizacao OTA |

## Estrategia de Deployment — CI/CD

```mermaid
flowchart LR
    DEV[Development<br/>Local Docker] --> TEST[Testing<br/>Unit + Integration<br/>+ Latency Benchmark]
    TEST --> STAGING[Staging<br/>Azure AKS Dev]
    STAGING --> CANARY[Canary Release<br/>5% Traffic]
    CANARY --> EVAL{Latency SLO<br/>e Accuracy OK?}
    EVAL -->|Sim| FULL[Full Rollout<br/>100% Traffic]
    EVAL -->|Nao| ROLLBACK[Rollback<br/>Versao Anterior]
    ROLLBACK --> DEV
```

## Requisitos de Infraestrutura

### Ambiente de Desenvolvimento
- Docker Desktop com GPU support (opcional)
- Python 3.10+ com venv
- 16GB RAM, 4 CPU cores minimo
- GPU NVIDIA com CUDA 12.0+ (recomendado)

### Ambiente de Staging
- Azure AKS com 1x GPU node (T4)
- Azure Cache for Redis (Basic)
- Azure Blob Storage (Hot tier)
- Azure ML Workspace

### Ambiente de Producao
- Azure AKS com GPU node pool (T4/A100, autoscaling 2-10 nodes)
- Azure Front Door (WAF enabled)
- Azure Cache for Redis (Premium, clustered)
- Azure Data Lake Storage Gen2
- Azure Monitor + Application Insights
- Azure ML Managed Online Endpoints (alternativa ao AKS)
