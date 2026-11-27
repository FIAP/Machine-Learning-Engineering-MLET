---
titulo: "Aula 08 – Parte 01: Detectando 'Bad Smells' - Diagnóstico de Código em Projetos DS"
modulo: "Engenharia de software para cientista de dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 20
prerequisitos:
  - "Python 3.12+"
  - "Projeto FastAPI em andamento"
  - "Conhecimento básico de testes"
tags: ["refatoracao", "code-smells", "qualidade", "fastapi", "ds"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos aprender a **diagnosticar problemas de qualidade** no código de projetos de Data Science.

Em DS é muito comum termos notebooks e scripts que funcionam, mas são difíceis de manter. O problema é que, quando o projeto cresce, esse “funciona” vira um risco: bugs escondidos, dependências implícitas e código impossível de reutilizar.

Hoje vamos identificar **bad smells** — sinais de alerta no código — e entender por que a refatoração contínua é essencial para manter nossa API FastAPI saudável enquanto ela evolui.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: O time tem vários notebooks duplicados, cada um com pequenas variações do mesmo pipeline.

**Agitação**: Uma correção precisa ser aplicada em 5 lugares diferentes. Um notebook é atualizado, outro não. A API passa a usar dados inconsistentes.

**Solução**: Detectar bad smells cedo, padronizar o código e refatorar continuamente. Assim, seguimos com a construção incremental da API sem acumular dívidas técnicas.

# 3. Objetivos de aprendizagem

Ao final você será capaz de:

1. **Identificar** bad smells em notebooks e scripts de DS
2. **Explicar** impactos desses smells na manutenção e colaboração
3. **Priorizar** quais smells refatorar primeiro
4. **Relacionar** smells com riscos na API FastAPI

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+
- uv instalado
- Projeto FastAPI em execução

**Setup:**

```bash
# Ativar ambiente
.\.venv\Scripts\Activate.ps1

# Rodar testes para garantir baseline
uv run pytest -q
```

**Checklist de setup:**
- [ ] Ambiente virtual ativo
- [ ] Testes rodando
- [ ] Código atual versionado no Git

# 5. Visão geral do que já existe no projeto (continuidade)

Estado esperado do projeto:
```
swe4ds-credit-api/
├── src/
│   ├── main.py
│   ├── routes/
│   └── services/
├── tests/
└── Consumer_API/
```

**O que será alterado nesta parte:**
- Não vamos alterar arquivos ainda. Vamos **diagnosticar** o estado atual.

# 6. Passo a passo (comandos + código)

## Passo 1: Tipos de bad smells mais comuns (Excalidraw: Slide 1)

**Intenção:** Reconhecer padrões antes de mexer em código.

Categorias principais:
- **Duplicação** (mesma lógica em múltiplos pontos)
- **Funções monolíticas** (muitas responsabilidades)
- **Dependências implícitas** (estado global / ordem de execução)
- **Nomes obscuros** (`df2`, `temp`, `x`)

**CHECKPOINT:** Você consegue citar 3 smells sem abrir o projeto.

---

## Passo 2: Critérios objetivos para diagnóstico

**Intenção:** Ter regras simples para identificar smells.

Critérios práticos (teóricos):
- Função > 30–40 linhas
- Mesmo bloco repetido 2+ vezes
- Módulo mistura leitura, validação e predição
- Variáveis globais controlam fluxo

**CHECKPOINT:** Você consegue aplicar esses critérios mentalmente ao projeto.

---

## Passo 3: Impacto dos smells na API FastAPI

**Intenção:** Conectar sinais com riscos reais.

Impactos típicos:
- **Bugs difíceis de rastrear**
- **Evolução lenta** (cada mudança quebra outra)
- **Onboarding pesado**
- **Deploy arriscado**

**CHECKPOINT:** Você consegue explicar por que smells aumentam risco de deploy.

---

## Passo 4: Priorização de refatoração

**Intenção:** Saber por onde começar.

Ordem sugerida:
1. Duplicações críticas
2. Funções monolíticas em rotas
3. Dependências implícitas de modelo

**CHECKPOINT:** Você consegue listar 3 pontos de prioridade antes de refatorar.

# 7. Testes rápidos e validação

Nesta parte, a validação é **conceitual**: você precisa garantir que há uma linha de base de testes antes de refatorar, mas a execução prática acontece na Parte 03.

**CHECKPOINT:** Você entende que refatoração sem testes é risco alto.

# 8. Observabilidade e boas práticas (mini-bloco)

1. **Identificação contínua de smells**: reduz dívidas técnicas. Trade-off: demanda tempo de revisão.
2. **Testes como rede de segurança**: garante refatoração segura. Trade-off: esforço inicial.
3. **Modularização gradual**: facilita evolução. Trade-off: mais arquivos para organizar.

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| Código duplicado não aparece em busca simples | Variações pequenas | Use buscas por padrões ou diff manual |
| Função longa ignorada | Pressão por entrega | Defina limite de linhas no time |
| Variáveis globais escondidas | Notebook “funcionou” | Mova estado para funções/serviços |

# 10. Exercícios (básico e avançado)

**Básico 1:** Encontre 3 duplicações no projeto.
- Concluído com sucesso: lista com local e motivo da duplicação.

**Básico 2:** Liste 2 funções com mais de 30 linhas e descreva o que fazem.
- Concluído com sucesso: lista com arquivo e responsabilidade.

**Avançado:** Criar um relatório curto de smells do projeto e priorizar 3 para refatorar.
- Concluído com sucesso: relatório com prioridade justificada.

# 11. Resultados e Lições

**Resultados (como medir):**
- Número de funções longas (contagem manual)
- Quantidade de duplicações (inspeção ou ferramenta)
- Cobertura de testes antes de refatorar (pytest --cov)

**Lições:**
- Smells são sinais, não bugs
- Diagnóstico cedo evita dívidas grandes
- Refatorar é parte do ciclo de vida

# 12. Encerramento e gancho para a próxima aula (script)

Nesta aula você aprendeu a **diagnosticar bad smells** em projetos de Data Science e entendeu por que eles impactam diretamente a evolução da nossa API FastAPI.

Na próxima aula, vamos aprender **técnicas de refatoração graduais**: Extract Function, Rename e Move/Rearrange. Você verá como aplicar essas mudanças passo a passo, sempre com testes garantindo que a API continue correta.
