# Jornada do Usuario — Cientista de Dados / ML Engineer

## Visao Geral

Diagrama da jornada do aluno/profissional utilizando este repositorio para desenvolver um projeto de ML com foco em latencia e performance, desde a escolha do problema ate o deployment em producao.

## Jornada do Usuario pelo Repositorio

```mermaid
journey
    title Jornada do ML Engineer pelo Repositorio
    section Fundamentos (Semana 1)
        Ler README.md e entender estrutura: 5: Aluno
        Estudar Aula 1 - Metricas de Latencia: 4: Aluno
        Configurar ambiente Python + GPU: 3: Aluno
        Executar profiling de modelo baseline: 4: Aluno
    section Modelos por Modalidade (Semanas 2-3)
        Estudar Aula 2 - NLP e Audio: 4: Aluno
        Implementar pipeline ASR com Whisper: 3: Aluno
        Estudar Aula 3 - Visao Computacional: 4: Aluno
        Treinar modelo de classificacao com ViT: 4: Aluno
    section Otimizacao (Semanas 4-5)
        Estudar Aula 4 - Pruning e Quantizacao: 4: Aluno
        Aplicar PTQ INT8 no modelo treinado: 5: Aluno
        Estudar Aula 5 - PEFT e LoRA: 4: Aluno
        Fine-tune LLM com QLoRA: 5: Aluno
    section Hardware e Distribuicao (Semanas 6-7)
        Estudar Aula 6 - GPU e Aceleradores: 4: Aluno
        Profiling com NVIDIA Nsight: 3: Aluno
        Estudar Aula 7 - Inferencia Distribuida: 4: Aluno
        Deploy com Triton e vLLM: 4: Aluno
    section Producao (Semana 8)
        Estudar Aula 8 - Orquestracao Multimodal: 5: Aluno
        Deploy pipeline multimodal no AKS: 4: Aluno
        Configurar SLI/SLO monitoring: 4: Aluno
        Apresentar projeto final: 5: Aluno
```

## Fluxo Detalhado de Uso do Repositorio

```mermaid
flowchart TD
    START([Aluno inicia<br/>disciplina]) --> README[Ler README.md<br/>Visao geral e pre-requisitos]
    README --> SETUP[Setup do Ambiente<br/>Python 3.10 + venv<br/>pip install -r requirements.txt]
    SETUP --> DOCS[Explorar Documentacao]

    DOCS --> ARCH[Ler docs/architecture/<br/>Entender arquitetura]
    DOCS --> BIZ[Ler docs/business/<br/>Entender use cases]
    DOCS --> ADR[Ler ADRs<br/>Entender decisoes tecnicas]

    ARCH --> AULA{Escolher<br/>Aula}

    AULA -->|Teoria| AULA_README[Ler README.md<br/>da Aula]
    AULA_README --> NOTEBOOK[Executar Notebooks<br/>Jupyter/Colab]
    NOTEBOOK --> CODE[Explorar Codigo<br/>src/]
    CODE --> EXERCISE[Resolver<br/>Exercicios]

    EXERCISE --> EXPERIMENT[Experimentar<br/>Variacoes]
    EXPERIMENT --> LOG[Registrar Experimentos<br/>MLflow Tracking]
    LOG --> COMPARE[Comparar Metricas<br/>Acuracia vs Latencia]

    COMPARE --> NEXT{Proxima<br/>Aula?}
    NEXT -->|Sim| AULA
    NEXT -->|Nao - Projeto| PROJECT[Projeto Final]

    PROJECT --> DEFINE[Definir Problema<br/>e SLOs de Latencia]
    DEFINE --> IMPLEMENT[Implementar Pipeline<br/>End-to-End]
    IMPLEMENT --> OPTIMIZE_P[Otimizar para<br/>Requisitos de Latencia]
    OPTIMIZE_P --> DEPLOY_P[Deploy em<br/>Producao - Azure AKS]
    DEPLOY_P --> MONITOR_P[Configurar<br/>Monitoramento SLI/SLO]
    MONITOR_P --> PRESENT[Apresentar<br/>Resultados]
    PRESENT --> CONTRIBUTE[Contribuir<br/>de volta ao repo]
    CONTRIBUTE --> END([Disciplina<br/>concluida])
```

## Checkpoints de Aprendizado

| Semana | Checkpoint | Evidencia |
|--------|-----------|-----------|
| 1 | Entende metricas de latencia P50/P95/P99 | Profiling executado e interpretado |
| 2 | Implementou pipeline NLP ou Audio | Notebook funcional com benchmark |
| 3 | Treinou modelo de visao computacional | Metricas de acuracia e latencia registradas |
| 4 | Aplicou pruning + quantizacao | Comparacao antes/depois com metricas |
| 5 | Fine-tuned modelo com PEFT | LoRA adapter treinado com metricas |
| 6 | Profiling em GPU com mixed precision | Nsight report ou PyTorch Profiler trace |
| 7 | Deploy distribuido funcional | Triton ou vLLM servindo inferencia |
| 8 | Pipeline multimodal em producao | AKS deployment com SLI/SLO dashboard |
