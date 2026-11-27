---
titulo: "Aula 03 – Parte 01: Pirâmide e Tipos de Teste - Unitário, Integração e End-to-End"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 20
prerequisitos:
  - "Python 3.12+"
  - "UV instalado"
  - "Git configurado"
  - "Aula 02 concluída (repositório swe4ds-credit-api)"
tags: ["testes", "qualidade", "piramide-testes", "unitario", "integracao", "e2e"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula, vamos falar sobre algo que separa código amador de código profissional: **testes automatizados**. Se você já trabalhou em um projeto de Data Science que funcionava perfeitamente até alguém fazer "uma pequena alteração" e quebrar tudo, você sabe exatamente do que estou falando.

Testes automatizados são a rede de segurança que permite você modificar código com confiança. Eles garantem que, a cada alteração, você saiba imediatamente se algo quebrou. Em projetos de Machine Learning, onde pipelines são complexos e dados mudam constantemente, essa segurança é ainda mais crítica.

Nesta aula, vamos entender a teoria por trás dos testes: o que são, quais tipos existem, e como a famosa "pirâmide de testes" nos guia na construção de uma suíte de testes eficiente. Prepare-se para mudar sua forma de pensar sobre qualidade de código.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você desenvolveu um pipeline de ML que funciona perfeitamente. Três meses depois, precisa adicionar uma nova feature de preprocessamento. Você faz a alteração, roda o script, e... erro. Mas não só na parte nova - algo quebrou na função de normalização que você nem tocou. Como? Por quê?

**Agitação**: Você passa horas debugando. Descobre que a nova função usa uma variável global que afetava a outra. Corrige. Funciona. Faz deploy. Na manhã seguinte, o cliente liga: "Os resultados estão estranhos". Você verifica: outra função que dependia do comportamento antigo agora está errada. É um ciclo infinito de correções que geram novos problemas. Cada mudança é um risco. A equipe tem medo de tocar no código.

**Solução**: Com testes automatizados, cada função crítica tem verificações que rodam em segundos. Antes de fazer qualquer alteração, você roda os testes. Depois da alteração, roda de novo. Se algo quebrou, você descobre imediatamente - não em produção. A suíte de testes se torna seu guardião. Modificar código deixa de ser arriscado e passa a ser rotina segura.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Explicar** por que testes automatizados são essenciais para projetos de Data Science
2. **Descrever** a pirâmide de testes e a proporção ideal entre tipos de teste
3. **Diferenciar** testes unitários, de integração e end-to-end
4. **Identificar** quais partes de um pipeline de ML devem ter cada tipo de teste
5. **Avaliar** o custo-benefício de diferentes estratégias de teste
6. **Planejar** uma estratégia de testes para o projeto de API de crédito

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Git 2.40+ instalado e configurado
- Python 3.12+
- UV instalado
- Repositório `swe4ds-credit-api` da Aula 02

**Verificação do ambiente:**

```bash
# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Ativar ambiente virtual
.venv\Scripts\activate

# Verificar Python
python --version
# Esperado: Python 3.12.x

# Verificar estrutura
ls src/
# Esperado: __init__.py  data_loader.py
```

**Checklist de Setup:**
- [ ] Repositório clonado e atualizado
- [ ] Ambiente virtual ativo
- [ ] Código da Aula 02 presente (src/data_loader.py)

# 5. Visão geral do que já existe no projeto (continuidade)

**Estrutura atual (após Aula 02):**
```
swe4ds-credit-api/
├── .git/
├── .dvc/
├── .dvcignore
├── .gitignore
├── .venv/
├── LICENSE
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   │   ├── .gitignore
│   │   └── credit_sample.csv.dvc
│   └── processed/
├── models/
├── scripts/
│   └── download_data.py
└── src/
    ├── __init__.py
    └── data_loader.py
```

**O que faremos nesta aula (teórico):**
- Entender a teoria de testes
- Planejar estrutura de testes para o projeto
- Preparar para implementação prática nas próximas partes

**O que será criado nas próximas partes:**
```
swe4ds-credit-api/
├── ...
├── tests/                    # [FUTURO] Pasta de testes
│   ├── __init__.py
│   ├── conftest.py          # Fixtures compartilhadas
│   ├── unit/                # Testes unitários
│   │   └── test_data_loader.py
│   └── integration/         # Testes de integração
│       └── test_pipeline.py
├── pyproject.toml           # [FUTURO] Configuração pytest
└── ...
```

# 6. Passo a passo (comandos + código)

## Passo 1: Por que Testes Automatizados? (Excalidraw: Slide 1)

**Intenção**: Entender o valor fundamental de testes antes de aprender a escrevê-los.

### O Custo de Não Ter Testes

Em projetos de Data Science, a ausência de testes leva a:

1. **Regressões silenciosas**: Alterações quebram funcionalidades sem aviso
2. **Medo de refatorar**: Código fica cada vez mais confuso
3. **Debug demorado**: Sem testes, você descobre bugs tarde demais
4. **Falta de documentação**: Testes servem como exemplos de uso

### O Valor dos Testes em ML

Para pipelines de Machine Learning:

| Sem Testes | Com Testes |
|------------|------------|
| "Funciona na minha máquina" | Funciona em qualquer ambiente |
| Alteração → Medo | Alteração → Confiança |
| Bug em produção | Bug detectado localmente |
| Horas de debug | Segundos para identificar |

### Testes como Documentação Viva

Testes bem escritos mostram:
- Como usar cada função
- Quais são os inputs esperados
- O que deve acontecer em cada caso

```python
# Exemplo: este teste documenta o comportamento esperado
def test_preprocess_removes_null_values():
    """Preprocessamento deve remover linhas com valores nulos."""
    df_with_nulls = pd.DataFrame({"a": [1, None, 3]})
    result = preprocess(df_with_nulls)
    assert result["a"].isna().sum() == 0
```

**CHECKPOINT**: Você consegue listar 3 benefícios de testes automatizados?

---

## Passo 2: A Pirâmide de Testes (Excalidraw: Slide 2)

**Intenção**: Entender a proporção ideal entre tipos de teste.

### Visualização da Pirâmide

```
                    ╱╲
                   ╱  ╲
                  ╱ E2E╲         ← Poucos (lentos, caros, frágeis)
                 ╱──────╲
                ╱        ╲
               ╱Integração╲      ← Alguns (moderados)
              ╱────────────╲
             ╱              ╲
            ╱   UNITÁRIOS    ╲   ← Muitos (rápidos, baratos, estáveis)
           ╱__________________╲
```

### Características de Cada Nível

| Tipo | Quantidade | Velocidade | Custo | Estabilidade |
|------|------------|------------|-------|--------------|
| Unitário | Muitos (70-80%) | Milissegundos | Baixo | Alta |
| Integração | Alguns (15-20%) | Segundos | Médio | Média |
| End-to-End | Poucos (5-10%) | Minutos | Alto | Baixa |

### Por que essa Proporção?

1. **Testes unitários são a base** porque:
   - São extremamente rápidos
   - Isolam problemas facilmente
   - São baratos de manter

2. **Testes de integração verificam conexões** porque:
   - Componentes podem funcionar isolados mas falhar juntos
   - APIs e bancos de dados precisam ser testados em conjunto

3. **Testes E2E são o topo** porque:
   - São caros e lentos
   - Tendem a ser "flaky" (falham aleatoriamente)
   - Mas são essenciais para cenários críticos

**CHECKPOINT**: Você sabe explicar por que testes unitários devem ser a maioria?

---

## Passo 3: Testes Unitários em Detalhes (Excalidraw: Slide 3)

**Intenção**: Entender profundamente o tipo mais importante de teste.

### O que é um Teste Unitário?

Um teste unitário verifica uma **única unidade de código** isoladamente:
- Uma função
- Um método
- Uma classe pequena

### Características

- **Isolado**: Não depende de banco de dados, API, arquivo
- **Rápido**: Executa em milissegundos
- **Determinístico**: Sempre produz o mesmo resultado
- **Focado**: Testa uma coisa só

### Exemplo no Contexto de ML

Considere nossa função `preprocess_data` do `data_loader.py`:

```python
# O que testar unitariamente:
# 1. Remoção correta da coluna ID
# 2. Separação correta de features e target
# 3. Normalização aplicada corretamente
# 4. Proporção correta de train/test split

def test_preprocess_removes_id_column():
    """Teste unitário: verifica remoção da coluna ID."""
    df = pd.DataFrame({
        "ID": [1, 2, 3],
        "feature1": [10, 20, 30],
        "default payment next month": [0, 1, 0]
    })
    X_train, X_test, _, _, _ = preprocess_data(df)
    # ID não deve estar nas features
    assert X_train.shape[1] == 1  # Apenas feature1
```

### O que NÃO é Teste Unitário

```python
# ISSO NÃO É TESTE UNITÁRIO - depende de arquivo externo
def test_load_credit_data():
    df = load_credit_data(Path("data/real_file.csv"))  # Arquivo real!
    assert len(df) > 0
```

Para transformar em unitário, usamos mocks (próxima aula).

**CHECKPOINT**: Você sabe identificar se um teste é unitário ou não?

---

## Passo 4: Testes de Integração

**Intenção**: Entender quando e por que testar componentes juntos.

### O que é um Teste de Integração?

Testes de integração verificam se **múltiplos componentes funcionam juntos**:
- Função A chama função B corretamente
- Pipeline completo de preprocessamento
- API conecta com serviço de ML

### Exemplo no Contexto de ML

```python
def test_pipeline_completo_preprocessamento():
    """
    Teste de integração: verifica pipeline completo.
    
    Testa: load_data -> preprocess -> validate
    """
    # Usa dados de teste (não mock)
    df = load_credit_data(test_filepath)
    
    # Processa
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)
    
    # Valida integração
    assert X_train.shape[0] == len(y_train)
    assert X_test.shape[0] == len(y_test)
    assert scaler is not None
```

### Diferença para Unitário

| Aspecto | Unitário | Integração |
|---------|----------|------------|
| Escopo | Uma função | Múltiplas funções |
| Dependências | Mockadas | Reais (ou quase) |
| Velocidade | Muito rápido | Mais lento |
| Isolamento | Total | Parcial |

**CHECKPOINT**: Você sabe quando usar integração em vez de unitário?

---

## Passo 5: Testes End-to-End (E2E)

**Intenção**: Entender o papel dos testes de sistema completo.

### O que é um Teste E2E?

Testes E2E simulam o **usuário real** interagindo com o sistema completo:
- Requisição HTTP real para API
- Banco de dados real
- Modelo carregado realmente

### Exemplo no Contexto da API de Crédito

```python
def test_api_prediction_endpoint():
    """
    Teste E2E: verifica fluxo completo da API.
    
    Simula: Cliente -> API -> Modelo -> Resposta
    """
    # API rodando (não mockada)
    response = requests.post(
        "http://localhost:8000/predict",
        json={
            "LIMIT_BAL": 50000,
            "SEX": 1,
            "EDUCATION": 2,
            # ... todos os campos
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probability" in data
    assert data["prediction"] in [0, 1]
```

### Quando Usar E2E

- Fluxos críticos de negócio
- Cenários que envolvem múltiplos serviços
- Validação final antes de deploy

### Custos do E2E

- **Lento**: Segundos a minutos por teste
- **Frágil**: Depende de muitos componentes
- **Caro**: Requer infraestrutura real

**CHECKPOINT**: Você sabe identificar quando um teste E2E é necessário?

---

## Passo 6: Aplicando a Pirâmide ao Projeto de Crédito

**Intenção**: Planejar estratégia de testes para nosso projeto específico.

### Mapeamento de Testes

```
┌─────────────────────────────────────────────────────────────────┐
│                 ESTRATÉGIA DE TESTES - API CRÉDITO              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  E2E (5-10%):                                                   │
│  ┌─────────────────────────────────────────────────┐           │
│  │ - POST /predict retorna predição válida         │           │
│  │ - GET /health retorna status do modelo          │           │
│  │ - Fluxo completo de autenticação (se houver)    │           │
│  └─────────────────────────────────────────────────┘           │
│                                                                 │
│  Integração (15-20%):                                           │
│  ┌─────────────────────────────────────────────────┐           │
│  │ - Pipeline: load -> preprocess -> predict        │           │
│  │ - Modelo carrega e faz inferência               │           │
│  │ - Scaler e modelo são compatíveis               │           │
│  └─────────────────────────────────────────────────┘           │
│                                                                 │
│  Unitários (70-80%):                                            │
│  ┌─────────────────────────────────────────────────┐           │
│  │ - load_credit_data: trata erros corretamente    │           │
│  │ - preprocess_data: normaliza, split correto     │           │
│  │ - get_feature_names: retorna lista correta      │           │
│  │ - validate_input: rejeita dados inválidos       │           │
│  │ - format_response: estrutura JSON correta       │           │
│  └─────────────────────────────────────────────────┘           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Quais Funções Testar Primeiro?

Priorize por **risco e complexidade**:

1. **Funções de preprocessamento**: Erros aqui afetam todo o pipeline
2. **Funções de validação de input**: Primeira linha de defesa
3. **Funções de formatação de output**: Interface com cliente
4. **Lógica de negócio**: Regras específicas do domínio

### Estrutura de Pastas Planejada

```
tests/
├── __init__.py
├── conftest.py              # Fixtures compartilhadas
├── unit/
│   ├── __init__.py
│   ├── test_data_loader.py  # Testes de src/data_loader.py
│   ├── test_validation.py   # Testes de validação
│   └── test_formatters.py   # Testes de formatação
├── integration/
│   ├── __init__.py
│   ├── test_pipeline.py     # Pipeline completo
│   └── test_model_service.py
└── e2e/
    ├── __init__.py
    └── test_api_endpoints.py
```

**CHECKPOINT**: Você consegue mapear quais testes criar para seu projeto?

---

## Passo 7: Cobertura de Testes

**Intenção**: Entender como medir a qualidade da suíte de testes.

### O que é Cobertura?

**Cobertura de testes** mede qual porcentagem do código é executada pelos testes.

```bash
# Executar testes com cobertura (veremos na prática depois)
pytest --cov=src tests/
```

**Exemplo de relatório:**
```
Name                    Stmts   Miss  Cover
-------------------------------------------
src/__init__.py             0      0   100%
src/data_loader.py         45     12    73%
-------------------------------------------
TOTAL                      45     12    73%
```

### Armadilhas da Cobertura

- **100% não significa sem bugs**: Cobertura mede linhas executadas, não casos testados
- **Cobertura baixa é alerta**: Menos de 60% indica risco
- **Meta razoável**: 70-80% para código de produção

### Cobertura em Data Science

Em ML, algumas partes são difíceis de testar:
- Treinamento de modelo (lento)
- Visualizações (subjetivo)
- Notebooks exploratórios

Foque cobertura em:
- Preprocessamento de dados
- Validação de inputs
- Lógica de negócio
- Formatação de outputs

**CHECKPOINT**: Você entende que cobertura é uma métrica útil mas não suficiente?

# 7. Testes rápidos e validação

Como esta aula é teórica, a validação será conceitual:

**Quiz de Verificação:**

1. Qual tipo de teste deve ser mais numeroso?
   - [ ] E2E
   - [x] Unitário
   - [ ] Integração

2. Testes unitários devem:
   - [x] Ser isolados e rápidos
   - [ ] Testar o sistema completo
   - [ ] Depender de banco de dados

3. Quando usar teste E2E?
   - [ ] Para toda função
   - [x] Para fluxos críticos de negócio
   - [ ] Nunca

**Respostas corretas indicam compreensão do conteúdo.**

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas de Estratégia de Testes

1. **Comece pelos testes unitários**
   - São mais fáceis de escrever
   - Dão feedback rápido
   - Criam base para refatoração
   - **Trade-off**: Investimento inicial de tempo, retorno enorme em manutenção

2. **Teste comportamento, não implementação**
   - Teste O QUE a função faz, não COMO ela faz
   - Permite refatorar sem quebrar testes
   - **Trade-off**: Exige pensar em termos de contrato/interface

3. **Nomeie testes descritivamente**
   - Nome deve explicar o cenário: `test_preprocess_removes_null_rows`
   - Facilita identificar falhas
   - **Trade-off**: Nomes longos, mas auto-documentados

4. **Mantenha testes independentes**
   - Um teste não deve depender de outro
   - Ordem de execução não deve importar
   - **Trade-off**: Pode haver alguma duplicação de setup

# 9. Troubleshooting (erros comuns)

| Problema | Causa | Solução |
|----------|-------|---------|
| "Testes passam localmente, falham no CI" | Dependência de ambiente | Use mocks para isolar |
| "Testes são lentos demais" | Muitos testes E2E | Rebalanceie para mais unitários |
| "Testes falham aleatoriamente" | Testes flaky | Elimine dependências de ordem/tempo |
| "Cobertura alta mas bugs em produção" | Testes superficiais | Teste casos de borda |
| "Difícil testar função X" | Função faz muitas coisas | Refatore para SRP |
| "Não sei o que testar" | Falta de planejamento | Mapeie riscos primeiro |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Identificar Tipo de Teste

Para cada descrição, identifique se é unitário, integração ou E2E:

1. "Testa se a função `normalize()` retorna valores entre 0 e 1"
2. "Testa se POST /predict retorna JSON com prediction e probability"
3. "Testa se o pipeline load -> preprocess -> predict funciona junto"

**Critério de sucesso**: Identificar corretamente os 3 tipos.

## Exercício Básico 2: Planejar Testes

Liste 5 testes unitários que você criaria para `src/data_loader.py`:

1. `test_...`
2. `test_...`
3. `test_...`
4. `test_...`
5. `test_...`

**Critério de sucesso**: Nomes descritivos que indicam comportamento testado.

## Exercício Avançado: Estratégia Completa

Crie um documento de estratégia de testes para a API de crédito:

1. Liste 10 testes unitários prioritários
2. Liste 5 testes de integração
3. Liste 2 testes E2E críticos
4. Estime cobertura alvo por módulo

**Critério de sucesso**: Documento coerente com a pirâmide de testes.

# 11. Resultados e Lições

## Como Medir Sucesso

| Métrica | Como Medir | Valor Referência |
|---------|------------|------------------|
| Compreensão da pirâmide | Quiz de verificação | 3/3 corretas |
| Planejamento | Lista de testes | 10+ testes planejados |
| Proporção | Contagem por tipo | ~70% unitários |

## Lições Aprendidas

1. **Testes são investimento, não custo** - economizam tempo de debug
2. **A pirâmide guia proporções** - muitos unitários, poucos E2E
3. **Isolamento é chave** - testes unitários não dependem de externos
4. **Cobertura é métrica útil mas não suficiente** - qualidade > quantidade
5. **Comece pequeno** - alguns testes bons > muitos testes ruins

# 12. Encerramento e gancho para a próxima aula (script)

Excelente! Agora você tem uma base sólida sobre a teoria de testes. Você entende a pirâmide, sabe diferenciar os tipos de teste, e consegue planejar uma estratégia para seu projeto.

Mas teoria sem prática não leva a lugar nenhum. Na próxima aula, vamos conhecer o **Pytest** - o framework de testes mais usado em Python. Vamos aprender a estrutura de um teste, como usar fixtures para setup, e o conceito de mocks para isolar dependências.

Também vamos introduzir o **TDD - Test-Driven Development**, uma técnica onde você escreve o teste ANTES do código. Parece contraintuitivo, mas é surpreendentemente poderoso para guiar o design de soluções mais simples.

Prepare-se para colocar a mão na massa!

Até a próxima aula!
