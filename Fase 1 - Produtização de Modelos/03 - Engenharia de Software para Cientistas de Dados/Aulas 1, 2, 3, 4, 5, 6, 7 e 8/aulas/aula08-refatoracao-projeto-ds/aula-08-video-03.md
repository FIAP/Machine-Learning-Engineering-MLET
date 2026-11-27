---
titulo: "Aula 08 – Parte 03: Hands-on - Refatorando um Código de Data Science (Antes e Depois)"
modulo: "Engenharia de software para cientista de dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 30
prerequisitos:
  - "Python 3.12+"
  - "Aula 08 - Parte 02 concluída"
  - "Testes automatizados básicos"
tags: ["hands-on", "refatoracao", "fastapi", "tests", "clean-code"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos fazer uma refatoração **na prática**.

Vamos pegar o código real da nossa API de crédito e identificar problemas típicos: lógica de negócio complexa dentro do serviço, cálculo de score com múltiplas regras não testadas isoladamente, e falta de separação entre feature engineering e predição. Vamos transformá-lo em um código organizado, testável e pronto para produção.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: A função `predict_one` em `model_service.py` tem 40+ linhas misturando cálculo de score, regras de negócio e decisão final.

**Agitação**: Quando surge uma nova regra de negócio (ex: limite de empréstimo baseado em idade), precisamos mexer em uma função gigante. Testar cada regra isoladamente é impossível.

**Solução**: Refatorar extraindo funções menores: `calculate_credit_score`, `apply_age_rules`, `apply_income_rules`. Cada uma testável, reutilizável e com responsabilidade única.

# 3. Objetivos de aprendizagem

Ao final você será capaz de:

1. **Refatorar** lógica de negócio complexa em funções menores
2. **Extrair** cálculos de features para módulo separado
3. **Criar** testes unitários para cada função extraída
4. **Comparar** estrutura original e refatorada

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+
- uv instalado
- Testes configurados

**Setup:**

```powershell
.\.venv\Scripts\Activate.ps1
uv run pytest -q
```

**Checklist de setup:**
- [ ] Ambiente virtual ativo
- [ ] Testes passando (todos os 8 testes)
- [ ] Git limpo (commit antes de refatorar)

# 5. Visão geral do que já existe no projeto (continuidade)

Estado atual:
```
swe4ds-credit-api/
├── src/
│   ├── main.py
│   ├── routes/
│   │   ├── predict.py      # Endpoint limpo
│   │   └── metrics.py
│   └── services/
│       └── model_service.py # 🔥 Precisa refatorar
├── tests/
│   ├── test_predict.py     # Testes de integração
│   └── test_health.py
└── logs/
```

**O que será alterado nesta parte:**
- Refatorar `services/model_service.py`
- Criar `services/scoring.py` (novo)
- Criar `services/business_rules.py` (novo)
- Adicionar testes unitários

# 6. Passo a passo (comandos + código)

## Passo 1: Analisar o código "antes" (Excalidraw: Slide 3)

**Intenção:** Ver o problema antes da refatoração.

Abra e analise o arquivo:

```powershell
code src/services/model_service.py
```

**Problemas identificados no código atual:**

```python
def predict_one(data: dict) -> dict:
    """40+ linhas fazendo muita coisa!"""
    # 1. Extração de features
    age = data.get("age", 0)
    income = data.get("income", 0)
    loan_amount = data.get("loan_amount", 0)
    credit_history = data.get("credit_history", "poor")
    
    # 2. Cálculo de score com múltiplas regras
    score = 0.5
    if credit_history == "good":
        score += 0.3
    elif credit_history == "fair":
        score += 0.1
    
    if age >= 25 and age <= 55:
        score += 0.1
    
    if income > loan_amount * 3:
        score += 0.2
    elif income > loan_amount * 2:
        score += 0.1
    
    # 3. Normalização
    score = min(1.0, max(0.0, score))
    
    # 4. Decisão
    prediction = "approved" if score >= 0.6 else "rejected"
    
    return {"prediction": prediction, "confidence": round(score, 3)}
```

**CHECKPOINT:** Função faz tudo: extração, cálculo, normalização e decisão.

---

## Passo 2: Extract Function - Scoring por histórico (Excalidraw: Slide 3)

**Intenção:** Isolar regras de histórico de crédito.

Crie o novo módulo:

```powershell
New-Item src/services/scoring.py -ItemType File
code src/services/scoring.py
```

Adicione as funções extraídas:

```python
"""Módulo de cálculo de score de crédito."""


def score_by_credit_history(credit_history: str) -> float:
    """
    Calcula pontuação baseada no histórico de crédito.
    
    Args:
        credit_history: Histórico do cliente ('good', 'fair', 'poor')
        
    Returns:
        float: Pontos adicionados ao score (0.0 a 0.3)
    """
    if credit_history == "good":
        return 0.3
    elif credit_history == "fair":
        return 0.1
    return 0.0


def score_by_age(age: int) -> float:
    """
    Calcula pontuação baseada na idade.
    
    Args:
        age: Idade do cliente
        
    Returns:
        float: Pontos adicionados ao score
    """
    if 25 <= age <= 55:
        return 0.1
    return 0.0


def score_by_income_ratio(income: float, loan_amount: float) -> float:
    """
    Calcula pontuação baseada na relação renda/empréstimo.
    
    Args:
        income: Renda mensal
        loan_amount: Valor solicitado
        
    Returns:
        float: Pontos adicionados ao score
    """
    if income > loan_amount * 3:
        return 0.2
    elif income > loan_amount * 2:
        return 0.1
    return 0.0


def calculate_credit_score(data: dict) -> float:
    """
    Calcula score de crédito completo.
    
    Args:
        data: Dicionário com features do cliente
        
    Returns:
        float: Score final entre 0.0 e 1.0
    """
    base_score = 0.5
    
    score = base_score
    score += score_by_credit_history(data.get("credit_history", "poor"))
    score += score_by_age(data.get("age", 0))
    score += score_by_income_ratio(
        data.get("income", 0),
        data.get("loan_amount", 0)
    )
    
    # Normaliza entre 0 e 1
    return min(1.0, max(0.0, score))
```

**CHECKPOINT:** Funções pequenas, testáveis e com responsabilidade única.

---

## Passo 3: Refatorar model_service.py (Excalidraw: Slide 4)

**Intenção:** Simplificar a função principal usando as novas funções.

Abra e edite:

```powershell
code src/services/model_service.py
```

```python
"""Serviço de modelo de ML (simulado)."""

import json
import logging
from pathlib import Path

from src.services.scoring import calculate_credit_score

logger = logging.getLogger("credit-api")

# Caminho para logs de drift
DRIFT_LOG_PATH = Path("logs/input_samples.jsonl")

# Threshold de aprovação
APPROVAL_THRESHOLD = 0.6


def load_model():
    """
    Carrega o modelo de ML.
    
    Nota: Por enquanto é um modelo simulado.
    Em produção, carregaria um modelo real treinado.
    
    Returns:
        dict: Configuração do modelo simulado
    """
    logger.info("Loading model...")
    return {
        "type": "simulated",
        "version": "0.1.0",
        "threshold": APPROVAL_THRESHOLD,
    }


def predict_one(data: dict) -> dict:
    """
    Realiza predição para um único registro.
    
    Args:
        data: Dicionário com features do cliente
        
    Returns:
        dict: Resultado da predição
    """
    # Calcula score usando funções isoladas
    score = calculate_credit_score(data)
    
    # Decisão baseada no threshold
    prediction = "approved" if score >= APPROVAL_THRESHOLD else "rejected"
    
    return {
        "prediction": prediction,
        "confidence": round(score, 3),
    }


def log_input_sample(payload: dict) -> None:
    """
    Registra amostra de entrada para análise de drift.
    
    Args:
        payload: Dados da requisição
    """
    try:
        DRIFT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with DRIFT_LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
    except Exception as e:
        logger.warning(f"Failed to log input sample: {e}")


# Carrega modelo na inicialização do módulo
MODEL = load_model()
```

**CHECKPOINT:** `predict_one` agora tem 5 linhas limpas!

---

## Passo 4: Criar testes unitários para scoring (Excalidraw: Slide 4)

**Intenção:** Garantir que cada regra funciona isoladamente.

Crie os testes:

```powershell
New-Item tests/test_scoring.py -ItemType File
code tests/test_scoring.py
```

```python
"""Testes unitários para módulo de scoring."""

from src.services.scoring import (
    calculate_credit_score,
    score_by_age,
    score_by_credit_history,
    score_by_income_ratio,
)


def test_score_by_credit_history_good():
    """Histórico bom retorna 0.3."""
    assert score_by_credit_history("good") == 0.3


def test_score_by_credit_history_fair():
    """Histórico regular retorna 0.1."""
    assert score_by_credit_history("fair") == 0.1


def test_score_by_credit_history_poor():
    """Histórico ruim retorna 0.0."""
    assert score_by_credit_history("poor") == 0.0


def test_score_by_age_in_range():
    """Idade na faixa ideal retorna 0.1."""
    assert score_by_age(30) == 0.1
    assert score_by_age(25) == 0.1
    assert score_by_age(55) == 0.1


def test_score_by_age_out_range():
    """Idade fora da faixa retorna 0.0."""
    assert score_by_age(20) == 0.0
    assert score_by_age(60) == 0.0


def test_score_by_income_ratio_high():
    """Renda > 3x empréstimo retorna 0.2."""
    assert score_by_income_ratio(10000, 3000) == 0.2


def test_score_by_income_ratio_medium():
    """Renda > 2x empréstimo retorna 0.1."""
    assert score_by_income_ratio(5000, 2000) == 0.1


def test_score_by_income_ratio_low():
    """Renda baixa retorna 0.0."""
    assert score_by_income_ratio(3000, 5000) == 0.0


def test_calculate_credit_score_best_case():
    """Melhor cenário deve dar score alto."""
    data = {
        "age": 35,
        "income": 10000,
        "loan_amount": 2000,
        "credit_history": "good"
    }
    score = calculate_credit_score(data)
    assert score == 1.0  # 0.5 + 0.3 + 0.1 + 0.2


def test_calculate_credit_score_worst_case():
    """Pior cenário deve dar score baixo."""
    data = {
        "age": 20,
        "income": 1000,
        "loan_amount": 5000,
        "credit_history": "poor"
    }
    score = calculate_credit_score(data)
    assert score == 0.5  # Apenas base score


def test_calculate_credit_score_medium():
    """Cenário médio."""
    data = {
        "age": 30,
        "income": 5000,
        "loan_amount": 2000,
        "credit_history": "fair"
    }
    score = calculate_credit_score(data)
    assert score == 0.8  # 0.5 + 0.1 + 0.1 + 0.1
```

**CHECKPOINT:** 13 testes unitários cobrindo cada regra isoladamente!

---

## Passo 5: Validar que tudo funciona

**Intenção:** Garantir que a refatoração não quebrou nada.

```powershell
# Rodar todos os testes
uv run pytest -v

# Deve mostrar:
# test_health.py::test_health_endpoint PASSED
# test_metrics.py::test_metrics_endpoint PASSED
# test_predict.py::test_predict_endpoint_with_valid_data PASSED
# test_predict.py::test_predict_endpoint_approved_scenario PASSED
# test_predict.py::test_predict_endpoint_rejected_scenario PASSED
# test_predict.py::test_predict_endpoint_with_invalid_age PASSED
# test_predict.py::test_predict_endpoint_with_invalid_credit_history PASSED
# test_predict.py::test_predict_endpoint_with_missing_field PASSED
# test_scoring.py::test_score_by_credit_history_good PASSED
# test_scoring.py::... (mais 12 testes)
```

**CHECKPOINT:** 21 testes passando! Refatoração segura concluída.

---

## Passo 6: Comparação Antes vs Depois (Excalidraw: Slide 5)

**Intenção:** Visualizar ganhos de qualidade.

### ANTES:
```python
# model_service.py - 40+ linhas
def predict_one(data: dict) -> dict:
    age = data.get("age", 0)
    income = data.get("income", 0)
    loan_amount = data.get("loan_amount", 0)
    credit_history = data.get("credit_history", "poor")
    
    score = 0.5
    if credit_history == "good":
        score += 0.3
    # ... muitas linhas
    return {"prediction": prediction, "confidence": score}
```

- ❌ Lógica misturada
- ❌ Difícil testar isoladamente
- ❌ Mudanças arriscadas

### DEPOIS:
```python
# model_service.py - 5 linhas
def predict_one(data: dict) -> dict:
    score = calculate_credit_score(data)
    prediction = "approved" if score >= APPROVAL_THRESHOLD else "rejected"
    return {"prediction": prediction, "confidence": round(score, 3)}

# scoring.py - Funções pequenas e testáveis
def score_by_credit_history(credit_history: str) -> float:
    ...
```

- ✅ Responsabilidades separadas
- ✅ Cada regra testada isoladamente
- ✅ Fácil adicionar novas regras

**CHECKPOINT:** Código mais limpo, testável e mantível.

# 7. Testes rápidos e validação

```powershell
# Rodar testes unitários
uv run pytest tests/test_scoring.py -v

# Rodar todos os testes
uv run pytest -v

# Subir API e testar manualmente
uv run uvicorn src.main:app --reload
```

Teste manual via PowerShell:

```powershell
$body = @{
    age = 35
    income = 8000.0
    loan_amount = 2000.0
    credit_history = "good"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/predict -Method Post -Body $body -ContentType "application/json"
```

# 8. Observabilidade e boas práticas (mini-bloco)

1. **Funções pequenas**: cada uma com <10 linhas. Trade-off: mais arquivos, mas mais testável.
2. **Single Responsibility**: cada função faz uma coisa só. Trade-off: mais funções, mas menor acoplamento.
3. **Testes unitários rápidos**: rodam em <1s. Trade-off: esforço inicial, mas segurança contínua.
4. **Constantes explícitas**: `APPROVAL_THRESHOLD` no topo. Trade-off: mais variáveis, mas configurável.

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `ModuleNotFoundError: No module named 'src.services.scoring'` | Import errado | Verificar caminho e __init__.py |
| Testes antigos falharam | Comportamento mudou | Revisar se lógica está igual |
| Score diferente do esperado | Regras alteradas | Ajustar testes ou lógica |
| Import circular | Módulos se importando | Reorganizar dependências |

# 10. Exercícios (básico e avançado)

**Básico 1:** Adicionar nova regra: desconto de 0.05 se `age > 60`.
- Criar `score_by_senior` em `scoring.py`
- Adicionar teste unitário
- Integrar em `calculate_credit_score`

**Básico 2:** Extrair validações de negócio para `business_rules.py`.
- Criar função `validate_loan_eligibility`
- Validar se `income >= loan_amount * 0.3` (mínimo 30%)
- Adicionar testes

**Avançado:** Criar sistema de pesos configurável.
- Substituir valores fixos (0.3, 0.2, etc) por um dict de configuração
- Permitir ajustar pesos sem mudar código
- Adicionar testes parametrizados

# 11. Resultados e Lições

**Resultados (como medir):**
- Linhas por função: de 40 para 5 em `predict_one`
- Cobertura de testes: de 0% para ~95% nas regras de score
- Número de funções testáveis: de 1 para 5
- Tempo de adição de nova regra: de horas para minutos

**Lições:**
- Refatoração não muda comportamento, melhora design
- Funções pequenas são mais fáceis de entender e testar
- Separação de responsabilidades facilita evolução
- Testes unitários dão confiança para mudanças

# 12. Encerramento e gancho para a próxima aula (script)

Nesta aula você realizou uma refatoração prática real, transformando uma função complexa de 40 linhas em módulos limpos e testáveis, aumentando a cobertura de testes de forma significativa.

Na próxima parte, vamos aprender a **reorganizar o projeto completo** com uma estrutura profissional baseada no Cookiecutter Data Science, integrando nossa API refatorada em uma estrutura escalável para produção.
