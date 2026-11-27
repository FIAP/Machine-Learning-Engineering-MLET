---
titulo: "Aula 07 – Parte 02: Estratégias de Deploy - Batch vs. Tempo Real, Blue-Green e Canary"
modulo: "Engenharia de software para cientista de dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 25
prerequisitos:
  - "Python 3.12+"
  - "FastAPI configurado"
  - "CI básico configurado"
tags: ["deploy", "batch", "real-time", "blue-green", "canary"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos falar sobre **estratégias de deploy** para projetos de Data Science.

Você já tem uma API FastAPI funcionando. Agora precisamos decidir **como** colocar esse modelo em produção. É um job agendado em batch? É uma API de inferência em tempo real? E como atualizar versões sem derrubar o serviço?

Vamos explorar estratégias clássicas como **Blue-Green** e **Canary Release**, além de comparar deploy batch vs. tempo real. Tudo conectado com a nossa API que consome o modelo da pasta Consumer_API.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você treina um novo modelo e sobe direto para produção. Alguns usuários começam a ter respostas inconsistentes.

**Agitação**: Não dá para saber se o problema é o modelo novo ou o tráfego. Você precisa fazer rollback rápido, mas não há estratégia definida.

**Solução**: Planejar o deploy. Usar batch quando o problema permite processamento em lotes, tempo real quando latência é crítica, e estratégias como Blue-Green e Canary para atualizar versões com segurança. Tudo isso integrado à evolução incremental da API.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Distinguir** deploy batch e tempo real
2. **Explicar** Blue-Green e Canary Release
3. **Simular** duas versões da API em paralelo
4. **Planejar** deploy seguro para a API de ML

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+
- FastAPI em execução
- Docker opcional (para simular múltiplas versões)

**Setup:**

```bash
# Ativar ambiente
.\.venv\Scripts\Activate.ps1

# Rodar API local
uv run uvicorn src.main:app --reload
```

**Checklist de setup:**
- [ ] API rodando localmente
- [ ] Endpoint /health funcionando
- [ ] Acesso ao modelo em Consumer_API

# 5. Visão geral do que já existe no projeto (continuidade)

Estado atual esperado:
```
swe4ds-credit-api/
├── src/
│   ├── main.py
│   ├── routes/
│   │   └── predict.py
│   └── services/
├── Consumer_API/        # Modelo e artefatos
└── tests/
```

**O que será alterado nesta parte:**
- Adição de um script batch
- Simulação de duas versões da API

# 6. Passo a passo (comandos + código)

## Passo 1: Batch vs. Tempo Real (Excalidraw: Slide 2)

**Intenção:** Fixar os critérios de decisão.

### Matriz de decisão

| Critério | Batch | Tempo real |
|---|---|---|
| Latência | Alta tolerável | Baixa exigida |
| Custo por request | Baixo | Mais alto |
| Volume | Muito alto | Moderado |
| Operação | Simples | Mais complexa |

**CHECKPOINT:** Você consegue justificar a escolha com base em latência e custo.

---

## Passo 2: Estratégias de rollout (Blue-Green e Canary)

**Intenção:** Entender o objetivo de cada estratégia.

### Blue-Green
- Duas versões completas em paralelo
- Troca de tráfego instantânea
- Rollback rápido

### Canary
- Exposição gradual do tráfego
- Detecta problemas cedo
- Requer métricas/monitoramento

**CHECKPOINT:** Você consegue explicar a diferença entre “troca total” e “troca gradual”.

---

## Passo 3: Riscos e trade-offs

**Intenção:** Mapear impactos antes de decidir.

| Estratégia | Vantagem | Risco/Trade-off |
|---|---|---|
| Blue-Green | Rollback simples | Custo duplicado temporário |
| Canary | Menor risco | Observabilidade obrigatória |

**CHECKPOINT:** Você consegue apontar quando Canary é inviável.

---

## Passo 4: Onde isso entra na nossa API

**Intenção:** Conectar a teoria ao projeto.

Na prática, vamos simular versões da API e rotas de tráfego na Parte 04, junto com o pipeline. Aqui, o foco é a **decisão de estratégia**.

**CHECKPOINT:** Você entende o “porquê” antes do “como”.

# 7. Testes rápidos e validação

Nesta parte, a validação é **conceitual**: você deve saber que batch e real-time precisam de testes diferentes (processamento em lote vs. contract test de endpoint).

**CHECKPOINT:** Você sabe qual tipo de teste valida cada estratégia.

# 8. Observabilidade e boas práticas (mini-bloco)

1. **Planejamento de deploy**: evita downtime. Trade-off: mais etapas no release.
2. **Separar batch e real-time**: performance e custo equilibrados. Trade-off: dois fluxos de execução.
3. **Estratégias de rollout**: Blue-Green e Canary reduzem risco. Trade-off: duplicar infraestrutura temporariamente.

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| Porta já em uso | Outra instância rodando | Trocar `--port` |
| Batch lento | CSV muito grande | Processar em chunks |
| Canary inconsistente | Modelos diferentes demais | Ajustar testes A/B |
| API responde 500 | Modelo não carregou | Validar caminho do modelo |

# 10. Exercícios (básico e avançado)

**Básico 1:** Criar um script que roteia 20% do tráfego para a versão green.
- Concluído com sucesso: script envia requisições com distribuição aproximada.

**Básico 2:** Comparar outputs do batch e da API para o mesmo input.
- Concluído com sucesso: outputs equivalentes.

**Avançado:** Escrever um mini relatório com critérios para escolher batch ou real-time no seu projeto.
- Concluído com sucesso: relatório com critérios claros (latência, custo, volume).

# 11. Resultados e Lições

**Resultados (como medir):**
- Latência média (medir com `time` ou logs)
- Taxa de erro (contar respostas não-2xx)
- Diferença entre versões (comparar outputs)

**Lições:**
- Batch é ótimo para volume, real-time para latência
- Blue-Green reduz risco de downtime
- Canary permite detectar problemas cedo

# 12. Encerramento e gancho para a próxima aula (script)

Nesta aula você aprendeu a escolher entre deploy batch e tempo real e a aplicar estratégias Blue-Green e Canary para atualizar sua API de ML com segurança.

Na próxima parte, vamos mergulhar em **observabilidade e monitoramento**: métricas de sistema, métricas de aplicação e métricas específicas de modelos como drift e acurácia. Você vai entender como manter a qualidade do modelo em produção.
