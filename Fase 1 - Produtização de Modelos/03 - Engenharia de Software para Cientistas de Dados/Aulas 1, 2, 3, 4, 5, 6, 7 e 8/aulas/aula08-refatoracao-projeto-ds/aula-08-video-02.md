---
titulo: "Aula 08 – Parte 02: Técnicas de Refatoração Graduais - Teoria e Estratégias"
modulo: "Engenharia de software para cientista de dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 20
prerequisitos:
  - "Python 3.12+"
  - "Aula 08 - Parte 01 concluída"
  - "Testes automatizados básicos"
tags: ["refatoracao", "extract-function", "rename", "move-code", "fastapi"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula vamos entender as **técnicas de refatoração graduais** mais úteis para projetos de Data Science.

Você já sabe identificar bad smells. Agora vamos aprender a resolvê-los de forma segura e incremental, sem quebrar a API FastAPI que estamos construindo. Vamos usar técnicas clássicas do catálogo de Martin Fowler, adaptadas ao nosso contexto: **Extract Function**, **Rename** e **Move/Rearrange Code**.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você encontrou uma função enorme dentro da API que carrega dados, valida, processa e retorna predição.

**Agitação**: Se você mexer em algo, corre o risco de quebrar outra parte. E a equipe não confia em grandes reescritas.

**Solução**: Refatorar em passos pequenos, com testes a cada etapa. Extraímos funções, renomeamos variáveis e movemos código para módulos mais adequados. A API continua estável, mas o design melhora continuamente.

# 3. Objetivos de aprendizagem

Ao final você será capaz de:

1. **Aplicar** Extract Function para reduzir funções longas
2. **Renomear** elementos para expressar intenção
3. **Mover** código para módulos adequados
4. **Planejar** refatorações em pequenos passos

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+
- uv instalado
- Testes existentes

**Setup:**

```bash
# Ativar ambiente
.\.venv\Scripts\Activate.ps1

# Rodar testes
uv run pytest -q
```

**Checklist de setup:**
- [ ] Ambiente virtual ativo
- [ ] Testes passando
- [ ] Git limpo (sem mudanças pendentes)

# 5. Visão geral do que já existe no projeto (continuidade)

Estado esperado:
```
swe4ds-credit-api/
├── src/
│   ├── routes/
│   ├── services/
│   └── main.py
├── tests/
└── Consumer_API/
```

**O que será alterado nesta parte:**
- Refatorações graduais em `services/`
- Melhoria de nomes em `routes/`

# 6. Passo a passo (comandos + código)

## Passo 1: Catálogo de técnicas (Excalidraw: Slide 2)

**Intenção:** Entender quando usar cada técnica.

| Técnica | Quando usar | Resultado esperado |
|---|---|---|
| Extract Function | Blocos repetidos | Reuso e testes fáceis |
| Rename | Nomes genéricos | Código autoexplicativo |
| Move/Rearrange | Mistura de camadas | Separação clara |

**CHECKPOINT:** Você sabe escolher a técnica correta para cada smell.

---

## Passo 2: Estratégia de risco controlado

**Intenção:** Refatorar sem quebrar a API.

Regras de ouro:
1. **Teste antes**
2. **Passos pequenos**
3. **Commit por mudança**

**CHECKPOINT:** Você consegue explicar o porquê dessa ordem.

---

## Passo 3: Critérios de sucesso

**Intenção:** Saber se a refatoração foi bem‑sucedida.

Critérios:
- Mesma resposta para o mesmo input
- Testes verdes
- Menos duplicação e menor acoplamento

**CHECKPOINT:** Você sabe provar que não mudou o comportamento.

# 7. Testes rápidos e validação

Nesta parte, a validação é **conceitual**. A execução prática (com comandos e testes reais) entra na Parte 03.

**CHECKPOINT:** Você entende que cada refatoração precisa de testes antes e depois.

# 8. Observabilidade e boas práticas (mini-bloco)

1. **Refatorar com testes**: reduz risco. Trade-off: mais tempo de preparação.
2. **Commits pequenos**: facilita rollback. Trade-off: histórico mais granular.
3. **Separação de camadas**: melhora manutenção. Trade-off: mais arquivos.

# 9. Troubleshooting (erros comuns)

| Erro | Causa | Solução |
|------|-------|---------|
| Quebrou import após mover função | Caminho errado | Atualizar importações |
| Testes falhando | Mudança de comportamento | Revisar refatoração |
| Renomeou e esqueceu referências | Busca incompleta | Usar rename da IDE |

# 10. Exercícios (básico e avançado)

**Básico 1:** Extrair função de validação de payload.
- Concluído com sucesso: código duplicado removido.

**Básico 2:** Renomear variáveis genéricas (`x`, `data`) para nomes de domínio.
- Concluído com sucesso: código legível sem comentários extras.

**Avançado:** Mover lógica de carregamento do modelo para `services/` e atualizar imports.
- Concluído com sucesso: endpoints continuam funcionando com testes verdes.

# 11. Resultados e Lições

**Resultados (como medir):**
- Redução de linhas por função (comparar antes/depois)
- Duplicação removida (contagem manual)
- Testes verdes após cada etapa

**Lições:**
- Refatorar é processo incremental
- Nomes são parte do design
- Organizar camadas reduz acoplamento

# 12. Encerramento e gancho para a próxima aula (script)

Nesta aula você aprendeu as principais técnicas de refatoração gradual: Extract Function, Rename e Move/Rearrange Code. Isso permite evoluir nossa API FastAPI com segurança, mantendo a estabilidade.

Na próxima parte, vamos para a prática completa: refatorar um código de Data Science passo a passo, comparando antes e depois, com testes em cada etapa.
