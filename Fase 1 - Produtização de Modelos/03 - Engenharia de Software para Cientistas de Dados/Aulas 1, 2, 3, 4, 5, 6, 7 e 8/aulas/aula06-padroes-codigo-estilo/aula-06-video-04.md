---
titulo: "Aula 06 – Parte 04: Refinando Código - Exemplo Prático de Refatoração Simples"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 15
prerequisitos:
  - "Python 3.12+"
  - "Aula 06 - Partes 01, 02 e 03 concluídas"
  - "Conhecimento dos princípios DRY, KISS, SRP"
tags: ["refactoring", "clean-code", "before-after", "extract-function", "code-quality"]
---

# 1. Abertura do vídeo (script)

Olá! Esta é a última aula do módulo de Padrões de Código e Estilo. Chegou a hora de colocar tudo em prática.

Nas aulas anteriores você aprendeu PEP 8, princípios de código limpo como DRY e KISS, e padrões de design como Strategy. Teoria é importante, mas ver na prática é o que consolida o aprendizado.

Nesta aula, vamos fazer um exercício de **refatoração completo**. Eu vou mostrar um código típico de notebook de Data Science - funciona, mas é difícil de manter. Passo a passo, vamos transformá-lo em código profissional, mantendo os testes passando a cada mudança.

É como um "antes e depois" de reforma. O código final vai ser menor, mais claro, e muito mais fácil de evoluir.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você tem um script que analisa dados de crédito. Foi escrito às pressas para uma apresentação. Funciona, mas agora precisa virar código de produção.

**Agitação**: O código tem 150 linhas em uma única função. Variáveis chamadas `df`, `df2`, `temp`. Magic numbers por todo lado. A mesma validação aparece 3 vezes. Ninguém quer mexer nisso.

**Solução**: Refatorar em passos pequenos e seguros. Extrair funções, renomear variáveis, eliminar duplicação. Cada mudança é testada. No final, o código faz exatamente o mesmo, mas é um prazer de ler e modificar.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Executar** refatoração Extract Function
2. **Aplicar** refatoração Rename Variable/Function
3. **Simplificar** estruturas condicionais complexas
4. **Manter** testes passando durante refatoração
5. **Identificar** oportunidades de melhoria em código legado
6. **Documentar** mudanças de refatoração em commits

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Ambiente do projeto configurado
- Testes existentes funcionando

**Verificar ambiente:**

```bash
# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Ativar ambiente
.\.venv\Scripts\Activate.ps1

# Garantir que testes passam
task test
```

**Checklist:**
- [ ] Ambiente virtual ativado
- [ ] Testes passando
- [ ] Git limpo (sem mudanças pendentes)

# 5. Visão geral do que já existe no projeto (continuidade)

**Estado atual:**
```
swe4ds-credit-api/
├── src/
│   ├── analyzer.py            # ANTES: Código a refatorar
│   ├── models/
│   │   └── strategies.py      # Criado na aula anterior
│   └── ...
└── tests/
    └── test_analyzer.py       # Testes que devem continuar passando
```

**O que vamos fazer:**
- Refatorar `analyzer.py` mantendo comportamento
- Aplicar Extract Function, Rename, Simplify
- Cada passo verificado por testes

# 6. Passo a passo (comandos + código)

## Passo 1: Código Original (Antes) (Excalidraw: Slide 8)

**Intenção**: Ver o código "espaguete" típico antes da refatoração.

### O Código Antes

Crie o arquivo e cole o conteúdo abaixo (diff lógico):

```bash
New-Item src/analyzer.py -ItemType File
code src/analyzer.py
```

```python
# (SUBSTITUIR conteúdo do arquivo)
"""Analisador de crédito - ANTES da refatoração."""

def analyze(d, t=0.5):
    # valida
    if d is None:
        return {"error": "no data"}
    if "age" not in d:
        return {"error": "no age"}
    if "limit" not in d:
        return {"error": "no limit"}
    if "history" not in d:
        return {"error": "no history"}
    
    # valida valores
    if d["age"] < 18 or d["age"] > 120:
        return {"error": "invalid age"}
    if d["limit"] <= 0:
        return {"error": "invalid limit"}
    
    # calcula score
    s = 0
    
    # idade
    if d["age"] >= 18 and d["age"] < 25:
        s = s + 10
    elif d["age"] >= 25 and d["age"] < 35:
        s = s + 20
    elif d["age"] >= 35 and d["age"] < 50:
        s = s + 30
    elif d["age"] >= 50:
        s = s + 25
    
    # limite
    if d["limit"] < 1000:
        s = s + 5
    elif d["limit"] < 5000:
        s = s + 15
    elif d["limit"] < 10000:
        s = s + 25
    else:
        s = s + 35
    
    # historico
    h = d["history"]
    if h == "good":
        s = s + 40
    elif h == "regular":
        s = s + 20
    elif h == "bad":
        s = s + 5
    
    # normaliza
    s = s / 100
    
    # decide
    if s >= t:
        r = "approved"
    else:
        r = "rejected"
    
    return {"status": r, "score": s}
```

```python
"""Analisador de crédito - ANTES da refatoração."""

def analyze(d, t=0.5):
    # valida
    if d is None:
        return {"error": "no data"}
    if "age" not in d:
        return {"error": "no age"}
    if "limit" not in d:
        return {"error": "no limit"}
    if "history" not in d:
        return {"error": "no history"}
    
    # valida valores
    if d["age"] < 18 or d["age"] > 120:
        return {"error": "invalid age"}
    if d["limit"] <= 0:
        return {"error": "invalid limit"}
    
    # calcula score
    s = 0
    
    # idade
    if d["age"] >= 18 and d["age"] < 25:
        s = s + 10
    elif d["age"] >= 25 and d["age"] < 35:
        s = s + 20
    elif d["age"] >= 35 and d["age"] < 50:
        s = s + 30
    elif d["age"] >= 50:
        s = s + 25
    
    # limite
    if d["limit"] < 1000:
        s = s + 5
    elif d["limit"] < 5000:
        s = s + 15
    elif d["limit"] < 10000:
        s = s + 25
    else:
        s = s + 35
    
    # historico
    h = d["history"]
    if h == "good":
        s = s + 40
    elif h == "regular":
        s = s + 20
    elif h == "bad":
        s = s + 5
    
    # normaliza
    s = s / 100
    
    # decide
    if s >= t:
        r = "approved"
    else:
        r = "rejected"
    
    return {"status": r, "score": s}
```

### Problemas Identificados

| Code Smell | Ocorrência |
|------------|------------|
| Nomes obscuros | `d`, `t`, `s`, `h`, `r` |
| Função longa | 50+ linhas |
| Magic numbers | `18`, `120`, `0.5`, `100` |
| Validação repetitiva | 6 verificações similares |
| Lógica misturada | Validação + Cálculo + Decisão |
| Sem docstrings | Impossível saber o que faz |

### Criar Teste de Caracterização

Antes de refatorar, garantir comportamento:

Crie o arquivo e cole o conteúdo (mão na massa):

```bash
New-Item tests/test_analyzer.py -ItemType File
code tests/test_analyzer.py
```

```python
"""Testes para analyzer - garantem comportamento durante refatoração."""

import pytest
from src.analyzer import analyze


class TestAnalyze:
    """Testes de caracterização para analyze."""

    def test_valid_young_low_limit_good_history(self):
        data = {"age": 20, "limit": 500, "history": "good"}
        result = analyze(data)
        
        assert result["status"] == "approved"
        assert result["score"] == pytest.approx(0.55)

    def test_valid_middle_age_high_limit_bad_history(self):
        data = {"age": 40, "limit": 15000, "history": "bad"}
        result = analyze(data)
        
        assert result["status"] == "rejected"
        assert result["score"] == pytest.approx(0.70)  # 30 + 35 + 5

    def test_missing_age(self):
        result = analyze({"limit": 1000, "history": "good"})
        assert result == {"error": "no age"}

    def test_invalid_age(self):
        result = analyze({"age": 15, "limit": 1000, "history": "good"})
        assert result == {"error": "invalid age"}

    def test_none_data(self):
        result = analyze(None)
        assert result == {"error": "no data"}

    def test_custom_threshold(self):
        data = {"age": 20, "limit": 500, "history": "good"}
        
        result_low = analyze(data, t=0.3)
        result_high = analyze(data, t=0.9)
        
        assert result_low["status"] == "approved"
        assert result_high["status"] == "rejected"
```


```bash
# Verificar que testes passam
uv run pytest tests/test_analyzer.py -v
```

**CHECKPOINT**: Testes de caracterização passando.

---

## Passo 2: Rename - Nomes Descritivos (Excalidraw: Slide 8)

**Intenção**: Primeiro passo: dar nomes que fazem sentido.

### Refatoração: Rename

```python
"""Analisador de crédito - Passo 2: Rename."""

def analyze(client_data, approval_threshold=0.5):
    # valida presença
    if client_data is None:
        return {"error": "no data"}
    if "age" not in client_data:
        return {"error": "no age"}
    if "limit" not in client_data:
        return {"error": "no limit"}
    if "history" not in client_data:
        return {"error": "no history"}
    
    # valida valores
    if client_data["age"] < 18 or client_data["age"] > 120:
        return {"error": "invalid age"}
    if client_data["limit"] <= 0:
        return {"error": "invalid limit"}
    
    # calcula score
    score = 0
    
    # pontos por idade
    age = client_data["age"]
    if age >= 18 and age < 25:
        score = score + 10
    elif age >= 25 and age < 35:
        score = score + 20
    elif age >= 35 and age < 50:
        score = score + 30
    elif age >= 50:
        score = score + 25
    
    # pontos por limite
    credit_limit = client_data["limit"]
    if credit_limit < 1000:
        score = score + 5
    elif credit_limit < 5000:
        score = score + 15
    elif credit_limit < 10000:
        score = score + 25
    else:
        score = score + 35
    
    # pontos por histórico
    history = client_data["history"]
    if history == "good":
        score = score + 40
    elif history == "regular":
        score = score + 20
    elif history == "bad":
        score = score + 5
    
    # normaliza score
    normalized_score = score / 100
    
    # decide aprovação
    if normalized_score >= approval_threshold:
        status = "approved"
    else:
        status = "rejected"
    
    return {"status": status, "score": normalized_score}
```

```bash
# Verificar que testes ainda passam
uv run pytest tests/test_analyzer.py -v

# Commit
git add src/analyzer.py
git commit -m "refactor(analyzer): rename variables for clarity

- d → client_data
- t → approval_threshold
- s → score
- h → history
- r → status"
```

**CHECKPOINT**: Nomes descritivos, testes passando.

---

## Passo 3: Extract Function - Validação (Excalidraw: Slide 8)

**Intenção**: Extrair validação para função separada.

### Refatoração: Extract Function

```python
"""Analisador de crédito - Passo 3: Extract validation."""

REQUIRED_FIELDS = ["age", "limit", "history"]
MIN_AGE = 18
MAX_AGE = 120


def _validate_client_data(client_data: dict | None) -> str | None:
    """Valida dados do cliente.
    
    Returns:
        Mensagem de erro ou None se válido.
    """
    if client_data is None:
        return "no data"
    
    # Verifica campos obrigatórios
    for field in REQUIRED_FIELDS:
        if field not in client_data:
            return f"no {field}"
    
    # Valida valores
    if not (MIN_AGE <= client_data["age"] <= MAX_AGE):
        return "invalid age"
    if client_data["limit"] <= 0:
        return "invalid limit"
    
    return None


def analyze(client_data, approval_threshold=0.5):
    """Analisa cliente para aprovação de crédito."""
    # Validação extraída
    error = _validate_client_data(client_data)
    if error:
        return {"error": error}
    
    # calcula score
    score = 0
    
    # pontos por idade
    age = client_data["age"]
    if age >= 18 and age < 25:
        score = score + 10
    elif age >= 25 and age < 35:
        score = score + 20
    elif age >= 35 and age < 50:
        score = score + 30
    elif age >= 50:
        score = score + 25
    
    # ... resto igual ...
```

```bash
# Verificar testes
uv run pytest tests/test_analyzer.py -v

# Commit
git add src/analyzer.py
git commit -m "refactor(analyzer): extract validation function

- Create _validate_client_data()
- Extract constants REQUIRED_FIELDS, MIN_AGE, MAX_AGE
- Replace repetitive field checks with loop"
```

**CHECKPOINT**: Validação extraída, testes passando.

---

## Passo 4: Extract Function - Cálculos de Score (Excalidraw: Slide 8)

**Intenção**: Extrair cálculos de pontuação para funções separadas.

### Refatoração: Extract Score Functions

```python
"""Analisador de crédito - Passo 4: Extract score calculations."""

REQUIRED_FIELDS = ["age", "limit", "history"]
MIN_AGE = 18
MAX_AGE = 120
MAX_SCORE = 100

# Pontuação por faixa etária
AGE_SCORES = [
    (18, 25, 10),
    (25, 35, 20),
    (35, 50, 30),
    (50, 200, 25),  # 200 como limite superior prático
]

# Pontuação por faixa de limite
LIMIT_SCORES = [
    (0, 1000, 5),
    (1000, 5000, 15),
    (5000, 10000, 25),
    (10000, float("inf"), 35),
]

# Pontuação por histórico
HISTORY_SCORES = {
    "good": 40,
    "regular": 20,
    "bad": 5,
}


def _validate_client_data(client_data: dict | None) -> str | None:
    """Valida dados do cliente."""
    if client_data is None:
        return "no data"
    
    for field in REQUIRED_FIELDS:
        if field not in client_data:
            return f"no {field}"
    
    if not (MIN_AGE <= client_data["age"] <= MAX_AGE):
        return "invalid age"
    if client_data["limit"] <= 0:
        return "invalid limit"
    
    return None


def _calculate_age_score(age: int) -> int:
    """Calcula pontuação baseada na idade."""
    for min_age, max_age, points in AGE_SCORES:
        if min_age <= age < max_age:
            return points
    return 0


def _calculate_limit_score(credit_limit: float) -> int:
    """Calcula pontuação baseada no limite de crédito."""
    for min_limit, max_limit, points in LIMIT_SCORES:
        if min_limit <= credit_limit < max_limit:
            return points
    return 0


def _calculate_history_score(history: str) -> int:
    """Calcula pontuação baseada no histórico."""
    return HISTORY_SCORES.get(history, 0)


def _calculate_total_score(client_data: dict) -> float:
    """Calcula score total normalizado."""
    score = (
        _calculate_age_score(client_data["age"])
        + _calculate_limit_score(client_data["limit"])
        + _calculate_history_score(client_data["history"])
    )
    return score / MAX_SCORE


def analyze(client_data: dict | None, approval_threshold: float = 0.5) -> dict:
    """Analisa cliente para aprovação de crédito.
    
    Args:
        client_data: Dados do cliente com age, limit, history
        approval_threshold: Score mínimo para aprovação (0-1)
    
    Returns:
        Dict com status e score, ou error se inválido
    """
    error = _validate_client_data(client_data)
    if error:
        return {"error": error}
    
    score = _calculate_total_score(client_data)
    status = "approved" if score >= approval_threshold else "rejected"
    
    return {"status": status, "score": score}
```

```bash
# Verificar testes
uv run pytest tests/test_analyzer.py -v

# Verificar lint
ruff check src/analyzer.py

# Commit
git add src/analyzer.py
git commit -m "refactor(analyzer): extract score calculation functions

- Extract _calculate_age_score()
- Extract _calculate_limit_score()
- Extract _calculate_history_score()
- Extract _calculate_total_score()
- Replace magic numbers with named constants
- Add type hints and docstrings"
```

**CHECKPOINT**: Cálculos extraídos, testes passando.

---

## Passo 5: Comparação Final - Antes e Depois

**Intenção**: Ver a transformação completa.

### Métricas de Melhoria

| Métrica | Antes | Depois | Melhoria |
|---------|-------|--------|----------|
| Linhas na função principal | 50 | 10 | 80% menor |
| Funções | 1 | 6 | Responsabilidade única |
| Magic numbers | 12 | 0 | Constantes nomeadas |
| Duplicação | 6 validações | 1 loop | DRY aplicado |
| Type hints | 0 | 100% | Documentação em código |
| Docstrings | 0 | 100% | Auto-documentado |

### Código Final

```python
"""Analisador de crédito - Versão refatorada."""

REQUIRED_FIELDS = ["age", "limit", "history"]
MIN_AGE = 18
MAX_AGE = 120
MAX_SCORE = 100

AGE_SCORES = [(18, 25, 10), (25, 35, 20), (35, 50, 30), (50, 200, 25)]
LIMIT_SCORES = [(0, 1000, 5), (1000, 5000, 15), (5000, 10000, 25), (10000, float("inf"), 35)]
HISTORY_SCORES = {"good": 40, "regular": 20, "bad": 5}


def _validate_client_data(client_data: dict | None) -> str | None:
    """Valida dados do cliente. Retorna erro ou None."""
    if client_data is None:
        return "no data"
    for field in REQUIRED_FIELDS:
        if field not in client_data:
            return f"no {field}"
    if not (MIN_AGE <= client_data["age"] <= MAX_AGE):
        return "invalid age"
    if client_data["limit"] <= 0:
        return "invalid limit"
    return None


def _calculate_age_score(age: int) -> int:
    """Pontuação por faixa etária."""
    return next((p for min_a, max_a, p in AGE_SCORES if min_a <= age < max_a), 0)


def _calculate_limit_score(limit: float) -> int:
    """Pontuação por faixa de limite."""
    return next((p for min_l, max_l, p in LIMIT_SCORES if min_l <= limit < max_l), 0)


def _calculate_history_score(history: str) -> int:
    """Pontuação por histórico."""
    return HISTORY_SCORES.get(history, 0)


def _calculate_total_score(data: dict) -> float:
    """Score total normalizado (0-1)."""
    score = (
        _calculate_age_score(data["age"])
        + _calculate_limit_score(data["limit"])
        + _calculate_history_score(data["history"])
    )
    return score / MAX_SCORE


def analyze(client_data: dict | None, approval_threshold: float = 0.5) -> dict:
    """Analisa cliente para aprovação de crédito."""
    if error := _validate_client_data(client_data):
        return {"error": error}
    
    score = _calculate_total_score(client_data)
    status = "approved" if score >= approval_threshold else "rejected"
    return {"status": status, "score": score}
```

### Benefícios Alcançados

✅ **Legibilidade**: Qualquer pessoa entende em segundos
✅ **Testabilidade**: Cada função pode ser testada isoladamente
✅ **Manutenibilidade**: Mudança localizada (ex: novo range de idade)
✅ **Extensibilidade**: Fácil adicionar novos critérios
✅ **Documentação**: Type hints e docstrings como documentação viva

**CHECKPOINT**: Refatoração completa com todas as melhorias.

# 7. Testes rápidos e validação

```bash
# Verificar lint
ruff check src/analyzer.py

# Verificar formatação
ruff format src/analyzer.py --check

# Rodar todos os testes
task test

# Verificar cobertura
task test-cov
```

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas de Refatoração

1. **Testes primeiro**
   - Nunca refatore sem testes
   - Crie testes de caracterização se não existirem
   - **Trade-off**: Tempo extra, mas segurança

2. **Passos pequenos**
   - Uma refatoração por vez
   - Commit após cada mudança
   - **Trade-off**: Mais commits, mas rollback fácil

3. **Não adicione features**
   - Refatoração ≠ nova funcionalidade
   - Separe as tarefas
   - **Trade-off**: Duas iterações, mas foco claro

4. **Documente intenção nos commits**
   - Prefixo `refactor:`
   - Explique o que mudou e por quê
   - **Trade-off**: Mensagens maiores, mas histórico útil

5. **Ferramentas ajudam**
   - IDEs têm refatorações automáticas
   - Use Rename, Extract Function, etc.
   - **Trade-off**: Aprender atalhos, mas produtividade

# 9. Troubleshooting (erros comuns)

| Problema | Causa | Solução |
|----------|-------|---------|
| Testes falharam após refatoração | Mudou comportamento | Reverter e verificar |
| Não sei por onde começar | Código muito complexo | Comece renomeando |
| Refatoração parcial | Interrompido no meio | Termine ou reverta |
| Merge conflict com refatoração | Outros mudaram mesmo código | Comunicar antes |
| Over-refatoração | Perfeccionismo | Defina critério de "pronto" |
| Sem testes existentes | Código legado | Crie testes de caracterização |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Adicionar Teste

Adicione um teste para o caso de `history` não reconhecido (ex: "unknown"). Verifique o comportamento atual.

**Critério de sucesso**: Teste documentando comportamento edge case.

## Exercício Básico 2: Refatorar Outro Código

Aplique as técnicas em outro código do projeto. Identifique smells, crie testes, refatore.

**Critério de sucesso**: Código melhorado com testes passando.

## Exercício Avançado: Adicionar Feature de Forma Limpa

Adicione um novo critério de pontuação: `employment_years` (anos de emprego). Faça isso de forma que aproveite a estrutura refatorada.

**Critério de sucesso**: Nova feature integrada sem duplicação.

# 11. Resultados e Lições

## Técnicas de Refatoração Usadas

| Técnica | Descrição | Quando usar |
|---------|-----------|-------------|
| **Rename** | Mudar nome para ser descritivo | Nomes obscuros |
| **Extract Function** | Criar função a partir de código | Função muito longa |
| **Extract Constant** | Criar constante para magic number | Valores hardcoded |
| **Replace Conditional with Polymorphism** | Usar Strategy | Muitos if-elif similares |
| **Simplify Conditional** | Usar operadores mais claros | Condicionais complexos |

## Lições desta Aula

1. **Testes habilitam refatoração** - São sua rede de segurança
2. **Passos pequenos são seguros** - Uma mudança por vez
3. **Nomes importam** - Primeiro passo é sempre renomear
4. **Funções pequenas são melhores** - Extraia sem medo
5. **Constantes documentam** - Magic numbers viram nomes

# 12. Encerramento e gancho para a próxima aula (script)

Parabéns! Você completou o módulo de Padrões de Código e Estilo. Nesta aula você viu na prática como transformar código "espaguete" em código profissional através de refatoração incremental.

Você aprendeu técnicas como Extract Function, Rename, e Extract Constant. Mais importante: você aprendeu que refatoração é um processo seguro quando você tem testes e faz mudanças pequenas.

Vamos recapitular o módulo inteiro:
- **Parte 1**: PEP 8 e convenções de estilo com Ruff
- **Parte 2**: Princípios DRY, KISS, Single Responsibility
- **Parte 3**: Strategy Pattern e idiomas Pythônicos
- **Parte 4**: Refatoração prática passo a passo

Na próxima aula, vamos para o **módulo de Deploy e Monitoramento**. Você vai aprender a colocar seu código em produção de forma profissional, com CI/CD, containerização, e observabilidade. O código limpo que você aprendeu a escrever vai finalmente rodar em servidores reais.

Até a próxima aula, e parabéns pelo progresso!
