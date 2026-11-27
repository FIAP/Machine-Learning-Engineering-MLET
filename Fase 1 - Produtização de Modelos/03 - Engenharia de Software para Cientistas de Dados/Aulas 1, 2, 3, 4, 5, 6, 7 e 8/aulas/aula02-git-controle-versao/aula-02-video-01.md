---
titulo: "Aula 02 – Parte 01: Git na Teoria - Conceitos Básicos de Controle de Versão Distribuído"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 20
prerequisitos:
  - "Python 3.12+"
  - "UV instalado"
  - "Conceitos da Aula 01"
  - "Conta no GitHub"
tags: ["git", "controle-versao", "github", "repositorio", "commits", "branches"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula, vamos mergulhar em uma das ferramentas mais fundamentais para qualquer profissional de tecnologia: o Git. Se na Aula 01 falamos sobre engenharia de software e boas práticas de código, agora vamos garantir que todo esse trabalho seja preservado, rastreável e colaborativo.

Imagine o seguinte cenário: você passou semanas desenvolvendo um modelo de Machine Learning, ajustando hiperparâmetros, experimentando diferentes features. Tudo funcionando perfeitamente. Aí você faz "uma pequena mudança" para testar algo e... catástrofe. O modelo parou de funcionar e você não lembra exatamente o que mudou. Sem controle de versão, você está perdido.

O Git resolve esse problema de forma elegante. Ele é como uma máquina do tempo para o seu código. Vamos entender profundamente como ele funciona e, mais importante, por que ele é essencial para projetos de Data Science.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você está desenvolvendo um pipeline de ML. Tem várias versões de scripts: `train_v1.py`, `train_v2_final.py`, `train_v2_final_REAL.py`, `train_v2_final_REAL_corrigido.py`. Cada arquivo tem pequenas diferenças que você não lembra mais. Qual é a versão que estava funcionando na semana passada? Onde está aquela configuração que dava bons resultados?

**Agitação**: Um colega pede para colaborar no projeto. Vocês trabalham no mesmo arquivo. Ele faz mudanças, você faz mudanças. Vocês sobrescrevem o trabalho um do outro. Alguém envia por email. Outro coloca no Drive. Conflitos aparecem. Ninguém sabe qual é a versão "oficial". O projeto que era promissor se torna um pesadelo de coordenação. Tempo perdido, frustração, retrabalho.

**Solução**: O Git oferece controle de versão distribuído. Cada alteração é registrada com autor, data e descrição. Você pode navegar no histórico, comparar versões, voltar no tempo. Branches permitem experimentar sem medo. Repositórios remotos (GitHub/GitLab) centralizam a colaboração. Isso não é apenas para grandes equipes - é essencial mesmo para você trabalhando sozinho. A partir desta aula, todo nosso projeto de API será versionado profissionalmente.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Explicar** o que é controle de versão e por que é fundamental para Data Science
2. **Diferenciar** repositórios locais e remotos, entendendo a natureza distribuída do Git
3. **Criar** um repositório no GitHub e cloná-lo localmente
4. **Realizar** commits com mensagens descritivas seguindo boas práticas
5. **Navegar** pelo histórico de commits e entender a estrutura de um repositório Git
6. **Compreender** o conceito de branches como ramificações de desenvolvimento

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Git 2.40+ instalado
- Python 3.12+
- UV instalado
- Conta no GitHub (gratuita)
- VS Code ou editor de sua preferência
- Terminal (PowerShell no Windows, bash no Linux/Mac)

**Instalação do Git:**

```bash
# Windows - Download do instalador oficial
# https://git-scm.com/download/win

# Verificar instalação
git --version
# Esperado: git version 2.40.0 ou superior
```

```bash
# Linux (Ubuntu/Debian)
sudo apt update
sudo apt install git

# macOS (com Homebrew)
brew install git
```

**Configuração inicial do Git (OBRIGATÓRIO na primeira vez):**

```bash
# Configurar seu nome (aparecerá nos commits)
git config --global user.name "Seu Nome Completo"

# Configurar seu email (mesmo do GitHub)
git config --global user.email "seu.email@exemplo.com"

# Configurar editor padrão (VS Code)
git config --global core.editor "code --wait"

# Configurar branch padrão como 'main'
git config --global init.defaultBranch main

# Verificar configurações
git config --list
```

**Checklist de Setup:**
- [ ] Git instalado e versão verificada (2.40+)
- [ ] Nome e email configurados globalmente
- [ ] Conta no GitHub criada e acessível
- [ ] VS Code instalado
- [ ] UV instalado

# 5. Visão geral do que já existe no projeto (continuidade)

Na Aula 01, criamos exemplos de código em uma estrutura local. Agora vamos oficializar nosso projeto criando um repositório Git. A partir deste momento, toda evolução será rastreada.

**Estrutura atual (local, sem Git):**
```
swe4ds-api-project/
├── .venv/
└── exemplos/
    ├── modularidade/
    ├── coesao/
    ├── acoplamento/
    ├── paradigmas/
    └── refatoracao/
```

**O que faremos nesta aula:**
```
swe4ds-api-project/           # Agora um repositório Git!
├── .git/                     # [NOVO] Pasta oculta do Git
├── .gitignore                # [NOVO] Arquivos a ignorar
├── README.md                 # [NOVO] Documentação do projeto
├── .venv/                    # (ignorado pelo Git)
└── exemplos/
    └── (...)
```

# 6. Passo a passo (comandos + código)

## Passo 1: Entendendo o Git Conceitualmente

**Intenção**: Antes de usar, vamos entender o que é o Git e como ele funciona internamente.

### O que é Controle de Versão?

Controle de versão é um sistema que registra alterações em arquivos ao longo do tempo. Imagine um "histórico de edições" sofisticado que permite:

- Ver exatamente o que mudou, quando e por quem
- Voltar para qualquer versão anterior
- Trabalhar em paralelo sem conflitos
- Mesclar trabalhos de diferentes pessoas

### Por que Git é "Distribuído"?

Diferente de sistemas centralizados (como SVN), no Git:

- **Cada desenvolvedor tem uma cópia completa do histórico**
- Você pode trabalhar offline
- Não há ponto único de falha
- Operações são extremamente rápidas (tudo é local)

**Conceito visual (Excalidraw: Slide 1 - Introdução ao Git):**
```
┌─────────────────────────────────────────────────────────────────┐
│                    SISTEMA DISTRIBUÍDO                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    ┌──────────┐         ┌──────────┐         ┌──────────┐       │
│    │ Dev A    │         │ GitHub   │         │ Dev B    │       │
│    │ ┌──────┐ │         │ ┌──────┐ │         │ ┌──────┐ │       │
│    │ │Repo  │ │◄───────►│ │Repo  │ │◄───────►│ │Repo  │ │       │
│    │ │Local │ │  push   │ │Remoto│ │  pull   │ │Local │ │       │
│    │ │      │ │  pull   │ │      │ │  push   │ │      │ │       │
│    │ └──────┘ │         │ └──────┘ │         │ └──────┘ │       │
│    └──────────┘         └──────────┘         └──────────┘       │
│                                                                 │
│    Cada desenvolvedor tem uma cópia COMPLETA do repositório     │
└─────────────────────────────────────────────────────────────────┘
```

**CHECKPOINT**: Você entende a diferença entre um sistema centralizado e distribuído? No Git, você tem autonomia total localmente.

---

## Passo 2: Estrutura de um Repositório Git

**Intenção**: Entender os conceitos fundamentais antes de criar nosso repositório.

### Os Três Estados do Git

Arquivos no Git podem estar em três estados:

1. **Working Directory (Diretório de Trabalho)**: Seus arquivos como você os vê
2. **Staging Area (Área de Preparação)**: Arquivos marcados para o próximo commit
3. **Repository (.git)**: Histórico completo de commits

**Fluxo básico (Excalidraw: Slide 2 - Estrutura do Git):**
```
┌────────────────────────────────────────────────────────────────────┐
│                    FLUXO DE TRABALHO GIT                           │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  Working Directory    Staging Area          Repository (.git)      │
│  ┌──────────────┐    ┌──────────────┐       ┌──────────────┐       │
│  │              │    │              │       │              │       │
│  │  Arquivos    │───►│  Preparados  │──────►│  Commits     │       │
│  │  modificados │add │  para commit │commit │ (histórico)  │       │
│  │              │    │              │       │              │       │
│  └──────────────┘    └──────────────┘       └──────────────┘       │
│                                                                    │
│  git add arquivo.py      git commit -m "mensagem"                  │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### O que é um Commit?

Um **commit** é um snapshot do seu projeto em um momento específico. Cada commit contém:

- **Hash único**: Identificador SHA-1 (ex: `a1b2c3d4...`)
- **Autor**: Quem fez a alteração
- **Data**: Quando foi feito
- **Mensagem**: Descrição do que mudou
- **Ponteiro para commit anterior**: Formando uma cadeia (histórico)

### O que são Branches?

**Branches** são ramificações independentes de desenvolvimento. Pense como universos paralelos onde você pode experimentar sem afetar o código principal.

```
main:     A ─── B ─── C ─── D ─── E
                       \
feature:                F ─── G ─── H
```

A branch `main` continua seu desenvolvimento enquanto `feature` evolui separadamente. Depois, você pode "mesclar" (merge) as mudanças.

**CHECKPOINT**: Você consegue explicar os três estados do Git e o que é um commit?

---

## Passo 3: Criando o Repositório no GitHub

**Intenção**: Criar nosso repositório remoto que será a "fonte da verdade" do projeto.

### 3.1 Acessar o GitHub

1. Acesse [github.com](https://github.com)
2. Faça login na sua conta
3. Clique no botão **"+"** no canto superior direito
4. Selecione **"New repository"**

### 3.2 Configurar o Repositório

Preencha os campos:

| Campo | Valor |
|-------|-------|
| Repository name | `swe4ds-credit-api` |
| Description | API REST para predição de inadimplência de cartão de crédito |
| Visibility | Public (ou Private se preferir) |
| Initialize with README | **Marque esta opção** |
| Add .gitignore | Python |
| License | MIT License |

**Por que essas escolhas?**
- **README**: Documenta o projeto (boa prática)
- **.gitignore Python**: Já vem configurado para ignorar `.venv/`, `__pycache__/`, etc.
- **MIT License**: Licença permissiva, comum em projetos open source

Clique em **"Create repository"**.

**CHECKPOINT**: Você deve ver seu repositório criado com README.md, .gitignore e LICENSE.

---

## Passo 4: Clonando o Repositório Localmente

**Intenção**: Trazer o repositório remoto para sua máquina local.

### 4.1 Copiar URL do Repositório

No GitHub, clique no botão verde **"Code"** e copie a URL HTTPS:
```
https://github.com/SEU_USUARIO/swe4ds-credit-api.git
```

### 4.2 Clonar via Terminal

```bash
# Navegue para onde você quer o projeto
cd c:\Users\diogomiyake\projects

# Clone o repositório
git clone https://github.com/SEU_USUARIO/swe4ds-credit-api.git

# Entre na pasta do projeto
cd swe4ds-credit-api

# Verifique que o Git está configurado
git status
```

**Saída esperada:**
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

### 4.3 Explorar a Estrutura Criada

```bash
# Listar todos os arquivos (incluindo ocultos)
# Windows PowerShell:
Get-ChildItem -Force

# Linux/macOS:
ls -la
```

**Estrutura após clone:**
```
swe4ds-credit-api/
├── .git/              # Pasta oculta com todo o histórico Git
├── .gitignore         # Arquivos a ignorar
├── LICENSE            # Licença MIT
└── README.md          # Documentação inicial
```

A pasta `.git/` é onde o Git armazena todo o histórico. **Nunca modifique manualmente!**

**CHECKPOINT**: O comando `git status` mostra "nothing to commit, working tree clean".

---

## Passo 5: Configurando o Ambiente Python no Projeto

**Intenção**: Preparar o ambiente de desenvolvimento com UV.

```bash
# Dentro da pasta do projeto clonado
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Criar ambiente virtual com UV
uv venv

# Ativar ambiente virtual (Windows)
.venv\Scripts\activate

# Instalar dependências iniciais
uv pip install pandas numpy scikit-learn

# Verificar instalação
python -c "import pandas; print(f'pandas {pandas.__version__}')"
```

**Verificar que .venv será ignorado:**

```bash
# Verificar conteúdo do .gitignore
cat .gitignore
```

O arquivo `.gitignore` gerado pelo GitHub para Python já inclui:
```gitignore
# Environments
.env
.venv
env/
venv/
```

**CHECKPOINT**: Ambiente virtual ativo e `.venv/` listado no `.gitignore`.

---

## Passo 6: Fazendo Nosso Primeiro Commit

**Intenção**: Registrar nossa primeira alteração no histórico.

### 6.1 Atualizar o README.md

Abra o arquivo `README.md` e substitua o conteúdo:

```markdown
# SWE4DS Credit API

API REST para predição de inadimplência de cartão de crédito, desenvolvida como projeto prático do curso de Engenharia de Machine Learning.

## Sobre o Projeto

Este projeto demonstra boas práticas de Engenharia de Software aplicadas a Data Science:

- Controle de versão com Git
- Ambientes reprodutíveis
- Testes automatizados
- Deploy em produção

## Tecnologias

- Python 3.12+
- FastAPI
- scikit-learn
- MLflow

## Setup

```bash
# Clonar repositório
git clone https://github.com/SEU_USUARIO/swe4ds-credit-api.git
cd swe4ds-credit-api

# Criar ambiente virtual
uv venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# Instalar dependências
uv pip install -r requirements.txt
```

## Autor

Seu Nome - Curso Engenharia de Machine Learning
```

### 6.2 Criar arquivo requirements.txt

```bash
# Criar requirements.txt com dependências atuais
uv pip freeze > requirements.txt
```

### 6.3 Verificar o Estado do Repositório

```bash
git status
```

**Saída esperada:**
```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
        modified:   README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        requirements.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

### 6.4 Adicionar Arquivos ao Staging

```bash
# Adicionar arquivos específicos
git add README.md requirements.txt

# Verificar staging
git status
```

**Saída esperada:**
```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   README.md
        new file:   requirements.txt
```

### 6.5 Criar o Commit

```bash
# Commit com mensagem descritiva
git commit -m "docs: atualiza README e adiciona requirements.txt

- Adiciona descrição completa do projeto
- Inclui instruções de setup com UV
- Lista tecnologias que serão utilizadas
- Gera requirements.txt com dependências iniciais"
```

**Convenção de mensagens de commit (Conventional Commits):**

| Prefixo | Uso |
|---------|-----|
| `feat:` | Nova funcionalidade |
| `fix:` | Correção de bug |
| `docs:` | Documentação |
| `style:` | Formatação (não afeta lógica) |
| `refactor:` | Refatoração de código |
| `test:` | Adição/modificação de testes |
| `chore:` | Tarefas de manutenção |

**CHECKPOINT**: O comando `git log --oneline` mostra seu novo commit.

---

## Passo 7: Enviando para o GitHub (Push)

**Intenção**: Sincronizar as alterações locais com o repositório remoto.

```bash
# Enviar commits para o GitHub
git push origin main
```

**Se for sua primeira vez**, o Git pode pedir autenticação. Recomendo configurar um **Personal Access Token** ou usar **SSH keys**. Por agora, use a autenticação via browser que o Git oferece.

**CHECKPOINT**: Acesse seu repositório no GitHub e veja as alterações refletidas.

---

## Passo 8: Visualizando o Histórico

**Intenção**: Aprender a navegar pelo histórico de commits.

```bash
# Ver histórico resumido
git log --oneline

# Ver histórico detalhado
git log

# Ver histórico com grafo de branches
git log --oneline --graph --all

# Ver alterações de um commit específico
git show HEAD
```

**Exemplo de saída:**
```
a1b2c3d (HEAD -> main, origin/main) docs: atualiza README e adiciona requirements.txt
f4e5d6c Initial commit
```

**Comandos úteis para explorar:**

```bash
# Ver diferenças não commitadas
git diff

# Ver diferenças no staging
git diff --staged

# Ver quem alterou cada linha de um arquivo
git blame README.md
```

**CHECKPOINT**: Você consegue ver o histórico de commits e entender cada entrada.

---

## Passo 9: Git e Data Science - Por que é Essencial?

**Intenção**: Conectar Git com o contexto de Data Science (Excalidraw: Slide 3 - Git e Data Science).

### Reprodutibilidade de Experimentos

Em Data Science, você frequentemente experimenta:
- Diferentes hiperparâmetros
- Diferentes features
- Diferentes algoritmos
- Diferentes preprocessamentos

Cada experimento pode ser uma branch ou um commit. Você pode:

```bash
# Voltar para uma versão específica
git checkout a1b2c3d

# Comparar duas versões
git diff v1.0 v2.0

# Ver qual versão tinha o melhor resultado
git log --oneline
```

### Rollback e Recuperação

Algo deu errado? Volte no tempo:

```bash
# Desfazer alterações não commitadas
git checkout -- arquivo.py

# Voltar para commit anterior (mantendo histórico)
git revert HEAD

# Ver versão antiga de um arquivo
git show HEAD~2:train.py
```

### Colaboração em Equipe

- Múltiplos cientistas de dados trabalhando no mesmo projeto
- Cada um em sua branch
- Code review antes de integrar
- Histórico completo de quem fez o quê

# 7. Testes rápidos e validação

**Verificar configuração do Git:**
```bash
git config --list | grep user
```

Esperado:
```
user.name=Seu Nome
user.email=seu.email@exemplo.com
```

**Verificar conexão com GitHub:**
```bash
git remote -v
```

Esperado:
```
origin  https://github.com/SEU_USUARIO/swe4ds-credit-api.git (fetch)
origin  https://github.com/SEU_USUARIO/swe4ds-credit-api.git (push)
```

**Verificar que commits locais e remotos estão sincronizados:**
```bash
git status
```

Esperado:
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas Aplicadas

1. **Mensagens de commit descritivas**
   - Use o padrão Conventional Commits (feat:, fix:, docs:, etc.)
   - Primeira linha é um resumo (max 50 caracteres)
   - Corpo explica o "porquê" (não apenas "o quê")
   - **Trade-off**: Leva mais tempo para escrever, mas economiza horas ao investigar bugs

2. **Commits atômicos**
   - Cada commit deve representar UMA mudança lógica
   - Evite commits gigantes com múltiplas alterações não relacionadas
   - **Trade-off**: Mais commits pequenos = histórico mais navegável

3. **.gitignore desde o início**
   - Nunca versione arquivos gerados, credenciais ou ambientes virtuais
   - O template Python do GitHub já cobre a maioria dos casos
   - **Trade-off**: Nenhum - é apenas boa prática, sem desvantagens

4. **README.md sempre atualizado**
   - É a porta de entrada do projeto
   - Inclua: descrição, setup, uso, contribuição
   - **Trade-off**: Exige manutenção, mas facilita onboarding

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `fatal: not a git repository` | Você não está em uma pasta com Git | Use `cd` para entrar na pasta do projeto |
| `error: failed to push some refs` | Há commits no remoto que você não tem | Execute `git pull` antes de `git push` |
| `Author identity unknown` | Git não sabe quem você é | Configure `git config --global user.name/email` |
| `Permission denied (publickey)` | Problema de autenticação SSH | Use HTTPS ou configure SSH keys |
| `fatal: refusing to merge unrelated histories` | Históricos incompatíveis | Use `git pull --allow-unrelated-histories` |
| `.venv/` aparece no `git status` | .gitignore não está correto | Verifique se `.venv/` está no .gitignore |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Adicionar novo arquivo

1. Crie um arquivo `CONTRIBUTING.md` com regras de contribuição
2. Adicione ao staging com `git add`
3. Faça commit com mensagem seguindo Conventional Commits
4. Envie para o GitHub com `git push`

**Critério de sucesso**: O arquivo aparece no GitHub.

## Exercício Básico 2: Explorar histórico

1. Use `git log --oneline` para listar commits
2. Escolha um commit e veja detalhes com `git show <hash>`
3. Use `git blame README.md` para ver quem editou cada linha

**Critério de sucesso**: Você consegue identificar autor e data de cada alteração.

## Exercício Avançado: Desfazendo alterações

1. Edite o `README.md` adicionando uma linha de erro
2. Antes de commitar, use `git diff` para ver a mudança
3. Desfaça a alteração com `git checkout -- README.md`
4. Verifique que o arquivo voltou ao estado original

**Critério de sucesso**: O `README.md` está igual ao último commit.

# 11. Resultados e Lições

## Como Medir o Sucesso

| Métrica | Como Medir | Valor Esperado |
|---------|------------|----------------|
| Repositório criado | Acessar URL no GitHub | Página carrega corretamente |
| Commits funcionando | `git log --oneline` | Pelo menos 2 commits listados |
| Sincronização | `git status` | "up to date with origin/main" |
| .gitignore correto | `.venv/` não aparece em `git status` | Sem arquivos de ambiente |

## Lições Aprendidas

1. **Git é uma máquina do tempo** - você pode navegar por qualquer versão do seu código
2. **Commits frequentes são seus amigos** - é mais fácil voltar em pequenos passos
3. **A configuração inicial vale o investimento** - user.name, user.email, .gitignore
4. **Repositório remoto é backup automático** - nunca perca código por problemas no HD
5. **Git é essencial para reprodutibilidade** - em Data Science, poder voltar para a versão que funcionava é crítico

# 12. Encerramento e gancho para a próxima aula (script)

Excelente! Você acaba de dar o primeiro passo para um fluxo de trabalho profissional. Agora você tem um repositório Git configurado, sabe fazer commits e push, e entende a estrutura fundamental do controle de versão.

Mas a verdade é que o poder real do Git aparece quando você trabalha em equipe. E mesmo trabalhando sozinho, você vai querer usar branches para experimentar sem medo de quebrar o que já funciona.

Na próxima aula, vamos mergulhar na **colaboração com Git**. Você vai aprender a criar branches para novas features, fazer Pull Requests, participar de code reviews, e trabalhar com forks. Vamos simular um fluxo de trabalho real de equipe de Data Science.

Prepare-se: vamos criar nossa primeira branch para implementar uma feature e abrir um Pull Request. É aqui que o Git brilha de verdade.

Até a próxima aula!
