---
titulo: "Aula 01 – Parte 01: Fundamentos de Engenharia de Software"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 30
prerequisitos:
  - "Python 3.12+"
  - "Conhecimento básico de programação"
  - "Familiaridade com conceitos de Data Science"
tags: ["engenharia-de-software", "fundamentos", "ciclo-de-vida", "metodologias", "data-science"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula, vamos começar uma jornada que vai transformar a forma como vocês desenvolvem seus projetos de Data Science. Vocês já se perguntaram por que alguns projetos de análise de dados funcionam perfeitamente no seu notebook, mas quando tentam colocar em produção ou compartilhar com o time, tudo desmorona? Por que aquele código que funcionava há três meses atrás agora não roda mais e você não sabe o motivo?

A resposta está na falta de fundamentos sólidos de engenharia de software. E é exatamente isso que vamos aprender a partir de agora. Não se trata apenas de escrever código que funciona hoje, mas de construir soluções que sejam mantíveis, escaláveis e profissionais. Vamos entender os conceitos fundamentais de engenharia de software e como aplicá-los no contexto de ciência de dados, começando pelo básico: a diferença entre programação ad hoc e desenvolvimento estruturado.

Ao longo deste módulo, vamos construir juntos uma API REST completa em Python usando FastAPI, que consumirá um modelo de Machine Learning. Mas não vamos apenas fazer funcionar - vamos fazer da forma certa, aplicando as melhores práticas da indústria.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Imagine a seguinte situação: você é um cientista de dados que acabou de desenvolver um modelo incrível que alcança 95% de acurácia. Você demonstra no Jupyter Notebook, todo mundo fica impressionado. Mas quando chega a hora de colocar em produção, o pesadelo começa. O código não roda em outra máquina, as dependências entram em conflito, ninguém mais consegue entender o que você fez, e o pior: você mesmo esquece como funciona depois de algumas semanas.

**Agitação**: Esse problema não é isolado. Ele gera retrabalho constante, frustra equipes inteiras, atrasa projetos críticos e, pior ainda, pode resultar em modelos que nunca saem do papel. Empresas perdem milhões porque bons modelos ficam presos em notebooks. A falta de estrutura e metodologia transforma o desenvolvimento em um caos imprevisível, onde cada mudança pode quebrar algo inesperadamente. Projetos de Data Science sem engenharia adequada têm uma taxa de falha alarmante: estudos mostram que cerca de 85% dos projetos de ML nunca chegam à produção.

**Solução**: A boa notícia é que existe uma disciplina madura e testada que resolve exatamente esses problemas: a Engenharia de Software. Ao aplicar seus princípios, metodologias e boas práticas no contexto de Data Science, conseguimos criar soluções robustas, reprodutíveis e mantíveis. Nesta aula, vamos entender os fundamentos dessa disciplina e começar a aplicá-los desde o primeiro momento. Ao final do módulo, você terá construído uma API REST profissional que serve seu modelo de ML, seguindo as melhores práticas da indústria.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Distinguir** programação ad hoc de desenvolvimento estruturado e identificar os problemas causados pela falta de metodologia
2. **Compreender** as fases do ciclo de vida do software (concepção, desenvolvimento, manutenção) e como aplicá-las em projetos de Data Science
3. **Comparar** metodologias ágeis e waterfall, identificando quando cada uma é mais apropriada
4. **Reconhecer** a importância da disciplina no desenvolvimento de projetos de ciência de dados
5. **Aplicar** conceitos fundamentais de engenharia de software no planejamento de um projeto de DS
6. **Avaliar** o impacto de boas práticas no sucesso de projetos de Machine Learning em produção

# 4. Pré-requisitos e Setup do Ambiente

Para acompanhar esta aula e o módulo completo, você precisará:

**Requisitos de Software:**
- Python 3.12 ou superior
- UV (gerenciador de pacotes moderno para Python)
- Git 2.40+
- Editor de código (recomendado: VS Code)
- Terminal/linha de comando

**Conhecimentos Prévios:**
- Programação básica em Python
- Conceitos fundamentais de Machine Learning
- Familiaridade com Jupyter Notebooks
- Conhecimento básico de linha de comando

**Instalação do UV:**

UV é um gerenciador de pacotes extremamente rápido para Python, escrito em Rust. Ele substitui pip, pip-tools e virtualenv com uma única ferramenta muito mais performática. Usaremos UV em todo o módulo.

```bash
# Instalar UV
# Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/Mac:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verificar instalação
uv --version
```

**Setup Inicial do Ambiente:**

```bash
# Verificar versão do Python
python --version
# Deve retornar: Python 3.12.x ou superior

# Criar pasta para o projeto do módulo
mkdir swe4ds-api-project
cd swe4ds-api-project

# Criar ambiente virtual com UV (muito mais rápido que venv tradicional)
uv venv

# Ativar ambiente virtual
# No Windows:
.venv\Scripts\activate
# No Linux/Mac:
source .venv/bin/activate

# Verificar que o ambiente virtual está ativo
# O prompt deve mostrar (.venv) no início
```

**Por que UV em vez de pip?**
- 10-100x mais rápido na instalação de pacotes
- Resolução de dependências mais inteligente
- Substitui pip, pip-tools e virtualenv
- Compatível com requirements.txt e pyproject.toml
- Ferramenta moderna adotada pela indústria

**Checklist de Setup:**
- [ ] Python 3.12+ instalado e funcionando
- [ ] UV instalado (`uv --version` funciona)
- [ ] Ambiente virtual criado com UV (`.venv/`)
- [ ] Prompt mostrando `(.venv)` indicando ambiente ativo
- [ ] Pasta do projeto criada (`swe4ds-api-project`)

# 5. Visão geral do que já existe no projeto (continuidade)

Nesta primeira parte do módulo, estamos começando do zero. Vamos estabelecer os fundamentos conceituais antes de começar a escrever código. No momento, nosso projeto tem apenas a estrutura básica:

```
swe4ds-api-project/
├── .venv/                # Ambiente virtual Python (criado com UV, não versionar)
└── (vazio por enquanto)
```

Ao longo das próximas aulas, essa estrutura vai evoluir gradualmente. Na próxima aula (Git e Controle de Versão), vamos:
- Inicializar um repositório Git
- Criar estrutura de pastas do projeto
- Começar a desenvolver os primeiros módulos da API

Por enquanto, o foco é **conceitual**: entender os princípios que guiarão todas as nossas decisões técnicas daqui para frente.

# 6. Passo a passo (comandos + código)

## Passo 1: Compreendendo Programação Ad Hoc vs. Estruturada

**Intenção**: Entender a diferença fundamental entre escrever código "que funciona" e código "bem engenheirado".

**Programação Ad Hoc** é aquela onde escrevemos código sem planejamento, estrutura ou metodologia definida. Características:
- Código linear, monolítico (tudo em um único arquivo)
- Sem separação de responsabilidades
- Falta de documentação
- Dependências não gerenciadas
- Difícil de testar e manter

**Exemplo de código Ad Hoc:**

```python
# script_analise.py - Exemplo do que NÃO fazer
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle

# Carrega dados
df = pd.read_csv('/home/usuario/dados/data.csv')

# Limpa dados
df = df.dropna()
df['idade'] = df['idade'].fillna(df['idade'].mean())
df = df[df['idade'] > 0]

# Treina modelo
X = df[['feature1', 'feature2', 'feature3']]
y = df['target']
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Salva modelo
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print('Modelo treinado!')
```

**Problemas deste código:**
- Caminhos absolutos e fixos
- Sem tratamento de erros
- Lógica de negócio misturada com I/O
- Impossível testar componentes isoladamente
- Sem configuração externa
- Sem logging ou monitoramento

**Desenvolvimento Estruturado** segue princípios e metodologias:
- Separação de responsabilidades (modularidade)
- Código organizado em módulos/pacotes
- Configuração externa
- Tratamento de erros robusto
- Documentação adequada
- Testabilidade

**CHECKPOINT**: Você consegue identificar pelo menos 3 problemas no código ad hoc acima? Se sim, você entendeu o conceito!

## Passo 2: Entendendo o Ciclo de Vida do Software

**Intenção**: Compreender que software passa por fases bem definidas, e projetos de DS também devem seguir esse ciclo.

O **ciclo de vida do software** tradicional inclui:

1. **Concepção/Planejamento**
   - Definição de requisitos
   - Análise de viabilidade
   - Arquitetura inicial
   
2. **Desenvolvimento**
   - Design detalhado
   - Implementação
   - Testes
   
3. **Implantação/Deploy**
   - Configuração de ambiente
   - Migração de dados
   - Go-live
   
4. **Manutenção**
   - Correção de bugs
   - Adição de features
   - Otimizações

**Aplicação em Data Science:**

Para projetos de DS/ML, o ciclo se adapta:

```
1. CONCEPÇÃO
   ├── Definir problema de negócio
   ├── Explorar dados disponíveis
   ├── Definir métricas de sucesso
   └── Escolher abordagem (modelo, arquitetura)

2. DESENVOLVIMENTO
   ├── Análise exploratória (EDA)
   ├── Feature engineering
   ├── Treinamento de modelos
   ├── Avaliação e validação
   └── Desenvolvimento da API/serviço

3. IMPLANTAÇÃO
   ├── Empacotamento do modelo
   ├── Deploy da API
   ├── Integração com sistemas
   └── Monitoramento inicial

4. MANUTENÇÃO
   ├── Monitoramento de performance
   ├── Retreinamento periódico
   ├── Atualização de features
   └── Correção de data drift
```

**CHECKPOINT**: Pense em um projeto de DS que você já fez. Você seguiu essas fases conscientemente ou pulou direto para o código? A diferença está na previsibilidade e qualidade do resultado.

## Passo 3: Metodologias Ágeis vs. Waterfall

**Intenção**: Entender diferentes abordagens para gerenciar o desenvolvimento e escolher a mais adequada.

**Waterfall (Cascata):**
- Fases sequenciais rígidas
- Cada fase deve ser completada antes da próxima
- Requisitos definidos no início
- Pouca flexibilidade para mudanças
- Documentação extensa

```
Requisitos → Design → Implementação → Testes → Deploy → Manutenção
(cada fase completa 100% antes de avançar)
```

**Quando usar Waterfall:**
- Requisitos muito bem definidos e estáveis
- Projetos regulamentados (ex: saúde, financeiro)
- Pouca incerteza no escopo
- Equipe distribuída que precisa de clareza total

**Metodologias Ágeis (Scrum, Kanban, etc.):**
- Desenvolvimento iterativo e incremental
- Entregas frequentes de valor
- Feedback constante
- Adaptação a mudanças
- Colaboração intensa

```
Sprint 1 → MVP
Sprint 2 → Feature A
Sprint 3 → Feature B + Melhorias
Sprint 4 → Feature C + Refinamentos
(cada sprint entrega valor incremental)
```

**Quando usar Ágil:**
- Requisitos podem evoluir
- Necessidade de feedback rápido
- Projetos inovadores/experimentais
- **Projetos de Data Science** (natureza exploratória)

**Por que Ágil é melhor para DS:**

```python
# Desenvolvimento ágil em DS permite:

# Sprint 1: MVP - Baseline
modelo_baseline = LogisticRegression()
# Entrega: modelo simples funcionando

# Sprint 2: Feature Engineering
modelo_v2 = RandomForest(com_features_engineered=True)
# Entrega: melhoria de performance

# Sprint 3: Modelo Avançado
modelo_v3 = XGBoost(com_hyperparameter_tuning=True)
# Entrega: otimização de resultados

# Sprint 4: API e Deploy
api = FastAPI(model=modelo_v3)
# Entrega: solução em produção
```

**CHECKPOINT**: Projetos de DS são naturalmente experimentais. Você não sabe de antemão qual modelo funcionará melhor. Ágil permite testar, aprender e adaptar. Isso faz sentido?

## Passo 4: A Importância da Disciplina em Data Science

**Intenção**: Reconhecer que ciência de dados precisa tanto de criatividade quanto de rigor.

Data Science é frequentemente vista como "exploratória" e "criativa" - e de fato é. Mas essa criatividade precisa de estrutura para gerar valor:

**Sem Disciplina:**
```
Notebook experimental → Funciona no meu PC → 
Não roda na máquina do colega → 
Não conseguimos colocar em produção → 
Projeto arquivado
```

**Com Disciplina:**
```
Exploração estruturada → Código modular → 
Testes automatizados → CI/CD → 
Deploy confiável → Monitoramento → 
Valor real entregue
```

**Pilares da Disciplina em DS:**

1. **Reprodutibilidade**
   - Controle de versão (código + dados + modelos)
   - Ambientes isolados e documentados
   - Seeds fixos para experimentos
   
2. **Testabilidade**
   - Testes unitários para transformações
   - Validação de dados (schemas)
   - Testes de integração da API
   
3. **Manutenibilidade**
   - Código limpo e documentado
   - Arquitetura modular
   - Padrões de projeto
   
4. **Observabilidade**
   - Logging estruturado
   - Métricas de performance
   - Monitoramento de modelo (drift, bias)

**CHECKPOINT**: Disciplina não mata criatividade - ela permite que suas melhores ideias cheguem à produção e gerem impacto real.

## Passo 5: Planejando nosso Projeto API de ML

**Intenção**: Aplicar conceitos aprendidos no planejamento do projeto que vamos construir ao longo do módulo.

Vamos planejar a **API REST que consumirá um modelo de ML**, aplicando os conceitos desta aula:

**1. Concepção (onde estamos agora):**
- Objetivo: API REST para servir predições de um modelo ML
- Requisitos funcionais:
  - Endpoint para receber dados e retornar predições
  - Carregar modelo treinado
  - Validação de entrada
  - Respostas estruturadas (JSON)
- Requisitos não-funcionais:
  - Baixa latência (< 200ms)
  - Escalável
  - Observável (logs, métricas)
  - Fácil de manter

**2. Abordagem Ágil:**
```
Aula 1-2: Setup + Git → estrutura básica versionada
Aula 3: Testes → garantir qualidade
Aula 4: Docker → ambiente reprodutível
Aula 5: Dependências → gestão de bibliotecas
Aula 6: Código limpo → refatoração e padrões
Aula 7: Deploy → colocar em produção
Aula 8: Refatoração final → projeto profissional
```

**3. Estrutura que vamos construir:**
```
swe4ds-api-project/
├── src/
│   ├── api/              # Endpoints FastAPI
│   ├── models/           # Loading e inferência do modelo
│   ├── data/             # Validação e transformação de dados
│   └── utils/            # Funções auxiliares
├── tests/                # Testes automatizados
├── docker/               # Dockerfiles e configs
├── .github/              # CI/CD workflows
├── pyproject.toml        # Dependências
└── README.md             # Documentação
```

**CHECKPOINT**: Neste ponto você tem um plano claro. Nas próximas aulas, vamos executá-lo incrementalmente, sempre com disciplina e boas práticas.

# 7. Testes rápidos e validação

Nesta aula teórica, não há código para testar ainda. Mas vamos fazer uma validação conceitual:

**Teste de Compreensão:**

1. **Você consegue explicar para um colega a diferença entre código ad hoc e código estruturado?**
   - Se sim: ✅ Objetivo alcançado

2. **Você sabe identificar em qual fase do ciclo de vida está um projeto de DS?**
   - Se sim: ✅ Objetivo alcançado

3. **Você entende por que metodologias ágeis são mais adequadas para DS?**
   - Se sim: ✅ Objetivo alcançado

**Exercício mental:**

Pense em um projeto de Data Science que você já trabalhou:
- Ele seguiu alguma metodologia?
- As fases do ciclo de vida foram respeitadas?
- Chegou em produção? Por quê sim ou não?

**Resultado esperado**: Clareza sobre como a falta de engenharia impacta projetos de DS e motivação para aprender as práticas corretas.

# 8. Observabilidade e boas práticas (mini-bloco)

Mesmo em uma aula conceitual, podemos estabelecer princípios que aplicaremos daqui para frente:

**1. Documentação é código**
- Todo projeto deve ter README explicativo
- Decisões arquiteturais devem ser registradas
- Trade-off: 10 minutos documentando poupam horas de confusão futura

**2. Planejamento antes de codificação**
- Defina requisitos antes de escrever a primeira linha
- Esboce a arquitetura em alto nível
- Trade-off: parece lento no início, mas acelera o desenvolvimento

**3. Escolha metodologia apropriada ao contexto**
- Projetos exploratórios → Ágil
- Projetos regulamentados → Waterfall ou híbrido
- Trade-off: flexibilidade vs. previsibilidade

**4. Pense em manutenção desde o dia 1**
- Código que você escreve hoje, você (ou outros) vai manter amanhã
- "Eu vou lembrar depois" nunca funciona
- Trade-off: esforço inicial vs. dívida técnica exponencial

**Por que vale a pena:**
- Redução de 60-80% em retrabalho
- Projetos chegam em produção
- Equipes conseguem colaborar eficientemente
- Você se torna um profissional mais valorizado

# 9. Troubleshooting (erros comuns)

Nesta fase conceitual, os "erros" são mais de mindset:

**Erro 1: "Vou aplicar boas práticas depois que funcionar"**
- **Sintoma**: Código sempre "temporário" que vira permanente
- **Solução**: Aplique práticas desde o início. É mais rápido corrigir na hora do que refatorar depois
- **Como identificar**: Projetos com código "provisório" há meses

**Erro 2: "Metodologia é burocracia, atrasa o projeto"**
- **Sintoma**: Projeto avança rápido no início, depois emperra com problemas
- **Solução**: Metodologia não é engessamento, é guia. Adapte ao seu contexto
- **Como identificar**: "Rapidez" inicial seguida de lentidão crescente

**Erro 3: "Data Science é diferente, essas práticas não se aplicam"**
- **Sintoma**: Projetos que nunca saem do notebook
- **Solução**: DS é software também. As práticas se aplicam sim, com adaptações
- **Como identificar**: Taxa de 0% de modelos em produção

**Erro 4: "Meu código funciona, não preciso documentar"**
- **Sintoma**: Ninguém (nem você mesmo) entende o código depois de 3 meses
- **Solução**: Documente enquanto escreve. É rápido e essencial
- **Como identificar**: Tempo excessivo tentando entender código antigo

**Erro 5: "Vou usar Waterfall porque parece mais 'profissional'"**
- **Sintoma**: Projeto trava esperando "todos os requisitos" serem definidos
- **Solução**: Em DS, requisitos emergem da exploração. Use Ágil
- **Como identificar**: Paralisia por análise, nada é entregue

**Erro 6: "Não preciso planejar, vou direto para o código"**
- **Sintoma**: Reescreve o código 5 vezes porque não pensou na arquitetura
- **Solução**: 30 minutos de planejamento poupam dias de retrabalho
- **Como identificar**: Refatorações massivas constantes

# 10. Exercícios (básico e avançado)

## Exercícios Básicos

**Exercício 1: Análise de Código Ad Hoc**

Pegue um script Python que você já escreveu (pode ser de qualquer projeto pessoal ou acadêmico) e faça:

a) Liste pelo menos 5 problemas de engenharia que ele tem
b) Classifique cada problema: (ad hoc, falta modularidade, sem tratamento de erro, etc.)
c) Esboce como você reestruturaria esse código

**Critério de sucesso**:
- [ ] Identificou pelo menos 5 problemas reais
- [ ] Propôs soluções viáveis para cada um
- [ ] Entendeu a diferença entre "funciona" e "bem engenheirado"

**Exercício 2: Mapeamento de Ciclo de Vida**

Para um projeto de Data Science (real ou hipotético):

a) Descreva cada fase do ciclo de vida aplicada a esse projeto
b) Identifique que ferramentas/práticas seriam usadas em cada fase
c) Estime o esforço relativo (%) de cada fase

Exemplo:
```
Concepção: 15% - Análise de requisitos, EDA inicial
Desenvolvimento: 50% - Feature eng, modelagem, testes
Implantação: 20% - API, docker, deploy
Manutenção: 15% - Monitoramento, retreino
```

**Critério de sucesso**:
- [ ] Todas as 4 fases descritas com clareza
- [ ] Ferramentas/práticas específicas listadas
- [ ] Estimativas justificadas

## Exercício Avançado

**Exercício 3: Proposta de Projeto Estruturado**

Crie uma proposta completa para um projeto de DS seguindo metodologia ágil:

**Contexto**: Sistema de recomendação de produtos para e-commerce

**Seu desafio**:

1. **Definir Requisitos** (funcionais e não-funcionais)
2. **Planejar Sprints** (mínimo 4 sprints, 2 semanas cada)
   - O que será entregue em cada sprint?
   - Qual o critério de sucesso?
3. **Esboçar Arquitetura** (desenho simples de componentes)
4. **Definir Métricas** de sucesso técnicas e de negócio
5. **Identificar Riscos** e plano de mitigação

**Critério de sucesso**:
- [ ] Requisitos claros e mensuráveis
- [ ] Sprints com entregas incrementais de valor
- [ ] Cada sprint pode ser validado independentemente
- [ ] Arquitetura modular e escalável
- [ ] Métricas técnicas (latência, throughput) e negócio (CTR, conversão) definidas
- [ ] Pelo menos 3 riscos identificados com plano de mitigação

**Entrega**: Documento de 2-3 páginas que poderia ser apresentado para um stakeholder técnico.

# 11. Resultados e Lições

## Resultados

Como esta é uma aula conceitual, os resultados são sobre mudança de mindset e preparação:

**Como medir o sucesso desta aula:**

1. **Compreensão Conceitual**:
   - Capacidade de explicar diferenças entre código ad hoc e estruturado
   - Entendimento das fases do ciclo de vida
   - Clareza sobre quando usar Ágil vs. Waterfall

2. **Aplicação Futura**:
   - Antes de começar novo projeto, você agora pensa em: requisitos, arquitetura, fases
   - Ao ver código, você identifica problemas de engenharia
   - Você consegue justificar escolhas técnicas com base em metodologia

3. **Preparação para o Módulo**:
   - Entendimento do que será construído (API ML)
   - Motivação para aplicar boas práticas
   - Mindset de engenheiro, não apenas programador

**Indicadores qualitativos** (você mesmo pode avaliar):
- Mudança na forma como planeja projetos
- Consciência de dívida técnica
- Valorização de disciplina e metodologia

## Lições

**1. Código que funciona ≠ Código bem engenheirado**
   - Funcionamento é apenas o primeiro passo
   - Qualidade do código determina manutenibilidade e escalabilidade
   - Investimento em engenharia compensa no médio-longo prazo

**2. Data Science é Software (com características próprias)**
   - Todos os princípios de engenharia se aplicam
   - Mas precisa de adaptações: experimentação, incerteza, dados
   - Ignore engenharia e seu modelo nunca chega em produção

**3. Metodologia não é burocracia, é estratégia**
   - Processos bem definidos aceleram (não atrasam) o desenvolvimento
   - Ágil é particularmente adequado para DS pela natureza exploratória
   - Disciplina liberta, não aprisiona

**4. Planejamento antecipa problemas**
   - 10% do tempo planejando poupa 50% do tempo corrigindo
   - Arquitetura bem pensada facilita mudanças futuras
   - Requisitos claros evitam retrabalho

**5. Projetos de DS falham mais por engenharia do que por algoritmo**
   - Escolher o algoritmo certo é 20% do problema
   - Colocar em produção, manter, escalar é 80%
   - Diferencial não é apenas saber ML, é saber engenharia de ML

# 12. Encerramento e gancho para a próxima aula (script)

Muito bem! Nesta aula cobrimos os fundamentos conceituais de engenharia de software e como eles se aplicam a projetos de Data Science. Vimos a diferença crucial entre programação ad hoc e desenvolvimento estruturado, entendemos o ciclo de vida do software e por que metodologias ágeis são especialmente adequadas para ciência de dados.

O mais importante: estabelecemos que Data Science não é apenas sobre algoritmos e métricas de modelo. É sobre construir **soluções de software confiáveis** que entreguem valor real em produção. E isso exige disciplina, metodologia e boas práticas.

Agora você tem o mindset correto. Mas mindset sem prática não gera resultado. Por isso, a partir da próxima aula, vamos colocar a mão na massa!

**Na Aula 01 - Parte 02**, vamos mergulhar em **princípios de design de código**: modularidade, coesão, acoplamento, legibilidade e manutenibilidade. Vamos entender o conceito de dívida técnica e como nossas decisões de hoje impactam o projeto no futuro. Mais importante: vamos ver exemplos práticos de código bem estruturado versus código problemático.

Preparados? Nos vemos na próxima parte. Até lá, pensem nos projetos que vocês já fizeram e identifiquem oportunidades de melhoria. Esse exercício mental vai tornar os próximos conceitos muito mais concretos.

Até já!
