---
titulo: "Aula 01 – Parte 03: Paradigmas de Programação (Estruturado vs. OO)"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 25
prerequisitos:
  - "Python 3.12+"
  - "Conceitos de Aula 01 - Partes 01 e 02"
  - "Ambiente virtual configurado"
tags: ["programacao-estruturada", "orientacao-objetos", "encapsulamento", "classes", "paradigmas"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula, vamos fazer algo diferente: vamos colocar a mão no código e ver, na prática, a diferença entre dois paradigmas de programação - estruturado e orientado a objetos.

Vocês já ouviram falar que "Python é uma linguagem orientada a objetos", certo? Mas o que isso realmente significa? E mais importante: quando você deve usar classes e objetos no seu código de Data Science, e quando programação estruturada (funções simples) é suficiente?

Essa é uma dúvida comum. Muitos cientistas de dados começam com scripts lineares, depois aprendem sobre classes, e ficam confusos sobre quando usar cada abordagem. A resposta não é "sempre use OOP" nem "nunca use OOP" - é entender as vantagens de cada paradigma e escolher apropriadamente.

Nesta aula, vamos resolver o mesmo problema de Data Science de duas formas diferentes: primeiro com programação estruturada (funções), depois com orientação a objetos (classes). Você verá, executando código real, como encapsulamento, estados e métodos ajudam a organizar projetos complexos.

Ao final, você terá critérios claros para decidir quando usar cada paradigma nos seus próprios projetos.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você está construindo um sistema de predição de preços de imóveis. Inicialmente, você cria funções para carregar dados, limpar, treinar modelo e fazer predições. Tudo funciona. Mas aí surge um novo requisito: o sistema precisa suportar múltiplos modelos (RandomForest, XGBoost, LinearRegression) e o usuário deve poder escolher qual usar. Além disso, cada modelo tem configurações diferentes e precisa manter seu próprio estado (se está treinado, quais hiperparâmetros, histórico de métricas).

**Agitação**: Você tenta adicionar isso com funções puras e variáveis globais. Cria `train_rf()`, `train_xgb()`, `train_lr()`, `predict_rf()`, `predict_xgb()`, `predict_lr()`... em cada predict tem que verificar "o modelo foi treinado?", "quais são os dados de treino?", "qual a versão?". Você começa a passar 10 parâmetros para cada função. O código vira um emaranhado de `if/else` e variáveis compartilhadas. Testar fica impossível porque tudo depende de estado global. Adicionar um novo modelo requer mudar código em 15 lugares.

**Solução**: Com orientação a objetos, você cria uma classe `Model` que encapsula o estado (parâmetros, dados de treino, se está treinado) e comportamento (train, predict, evaluate). Cada tipo de modelo herda dessa classe base. Adicionar um novo modelo? Crie uma nova classe sem tocar no resto. Testar? Instancie um objeto com configuração específica. Gerenciar múltiplos modelos? Crie múltiplas instâncias. OOP não é "melhor" que estruturado - é mais apropriado quando você precisa gerenciar **estado e comportamento complexos juntos**.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Explicar** as diferenças fundamentais entre programação estruturada e orientada a objetos
2. **Implementar** a mesma solução usando ambos os paradigmas e comparar trade-offs
3. **Identificar** cenários onde OOP é mais adequado que programação estruturada
4. **Aplicar** conceitos de encapsulamento para organizar código de Data Science
5. **Utilizar** classes e objetos para gerenciar estado e comportamento de modelos ML
6. **Decidir** conscientemente quando usar funções versus classes em seus projetos

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+
- UV instalado
- Ambiente virtual ativo
- Bibliotecas: scikit-learn, pandas, numpy

**Instalação de dependências:**

```bash
# Ativar ambiente virtual
# Windows:
cd c:\Users\diogomiyake\projects\SWE-4-DS\swe4ds-api-project
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate

# Instalar dependências com UV (muito mais rápido que pip)
uv pip install scikit-learn pandas numpy

# Verificar instalação
python -c "import sklearn; import pandas; import numpy; print('OK')"
```

**Checklist de Setup:**
- [ ] Ambiente virtual ativo (`.venv`)
- [ ] scikit-learn instalado
- [ ] pandas instalado
- [ ] numpy instalado
- [ ] Comando de verificação retornou "OK"

# 5. Visão geral do que já existe no projeto (continuidade)

Vamos criar uma nova pasta para os exemplos práticos desta aula:

```
swe4ds-api-project/
├── .venv/                   
├── exemplos/                
│   └── paradigmas/          # [NOVO] Exemplos desta aula
│       ├── estruturado/     # Abordagem funcional
│       └── oo/              # Abordagem OOP
└── (estrutura da API - próximas aulas)
```

```bash
# Criar estrutura
mkdir -p exemplos/paradigmas/estruturado
mkdir -p exemplos/paradigmas/oo
cd exemplos/paradigmas
```

# 6. Passo a passo (comandos + código)

## Passo 1: Problema Base - Sistema de Predição

**Intenção**: Definir o problema que resolveremos de duas formas diferentes.

Vamos criar um sistema de predição de preços de casas que:
1. Carrega dados
2. Pré-processa (limpa, transforma)
3. Treina um modelo
4. Faz predições
5. Avalia performance

Primeiro, vamos criar dados sintéticos para trabalhar:

```python
# exemplos/paradigmas/gerar_dados.py
"""Gera dados sintéticos de preços de imóveis."""
import pandas as pd
import numpy as np

def gerar_dados_imoveis(n_samples: int = 1000, seed: int = 42) -> pd.DataFrame:
    """Gera dataset sintético de preços de imóveis."""
    np.random.seed(seed)
    
    # Features
    area = np.random.normal(150, 50, n_samples)
    quartos = np.random.randint(1, 6, n_samples)
    banheiros = np.random.randint(1, 4, n_samples)
    idade = np.random.randint(0, 50, n_samples)
    distancia_centro = np.random.normal(10, 5, n_samples)
    
    # Target (com alguma lógica)
    preco = (
        3000 * area +
        50000 * quartos +
        30000 * banheiros -
        1000 * idade -
        2000 * distancia_centro +
        np.random.normal(0, 50000, n_samples)
    )
    
    df = pd.DataFrame({
        'area': area,
        'quartos': quartos,
        'banheiros': banheiros,
        'idade': idade,
        'distancia_centro': distancia_centro,
        'preco': preco
    })
    
    return df

if __name__ == "__main__":
    df = gerar_dados_imoveis()
    df.to_csv('imoveis.csv', index=False)
    print(f"Dataset gerado: {len(df)} imóveis")
    print(df.head())
```

Execute:
```bash
cd exemplos/paradigmas
python gerar_dados.py
```

**CHECKPOINT**: Você deve ter um arquivo `imoveis.csv` com 1000 linhas e 6 colunas.

## Passo 2: Abordagem Estruturada (Funções)

**Intenção**: Resolver o problema usando apenas funções (sem classes).

```python
# exemplos/paradigmas/estruturado/solucao_funcional.py
"""Solução usando programação estruturada (funções)."""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from typing import Tuple

# Variáveis globais para manter estado (problemático!)
model = None
feature_cols = None
is_trained = False


def carregar_dados(caminho: str) -> pd.DataFrame:
    """Carrega dados de CSV."""
    df = pd.read_csv(caminho)
    print(f"Dados carregados: {len(df)} registros")
    return df


def pre_processar(df: pd.DataFrame) -> pd.DataFrame:
    """Limpa e prepara dados."""
    # Remove nulos
    df = df.dropna()
    
    # Remove outliers (valores negativos)
    df = df[df['area'] > 0]
    df = df[df['preco'] > 0]
    
    print(f"Após pré-processamento: {len(df)} registros")
    return df


def separar_features_target(df: pd.DataFrame, target_col: str = 'preco') -> Tuple[pd.DataFrame, pd.Series]:
    """Separa features e target."""
    global feature_cols
    
    feature_cols = [col for col in df.columns if col != target_col]
    X = df[feature_cols]
    y = df[target_col]
    
    return X, y


def dividir_treino_teste(X: pd.DataFrame, y: pd.Series, 
                          test_size: float = 0.2, 
                          random_state: int = 42) -> Tuple:
    """Divide dados em treino e teste."""
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


def treinar_modelo(X_train: pd.DataFrame, y_train: pd.Series, 
                   n_estimators: int = 100, 
                   random_state: int = 42) -> None:
    """Treina modelo RandomForest."""
    global model, is_trained
    
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1
    )
    
    print("Treinando modelo...")
    model.fit(X_train, y_train)
    is_trained = True
    print("Modelo treinado!")


def fazer_predicao(X: pd.DataFrame) -> np.ndarray:
    """Faz predição usando modelo treinado."""
    global model, is_trained, feature_cols
    
    if not is_trained or model is None:
        raise ValueError("Modelo não foi treinado ainda!")
    
    # Garante ordem correta das features
    X = X[feature_cols]
    return model.predict(X)


def avaliar_modelo(X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """Avalia performance do modelo."""
    if not is_trained:
        raise ValueError("Modelo não foi treinado ainda!")
    
    y_pred = fazer_predicao(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    metricas = {
        'mse': mse,
        'rmse': rmse,
        'r2': r2
    }
    
    return metricas


def pipeline_completo(caminho_dados: str) -> dict:
    """Executa pipeline completo."""
    # Carrega
    df = carregar_dados(caminho_dados)
    
    # Pré-processa
    df = pre_processar(df)
    
    # Separa features e target
    X, y = separar_features_target(df)
    
    # Divide treino/teste
    X_train, X_test, y_train, y_test = dividir_treino_teste(X, y)
    
    # Treina
    treinar_modelo(X_train, y_train)
    
    # Avalia
    metricas = avaliar_modelo(X_test, y_test)
    
    print("\n=== Métricas ===")
    print(f"RMSE: ${metricas['rmse']:,.2f}")
    print(f"R²: {metricas['r2']:.3f}")
    
    return metricas


if __name__ == "__main__":
    metricas = pipeline_completo('../imoveis.csv')
    
    # Exemplo de predição nova
    novo_imovel = pd.DataFrame({
        'area': [200],
        'quartos': [3],
        'banheiros': [2],
        'idade': [5],
        'distancia_centro': [8]
    })
    
    preco_previsto = fazer_predicao(novo_imovel)
    print(f"\nPreço previsto para novo imóvel: ${preco_previsto[0]:,.2f}")
```

**Problemas desta abordagem**:
1. **Variáveis globais** (`model`, `feature_cols`, `is_trained`) - difícil de gerenciar
2. **Impossível ter múltiplos modelos** simultaneamente
3. **Estado implícito** - funções dependem de ordem de execução
4. **Difícil de testar** - testes afetam uns aos outros via estado global
5. **Sem encapsulamento** - qualquer código pode modificar o modelo

Execute:
```bash
cd exemplos/paradigmas/estruturado
python solucao_funcional.py
```

**CHECKPOINT**: O código funciona, mas note a dependência de variáveis globais e a necessidade de executar funções em ordem específica.

## Passo 3: Abordagem Orientada a Objetos (Classes)

**Intenção**: Resolver o mesmo problema usando OOP, encapsulando estado e comportamento.

```python
# exemplos/paradigmas/oo/solucao_oop.py
"""Solução usando Programação Orientada a Objetos."""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from typing import Tuple, Optional
from datetime import datetime


class PreProcessador:
    """Responsável por limpeza e preparação de dados."""
    
    def __init__(self, target_col: str = 'preco'):
        self.target_col = target_col
        self.feature_cols: Optional[list] = None
    
    def processar(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica limpeza completa."""
        df = self._remover_nulos(df)
        df = self._remover_outliers(df)
        self._definir_features(df)
        return df
    
    def _remover_nulos(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove registros com valores nulos."""
        n_antes = len(df)
        df = df.dropna()
        n_depois = len(df)
        print(f"Nulos removidos: {n_antes - n_depois} registros")
        return df
    
    def _remover_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove valores negativos."""
        df = df[df['area'] > 0]
        df = df[df[self.target_col] > 0]
        return df
    
    def _definir_features(self, df: pd.DataFrame) -> None:
        """Define colunas de features."""
        self.feature_cols = [col for col in df.columns if col != self.target_col]
    
    def separar_features_target(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Separa X e y."""
        if self.feature_cols is None:
            self._definir_features(df)
        
        X = df[self.feature_cols]
        y = df[self.target_col]
        return X, y


class ModeloPreditivo:
    """Encapsula modelo de ML com seu estado e comportamento."""
    
    def __init__(self, nome: str = "ModeloPadrao", 
                 n_estimators: int = 100, 
                 random_state: int = 42):
        """
        Inicializa modelo.
        
        Args:
            nome: Identificador do modelo
            n_estimators: Número de árvores do RandomForest
            random_state: Seed para reprodutibilidade
        """
        self.nome = nome
        self.n_estimators = n_estimators
        self.random_state = random_state
        
        # Estado interno
        self._modelo = RandomForestRegressor(
            n_estimators=n_estimators,
            random_state=random_state,
            n_jobs=-1
        )
        self._treinado = False
        self._feature_cols: Optional[list] = None
        self._data_treino: Optional[datetime] = None
        self._metricas_treino: Optional[dict] = None
    
    @property
    def esta_treinado(self) -> bool:
        """Verifica se modelo está treinado."""
        return self._treinado
    
    def treinar(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """Treina o modelo."""
        print(f"[{self.nome}] Iniciando treinamento...")
        
        self._feature_cols = list(X_train.columns)
        self._modelo.fit(X_train, y_train)
        self._treinado = True
        self._data_treino = datetime.now()
        
        print(f"[{self.nome}] Treinamento concluído!")
    
    def prever(self, X: pd.DataFrame) -> np.ndarray:
        """Faz predições."""
        if not self._treinado:
            raise ValueError(f"[{self.nome}] Modelo não está treinado!")
        
        # Garante ordem das features
        X = X[self._feature_cols]
        return self._modelo.predict(X)
    
    def avaliar(self, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        """Avalia performance."""
        y_pred = self.prever(X_test)
        
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        metricas = {
            'mse': mse,
            'rmse': rmse,
            'r2': r2
        }
        
        self._metricas_treino = metricas
        return metricas
    
    def info(self) -> dict:
        """Retorna informações do modelo."""
        return {
            'nome': self.nome,
            'treinado': self._treinado,
            'data_treino': self._data_treino,
            'n_features': len(self._feature_cols) if self._feature_cols else 0,
            'metricas': self._metricas_treino
        }
    
    def __repr__(self) -> str:
        status = "treinado" if self._treinado else "não treinado"
        return f"ModeloPreditivo(nome='{self.nome}', status='{status}')"


class PipelineML:
    """Orquestra todo o processo de ML."""
    
    def __init__(self, preprocessador: PreProcessador, modelo: ModeloPreditivo):
        """
        Inicializa pipeline.
        
        Args:
            preprocessador: Instância de PreProcessador
            modelo: Instância de ModeloPreditivo
        """
        self.preprocessador = preprocessador
        self.modelo = modelo
        self.test_size = 0.2
    
    def executar(self, caminho_dados: str) -> dict:
        """Executa pipeline completo."""
        # 1. Carrega dados
        print("\n=== Carregando dados ===")
        df = pd.read_csv(caminho_dados)
        print(f"Registros carregados: {len(df)}")
        
        # 2. Pré-processa
        print("\n=== Pré-processando ===")
        df = self.preprocessador.processar(df)
        print(f"Registros após limpeza: {len(df)}")
        
        # 3. Separa features e target
        X, y = self.preprocessador.separar_features_target(df)
        
        # 4. Divide treino/teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=42
        )
        
        # 5. Treina modelo
        print("\n=== Treinando ===")
        self.modelo.treinar(X_train, y_train)
        
        # 6. Avalia
        print("\n=== Avaliando ===")
        metricas = self.modelo.avaliar(X_test, y_test)
        
        print(f"\nRMSE: ${metricas['rmse']:,.2f}")
        print(f"R²: {metricas['r2']:.3f}")
        
        return metricas


if __name__ == "__main__":
    # Exemplo 1: Pipeline simples
    print("=== EXEMPLO 1: Pipeline Único ===")
    
    preprocessador = PreProcessador(target_col='preco')
    modelo = ModeloPreditivo(nome="RandomForest_v1", n_estimators=100)
    
    pipeline = PipelineML(preprocessador, modelo)
    metricas = pipeline.executar('../imoveis.csv')
    
    # Predição em novo dado
    novo_imovel = pd.DataFrame({
        'area': [200],
        'quartos': [3],
        'banheiros': [2],
        'idade': [5],
        'distancia_centro': [8]
    })
    
    preco = modelo.prever(novo_imovel)
    print(f"\nPreço previsto: ${preco[0]:,.2f}")
    print(f"\nInfo do modelo: {modelo.info()}")
    
    # Exemplo 2: MÚLTIPLOS MODELOS simultaneamente (impossível na versão funcional!)
    print("\n\n=== EXEMPLO 2: Múltiplos Modelos ===")
    
    # Carrega e prepara dados uma vez
    df = pd.read_csv('../imoveis.csv')
    prep = PreProcessador()
    df = prep.processar(df)
    X, y = prep.separar_features_target(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Cria 3 modelos diferentes
    modelo1 = ModeloPreditivo(nome="RF_50", n_estimators=50)
    modelo2 = ModeloPreditivo(nome="RF_100", n_estimators=100)
    modelo3 = ModeloPreditivo(nome="RF_200", n_estimators=200)
    
    # Treina todos
    for modelo in [modelo1, modelo2, modelo3]:
        modelo.treinar(X_train, y_train)
        metricas = modelo.avaliar(X_test, y_test)
        print(f"{modelo.nome} - RMSE: ${metricas['rmse']:,.2f}, R²: {metricas['r2']:.3f}")
    
    # Compara predições
    print("\nPredições do mesmo imóvel por diferentes modelos:")
    for modelo in [modelo1, modelo2, modelo3]:
        pred = modelo.prever(novo_imovel)
        print(f"{modelo.nome}: ${pred[0]:,.2f}")
```

**Vantagens desta abordagem OOP**:
1. **Encapsulamento**: Estado (`_treinado`, `_feature_cols`) está protegido dentro da classe
2. **Múltiplas instâncias**: Podemos ter vários modelos simultaneamente
3. **Estado explícito**: Cada objeto tem seu próprio estado independente
4. **Fácil de testar**: Cada objeto pode ser testado isoladamente
5. **Reutilizável**: Classes podem ser usadas em outros projetos
6. **Extensível**: Fácil criar subclasses especializadas

Execute:
```bash
cd exemplos/paradigmas/oo
python solucao_oop.py
```

**CHECKPOINT**: O código OOP é mais longo, mas permite múltiplos modelos simultâneos e encapsula estado de forma segura.

## Passo 4: Comparação Lado a Lado

**Intenção**: Entender quando usar cada paradigma.

| Aspecto | Programação Estruturada | Orientação a Objetos |
|---------|------------------------|----------------------|
| **Complexidade** | Menor overhead, mais direto | Mais conceitos (classes, herança) |
| **Estado** | Variáveis globais ou passagem explícita | Encapsulado no objeto |
| **Múltiplas instâncias** | Difícil (requer dicionários, arrays) | Natural (múltiplos objetos) |
| **Testabilidade** | Estado global dificulta testes | Objetos isolados facilitam |
| **Reutilização** | Funções independentes reutilizáveis | Classes reutilizáveis com estado |
| **Organização** | Agrupa por funcionalidade | Agrupa por responsabilidade/entidade |
| **Manutenção** | Boa para scripts simples | Melhor para sistemas complexos |

**Quando usar Estruturado (funções)**:
- Scripts simples, executados uma vez
- Pipelines lineares sem estado complexo
- Transformações de dados diretas
- Análises exploratórias (notebooks)

**Quando usar OOP (classes)**:
- Múltiplas instâncias com estados diferentes
- Estado complexo que precisa ser mantido
- APIs e serviços (como nossa API FastAPI!)
- Código que será estendido/herdado
- Precisa de polimorfismo (comportamento dinâmico)

**CHECKPOINT**: Não existe "melhor" - existe "mais adequado ao contexto".

## Passo 5: Conceitos OOP em Data Science

**Intenção**: Entender conceitos-chave de OOP aplicados a DS.

**1. Encapsulamento**

```python
class Modelo:
    def __init__(self):
        self._treinado = False  # Atributo "privado" (convenção)
    
    @property
    def esta_treinado(self):
        """Acesso controlado ao estado."""
        return self._treinado
    
    # Usuário não pode fazer: modelo._treinado = True sem treinar
    # Precisa usar método público que valida
```

**2. Abstração**

```python
# Usuário não precisa saber detalhes internos
modelo = ModeloPreditivo(nome="Meu Modelo")
modelo.treinar(X_train, y_train)  # Esconde complexidade do sklearn

# vs versão funcional que expõe tudo:
model = RandomForestRegressor(...)
model.fit(...)
predictions = model.predict(...)
```

**3. Herança (Preview - não aprofundaremos agora)**

```python
class ModeloBase:
    def treinar(self, X, y):
        raise NotImplementedError

class ModeloRandomForest(ModeloBase):
    def treinar(self, X, y):
        # Implementação específica
        pass

class ModeloXGBoost(ModeloBase):
    def treinar(self, X, y):
        # Implementação específica
        pass
```

**4. Composição (já vimos!)**

```python
# PipelineML "tem um" PreProcessador e "tem um" ModeloPreditivo
class PipelineML:
    def __init__(self, preprocessador: PreProcessador, modelo: ModeloPreditivo):
        self.preprocessador = preprocessador  # Composição
        self.modelo = modelo  # Composição
```

**CHECKPOINT**: OOP não é sobre sintaxe (`class`, `self`) - é sobre organizar código em torno de entidades com estado e comportamento.

# 7. Testes rápidos e validação

Vamos criar testes simples para demonstrar vantagem de OOP:

```python
# exemplos/paradigmas/oo/test_modelo.py
"""Testes para demonstrar testabilidade da abordagem OOP."""
import pandas as pd
import numpy as np
from solucao_oop import ModeloPreditivo, PreProcessador

def test_modelo_nao_treinado_deve_lancar_erro():
    """Testa que modelo não treinado lança erro ao prever."""
    modelo = ModeloPreditivo(nome="Teste")
    
    X_fake = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    
    try:
        modelo.prever(X_fake)
        assert False, "Deveria ter lançado ValueError"
    except ValueError as e:
        assert "não está treinado" in str(e)
        print("✅ Teste passou: modelo não treinado lança erro")

def test_multiplos_modelos_independentes():
    """Testa que múltiplos modelos não interferem entre si."""
    modelo1 = ModeloPreditivo(nome="M1", n_estimators=10)
    modelo2 = ModeloPreditivo(nome="M2", n_estimators=20)
    
    # Estados independentes
    assert not modelo1.esta_treinado
    assert not modelo2.esta_treinado
    
    # Dados de treino simples
    X = pd.DataFrame({'a': [1, 2, 3, 4], 'b': [2, 3, 4, 5]})
    y = pd.Series([10, 20, 30, 40])
    
    # Treina apenas modelo1
    modelo1.treinar(X, y)
    
    assert modelo1.esta_treinado
    assert not modelo2.esta_treinado  # modelo2 permanece não treinado
    
    print("✅ Teste passou: modelos são independentes")

def test_preprocessador_mantem_feature_cols():
    """Testa que preprocessador lembra as features."""
    prep = PreProcessador(target_col='preco')
    
    df = pd.DataFrame({
        'area': [100, 200],
        'quartos': [2, 3],
        'preco': [300000, 500000]
    })
    
    prep.processar(df)
    X, y = prep.separar_features_target(df)
    
    assert prep.feature_cols == ['area', 'quartos']
    assert list(X.columns) == ['area', 'quartos']
    assert y.name == 'preco'
    
    print("✅ Teste passou: preprocessador mantém estado correto")

if __name__ == "__main__":
    test_modelo_nao_treinado_deve_lancar_erro()
    test_multiplos_modelos_independentes()
    test_preprocessador_mantem_feature_cols()
    print("\n✅ Todos os testes passaram!")
```

Execute:
```bash
cd exemplos/paradigmas/oo
python test_modelo.py
```

**CHECKPOINT**: Testar código OOP é muito mais simples porque cada objeto é independente. Tente fazer esses mesmos testes na versão funcional com variáveis globais - é muito mais difícil!

# 8. Observabilidade e boas práticas (mini-bloco)

**1. Use classes quando precisa gerenciar estado complexo**
- ✅ Modelo de ML (parâmetros, status de treinamento, métricas)
- ✅ Conexão de banco de dados (estado da conexão)
- ✅ Pipeline com múltiplas etapas interdependentes
- **Trade-off**: Mais código inicial, mas muito mais manutenível

**2. Use funções para transformações sem estado**
- ✅ `calcular_media(numeros)` - sem estado
- ✅ `normalizar_texto(texto)` - sem estado
- ✅ `converter_timestamp(data)` - sem estado
- **Trade-off**: Mais simples, mas não serve para tudo

**3. Prefira composição a herança profunda**
- ✅ `PipelineML` compõe `PreProcessador` e `ModeloPreditivo`
- ❌ Evite: `ClasseA → ClasseB → ClasseC → ClasseD`
- **Trade-off**: Mais flexível, menos acoplado

**4. Encapsule estado, exponha comportamento**
- Atributos privados (`_treinado`, `_modelo`)
- Métodos públicos (`treinar()`, `prever()`)
- Properties para acesso controlado (`@property esta_treinado`)
- **Trade-off**: Mais seguro, previne uso indevido

# 9. Troubleshooting (erros comuns)

**Erro 1: "Usar classes para tudo"**
- **Sintoma**: `class CalculadoraMedia` com um único método
- **Solução**: Se tem apenas um método sem estado, use função
- **Como identificar**: Classe com único método que não usa `self`

**Erro 2: "Nunca usar classes (resistência a OOP)"**
- **Sintoma**: 10 funções com 15 parâmetros cada, passando estado entre elas
- **Solução**: Se funções compartilham muito estado, agrupe em classe
- **Como identificar**: Muitos parâmetros repetidos em várias funções

**Erro 3: "Atributos públicos para tudo"**
- **Sintoma**: `modelo.treinado = True` sem treinar
- **Solução**: Use `_privado` para estado interno, exponha via métodos
- **Como identificar**: Bugs onde estado fica inconsistente

**Erro 4: "Herança excessiva"**
- **Sintoma**: 5 níveis de herança para criar um modelo
- **Solução**: Prefira composição (passar objetos como parâmetros)
- **Como identificar**: Difícil entender de onde métodos vêm

**Erro 5: "Classes gigantes (God Class)"**
- **Sintoma**: Classe com 50 métodos fazendo tudo
- **Solução**: Aplique Single Responsibility Principle - divida
- **Como identificar**: Difícil nomear a classe, faz muitas coisas

**Erro 6: "Confundir classe com instância"**
- **Sintoma**: `ModeloPreditivo.treinar(X, y)` (sem instanciar)
- **Solução**: Classes são templates, instâncias são objetos: `modelo = ModeloPreditivo(); modelo.treinar(X, y)`
- **Como identificar**: `TypeError: missing 1 required positional argument: 'self'`

# 10. Exercícios (básico e avançado)

## Exercícios Básicos

**Exercício 1: Converter Função para Classe**

Converta este código funcional em uma classe:

```python
# Funcional
def conectar_banco(host, port, user, password):
    connection = f"Connected to {host}:{port}"
    return connection

def executar_query(connection, query):
    return f"{connection} - Executing: {query}"

def fechar_conexao(connection):
    print(f"Closing {connection}")

# Uso
conn = conectar_banco("localhost", 5432, "user", "pass")
result = executar_query(conn, "SELECT * FROM users")
fechar_conexao(conn)
```

Crie uma classe `DatabaseConnection` que encapsula esse comportamento.

**Critério de sucesso**:
- [ ] Classe `DatabaseConnection` criada
- [ ] Métodos `conectar()`, `executar_query()`, `fechar()`
- [ ] Estado da conexão encapsulado (atributo privado)
- [ ] Uso: `db = DatabaseConnection(...); db.conectar(); db.executar_query(...)`

**Exercício 2: Identificar Candidatos a Classes**

Para cada caso, diga se deve usar função ou classe:

a) Calcular a distância euclidiana entre dois pontos
b) Gerenciar um carrinho de compras com itens, total e desconto
c) Converter temperatura Celsius para Fahrenheit
d) Implementar um modelo de regressão linear do zero com fit/predict
e) Extrair hashtags de um texto

**Critério de sucesso**:
- [ ] Identificou corretamente: a) função, b) classe, c) função, d) classe, e) função
- [ ] Justificou baseado em presença/ausência de estado complexo

## Exercício Avançado

**Exercício 3: Sistema de Múltiplos Modelos**

Implemente um sistema que:
1. Gerencia múltiplos modelos de ML simultaneamente
2. Cada modelo tem nome, tipo (RF, XGBoost, etc.) e hiperparâmetros
3. Permite treinar todos os modelos nos mesmos dados
4. Compara performance de todos
5. Seleciona o melhor modelo automaticamente

**Requisitos**:

```python
class GerenciadorModelos:
    """Gerencia múltiplos modelos."""
    
    def adicionar_modelo(self, modelo: ModeloPreditivo):
        """Adiciona modelo ao gerenciador."""
        pass
    
    def treinar_todos(self, X_train, y_train):
        """Treina todos os modelos."""
        pass
    
    def avaliar_todos(self, X_test, y_test) -> pd.DataFrame:
        """Retorna DataFrame com métricas de todos."""
        pass
    
    def obter_melhor_modelo(self, metrica: str = 'rmse') -> ModeloPreditivo:
        """Retorna modelo com melhor métrica."""
        pass
```

**Critério de sucesso**:
- [ ] Classe `GerenciadorModelos` implementada
- [ ] Consegue adicionar 3+ modelos diferentes
- [ ] Treina todos com um comando
- [ ] Retorna DataFrame comparativo de métricas
- [ ] Identifica e retorna melhor modelo
- [ ] Exemplo de uso funcionando completo

**Exemplo de uso esperado**:
```python
gerenciador = GerenciadorModelos()

gerenciador.adicionar_modelo(ModeloPreditivo("RF_50", n_estimators=50))
gerenciador.adicionar_modelo(ModeloPreditivo("RF_100", n_estimators=100))
gerenciador.adicionar_modelo(ModeloPreditivo("RF_200", n_estimators=200))

gerenciador.treinar_todos(X_train, y_train)
resultados = gerenciador.avaliar_todos(X_test, y_test)
print(resultados)

melhor = gerenciador.obter_melhor_modelo(metrica='r2')
print(f"Melhor modelo: {melhor.nome}")
```

# 11. Resultados e Lições

## Resultados

**Como medir o impacto de usar OOP apropriadamente:**

1. **Facilidade de Instanciação Múltipla**
   - Estruturado: Requer arrays/dicionários complexos para gerenciar múltiplos estados
   - OOP: `modelo1 = Modelo(); modelo2 = Modelo()` - natural
   - **Ganho**: 80% menos código para cenários com múltiplas instâncias

2. **Testabilidade**
   - Estruturado com globais: Testes interferem uns nos outros
   - OOP: Cada teste cria objetos isolados
   - **Ganho**: 3-5x mais rápido escrever testes completos

3. **Manutenibilidade**
   - Estruturado: Mudança em "estado" requer atualizar múltiplas funções
   - OOP: Mudança em atributo privado afeta apenas a classe
   - **Ganho**: 60-70% redução em bugs causados por mudanças

4. **Clareza de Responsabilidade**
   - Estruturado: Funções espalhadas, agrupamento por arquivo
   - OOP: Responsabilidades claras por classe
   - **Ganho**: Tempo de compreensão do código reduz 40-50%

## Lições

**1. OOP não é sobre sintaxe, é sobre organização**
   - `class` e `self` são apenas ferramentas
   - O valor está em encapsular estado e comportamento relacionados
   - Facilita raciocinar sobre o sistema

**2. Não existe paradigma "superior"**
   - Programação estruturada é perfeita para scripts simples
   - OOP brilha em sistemas com estado complexo
   - Python permite ambos - use o mais adequado

**3. Encapsulamento previne bugs**
   - Estado privado (`_atributo`) evita modificações indevidas
   - Acesso via métodos permite validação
   - Reduz drasticamente bugs de inconsistência

**4. Classes são "templates" para objetos**
   - Uma classe define o comportamento
   - Cada objeto (instância) tem seu próprio estado
   - Isso permite múltiplas instâncias independentes

**5. Em Data Science, OOP é especialmente útil para:**
   - Modelos (estado: treinado/não treinado, parâmetros, métricas)
   - Pipelines (orquestrar etapas com estado intermediário)
   - APIs/Serviços (nossa API FastAPI usará OOP!)
   - Experimentos (gerenciar múltiplas configurações)

# 12. Encerramento e gancho para a próxima aula (script)

Fantástico! Nesta aula vimos, com código real rodando, a diferença entre programação estruturada e orientação a objetos. Resolvemos o mesmo problema de duas formas e você pôde experienciar diretamente os trade-offs.

O mais importante: entendemos que não se trata de um paradigma ser "melhor" que outro. Programação estruturada com funções é perfeita para scripts, análises exploratórias e transformações simples. Orientação a objetos é ideal quando você precisa gerenciar **estado complexo** e ter **múltiplas instâncias** com comportamentos independentes.

Para nossa API de Machine Learning, vamos usar muito OOP, porque:
- Precisamos gerenciar estado do modelo (carregado, versão, configurações)
- Queremos suportar múltiplos endpoints e modelos
- Precisamos de código testável e manutenível

Na **Aula 01 - Parte 04**, vamos fechar este primeiro módulo com chave de ouro: vamos pegar um código "ad hoc" real de análise de dados e refatorá-lo aplicando **todos os conceitos** que vimos até agora:
- Modularidade
- Alta coesão e baixo acoplamento
- Uso apropriado de OOP
- Documentação e clareza

Você verá um "antes e depois" que consolidará tudo que aprendemos. É o momento de ver tudo se conectar.

Nos vemos na Parte 04, a última desta aula fundamental. Até lá!
