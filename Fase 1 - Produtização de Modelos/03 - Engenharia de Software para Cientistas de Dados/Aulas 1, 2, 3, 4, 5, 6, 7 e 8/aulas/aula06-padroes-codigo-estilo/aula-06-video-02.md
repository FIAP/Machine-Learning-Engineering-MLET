---
titulo: "Aula 06 – Parte 02: Princípios de Código Limpo - DRY, KISS e Evitando Code Smells"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 25
prerequisitos:
  - "Python 3.12+"
  - "Aula 06 - Parte 01 concluída"
  - "Conhecimento básico de funções e classes"
tags: ["clean-code", "dry", "kiss", "code-smells", "refactoring"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos além da formatação e entrar no território do **código limpo** - Clean Code.

Na aula anterior, você aprendeu a deixar seu código visualmente consistente com PEP 8. Mas código pode estar perfeitamente formatado e ainda assim ser um pesadelo de manter. Funções com 200 linhas, lógica duplicada em 5 lugares, variáveis chamadas `x`, `temp` e `data2`. Isso é código que funciona, mas ninguém quer tocar.

Hoje vamos aprender princípios fundamentais que vão transformar a qualidade do seu código: **DRY** (Don't Repeat Yourself), **KISS** (Keep It Simple, Stupid), e **Single Responsibility**. Também vamos aprender a identificar **code smells** - aqueles padrões que indicam que algo está errado.

Esses princípios vão ser aplicados no nosso projeto de crédito para garantir que o código seja não apenas funcional, mas também fácil de entender e evoluir.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você herda um projeto de ML de alguém que saiu da empresa. O código funciona... às vezes. Tem uma função `process_data()` com 300 linhas. A mesma lógica de validação aparece em 4 arquivos diferentes. Variáveis chamadas `df`, `df2`, `df_final`, `df_final_v2`.

**Agitação**: Você precisa adicionar uma nova feature. Mas onde? A função de 300 linhas faz tudo: carrega dados, limpa, transforma, treina modelo, salva resultados. Você muda a validação em um lugar, esquece dos outros 3. Bug em produção. O gerente pergunta quanto tempo para corrigir. Você não sabe, porque não entende o código. Cada mudança quebra algo inesperado.

**Solução**: Refatorar aplicando princípios de código limpo. Dividir a função gigante em funções menores com responsabilidade única. Extrair a lógica duplicada para um único lugar. Renomear variáveis para serem descritivas. O código fica menor, mais claro, e mudanças se tornam previsíveis.

No nosso projeto de crédito, vamos aplicar esses princípios desde o início para evitar que o código vire um monstro.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Aplicar** o princípio DRY para eliminar duplicação
2. **Aplicar** o princípio KISS para simplificar soluções
3. **Explicar** o princípio de Single Responsibility
4. **Identificar** code smells comuns em projetos de DS
5. **Refatorar** código para melhorar legibilidade
6. **Justificar** decisões de design baseadas em princípios

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Ambiente do projeto configurado
- Código passando em `ruff check`

**Verificar ambiente:**

```bash
# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Ativar ambiente
.\.venv\Scripts\Activate.ps1

# Verificar que código está limpo
ruff check src/ tests/
```

**Checklist:**
- [ ] Ambiente virtual ativado
- [ ] Código sem erros de lint
- [ ] Testes passando

# 5. Visão geral do que já existe no projeto (continuidade)

**Estado atual:**
```
swe4ds-credit-api/
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Vamos analisar
│   └── validation.py           # Vamos analisar
├── tests/
│   └── test_validation.py
└── ...
```

**O que vamos fazer nesta aula:**
- Analisar código existente buscando code smells
- Aplicar princípios DRY, KISS, SRP
- Melhorar legibilidade sem mudar comportamento

# 6. Passo a passo (comandos + código)

## Passo 1: Princípio DRY - Don't Repeat Yourself (Excalidraw: Slide 2)

**Intenção**: Entender e aplicar o princípio mais importante de código limpo.

### O que é DRY?

> "Every piece of knowledge must have a single, unambiguous, authoritative representation within a system."
> — The Pragmatic Programmer

Em outras palavras: **não duplique lógica**.

### Exemplo de Violação

```python
# RUIM: Lógica duplicada
def process_client_a(data):
    # Validação duplicada!
    if data["age"] < 18 or data["age"] > 120:
        raise ValueError("Idade inválida")
    if data["limit"] <= 0:
        raise ValueError("Limite inválido")
    # ... processamento específico de A
    return result_a

def process_client_b(data):
    # Mesma validação duplicada!
    if data["age"] < 18 or data["age"] > 120:
        raise ValueError("Idade inválida")
    if data["limit"] <= 0:
        raise ValueError("Limite inválido")
    # ... processamento específico de B
    return result_b
```

### Aplicando DRY

```python
# BOM: Lógica extraída para função reutilizável
def validate_client_data(data: dict) -> None:
    """Valida dados comuns de cliente."""
    if data["age"] < 18 or data["age"] > 120:
        raise ValueError("Idade inválida")
    if data["limit"] <= 0:
        raise ValueError("Limite inválido")


def process_client_a(data: dict) -> dict:
    validate_client_data(data)  # Reutiliza!
    # ... processamento específico de A
    return result_a


def process_client_b(data: dict) -> dict:
    validate_client_data(data)  # Reutiliza!
    # ... processamento específico de B
    return result_b
```

### Benefícios

| Antes (duplicado) | Depois (DRY) |
|-------------------|--------------|
| Bug precisa ser corrigido em N lugares | Corrige em 1 lugar |
| Inconsistência fácil | Comportamento garantido |
| Mais código para manter | Menos código |
| Difícil de testar tudo | Testa uma vez |

**CHECKPOINT**: Você entende que duplicação é o inimigo #1 da manutenção.

---

## Passo 2: Princípio KISS - Keep It Simple, Stupid (Excalidraw: Slide 2)

**Intenção**: Preferir soluções simples sobre complexas.

### O que é KISS?

> "Simplicity is the ultimate sophistication."
> — Leonardo da Vinci

A solução mais simples que funciona é geralmente a melhor.

### Exemplo de Over-Engineering

```python
# RUIM: Complexidade desnecessária
class ValidationStrategyFactory:
    _strategies = {}
    
    @classmethod
    def register(cls, name):
        def decorator(strategy_class):
            cls._strategies[name] = strategy_class
            return strategy_class
        return decorator
    
    @classmethod
    def create(cls, name):
        return cls._strategies[name]()

@ValidationStrategyFactory.register("age")
class AgeValidationStrategy:
    def validate(self, value):
        return 18 <= value <= 120

# Para validar idade:
factory = ValidationStrategyFactory()
strategy = factory.create("age")
is_valid = strategy.validate(25)
```

### Aplicando KISS

```python
# BOM: Simples e direto
def validate_age(age: int) -> bool:
    """Valida se idade está no range permitido."""
    return 18 <= age <= 120

# Para validar idade:
is_valid = validate_age(25)
```

### Quando Complexidade é Justificada?

| Simples | Complexo (justificado) |
|---------|------------------------|
| 1-3 tipos de validação | 20+ tipos dinâmicos |
| Requisitos estáveis | Requisitos mudam frequentemente |
| Time pequeno | Time grande com especialização |
| Projeto único | Biblioteca reutilizável |

### Regra de Ouro

> "Make it work, make it right, make it fast."
> — Kent Beck

1. Primeiro: funciona
2. Depois: limpo e correto
3. Por último: otimizado (se necessário)

**CHECKPOINT**: Você entende que simplicidade é uma virtude, não uma limitação.

---

## Passo 3: Single Responsibility Principle (Excalidraw: Slide 2)

**Intenção**: Cada módulo/função deve ter uma única responsabilidade.

### O que é SRP?

> "A module should have one, and only one, reason to change."
> — Robert C. Martin

Se uma função faz 5 coisas, ela tem 5 motivos para mudar.

### Exemplo de Violação

```python
# RUIM: Função faz tudo
def process_credit_application(filepath: str) -> dict:
    # Responsabilidade 1: Ler arquivo
    with open(filepath) as f:
        data = json.load(f)
    
    # Responsabilidade 2: Validar
    if data["age"] < 18:
        raise ValueError("Menor de idade")
    
    # Responsabilidade 3: Calcular score
    score = data["limit"] * 0.01 + data["age"] * 0.5
    
    # Responsabilidade 4: Decidir aprovação
    approved = score > 50
    
    # Responsabilidade 5: Salvar resultado
    with open("result.json", "w") as f:
        json.dump({"approved": approved}, f)
    
    # Responsabilidade 6: Enviar notificação
    send_email(data["email"], f"Resultado: {approved}")
    
    return {"approved": approved, "score": score}
```

### Aplicando SRP

```python
# BOM: Cada função tem uma responsabilidade

def load_application(filepath: str) -> dict:
    """Carrega aplicação de arquivo."""
    with open(filepath) as f:
        return json.load(f)


def validate_application(data: dict) -> None:
    """Valida dados da aplicação."""
    if data["age"] < 18:
        raise ValueError("Menor de idade")


def calculate_credit_score(data: dict) -> float:
    """Calcula score de crédito."""
    return data["limit"] * 0.01 + data["age"] * 0.5


def decide_approval(score: float, threshold: float = 50) -> bool:
    """Decide se aplicação é aprovada."""
    return score > threshold


def save_result(result: dict, filepath: str) -> None:
    """Salva resultado em arquivo."""
    with open(filepath, "w") as f:
        json.dump(result, f)


def process_credit_application(filepath: str) -> dict:
    """Orquestra o processamento de aplicação de crédito."""
    data = load_application(filepath)
    validate_application(data)
    score = calculate_credit_score(data)
    approved = decide_approval(score)
    result = {"approved": approved, "score": score}
    save_result(result, "result.json")
    return result
```

### Benefícios do SRP

| Aspecto | Função Monolítica | Funções Separadas |
|---------|-------------------|-------------------|
| Testabilidade | Difícil | Fácil |
| Reutilização | Impossível | Natural |
| Manutenção | Arriscada | Localizada |
| Entendimento | Complexo | Óbvio |

**CHECKPOINT**: Você entende que funções devem fazer uma coisa bem feita.

---

## Passo 4: Identificando Code Smells (Excalidraw: Slide 2)

**Intenção**: Reconhecer padrões que indicam problemas.

### O que são Code Smells?

"Cheiros" no código que indicam problemas de design. Não são bugs, mas sintomas de que algo pode melhorar.

### Code Smells Comuns em Data Science

| Smell | Sintoma | Solução |
|-------|---------|---------|
| **Função Longa** | > 20 linhas | Extrair subfunções |
| **Código Duplicado** | Copy-paste | Extrair função comum |
| **Nomes Obscuros** | `df2`, `temp`, `x` | Renomear descritivamente |
| **Magic Numbers** | `if x > 0.85:` | Extrair constante |
| **Comentários Excessivos** | Código precisa explicação | Refatorar para ser óbvio |
| **God Class/Function** | Faz tudo | Dividir responsabilidades |
| **Dead Code** | Código nunca executado | Remover |
| **Feature Envy** | Usa mais dados de outro módulo | Mover para lá |

### Exemplos Práticos

```python
# SMELL: Magic Numbers
if score > 0.85:  # O que é 0.85?
    return "approved"

# MELHOR: Constante nomeada
APPROVAL_THRESHOLD = 0.85
if score > APPROVAL_THRESHOLD:
    return "approved"
```

```python
# SMELL: Nomes obscuros
def proc(df, n, t):
    df2 = df[df["x"] > t]
    return df2.head(n)

# MELHOR: Nomes descritivos
def filter_high_value_clients(
    clients: pd.DataFrame,
    limit: int,
    min_credit_score: float,
) -> pd.DataFrame:
    high_value = clients[clients["credit_score"] > min_credit_score]
    return high_value.head(limit)
```

```python
# SMELL: Comentário explicando código ruim
# Verifica se o cliente é elegível baseado na idade,
# limite de crédito e score, retornando True se todos
# os critérios forem atendidos
def check(a, l, s):
    return a >= 18 and l > 0 and s > 0.5

# MELHOR: Código auto-explicativo
def is_client_eligible(age: int, credit_limit: float, score: float) -> bool:
    is_adult = age >= 18
    has_valid_limit = credit_limit > 0
    has_minimum_score = score > 0.5
    return is_adult and has_valid_limit and has_minimum_score
```

**CHECKPOINT**: Você sabe identificar code smells comuns.

---

## Passo 5: Refatoração Contínua (Excalidraw: Slide 2)

**Intenção**: Melhorar código gradualmente, mantendo funcionamento.

### O que é Refatoração?

> "Refactoring is the process of changing a software system in such a way that it does not alter the external behavior of the code yet improves its internal structure."
> — Martin Fowler

Mudar a estrutura **sem mudar o comportamento**.

### Regras de Ouro da Refatoração

1. **Testes primeiro**: Tenha testes passando antes de refatorar
2. **Passos pequenos**: Uma mudança por vez
3. **Commit frequente**: Cada melhoria é um commit
4. **Não adicione features**: Refatoração ≠ nova funcionalidade

### Fluxo de Refatoração

```
1. Identifica smell    → Função longa
2. Escreve teste       → Garante comportamento atual
3. Refatora            → Extrai subfunção
4. Roda teste          → Verifica que não quebrou
5. Commit              → "refactor: extract validation"
6. Repete              → Próximo smell
```

### Exemplo de Refatoração Incremental

```python
# ANTES: Função com múltiplas responsabilidades
def analyze_client(data):
    # Validação
    if data["age"] < 18:
        return {"error": "underage"}
    if data["limit"] <= 0:
        return {"error": "invalid_limit"}
    
    # Cálculo
    score = data["limit"] * 0.01 + data["age"] * 0.5
    
    # Decisão
    if score > 50:
        return {"status": "approved", "score": score}
    return {"status": "rejected", "score": score}
```

```python
# DEPOIS: Refatorado incrementalmente

# Passo 1: Extrair validação
def validate_client_data(data: dict) -> str | None:
    """Retorna erro ou None se válido."""
    if data["age"] < 18:
        return "underage"
    if data["limit"] <= 0:
        return "invalid_limit"
    return None

# Passo 2: Extrair cálculo de score
def calculate_score(data: dict) -> float:
    """Calcula score de crédito."""
    return data["limit"] * 0.01 + data["age"] * 0.5

# Passo 3: Extrair decisão
APPROVAL_THRESHOLD = 50

def decide_status(score: float) -> str:
    """Determina status baseado no score."""
    return "approved" if score > APPROVAL_THRESHOLD else "rejected"

# Função principal agora é simples
def analyze_client(data: dict) -> dict:
    """Analisa cliente e retorna resultado."""
    error = validate_client_data(data)
    if error:
        return {"error": error}
    
    score = calculate_score(data)
    status = decide_status(score)
    return {"status": status, "score": score}
```

**CHECKPOINT**: Você entende o processo de refatoração incremental.

---

## Passo 6: Diagnóstico Teórico no Projeto de Crédito

**Intenção**: Saber **o que procurar** antes de refatorar.

Nesta parte, o foco é **mapear smells e princípios violados** sem ainda modificar o código. Você deve conseguir responder:

- Onde há **duplicação**? (DRY)
- Onde há **complexidade desnecessária**? (KISS)
- Que funções **fazem mais de uma coisa**? (SRP)
- Onde há **nomes obscuros** e **magic numbers**?

### Checklist de diagnóstico

- [ ] Funções muito longas (> 20 linhas)
- [ ] Código duplicado em mais de um arquivo
- [ ] Nomes pouco descritivos
- [ ] Magic numbers sem constantes
- [ ] Responsabilidades misturadas

**Nota:** A execução prática (alterar arquivos, rodar testes, commitar) será feita nas Partes 03 e 04.

**CHECKPOINT**: Você consegue apontar 3–5 melhorias sem abrir um editor.

# 7. Testes rápidos e validação

Nesta parte, a validação é **conceitual**: você deve saber que toda refatoração precisa de testes e lint antes de ir para o Git.

**CHECKPOINT**: Você consegue explicar por que testes são o “cinto de segurança” da refatoração.

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas de Código Limpo

1. **Refatore continuamente**
   - Não acumule débito técnico
   - "Leave the code cleaner than you found it"
   - **Trade-off**: Tempo extra agora, economia depois

2. **Nomes são documentação**
   - `calculate_credit_score()` > `calc()` > `c()`
   - Gaste tempo escolhendo bons nomes
   - **Trade-off**: Nomes longos, mas código auto-documentado

3. **Funções pequenas**
   - Ideal: 5-15 linhas
   - Máximo: 20-25 linhas
   - **Trade-off**: Mais funções, mas mais fáceis de entender

4. **Testes habilitam refatoração**
   - Sem testes, refatorar é arriscado
   - Com testes, é seguro
   - **Trade-off**: Esforço em testes, mas liberdade para melhorar

5. **Código óbvio > comentários**
   - Se precisa explicar, talvez deva refatorar
   - Comentários ficam desatualizados
   - **Trade-off**: Mais esforço no código, menos manutenção de docs

# 9. Troubleshooting (erros comuns)

| Problema | Causa | Solução |
|----------|-------|---------|
| Refatoração quebrou funcionalidade | Sem testes | Escrever testes primeiro |
| Não sei por onde começar | Código muito bagunçado | Comece pelo smell mais óbvio |
| Refatoração nunca termina | Perfeccionismo | Defina escopo antes |
| Time não aceita refatoração | "Funciona, não mexa" | Mostre benefícios concretos |
| Over-refatoração | KISS violado | Simplicidade é o objetivo |
| Medo de mudar | Código frágil | Adicione testes de caracterização |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Identificar Smells

No código abaixo, identifique pelo menos 5 code smells:

```python
def p(d):
    # processa dados
    r = []
    for i in d:
        if i["v"] > 100:
            x = i["v"] * 0.1
            if i["t"] == 1:
                x = x * 1.5
            elif i["t"] == 2:
                x = x * 1.2
            r.append({"id": i["id"], "result": x})
    return r
```

**Critério de sucesso**: Lista com 5+ smells identificados.

## Exercício Básico 2: Refatorar Código

Refatore o código do exercício anterior aplicando DRY, KISS e nomes descritivos.

**Critério de sucesso**: Código limpo, legível, sem duplicação.

## Exercício Avançado: Refatorar Módulo Real

Analise o `data_loader.py` do projeto. Identifique oportunidades de melhoria e refatore mantendo os testes passando. Documente as mudanças.

**Critério de sucesso**: Pull request com descrição das melhorias e testes passando.

# 11. Resultados e Lições

## Métricas para Acompanhar

| Métrica | Como medir | Direção desejada |
|---------|------------|-----------------|
| Linhas por função | Contar manualmente ou tool | Menor é melhor |
| Complexidade ciclomática | `radon cc src/` | Menor é melhor |
| Duplicação | Análise manual | Zero |
| Cobertura de testes | `task test-cov` | Maior é melhor |

## Lições desta Aula

1. **DRY elimina duplicação** - Uma fonte de verdade
2. **KISS prefere simplicidade** - Não over-engineer
3. **SRP divide responsabilidades** - Uma função, um propósito
4. **Code smells são sintomas** - Aprenda a reconhecê-los
5. **Refatoração é contínua** - Melhore sempre, em passos pequenos

# 12. Encerramento e gancho para a próxima aula (script)

Nesta aula você aprendeu os princípios fundamentais de código limpo: DRY para eliminar duplicação, KISS para manter simplicidade, e Single Responsibility para organizar responsabilidades. Você também aprendeu a identificar code smells e refatorar de forma segura.

Esses princípios são a base. Na próxima aula, vamos um nível acima e falar sobre **padrões de design** - soluções reutilizáveis para problemas recorrentes. Você vai aprender o **Strategy Pattern** para alternar entre diferentes modelos de ML, e ver outros padrões úteis em projetos de Data Science.

Se os princípios são como gramática, os padrões são como técnicas de escrita que você pode aplicar em diferentes situações. Até a próxima aula!
