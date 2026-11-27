---
titulo: "Aula 05 – Parte 04: Publicando Código Reutilizável - Setup.py e Estrutura de Pacotes"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 15
prerequisitos:
  - "Python 3.12+"
  - "UV instalado"
  - "Aula 05 - Partes 01 a 03 concluídas"
tags: ["packaging", "setup.py", "pyproject.toml", "pip", "distribution"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Essa é a última aula do módulo de gerenciamento de dependências, e vamos fechar com um tema que conecta tudo que você aprendeu: **empacotar código reutilizável**.

Até agora, você criou um projeto Python com ambiente isolado, dependências gerenciadas e ferramentas de qualidade. Mas e se você quiser reutilizar a lógica de validação em outro projeto? E se quiser compartilhar seu código com a equipe de forma que eles possam simplesmente fazer `pip install swe4ds-credit-api`?

Empacotar código Python permite exatamente isso. Você transforma seu projeto em um pacote instalável. Pode ser distribuído internamente, no PyPI (repositório público), ou simplesmente instalado localmente em modo de desenvolvimento.

Nesta aula, vamos entender a estrutura de pacotes Python e configurar nosso projeto para ser instalável. Ao final, você saberá quando e como empacotar código.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você desenvolveu funções de validação excelentes para o projeto de crédito. Agora outro projeto da empresa precisa da mesma lógica. Você copia e cola o código. Meses depois, você descobre um bug na validação. Corrige no projeto original. E no segundo projeto? Continua com o bug.

**Agitação**: Você tem 5 projetos usando código copiado. Cada um tem uma versão levemente diferente. Você não sabe mais qual é a mais recente. Um dia, uma mudança na lógica de negócio requer atualização em todos. Você gasta uma semana atualizando código duplicado. Erros aparecem porque você esqueceu um projeto. O time está frustrado.

**Solução**: Empacotar o código uma vez e instalar como dependência em todos os projetos. Quando corrige um bug, você atualiza o pacote. Cada projeto faz `pip install --upgrade` e todos têm a correção. Versionamento semântico garante compatibilidade. Uma fonte de verdade, múltiplos consumidores.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Explicar** quando vale a pena empacotar código
2. **Estruturar** um projeto Python como pacote instalável
3. **Configurar** metadados no pyproject.toml para distribuição
4. **Instalar** um pacote em modo editável (`pip install -e .`)
5. **Construir** um pacote para distribuição
6. **Aplicar** boas práticas de empacotamento

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Ambiente virtual ativado
- UV e dependências instaladas

**Verificar ambiente:**

```bash
# Navegar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Ativar ambiente
.\.venv\Scripts\Activate.ps1

# Verificar UV
uv --version

# Verificar estrutura
ls src/
```

**Checklist:**
- [ ] Ambiente virtual ativado
- [ ] pyproject.toml existente
- [ ] Código em `src/`

# 5. Visão geral do que já existe no projeto (continuidade)

**Estado atual:**
```
swe4ds-credit-api/
├── .venv/
├── pyproject.toml              # Já tem dependências
├── uv.lock
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   └── validation.py
├── tests/
│   └── test_validation.py
└── ...
```

**O que vamos configurar:**
```
pyproject.toml
├── [project]                   # [MELHORAR] Metadados de distribuição
├── [project.scripts]           # [NOVO] CLI entry points
└── [build-system]              # [VERIFICAR] Build backend

src/
├── __init__.py                 # [MELHORAR] Versão e exports
└── ...
```

# 6. Passo a passo (comandos + código)

## Passo 1: Quando Empacotar? (Excalidraw: Slide 7)

**Intenção**: Entender quando o esforço de empacotamento vale a pena.

### Vale Empacotar Quando:

| Situação | Por que empacotar |
|----------|-------------------|
| Código reutilizado em múltiplos projetos | Evita duplicação |
| Biblioteca compartilhada entre times | Versionamento centralizado |
| CLI tool que será distribuída | Instalação simplificada |
| Projeto open source | Distribuição via PyPI |
| Código de produção com releases | Controle de versões |

### NÃO Vale Empacotar Quando:

| Situação | Por que não |
|----------|-------------|
| Projeto único sem reutilização | Overhead desnecessário |
| Notebook exploratório | Não é código de produção |
| Script one-off | Não será mantido |
| Protótipo descartável | Vai mudar muito |

### Trade-offs

| Benefício | Custo |
|-----------|-------|
| Reutilização | Mais configuração inicial |
| Versionamento | Processo de release |
| Instalação simples | Manutenção do pacote |
| Distribuição | Documentação necessária |

**CHECKPOINT**: Você sabe avaliar quando empacotar faz sentido.

---

## Passo 2: Estrutura de Pacote Python (Excalidraw: Slide 7)

**Intenção**: Entender a anatomia de um pacote.

### Estrutura Mínima

```
meu-pacote/
├── pyproject.toml              # Metadados e build config
├── README.md                   # Documentação
├── src/
│   └── meu_pacote/             # Código do pacote
│       ├── __init__.py         # Torna diretório um pacote
│       └── modulo.py           # Módulos do pacote
└── tests/
    └── test_modulo.py          # Testes
```

### O Padrão src/

Por que usar `src/`:
- Evita imports acidentais do código local
- Garante que testes usam o pacote instalado
- Padrão recomendado pela comunidade

### __init__.py

```python
# src/meu_pacote/__init__.py

# Versão do pacote
__version__ = "0.1.0"

# Exports públicos
from .modulo import funcao_principal

# O que é exposto quando alguém faz "from meu_pacote import *"
__all__ = ["funcao_principal", "__version__"]
```

**CHECKPOINT**: Você entende a estrutura padrão de pacotes Python.

---

## Passo 3: Atualizando src/__init__.py

**Intenção**: Configurar exports do pacote.

Abra o arquivo e aplique o **diff lógico** abaixo:

```bash
# Abrir o arquivo
code src/__init__.py
```

```python
# (SUBSTITUIR conteúdo do arquivo)
# src/__init__.py
"""
SWE4DS Credit API - Módulo de análise de crédito.

Este pacote fornece ferramentas para validação e análise
de dados de crédito, desenvolvido como parte do curso
Engenharia de Machine Learning.

Uso básico:
    from src import validate_limit_bal, validate_age
    
    is_valid = validate_limit_bal(50000)
"""

__version__ = "0.1.0"
__author__ = "SWE4DS Team"

# Imports públicos
from .validation import (
    validate_age,
    validate_education,
    validate_input,
    validate_limit_bal,
)

__all__ = [
    "__version__",
    "__author__",
    "validate_limit_bal",
    "validate_age",
    "validate_education",
    "validate_input",
]
```

Depois de salvar, rode o teste de import:

```python
# src/__init__.py
"""
SWE4DS Credit API - Módulo de análise de crédito.

Este pacote fornece ferramentas para validação e análise
de dados de crédito, desenvolvido como parte do curso
Engenharia de Machine Learning.

Uso básico:
    from src import validate_limit_bal, validate_age
    
    is_valid = validate_limit_bal(50000)
"""

__version__ = "0.1.0"
__author__ = "SWE4DS Team"

# Imports públicos
from .validation import (
    validate_age,
    validate_education,
    validate_input,
    validate_limit_bal,
)

__all__ = [
    "__version__",
    "__author__",
    "validate_limit_bal",
    "validate_age",
    "validate_education",
    "validate_input",
]
```

### Verificar exports

```bash
# Testar imports
python -c "from src import __version__, validate_limit_bal; print(f'v{__version__}: {validate_limit_bal(50000)}')"
```

**Saída esperada:**
```
v0.1.0: True
```

**CHECKPOINT**: `__init__.py` configura exports corretamente.

---

## Passo 4: Configurando pyproject.toml para Distribuição (Excalidraw: Slide 8)

**Intenção**: Adicionar metadados necessários para empacotamento.

Abra o `pyproject.toml` e **substitua a seção `[project]`** para ficar como abaixo (mão na massa):

```bash
# Abrir o arquivo
code pyproject.toml
```

```toml
# (SUBSTITUIR a seção [project] inteira e adicionar seções indicadas)
[project]
name = "swe4ds-credit-api"
version = "0.1.0"
description = "API de análise de crédito para o curso SWE4DS"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.12"

authors = [
    {name = "SWE4DS Team", email = "team@example.com"}
]

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.12",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]

keywords = ["credit", "machine-learning", "api", "fastapi"]

dependencies = [
    "pandas>=2.0,<3.0",
    "numpy>=1.24,<2.0",
    "scikit-learn>=1.3,<2.0",
    "pydantic>=2.0,<3.0",
    "fastapi>=0.100,<1.0",
    "uvicorn>=0.24,<1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0,<9.0",
    "pytest-cov>=4.0,<6.0",
    "ruff>=0.1,<1.0",
    "taskipy>=1.12,<2.0",
]

[project.scripts]
# swe4ds-credit = "src.cli:main"

[project.urls]
Homepage = "https://github.com/swe4ds/credit-api"
Documentation = "https://github.com/swe4ds/credit-api#readme"
Repository = "https://github.com/swe4ds/credit-api"
Issues = "https://github.com/swe4ds/credit-api/issues"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src"]
```

```toml
[project]
name = "swe4ds-credit-api"
version = "0.1.0"
description = "API de análise de crédito para o curso SWE4DS"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.12"

# Autores
authors = [
    {name = "SWE4DS Team", email = "team@example.com"}
]

# Classificadores PyPI
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.12",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]

# Keywords para busca
keywords = ["credit", "machine-learning", "api", "fastapi"]

# Dependências de produção
dependencies = [
    "pandas>=2.0,<3.0",
    "numpy>=1.24,<2.0",
    "scikit-learn>=1.3,<2.0",
    "pydantic>=2.0,<3.0",
    "fastapi>=0.100,<1.0",
    "uvicorn>=0.24,<1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0,<9.0",
    "pytest-cov>=4.0,<6.0",
    "ruff>=0.1,<1.0",
    "taskipy>=1.12,<2.0",
]

# Entry points para CLI (opcional)
[project.scripts]
# swe4ds-credit = "src.cli:main"  # Descomente se criar CLI

# URLs do projeto
[project.urls]
Homepage = "https://github.com/swe4ds/credit-api"
Documentation = "https://github.com/swe4ds/credit-api#readme"
Repository = "https://github.com/swe4ds/credit-api"
Issues = "https://github.com/swe4ds/credit-api/issues"

# Sistema de build
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# Configuração do Hatch para encontrar o pacote em src/
[tool.hatch.build.targets.wheel]
packages = ["src"]
```

### Explicação dos Campos

| Campo | Propósito |
|-------|-----------|
| `name` | Nome no PyPI (único) |
| `version` | Versão semântica |
| `description` | Descrição curta (uma linha) |
| `readme` | Arquivo de documentação |
| `license` | Licença do código |
| `requires-python` | Versão mínima do Python |
| `classifiers` | Categorização no PyPI |
| `dependencies` | Pacotes necessários |
| `[project.scripts]` | Comandos CLI |
| `[build-system]` | Backend de build |

**CHECKPOINT**: pyproject.toml tem metadados completos.

---

## Passo 5: Instalação em Modo Editável (Excalidraw: Slide 8)

**Intenção**: Instalar o pacote localmente para desenvolvimento.

```bash
# Instalar em modo editável (-e = editable)
uv pip install -e .

# Verificar que foi instalado
uv pip list | grep swe4ds

# Testar import como pacote instalado
python -c "import src; print(src.__version__)"
```

**Saída esperada:**
```
swe4ds-credit-api  0.1.0
0.1.0
```

### O que é Modo Editável?

- O pacote é "instalado" como link simbólico
- Mudanças no código são refletidas imediatamente
- Não precisa reinstalar após cada mudança
- Ideal para desenvolvimento

### Sem Modo Editável

```bash
# Instalação normal (copia código)
uv pip install .

# Mudanças no código NÃO são refletidas
# Precisa reinstalar: uv pip install . --force-reinstall
```

**CHECKPOINT**: Pacote instalado em modo editável.

---

## Passo 6: Construindo o Pacote com UV

**Intenção**: Gerar arquivos de distribuição usando UV.

```bash
# Construir pacote com UV (não precisa instalar nada extra)
uv build

# Verificar artefatos gerados
ls dist/
```

**Nota**: O comando `uv build` é equivalente a `python -m build`, mas integrado ao UV. Ele automaticamente gerencia as dependências de build.

**Saída esperada:**
```
dist/
├── swe4ds_credit_api-0.1.0-py3-none-any.whl  # Wheel (preferido)
└── swe4ds_credit_api-0.1.0.tar.gz            # Source distribution
```

### Tipos de Distribuição

| Tipo | Extensão | Uso |
|------|----------|-----|
| **Wheel** | `.whl` | Instalação rápida, pré-compilado |
| **Source** | `.tar.gz` | Build a partir do fonte |

Wheel é preferido porque:
- Instala mais rápido
- Não precisa compilar
- Mais seguro

**CHECKPOINT**: Arquivos de distribuição gerados em `dist/`.

---

## Passo 7: Testando o Pacote

**Intenção**: Verificar que o pacote instalável funciona.

```bash
# Criar ambiente temporário para teste
cd ..
mkdir test-install
cd test-install
uv venv
.\.venv\Scripts\Activate.ps1

# Instalar do arquivo wheel
uv pip install ../swe4ds-credit-api/dist/swe4ds_credit_api-0.1.0-py3-none-any.whl

# Testar
python -c "
from src import validate_limit_bal, __version__
print(f'Versão: {__version__}')
print(f'Validação: {validate_limit_bal(50000)}')
"

# Limpar
deactivate
cd ..
rm -rf test-install
```

**Saída esperada:**
```
Versão: 0.1.0
Validação: True
```

**CHECKPOINT**: Pacote instalável e funcional.

---

## Passo 8: Distribuição (Visão Geral)

**Intenção**: Entender as opções de distribuição.

### Opções de Distribuição

| Método | Uso | Comando de Instalação |
|--------|-----|----------------------|
| **Local** | Desenvolvimento | `pip install -e .` |
| **Wheel file** | Compartilhar diretamente | `pip install pacote.whl` |
| **Git URL** | Repos privados | `pip install git+https://...` |
| **PyPI** | Público | `pip install pacote` |
| **Private PyPI** | Empresas | Configurar index URL |

### Publicar no PyPI (Referência)

```bash
# 1. Criar conta no PyPI
# 2. Instalar twine
uv pip install twine

# 3. Upload (CUIDADO: irreversível)
# python -m twine upload dist/*
```

**Nota**: Não vamos publicar no PyPI neste curso. Esta é apenas uma referência.

### Instalação de Git

```bash
# Instalar diretamente de repositório
pip install git+https://github.com/user/repo.git

# Instalar branch específico
pip install git+https://github.com/user/repo.git@branch

# Instalar tag específica
pip install git+https://github.com/user/repo.git@v1.0.0
```

**CHECKPOINT**: Você conhece as opções de distribuição.

---

## Passo 9: Commit Final do Módulo

**Intenção**: Versionar configuração de empacotamento.

```bash
# Voltar para o projeto
cd c:\Users\diogomiyake\projects\swe4ds-credit-api

# Adicionar arquivos
git add pyproject.toml src/__init__.py

# Ignorar dist/ (artefatos de build)
echo "dist/" >> .gitignore
echo "*.egg-info/" >> .gitignore

git add .gitignore

# Commit
git commit -m "feat: configura projeto como pacote instalável

Atualizações:
- pyproject.toml com metadados completos para distribuição
- src/__init__.py com versão e exports públicos
- .gitignore inclui artefatos de build

O pacote pode ser instalado com:
- pip install -e . (desenvolvimento)
- pip install . (produção)
- pip install git+<repo_url> (de repositório)"

# Push
git push origin main
```

**CHECKPOINT**: Configuração de pacote versionada.

# 7. Testes rápidos e validação

```bash
# Verificar pyproject.toml válido
python -c "import tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['name'])"

# Verificar instalação editável
uv pip show swe4ds-credit-api

# Testar imports
python -c "from src import __version__, validate_limit_bal; print(f'{__version__}: {validate_limit_bal(50000)}')"

# Construir pacote com UV
uv build

# Verificar wheel
ls dist/*.whl
```

# 8. Observabilidade e boas práticas (mini-bloco)

### Boas Práticas de Empacotamento

1. **Versão única em um lugar**
   - Defina `__version__` em `__init__.py`
   - Use dynamic version no pyproject.toml se necessário
   - **Trade-off**: Mais simples, mas pode dessincronizar

2. **Changelog mantido**
   - Documente mudanças entre versões
   - Siga formato Keep a Changelog
   - **Trade-off**: Trabalho extra, mas usuários agradecem

3. **Testes passam antes de release**
   - CI deve validar build
   - Testes em múltiplas versões Python
   - **Trade-off**: Build mais lento, mas mais confiável

4. **Dependências com ranges**
   - Não trave versões exatas em pacotes
   - Deixe flexibilidade para consumidores
   - **Trade-off**: Pode ter incompatibilidades, mas mais flexível

5. **Documentação incluída**
   - README.md é essencial
   - Docstrings em funções públicas
   - **Trade-off**: Tempo extra, mas aumenta adoção

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| `ModuleNotFoundError` após install | Estrutura de pastas errada | Verificar `packages` no pyproject.toml |
| Build falha | Dependência de build faltando | `pip install build hatchling` |
| `Invalid version` | Versão não segue SemVer | Usar formato X.Y.Z |
| Package não encontrado no import | Nome diferente do diretório | Verificar nome em pyproject.toml |
| `Could not find a version` | requires-python incompatível | Verificar versão do Python |
| Wheel não inclui arquivos | Configuração de build errada | Verificar `[tool.hatch.build]` |

# 10. Exercícios (básico e avançado)

## Exercício Básico 1: Atualizar Versão

Atualize a versão do pacote para `0.2.0`, reconstrua o wheel, e verifique que a nova versão é refletida.

**Critério de sucesso**: `python -c "import src; print(src.__version__)"` mostra `0.2.0`.

## Exercício Básico 2: Adicionar Autor

Adicione seu nome como autor no pyproject.toml. Reconstrua o pacote e verifique os metadados com `uv pip show swe4ds-credit-api`.

**Critério de sucesso**: Seu nome aparece no campo Author.

## Exercício Avançado: CLI Entry Point

Crie um arquivo `src/cli.py` com uma função `main()` que imprime informações do pacote. Configure o entry point `swe4ds-credit` no pyproject.toml. Após reinstalar, o comando `swe4ds-credit` deve funcionar no terminal.

**Critério de sucesso**: `swe4ds-credit` executa e mostra versão e informações.

# 11. Resultados e Lições

## Métricas do Módulo de Dependências

| Métrica | Início | Fim |
|---------|--------|-----|
| Ambiente isolado | Não | `.venv/` configurado |
| Gerenciador de pacotes | pip básico | UV moderno |
| Lockfile | Não | `uv.lock` |
| Ferramentas dev | Nenhuma | taskipy, pytest, ruff |
| Empacotamento | Não | Wheel buildável |

## Lições do Módulo

1. **Isolamento previne conflitos** - Um ambiente por projeto
2. **UV é o futuro** - Mais rápido e integrado que pip
3. **Lockfile garante reprodutibilidade** - Versões exatas registradas
4. **Automação economiza tempo** - Taskipy para comandos repetitivos
5. **Empacotamento tem trade-offs** - Avalie antes de investir

## Resumo de Comandos UV

```bash
# Ambiente
uv venv                    # Criar ambiente
uv sync                    # Sincronizar dependências

# Pacotes
uv add pacote              # Adicionar dependência
uv add --dev pacote        # Adicionar dev dependency
uv remove pacote           # Remover pacote

# Execução
uv run comando             # Executar no ambiente
task tarefa                # Rodar tarefa taskipy

# Build e Empacotamento
uv build                   # Construir pacote (wheel + sdist)
uv pip install -e .        # Instalar editável
uv pip install .           # Instalar normal
```

# 12. Encerramento e gancho para a próxima aula (script)

Parabéns! Você completou o módulo de Gerenciamento de Dependências. Em 4 aulas você aprendeu:

- Por que isolamento é fundamental e como usar UV
- Versionamento semântico e gerenciamento moderno de pacotes
- Ferramentas de desenvolvimento: taskipy, pytest, ruff
- Como empacotar código para distribuição

Seu projeto agora tem um ambiente profissional de desenvolvimento. Dependências são gerenciadas, código é testado e formatado, e o pacote pode ser distribuído.

Na próxima aula, vamos mudar de assunto e falar sobre **Padrões de Código e Estilo**. Você vai aprender sobre PEP 8, princípios de código limpo como DRY e KISS, e padrões de design aplicados a Data Science. Vamos ver como escrever código que não só funciona, mas é fácil de ler, manter e evoluir.

O ambiente está pronto. Agora vamos garantir que o código dentro dele seja de alta qualidade. Até a próxima aula!
