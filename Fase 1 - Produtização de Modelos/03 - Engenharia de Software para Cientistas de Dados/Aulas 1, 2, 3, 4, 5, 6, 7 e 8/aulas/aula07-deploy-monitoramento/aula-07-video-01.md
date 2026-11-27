---
titulo: "Aula 07 – Parte 01: Integração Contínua (CI) para Ciência de Dados"
modulo: "Engenharia de software para cientista de dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 15
prerequisitos:
  - "Python 3.12+"
  - "uv e ambiente virtual configurados"
  - "Projeto FastAPI iniciado nas aulas anteriores"
tags: ["ci", "github-actions", "devops", "fastapi", "qualidade"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos dar o primeiro passo no mundo de Deploy e Monitoramento: a Integração Contínua, ou CI.

Em projetos de Data Science, é comum o código funcionar no notebook e quebrar quando vai para o repositório. O CI resolve exatamente essa dor: toda mudança no código dispara testes e verificações automaticamente, evitando surpresas quando alguém faz um merge.

Aqui, nosso foco é garantir que a API FastAPI que estamos construindo com o modelo da pasta Consumer_API esteja sempre saudável. Vamos integrar testes, lint e checagens de estilo em um pipeline automatizado. Esse é o começo de uma cultura DevOps aplicada à ciência de dados.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você atualiza o endpoint de predição e faz push no repositório. O time de dados só percebe depois que a API quebrou.

**Agitação**: O deploy falha, o ambiente para, e o time perde tempo caçando o erro em algo simples: um import errado ou uma função que não passou nos testes.

**Solução**: CI. Cada push dispara automaticamente lint, testes e build. Assim, qualquer problema é detectado minutos depois do commit. E seguimos evoluindo a API incrementalmente, com segurança.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Explicar** o conceito de CI aplicado a projetos de DS
2. **Configurar** um pipeline simples no GitHub Actions
3. **Integrar** lint e testes no pipeline
4. **Validar** que a API FastAPI permanece estável a cada mudança

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+
- uv instalado
- Projeto FastAPI existente com testes básicos

**Setup:**

```bash
# Ativar o ambiente virtual
.\.venv\Scripts\Activate.ps1

# Verificar dependências
author=$(uv pip show fastapi | Select-String Name)

author

# Rodar testes localmente
uv run pytest -q
```

**Checklist de setup:**
- [ ] Ambiente virtual ativado
- [ ] Dependências instaladas via uv
- [ ] Testes locais passando
- [ ] Repositório com Git inicializado

# 5. Visão geral do que já existe no projeto (continuidade)

Estado atual esperado:
```
swe4ds-credit-api/
├── src/
│   ├── main.py
│   ├── routes/
│   └── services/
├── tests/
│   └── test_health.py
├── pyproject.toml
└── ...
```

**O que será alterado nesta parte:**
- Adição de um workflow de CI no GitHub Actions
- Inclusão de lint e testes no pipeline

# 6. Passo a passo (comandos + código)

## Passo 1: O que compõe um pipeline de CI (Excalidraw: Slide 1)

**Intenção:** Entender os blocos fundamentais do CI antes de escrever qualquer YAML.

### Componentes mínimos de um CI saudável

1. **Checkout do código**
2. **Setup do runtime** (Python 3.12)
3. **Instalação de dependências** (uv + `uv.lock`)
4. **Quality gates** (lint + testes)

```
Checkout → Setup → Install → Lint → Tests
```

**CHECKPOINT:** Você consegue explicar por que cada etapa existe.

---

## Passo 2: Estrutura mental do workflow

**Intenção:** Entender a anatomia de um workflow do GitHub Actions.

```yaml
name: ci
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - checkout
      - setup python
      - install deps
      - lint
      - tests
```

Esse YAML é um **mapa mental**. A implementação prática (arquivo real) será feita na Parte 04.

**CHECKPOINT:** Você sabe reconhecer as seções `on`, `jobs` e `steps`.

---

## Passo 3: Quality Gates (teoria aplicada)

**Intenção:** Definir o que bloqueia merges automaticamente.

Quality gates típicos:
- **Lint** (estilo e erros rápidos)
- **Testes** (contrato de comportamento)
- **Verificações mínimas de infra** (ex.: presença de Dockerfile)

**CHECKPOINT:** Você sabe quais gates são obrigatórios no nosso projeto.

---

## Passo 4: Documentação do CI

**Intenção:** Tornar o pipeline visível para o time.

Na prática, adicionamos um pequeno bloco no README para que novos membros saibam que CI existe e o que ele valida. A alteração real fica para a Parte 04.

**CHECKPOINT:** Você entende por que CI precisa estar documentado.

# 7. Testes rápidos e validação

Nesta parte, a validação é **conceitual**: você deve saber que lint e testes são o “contrato” que protege o merge. A execução prática completa será feita na Parte 04.

**CHECKPOINT:** Você consegue explicar por que rodar lint + testes antes do push evita regressões.

# 8. Observabilidade e boas práticas (mini-bloco)

1. **Automatize a qualidade**: CI reduz regressões e acelera revisões. Trade-off: pipelines podem levar minutos extras.
2. **Testes como contrato**: garante que a API não quebre com mudanças. Trade-off: exige esforço inicial para criar testes.
3. **Valide infra**: Dockerfile e configs não podem quebrar. Trade-off: mais passos no pipeline.

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| Pipeline falha ao instalar deps | `uv sync` sem lock | Gerar `uv.lock` localmente | 
| `ruff` não encontrado | Dependência ausente | Adicionar `ruff` em `pyproject.toml` |
| Tests falham no CI mas não local | Diferenças de ambiente | Fixar versões e usar `uv.lock` |
| Actions não roda | Branch não é `main` | Ajustar `branches` no YAML |

# 10. Exercícios (básico e avançado)

**Básico 1:** Adicionar um passo no CI para `ruff format --check`.
- Concluído com sucesso: pipeline executa format check sem falhar.

**Básico 2:** Criar um badge de status do GitHub Actions no README.
- Concluído com sucesso: badge aparece e atualiza o status.

**Avançado:** Adicionar job paralelo para rodar `pytest -q` e `pytest -m slow` em matriz.
- Concluído com sucesso: CI roda testes rápidos e lentos separadamente.

# 11. Resultados e Lições

**Resultados (como medir):**
- Tempo médio de execução do pipeline (medir nos logs do Actions)
- Número de falhas por commit (contar ocorrências)
- Cobertura de testes (usar `pytest --cov`)

**Lições:**
- CI reduz riscos e retrabalho
- Testes automatizados são base da evolução incremental
- Infra-as-Code também deve ser validada

# 12. Encerramento e gancho para a próxima aula (script)

Nesta aula, você configurou o primeiro pipeline de CI e garantiu que seu projeto FastAPI seja validado automaticamente a cada mudança.

Na próxima parte, vamos discutir **estratégias de deploy**: batch vs tempo real, Blue-Green e Canary. Vamos entender quando usar cada abordagem e como elas se encaixam na evolução da nossa API de ML.
