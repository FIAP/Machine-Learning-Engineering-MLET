---
titulo: "Aula 02 – Parte 03: Git Avançado na Prática - Merge Conflicts e Comandos Poderosos"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 30
prerequisitos:
  - "Python 3.12+"
  - "UV instalado"
  - "Aula 02 - Partes 01 e 02 concluídas"
  - "Repositório swe4ds-credit-api com estrutura inicial"
tags: ["git", "merge-conflict", "revert", "reset", "cherry-pick", "rebase", "avancado"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula, vamos enfrentar os momentos mais temidos por quem está começando com Git: os **conflitos de merge**. E vou te contar um segredo: eles parecem assustadores, mas são completamente gerenciáveis quando você entende o que está acontecendo.

Além disso, vamos explorar comandos avançados que vão te dar superpoderes no Git. Comandos como `revert`, `reset` e `cherry-pick` não são usados todo dia, mas quando você precisa deles, eles salvam seu projeto.

Esta é uma aula prática e intensa. Vamos simular problemas reais e resolvê-los juntos. Ao final, você vai olhar para conflitos de merge não com medo, mas com confiança.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você e seu colega estão trabalhando em branches separadas, mas ambos precisaram modificar o mesmo arquivo - o `data_loader.py`. Ele adicionou tratamento de erro, você otimizou uma função. Na hora de integrar, o Git grita: "CONFLICT!". O terminal fica vermelho. Você não sabe o que fazer.

**Agitação**: Você tenta resolver, mas acaba apagando o código do colega. Ele fica chateado. Vocês tentam de novo, dessa vez apagando seu código. O prazo está chegando. A frustração aumenta. Alguém sugere "apagar tudo e começar de novo". Parece que o Git está trabalhando contra vocês.

**Solução**: Conflitos são naturais e esperados. O Git está pedindo uma decisão humana porque duas pessoas editaram a mesma região do código. Você aprende a ler os marcadores de conflito, usar ferramentas visuais para comparar, decidir qual código manter (ou combinar os dois), e finalizar o merge. Em 5 minutos, o que parecia impossível está resolvido. Vocês aprendem a comunicar melhor sobre quem está editando o quê. Conflitos se tornam raros e triviais.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Identificar** a causa de merge conflicts e quando eles ocorrem
2. **Resolver** conflitos manualmente usando marcadores do Git
3. **Utilizar** ferramentas visuais de diff para facilitar a resolução
4. **Aplicar** `git revert` para desfazer commits mantendo histórico
5. **Usar** `git reset` com segurança para reorganizar commits locais
6. **Aplicar** `git cherry-pick` para selecionar commits específicos
7. **Manter** um histórico limpo com boas práticas de commits

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Git 2.40+ instalado e configurado
- Python 3.12+
- UV instalado
- Repositório `swe4ds-credit-api` com estrutura da aula anterior
- VS Code com extensão GitLens (recomendado)

**Instalação do GitLens (opcional, mas recomendado):**

No VS Code:
1. Ctrl+Shift+X (abrir extensões)
2. Buscar "GitLens"
3. Instalar "GitLens — Git supercharged"

**Verificação do ambiente:**

```bash
# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Verificar branch e status
git branch
git status

# Garantir que está atualizado
git checkout main
git pull origin main
```

**Checklist de Setup:**
- [ ] Repositório atualizado no main
- [ ] Status limpo (nothing to commit)
- [ ] GitLens instalado (opcional)
- [ ] Ambiente virtual ativo

# 5. Visão geral do que já existe no projeto (continuidade)

**Estrutura atual (após Aula 02 - Parte 02):**
```
swe4ds-credit-api/
├── .git/
├── .gitignore
├── .venv/
├── LICENSE
├── README.md
├── requirements.txt
└── src/
    ├── __init__.py
    └── data_loader.py      # Vamos provocar conflitos aqui
```

**O que faremos nesta aula:**
- Simular um conflito de merge em `data_loader.py`
- Resolver o conflito
- Praticar comandos avançados

# 6. Passo a passo (comandos + código)

## Passo 1: Entendendo Merge Conflicts (Excalidraw: Slide 7 - Merge Conflicts)

**Intenção**: Entender por que e quando conflitos acontecem.

### Quando Conflitos NÃO Acontecem

Conflitos NÃO ocorrem quando:
- Duas pessoas editam **arquivos diferentes**
- Duas pessoas editam **regiões diferentes** do mesmo arquivo
- Apenas uma pessoa editou o arquivo desde a divisão

### Quando Conflitos ACONTECEM

Conflitos ocorrem quando:
- Duas branches editam a **mesma linha** do mesmo arquivo
- Git não consegue decidir automaticamente qual versão usar

```
main:     A ─── B ─── C ─────────────── ? (conflito!)
                       \               /
feature:                D (edita L10) 
                              \
main (C):                      E (também edita L10)
```

Quando você tenta fazer merge, Git pergunta: "Qual versão da linha 10 você quer?"

**CHECKPOINT**: Você entende que conflitos são pedidos de decisão, não erros?

---

## Passo 2: Simulando um Conflito

**Intenção**: Criar intencionalmente um cenário de conflito para praticar.

### 2.1 Criar Branch de Simulação A

```bash
# Criar primeira branch de simulação
git checkout -b feature/conflict-simulation-a

# Editar data_loader.py
```

Edite `src/data_loader.py` - altere a constante DATASET_URL (linha ~15):

```python
# ANTES:
DATASET_URL = (
    "https://archive.ics.uci.edu/ml/machine-learning-databases/"
    "00350/default%20of%20credit%20card%20clients.xls"
)

# DEPOIS (na branch A):
DATASET_URL = (
    "https://archive.ics.uci.edu/static/public/"
    "350/default+of+credit+card+clients.zip"
)
```

```bash
# Commit na branch A
git add src/data_loader.py
git commit -m "feat: atualiza URL para novo endpoint UCI"
```

### 2.2 Voltar ao Main e Criar Branch B

```bash
# Voltar ao main
git checkout main

# Criar segunda branch (a partir do main, sem as mudanças de A)
git checkout -b feature/conflict-simulation-b

# Editar a MESMA região do arquivo
```

Edite `src/data_loader.py` - altere a mesma constante de forma DIFERENTE:

```python
# DEPOIS (na branch B):
DATASET_URL = (
    "https://raw.githubusercontent.com/dados-ml/"
    "credit-default/main/data.csv"
)
```

```bash
# Commit na branch B
git add src/data_loader.py
git commit -m "feat: usa mirror do dataset no GitHub"
```

### 2.3 Fazer Merge da Branch A no Main

```bash
# Voltar ao main
git checkout main

# Merge da branch A (sem conflitos, main não mudou)
git merge feature/conflict-simulation-a
```

**Saída esperada:**
```
Updating abc123..def456
Fast-forward
 src/data_loader.py | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
```

### 2.4 Tentar Merge da Branch B (CONFLITO!)

```bash
# Agora tentar merge da branch B
git merge feature/conflict-simulation-b
```

**Saída esperada:**
```
Auto-merging src/data_loader.py
CONFLICT (content): Merge conflict in src/data_loader.py
Automatic merge failed; fix conflicts and then commit the result.
```

**CHECKPOINT**: Você provocou um conflito com sucesso!

---

## Passo 3: Anatomia de um Conflito

**Intenção**: Entender os marcadores de conflito do Git.

```bash
# Ver status durante conflito
git status
```

**Saída:**
```
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   src/data_loader.py
```

Abra `src/data_loader.py`. Você verá algo assim:

```python
<<<<<<< HEAD
DATASET_URL = (
    "https://archive.ics.uci.edu/static/public/"
    "350/default+of+credit+card+clients.zip"
)
=======
DATASET_URL = (
    "https://raw.githubusercontent.com/dados-ml/"
    "credit-default/main/data.csv"
)
>>>>>>> feature/conflict-simulation-b
```

### Entendendo os Marcadores

| Marcador | Significado |
|----------|-------------|
| `<<<<<<< HEAD` | Início do código da branch atual (main) |
| `=======` | Separador entre as versões |
| `>>>>>>> feature/...` | Fim do código da branch sendo mergeada |

O Git está dizendo: "Eu encontrei duas versões diferentes. Você decide qual usar."

**CHECKPOINT**: Você consegue identificar as duas versões no conflito?

---

## Passo 4: Resolvendo o Conflito (Excalidraw: Slide 8 - Comandos Avançados)

**Intenção**: Resolver o conflito manualmente.

### Opção 1: Manter Apenas uma Versão

Para manter a versão do main (HEAD):
```python
# Remova TUDO entre <<<<<<< e >>>>>>> e mantenha apenas:
DATASET_URL = (
    "https://archive.ics.uci.edu/static/public/"
    "350/default+of+credit+card+clients.zip"
)
```

### Opção 2: Manter a Outra Versão

Para manter a versão da branch:
```python
DATASET_URL = (
    "https://raw.githubusercontent.com/dados-ml/"
    "credit-default/main/data.csv"
)
```

### Opção 3: Combinar as Duas (Nossa Escolha)

Muitas vezes a melhor solução é combinar:

```python
# URL primária (UCI oficial)
DATASET_URL_PRIMARY = (
    "https://archive.ics.uci.edu/static/public/"
    "350/default+of+credit+card+clients.zip"
)

# URL de fallback (mirror GitHub)
DATASET_URL_FALLBACK = (
    "https://raw.githubusercontent.com/dados-ml/"
    "credit-default/main/data.csv"
)

# URL padrão
DATASET_URL = DATASET_URL_PRIMARY
```

**IMPORTANTE**: Remova TODOS os marcadores (`<<<<<<<`, `=======`, `>>>>>>>`).

### Finalizando a Resolução

```bash
# Adicionar arquivo resolvido
git add src/data_loader.py

# Verificar status
git status

# Commit de merge
git commit -m "merge: combina URLs do dataset com fallback

Resolve conflito entre feature/conflict-simulation-a e 
feature/conflict-simulation-b combinando as duas abordagens:
- URL primária: UCI oficial (novo endpoint)
- URL fallback: mirror no GitHub para redundância"
```

**CHECKPOINT**: `git log --oneline` mostra o merge commit.

---

## Passo 5: Usando Ferramentas Visuais

**Intenção**: Mostrar alternativas mais amigáveis para resolver conflitos.

### VS Code como Ferramenta de Merge

Quando você abre um arquivo com conflito no VS Code:
- Você vê botões: "Accept Current Change", "Accept Incoming Change", "Accept Both Changes"
- Clique no que preferir ou edite manualmente

### Git Mergetool

Configure uma ferramenta visual:

```bash
# Configurar VS Code como mergetool
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# Usar durante conflito
git mergetool
```

### GitLens no VS Code

Se você instalou GitLens:
- Mostra side-by-side comparison
- Highlighting colorido das diferenças
- Atalhos para aceitar versões

---

## Passo 6: Git Revert - Desfazendo Commits com Segurança

**Intenção**: Aprender a desfazer commits mantendo o histórico intacto.

### Quando Usar Revert

- Commit já foi publicado (pushed)
- Você precisa manter rastreabilidade
- Desfazer uma mudança específica

```bash
# Criar algo para reverter
git checkout -b feature/will-revert

# Adicionar um arquivo "errado"
echo "Este arquivo não deveria existir" > arquivo_errado.py
git add arquivo_errado.py
git commit -m "feat: adiciona arquivo (vai ser revertido)"

# Ver o histórico
git log --oneline -3

# Reverter o último commit
git revert HEAD
```

O Git abre um editor para a mensagem do revert. Salve e feche.

```bash
# Verificar que o arquivo sumiu
ls arquivo_errado.py
# Erro: arquivo não existe

# Ver histórico - o revert aparece como novo commit
git log --oneline -3
```

**Saída esperada:**
```
abc1234 Revert "feat: adiciona arquivo (vai ser revertido)"
def5678 feat: adiciona arquivo (vai ser revertido)
ghi9012 merge: combina URLs do dataset com fallback
```

**IMPORTANTE**: O commit original ainda existe no histórico! Revert cria um NOVO commit que desfaz as mudanças.

---

## Passo 7: Git Reset - Reescrevendo Histórico Local

**Intenção**: Entender reset e seus modos (Excalidraw: Slide 8 - Revert e Reset).

### Modos do Reset

| Modo | Flag | Working Dir | Staging | Commits |
|------|------|-------------|---------|---------|
| Soft | `--soft` | Mantém | Mantém | Remove |
| Mixed | (padrão) | Mantém | Limpa | Remove |
| Hard | `--hard` | Limpa | Limpa | Remove |

### Soft Reset - Desfazer commit, manter tudo

```bash
# Criar commits para testar
echo "teste 1" > teste1.txt
git add teste1.txt
git commit -m "test: commit 1"

echo "teste 2" > teste2.txt
git add teste2.txt
git commit -m "test: commit 2"

# Ver histórico
git log --oneline -4

# Soft reset: volta 1 commit, mantém mudanças staged
git reset --soft HEAD~1

# Verificar: arquivo ainda existe e está staged
git status
```

### Mixed Reset - Desfazer commit e staging

```bash
# Commit novamente
git commit -m "test: commit 2 (again)"

# Mixed reset: volta 1 commit, mantém arquivo mas remove do staging
git reset HEAD~1

# Verificar: arquivo existe mas NÃO está staged
git status
```

### Hard Reset - Apagar tudo (CUIDADO!)

```bash
# Adicionar e commitar
git add teste2.txt
git commit -m "test: commit 2 (final)"

# Hard reset: APAGA tudo
git reset --hard HEAD~1

# Verificar: arquivo SUMIU
ls teste2.txt
# Erro: arquivo não existe
```

**CUIDADO**: `git reset --hard` é destrutivo! Use apenas em commits LOCAIS.

---

## Passo 8: Git Cherry-Pick - Selecionando Commits

**Intenção**: Pegar commits específicos de outras branches.

### Cenário

Você tem uma branch experimental com vários commits. Apenas UM deles é útil. Em vez de fazer merge de tudo, você "pega" só aquele commit.

```bash
# Voltar ao main e limpar
git checkout main
git branch -D feature/will-revert

# Criar branch experimental
git checkout -b experimental/varios-testes

# Vários commits
echo "experimento 1" > exp1.txt
git add exp1.txt
git commit -m "exp: teste 1 (não queremos)"

echo "funcionalidade útil" > util.txt
git add util.txt
git commit -m "feat: funcionalidade útil (QUEREMOS!)"

echo "experimento 2" > exp2.txt
git add exp2.txt
git commit -m "exp: teste 2 (não queremos)"

# Ver hashes
git log --oneline -3
```

Anote o hash do commit "feat: funcionalidade útil".

```bash
# Voltar ao main
git checkout main

# Cherry-pick apenas o commit útil
git cherry-pick <HASH_DO_COMMIT_UTIL>
```

**Saída esperada:**
```
[main abc1234] feat: funcionalidade útil (QUEREMOS!)
 1 file changed, 1 insertion(+)
 create mode 100644 util.txt
```

```bash
# Verificar: apenas util.txt veio
ls *.txt
# Apenas util.txt (exp1.txt e exp2.txt NÃO vieram)

# Limpar branch experimental
git branch -D experimental/varios-testes
```

**CHECKPOINT**: O arquivo `util.txt` existe no main, mas `exp1.txt` e `exp2.txt` não.

---

## Passo 9: Boas Práticas para Histórico Limpo (Excalidraw: Slide 9 - Melhores Práticas)

**Intenção**: Manter um histórico Git navegável e útil.

### Amend - Corrigir o Último Commit

Esqueceu algo no último commit?

```bash
# Fazer alteração esquecida
echo "# Comentário faltando" >> util.txt

# Adicionar ao MESMO commit (sem criar novo)
git add util.txt
git commit --amend --no-edit

# Ou para também mudar a mensagem:
git commit --amend -m "feat: funcionalidade útil com documentação"
```

**IMPORTANTE**: Só use amend em commits NÃO publicados!

### Squash - Combinar Commits

Durante um rebase interativo, você pode combinar vários commits em um:

```bash
# Rebase interativo dos últimos 3 commits
git rebase -i HEAD~3

# No editor, marque commits como 'squash' ou 's'
# Primeiro commit fica 'pick', outros ficam 'squash'
```

### Mensagens de Commit de Qualidade

```bash
# RUIM
git commit -m "fix"
git commit -m "update"
git commit -m "wip"

# BOM
git commit -m "fix: corrige divisão por zero em preprocess_data

O cálculo de média falhava quando dataset estava vazio.
Adiciona verificação de len(df) > 0 antes da operação.

Closes #42"
```

# 7. Testes rápidos e validação

**Verificar que conflito foi resolvido:**
```bash
git log --oneline --graph -10
```

Esperado: Ver o merge commit sem indicação de conflito pendente.

**Verificar que revert funcionou:**
```bash
git log --oneline | grep -i revert
```

Esperado: Ver commits de revert se você os criou.

**Verificar cherry-pick:**
```bash
ls util.txt && echo "Cherry-pick funcionou!"
```

Esperado: "Cherry-pick funcionou!"

**Testar que o código ainda funciona:**
```bash
python -c "from src.data_loader import get_feature_names; print('OK:', len(get_feature_names()))"
```

Esperado: `OK: 23`

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas Aplicadas

1. **Resolver conflitos cedo**
   - Não deixe branches divergirem por muito tempo
   - Faça pull do main frequentemente na sua branch
   - **Trade-off**: Mais trabalho contínuo, menos dor na integração

2. **Use revert, não reset, para commits públicos**
   - Revert mantém histórico transparente
   - Reset reescreve história (ruim para colaboração)
   - **Trade-off**: Histórico mais longo, mas mais seguro

3. **Cherry-pick com moderação**
   - Útil para hotfixes urgentes
   - Pode causar commits duplicados se não for cuidadoso
   - **Trade-off**: Flexibilidade vs. histórico confuso

4. **Commits atômicos e focados**
   - Cada commit deve ser uma unidade lógica
   - Facilita cherry-pick, revert e bisect
   - **Trade-off**: Mais commits, mas mais granularidade

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `CONFLICT` em arquivo que você não editou | Mudanças em branches ancestrais | Aceite uma versão ou combine manualmente |
| `error: You have not concluded your merge` | Merge não finalizado | `git merge --abort` para cancelar ou resolva e commit |
| `Cannot revert: your index contains uncommitted changes` | Arquivos não commitados | Commit ou stash antes de revert |
| `fatal: bad revision 'HEAD~3'` | Não há commits suficientes | Use número menor ou hash específico |
| `error: could not apply <hash>` | Cherry-pick com conflito | Resolva conflito como em merge |
| `warning: refname 'HEAD~1' is ambiguous` | Sintaxe problemática | Use `git log` para pegar hash exato |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Resolver Conflito Proposital

1. Crie duas branches a partir de main
2. Edite a MESMA linha do README.md em ambas
3. Faça merge de uma
4. Tente merge da outra (conflito!)
5. Resolva mantendo AMBOS os textos

**Critério de sucesso**: Merge concluído com as duas contribuições.

## Exercício Básico 2: Praticar Revert

1. Faça 3 commits (A, B, C)
2. Reverta o commit B (do meio)
3. Verifique que A e C ainda estão, mas B foi desfeito

**Critério de sucesso**: `git log` mostra commit de revert para B.

## Exercício Avançado: Pipeline de Cherry-Pick

1. Crie branch `experimental/features`
2. Faça 5 commits com features numeradas (1 a 5)
3. Volte ao main
4. Cherry-pick apenas os commits ímpares (1, 3, 5)
5. Verifique que apenas essas features estão no main

**Critério de sucesso**: Main tem features 1, 3, 5 mas não 2, 4.

# 11. Resultados e Lições

## Como Medir o Sucesso

| Métrica | Como Medir | Valor Esperado |
|---------|------------|----------------|
| Conflitos resolvidos | Nenhum arquivo em estado "unmerged" | `git status` limpo |
| Reverts aplicados | `git log --oneline \| grep -i revert` | Reverts listados |
| Cherry-picks bem-sucedidos | Commits aparecem no histórico | Hash correto no log |
| Histórico limpo | `git log --oneline` é legível | Mensagens descritivas |

## Lições Aprendidas

1. **Conflitos são normais** - não entre em pânico, leia os marcadores
2. **Ferramentas visuais ajudam** - VS Code e GitLens simplificam muito
3. **Revert é seguro** - mantém histórico, ideal para commits públicos
4. **Reset é poderoso, mas perigoso** - use apenas em commits locais
5. **Cherry-pick é cirúrgico** - pega exatamente o que você precisa

# 12. Encerramento e gancho para a próxima aula (script)

Fantástico! Você acabou de desbloquear o nível avançado do Git. Conflitos de merge não são mais mistério - você sabe identificar, entender e resolver. E agora tem ferramentas como revert, reset e cherry-pick no seu arsenal.

Com o que aprendemos até aqui, você já consegue trabalhar profissionalmente com código em qualquer equipe. Mas e os dados? E os modelos de Machine Learning?

Na próxima aula, vamos introduzir o **DVC - Data Version Control**. É uma ferramenta que estende o Git para versionar também datasets e modelos. Imagine poder voltar no tempo não só no código, mas também nos dados de treino e nos artefatos do modelo. É isso que o DVC permite.

Vamos ver como integrar DVC ao nosso projeto de API de crédito, versionando o dataset e os modelos de forma que qualquer experimento seja 100% reprodutível.

Prepare-se para dar o próximo passo na reprodutibilidade de projetos de Data Science!

Até a próxima aula!
