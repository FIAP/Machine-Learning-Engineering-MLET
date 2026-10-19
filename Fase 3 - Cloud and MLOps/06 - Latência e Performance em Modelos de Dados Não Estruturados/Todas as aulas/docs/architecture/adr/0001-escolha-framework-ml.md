# ADR-0001: Escolha de Frameworks de Machine Learning

## Status

Aceito

## Data

2026-03-01

## Contexto

A disciplina requer frameworks de ML que suportem o desenvolvimento, otimizacao e deployment de modelos para dados nao estruturados (texto, imagem, audio, video) com foco em **minimizacao de latencia**. O framework escolhido precisa:

- Suportar treinamento e inferencia de redes neurais profundas (CNNs, Transformers, LLMs)
- Oferecer ferramentas nativas de otimizacao (quantizacao, pruning, mixed precision)
- Integrar-se com aceleradores de hardware (GPU CUDA, Tensor Cores, TPU)
- Ter ecossistema maduro para serving em producao (TorchServe, Triton, vLLM)
- Permitir PEFT (LoRA, QLoRA) e otimizacao de grafos computacionais

## Decisao

Adotar **PyTorch como framework principal**, com **TensorFlow/Keras como framework complementar** e **scikit-learn para tarefas classicas** de ML.

**Justificativa:**

- **PyTorch** domina a pesquisa em ML (>70% dos papers em NeurIPS/ICML 2024) e possui o melhor ecossistema para otimizacao de latencia: `torch.compile` (Dynamo + Inductor), quantizacao nativa (`torch.quantization`), pruning (`torch.nn.utils.prune`), mixed precision (AMP), e integracao direta com Hugging Face (Transformers, PEFT, bitsandbytes).
- **TensorFlow/Keras** e mantido para cenarios especificos: TFLite para deployment mobile/edge, e TF Serving para serving em producao existente.
- **scikit-learn** e utilizado para modelos classicos (baselines), pre-processamento e avaliacao, onde a latencia de inferencia e intrinsecamente baixa.

## Consequencias

### Positivas

- Ecossistema unificado com Hugging Face para NLP, Visao e Audio
- `torch.compile` oferece compilacao JIT com speedups de 1.5-3x em inferencia
- Suporte nativo a mixed precision (FP16, BF16, TF32) via AMP
- Integracao direta com NVIDIA TensorRT via `torch_tensorrt`
- Comunidade ativa e rapida adocao de tecnicas de ponta (Flash Attention, PagedAttention)
- vLLM e TGI utilizam PyTorch como backend para serving de LLMs

### Negativas

- Dois frameworks para manter (PyTorch + TensorFlow) aumentam carga cognitiva
- TensorFlow Lite e superior ao PyTorch Mobile para deployment em dispositivos moveis
- Curva de aprendizado para `torch.compile` e suas limitacoes (graph breaks)

## Alternativas Consideradas

1. **Apenas TensorFlow/Keras** — Rejeitada porque o ecossistema de otimizacao (PEFT, vLLM, Flash Attention) gravita fortemente para PyTorch. TF tem menos suporte para tecnicas de ponta em LLMs.
2. **JAX/Flax** — Rejeitada porque, apesar de excelente para TPUs e compilacao XLA, o ecossistema e menos maduro para serving em producao e PEFT. Comunidade menor no Brasil.
3. **Apenas PyTorch (sem TF)** — Quase aceita, mas TFLite para edge e TF Serving para cenarios legados justificam manter TF como complementar.

## Criterios de Avaliacao

| Criterio | Peso | PyTorch (Principal) | TensorFlow | JAX |
|----------|------|---------------------|------------|-----|
| Otimizacao de Latencia | Alto | Excelente (torch.compile, TRT) | Bom (XLA, TFLite) | Excelente (XLA) |
| Ecossistema PEFT/LLM | Alto | Excelente (HF, vLLM, TGI) | Limitado | Parcial |
| Serving em Producao | Alto | Excelente (Triton, vLLM) | Bom (TF Serving) | Limitado |
| Quantizacao/Pruning | Alto | Nativo + TensorRT | Nativo + TFLite | Parcial |
| Comunidade/Docs | Medio | Excelente | Bom | Em crescimento |
| Deploy Mobile/Edge | Medio | Bom (ExecuTorch) | Excelente (TFLite) | Limitado |

## Referencias

- [PyTorch 2.0 — torch.compile](https://pytorch.org/get-started/pytorch-2.0/)
- [Hugging Face Ecosystem](https://huggingface.co/docs)
- [vLLM: Efficient LLM Serving](https://docs.vllm.ai/)
- [TensorRT Integration for PyTorch](https://developer.nvidia.com/tensorrt)
- Papers With Code — Framework Trends 2024
