# Diagrama de Fluxo de Dados

## Visao Geral

Fluxo completo dos dados desde a ingestao bruta (imagens, textos, audio) ate a predicao final, detalhando as transformacoes e pontos de decisao que impactam latencia em cada etapa.

## Fluxo de Dados — Ingestao ate Predicao

```mermaid
flowchart TD
    subgraph "1 - Ingestao de Dados"
        A1[Upload de Imagem<br/>JPEG/PNG/WebP] --> V1{Validacao<br/>Formato e Tamanho}
        A2[Stream de Audio<br/>WAV/MP3/FLAC] --> V2{Validacao<br/>Sample Rate}
        A3[Texto<br/>UTF-8] --> V3{Validacao<br/>Encoding e Length}
        A4[Stream de Video<br/>MP4/RTSP] --> V4{Validacao<br/>Codec e Resolucao}

        V1 -->|Valido| B1[Buffer de Ingestao]
        V2 -->|Valido| B1
        V3 -->|Valido| B1
        V4 -->|Valido| B1
        V1 -->|Invalido| ERR[Erro 422]
        V2 -->|Invalido| ERR
        V3 -->|Invalido| ERR
        V4 -->|Invalido| ERR
    end

    subgraph "2 - Pre-processamento"
        B1 --> ROUTE{Tipo de Dado}

        ROUTE -->|Imagem| IMG_P[Resize 224x224<br/>Normalize 0-1<br/>Channel Reorder HWC-CHW]
        ROUTE -->|Audio| AUD_P[Resample 16kHz<br/>Mel Spectrogram<br/>Segment 30s Windows]
        ROUTE -->|Texto| TXT_P[Tokenizacao BPE<br/>Padding/Truncation<br/>Attention Mask]
        ROUTE -->|Video| VID_P[Keyframe Extraction<br/>Temporal Downsample<br/>Frame Resize]

        IMG_P --> TENSOR[Tensor float32/float16]
        AUD_P --> TENSOR
        TXT_P --> TENSOR
        VID_P --> TENSOR
    end

    subgraph "3 - Cache e Deduplicacao"
        TENSOR --> HASH[Embedding Hash<br/>Locality-Sensitive]

        HASH --> CACHE{Cache Hit?}
        CACHE -->|Hit| CACHED_RES[Resultado Cacheado]
        CACHE -->|Miss| QUEUE[Fila de Inferencia]
    end

    subgraph "4 - Inferencia"
        QUEUE --> BATCHER[Dynamic Batcher<br/>Continuous Batching]
        BATCHER --> HW{Hardware}

        HW -->|GPU Tensor Cores| INF_GPU[Inferencia TensorRT<br/>FP16/INT8]
        HW -->|vLLM| INF_LLM[LLM Inference<br/>PagedAttention<br/>KV-Cache]
        HW -->|CPU Fallback| INF_CPU[ONNX Runtime<br/>INT8 Quantized]

        INF_GPU --> RAW_PRED[Logits/Probabilidades]
        INF_LLM --> RAW_PRED
        INF_CPU --> RAW_PRED
    end

    subgraph "5 - Pos-processamento"
        RAW_PRED --> POST[Pos-processamento]
        POST --> SOFTMAX[Softmax/Argmax<br/>Beam Search/Sampling]
        SOFTMAX --> THRESHOLD{Confianca >= Threshold?}

        THRESHOLD -->|Sim| RESULT[Resultado Final<br/>Label + Score]
        THRESHOLD -->|Nao| UNCERTAIN[Low Confidence<br/>Flag para Review]
    end

    subgraph "6 - Logging e Feedback Loop"
        RESULT --> LOG_STORE[(Prediction Log<br/>Azure Data Lake)]
        UNCERTAIN --> LOG_STORE
        CACHED_RES --> RESP[API Response<br/>JSON]
        RESULT --> RESP
        UNCERTAIN --> RESP
        LOG_STORE --> DRIFT[Drift Detection<br/>PSI/KL Divergence]
        DRIFT --> RETRAIN{Drift Detectado?}
        RETRAIN -->|Sim| TRIGGER[Trigger Retraining]
        RETRAIN -->|Nao| CONTINUE[Continuar Monitoramento]
    end
```

## Fluxo de Dados de Treinamento e Otimizacao

```mermaid
flowchart LR
    subgraph "Coleta"
        RAW[Raw Data] --> LABEL[Labeling Tool]
        LABEL --> STORE[(Data Lake<br/>DVC Versioned)]
    end

    subgraph "Preparacao"
        STORE --> SPLIT[Train/Val/Test<br/>Stratified Split]
        SPLIT --> AUG[Data Augmentation<br/>Albumentations/NLPAug]
        AUG --> FEAT[Feature Engineering<br/>Embeddings Pre-computados]
    end

    subgraph "Treinamento"
        FEAT --> TRAIN[Training<br/>PyTorch + AMP FP16]
        TRAIN --> EVAL[Evaluation<br/>Accuracy + Latency P95]
        EVAL --> PEFT_FT[PEFT Fine-tuning<br/>LoRA/QLoRA]
    end

    subgraph "Otimizacao"
        PEFT_FT --> PRUNE[Pruning<br/>Structured]
        PRUNE --> QUANT[Quantization<br/>PTQ INT8 / QAT]
        QUANT --> DISTILL[Knowledge Distillation<br/>Teacher-Student]
        DISTILL --> EXPORT[Export<br/>ONNX/TorchScript/TFLite]
    end

    subgraph "Registry e Deploy"
        EXPORT --> BENCH[Benchmark<br/>Latency P50/P95/P99]
        BENCH --> REG[(Model Registry<br/>MLflow)]
        REG --> DEPLOY[Deploy<br/>Triton/vLLM/KServe]
    end
```

## Metricas por Etapa do Fluxo

| Etapa | Metrica Principal | Alvo | Formato de Dado |
|-------|------------------|------|-----------------|
| Ingestao | Throughput (req/s) | > 1000 | Raw binary |
| Validacao | Rejection rate (%) | < 5% | Raw binary |
| Pre-processamento | Latencia (ms) | < 20ms | Tensor float32/float16 |
| Cache Lookup | Latencia (ms) | < 1ms | Hash key |
| Dynamic Batching | Batch fill rate (%) | > 80% | Tensor batch |
| Inferencia GPU (CV) | Latencia P95 (ms) | < 50ms | Tensor float16/int8 |
| Inferencia LLM | TTFT (ms) | < 300ms | Token sequence |
| Inferencia CPU | Latencia P95 (ms) | < 200ms | Tensor int8 |
| Pos-processamento | Latencia (ms) | < 5ms | JSON |
| **Total E2E** | **Latencia P95** | **< 100ms (CV)** | **JSON** |
