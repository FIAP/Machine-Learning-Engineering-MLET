---
titulo: "Aula 06 – Parte 01: PEP 8 e Convenções de Estilo em Python"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 20
prerequisitos:
  - "Python 3.12+"
  - "UV instalado"
  - "Ruff configurado (Aula 05)"
  - "Projeto swe4ds-credit-api"
tags: ["pep8", "style-guide", "linter", "ruff", "code-quality"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos falar sobre algo que parece trivial mas faz toda a diferença em projetos profissionais: **convenções de estilo de código**.

Você já abriu um código Python e ficou perdido porque cada função tinha um estilo diferente? Variáveis em camelCase misturadas com snake_case, indentação inconsistente, imports espalhados pelo arquivo? Isso não é apenas feio - é um problema real de manutenção.

A comunidade Python criou a **PEP 8** justamente para resolver isso. É um guia de estilo que define como código Python deve ser formatado. Quando todo mundo segue o mesmo padrão, o código fica mais fácil de ler, revisar e manter.

Na Aula 05, você já configurou o Ruff como linter e formatador. Agora vamos entender **por que** essas regras existem e como aplicá-las conscientemente no nosso projeto de crédito.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você trabalha em um projeto de Data Science com mais 3 pessoas. Cada um tem seu estilo: Maria usa tabs, João usa 2 espaços, você usa 4 espaços. Maria nomeia variáveis em português, João em inglês com camelCase, você em inglês com snake_case.

**Agitação**: Code reviews viram discussões sobre estilo em vez de lógica. "Muda isso para snake_case", "Arruma a indentação", "Import errado". O PR que deveria ser aprovado em 10 minutos leva 2 dias. Pior: bugs passam despercebidos porque o revisor está distraído com problemas de formatação. O código vira uma colcha de retalhos impossível de manter.

**Solução**: A equipe adota a PEP 8 como padrão. Configuram Ruff para formatar automaticamente. Agora o código é consistente - não importa quem escreveu. Code reviews focam em lógica e arquitetura. O time é mais produtivo e o código mais profissional.

No nosso projeto de crédito, vamos garantir que todo código siga PEP 8, usando Ruff para automatizar a verificação.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Explicar** a importância de guias de estilo para colaboração
2. **Aplicar** as principais regras da PEP 8 (indentação, nomes, imports)
3. **Identificar** violações de estilo em código Python
4. **Usar** Ruff para detectar e corrigir problemas automaticamente
5. **Configurar** regras de estilo no pyproject.toml
6. **Justificar** decisões de estilo em code reviews

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Ruff instalado (configurado na Aula 05)
- Projeto swe4ds-credit-api

**Verificar ambiente:**

```bash
# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Ativar ambiente
.\.venv\Scripts\Activate.ps1

# Verificar Ruff
ruff --version

# Verificar configuração existente
cat pyproject.toml | Select-String -Pattern "ruff" -Context 0,5
```

**Checklist:**
- [ ] Ambiente virtual ativado
- [ ] Ruff disponível
- [ ] pyproject.toml com configuração de Ruff

# 5. Visão geral do que já existe no projeto (continuidade)

**Estado atual:**
```
swe4ds-credit-api/
├── .venv/
├── pyproject.toml              # Já tem [tool.ruff]
├── uv.lock
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   └── validation.py
├── tests/
│   └── test_validation.py
└── ...
```

**O que vamos fazer nesta aula:**
- Entender as regras PEP 8 que o Ruff aplica
- Revisar e melhorar a configuração do Ruff
- Aplicar padrões no código existente

# 6. Passo a passo (comandos + código)

## Passo 1: O que é PEP 8? (Excalidraw: Slide 1)

**Intenção**: Entender o contexto e importância da PEP 8.

### PEP = Python Enhancement Proposal

- PEP 8 foi escrita por Guido van Rossum (criador do Python)
- Define convenções de estilo para código Python
- Não é lei, mas é o padrão da comunidade
- "Readability counts" - Zen do Python

### Por que seguir?

| Benefício | Descrição |
|-----------|-----------|
| **Consistência** | Todo código parece escrito pela mesma pessoa |
| **Legibilidade** | Mais fácil de ler e entender |
| **Colaboração** | Menos atrito em code reviews |
| **Onboarding** | Novos membros aprendem mais rápido |
| **Ferramentas** | Linters e formatadores funcionam melhor |

### Filosofia

> "Code is read much more often than it is written."
> — PEP 8

Você escreve código uma vez, mas ele é lido dezenas de vezes por você e outros.

**CHECKPOINT**: Você entende que PEP 8 é o guia de estilo padrão do Python.

---

## Passo 2: Indentação e Espaçamento (Excalidraw: Slide 1)

**Intenção**: Dominar as regras de indentação.

### Regra: 4 espaços por nível

```python
# CORRETO: 4 espaços
def calcular_score(limite, idade):
    if limite > 0:
        score = limite * 0.01
        if idade > 25:
            score += 10
        return score
    return 0

# ERRADO: 2 espaços
def calcular_score(limite, idade):
  if limite > 0:  # Inconsistente!
    score = limite * 0.01
    return score
```

### Regra: Linhas longas (máximo 88-120 caracteres)

```python
# RUIM: Linha muito longa
resultado = funcao_com_nome_grande(argumento_um, argumento_dois, argumento_tres, argumento_quatro, argumento_cinco)

# BOM: Quebra com indentação de continuação
resultado = funcao_com_nome_grande(
    argumento_um,
    argumento_dois,
    argumento_tres,
    argumento_quatro,
    argumento_cinco,
)
```

### Regra: Espaços em operadores

```python
# CORRETO
x = 1
y = x + 2
lista = [1, 2, 3]
dicionario = {"chave": "valor"}

# ERRADO
x=1
y = x+2
lista = [1,2,3]
dicionario = {"chave" : "valor"}
```

### Regra: Linhas em branco

```python
# CORRETO: 2 linhas entre funções top-level
def funcao_um():
    pass


def funcao_dois():
    pass


# CORRETO: 1 linha entre métodos de classe
class MinhaClasse:
    def metodo_um(self):
        pass

    def metodo_dois(self):
        pass
```

**CHECKPOINT**: Você conhece as regras de indentação e espaçamento.

---

## Passo 3: Convenções de Nomes (Excalidraw: Slide 1)

**Intenção**: Aprender os padrões de nomenclatura Python.

### Tabela de Convenções

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| Variáveis | snake_case | `limite_credito` |
| Funções | snake_case | `calcular_score()` |
| Constantes | UPPER_SNAKE_CASE | `MAX_LIMITE = 100000` |
| Classes | PascalCase | `ClienteCredito` |
| Módulos | snake_case | `data_loader.py` |
| Pacotes | snake_case | `credit_api` |
| Privados | _prefixo | `_validar_interno()` |
| "Dunder" | __double__ | `__init__`, `__str__` |

### Exemplos Práticos

```python
# Constantes (no topo do módulo)
MAX_CREDIT_LIMIT = 1_000_000
DEFAULT_INTEREST_RATE = 0.15

# Classes
class CreditApplication:
    """Representa uma aplicação de crédito."""
    
    def __init__(self, client_id: int, requested_amount: float):
        self.client_id = client_id
        self.requested_amount = requested_amount
        self._internal_score = None  # Privado
    
    def calculate_score(self) -> float:
        """Calcula o score de crédito."""
        return self._compute_internal_score()
    
    def _compute_internal_score(self) -> float:
        """Método interno - não usar diretamente."""
        return 0.5

# Funções
def validate_credit_limit(limit: float) -> bool:
    """Valida se o limite está dentro dos parâmetros."""
    return 0 < limit <= MAX_CREDIT_LIMIT
```

### Nomes Descritivos vs. Abreviados

```python
# RUIM: Abreviações obscuras
def calc_sc(l, a, e):
    return l * 0.01 + a * 0.5 + e * 2

# BOM: Nomes descritivos
def calculate_credit_score(
    credit_limit: float,
    age: int,
    education_level: int,
) -> float:
    return credit_limit * 0.01 + age * 0.5 + education_level * 2
```

**CHECKPOINT**: Você sabe qual convenção usar para cada tipo de identificador.

---

## Passo 4: Organização de Imports (Excalidraw: Slide 1)

**Intenção**: Estruturar imports de forma consistente.

### Ordem dos Imports (PEP 8)

```python
# 1. Biblioteca padrão
import os
import sys
from collections import defaultdict
from typing import Any, Optional

# 2. Bibliotecas de terceiros
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 3. Imports locais (do seu projeto)
from src.validation import validate_limit_bal
from src.data_loader import load_credit_data
```

### Regras de Organização

```python
# CORRETO: Separados por linha em branco, alfabéticos
import os
import sys

import numpy as np
import pandas as pd

from src.validation import validate_age, validate_limit_bal

# ERRADO: Misturados, sem ordem
from src.validation import validate_limit_bal
import pandas as pd
import os
import numpy as np
from src.data_loader import load_data
import sys
```

### Imports Absolutos vs. Relativos

```python
# PREFERIDO: Import absoluto
from src.validation import validate_limit_bal

# ACEITÁVEL: Import relativo (dentro do mesmo pacote)
from .validation import validate_limit_bal

# EVITAR: Import com *
from src.validation import *  # Não faça isso!
```

**CHECKPOINT**: Você sabe organizar imports seguindo PEP 8.

---

## Passo 5: Ruff como Guardião do Estilo (Excalidraw: Slide 1)

**Intenção**: Usar Ruff para automatizar verificação de estilo.

### Verificando o Código

```bash
# Verificar todo o código
ruff check src/ tests/

# Ver detalhes de um erro específico
ruff rule E501  # Explica a regra E501

# Corrigir automaticamente
ruff check src/ tests/ --fix
```

### Entendendo os Códigos de Erro

| Prefixo | Origem | Exemplo |
|---------|--------|---------|
| E | pycodestyle (erros) | E501: linha longa |
| W | pycodestyle (warnings) | W291: whitespace no final |
| F | Pyflakes | F401: import não usado |
| I | isort | I001: imports não ordenados |
| B | flake8-bugbear | B008: default mutável |
| UP | pyupgrade | UP035: sintaxe antiga |

### Exemplo de Saída

```bash
$ ruff check src/
src/data_loader.py:5:1: I001 Import block is un-sorted or un-formatted
src/validation.py:15:89: E501 Line too long (95 > 88)
src/validation.py:20:5: F841 Local variable `temp` is assigned to but never used
Found 3 errors.
[*] 2 fixable with the `--fix` option.
```

**CHECKPOINT**: Você sabe interpretar a saída do Ruff.

---

## Passo 6: Configuração Avançada do Ruff

**Intenção**: Personalizar regras para o projeto.

Revise a configuração em `pyproject.toml`:

```toml
[tool.ruff]
# Versão do Python alvo
target-version = "py312"

# Tamanho máximo de linha (88 é padrão do Black)
line-length = 88

# Diretórios a verificar
src = ["src", "tests"]

# Arquivos/pastas a ignorar
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
]

[tool.ruff.lint]
# Regras habilitadas
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "SIM",    # flake8-simplify
    "N",      # pep8-naming (NOVO!)
]

# Regras ignoradas
ignore = [
    "E501",   # line too long (formatador cuida)
]

[tool.ruff.lint.pep8-naming]
# Permitir nomes específicos
classmethod-decorators = ["classmethod", "pydantic.validator"]

[tool.ruff.lint.isort]
# Imports do projeto
known-first-party = ["src"]
# Forçar imports em linhas separadas
force-single-line = false
# Seções
section-order = ["future", "standard-library", "third-party", "first-party", "local-folder"]

[tool.ruff.format]
# Estilo de aspas
quote-style = "double"
# Indentação
indent-style = "space"
```

### O que essa configuração significa (visão teórica)

Em termos de **governança de estilo**, essa configuração decide:

- **O que é considerado erro** (ex.: `N` para naming, `I` para imports)
- **O que o time aceita ignorar** (ex.: `E501` porque o formatador decide)
- **Como o projeto “parece” visualmente** (aspas, indentação, line length)

O mais importante nesta parte é **entender** que o estilo fica **documentado no repositório**, e não na cabeça de cada dev.

**CHECKPOINT**: Você entende que o `pyproject.toml` é o contrato de estilo do time.

---

## Passo 7: PEP 8 como Contrato de Time

**Intenção**: Fixar a teoria de por que estilo é governança, não estética.

### O que muda quando o time adota PEP 8

- **Code review** foca em lógica, não em formatação
- **Onboarding** fica mais rápido (código previsível)
- **Menos bugs** passam escondidos por “ruído visual”

### Onde o estilo vive

- **No repositório** (`pyproject.toml`)
- **No CI** (lint automático)
- **No editor** (formatação automática)

Nesta parte o foco é entender o **porquê**. A execução prática completa (rodar Ruff, corrigir erros, fazer commit) será feita na Parte 03.

**CHECKPOINT**: Você consegue explicar por que estilo é uma decisão de time.

# 7. Testes rápidos e validação

Nesta parte, a validação é **conceitual**: você já sabe quais comandos usar para garantir estilo e testes. A execução prática completa entra na Parte 03.

**CHECKPOINT**: Você sabe que a validação envolve lint, format e testes antes de commit.

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas de Estilo de Código

1. **Automatize a formatação**
   - Configure Ruff/Black para rodar no save (IDE)
   - Nunca discuta formatação em code reviews
   - **Trade-off**: Configuração inicial, mas zero esforço depois

2. **Documente exceções**
   - Se ignorar uma regra, explique por quê
   - Use `# noqa: EXXXX` com comentário
   - **Trade-off**: Mais verboso, mas decisões explícitas

3. **Consistência > Perfeição**
   - Melhor todo código igual que metade "perfeito"
   - Siga o estilo existente no projeto
   - **Trade-off**: Pode não ser seu preferido, mas é do time

4. **Configure no projeto, não na máquina**
   - pyproject.toml é versionado
   - Todos usam as mesmas regras
   - **Trade-off**: Menos flexibilidade pessoal

5. **Pre-commit hooks**
   - Ruff roda antes de cada commit
   - Impossível commitar código fora do padrão
   - **Trade-off**: Mais lento, mas garante qualidade

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `E501: Line too long` | Linha > 88 chars | Ruff format ou quebrar manualmente |
| `I001: Import block unsorted` | Imports fora de ordem | `ruff check --fix` |
| `F401: imported but unused` | Import não usado | Remover ou usar |
| `N802: function name should be lowercase` | Função em CamelCase | Renomear para snake_case |
| `W291: trailing whitespace` | Espaço no final da linha | Ruff format |
| Conflito entre regras | Configuração inconsistente | Revisar pyproject.toml |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Identificar Violações

Dado o código abaixo, identifique todas as violações de PEP 8:

```python
import pandas as pd
import os
from src.validation import validate_limit_bal
import sys

def CalculateScore(Limit,Age):
    x=Limit*0.01
    y = Age * 0.5
    return x+y

class credit_application:
    def __init__(self,ID):
        self.ID=ID
```

**Critério de sucesso**: Lista com pelo menos 8 violações identificadas.

## Exercício Básico 2: Corrigir Código

Reescreva o código do exercício anterior seguindo PEP 8 completamente.

**Critério de sucesso**: `ruff check` não retorna erros.

## Exercício Avançado: Configurar Pre-commit

Configure o `pre-commit` para rodar Ruff automaticamente antes de cada commit. Crie `.pre-commit-config.yaml` e teste.

**Critério de sucesso**: Tentar commitar código com erro de estilo falha automaticamente.

# 11. Resultados e Lições

## Métricas para Acompanhar

| Métrica | Como medir | Valor esperado |
|---------|------------|----------------|
| Erros de lint | `ruff check \| wc -l` | 0 |
| Arquivos formatados | `ruff format --check` | Todos passam |
| Tempo de format | `Measure-Command { ruff format src/ }` | < 1 segundo |
| Cobertura de regras | Contar regras em `select` | >= 8 categorias |

## Lições desta Aula

1. **PEP 8 é padrão** - Não é opcional em projetos profissionais
2. **Automação é essencial** - Ruff formata automaticamente
3. **Nomes importam** - snake_case para funções/variáveis, PascalCase para classes
4. **Imports organizados** - Stdlib, terceiros, locais
5. **Consistência > preferência pessoal** - Siga o padrão do projeto

# 12. Encerramento e gancho para a próxima aula (script)

Nesta aula você aprendeu as principais regras da PEP 8 e como usar o Ruff para garantir que seu código siga o padrão da comunidade Python. Indentação, nomes, imports - tudo isso agora é automático.

Mas seguir PEP 8 é apenas o começo. Código pode estar perfeitamente formatado e ainda assim ser difícil de manter. Na próxima aula, vamos falar sobre **princípios de código limpo**: DRY (Don't Repeat Yourself), KISS (Keep It Simple), e como identificar "code smells" - aqueles padrões que indicam que algo pode melhorar.

Você vai aprender a escrever código que não só é bonito, mas também é fácil de entender e manter. Até a próxima aula!
