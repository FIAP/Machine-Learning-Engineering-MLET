---
titulo: "Aula 05 – Parte 02: Gerenciando Pacotes - Requirements.txt, SemVer, Poetry e UV"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 15
prerequisitos:
  - "Python 3.12+"
  - "UV instalado"
  - "Aula 05 - Parte 01 concluída"
tags: ["uv", "semver", "pyproject.toml", "lockfile", "dependencies"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos aprender a **gerenciar pacotes de forma profissional**.

Na aula passada, você criou um ambiente virtual e instalou pacotes manualmente com `uv pip install`. Funciona, mas tem um problema: como você garante que outra pessoa instale exatamente as mesmas versões? Como você documenta as dependências do projeto?

A resposta tradicional é o famoso `requirements.txt`. Mas essa solução tem limitações sérias que vamos discutir. Vamos entender **versionamento semântico** - o que significa quando você vê `pandas>=2.0,<3.0`. E vamos configurar o UV para gerenciar dependências de forma moderna usando `pyproject.toml` e lockfiles.

Ao final, nosso projeto de crédito terá dependências declaradas, versionadas e travadas - qualquer pessoa poderá reproduzir exatamente o mesmo ambiente.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você desenvolveu um modelo de ML fantástico. Funciona perfeitamente no seu computador. Você manda para o colega rodar, ele instala as dependências e... não funciona. "Mas eu segui o requirements.txt!", ele reclama.

**Agitação**: O requirements.txt dizia `pandas`. Sem versão. Você tinha pandas 1.5.3, ele instalou 2.1.0 (a mais recente). Uma função mudou de comportamento. O modelo não carrega. Vocês gastam horas debugando até descobrir que é incompatibilidade de versão. Você corrige: `pandas==1.5.3`. Funciona... até que 6 meses depois uma dependência do pandas precisa de atualização de segurança, e ela conflita com a versão travada. Dependency hell de novo.

**Solução**: Gerenciamento de dependências moderno. Em vez de travar versões exatas cegamente, você define **ranges de versão** usando versionamento semântico. Um **lockfile** registra as versões exatas que funcionam juntas. Quando precisar atualizar, você atualiza o lockfile de forma controlada. O UV faz tudo isso de forma integrada e rápida.

Nosso projeto de crédito vai sair do `requirements.txt` artesanal para um `pyproject.toml` profissional com UV.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Explicar** as limitações do requirements.txt tradicional
2. **Interpretar** versionamento semântico (Major.Minor.Patch)
3. **Configurar** dependências no pyproject.toml com UV
4. **Diferenciar** dependências de produção e desenvolvimento
5. **Gerar** e usar lockfiles para reprodutibilidade
6. **Sincronizar** ambientes com `uv sync`

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- UV instalado e funcionando
- Ambiente virtual criado na aula anterior

**Verificar ambiente:**

```bash
# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Verificar UV
uv --version

# Ativar ambiente
.\.venv\Scripts\Activate.ps1

# Verificar que está no ambiente correto
where python
```

**Checklist:**
- [ ] UV funcionando
- [ ] Ambiente virtual ativado
- [ ] Terminal no diretório do projeto

# 5. Visão geral do que já existe no projeto (continuidade)

**Estado atual:**
```
swe4ds-credit-api/
├── .venv/                      # [NOVO] Ambiente virtual
├── pyproject.toml              # Existe - vamos melhorar
├── requirements.txt            # Existe - vamos substituir
└── ...
```

**O que vamos modificar:**
```
swe4ds-credit-api/
├── pyproject.toml              # [MODIFICAR] Adicionar dependências UV
├── uv.lock                     # [NOVO] Lockfile do UV
├── requirements.txt            # [REMOVER] Substituído pelo UV
└── ...
```

# 6. Passo a passo (comandos + código)

## Passo 1: Limitações do requirements.txt (Excalidraw: Slide 3)

**Intenção**: Consolidar a teoria de versionamento e reprodutibilidade.

### O que o requirements.txt NÃO resolve

Mesmo com versões fixadas, ele não descreve **o grafo de dependências** completo:

```
fastapi
└── starlette
    └── anyio
    └── idna
```

Sem um lockfile, cada instalação pode resolver versões diferentes dessas dependências transitivas.

### Limitações conceituais

1. **Sem contexto de ambiente**: não diferencia dev, test e prod
2. **Sem histórico de resolução**: não guarda o “conjunto exato” que funcionou
3. **Sem política de atualização**: não define como evoluir versões com segurança

### O papel do pyproject + lockfile

```
pyproject.toml (intenção: ranges)
    ↓
uv.lock (realidade: versões exatas)
    ↓
.venv   (ambiente reproduzível)
```

**CHECKPOINT**: Você entende por que o requirements.txt é insuficiente para reprodutibilidade real.

---

## Passo 2: Versionamento Semântico (SemVer) (Excalidraw: Slide 4)

**Intenção**: Entender a teoria por trás de ranges seguros.

### O que o SemVer garante (e o que NÃO garante)

```
MAJOR.MINOR.PATCH
```

- **PATCH**: correções compatíveis
- **MINOR**: novas features compatíveis
- **MAJOR**: mudanças incompatíveis

Mas atenção: nem todo projeto segue SemVer corretamente. Por isso, ranges são **política de risco**, não garantia absoluta.

### Estratégia de risco controlado

```
pacote>=MAJOR.MINOR,<MAJOR+1
```

Isso permite correções e features sem quebrar a API principal. O lockfile registra a versão específica que foi testada.

**CHECKPOINT**: Você consegue justificar por que usamos ranges + lockfile.

---

## Passo 3: Inicializando Projeto UV (Excalidraw: Slide 3)

**Intenção**: Configurar o projeto para usar UV nativamente.

```bash
# Garantir que está no diretório do projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Inicializar projeto UV (se ainda não tem pyproject.toml configurado)
uv init --name swe4ds-credit-api
```

Se já existe pyproject.toml, vamos editá-lo. Veja o conteúdo atual:

```bash
cat pyproject.toml
```

### Estrutura do pyproject.toml para UV

Crie ou atualize `pyproject.toml`:

```toml
[project]
name = "swe4ds-credit-api"
version = "0.1.0"
description = "API de análise de crédito para o curso SWE4DS"
readme = "README.md"
requires-python = ">=3.12"

# Dependências de produção
dependencies = [
    "pandas>=2.0,<3.0",
    "numpy>=1.24,<2.0",
    "scikit-learn>=1.3,<2.0",
    "pydantic>=2.0,<3.0",
]

[project.optional-dependencies]
# Dependências de desenvolvimento
dev = [
    "pytest>=7.0,<9.0",
    "pytest-cov>=4.0,<6.0",
    "ruff>=0.1,<1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
# Configurações específicas do UV
dev-dependencies = [
    "pytest>=7.0,<9.0",
    "pytest-cov>=4.0,<6.0",
    "ruff>=0.1,<1.0",
    "taskipy>=1.12,<2.0",
]
```

### Explicação das Seções

| Seção | Propósito |
|-------|-----------|
| `[project]` | Metadados do projeto (nome, versão, descrição) |
| `dependencies` | Pacotes necessários para rodar |
| `[project.optional-dependencies]` | Grupos opcionais (dev, test, docs) |
| `[tool.uv]` | Configurações específicas do UV |
| `dev-dependencies` | Dependências de desenvolvimento (UV específico) |

**CHECKPOINT**: `pyproject.toml` criado/atualizado com estrutura correta.

---

## Passo 4: Adicionando Dependências com UV (Excalidraw: Slide 3)

**Intenção**: Usar comandos UV para gerenciar pacotes.

### Adicionar Dependência de Produção

```bash
# Adicionar uma dependência
uv add fastapi

# Adicionar com versão específica
uv add "uvicorn>=0.24,<1.0"

# Adicionar múltiplas
uv add httpx python-dotenv
```

### Adicionar Dependência de Desenvolvimento

```bash
# Flag --dev para dependências de desenvolvimento
uv add --dev pytest
uv add --dev ruff
uv add --dev taskipy
```

### Ver o que foi adicionado

```bash
# Verificar pyproject.toml
cat pyproject.toml

# Verificar lockfile gerado
cat uv.lock | head -50
```

**Saída esperada no pyproject.toml:**
```toml
[project]
dependencies = [
    "fastapi>=0.115.6",
    "httpx>=0.28.1",
    # ...
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.3.4",
    "ruff>=0.9.2",
    # ...
]
```

**CHECKPOINT**: Dependências adicionadas e visíveis no pyproject.toml.

---

## Passo 5: Entendendo o Lockfile (Excalidraw: Slide 4)

**Intenção**: Compreender o papel do lockfile na reprodutibilidade.

### O que é uv.lock?

```bash
# Visualizar parte do lockfile
cat uv.lock | head -100
```

**Estrutura típica:**
```toml
version = 1
requires-python = ">=3.12"

[[package]]
name = "fastapi"
version = "0.115.6"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "pydantic" },
    { name = "starlette" },
    # ...
]

[[package]]
name = "pandas"
version = "2.1.4"
source = { registry = "https://pypi.org/simple" }
# ...
```

### Lockfile vs pyproject.toml

| Arquivo | Propósito | Editável? |
|---------|-----------|-----------|
| `pyproject.toml` | Declara o que você QUER | Sim, manualmente |
| `uv.lock` | Registra o que foi RESOLVIDO | Não, gerado pelo UV |

### Fluxo de Trabalho

```
pyproject.toml (ranges)
        │
        ▼ uv lock
    uv.lock (versões exatas)
        │
        ▼ uv sync
    .venv/ (instalado)
```

**CHECKPOINT**: Você entende que o lockfile registra versões exatas resolvidas.

---

## Passo 6: Sincronizando Ambiente (Excalidraw: Slide 4)

**Intenção**: Instalar todas as dependências de uma vez.

```bash
# Sincronizar ambiente com lockfile
uv sync

# Incluir dependências de desenvolvimento
uv sync --dev

# Verificar pacotes instalados
uv pip list
```

**Saída esperada:**
```
Resolved 42 packages in 0.5s
Installed 42 packages in 1.2s
 + fastapi==0.115.6
 + pandas==2.1.4
 + pytest==8.3.4
 ...
```

### Verificar que funciona

```bash
# Testar import
python -c "import fastapi; import pandas; import pytest; print('Tudo importado!')"
```

**CHECKPOINT**: `uv sync` instala todas as dependências corretamente.

---

## Passo 7: Comandos Essenciais do UV

**Intenção**: Dominar os comandos do dia a dia.

### Referência Rápida

```bash
# Adicionar dependência
uv add pacote
uv add "pacote>=1.0,<2.0"
uv add --dev pacote-dev

# Remover dependência
uv remove pacote

# Atualizar dependência
uv add pacote@latest  # Atualiza para mais recente dentro do range

# Atualizar lockfile (após editar pyproject.toml manualmente)
uv lock

# Sincronizar ambiente
uv sync
uv sync --dev  # Inclui dev dependencies

# Executar comando no ambiente
uv run python script.py
uv run pytest

# Listar pacotes
uv pip list
uv pip show pacote

# Exportar para requirements.txt (compatibilidade)
uv pip compile pyproject.toml -o requirements.txt
```

### Quando usar cada comando

| Situação | Comando |
|----------|---------|
| Adicionar nova biblioteca | `uv add nome` |
| Adicionar ferramenta de dev | `uv add --dev nome` |
| Clonou o projeto | `uv sync --dev` |
| Atualizar dependências | `uv lock --upgrade` |
| Executar script | `uv run python script.py` |

**CHECKPOINT**: Você conhece os comandos essenciais do UV.

---

## Passo 8: Removendo requirements.txt

**Intenção**: Migrar completamente para UV.

```bash
# Se ainda existe requirements.txt, podemos removê-lo
# (o UV agora é a fonte de verdade)

# Backup opcional
mv requirements.txt requirements.txt.old

# Ou deletar
rm requirements.txt
```

### Atualizar Documentação

Atualize o README.md do projeto para refletir o novo setup:

```markdown
## Setup do Ambiente

### Pré-requisitos
- Python 3.12+
- UV (instalador de pacotes)

### Instalação

```bash
# Instalar UV (se ainda não tem)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clonar o projeto
git clone <repo>
cd swe4ds-credit-api

# Criar ambiente e instalar dependências
uv sync --dev
```

### Executar

```bash
# Rodar testes
uv run pytest

# Rodar script
uv run python scripts/download_data.py
```
```

**CHECKPOINT**: requirements.txt removido, README atualizado.

# 7. Testes rápidos e validação

```bash
# Verificar pyproject.toml está válido
uv lock --check

# Sincronizar ambiente
uv sync --dev

# Testar imports
python -c "
import pandas
import numpy
import sklearn
import fastapi
import pytest
print('Todas as dependências instaladas corretamente!')
"

# Rodar testes
uv run pytest tests/ -v

# Verificar versões
uv pip list | grep -E "pandas|fastapi|pytest"
```

**Saída esperada dos imports:**
```
Todas as dependências instaladas corretamente!
```

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas de Gerenciamento de Dependências

1. **Use ranges de versão, não exatas**
   - `pandas>=2.0,<3.0` em vez de `pandas==2.0.3`
   - Permite atualizações de segurança dentro do major
   - **Trade-off**: Menos controle, mas mais flexibilidade

2. **Sempre commite o lockfile**
   - `uv.lock` deve ir para o git
   - Garante reprodutibilidade exata
   - **Trade-off**: Arquivo grande, mas essencial

3. **Separe dependências dev/prod**
   - Testes e linters não vão para produção
   - Reduz tamanho da imagem Docker
   - **Trade-off**: Mais configuração, mas deploy mais limpo

4. **Documente a versão mínima do Python**
   - `requires-python = ">=3.12"` no pyproject.toml
   - Evita erros de sintaxe em versões antigas
   - **Trade-off**: Pode excluir contribuidores com Python antigo

5. **Atualize regularmente**
   - `uv lock --upgrade` periodicamente
   - Patches de segurança são importantes
   - **Trade-off**: Pode introduzir bugs, teste após atualizar

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `No solution found` | Conflito de versões | Relaxar ranges, verificar compatibilidade |
| `Package not found` | Nome errado ou PyPI indisponível | Verificar nome exato no PyPI |
| `uv.lock out of date` | pyproject.toml editado manualmente | `uv lock` para atualizar |
| `Module not found` | Ambiente não sincronizado | `uv sync` |
| Versão errada instalada | Lockfile desatualizado | `uv lock --upgrade`, `uv sync` |
| Hash mismatch | Cache corrompido | `uv cache clean`, `uv sync` |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Adicionar Dependência

Adicione a biblioteca `httpx` (cliente HTTP moderno) como dependência de produção e `black` como dependência de desenvolvimento. Verifique que ambas aparecem nas seções corretas do pyproject.toml.

**Critério de sucesso**: `uv pip list` mostra ambos pacotes, pyproject.toml tem separação correta.

## Exercício Básico 2: Recriar Ambiente

Delete a pasta `.venv/` completamente e recrie o ambiente usando apenas `uv sync --dev`. Verifique que todas as dependências são instaladas corretamente.

**Critério de sucesso**: Ambiente recriado funcional sem intervenção manual.

## Exercício Avançado: Análise de Dependências

Use `uv pip show pandas` para ver as dependências do pandas. Depois, examine o `uv.lock` e identifique todas as dependências transitivas que o pandas trouxe. Documente a árvore de dependências.

**Critério de sucesso**: Documento mostrando pandas → suas dependências → dependências das dependências.

# 11. Resultados e Lições

## Métricas para Acompanhar

| Métrica | Como medir | Valor esperado |
|---------|------------|----------------|
| Tempo de sync | `Measure-Command { uv sync }` | < 5 segundos |
| Número de dependências | `uv pip list \| wc -l` | ~30-50 pacotes |
| Tamanho do lockfile | `(Get-Item uv.lock).Length / 1KB` | ~50-100 KB |
| Reprodutibilidade | Deletar .venv, sync, testar | 100% funcional |

## Lições desta Aula

1. **requirements.txt é limitado** - Sem lockfile, sem separação dev/prod
2. **SemVer é contrato** - MAJOR.MINOR.PATCH tem significado
3. **Ranges são melhores que exatas** - Permitem atualizações seguras
4. **Lockfile é a fonte de verdade** - Versões exatas resolvidas
5. **UV simplifica tudo** - Um comando para cada tarefa

# 12. Encerramento e gancho para a próxima aula (script)

Excelente! Agora você entende versionamento semântico e sabe gerenciar dependências de forma profissional com UV. Seu projeto tem um `pyproject.toml` bem estruturado e um `uv.lock` que garante reprodutibilidade.

Na próxima aula, vamos colocar a mão na massa de verdade. Vamos configurar:
- **Taskipy** para automação de comandos
- **Pytest** integrado ao workflow
- **Ruff** para linting e formatação

Você vai ver como essas ferramentas se integram no dia a dia de desenvolvimento e como configurar scripts no pyproject.toml para rodar tudo com comandos simples como `uv run task test` ou `uv run task lint`.

Até a próxima aula!
