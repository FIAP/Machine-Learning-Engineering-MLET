---
titulo: "Aula 07 – Parte 04: Pipeline Automatizado - Exemplo de CI/CD com Deploy e Monitoramento"
modulo: "Engenharia de software para cientista de dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 20
prerequisitos:
  - "Python 3.12+"
  - "GitHub Actions configurado"
  - "Docker instalado (opcional para build local)"
tags: ["ci-cd", "docker", "github-actions", "deploy", "monitoring"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos fechar o ciclo completo: do commit ao deploy com monitoramento.

Você já configurou CI, já conhece estratégias de deploy e já instrumentou a API com logs e métricas básicas. Agora vamos integrar tudo em um pipeline CI/CD simples no GitHub Actions: testes, build do contêiner, publicação em registry simulado e execução em ambiente de staging.

Esse pipeline representa a forma como equipes profissionais colocam modelos em produção com segurança. E tudo conectado à API que consome o modelo da pasta Consumer_API.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Cada deploy é feito manualmente. Às vezes você esquece um passo, às vezes faz build com a versão errada.

**Agitação**: Erros humanos causam instabilidade. O modelo pode ficar indisponível e o time perde confiança na entrega.

**Solução**: CI/CD. O pipeline automatiza testes, build e deploy. Você faz o commit e o sistema faz o resto, com logs e métricas para acompanhar. Assim, a API evolui de forma incremental e confiável.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Configurar** um pipeline CI/CD completo
2. **Automatizar** build e push de container
3. **Implantar** em ambiente de staging (simulado)
4. **Coletar** logs e métricas pós-deploy

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+
- GitHub Actions habilitado
- Docker (opcional local)

**Setup local:**

```bash
# Ativar ambiente
.\.venv\Scripts\Activate.ps1

# Rodar testes
uv run pytest -q

# Build local do container (opcional)
docker build -t credit-api:local .
```

**Checklist de setup:**
- [ ] Repositório com CI funcionando
- [ ] Docker instalado (se for build local)
- [ ] Secrets configurados no GitHub (se usar registry)

# 5. Visão geral do que já existe no projeto (continuidade)

Estado atual esperado:
```
swe4ds-credit-api/
├── src/
├── tests/
├── Dockerfile
├── .github/workflows/ci.yml
└── ...
```

**O que será alterado nesta parte:**
- Adicionar workflow de CI/CD
- Script de deploy em staging (simulado)
- Verificação de logs e métricas

# 6. Passo a passo (comandos + código)

## Passo 1: Workflow de CI/CD (Excalidraw: Slide 6)

**Intenção:** Executar testes, build e push da imagem.

Arquivo: `.github/workflows/cicd.yml` (novo — criar arquivo)

```bash
mkdir .github
mkdir .github\workflows
New-Item .github/workflows/cicd.yml -ItemType File
code .github/workflows/cicd.yml
```

```yaml
name: cicd

on:
  push:
    branches: ["main"]

jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: uv sync

      - name: Lint
        run: uv run ruff check src/ tests/

      - name: Tests
        run: uv run pytest -q

      - name: Build Docker image
        run: docker build -t credit-api:${{ github.sha }} .

      - name: Tag for registry
        run: docker tag credit-api:${{ github.sha }} ${{ secrets.REGISTRY_URL }}/credit-api:${{ github.sha }}

      - name: Push to registry (simulado)
        run: |
          echo "docker push ${{ secrets.REGISTRY_URL }}/credit-api:${{ github.sha }}"
```

**CHECKPOINT:** No Actions, você verá os passos de build e tag executando.

---

## Passo 2: Deploy em staging (Excalidraw: Slide 7)

**Intenção:** Simular deploy da imagem para staging.

Arquivo: `scripts/deploy_staging.ps1` (novo — criar arquivo)

```bash
New-Item scripts/deploy_staging.ps1 -ItemType File
code scripts/deploy_staging.ps1
```

```powershell
param(
    [string]$ImageTag
)

Write-Host "Deploying image to staging: $ImageTag"
# Aqui você integraria com Kubernetes, Docker Compose ou VM
```

Adicionar passo no workflow:

```yaml
      - name: Deploy to staging (simulado)
        run: pwsh ./scripts/deploy_staging.ps1 -ImageTag ${{ github.sha }}
```

**CHECKPOINT:** Log do Actions mostra mensagem de deploy.

---

## Passo 3: Coletar logs e métricas pós-deploy (Excalidraw: Slide 8)

**Intenção:** Verificar que a aplicação está saudável após o deploy.

Exemplo de etapa no workflow:

```yaml
      - name: Check health (simulado)
        run: |
          echo "curl http://staging.example/health"
```

**CHECKPOINT:** Workflow registra a verificação de saúde.

---

## Passo 4: Simular Blue-Green local (opcional)

**Intenção:** Tornar visível a estratégia na prática.

```bash
# Versão blue
uv run uvicorn src.main:app --port 8000

# Versão green
uv run uvicorn src.main:app --port 8001
```

**CHECKPOINT:** As duas portas respondem a `/health`.

# 7. Testes rápidos e validação

```bash
# Local
uv run pytest -q
ruff check src/ tests/

# Validar container localmente
curl http://localhost:8000/health
```

Resposta esperada (exemplo):
```json
{"status": "ok"}
```

# 8. Observabilidade e boas práticas (mini-bloco)

1. **Builds reproduzíveis**: tags por commit reduzem inconsistência. Trade-off: mais imagens no registry.
2. **Deploy automatizado**: reduz erro humano. Trade-off: exige manutenção do pipeline.
3. **Health checks**: detectam falhas cedo. Trade-off: precisa de endpoints dedicados.

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| Docker build falha | Dockerfile inválido | Validar localmente |
| Push falha | Secrets não configurados | Ajustar `REGISTRY_URL` |
| Deploy script não roda | Permissão | Executar com `pwsh` |
| Health check falha | API não subiu | Revisar logs do container |

# 10. Exercícios (básico e avançado)

**Básico 1:** Adicionar job de `ruff format --check` no pipeline.
- Concluído com sucesso: pipeline valida formatação.

**Básico 2:** Adicionar step de `docker run` para smoke test.
- Concluído com sucesso: container sobe e responde `/health`.

**Avançado:** Criar pipeline com ambientes separados (staging e production).
- Concluído com sucesso: deploy em staging só promove para production após aprovação manual.

# 11. Resultados e Lições

**Resultados (como medir):**
- Tempo de execução do pipeline (ver logs do Actions)
- Taxa de falhas por deploy (contar execuções falhas)
- Latência da API após deploy (medir com logs)

**Lições:**
- CI/CD elimina passos manuais críticos
- Deploy automatizado precisa de validação pós-deploy
- Observabilidade fecha o ciclo da entrega

# 12. Encerramento e gancho para a próxima aula (script)

Nesta aula, você montou um pipeline completo de CI/CD com build de contêiner, deploy em staging e validações pós-deploy.

Com isso, fechamos o módulo de Deploy e Monitoramento. Na próxima aula, vamos avançar para refatoração de projetos de Data Science, identificando problemas de código e reestruturando o projeto de forma profissional.
