---
titulo: "Aula 02 – Parte 02: Colaboração com Git - Branches, Pull Requests e Code Review"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 25
prerequisitos:
  - "Python 3.12+"
  - "UV instalado"
  - "Aula 02 - Parte 01 concluída"
  - "Repositório swe4ds-credit-api criado e clonado"
  - "Conta no GitHub"
tags: ["git", "branches", "pull-request", "code-review", "github", "colaboracao"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula, vamos subir mais um degrau na sua jornada com Git e aprender sobre **colaboração**. Se na aula anterior você aprendeu a registrar e rastrear suas próprias mudanças, agora vamos descobrir como trabalhar com outras pessoas - e até consigo mesmo de forma mais organizada.

Sabe aquele momento em que você quer testar uma ideia maluca no código, mas tem medo de quebrar o que já está funcionando? Ou quando você está trabalhando numa feature nova e precisa parar para corrigir um bug urgente? É exatamente para isso que existem branches.

E quando falamos de equipes de Data Science, a história fica ainda mais interessante. Pull Requests e Code Reviews não são apenas burocracia - são ferramentas poderosas para compartilhar conhecimento, evitar bugs em produção e manter a qualidade do código.

Vamos colocar a mão na massa e simular um fluxo real de trabalho colaborativo.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você está trabalhando em um modelo de ML e precisa adicionar uma nova feature. No meio do desenvolvimento, seu colega descobre um bug crítico na função de preprocessamento que está em produção. Vocês dois precisam trabalhar no mesmo repositório, mas em coisas diferentes. Como coordenar isso sem um pisar no código do outro?

**Agitação**: Sem organização, você faz as alterações da feature, ele corrige o bug, vocês tentam juntar tudo e... desastre. Conflitos em todo lugar. Alterações perdidas. Ninguém sabe qual versão é a correta. O código que estava funcionando agora está quebrado. O deploy tem que esperar. O cliente está nervoso. A pressão aumenta.

**Solução**: Com branches, cada pessoa trabalha em sua própria "linha do tempo" isolada. O bug é corrigido em uma branch `fix/preprocessing-bug`, revisado via Pull Request, aprovado por code review, e integrado ao main. Enquanto isso, você continua sua feature em `feature/nova-metrica` sem interferência. Quando terminar, abre seu próprio PR, recebe feedback, ajusta, e integra. Tudo organizado, rastreável, seguro.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Criar** branches para desenvolver features isoladamente
2. **Navegar** entre branches e entender o estado de cada uma
3. **Abrir** um Pull Request no GitHub com descrição adequada
4. **Realizar** code review comentando e aprovando PRs
5. **Integrar** branches via merge após aprovação
6. **Aplicar** boas práticas de colaboração em projetos de Data Science

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Git 2.40+ instalado e configurado
- Python 3.12+
- UV instalado
- Repositório `swe4ds-credit-api` clonado e funcional
- Conta no GitHub
- VS Code ou editor de sua preferência

**Verificação do ambiente:**

```bash
# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Verificar que está no branch main
git branch

# Verificar status limpo
git status

# Garantir que está sincronizado
git pull origin main
```

**Saída esperada de `git branch`:**
```
* main
```

**Checklist de Setup:**
- [ ] Repositório clonado e funcional
- [ ] Branch `main` ativo
- [ ] Status limpo (nothing to commit)
- [ ] Ambiente virtual ativo (`.venv`)

# 5. Visão geral do que já existe no projeto (continuidade)

**Estrutura atual do projeto (após Aula 02 - Parte 01):**
```
swe4ds-credit-api/
├── .git/                 # Histórico Git
├── .gitignore            # Arquivos ignorados
├── .venv/                # Ambiente virtual (ignorado)
├── LICENSE               # Licença MIT
├── README.md             # Documentação atualizada
└── requirements.txt      # Dependências Python
```

**O que faremos nesta aula:**
```
swe4ds-credit-api/
├── .git/
├── .gitignore
├── .venv/
├── LICENSE
├── README.md
├── requirements.txt
└── src/                  # [NOVO] Pasta de código fonte
    ├── __init__.py
    └── data_loader.py    # [NOVO] Módulo de carregamento de dados
```

Vamos criar uma estrutura inicial de código em uma branch separada e integrar via Pull Request.

# 6. Passo a passo (comandos + código)

## Passo 1: Entendendo Branches

**Intenção**: Compreender o conceito de branches antes de usá-los (Excalidraw: Slide 4 - Fluxos de Trabalho em Equipe).

### O que é uma Branch?

Uma **branch** é uma linha de desenvolvimento independente. Imagine como "universos paralelos" onde você pode fazer alterações sem afetar o código principal.

```
main:     A ─── B ─── C ─── D ─── E ─── F (merge)
                       \             /
feature:                G ─── H ─── I
```

- **main**: Branch principal, sempre estável
- **feature**: Branch temporária para desenvolvimento

### Fluxo de Trabalho Típico

1. Criar branch a partir de `main`
2. Desenvolver a feature
3. Fazer commits na branch
4. Abrir Pull Request
5. Passar por code review
6. Fazer merge para `main`
7. Deletar branch de feature

**CHECKPOINT**: Você entende que branches são linhas de desenvolvimento paralelas?

---

## Passo 2: Criando Nossa Primeira Branch

**Intenção**: Criar uma branch para desenvolver a estrutura inicial do projeto.

### 2.1 Verificar Branch Atual

```bash
# Ver todas as branches
git branch

# Ver branch atual (com *)
git branch --show-current
```

### 2.2 Criar e Mudar para Nova Branch

```bash
# Criar branch E mudar para ela (forma recomendada)
git checkout -b feature/estrutura-inicial

# Verificar que mudou
git branch
```

**Saída esperada:**
```
* feature/estrutura-inicial
  main
```

O asterisco (*) indica a branch atual.

### Nomenclatura de Branches

Use prefixos para organizar:

| Prefixo | Uso | Exemplo |
|---------|-----|---------|
| `feature/` | Nova funcionalidade | `feature/modelo-rf` |
| `fix/` | Correção de bug | `fix/null-values` |
| `hotfix/` | Correção urgente | `hotfix/deploy-error` |
| `docs/` | Documentação | `docs/api-guide` |
| `refactor/` | Refatoração | `refactor/data-pipeline` |

**CHECKPOINT**: O comando `git branch` mostra `feature/estrutura-inicial` com asterisco.

---

## Passo 3: Desenvolvendo na Branch

**Intenção**: Criar a estrutura inicial de código do projeto.

### 3.1 Criar Estrutura de Pastas

```bash
# Criar pasta src
mkdir src

# Criar __init__.py (marca como pacote Python)
# Windows PowerShell:
New-Item -Path "src/__init__.py" -ItemType File

# Linux/macOS:
# touch src/__init__.py
```

### 3.2 Criar Módulo data_loader.py

Crie o arquivo `src/data_loader.py`:

```python
"""
Módulo de carregamento e preprocessamento de dados.

Este módulo é responsável por carregar o dataset de inadimplência
de cartão de crédito e preparar os dados para treinamento/inferência.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# URL do dataset UCI Credit Card Default
DATASET_URL = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/"
    "00350/default%20of%20credit%20card%20clients.xls"
)


def load_credit_data(
    filepath: Optional[Path] = None,
    use_cache: bool = True
) -> pd.DataFrame:
    """
    Carrega o dataset de inadimplência de cartão de crédito.
    
    Args:
        filepath: Caminho para arquivo local. Se None, baixa da UCI.
        use_cache: Se True, salva/carrega de cache local.
    
    Returns:
        DataFrame com os dados brutos.
        
    Raises:
        FileNotFoundError: Se filepath especificado não existir.
        ValueError: Se dados estiverem corrompidos.
    """
    cache_path = Path("data/credit_data.parquet")
    
    # Tentar carregar do cache
    if use_cache and cache_path.exists():
        print(f"Carregando dados do cache: {cache_path}")
        return pd.read_parquet(cache_path)
    
    # Carregar de arquivo local ou URL
    if filepath is not None:
        if not filepath.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
        print(f"Carregando dados de: {filepath}")
        df = pd.read_excel(filepath, header=1)
    else:
        print(f"Baixando dados de: {DATASET_URL}")
        df = pd.read_excel(DATASET_URL, header=1)
    
    # Validar dados
    if df.empty:
        raise ValueError("Dataset vazio!")
    
    # Salvar cache
    if use_cache:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(cache_path)
        print(f"Cache salvo em: {cache_path}")
    
    return df


def preprocess_data(
    df: pd.DataFrame,
    target_column: str = "default payment next month",
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, StandardScaler]:
    """
    Preprocessa os dados para treinamento.
    
    Args:
        df: DataFrame com dados brutos.
        target_column: Nome da coluna alvo.
        test_size: Proporção do conjunto de teste.
        random_state: Seed para reprodutibilidade.
    
    Returns:
        Tupla com (X_train, X_test, y_train, y_test, scaler).
    """
    # Remover coluna ID
    df = df.drop(columns=["ID"], errors="ignore")
    
    # Separar features e target
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    # Split treino/teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=test_size, 
        random_state=random_state,
        stratify=y
    )
    
    # Normalizar features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train.values, y_test.values, scaler


def get_feature_names() -> list:
    """
    Retorna os nomes das features do dataset.
    
    Returns:
        Lista com nomes das features.
    """
    return [
        "LIMIT_BAL", "SEX", "EDUCATION", "MARRIAGE", "AGE",
        "PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6",
        "BILL_AMT1", "BILL_AMT2", "BILL_AMT3", "BILL_AMT4", "BILL_AMT5", "BILL_AMT6",
        "PAY_AMT1", "PAY_AMT2", "PAY_AMT3", "PAY_AMT4", "PAY_AMT5", "PAY_AMT6"
    ]


if __name__ == "__main__":
    # Teste rápido do módulo
    print("Testando data_loader...")
    
    # Nota: Descomentar para testar (requer internet)
    # df = load_credit_data()
    # print(f"Shape: {df.shape}")
    # print(f"Colunas: {df.columns.tolist()}")
    
    print("Módulo carregado com sucesso!")
    print(f"Features disponíveis: {len(get_feature_names())}")
```

### 3.3 Atualizar requirements.txt

```bash
# Adicionar novas dependências
uv pip install openpyxl pyarrow

# Regenerar requirements.txt
uv pip freeze > requirements.txt
```

**CHECKPOINT**: Os arquivos `src/__init__.py` e `src/data_loader.py` existem.

---

## Passo 4: Fazendo Commits na Branch

**Intenção**: Registrar as alterações de forma organizada.

```bash
# Verificar status
git status
```

**Saída esperada:**
```
On branch feature/estrutura-inicial
Untracked files:
        src/

Changes not staged for commit:
        modified:   requirements.txt
```

```bash
# Adicionar todos os arquivos novos e modificados
git add .

# Verificar staging
git status

# Commit com mensagem descritiva
git commit -m "feat: adiciona estrutura inicial do projeto

- Cria pasta src/ como pacote Python
- Implementa data_loader.py com funções de ETL
- Adiciona cache em parquet para performance
- Atualiza requirements.txt com openpyxl e pyarrow"
```

**CHECKPOINT**: `git log --oneline` mostra o novo commit na branch.

---

## Passo 5: Publicando a Branch no GitHub

**Intenção**: Enviar a branch para o repositório remoto.

```bash
# Push da branch para o GitHub
# -u configura upstream (só precisa na primeira vez)
git push -u origin feature/estrutura-inicial
```

**Saída esperada:**
```
Enumerating objects: 7, done.
...
To https://github.com/SEU_USUARIO/swe4ds-credit-api.git
 * [new branch]      feature/estrutura-inicial -> feature/estrutura-inicial
Branch 'feature/estrutura-inicial' set up to track remote branch
```

**CHECKPOINT**: No GitHub, você vê a nova branch no dropdown de branches.

---

## Passo 6: Criando um Pull Request

**Intenção**: Solicitar que as alterações sejam revisadas e integradas ao main.

### 6.1 Acessar o GitHub

1. Acesse seu repositório no GitHub
2. Você verá um banner: "feature/estrutura-inicial had recent pushes. Compare & pull request"
3. Clique em **"Compare & pull request"**

### 6.2 Preencher o Pull Request (Excalidraw: Slide 5 - Pull Requests e Revisão de Código)

**Título**: `feat: adiciona estrutura inicial do projeto`

**Descrição** (use este template):

```markdown
## Descrição
Implementa a estrutura inicial do projeto com módulo de carregamento de dados.

## Alterações
- Cria pasta `src/` como pacote Python
- Implementa `data_loader.py` com:
  - `load_credit_data()`: carrega dataset da UCI ou cache local
  - `preprocess_data()`: prepara dados para ML
  - `get_feature_names()`: retorna lista de features
- Adiciona cache em formato Parquet para performance
- Atualiza `requirements.txt`

## Checklist
- [x] Código segue padrões PEP 8
- [x] Funções documentadas com docstrings
- [x] Type hints adicionados
- [x] requirements.txt atualizado

## Testes
- [ ] Testes unitários (será adicionado em aula posterior)

## Screenshots/Logs
N/A (código de backend)
```

Clique em **"Create pull request"**.

**CHECKPOINT**: Pull Request criado e visível na aba "Pull requests".

---

## Passo 7: Code Review (Excalidraw: Slide 6 - Qualidade do Código)

**Intenção**: Entender e praticar o processo de revisão de código.

### O que é Code Review?

Code Review é a prática de ter outra pessoa revisando seu código antes de integrá-lo. Benefícios:

1. **Encontrar bugs** antes de chegarem à produção
2. **Compartilhar conhecimento** entre a equipe
3. **Manter padrões** de qualidade
4. **Documentação viva** através de discussões

### Simulando uma Revisão

Como você provavelmente está sozinho, vamos simular o processo:

1. **Na aba "Files changed"**: Veja as diferenças
2. **Clique em uma linha**: Adicione um comentário
   - Exemplo: "Considerar adicionar tratamento para timeout no download"
3. **Start a review**: Agrupa comentários antes de enviar
4. **Submit review**: Escolha "Approve", "Request changes" ou "Comment"

### Tipos de Comentários

| Tipo | Quando Usar | Exemplo |
|------|-------------|---------|
| Bloqueante | Bug crítico, falha de segurança | "Esta função pode causar SQL injection" |
| Sugestão | Melhoria possível | "Considere usar logging ao invés de print" |
| Pergunta | Entender decisão | "Por que escolheu Parquet ao invés de Pickle?" |
| Elogio | Boa prática | "Excelente uso de type hints!" |

**CHECKPOINT**: Você adicionou pelo menos um comentário de revisão.

---

## Passo 8: Fazendo Merge do Pull Request

**Intenção**: Integrar as alterações ao branch principal.

### 8.1 Aprovar o PR (se ainda não fez)

1. Na aba "Files changed"
2. Clique em "Review changes"
3. Selecione "Approve"
4. Clique em "Submit review"

### 8.2 Merge

1. Volte para a aba "Conversation"
2. Clique em **"Merge pull request"**
3. Clique em **"Confirm merge"**
4. Opcionalmente, clique em **"Delete branch"** (recomendado)

### Estratégias de Merge

| Estratégia | Descrição | Quando Usar |
|------------|-----------|-------------|
| Merge commit | Cria commit de merge | Preservar histórico de branches |
| Squash and merge | Combina commits em um só | Features com muitos commits pequenos |
| Rebase and merge | Reaplica commits linearmente | Histórico linear, sem merges |

**CHECKPOINT**: A branch foi integrada e aparece no histórico do main.

---

## Passo 9: Sincronizando Localmente

**Intenção**: Atualizar seu repositório local com as mudanças do remoto.

```bash
# Voltar para main
git checkout main

# Puxar alterações do remoto
git pull origin main

# Verificar que o código está lá
ls src/

# Deletar branch local (já não é necessária)
git branch -d feature/estrutura-inicial
```

**Saída esperada de `ls src/`:**
```
__init__.py    data_loader.py
```

**CHECKPOINT**: O main local tem os arquivos da feature.

---

## Passo 10: Fluxo Completo Visualizado

**Resumo do que fizemos (Excalidraw: Fluxo Completo):**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         FLUXO DE TRABALHO GIT                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. Criar Branch        2. Desenvolver         3. Push                     │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐              │
│  │ git checkout │      │ código       │      │ git push     │              │
│  │ -b feature/  │ ───► │ git add      │ ───► │ origin       │              │
│  │              │      │ git commit   │      │ feature/     │              │
│  └──────────────┘      └──────────────┘      └──────────────┘              │
│                                                     │                       │
│                                                     ▼                       │
│  6. Pull & Cleanup     5. Merge PR            4. Abrir PR                  │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐              │
│  │ git checkout │      │ GitHub UI    │      │ GitHub UI    │              │
│  │ main         │ ◄─── │ Merge button │ ◄─── │ Compare &    │              │
│  │ git pull     │      │              │      │ pull request │              │
│  └──────────────┘      └──────────────┘      └──────────────┘              │
│                              ▲                       │                      │
│                              │                       ▼                      │
│                        ┌─────────────────────────────────┐                 │
│                        │      CODE REVIEW                │                 │
│                        │  - Revisar alterações           │                 │
│                        │  - Comentar/Sugerir             │                 │
│                        │  - Aprovar ou solicitar mudanças│                 │
│                        └─────────────────────────────────┘                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

# 7. Testes rápidos e validação

**Verificar que main está atualizado:**
```bash
git log --oneline -5
```

Esperado: Ver o merge commit e os commits da feature.

**Verificar que a estrutura está correta:**
```bash
python -c "from src.data_loader import get_feature_names; print(len(get_feature_names()))"
```

Esperado:
```
23
```

**Verificar branches locais:**
```bash
git branch
```

Esperado:
```
* main
```

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas de Colaboração

1. **Uma feature, uma branch**
   - Branches devem ser focadas e curtas
   - Evite branches com múltiplas features não relacionadas
   - **Trade-off**: Mais PRs menores são mais fáceis de revisar que um PR gigante

2. **Pull Requests descritivos**
   - Use templates de PR
   - Descreva O QUE mudou e POR QUE
   - Inclua checklist e screenshots quando aplicável
   - **Trade-off**: Leva mais tempo para escrever, mas economiza perguntas

3. **Code Review construtivo**
   - Seja específico nas sugestões
   - Elogie boas práticas, não apenas critique
   - Pergunte antes de assumir que está errado
   - **Trade-off**: Reviews rápidos demais perdem bugs; lentos demais atrasam entregas

4. **Deletar branches após merge**
   - Mantenha o repositório limpo
   - Branches concluídas não têm utilidade
   - **Trade-off**: Nenhum real - é só boa higiene

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `fatal: A branch named 'X' already exists` | Branch já existe | Use outro nome ou delete com `git branch -D X` |
| `error: Your local changes would be overwritten` | Alterações não commitadas | Commit ou stash antes de trocar de branch |
| `PR não pode ser mergeado` | Conflitos com main | Resolva conflitos (próxima aula) |
| `git push` rejeitado | Branch não existe no remoto | Use `git push -u origin nome-branch` |
| "Base changed since you started review" | Main foi atualizado | Atualize PR: `git pull origin main` na branch |
| `Permission denied` | Sem permissão no repo | Verifique se é colaborador ou faça fork |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Nova Branch para Documentação

1. Crie uma branch `docs/api-usage`
2. Adicione um arquivo `docs/API_USAGE.md` com instruções de uso
3. Faça commit e push
4. Abra um Pull Request
5. Faça merge

**Critério de sucesso**: Arquivo visível no main após merge.

## Exercício Básico 2: Code Review Detalhado

1. Crie uma branch `feature/test-file`
2. Adicione um arquivo Python simples
3. Abra um PR
4. Na revisão, adicione 3 comentários diferentes:
   - Uma sugestão de melhoria
   - Uma pergunta
   - Um elogio
5. Resolva os comentários e faça merge

**Critério de sucesso**: PR com histórico de comentários resolvidos.

## Exercício Avançado: Múltiplas Branches Simultâneas

1. Crie duas branches a partir de main: `feature/a` e `feature/b`
2. Em cada uma, faça alterações em ARQUIVOS DIFERENTES
3. Abra PRs para ambas
4. Faça merge de `feature/a` primeiro
5. Faça merge de `feature/b` depois (deve funcionar sem conflitos)

**Critério de sucesso**: Ambos os PRs mergeados, main com todas as alterações.

# 11. Resultados e Lições

## Como Medir o Sucesso

| Métrica | Como Medir | Valor Esperado |
|---------|------------|----------------|
| Branches criadas | `git branch -a` | Pelo menos 1 feature branch |
| PRs abertos | Aba "Pull requests" no GitHub | Pelo menos 1 PR |
| PRs mergeados | Aba "Pull requests" > Closed | PR mostra "Merged" |
| Code reviews | Histórico do PR | Pelo menos 1 comentário |

## Lições Aprendidas

1. **Branches são baratas** - crie-as livremente para isolar trabalho
2. **PRs são mais que código** - são documentação de decisões
3. **Code review é aprendizado** - tanto para quem revisa quanto para quem é revisado
4. **Merge não é o fim** - delete branches e mantenha repositório limpo
5. **Prática leva à fluência** - no início parece burocracia, depois vira instinto

# 12. Encerramento e gancho para a próxima aula (script)

Perfeito! Agora você domina o fluxo de trabalho colaborativo com Git. Você sabe criar branches, desenvolver isoladamente, abrir Pull Requests e fazer code review. Isso já é suficiente para trabalhar profissionalmente em qualquer equipe de tecnologia.

Mas o que acontece quando duas pessoas editam o MESMO arquivo? Ou quando você precisa pegar apenas um commit específico de outra branch? E se você fizer um commit errado e precisar desfazer?

Na próxima aula, vamos enfrentar essas situações de frente. Vamos simular **merge conflicts** e aprender a resolvê-los sem pânico. Também vamos explorar comandos avançados como `revert`, `reset` e `cherry-pick` - ferramentas que podem salvar seu dia em situações complicadas.

Prepare-se para sujar as mãos com cenários mais desafiadores. É onde você realmente aprende Git!

Até a próxima aula!
