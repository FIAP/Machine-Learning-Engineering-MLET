# ADR-0003: Arquitetura de API para Serving de Modelos

## Status

Aceito

## Data

2026-03-01

## Contexto

Os modelos de ML treinados na disciplina precisam ser expostos como servicos de inferencia com **requisitos rigorosos de latencia** (P95 < 100ms para CV/Audio, TTFT < 300ms para LLMs). A camada de API precisa:

- Suportar inferencia sincrona de baixa latencia para modelos de visao e audio
- Suportar streaming de tokens para modelos de linguagem (LLMs)
- Oferecer dynamic batching para maximizar throughput da GPU
- Integrar-se com model serving engines (Triton, vLLM)
- Permitir monitoramento de SLIs/SLOs de latencia por endpoint

## Decisao

Adotar **FastAPI como camada de API REST** com integracao a **inference servers especializados**:

1. **FastAPI** — Gateway de API com pre/pos-processamento, autenticacao, rate limiting e roteamento
2. **NVIDIA Triton Inference Server** — Serving de modelos de CV e audio (TensorRT, ONNX) com dynamic batching
3. **vLLM** — Serving de LLMs com continuous batching e PagedAttention
4. Protocolo **REST (JSON)** para clientes gerais + **gRPC** para comunicacao interna API-Triton

## Consequencias

### Positivas

- FastAPI oferece performance competitiva (Uvicorn/ASGI) com latencia < 2ms de overhead por request
- Suporte nativo a Server-Sent Events (SSE) para streaming de tokens de LLMs
- Triton oferece dynamic batching transparente com ganhos de 2-5x em throughput
- vLLM com PagedAttention reduz TTFT em 3-5x comparado a serving naive de LLMs
- gRPC para comunicacao interna elimina overhead de serializacao JSON (protobuf e 3-10x mais rapido)
- Documentacao OpenAPI automatica (Swagger UI) para facilitar integracao

### Negativas

- Tres componentes de serving aumentam complexidade operacional
- gRPC requer definicao de `.proto` files e geracao de stubs
- Triton tem curva de aprendizado para configuracao de model repository e ensemble pipelines
- vLLM e especializado em LLMs — nao substitui Triton para modelos de CV/Audio

## Alternativas Consideradas

1. **Flask/Django REST** — Rejeitada. Flask e sincrono (WSGI) e adiciona 5-10ms de overhead por request comparado ao FastAPI (ASGI). Django e over-engineered para serving de inference.
2. **gRPC puro (sem REST)** — Rejeitada. gRPC e mais eficiente, mas clientes web/mobile requerem proxying (gRPC-Web). REST com JSON e mais acessivel para integracao. Solucao hibrida (REST externo + gRPC interno) oferece o melhor dos dois mundos.
3. **TorchServe** — Considerada. Integra-se bem com PyTorch, mas nao oferece continuous batching para LLMs nem PagedAttention. Triton + vLLM cobrem todos os cenarios com melhor performance.
4. **BentoML** — Considerada. Framework de serving elegante com batching adaptativo, mas nao oferece o nivel de otimizacao do Triton (TensorRT native) nem do vLLM (PagedAttention).
5. **Azure ML Managed Online Endpoints** — Complementar, nao substituto. Oferece serving gerenciado com autoscaling, mas sem controle fino sobre batching e KV-Cache. Pode ser usado em paralelo para cenarios mais simples.

## Criterios de Avaliacao

| Criterio | Peso | FastAPI + Triton + vLLM | Flask + TorchServe | BentoML | Azure ML Endpoints |
|----------|------|-------------------------|---------------------|---------|---------------------|
| Latencia P95 (CV) | Alto | < 50ms | ~80ms | ~60ms | ~70ms |
| TTFT (LLM) | Alto | < 300ms (PagedAttention) | > 1s | ~500ms | ~500ms |
| Dynamic Batching | Alto | Nativo (Triton) | Limitado | Adaptativo | Basico |
| Streaming (SSE) | Alto | Nativo (FastAPI) | Manual | Nativo | Nativo |
| Complexidade Ops | Medio | Alta (3 componentes) | Media | Baixa | Muito baixa |
| Flexibilidade | Medio | Maxima | Media | Media | Limitada |

## Referencias

- [FastAPI — Performance Benchmarks](https://fastapi.tiangolo.com/)
- [NVIDIA Triton Inference Server](https://developer.nvidia.com/triton-inference-server)
- [vLLM — Efficient LLM Serving with PagedAttention](https://docs.vllm.ai/)
- Kwon, W. et al. (2023). *Efficient Memory Management for Large Language Model Serving with PagedAttention*. SOSP.
- [Azure ML Online Endpoints](https://learn.microsoft.com/en-us/azure/machine-learning/concept-endpoints)
