---
titulo: "Aula 01 – Parte 04: Aplicando Fundamentos em Projeto de DS"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 15
prerequisitos:
  - "Python 3.12+"
  - "Conceitos de Aula 01 - Partes 01, 02 e 03"
  - "Ambiente virtual configurado"
  - "scikit-learn, pandas, numpy instalados"
tags: ["refatoracao", "boas-praticas", "caso-pratico", "projeto-real", "integração"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula, vamos colocar em prática absolutamente tudo que aprendemos até agora neste módulo de fundamentos. Se nas aulas anteriores vimos conceitos isolados, agora vamos integrá-los em um caso prático completo.

Você vai experienciar o "antes e depois" de um código real de Data Science. Vamos pegar um script típico que você poderia encontrar em qualquer empresa - aquele script "ad hoc" que funciona mas é um pesadelo de manter - e vamos transformá-lo em um projeto estruturado, modular e profissional.

Este é o momento onde tudo se conecta. Você verá como modularidade, coesão, baixo acoplamento e OOP trabalham juntos para transformar código caótico em código elegante. Mais importante: você terá um template mental que poderá aplicar em todos os seus projetos futuros.

É uma aula curta mas densa. Ao final, você terá um exemplo completo de como aplicar engenharia de software em um projeto de ciência de dados do mundo real.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você recebe um projeto de análise de dados para dar manutenção. O código "funciona" - gera relatórios, treina modelos, faz predições. Mas é um único arquivo de 600 linhas, `analise_completa.py`, sem documentação, com funções gigantes, variáveis espalhadas, lógica de negócio misturada com I/O, caminhos hardcoded. O desenvolvedor original saiu da empresa há 6 meses. Seu trabalho: adicionar suporte para uma nova fonte de dados e um novo tipo de relatório.

**Agitação**: Você passa 3 dias apenas tentando entender o que o código faz. Cada tentativa de modificação quebra algo inesperado. Os testes? Não existem. A documentação? Um comentário no topo dizendo "# Código de análise". Você precisa ler as 600 linhas linha por linha. Descobre que mudanças em uma parte afetam outras de forma não óbvia. Existem 5 funções chamadas `process_data`, `process_data2`, `process_data_final`, etc. Variáveis globais são modificadas em 20 lugares diferentes. É impossível testar componentes isoladamente. A frustração é enorme.

**Solução**: Você decide: antes de adicionar a nova funcionalidade, vamos refatorar isso corretamente. Aplica os princípios de engenharia de software: divide em módulos com responsabilidades claras, encapsula lógica em classes, remove acoplamento, adiciona documentação mínima, cria estrutura de projeto adequada. O "novo" código é maior em número de arquivos, mas infinitamente mais claro, testável e extensível. Adicionar a nova funcionalidade, que parecia impossível, agora é apenas criar um novo módulo e integrá-lo. Trabalho de 3 dias se torna 3 horas.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Identificar** problemas de engenharia em código "ad hoc" real de Data Science
2. **Aplicar** princípios de modularidade, coesão e acoplamento em refatoração prática
3. **Estruturar** um projeto de DS com separação clara de responsabilidades
4. **Documentar** código de forma mínima mas suficiente para manutenibilidade
5. **Integrar** todos os conceitos de engenharia de software vistos no módulo
6. **Avaliar** o impacto de boas práticas na qualidade e manutenibilidade do código

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+
- UV instalado
- Ambiente virtual ativo
- Bibliotecas: pandas, numpy, scikit-learn, matplotlib

**Setup:**

```bash
# Ativar ambiente virtual
cd c:\Users\diogomiyake\projects\SWE-4-DS\swe4ds-api-project
.venv\Scripts\activate

# Instalar matplotlib com UV (se ainda não tiver)
uv pip install matplotlib

# Criar pasta para o caso prático
mkdir -p exemplos/refatoracao
cd exemplos/refatoracao
```

**Checklist de Setup:**
- [ ] Ambiente virtual ativo (`.venv`)
- [ ] Todas as bibliotecas instaladas (pandas, numpy, sklearn, matplotlib)
- [ ] Pasta `exemplos/refatoracao` criada

# 5. Visão geral do que já existe no projeto (continuidade)

Estrutura atual do projeto:

```
swe4ds-api-project/
├── .venv/                   
├── exemplos/
│   ├── modularidade/       (Aula 01 - Parte 02)
│   ├── coesao/             (Aula 01 - Parte 02)
│   ├── acoplamento/        (Aula 01 - Parte 02)
│   ├── paradigmas/         (Aula 01 - Parte 03)
│   └── refatoracao/        # [NOVO] Caso prático desta aula
│       ├── antes/          # Código original (problemático)
│       └── depois/         # Código refatorado (boas práticas)
└── (estrutura da API - a partir da Aula 02)
```

Vamos criar um "antes" e "depois" claros para comparação direta.

# 6. Passo a passo (comandos + código)

## Passo 1: O Código "Antes" (Ad Hoc)

**Intenção**: Ver um exemplo realista de código problemático que precisa refatoração.

```python
# exemplos/refatoracao/antes/analise_completa.py
"""
# Código de análise
# Autor: Desconhecido
# Última modificação: 6 meses atrás
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Variáveis globais
df = None
model = None
trained = False
features = []

def load_data():
    global df
    # Caminho hardcoded
    df = pd.read_csv('C:/Users/antigo/dados/customer_data.csv')
    print(len(df))

def clean_data():
    global df
    df = df.dropna()
    df = df[df['age'] > 0]
    df = df[df['age'] < 120]
    df = df[df['income'] > 0]
    df['income'] = df['income'].fillna(df['income'].mean())
    df['education'] = df['education'].fillna('unknown')
    
def create_features():
    global df, features
    df['income_age_ratio'] = df['income'] / df['age']
    df['age_group'] = pd.cut(df['age'], bins=[0, 25, 45, 65, 120], labels=['young', 'adult', 'middle', 'senior'])
    df = pd.get_dummies(df, columns=['education', 'age_group'])
    df['high_value'] = (df['income'] > 100000).astype(int)
    features = [c for c in df.columns if c not in ['customer_id', 'churn']]

def split_data():
    global df, features
    X = df[features]
    y = df['churn']
    return train_test_split(X, y, test_size=0.3, random_state=42)

def train_model(X_train, y_train):
    global model, trained
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10, min_samples_split=5)
    model.fit(X_train, y_train)
    trained = True
    print('model trained')

def evaluate(X_test, y_test):
    global model, trained
    if not trained:
        print('ERROR: model not trained')
        return
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f'accuracy: {acc}')
    print(classification_report(y_test, y_pred))
    
def plot_feature_importance():
    global model, features
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    plt.figure(figsize=(12, 6))
    plt.title('Feature Importances')
    plt.bar(range(len(importances)), importances[indices])
    plt.xticks(range(len(importances)), [features[i] for i in indices], rotation=90)
    plt.tight_layout()
    plt.savefig('feature_importance.png')
    print('plot saved')

def predict_new_customer(age, income, education):
    global model, trained, df
    if not trained:
        print('ERROR: train first')
        return None
    
    # Precisa recriar TODAS as features
    new_data = pd.DataFrame({
        'age': [age],
        'income': [income],
        'education': [education],
        'customer_id': [0]
    })
    
    new_data['income_age_ratio'] = new_data['income'] / new_data['age']
    new_data['age_group'] = pd.cut(new_data['age'], bins=[0, 25, 45, 65, 120], labels=['young', 'adult', 'middle', 'senior'])
    new_data = pd.get_dummies(new_data, columns=['education', 'age_group'])
    new_data['high_value'] = (new_data['income'] > 100000).astype(int)
    
    # Problema: precisa ter EXATAMENTE as mesmas colunas
    for col in features:
        if col not in new_data.columns:
            new_data[col] = 0
    
    new_data = new_data[features]
    pred = model.predict(new_data)[0]
    return 'Churn' if pred == 1 else 'No Churn'

def generate_report():
    global df
    print('=== REPORT ===')
    print(f'Total customers: {len(df)}')
    print(f'Churn rate: {df["churn"].mean():.2%}')
    print(f'Avg income: ${df["income"].mean():,.2f}')
    print(f'Avg age: {df["age"].mean():.1f}')

def main():
    load_data()
    clean_data()
    create_features()
    X_train, X_test, y_train, y_test = split_data()
    train_model(X_train, y_train)
    evaluate(X_test, y_test)
    plot_feature_importance()
    generate_report()
    
    # Teste predição
    result = predict_new_customer(35, 75000, 'bachelor')
    print(f'Prediction: {result}')

if __name__ == '__main__':
    main()
```

**Problemas identificados** (conte quantos você consegue identificar):
1. ❌ Variáveis globais por toda parte
2. ❌ Caminhos hardcoded
3. ❌ Funções modificam estado global (side effects)
4. ❌ Lógica de feature engineering duplicada
5. ❌ Impossível testar componentes isoladamente
6. ❌ Sem documentação adequada
7. ❌ Funções fazem múltiplas coisas (baixa coesão)
8. ❌ Acoplamento altíssimo (tudo depende de tudo)
9. ❌ Warnings silenciados (esconde problemas)
10. ❌ Print em vez de logging apropriado
11. ❌ Sem tratamento de erros
12. ❌ Nomes genéricos (df, model, features)

**CHECKPOINT**: Você consegue identificar pelo menos 8 dos 12 problemas? Se sim, você assimilou os conceitos!

## Passo 2: Planejando a Refatoração

**Intenção**: Antes de refatorar, planejar a estrutura desejada.

**Análise de responsabilidades:**

1. **Carregar dados** → `DataLoader`
2. **Limpar dados** → `DataCleaner`
3. **Feature engineering** → `FeatureEngineer`
4. **Treinar/avaliar modelo** → `ChurnPredictor`
5. **Gerar relatórios** → `ReportGenerator`
6. **Orquestrar tudo** → `ChurnAnalysisPipeline`

**Estrutura de arquivos planejada:**

```
exemplos/refatoracao/depois/
├── config.py              # Configurações centralizadas
├── data_loader.py         # Responsável por I/O
├── data_cleaner.py        # Limpeza de dados
├── feature_engineer.py    # Feature engineering
├── churn_predictor.py     # Modelo de ML
├── report_generator.py    # Geração de relatórios
├── pipeline.py            # Orquestração
└── main.py                # Ponto de entrada
```

**CHECKPOINT**: Estrutura clara, cada módulo com responsabilidade única (alta coesão).

## Passo 3: Código "Depois" (Refatorado)

**Intenção**: Implementar a solução aplicando todos os princípios.

```python
# exemplos/refatoracao/depois/config.py
"""Configurações centralizadas do projeto."""
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    """Configurações da aplicação."""
    
    # Caminhos
    data_path: Path = Path('./data/customer_data.csv')
    output_dir: Path = Path('./output')
    
    # Parâmetros do modelo
    test_size: float = 0.3
    random_state: int = 42
    n_estimators: int = 100
    max_depth: int = 10
    min_samples_split: int = 5
    
    # Parâmetros de features
    age_bins: list = None
    age_labels: list = None
    high_income_threshold: int = 100000
    
    def __post_init__(self):
        """Inicializa valores padrão complexos."""
        if self.age_bins is None:
            self.age_bins = [0, 25, 45, 65, 120]
        if self.age_labels is None:
            self.age_labels = ['young', 'adult', 'middle', 'senior']
        
        # Garante que diretórios existem
        self.output_dir.mkdir(parents=True, exist_ok=True)
```

```python
# exemplos/refatoracao/depois/data_loader.py
"""Módulo responsável por carregar dados."""
import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """Carrega dados de diferentes fontes."""
    
    def __init__(self, data_path: Path):
        """
        Inicializa loader.
        
        Args:
            data_path: Caminho para arquivo de dados
        """
        self.data_path = Path(data_path)
    
    def load(self) -> pd.DataFrame:
        """
        Carrega dados de CSV.
        
        Returns:
            DataFrame com dados carregados
            
        Raises:
            FileNotFoundError: Se arquivo não existe
            ValueError: Se arquivo está vazio ou mal formatado
        """
        if not self.data_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.data_path}")
        
        try:
            df = pd.read_csv(self.data_path)
            logger.info(f"Dados carregados: {len(df)} registros de {self.data_path}")
            
            if df.empty:
                raise ValueError("Arquivo está vazio")
            
            return df
        
        except pd.errors.EmptyDataError:
            raise ValueError(f"Arquivo CSV vazio: {self.data_path}")
        except Exception as e:
            raise ValueError(f"Erro ao ler CSV: {e}")
```

```python
# exemplos/refatoracao/depois/data_cleaner.py
"""Módulo responsável por limpeza de dados."""
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class DataCleaner:
    """Aplica regras de limpeza nos dados."""
    
    def __init__(self, age_min: int = 0, age_max: int = 120):
        """
        Inicializa cleaner.
        
        Args:
            age_min: Idade mínima válida
            age_max: Idade máxima válida
        """
        self.age_min = age_min
        self.age_max = age_max
    
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica todas as regras de limpeza.
        
        Args:
            df: DataFrame original
            
        Returns:
            DataFrame limpo
        """
        n_original = len(df)
        
        df = self._remove_duplicates(df)
        df = self._remove_nulls(df)
        df = self._fix_age(df)
        df = self._fix_income(df)
        df = self._fix_education(df)
        
        n_final = len(df)
        logger.info(f"Limpeza concluída: {n_original} → {n_final} registros ({n_original - n_final} removidos)")
        
        return df
    
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove registros duplicados."""
        return df.drop_duplicates()
    
    def _remove_nulls(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove linhas com nulos em colunas críticas."""
        critical_cols = ['customer_id', 'age', 'churn']
        return df.dropna(subset=critical_cols)
    
    def _fix_age(self, df: pd.DataFrame) -> pd.DataFrame:
        """Corrige valores de idade."""
        if 'age' not in df.columns:
            return df
        
        # Filtra idades válidas
        df = df[(df['age'] > self.age_min) & (df['age'] < self.age_max)]
        return df
    
    def _fix_income(self, df: pd.DataFrame) -> pd.DataFrame:
        """Corrige valores de income."""
        if 'income' not in df.columns:
            return df
        
        # Remove valores negativos
        df = df[df['income'] > 0]
        
        # Preenche nulos com mediana
        if df['income'].isnull().any():
            median_income = df['income'].median()
            df['income'] = df['income'].fillna(median_income)
            logger.info(f"Income nulos preenchidos com mediana: ${median_income:,.2f}")
        
        return df
    
    def _fix_education(self, df: pd.DataFrame) -> pd.DataFrame:
        """Corrige valores de education."""
        if 'education' not in df.columns:
            return df
        
        df['education'] = df['education'].fillna('unknown')
        return df
```

```python
# exemplos/refatoracao/depois/feature_engineer.py
"""Módulo responsável por feature engineering."""
import pandas as pd
import logging
from typing import List

logger = logging.getLogger(__name__)

class FeatureEngineer:
    """Cria features derivadas dos dados."""
    
    def __init__(self, age_bins: List[int], age_labels: List[str], 
                 high_income_threshold: int):
        """
        Inicializa engineer.
        
        Args:
            age_bins: Limites para binning de idade
            age_labels: Labels para grupos de idade
            high_income_threshold: Threshold para flag de alto income
        """
        self.age_bins = age_bins
        self.age_labels = age_labels
        self.high_income_threshold = high_income_threshold
        self.feature_names: List[str] = []
    
    def engineer(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica todas as transformações de features.
        
        Args:
            df: DataFrame com dados limpos
            
        Returns:
            DataFrame com features engineered
        """
        logger.info("Iniciando feature engineering...")
        
        df = self._create_ratio_features(df)
        df = self._create_age_groups(df)
        df = self._create_binary_flags(df)
        df = self._encode_categorical(df)
        
        self._define_feature_names(df)
        
        logger.info(f"Features criadas: {len(self.feature_names)} features")
        return df
    
    def _create_ratio_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cria features de razão."""
        if 'income' in df.columns and 'age' in df.columns:
            df['income_age_ratio'] = df['income'] / df['age']
        return df
    
    def _create_age_groups(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cria grupos etários."""
        if 'age' in df.columns:
            df['age_group'] = pd.cut(df['age'], bins=self.age_bins, labels=self.age_labels)
        return df
    
    def _create_binary_flags(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cria flags binárias."""
        if 'income' in df.columns:
            df['high_value'] = (df['income'] > self.high_income_threshold).astype(int)
        return df
    
    def _encode_categorical(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica one-hot encoding."""
        categorical_cols = ['education', 'age_group']
        existing_cols = [col for col in categorical_cols if col in df.columns]
        
        if existing_cols:
            df = pd.get_dummies(df, columns=existing_cols, drop_first=False)
        
        return df
    
    def _define_feature_names(self, df: pd.DataFrame) -> None:
        """Define lista de nomes de features."""
        exclude = ['customer_id', 'churn']
        self.feature_names = [col for col in df.columns if col not in exclude]
    
    def transform_new_data(self, df_new: pd.DataFrame, 
                          reference_features: List[str]) -> pd.DataFrame:
        """
        Transforma novos dados garantindo compatibilidade.
        
        Args:
            df_new: Novos dados
            reference_features: Features esperadas (do treino)
            
        Returns:
            DataFrame transformado
        """
        # Aplica as mesmas transformações
        df_new = self._create_ratio_features(df_new)
        df_new = self._create_age_groups(df_new)
        df_new = self._create_binary_flags(df_new)
        df_new = self._encode_categorical(df_new)
        
        # Garante mesmas colunas que o treino
        for col in reference_features:
            if col not in df_new.columns:
                df_new[col] = 0
        
        # Remove colunas extras e reordena
        df_new = df_new[reference_features]
        
        return df_new
```

```python
# exemplos/refatoracao/depois/churn_predictor.py
"""Módulo responsável pelo modelo de predição de churn."""
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from typing import Tuple, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ChurnPredictor:
    """Modelo de predição de churn de clientes."""
    
    def __init__(self, n_estimators: int = 100, max_depth: int = 10, 
                 min_samples_split: int = 5, random_state: int = 42):
        """
        Inicializa preditor.
        
        Args:
            n_estimators: Número de árvores
            max_depth: Profundidade máxima das árvores
            min_samples_split: Mínimo de samples para split
            random_state: Seed para reprodutibilidade
        """
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=random_state,
            n_jobs=-1
        )
        self._is_trained = False
        self._feature_names: Optional[list] = None
    
    @property
    def is_trained(self) -> bool:
        """Verifica se modelo está treinado."""
        return self._is_trained
    
    @property
    def feature_names(self) -> list:
        """Retorna nomes das features."""
        if not self._is_trained:
            raise ValueError("Modelo não treinado")
        return self._feature_names
    
    def train(self, X: pd.DataFrame, y: pd.Series) -> None:
        """
        Treina o modelo.
        
        Args:
            X: Features de treino
            y: Target de treino
        """
        logger.info(f"Treinando modelo com {len(X)} samples...")
        
        self._feature_names = list(X.columns)
        self.model.fit(X, y)
        self._is_trained = True
        
        logger.info("Treinamento concluído")
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Faz predições.
        
        Args:
            X: Features para predição
            
        Returns:
            Array de predições
        """
        if not self._is_trained:
            raise ValueError("Modelo não está treinado")
        
        return self.model.predict(X)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Retorna probabilidades das predições."""
        if not self._is_trained:
            raise ValueError("Modelo não está treinado")
        
        return self.model.predict_proba(X)
    
    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> Dict:
        """
        Avalia performance do modelo.
        
        Args:
            X_test: Features de teste
            y_test: Target de teste
            
        Returns:
            Dicionário com métricas
        """
        y_pred = self.predict(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        logger.info(f"Acurácia: {metrics['accuracy']:.3f}")
        
        return metrics
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Retorna importância das features.
        
        Returns:
            DataFrame com features e importâncias
        """
        if not self._is_trained:
            raise ValueError("Modelo não está treinado")
        
        importances = self.model.feature_importances_
        
        df_importance = pd.DataFrame({
            'feature': self._feature_names,
            'importance': importances
        }).sort_values('importance', ascending=False)
        
        return df_importance
```

```python
# exemplos/refatoracao/depois/report_generator.py
"""Módulo responsável por geração de relatórios."""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Gera relatórios e visualizações."""
    
    def __init__(self, output_dir: Path):
        """
        Inicializa gerador.
        
        Args:
            output_dir: Diretório para salvar outputs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_summary(self, df: pd.DataFrame) -> Dict:
        """
        Gera resumo estatístico dos dados.
        
        Args:
            df: DataFrame com dados
            
        Returns:
            Dicionário com estatísticas
        """
        summary = {
            'total_customers': len(df),
            'churn_rate': df['churn'].mean() if 'churn' in df.columns else None,
            'avg_income': df['income'].mean() if 'income' in df.columns else None,
            'avg_age': df['age'].mean() if 'age' in df.columns else None
        }
        
        logger.info("Resumo estatístico gerado")
        return summary
    
    def print_summary(self, summary: Dict) -> None:
        """Imprime resumo formatado."""
        print("\n=== RELATÓRIO DE ANÁLISE ===")
        print(f"Total de clientes: {summary['total_customers']:,}")
        
        if summary['churn_rate'] is not None:
            print(f"Taxa de churn: {summary['churn_rate']:.2%}")
        
        if summary['avg_income'] is not None:
            print(f"Income médio: ${summary['avg_income']:,.2f}")
        
        if summary['avg_age'] is not None:
            print(f"Idade média: {summary['avg_age']:.1f} anos")
    
    def plot_feature_importance(self, importance_df: pd.DataFrame, 
                                top_n: int = 15) -> Path:
        """
        Plota importância das features.
        
        Args:
            importance_df: DataFrame com features e importâncias
            top_n: Número de top features a mostrar
            
        Returns:
            Caminho do arquivo salvo
        """
        top_features = importance_df.head(top_n)
        
        plt.figure(figsize=(10, 6))
        plt.barh(top_features['feature'], top_features['importance'])
        plt.xlabel('Importância')
        plt.title(f'Top {top_n} Features Mais Importantes')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        
        output_path = self.output_dir / 'feature_importance.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info(f"Gráfico salvo em: {output_path}")
        return output_path
```

```python
# exemplos/refatoracao/depois/pipeline.py
"""Pipeline principal que orquestra todo o processo."""
import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path
import logging
from typing import Dict

from config import Config
from data_loader import DataLoader
from data_cleaner import DataCleaner
from feature_engineer import FeatureEngineer
from churn_predictor import ChurnPredictor
from report_generator import ReportGenerator

logger = logging.getLogger(__name__)

class ChurnAnalysisPipeline:
    """Orquestra todo o processo de análise de churn."""
    
    def __init__(self, config: Config):
        """
        Inicializa pipeline.
        
        Args:
            config: Objeto de configuração
        """
        self.config = config
        
        # Inicializa componentes
        self.loader = DataLoader(config.data_path)
        self.cleaner = DataCleaner()
        self.engineer = FeatureEngineer(
            age_bins=config.age_bins,
            age_labels=config.age_labels,
            high_income_threshold=config.high_income_threshold
        )
        self.predictor = ChurnPredictor(
            n_estimators=config.n_estimators,
            max_depth=config.max_depth,
            min_samples_split=config.min_samples_split,
            random_state=config.random_state
        )
        self.reporter = ReportGenerator(config.output_dir)
    
    def run(self) -> Dict:
        """
        Executa pipeline completo.
        
        Returns:
            Dicionário com resultados e métricas
        """
        logger.info("=== Iniciando Pipeline de Análise de Churn ===")
        
        # 1. Carrega dados
        df = self.loader.load()
        
        # 2. Limpa dados
        df = self.cleaner.clean(df)
        
        # 3. Feature engineering
        df = self.engineer.engineer(df)
        
        # 4. Separa features e target
        X = df[self.engineer.feature_names]
        y = df['churn']
        
        # 5. Divide treino/teste
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=self.config.test_size,
            random_state=self.config.random_state
        )
        logger.info(f"Dados divididos: {len(X_train)} treino, {len(X_test)} teste")
        
        # 6. Treina modelo
        self.predictor.train(X_train, y_train)
        
        # 7. Avalia
        metrics = self.predictor.evaluate(X_test, y_test)
        
        # 8. Gera relatórios
        summary = self.reporter.generate_summary(df)
        self.reporter.print_summary(summary)
        
        importance = self.predictor.get_feature_importance()
        self.reporter.plot_feature_importance(importance)
        
        logger.info("=== Pipeline concluído com sucesso ===")
        
        return {
            'metrics': metrics,
            'summary': summary,
            'feature_importance': importance
        }
    
    def predict_customer(self, customer_data: Dict) -> str:
        """
        Prediz churn para um novo cliente.
        
        Args:
            customer_data: Dicionário com dados do cliente
            
        Returns:
            Predição ('Churn' ou 'No Churn')
        """
        if not self.predictor.is_trained:
            raise ValueError("Modelo não foi treinado. Execute run() primeiro.")
        
        # Cria DataFrame
        df_new = pd.DataFrame([customer_data])
        
        # Aplica mesmas transformações
        df_new = self.engineer.transform_new_data(
            df_new, 
            self.predictor.feature_names
        )
        
        # Prediz
        prediction = self.predictor.predict(df_new)[0]
        proba = self.predictor.predict_proba(df_new)[0]
        
        result = 'Churn' if prediction == 1 else 'No Churn'
        confidence = proba[1] if prediction == 1 else proba[0]
        
        logger.info(f"Predição: {result} (confiança: {confidence:.2%})")
        
        return result
```

```python
# exemplos/refatoracao/depois/main.py
"""Ponto de entrada da aplicação."""
import logging
from config import Config
from pipeline import ChurnAnalysisPipeline

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Função principal."""
    # Carrega configurações
    config = Config()
    
    # Cria e executa pipeline
    pipeline = ChurnAnalysisPipeline(config)
    results = pipeline.run()
    
    # Exemplo de predição
    print("\n=== Predição para Novo Cliente ===")
    novo_cliente = {
        'age': 35,
        'income': 75000,
        'education': 'bachelor',
        'customer_id': 99999
    }
    
    prediction = pipeline.predict_customer(novo_cliente)
    print(f"Cliente com {novo_cliente['age']} anos, income ${novo_cliente['income']:,}")
    print(f"Predição: {prediction}")

if __name__ == "__main__":
    main()
```

**Benefícios da refatoração**:
1. ✅ Cada módulo tem responsabilidade única (alta coesão)
2. ✅ Módulos independentes (baixo acoplamento)
3. ✅ Sem variáveis globais (estado encapsulado)
4. ✅ Configuração centralizada
5. ✅ Fácil de testar cada componente
6. ✅ Documentação adequada (docstrings)
7. ✅ Logging estruturado
8. ✅ Tratamento de erros
9. ✅ Extensível (fácil adicionar novas features/modelos)
10. ✅ Código profissional e manutenível

**CHECKPOINT**: Compare a estrutura. O código refatorado é maior, mas infinitamente mais claro e manutenível.

# 7. Testes rápidos e validação

**Para validar a qualidade da refatoração:**

1. **Teste de Isolamento**:
   - Consegue testar `DataCleaner` sem `DataLoader`? ✅ Sim
   - Consegue testar `ChurnPredictor` sem dados reais? ✅ Sim (mock)
   
2. **Teste de Extensibilidade**:
   - Adicionar nova fonte de dados? → Apenas modifique/crie novo `DataLoader`
   - Adicionar nova feature? → Apenas modifique `FeatureEngineer`
   - Trocar algoritmo? → Apenas modifique `ChurnPredictor`
   
3. **Teste de Compreensão**:
   - Tempo para novo desenvolvedor entender: Antes (horas), Depois (minutos)
   - Clareza de onde cada responsabilidade está: Antes (confuso), Depois (óbvio)

# 8. Observabilidade e boas práticas (mini-bloco)

**1. Configuração centralizada**
- Todas as configs em um só lugar
- Fácil mudar parâmetros sem tocar no código
- **Trade-off**: arquivo extra, mas manutenção 10x mais fácil

**2. Logging em vez de print**
- Níveis de log (INFO, WARNING, ERROR)
- Pode desligar/filtrar conforme necessário
- **Trade-off**: setup inicial, mas profissionalismo total

**3. Separação de responsabilidades**
- Cada classe faz uma coisa
- Mudanças ficam localizadas
- **Trade-off**: mais arquivos, mas cada um é simples

**4. Tratamento de erros explícito**
- Erros claros com mensagens úteis
- Sistema não quebra silenciosamente
- **Trade-off**: mais código, mas muito mais confiável

# 9. Troubleshooting (erros comuns)

**Erro 1: "Refatorar tudo de uma vez"**
- **Sintoma**: Projeto parado por semanas refatorando
- **Solução**: Refatore incrementalmente, mantendo funcionalidade
- **Como evitar**: Uma responsabilidade de cada vez

**Erro 2: "Criar arquivos demais"**
- **Sintoma**: 50 arquivos para 200 linhas de código
- **Solução**: Balance. Módulo deve ter ~100-500 linhas
- **Como evitar**: Se arquivo tem < 30 linhas, pode ser função em outro módulo

**Erro 3: "Não testar após refatoração"**
- **Sintoma**: Refatorou e quebrou funcionalidade
- **Solução**: Teste a cada mudança incremental
- **Como evitar**: Testes automatizados (próxima aula!)

**Erro 4: "Abstrair prematuramente"**
- **Sintoma**: Interfaces e hierarquias complexas antes de necessário
- **Solução**: Primeiro deixe funcionar, depois refatore
- **Como evitar**: YAGNI (You Aren't Gonna Need It)

# 10. Exercícios (básico e avançado)

## Exercício Básico

**Exercício 1: Análise de Problemas**

Pegue um script Python que você escreveu (ou use o código "antes" fornecido) e:

1. Liste todos os problemas de engenharia que identifica
2. Classifique cada problema: (coesão/acoplamento/modularidade/etc.)
3. Proponha estrutura refatorada com módulos e responsabilidades

**Critério de sucesso**:
- [ ] Identificou ≥ 5 problemas reais
- [ ] Classificou corretamente
- [ ] Estrutura proposta segue princípios de modularidade e coesão

## Exercício Avançado

**Exercício 2: Refatoração Completa**

Refatore um projeto real seu aplicando todos os conceitos:

1. **Estruture**: Crie módulos com responsabilidades claras
2. **Encapsule**: Use classes onde apropriado
3. **Configure**: Centralize configurações
4. **Documente**: Adicione docstrings
5. **Valide**: Garanta que funcionalidade é preservada

**Critério de sucesso**:
- [ ] ≥ 3 módulos criados com alta coesão
- [ ] Baixo acoplamento entre módulos
- [ ] Configuração externa (não hardcoded)
- [ ] Docstrings em classes e métodos públicos
- [ ] Código funciona igual (ou melhor) que antes
- [ ] README explicando estrutura

# 11. Resultados e Lições

## Resultados

**Comparação objetiva:**

| Métrica | Antes (Ad Hoc) | Depois (Refatorado) | Melhoria |
|---------|----------------|---------------------|----------|
| **Arquivos** | 1 | 8 | Modularizado |
| **Linhas/arquivo** | 200+ | 50-150 | Mais gerenciável |
| **Testabilidade** | Impossível testar partes | Cada módulo testável | 10x melhor |
| **Tempo adicionar feature** | Horas/dias | Minutos/horas | 5-10x mais rápido |
| **Tempo para novo dev entender** | 3-5 horas | 30-60 minutos | 5x mais rápido |
| **Bugs por mudança** | Alto (estado global) | Baixo (isolado) | 70% redução |
| **Manutenibilidade** | Muito baixa | Alta | Transformador |

## Lições

**1. Refatoração não é reescrever - é reorganizar**
   - Funcionalidade permanece idêntica
   - Estrutura muda para melhor
   - Incremental, não "big bang"

**2. Boas práticas têm custo inicial mas retorno exponencial**
   - Mais arquivos, mais código
   - Mas 5-10x mais produtivo no médio prazo
   - Investimento que se paga rapidamente

**3. Modularidade é sobre responsabilidades, não arquivos**
   - Cada módulo = uma responsabilidade
   - Nome do módulo deve ser claro
   - Se difícil nomear, provavelmente baixa coesão

**4. Estado encapsulado evita 80% dos bugs**
   - Variáveis globais são raiz de muito mal
   - Estado privado em classes previne uso indevido
   - Dificulta fazer errado

**5. Código profissional é código manutenível**
   - "Funciona" é 20% do trabalho
   - Outros 80%: legível, testável, extensível
   - Diferença entre hobby e produção

# 12. Encerramento e gancho para a próxima aula (script)

Excelente trabalho! Concluímos a Aula 01 - Fundamentos de Engenharia de Software. Fizemos uma jornada completa:

- **Parte 01**: Entendemos os conceitos fundamentais e por que engenharia importa
- **Parte 02**: Aprendemos princípios de design (modularidade, coesão, acoplamento)
- **Parte 03**: Vimos programação estruturada vs. OOP na prática
- **Parte 04**: Aplicamos tudo em uma refatoração completa de projeto real

Você agora tem uma base sólida de engenharia de software aplicada a Data Science. Mas tem um componente crítico que ainda não cobrimos e que é fundamental para qualquer projeto profissional: **controle de versão**.

Imagine todo esse código maravilhoso que criamos... e de repente você deleta um arquivo por acidente, ou faz uma mudança que quebra tudo e não lembra como estava funcionando antes. Ou pior: você e um colega tentam trabalhar no mesmo projeto e ficam sobrescrevendo o trabalho um do outro.

É aí que entra **Git**, o sistema de controle de versão mais usado no mundo. Na **Aula 02**, vamos aprender:
- Como versionar código profissionalmente
- Trabalhar em equipe sem conflitos
- Manter histórico completo de mudanças
- Branches, merges, pull requests
- E um bônus: DVC para versionar dados e modelos!

A partir da Aula 02, vamos **começar a construir de verdade** nossa API de Machine Learning, aplicando Git desde o primeiro commit. O que fizemos até agora foram exemplos conceituais. Agora vamos construir um projeto real, do zero, passo a passo.

Vocês estão prontos? Nos vemos na Aula 02!

Até lá, e parabéns por chegarem até aqui. Vocês deram um salto enorme em maturidade como desenvolvedores de Data Science!
