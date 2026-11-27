---
titulo: "Aula 06 – Parte 03: Padrões de Design em Data Science - Strategy Pattern e Outros Exemplos"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 20
prerequisitos:
  - "Python 3.12+"
  - "Aula 06 - Partes 01 e 02 concluídas"
  - "Conhecimento de classes em Python"
tags: ["design-patterns", "strategy-pattern", "factory", "python-idioms", "clean-code"]
---

# 1. Abertura do vídeo (script)

Olá! Nas aulas anteriores você aprendeu sobre estilo de código e princípios de código limpo. Agora vamos falar sobre **padrões de design** - soluções testadas e aprovadas para problemas que aparecem repetidamente em software.

Muita gente acha que padrões de design são coisa de desenvolvedor Java enterprise, que Data Scientists não precisam disso. Eu discordo parcialmente. Você não precisa conhecer todos os 23 padrões do livro do Gang of Four. Mas alguns padrões são extremamente úteis no dia a dia de ML.

O mais útil para nós é o **Strategy Pattern**. Imagina que você tem um pipeline que pode usar Random Forest, XGBoost ou LightGBM dependendo da configuração. Como organizar isso de forma limpa? O Strategy Pattern resolve exatamente esse problema.

Nesta aula vamos aprender esse padrão na prática, ver alguns outros úteis, e entender quando usar - e quando **não usar** padrões. O perigo do over-engineering é real.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Seu pipeline de ML precisa suportar múltiplos modelos. Você começa com Random Forest. Depois pedem XGBoost. Depois LightGBM. Depois um modelo customizado.

**Agitação**: O código vira uma cascata de if-elif:

```python
if model_type == "rf":
    model = RandomForestClassifier()
    model.fit(X, y, ...)
elif model_type == "xgb":
    model = XGBClassifier()
    model.fit(X, y, ...)
elif model_type == "lgb":
    model = LGBMClassifier()
    model.fit(X, y, train_set=...)  # API diferente!
# ... mais 10 elif ...
```

Cada modelo tem uma API ligeiramente diferente. Os ifs se espalham por todo o código. Adicionar um novo modelo significa caçar todos os lugares que precisam de elif.

**Solução**: Strategy Pattern. Cada modelo é uma "estratégia" com a mesma interface. O código principal não sabe qual modelo está usando - só chama `model.fit()` e `model.predict()`. Adicionar um novo modelo é criar uma nova classe, sem mexer no código existente.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Implementar** o Strategy Pattern em Python
2. **Aplicar** o padrão para alternar modelos de ML
3. **Reconhecer** quando usar Observer e Factory patterns
4. **Usar** idiomas Pythônicos (list comprehensions, generators)
5. **Avaliar** trade-offs entre padrões e simplicidade
6. **Evitar** over-engineering em projetos de DS

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Ambiente do projeto configurado
- Código limpo (sem code smells óbvios)

**Verificar ambiente:**

```bash
# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Ativar ambiente
.\.venv\Scripts\Activate.ps1

# Verificar código limpo
ruff check src/ tests/
```

**Checklist:**
- [ ] Ambiente virtual ativado
- [ ] Código sem erros de lint
- [ ] Entendimento de classes em Python

# 5. Visão geral do que já existe no projeto (continuidade)

**Estado atual:**
```
swe4ds-credit-api/
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── validation.py
│   └── models/                 # NOVO: Vamos criar
│       ├── __init__.py
│       └── strategies.py       # Strategy Pattern
├── tests/
└── ...
```

**O que vamos fazer nesta aula:**
- Criar estrutura de modelos usando Strategy Pattern
- Implementar estratégias para diferentes algoritmos
- Usar idiomas Pythônicos no código

# 6. Passo a passo (comandos + código)

## Passo 1: Entendendo o Strategy Pattern (Excalidraw: Slide 3)

**Intenção**: Compreender o padrão antes de implementar.

### O que é Strategy Pattern?

> Define uma família de algoritmos, encapsula cada um, e os torna intercambiáveis.

Em palavras simples: você tem várias formas de fazer a mesma coisa, e quer poder trocar entre elas facilmente.

### Estrutura

```
┌─────────────────────────────────────────────────┐
│                   Context                        │
│  (usa estratégia, não sabe qual)                │
│                                                  │
│  - strategy: Strategy                            │
│  + execute(): chama strategy.algorithm()        │
└─────────────────────────────────────────────────┘
                        │
                        ▼ usa
┌─────────────────────────────────────────────────┐
│              Strategy (Interface)               │
│                                                  │
│  + algorithm(): abstrato                        │
└─────────────────────────────────────────────────┘
            ▲               ▲               ▲
            │               │               │
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ ConcreteA     │  │ ConcreteB     │  │ ConcreteC     │
│               │  │               │  │               │
│ +algorithm()  │  │ +algorithm()  │  │ +algorithm()  │
│  (implementa) │  │  (implementa) │  │  (implementa) │
└───────────────┘  └───────────────┘  └───────────────┘
```

### Em ML

- **Context**: Pipeline de treinamento
- **Strategy**: Interface de modelo (fit, predict)
- **Concrete**: RandomForest, XGBoost, LightGBM

**CHECKPOINT**: Você entende a estrutura do padrão.

---

## Passo 2: Implementando Strategy Pattern para Modelos (Excalidraw: Slide 4)

**Intenção**: Criar estrutura flexível para múltiplos modelos.

### Criar pasta de modelos

```bash
# Criar estrutura
mkdir src/models
New-Item src/models/__init__.py -ItemType File
```

Abra o `src/models/__init__.py` e adicione um export mínimo (diff lógico):

```python
# (ADICIONAR no arquivo)
"""Pacote de estratégias de modelos."""

from .strategies import (
    DummyStrategy,
    LogisticRegressionStrategy,
    ModelFactory,
    ModelStrategy,
    RandomForestStrategy,
)

__all__ = [
    "ModelStrategy",
    "RandomForestStrategy",
    "LogisticRegressionStrategy",
    "DummyStrategy",
    "ModelFactory",
]
```

### Criar arquivo de estratégias

Criar `src/models/strategies.py`:

```python
"""
Estratégias de modelos de ML usando Strategy Pattern.

Este módulo implementa diferentes algoritmos de classificação
com uma interface unificada para facilitar experimentação.
"""

from abc import ABC, abstractmethod
from typing import Any

import numpy as np
from numpy.typing import NDArray


class ModelStrategy(ABC):
    """Interface base para estratégias de modelo."""

    @abstractmethod
    def fit(self, X: NDArray, y: NDArray) -> None:
        """Treina o modelo com dados de entrada."""
        pass

    @abstractmethod
    def predict(self, X: NDArray) -> NDArray:
        """Faz predições com o modelo treinado."""
        pass

    @abstractmethod
    def predict_proba(self, X: NDArray) -> NDArray:
        """Retorna probabilidades de predição."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Nome descritivo do modelo."""
        pass


class RandomForestStrategy(ModelStrategy):
    """Estratégia usando Random Forest."""

    def __init__(self, n_estimators: int = 100, **kwargs: Any) -> None:
        from sklearn.ensemble import RandomForestClassifier

        self._model = RandomForestClassifier(
            n_estimators=n_estimators,
            **kwargs,
        )

    def fit(self, X: NDArray, y: NDArray) -> None:
        self._model.fit(X, y)

    def predict(self, X: NDArray) -> NDArray:
        return self._model.predict(X)

    def predict_proba(self, X: NDArray) -> NDArray:
        return self._model.predict_proba(X)

    @property
    def name(self) -> str:
        return "RandomForest"


class LogisticRegressionStrategy(ModelStrategy):
    """Estratégia usando Regressão Logística."""

    def __init__(self, **kwargs: Any) -> None:
        from sklearn.linear_model import LogisticRegression

        self._model = LogisticRegression(**kwargs)

    def fit(self, X: NDArray, y: NDArray) -> None:
        self._model.fit(X, y)

    def predict(self, X: NDArray) -> NDArray:
        return self._model.predict(X)

    def predict_proba(self, X: NDArray) -> NDArray:
        return self._model.predict_proba(X)

    @property
    def name(self) -> str:
        return "LogisticRegression"


class DummyStrategy(ModelStrategy):
    """Estratégia dummy para testes e baseline."""

    def __init__(self, strategy: str = "most_frequent") -> None:
        from sklearn.dummy import DummyClassifier

        self._model = DummyClassifier(strategy=strategy)

    def fit(self, X: NDArray, y: NDArray) -> None:
        self._model.fit(X, y)

    def predict(self, X: NDArray) -> NDArray:
        return self._model.predict(X)

    def predict_proba(self, X: NDArray) -> NDArray:
        return self._model.predict_proba(X)

    @property
    def name(self) -> str:
        return "Dummy"
```

### Usar as estratégias

```python
# Em qualquer lugar do código:
from src.models.strategies import (
    ModelStrategy,
    RandomForestStrategy,
    LogisticRegressionStrategy,
)

# Trocar modelo é trocar uma linha
model: ModelStrategy = RandomForestStrategy(n_estimators=200)
# ou
model: ModelStrategy = LogisticRegressionStrategy(max_iter=1000)

# O resto do código não muda!
model.fit(X_train, y_train)
predictions = model.predict(X_test)
probas = model.predict_proba(X_test)
```

**CHECKPOINT**: Strategy Pattern implementado para modelos.

### Teste rápido (mão na massa)

Crie `tests/test_strategies.py` com testes simples de inicialização:

```python
"""Testes básicos das estratégias de modelo."""

from src.models.strategies import DummyStrategy, LogisticRegressionStrategy, RandomForestStrategy


def test_random_forest_strategy_name():
    model = RandomForestStrategy(n_estimators=10)
    assert model.name == "RandomForest"


def test_logistic_strategy_name():
    model = LogisticRegressionStrategy(max_iter=100)
    assert model.name == "LogisticRegression"


def test_dummy_strategy_name():
    model = DummyStrategy(strategy="most_frequent")
    assert model.name == "Dummy"
```

```bash
# Rodar somente os testes novos
uv run pytest tests/test_strategies.py -v
```

**CHECKPOINT**: Testes de estratégias passam.

---

## Passo 3: Factory Pattern para Criar Estratégias (Excalidraw: Slide 7)

**Intenção**: Centralizar a criação de modelos.

### O que é Factory Pattern?

Encapsula a lógica de criação de objetos. Útil quando a criação é complexa ou precisa ser configurável.

### Implementação

Adicionar ao `src/models/strategies.py` (diff lógico — cole ao final do arquivo):

```python
class ModelFactory:
    """Factory para criar estratégias de modelo."""

    _strategies: dict[str, type[ModelStrategy]] = {
        "random_forest": RandomForestStrategy,
        "logistic_regression": LogisticRegressionStrategy,
        "dummy": DummyStrategy,
    }

    @classmethod
    def create(cls, name: str, **kwargs: Any) -> ModelStrategy:
        """Cria uma estratégia de modelo pelo nome.

        Args:
            name: Nome do modelo (random_forest, logistic_regression, dummy)
            **kwargs: Parâmetros para o modelo

        Returns:
            Instância da estratégia de modelo

        Raises:
            ValueError: Se o nome não for reconhecido
        """
        if name not in cls._strategies:
            available = ", ".join(cls._strategies.keys())
            raise ValueError(
                f"Modelo '{name}' não encontrado. "
                f"Disponíveis: {available}"
            )
        return cls._strategies[name](**kwargs)

    @classmethod
    def register(cls, name: str, strategy: type[ModelStrategy]) -> None:
        """Registra uma nova estratégia.

        Args:
            name: Nome para o modelo
            strategy: Classe da estratégia
        """
        cls._strategies[name] = strategy

    @classmethod
    def available(cls) -> list[str]:
        """Retorna nomes de modelos disponíveis."""
        return list(cls._strategies.keys())
```

### Uso

```python
from src.models.strategies import ModelFactory

# Criar modelo por nome (útil para configs)
model = ModelFactory.create("random_forest", n_estimators=200)

# Listar disponíveis
print(ModelFactory.available())
# ['random_forest', 'logistic_regression', 'dummy']

# Adicionar modelo customizado
ModelFactory.register("my_model", MyCustomStrategy)
```

**CHECKPOINT**: Factory Pattern centraliza criação de modelos.

---

## Passo 4: Observer Pattern (Simplificado) (Excalidraw: Slide 7)

**Intenção**: Entender quando usar notificações entre objetos.

### O que é Observer Pattern?

Define dependência um-para-muitos. Quando um objeto muda estado, todos os dependentes são notificados.

### Uso em ML

Útil para:
- Callbacks de treinamento (logs, early stopping)
- Métricas em tempo real
- Notificações de pipeline

### Exemplo Simples

```python
from typing import Callable

class TrainingObserver:
    """Observador simples para eventos de treinamento."""

    def __init__(self) -> None:
        self._callbacks: list[Callable[[dict], None]] = []

    def register(self, callback: Callable[[dict], None]) -> None:
        """Registra callback para eventos."""
        self._callbacks.append(callback)

    def notify(self, event: dict) -> None:
        """Notifica todos os callbacks."""
        for callback in self._callbacks:
            callback(event)


# Uso
observer = TrainingObserver()

# Registrar callbacks
observer.register(lambda e: print(f"Época {e['epoch']}: loss={e['loss']:.4f}"))
observer.register(lambda e: mlflow.log_metric("loss", e["loss"], step=e["epoch"]))

# Durante treinamento
for epoch in range(10):
    loss = train_one_epoch()
    observer.notify({"epoch": epoch, "loss": loss})
```

### Na Prática

Muitos frameworks já implementam isso:
- Keras: `callbacks` em `model.fit()`
- PyTorch Lightning: `Callbacks`
- Scikit-learn: Não tem (você pode adicionar)

**CHECKPOINT**: Observer Pattern notifica múltiplos interessados.

---

## Passo 5: Idiomas Pythônicos (Excalidraw: Slide 7)

**Intenção**: Usar recursos da linguagem para código mais limpo.

### List Comprehensions

```python
# RUIM: Loop explícito
filtered = []
for item in items:
    if item > 0:
        filtered.append(item * 2)

# BOM: List comprehension
filtered = [item * 2 for item in items if item > 0]
```

### Dictionary Comprehensions

```python
# RUIM: Loop explícito
scores = {}
for name, value in results:
    scores[name] = round(value, 2)

# BOM: Dict comprehension
scores = {name: round(value, 2) for name, value in results}
```

### Generator Expressions (memória eficiente)

```python
# RUIM: Cria lista inteira na memória
total = sum([x**2 for x in range(1_000_000)])

# BOM: Generator, processa um por vez
total = sum(x**2 for x in range(1_000_000))
```

### Context Managers

```python
# RUIM: Pode esquecer de fechar
f = open("file.txt")
data = f.read()
f.close()

# BOM: Garante fechamento
with open("file.txt") as f:
    data = f.read()
```

### Walrus Operator (:=)

```python
# RUIM: Repetição
if len(data) > 10:
    print(f"Data tem {len(data)} itens")

# BOM: Atribui e usa
if (n := len(data)) > 10:
    print(f"Data tem {n} itens")
```

### Structural Pattern Matching (Python 3.10+)

```python
# RUIM: Cascata de if-elif
if status == 200:
    handle_success(response)
elif status == 404:
    handle_not_found()
elif status in (500, 502, 503):
    handle_server_error(status)
else:
    handle_unknown(status)

# BOM: Match statement
match status:
    case 200:
        handle_success(response)
    case 404:
        handle_not_found()
    case 500 | 502 | 503:
        handle_server_error(status)
    case _:
        handle_unknown(status)
```

**CHECKPOINT**: Idiomas Pythônicos deixam código mais expressivo.

---

## Passo 6: Evitando Over-Engineering (Excalidraw: Slide 7)

**Intenção**: Saber quando NÃO usar padrões.

### YAGNI: You Ain't Gonna Need It

> Não implemente algo até que você realmente precise.

### Sinais de Over-Engineering

| Sinal | Problema |
|-------|----------|
| Abstract classes para 1 implementação | Complexidade sem benefício |
| Factory para 2-3 classes simples | Um `if` seria suficiente |
| 10 arquivos para 100 linhas de código | Fragmentação excessiva |
| Padrões que ninguém do time conhece | Barreira de entrada |
| Configuração maior que código | Prioridades invertidas |

### Quando Usar Padrões

✅ **USE quando:**
- Problema é recorrente e bem definido
- Time conhece o padrão
- Flexibilidade é realmente necessária
- Código será mantido por muito tempo

❌ **EVITE quando:**
- É um script único ou protótipo
- Solução simples resolve
- Você está "preparando para o futuro"
- Ninguém além de você entende

### Exemplo: Strategy vs. Simples

```python
# Se você tem APENAS 2 modelos e não vai mudar:

# OVER-ENGINEERING
class ModelStrategy(ABC): ...
class RFStrategy(ModelStrategy): ...
class LRStrategy(ModelStrategy): ...
class ModelFactory: ...

# SIMPLES E SUFICIENTE
def create_model(name: str):
    if name == "rf":
        return RandomForestClassifier()
    return LogisticRegression()
```

O Strategy Pattern faz sentido quando:
- Você tem 4+ implementações
- Novas implementações são esperadas
- O comportamento varia de formas complexas

**CHECKPOINT**: Simplicidade primeiro, padrões quando necessário.

---

## Passo 7: Integrar ao Projeto

**Intenção**: Aplicar o aprendizado no projeto real.

### Atualizar exports

Criar `src/models/__init__.py`:

```python
"""Módulo de modelos de ML."""

from src.models.strategies import (
    DummyStrategy,
    LogisticRegressionStrategy,
    ModelFactory,
    ModelStrategy,
    RandomForestStrategy,
)

__all__ = [
    "ModelStrategy",
    "RandomForestStrategy",
    "LogisticRegressionStrategy",
    "DummyStrategy",
    "ModelFactory",
]
```

### Criar testes

Criar `tests/test_models.py`:

```python
"""Testes para estratégias de modelo."""

import numpy as np
import pytest

from src.models import (
    DummyStrategy,
    LogisticRegressionStrategy,
    ModelFactory,
    RandomForestStrategy,
)


@pytest.fixture
def sample_data():
    """Dados de exemplo para testes."""
    np.random.seed(42)
    X = np.random.randn(100, 5)
    y = (X[:, 0] > 0).astype(int)
    return X, y


class TestModelStrategies:
    """Testes para estratégias de modelo."""

    def test_random_forest_strategy(self, sample_data):
        X, y = sample_data
        model = RandomForestStrategy(n_estimators=10)

        model.fit(X, y)
        predictions = model.predict(X)
        probas = model.predict_proba(X)

        assert len(predictions) == len(y)
        assert probas.shape == (len(y), 2)
        assert model.name == "RandomForest"

    def test_logistic_regression_strategy(self, sample_data):
        X, y = sample_data
        model = LogisticRegressionStrategy()

        model.fit(X, y)
        predictions = model.predict(X)

        assert len(predictions) == len(y)
        assert model.name == "LogisticRegression"

    def test_dummy_strategy(self, sample_data):
        X, y = sample_data
        model = DummyStrategy()

        model.fit(X, y)
        predictions = model.predict(X)

        assert len(predictions) == len(y)
        assert model.name == "Dummy"


class TestModelFactory:
    """Testes para factory de modelos."""

    def test_create_random_forest(self):
        model = ModelFactory.create("random_forest", n_estimators=10)
        assert isinstance(model, RandomForestStrategy)

    def test_create_invalid_model(self):
        with pytest.raises(ValueError, match="não encontrado"):
            ModelFactory.create("invalid_model")

    def test_available_models(self):
        available = ModelFactory.available()
        assert "random_forest" in available
        assert "logistic_regression" in available
        assert "dummy" in available
```

### Rodar testes

```bash
# Instalar sklearn se necessário
uv add scikit-learn

# Rodar testes
task test

# Verificar cobertura
task test-cov
```

**CHECKPOINT**: Estratégias testadas e integradas.

# 7. Testes rápidos e validação

```bash
# Verificar lint
ruff check src/ tests/

# Rodar testes específicos
uv run pytest tests/test_models.py -v

# Verificar que Factory funciona
uv run python -c "
from src.models import ModelFactory
print('Modelos disponíveis:', ModelFactory.available())
model = ModelFactory.create('dummy')
print('Modelo criado:', model.name)
"
```

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas com Padrões de Design

1. **Conheça antes de usar**
   - Estude o padrão, não copie código
   - Entenda quando é apropriado
   - **Trade-off**: Tempo de aprendizado, mas uso correto

2. **Documente a intenção**
   - Deixe claro por que usou o padrão
   - Ajude outros desenvolvedores
   - **Trade-off**: Documentação extra, mas onboarding fácil

3. **Comece simples**
   - If-elif está ok para começar
   - Refatore para padrão quando necessário
   - **Trade-off**: Refatoração futura, mas não over-engineer

4. **Prefira composição sobre herança**
   - Herança é rígida
   - Composição é flexível
   - **Trade-off**: Mais objetos, mas mais flexibilidade

5. **Use tipos para documentar interfaces**
   - Type hints mostram o contrato
   - ABC define interface formal
   - **Trade-off**: Mais código, mas mais segurança

# 9. Troubleshooting (erros comuns)

| Problema | Causa | Solução |
|----------|-------|---------|
| "ABC não pode ser instanciada" | Método abstrato não implementado | Implementar todos os `@abstractmethod` |
| Over-engineering | Padrão usado desnecessariamente | Avaliar se `if-elif` resolve |
| Circular imports | Estrutura de módulos errada | Reorganizar imports |
| Strategy não intercambiável | Interfaces diferentes | Padronizar métodos |
| Factory muito complexa | Registros dinâmicos demais | Simplificar para dict |
| Testes difíceis | Dependências concretas | Usar injeção de dependência |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Nova Estratégia

Implemente `GradientBoostingStrategy` seguindo o padrão existente. Registre na Factory.

**Critério de sucesso**: Testes passando com nova estratégia.

## Exercício Básico 2: Idiomas Pythônicos

Refatore este código usando idiomas Pythônicos:

```python
results = []
for i in range(len(data)):
    if data[i]["score"] > 0.5:
        item = {}
        item["id"] = data[i]["id"]
        item["score"] = data[i]["score"]
        results.append(item)
```

**Critério de sucesso**: Uma linha de list/dict comprehension.

## Exercício Avançado: Pipeline com Strategy

Crie um `TrainingPipeline` que:
1. Aceite qualquer `ModelStrategy`
2. Implemente cross-validation
3. Use Observer para callbacks
4. Tenha testes completos

**Critério de sucesso**: Pipeline funcionando com testes e documentação.

# 11. Resultados e Lições

## Padrões Aprendidos

| Padrão | Uso em ML | Quando usar |
|--------|-----------|-------------|
| Strategy | Alternar modelos/algoritmos | 3+ implementações |
| Factory | Criar objetos por config | Criação complexa |
| Observer | Callbacks de treinamento | Notificações múltiplas |

## Lições desta Aula

1. **Strategy Pattern** encapsula algoritmos intercambiáveis
2. **Factory Pattern** centraliza criação de objetos
3. **Observer Pattern** notifica múltiplos interessados
4. **Idiomas Pythônicos** deixam código mais expressivo
5. **Over-engineering é perigoso** - simplicidade primeiro

# 12. Encerramento e gancho para a próxima aula (script)

Nesta aula você aprendeu padrões de design úteis para Data Science: Strategy para alternar modelos, Factory para criação centralizada, e Observer para callbacks. Você também viu idiomas Pythônicos que deixam o código mais limpo e expressivo.

O mais importante: você aprendeu a avaliar **quando usar** e **quando evitar** padrões. Simplicidade é uma virtude. Padrões são ferramentas, não objetivos.

Na próxima aula, vamos colocar tudo em prática com um **exemplo completo de refatoração**. Você vai pegar um código "espaguete" típico de notebook e transformá-lo em código profissional, aplicando todos os princípios e padrões que aprendemos.

Será como um before/after de reforma de casa, mas com código. Até a próxima aula!
