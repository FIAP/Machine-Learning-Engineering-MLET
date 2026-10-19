# ADR-0002: Estrategia de Armazenamento de Dados

## Status

Aceito

## Data

2026-03-01

## Contexto

A disciplina trabalha com **dados nao estruturados** de grande volume (imagens em alta resolucao, audio em formato WAV, texto de documentos longos, streaming de video). O sistema de armazenamento precisa:

- Suportar armazenamento eficiente de blobs binarios (imagens, audio, video)
- Permitir acesso de baixa latencia para pipelines de pre-processamento e inferencia
- Integrar-se com pipelines de treinamento (batch reads de datasets)
- Oferecer versionamento de datasets para reprodutibilidade
- Escalar de gigabytes (prototipagem) a terabytes (producao)

## Decisao

Adotar uma **estrategia hibrida** com tres camadas:

1. **Azure Data Lake Storage Gen2** — Armazenamento primario de dados nao estruturados (raw data, datasets processados, artefatos de treinamento)
2. **Azure Blob Storage** — Artefatos de modelo (pesos, ONNX, TensorRT engines) com acesso rapido via CDN
3. **Redis (Azure Cache for Redis)** — Cache de embeddings pre-computados e predicoes frequentes para minimizar latencia de inferencia

**Versionamento de dados** via **DVC (Data Version Control)** integrado ao Git.

## Consequencias

### Positivas

- Data Lake Gen2 oferece namespace hierarquico com performance otimizada para big data (throughput > 10 GB/s)
- Blob Storage com tier Hot garante latencia < 10ms para download de artefatos de modelo
- Redis como cache de embeddings reduz latencia de inferencia repetida para < 1ms
- DVC permite reprodutibilidade completa de experimentos sem armazenar dados no Git
- Integracao nativa com Azure ML para pipelines de treinamento

### Negativas

- Tres sistemas de armazenamento aumentam complexidade operacional
- DVC requer configuracao adicional e disciplina no workflow
- Custo de Data Lake Gen2 pode ser significativo para datasets muito grandes (> 10 TB)
- Redis requer gerenciamento de politica de eviction e TTL

## Alternativas Consideradas

1. **PostgreSQL + extensoes binarias (pg_largeobject)** — Rejeitada. Bancos relacionais nao sao otimizados para armazenamento de blobs grandes. Latencia de leitura de imagens/audio significativamente superior ao Blob Storage.
2. **MongoDB GridFS** — Rejeitada. Embora suporte dados binarios, nao oferece o throughput do Data Lake Gen2 para datasets de treinamento e carece de integracao nativa com Azure ML.
3. **MinIO (S3-compatible)** — Considerada para cenarios on-premises. Viavel como alternativa local, mas nao oferece os servicos gerenciados (CDN, tiering, integracao com AKS) do ecossistema Azure.
4. **Delta Lake sobre Data Lake** — Complementar, nao substituto. Pode ser adotado no futuro para datasets tabulares derivados, mas dados raw nao estruturados seguem melhor como blobs.

## Criterios de Avaliacao

| Criterio | Peso | Data Lake + Blob + Redis | PostgreSQL | MongoDB GridFS | MinIO |
|----------|------|--------------------------|------------|----------------|-------|
| Latencia de leitura (blobs) | Alto | < 10ms (Blob Hot) | > 50ms | ~30ms | ~15ms |
| Throughput (treinamento) | Alto | > 10 GB/s | Limitado | Moderado | Bom |
| Cache de inferencia | Alto | < 1ms (Redis) | N/A | N/A | N/A |
| Versionamento de dados | Medio | DVC | Manual | Manual | DVC |
| Custo | Medio | Moderado | Baixo | Baixo | Baixo (self-hosted) |
| Gerenciamento | Medio | PaaS (gerenciado) | PaaS | Self-hosted | Self-hosted |

## Referencias

- [Azure Data Lake Storage Gen2 — Performance](https://learn.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-introduction)
- [Azure Cache for Redis — Best Practices](https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-best-practices)
- [DVC — Data Version Control](https://dvc.org/doc)
- [MLOps Data Management Patterns](https://ml-ops.org/content/data-management)
