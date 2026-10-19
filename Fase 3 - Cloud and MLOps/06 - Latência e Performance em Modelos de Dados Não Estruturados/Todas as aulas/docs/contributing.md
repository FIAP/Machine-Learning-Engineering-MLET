# Guia de Contribuicao

Obrigado por considerar contribuir com este repositorio! Este guia descreve o processo para reportar issues, submeter pull requests e manter a qualidade do codigo e da documentacao.

---

## Como Reportar Issues

1. Verifique se a issue ja nao foi reportada na [aba Issues](../../issues)
2. Crie uma nova issue usando um dos templates disponiveis:
   - **Bug Report:** Para erros em codigo, notebooks ou documentacao
   - **Feature Request:** Para sugestoes de novo conteudo ou melhorias
   - **Question:** Para duvidas sobre o material

### Template de Bug Report

```markdown
## Descricao do Bug
[Descricao clara e concisa]

## Passos para Reproduzir
1. Navegar para '...'
2. Executar '...'
3. Observar erro '...'

## Comportamento Esperado
[O que deveria acontecer]

## Ambiente
- OS: [ex: Windows 11, Ubuntu 22.04]
- Python: [ex: 3.10.12]
- PyTorch: [ex: 2.1.0]
- GPU: [ex: NVIDIA RTX 3080, nenhuma]

## Logs / Screenshots
[Se aplicavel]
```

---

## Como Submeter Pull Requests

### 1. Fork e Branch

```bash
# Fork o repositorio no GitHub
# Clone seu fork
git clone https://github.com/SEU_USUARIO/latencia-performance-dados-nao-estruturados.git
cd latencia-performance-dados-nao-estruturados

# Crie uma branch para sua feature
git checkout -b feature/nome-da-feature
# ou
git checkout -b fix/descricao-do-fix
```

### 2. Convencao de Branches

| Prefixo | Uso |
|---------|-----|
| `feature/` | Nova funcionalidade ou conteudo |
| `fix/` | Correcao de bug |
| `docs/` | Alteracao apenas em documentacao |
| `refactor/` | Refatoracao sem mudanca de comportamento |

### 3. Faca suas alteracoes

- Siga os padroes de codigo descritos abaixo
- Adicione testes quando aplicavel
- Atualize a documentacao se necessario

### 4. Commits

Siga [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(aula4): adicionar notebook de quantizacao QAT
fix(aula2): corrigir tokenizacao para sequencias longas
docs(readme): atualizar instrucoes de instalacao
refactor(aula6): simplificar profiling com PyTorch Profiler
```

### 5. Submeta o Pull Request

```bash
git push origin feature/nome-da-feature
```

No GitHub, crie o PR para a branch `main` com:
- Titulo descritivo seguindo Conventional Commits
- Descricao do que foi alterado e por que
- Referencia a issues relacionadas (ex: `Closes #42`)

---

## Padroes de Codigo

### Python (PEP 8 + Type Hints)

```python
# Exemplo de padrao esperado
from typing import Optional
import numpy as np
import torch
from torch import nn, Tensor


def optimize_model(
    model: nn.Module,
    quantize: bool = True,
    target_latency_ms: float = 50.0,
) -> nn.Module:
    """Otimiza modelo para inferencia de baixa latencia.

    Args:
        model: Modelo PyTorch a ser otimizado.
        quantize: Se True, aplica quantizacao INT8.
        target_latency_ms: Latencia alvo em milissegundos.

    Returns:
        Modelo otimizado.

    Raises:
        ValueError: Se target_latency_ms for negativo.
    """
    if target_latency_ms < 0:
        raise ValueError("target_latency_ms deve ser positivo")

    if quantize:
        model = torch.quantization.quantize_dynamic(
            model, {nn.Linear}, dtype=torch.qint8
        )

    return model
```

### Regras Gerais

- **PEP 8:** Seguir estritamente (use `ruff` ou `flake8` para validacao)
- **Type hints:** Obrigatorios em funcoes publicas
- **Docstrings:** Google style para funcoes e classes publicas
- **Imports:** Ordenados com `isort` (stdlib → third-party → local)
- **Formatacao:** `black` com line length 88
- **Linting:** `ruff` com configuracao do projeto
- **Nomes:** snake_case para funcoes/variaveis, PascalCase para classes

### Notebooks

- Celulas devem ser executaveis **em ordem** (top-to-bottom)
- Incluir celula de `pip install` com dependencias no topo
- Limpar outputs antes de commit (use `nbstripout`)
- Usar Markdown cells para explicar conceitos e decisoes

---

## Como Executar Testes

```bash
# Instalar dependencias de teste
pip install pytest pytest-cov

# Executar todos os testes
pytest tests/ -v

# Executar testes de uma aula especifica
pytest tests/test_aula04_quantization.py -v

# Executar com cobertura
pytest tests/ --cov=src --cov-report=html

# Verificar estilo de codigo
ruff check .
black --check .
```

---

## Como Adicionar Nova Aula

### 1. Criar Estrutura de Pasta

```
NN_nome_da_aula/
├── README.md              # Descricao, objetivos, instrucoes
├── requirements.txt       # Dependencias especificas da aula
├── notebooks/
│   ├── 01_conceitos.ipynb
│   └── 02_pratica.ipynb
├── src/
│   ├── __init__.py
│   ├── model.py
│   └── utils.py
├── tests/
│   └── test_model.py
└── data/
    └── .gitkeep
```

### 2. Checklist de Qualidade

- [ ] README.md com objetivo, teoria-chave e instrucoes de execucao
- [ ] requirements.txt com dependencias pinadas
- [ ] Notebooks executaveis em ordem com outputs limpos
- [ ] Codigo em `src/` com type hints e docstrings
- [ ] Testes em `tests/` com cobertura minima de 80%
- [ ] Benchmark de latencia documentado (antes/depois de otimizacao)
- [ ] Links atualizados no README.md principal

### 3. Atualizar Documentacao

- Adicionar entrada no README.md principal (secao Conteudo das Aulas)
- Adicionar pasta na arvore de diretorios (secao Estrutura do Repositorio)
- Atualizar `docs/business/use-cases.md` se aplicavel

---

## Configuracao de Ferramentas

### pyproject.toml (recomendado)

```toml
[tool.black]
line-length = 88
target-version = ['py310']

[tool.ruff]
line-length = 88
target-version = "py310"
select = ["E", "F", "I", "N", "W"]

[tool.isort]
profile = "black"
line_length = 88

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
```

---

## Codigo de Conduta

Este projeto adere ao [Contributor Covenant](https://www.contributor-covenant.org/). Ao participar, espera-se que voce mantenha um ambiente respeitoso e inclusivo.

---

## Duvidas?

Abra uma [Discussion](../../discussions) no GitHub ou entre em contato com os mantenedores do repositorio.
