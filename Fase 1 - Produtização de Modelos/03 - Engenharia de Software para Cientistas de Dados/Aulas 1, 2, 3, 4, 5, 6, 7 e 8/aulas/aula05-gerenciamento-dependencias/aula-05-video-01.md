---
titulo: "Aula 05 – Parte 01: Isolamento de Dependências - Ambientes Virtuais em Python"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 20
prerequisitos:
  - "Python 3.12+"
  - "Aula 04 de Docker concluída"
  - "Projeto swe4ds-credit-api criado"
tags: ["python", "virtualenv", "uv", "dependency-management", "isolation"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos falar sobre um tema que parece simples mas causa muita dor de cabeça: **gerenciamento de dependências**.

Você já tentou rodar um código antigo seu e deu erro porque uma biblioteca foi atualizada? Ou instalou um pacote para um projeto e quebrou outro? Ou pior: mandou seu código para um colega e ele não conseguiu rodar porque tinha versões diferentes das bibliotecas?

Esses problemas acontecem porque, por padrão, Python instala tudo globalmente. Todos os projetos compartilham as mesmas bibliotecas. Quando um projeto precisa de pandas 1.5 e outro de pandas 2.0... caos.

Nesta aula, vamos entender o conceito de **ambientes virtuais** e conhecer o **UV** - uma ferramenta moderna que vai substituir o venv, virtualenv, pip e até o Poetry no seu workflow. Ao final, você vai entender por que isolamento é fundamental e como configurar isso no nosso projeto de crédito.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você desenvolve projetos de Data Science. Cada projeto usa bibliotecas diferentes: um usa TensorFlow 1.x (legado), outro usa TensorFlow 2.x. Um precisa de pandas 1.5 por compatibilidade, outro quer pandas 2.0 por performance. Você instala tudo no Python global.

**Agitação**: Um dia você atualiza o pandas para o projeto novo. O projeto antigo para de funcionar. Você tenta fazer downgrade, quebra o projeto novo. Você reinstala tudo, agora nenhum dos dois funciona. Seu colega tenta rodar seu código e não consegue porque ele tem outras versões. O `requirements.txt` que você mandou estava desatualizado. O tempo que você deveria gastar desenvolvendo, você gasta debugando conflitos de versão. Isso tem nome: **dependency hell**.

**Solução**: Ambientes virtuais. Cada projeto tem seu próprio ambiente isolado com suas próprias bibliotecas. Você pode ter 10 versões diferentes do pandas instaladas - uma para cada projeto. Quando você ativa um ambiente, só ele está acessível. Mudanças em um projeto não afetam os outros. E com ferramentas modernas como **UV**, criar e gerenciar esses ambientes é rápido e simples.

No nosso projeto de crédito, vamos migrar do setup tradicional para UV, garantindo que qualquer pessoa consiga reproduzir exatamente o mesmo ambiente.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Explicar** o problema do "dependency hell" e suas consequências
2. **Diferenciar** ambientes globais de ambientes virtuais isolados
3. **Comparar** ferramentas tradicionais (venv, virtualenv, conda) com UV
4. **Instalar** e configurar o UV no seu sistema
5. **Criar** um ambiente virtual com UV
6. **Identificar** os benefícios de isolamento para reprodutibilidade

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+ instalado
- Windows com PowerShell ou WSL
- Projeto swe4ds-credit-api das aulas anteriores

**Verificar ambiente:**

```bash
# Verificar versão do Python
python --version

# Verificar onde Python está instalado
where python

# Verificar pip
pip --version

# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api
```

**Checklist:**
- [ ] Python 3.12+ disponível
- [ ] Acesso ao terminal (PowerShell ou bash)
- [ ] Projeto existente acessível

# 5. Visão geral do que já existe no projeto (continuidade)

**Estado atual do projeto** (após módulo de Docker):

```
swe4ds-credit-api/
# 6. Passo a passo (comandos + código)

## Passo 1: Entendendo o Problema - Instalação Global (Excalidraw: Slide 1)

**Intenção**: Fixar a teoria por trás do “dependency hell”.

### Como o Python resolve imports (visão conceitual)

Quando você roda `import pandas`, o Python procura módulos nesta ordem:
1. Diretório atual do projeto
2. Diretórios do `PYTHONPATH`
3. `site-packages` do Python ativo

Se você instala tudo no Python global, **todo projeto compartilha o mesmo `site-packages`**.

```
Python global
└── Lib/site-packages
   ├── pandas (uma única versão)
   ├── numpy (uma única versão)
   └── ...
```

### O Problema: versão única, muitos projetos

```
C:\Users\diogomiyake\
├── projeto-A/          → precisa pandas 1.5.x
├── projeto-B/          → precisa pandas 2.x
└── Python312/
   └── site-packages/  → só pode haver UMA versão instalada
```

**CHECKPOINT**: Você entende que o conflito acontece porque todos os projetos “enxergam” o mesmo `site-packages`.

---

## Passo 2: Conceito de Ambiente Virtual (Excalidraw: Slide 1)

**Intenção**: Consolidar a teoria do isolamento.

### O que é um ambiente virtual de verdade?

Um ambiente virtual cria um **Python isolado** com:
- seus próprios `site-packages`
- seu próprio executável `python`
- seu próprio `pip`

```
C:\Users\diogomiyake\
├── projeto-A/
│   └── .venv/                  # Ambiente isolado
│       └── Lib/site-packages/  # dependências do projeto A
│
├── projeto-B/
│   └── .venv/                  # Ambiente isolado
│       └── Lib/site-packages/  # dependências do projeto B
│
└── Python312/                  # Python global (limpo)
```

**Benefícios teóricos principais:**
| Aspecto | Global | Ambiente Virtual |
|---------|--------|-----------------|
| Isolamento | Nenhum | Total por projeto |
| Conflitos | Frequentes | Improváveis |
| Reprodutibilidade | Difícil | Controlável |
| Limpeza | Arriscada | Remove só a pasta |

**CHECKPOINT**: Você consegue explicar por que isolamento resolve conflitos.

---

## Passo 3: Ferramentas Tradicionais vs. UV (Excalidraw: Slide 2)

**Intenção**: Entender, no nível conceitual, o papel de cada ferramenta.

### Onde cada ferramenta atua no ciclo de vida

| Etapa | Ferramenta tradicional | UV |
|------|-------------------------|----|
| Criar ambiente | venv/virtualenv | `uv venv` |
| Instalar pacotes | pip | `uv add` / `uv pip` |
| Resolver versões | pip-tools | `uv lock` |
| Reproduzir ambiente | manual | `uv sync` |

### Por que UV vira padrão?

O UV unifica tudo em um fluxo:
```
declarar (pyproject) → resolver (lock) → sincronizar (sync)
```

Isso reduz **erros humanos**, aumenta **reprodutibilidade** e dá **velocidade** ao ciclo de desenvolvimento.

**CHECKPOINT**: Você entende o papel do UV no fluxo de dependências.
conda create -n meuenv python=3.12
conda activate meuenv
conda install pandas
```

### Problemas das Ferramentas Tradicionais

| Ferramenta | Problema |
|------------|----------|
| venv/pip | Lento, não tem lockfile nativo |
| virtualenv | Precisa instalar separadamente |
| Conda | Pesado, conflitos com pip, resolve lento |
| Poetry | Lento para instalar, complexo |

### Por que UV?

**UV** é uma ferramenta escrita em Rust que substitui:
- `venv` → `uv venv`
- `pip` → `uv pip` ou `uv add`
- `pip-tools` → lockfile nativo
- `virtualenv` → mais rápido
- `poetry` → mais simples e rápido

**Vantagens do UV:**
- **10-100x mais rápido** que pip
- **Lockfile nativo** para reprodutibilidade
- **Compatível com pip** (usa mesmos pacotes)
- **Single binary** (fácil de instalar)
- **Resolve dependências** corretamente

**CHECKPOINT**: Você entende as vantagens do UV sobre ferramentas tradicionais.

---

## Passo 4: Instalando UV (Excalidraw: Slide 2)

**Intenção**: Instalar UV no sistema.

### Windows (PowerShell)

```powershell
# Método 1: via instalador oficial (recomendado)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Método 2: via pip (se preferir)
pip install uv
```

### Linux/Mac

```bash
# Via curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Verificar instalação

```bash
# Verificar versão
uv --version

# Ver comandos disponíveis
uv --help
```

**Saída esperada:**
```
uv 0.4.x (ou versão mais recente)
```

### Estrutura de Comandos UV

```
uv
├── venv        # Criar ambiente virtual
├── pip         # Comandos compatíveis com pip
├── add         # Adicionar dependência ao projeto
├── remove      # Remover dependência
├── sync        # Sincronizar ambiente com lockfile
├── lock        # Gerar lockfile
├── run         # Executar comando no ambiente
└── tool        # Gerenciar ferramentas CLI
```

**CHECKPOINT**: UV está instalado e funciona (`uv --version` retorna versão).

---

## Passo 5: Criando Primeiro Ambiente com UV

**Intenção**: Praticar a criação de ambiente virtual com UV.

```bash
# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Criar ambiente virtual com UV
uv venv

# Verificar que foi criado
dir .venv
```

**Saída esperada:**
```
Using CPython 3.12.x
Creating virtual environment at: .venv
Activate with: .venv\Scripts\activate
```

### Ativando o Ambiente

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Ou (cmd)
.\.venv\Scripts\activate.bat

# Verificar que está ativo (prompt muda)
# (.venv) PS C:\Users\diogomiyake\projects\swe4ds-credit-api>

# Verificar Python do ambiente
where python
# Deve mostrar: .venv\Scripts\python.exe

# Verificar que está vazio
pip list
# Deve mostrar apenas pip e setuptools
```

### Desativando

```bash
deactivate
```

**CHECKPOINT**: Ambiente criado e ativável. `where python` mostra caminho dentro de `.venv`.

---

## Passo 6: Comparativo de Velocidade

**Intenção**: Demonstrar a velocidade do UV.

```bash
# Ativar ambiente
.\.venv\Scripts\Activate.ps1

# Instalar pandas com uv pip (observe a velocidade)
uv pip install pandas

# Verificar instalação
python -c "import pandas; print(pandas.__version__)"

# Remover para teste comparativo
uv pip uninstall pandas -y

# Instalar com pip tradicional (mais lento)
pip install pandas

# Comparar tempos (você vai notar a diferença)
```

**UV típico:** 2-5 segundos para pandas
**pip tradicional:** 15-30 segundos

**CHECKPOINT**: Você percebeu a diferença de velocidade entre UV e pip.

---

## Passo 7: Atualizando .gitignore

**Intenção**: Garantir que ambiente virtual não seja commitado.

Verifique se `.gitignore` tem:

```bash
# Verificar se .venv está no .gitignore
cat .gitignore | grep venv
```

Se não tiver, adicione:

```bash
# Adicionar ao .gitignore
echo ".venv/" >> .gitignore
```

**Por que não commitar .venv?**
- É grande (centenas de MB)
- É específico do sistema operacional
- Pode ser recriado a partir do lockfile
- Contém binários compilados

**CHECKPOINT**: `.venv/` está no `.gitignore`.

# 7. Testes rápidos e validação

```bash
# Verificar UV instalado
uv --version

# Verificar ambiente existe
Test-Path .venv  # PowerShell
# ou
ls .venv  # bash

# Ativar e verificar isolamento
.\.venv\Scripts\Activate.ps1
where python  # Deve mostrar .venv\Scripts\python.exe
python --version

# Instalar pacote de teste
uv pip install httpx
python -c "import httpx; print('httpx importado com sucesso!')"

# Desativar
deactivate

# Tentar importar fora do ambiente (deve falhar se não está global)
python -c "import httpx"  # Pode falhar (correto!)
```

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas de Ambientes Virtuais

1. **Um ambiente por projeto**
   - Nunca compartilhe ambientes entre projetos
   - Nome padrão: `.venv` (convenção)
   - **Trade-off**: Usa mais espaço em disco, mas evita conflitos

2. **Sempre ative antes de trabalhar**
   - Verifique o prompt (deve mostrar nome do ambiente)
   - Configure seu IDE para ativar automaticamente
   - **Trade-off**: Um passo extra, mas garante consistência

3. **Nunca instale no global**
   - Exceção: ferramentas CLI (uv, pipx)
   - Tudo mais: dentro do ambiente
   - **Trade-off**: Precisa ativar ambiente, mas evita dependency hell

4. **Ambiente virtual no .gitignore**
   - Não versione `.venv/`
   - Versione apenas arquivos de lock
   - **Trade-off**: Precisa recriar ambiente ao clonar

5. **Documente a versão do Python**
   - No pyproject.toml: `requires-python = ">=3.12"`
   - Evita erros de compatibilidade
   - **Trade-off**: Pode limitar contribuidores com Python antigo

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `uv: command not found` | UV não instalado ou não no PATH | Reinstalar UV, reiniciar terminal |
| `Activate.ps1 cannot be loaded` | Política de execução PS | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Pacote não encontrado após instalar | Ambiente não ativado | Ativar ambiente antes de usar |
| `python` ainda usa global | PATH não atualizado | Reativar ambiente, verificar `where python` |
| Ambiente corrompido | Instalação interrompida | Deletar `.venv/`, recriar |
| Versão errada do Python | Múltiplos Pythons instalados | `uv venv --python 3.12` |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Criar Ambiente de Teste

Crie um novo diretório `teste-isolamento/`, crie um ambiente virtual com UV, instale `requests`, e verifique que o pacote só existe nesse ambiente.

**Critério de sucesso**: `import requests` funciona dentro do ambiente e falha fora dele.

## Exercício Básico 2: Verificar Isolamento

Com dois terminais abertos, ative ambientes diferentes em cada um. Em um instale `rich`, no outro não. Verifique que `import rich` funciona em um e falha no outro.

**Critério de sucesso**: Demonstrar que os ambientes são realmente isolados.

## Exercício Avançado: Comparar Velocidades

Crie um script que mede o tempo de instalação de 10 pacotes populares usando `pip` vs `uv pip`. Documente os resultados em uma tabela.

**Critério de sucesso**: Tabela comparativa mostrando speedup do UV.

# 11. Resultados e Lições

## Métricas para Acompanhar

| Métrica | Como medir | Valor esperado |
|---------|------------|----------------|
| Tempo de criação do venv | `Measure-Command { uv venv }` | < 1 segundo |
| Tempo de instalação pandas | `Measure-Command { uv pip install pandas }` | < 5 segundos |
| Tamanho do ambiente | `(Get-ChildItem .venv -Recurse \| Measure-Object -Property Length -Sum).Sum / 1MB` | Varia |
| Isolamento funcional | Teste de import dentro/fora | 100% isolado |

## Lições desta Aula

1. **Dependency hell é real** - Projetos com dependências globais eventualmente quebram
2. **Isolamento é fundamental** - Cada projeto deve ter seu ambiente
3. **UV é a ferramenta moderna** - Mais rápido e simples que alternativas
4. **Ambiente virtual não se versiona** - Apenas o lockfile
5. **Ativar antes de trabalhar** - Sempre verifique o prompt

# 12. Encerramento e gancho para a próxima aula (script)

Nesta aula você entendeu o problema do dependency hell e por que ambientes virtuais são essenciais para qualquer projeto Python profissional. Você instalou o UV - uma ferramenta moderna que vai acelerar muito seu workflow - e criou seu primeiro ambiente isolado.

Na próxima aula, vamos mergulhar no **gerenciamento de pacotes propriamente dito**. Você vai aprender sobre:
- Versionamento semântico (o que significa `pandas>=2.0,<3.0`)
- Como o UV gerencia dependências com `pyproject.toml`
- O poder do lockfile para reprodutibilidade perfeita
- Diferença entre dependências de produção e desenvolvimento

Vamos transformar nosso projeto de crédito em um projeto Python moderno com todas as dependências declaradas e travadas. Até a próxima aula!
