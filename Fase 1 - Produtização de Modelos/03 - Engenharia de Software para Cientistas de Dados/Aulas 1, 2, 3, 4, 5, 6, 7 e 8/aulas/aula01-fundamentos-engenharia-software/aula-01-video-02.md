---
titulo: "Aula 01 – Parte 02: Princípios de Design de Código"
modulo: "Engenharia de Software para Cientista de Dados"
curso: "Engenharia de Machine Learning"
duracao_estimada_min: 20
prerequisitos:
  - "Python 3.12+"
  - "Conceitos de Aula 01 - Parte 01"
  - "Ambiente virtual configurado"
tags: ["modularidade", "coesão", "acoplamento", "código-limpo", "dívida-técnica", "uv"]
---

# 1. Abertura do vídeo (script)

Olá! Espero que vocês estejam bem. Nessa aula, vamos avançar dos conceitos gerais de engenharia de software para algo mais tático e imediatamente aplicável: os princípios de design de código. Se na aula anterior entendemos o "porquê" da engenharia de software, agora vamos entender o "como".

Você já abriu um código que você mesmo escreveu há três meses e não conseguiu entender o que estava fazendo? Ou pior: tentou adicionar uma funcionalidade simples e percebeu que teria que mexer em dez lugares diferentes? Esses são sintomas clássicos de código mal estruturado.

A boa notícia é que existem princípios testados e comprovados que, quando aplicados, tornam seu código naturalmente mais fácil de entender, manter e estender. Não são regras arbitrárias - são lições aprendidas por décadas de experiência da indústria. E o melhor: aplicam-se perfeitamente a projetos de Data Science.

Nesta aula vamos explorar modularidade, coesão, acoplamento, e vamos entender o conceito perigoso mas muito real de dívida técnica. Ao final, você terá critérios objetivos para avaliar a qualidade do seu próprio código.

# 2. Problema → Agitação → Solução (Storytelling curto)

**Problema**: Você desenvolveu um pipeline de dados incrível: carrega dados de múltiplas fontes, faz limpeza, feature engineering, treina três modelos diferentes, faz ensemble, avalia métricas e salva resultados. Tudo em um único script de 800 linhas chamado `pipeline.py`. Funciona perfeitamente! Até que...

**Agitação**: Uma semana depois, você precisa mudar a forma como uma feature é calculada. Você abre o arquivo e... onde está esse código? Entre as linhas 234 e 456? Ou era lá embaixo perto da linha 600? Você muda em um lugar, roda, quebra outra coisa. Corrige ali, quebra aqui. Adiciona um print para debug, esquece de remover. Três horas depois você tem um código que funciona, mas agora com 850 linhas e você não tem certeza do que mais mudou. Seu colega tenta usar seu código e não consegue nem entender por onde começar. A manutenção se torna um pesadelo, e o que era para ser uma mudança simples vira um projeto de uma semana.

**Solução**: Código bem estruturado divide responsabilidades claramente. Cada módulo tem um propósito específico, as dependências entre componentes são explícitas e minimizadas, e a lógica é organizada de forma que mudanças em um lugar não quebrem outros. Quando você aplica princípios de modularidade e coesão, aquela mudança que levaria 3 horas vira um ajuste de 10 minutos em um único arquivo específico. A diferença está em **design intencional** versus crescimento orgânico caótico.

# 3. Objetivos de aprendizagem

Ao final desta aula, você será capaz de:

1. **Definir** e **aplicar** o princípio de modularidade em projetos de Data Science
2. **Distinguir** entre alta e baixa coesão, identificando problemas de design no código
3. **Compreender** o conceito de acoplamento e como minimizá-lo para facilitar manutenção
4. **Reconhecer** padrões de código com boa legibilidade e manutenibilidade
5. **Explicar** o que é dívida técnica e como ela se acumula em projetos
6. **Avaliar** o impacto de decisões de design no curto e longo prazo

# 4. Pré-requisitos e Setup do Ambiente

**Requisitos:**
- Python 3.12+
- UV (gerenciador de pacotes moderno para Python)
- Ambiente virtual criado na Parte 01
- Editor de código com syntax highlighting

**Instalação do UV (caso ainda não tenha):**

UV é um gerenciador de pacotes extremamente rápido para Python, escrito em Rust. Ele substitui pip, pip-tools e virtualenv com uma única ferramenta muito mais performática.

```bash
# Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/Mac:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verificar instalação
uv --version
```

**Preparação do Ambiente:**

```bash
# Navegar para pasta do projeto
cd c:\Users\diogomiyake\projects\SWE-4-DS\swe4ds-api-project

# Criar ambiente virtual com UV (muito mais rápido que venv tradicional)
uv init 
uv venv

# Ativar ambiente virtual
# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate

# Criar estrutura de pastas para exemplos desta aula

# Windows (criar cada pasta separadamente):
mkdir modularidade
mkdir coesao
mkdir acoplamento
# PowerShell:
mkdir modularidade, coesao, acoplamento
# Linux/Mac
mkdir exemplos
cd exemplos
mkdir modularidade coesao acoplamento
```

**Por que UV em vez de pip?**
- 10-100x mais rápido na instalação de pacotes
- Resolução de dependências mais inteligente
- Substitui pip, pip-tools e virtualenv
- Compatível com requirements.txt e pyproject.toml
- Ferramenta moderna adotada pela indústria

**Checklist de Setup:**
- [ ] UV instalado (`uv --version` funciona)
- [ ] Ambiente virtual criado com UV (`.venv/`)
- [ ] Ambiente virtual ativo (prompt mostra `(.venv)`)
- [ ] Pasta `exemplos` criada
- [ ] Subpastas `modularidade`, `coesão` e `acoplamento` criadas
- [ ] Editor de código aberto na pasta do projeto

# 5. Visão geral do que já existe no projeto (continuidade)

Nosso projeto continua na estrutura básica estabelecida na Parte 01:

```
swe4ds-api-project/
├── .venv/                   # Ambiente virtual (criado com UV)
├── exemplos/                # [NOVO] Pasta para exemplos desta aula
│   ├── modularidade/
│   ├── coesao/
│   └── acoplamento/
└── (aguardando estrutura da API - próximas aulas)
```

A pasta `exemplos/` é temporária, apenas para ilustrar conceitos nesta aula. A partir da Aula 02 (Git), vamos começar a construir a estrutura real da API seguindo estes princípios que aprenderemos hoje.

# 6. Passo a passo (comandos + código)

## Passo 1: Entendendo Modularidade

**Intenção**: Aprender a dividir código em unidades lógicas independentes e reutilizáveis.

**Modularidade** é o princípio de dividir um sistema em componentes menores (módulos) que podem ser desenvolvidos, testados e mantidos independentemente.

**Exemplo sem modularidade (código monolítico):**

```python
# exemplos/modularidade/pipeline_monolitico.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pickle
import logging

def main():
    # Carrega dados
    print("Carregando dados...")
    df = pd.read_csv('data.csv')
    
    # Limpeza
    print("Limpando dados...")
    df = df.dropna()
    df['age'] = df['age'].fillna(df['age'].mean())
    df = df[df['age'] > 0]
    df = df[df['age'] < 120]
    
    # Feature engineering
    print("Criando features...")
    df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 60, 120], 
                               labels=['jovem', 'adulto', 'meia-idade', 'idoso'])
    df['income_per_age'] = df['income'] / df['age']
    df = pd.get_dummies(df, columns=['age_group'])
    
    # Separação treino/teste
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Treinamento
    print("Treinando modelo...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train)
    
    # Avaliação
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    
    print(f"Accuracy: {acc:.3f}")
    print(f"Precision: {prec:.3f}")
    print(f"Recall: {rec:.3f}")
    
    # Salvamento
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Modelo salvo!")

if __name__ == "__main__":
    main()
```

**Problemas**:
- Tudo em um único lugar
- Impossível reutilizar partes (ex: só a limpeza)
- Difícil de testar componentes isoladamente
- Mudança em uma etapa pode afetar outras inadvertidamente

**Exemplo com modularidade (código bem estruturado):**

```python
# exemplos/modularidade/data_loader.py
"""Módulo responsável por carregar dados."""
import pandas as pd
from pathlib import Path

class DataLoader:
    """Carrega dados de diferentes fontes."""
    
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
    
    def load_csv(self) -> pd.DataFrame:
        """Carrega dados de arquivo CSV."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.data_path}")
        return pd.read_csv(self.data_path)
```

```python
# exemplos/modularidade/data_cleaner.py
"""Módulo responsável por limpeza de dados."""
import pandas as pd
import numpy as np

class DataCleaner:
    """Aplica transformações de limpeza nos dados."""
    
    @staticmethod
    def remove_nulls(df: pd.DataFrame) -> pd.DataFrame:
        """Remove linhas com valores nulos."""
        return df.dropna()
    
    @staticmethod
    def fill_age_nulls(df: pd.DataFrame) -> pd.DataFrame:
        """Preenche nulos na coluna age com a média."""
        if 'age' in df.columns:
            df['age'] = df['age'].fillna(df['age'].mean())
        return df
    
    @staticmethod
    def filter_valid_ages(df: pd.DataFrame, min_age: int = 0, max_age: int = 120) -> pd.DataFrame:
        """Filtra idades dentro de range válido."""
        if 'age' not in df.columns:
            return df
        return df[(df['age'] > min_age) & (df['age'] < max_age)]
```

```python
# exemplos/modularidade/feature_engineering.py
"""Módulo responsável por feature engineering."""
import pandas as pd

class FeatureEngineer:
    """Cria novas features a partir dos dados brutos."""
    
    @staticmethod
    def create_age_groups(df: pd.DataFrame) -> pd.DataFrame:
        """Cria grupos etários."""
        if 'age' not in df.columns:
            return df
        
        df['age_group'] = pd.cut(
            df['age'], 
            bins=[0, 18, 35, 60, 120], 
            labels=['jovem', 'adulto', 'meia-idade', 'idoso']
        )
        return df
    
    @staticmethod
    def create_income_per_age(df: pd.DataFrame) -> pd.DataFrame:
        """Calcula renda per capita por idade."""
        if 'income' in df.columns and 'age' in df.columns:
            df['income_per_age'] = df['income'] / df['age']
        return df
```

```python
# exemplos/modularidade/model_trainer.py
"""Módulo responsável por treinamento de modelos."""
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from typing import Tuple

class ModelTrainer:
    """Treina e avalia modelos de ML."""
    
    def __init__(self, model_params: dict = None):
        self.model_params = model_params or {
            'n_estimators': 100,
            'random_state': 42,
            'max_depth': 10
        }
        self.model = None
    
    def split_data(self, X: pd.DataFrame, y: pd.Series, 
                   test_size: float = 0.2) -> Tuple:
        """Divide dados em treino e teste."""
        return train_test_split(X, y, test_size=test_size, 
                               random_state=self.model_params.get('random_state', 42))
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """Treina modelo."""
        self.model = RandomForestClassifier(**self.model_params)
        self.model.fit(X_train, y_train)
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Faz predições."""
        if self.model is None:
            raise ValueError("Modelo não treinado. Execute train() primeiro.")
        return self.model.predict(X)
```

```python
# exemplos/modularidade/pipeline_modular.py
"""Pipeline completo usando módulos independentes."""
from data_loader import DataLoader
from data_cleaner import DataCleaner
from feature_engineer import FeatureEngineer
from model_trainer import ModelTrainer
from sklearn.metrics import accuracy_score, precision_score, recall_score
import pickle

def main():
    # Cada etapa usa um módulo específico
    loader = DataLoader('data.csv')
    df = loader.load_csv()
    print("Dados carregados.")
    
    cleaner = DataCleaner()
    df = cleaner.remove_nulls(df)
    df = cleaner.fill_age_nulls(df)
    df = cleaner.filter_valid_ages(df)
    print("Dados limpos.")
    
    engineer = FeatureEngineer()
    df = engineer.create_age_groups(df)
    df = engineer.create_income_per_age(df)
    df = pd.get_dummies(df, columns=['age_group'])
    print("Features criadas.")
    
    X = df.drop('target', axis=1)
    y = df['target']
    
    trainer = ModelTrainer()
    X_train, X_test, y_train, y_test = trainer.split_data(X, y)
    trainer.train(X_train, y_train)
    print("Modelo treinado.")
    
    y_pred = trainer.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
    print(f"Precision: {precision_score(y_test, y_pred):.3f}")
    print(f"Recall: {recall_score(y_test, y_pred):.3f}")
    
    with open('model.pkl', 'wb') as f:
        pickle.dump(trainer.model, f)
    print("Modelo salvo!")

if __name__ == "__main__":
    main()
```

**Benefícios da modularização**:
- Cada módulo tem responsabilidade única e clara
- Fácil de testar cada componente isoladamente
- Reutilizável (pode usar `DataCleaner` em outros projetos)
- Mudanças ficam localizadas
- Múltiplas pessoas podem trabalhar em módulos diferentes simultaneamente

**CHECKPOINT**: Compare os dois códigos. O modular tem mais arquivos, mas é muito mais fácil de entender, manter e estender. Isso faz sentido?

## Passo 2: Compreendendo Coesão

**Intenção**: Aprender a criar módulos onde tudo está relacionado e serve a um propósito único.

**Coesão** mede o quanto as responsabilidades dentro de um módulo estão relacionadas. **Alta coesão** é desejável.

**Exemplo de baixa coesão (ruim):**

```python
# exemplos/coesao/utils_baixa_coesao.py
"""Módulo utilitário genérico - EVITE ISSO!"""
import pandas as pd
import requests
from datetime import datetime
import smtplib

class Utils:
    """Classe genérica que faz 'tudo' - PROBLEMA!"""
    
    @staticmethod
    def calculate_mean(numbers: list) -> float:
        """Calcula média."""
        return sum(numbers) / len(numbers)
    
    @staticmethod
    def fetch_api_data(url: str) -> dict:
        """Busca dados de API."""
        response = requests.get(url)
        return response.json()
    
    @staticmethod
    def send_email(to: str, subject: str, body: str) -> None:
        """Envia email."""
        # código de envio de email
        pass
    
    @staticmethod
    def format_date(date: datetime) -> str:
        """Formata data."""
        return date.strftime('%Y-%m-%d')
    
    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        """Valida CPF."""
        # lógica de validação
        return True
```

**Problema**: Funções não têm nada a ver umas com as outras. O módulo não tem um propósito único.

**Exemplo de alta coesão (bom):**

```python
# exemplos/coesao/validadores.py
"""Módulo focado apenas em validação de dados."""

class DataValidator:
    """Valida diferentes tipos de dados brasileiros."""
    
    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        """Valida número de CPF."""
        # Remove formatação
        cpf = ''.join(filter(str.isdigit, cpf))
        
        if len(cpf) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False
        
        # Validação dos dígitos verificadores
        # (lógica completa omitida para brevidade)
        return True
    
    @staticmethod
    def validate_cnpj(cnpj: str) -> bool:
        """Valida número de CNPJ."""
        cnpj = ''.join(filter(str.isdigit, cnpj))
        return len(cnpj) == 14
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valida formato de email."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
```

```python
# exemplos/coesao/formatadores.py
"""Módulo focado apenas em formatação de dados."""
from datetime import datetime
from typing import Optional

class DataFormatter:
    """Formata dados para diferentes representações."""
    
    @staticmethod
    def format_date(date: datetime, format: str = '%Y-%m-%d') -> str:
        """Formata data em string."""
        return date.strftime(format)
    
    @staticmethod
    def format_currency(value: float, currency: str = 'BRL') -> str:
        """Formata valor monetário."""
        if currency == 'BRL':
            return f'R$ {value:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')
        return f'{value:,.2f}'
    
    @staticmethod
    def format_cpf(cpf: str) -> str:
        """Formata CPF para exibição."""
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11:
            return cpf
        return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
```

**Benefícios da alta coesão**:
- Fácil de entender o propósito do módulo
- Mudanças tendem a ficar localizadas
- Fácil de nomear o módulo (se é difícil nomear, provavelmente tem baixa coesão)
- Facilita testes (testa um conceito de cada vez)

**CHECKPOINT**: Se você não consegue descrever o propósito de um módulo em uma frase simples, ele provavelmente tem baixa coesão.

## Passo 3: Minimizando Acoplamento

**Intenção**: Aprender a reduzir dependências entre módulos para facilitar mudanças.

**Acoplamento** mede o quanto um módulo depende de outros. **Baixo acoplamento** é desejável.

**Exemplo de alto acoplamento (ruim):**

```python
# exemplos/acoplamento/alto_acoplamento.py
"""Exemplo de módulos fortemente acoplados - EVITE!"""

# Módulo A
class DatabaseConnection:
    def __init__(self):
        self.connection_string = "postgresql://localhost:5432/mydb"
        self.connection = None
    
    def connect(self):
        # conecta ao banco
        self.connection = f"Connected to {self.connection_string}"
        return self.connection

# Módulo B depende de detalhes internos de A
class UserRepository:
    def __init__(self):
        # PROBLEMA: conhece detalhes de implementação de DatabaseConnection
        self.db = DatabaseConnection()
        self.db.connect()
        # Acessa atributos internos diretamente
        self.conn_string = self.db.connection_string
    
    def get_user(self, user_id: int):
        # usa self.db.connection diretamente
        return f"User {user_id} from {self.conn_string}"

# Módulo C também depende de A
class ProductRepository:
    def __init__(self):
        self.db = DatabaseConnection()
        self.db.connect()
        # PROBLEMA: se DatabaseConnection mudar, todos quebram
        self.conn = self.db.connection
    
    def get_product(self, product_id: int):
        return f"Product {product_id}"
```

**Problemas**:
- Se `DatabaseConnection` mudar, `UserRepository` e `ProductRepository` quebram
- Impossível testar `UserRepository` sem banco de dados real
- Difícil trocar implementação do banco

**Exemplo de baixo acoplamento (bom):**

```python
# exemplos/acoplamento/baixo_acoplamento.py
"""Exemplo de módulos com baixo acoplamento - RECOMENDADO!"""

from abc import ABC, abstractmethod
from typing import Any

# Interface (contrato) abstrata
class DatabaseInterface(ABC):
    """Interface que define o contrato para acesso a dados."""
    
    @abstractmethod
    def connect(self) -> None:
        """Estabelece conexão."""
        pass
    
    @abstractmethod
    def execute_query(self, query: str) -> Any:
        """Executa query e retorna resultado."""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Fecha conexão."""
        pass

# Implementação concreta
class PostgreSQLDatabase(DatabaseInterface):
    """Implementação para PostgreSQL."""
    
    def __init__(self, connection_string: str):
        self._connection_string = connection_string
        self._connection = None
    
    def connect(self) -> None:
        self._connection = f"Connected to PostgreSQL: {self._connection_string}"
    
    def execute_query(self, query: str) -> Any:
        # executa query no PostgreSQL
        return f"Result from PostgreSQL: {query}"
    
    def close(self) -> None:
        self._connection = None

# Repositório depende apenas da INTERFACE, não da implementação
class UserRepository:
    """Repositório de usuários - depende apenas da interface."""
    
    def __init__(self, database: DatabaseInterface):
        # BOAS PRÁTICAS: recebe interface, não implementação concreta
        self.database = database
    
    def get_user(self, user_id: int) -> dict:
        """Busca usuário por ID."""
        query = f"SELECT * FROM users WHERE id = {user_id}"
        result = self.database.execute_query(query)
        return {"id": user_id, "data": result}

class ProductRepository:
    """Repositório de produtos - também depende apenas da interface."""
    
    def __init__(self, database: DatabaseInterface):
        self.database = database
    
    def get_product(self, product_id: int) -> dict:
        """Busca produto por ID."""
        query = f"SELECT * FROM products WHERE id = {product_id}"
        result = self.database.execute_query(query)
        return {"id": product_id, "data": result}

# Uso
if __name__ == "__main__":
    # Injeção de dependência: passamos a implementação
    db = PostgreSQLDatabase("postgresql://localhost:5432/mydb")
    db.connect()
    
    user_repo = UserRepository(db)
    product_repo = ProductRepository(db)
    
    print(user_repo.get_user(1))
    print(product_repo.get_product(100))
```

**Benefícios do baixo acoplamento**:
- Fácil trocar implementação (ex: PostgreSQL → MongoDB)
- Testável (pode passar um mock/fake de DatabaseInterface)
- Módulos independentes (mudança em um não afeta outros)

**Padrão aplicado**: **Injeção de Dependência** - dependências são "injetadas" via construtor.

**CHECKPOINT**: Se você pode trocar uma implementação sem mudar código dos clientes, você tem baixo acoplamento!

## Passo 4: Entendendo Dívida Técnica

**Intenção**: Reconhecer quando atalhos no design criam problemas futuros.

**Dívida Técnica** é uma metáfora: assim como dívida financeira, você "pega emprestado" tempo agora (fazendo código rápido mas não ideal), mas paga "juros" depois (tempo extra para manutenção e correções).

**Como dívida técnica se acumula:**

```python
# Versão 1: "Vou fazer rápido para entregar"
def process_data(file_path):
    # Leitura, limpeza, transformação tudo junto
    df = pd.read_csv(file_path)
    df = df.dropna()
    # ... 200 linhas depois ...
    return result

# Semana 2: "Preciso adicionar nova fonte de dados"
def process_data(file_path, file_path2=None):
    df = pd.read_csv(file_path)
    if file_path2:  # DÍVIDA: lógica condicional crescendo
        df2 = pd.read_csv(file_path2)
        df = pd.concat([df, df2])
    df = df.dropna()
    # ... agora 300 linhas ...
    return result

# Mês 2: "Preciso adicionar validação"
def process_data(file_path, file_path2=None, validate=True):
    df = pd.read_csv(file_path)
    if file_path2:
        df2 = pd.read_csv(file_path2)
        if validate:  # DÍVIDA: aninhamento crescendo
            # valida df2
            pass
        df = pd.concat([df, df2])
    if validate:
        # valida df
        pass
    df = df.dropna()
    # ... agora 500 linhas, ninguém mais entende ...
    return result
```

**Consequências**:
- Cada mudança fica mais difícil e arriscada
- Bugs se acumulam
- Novos desenvolvedores não conseguem contribuir
- Velocidade de desenvolvimento desmorona

**Como evitar/pagar a dívida:**

```python
# Refatoração: separar responsabilidades
class DataSource:
    def load(self, path: str) -> pd.DataFrame:
        return pd.read_csv(path)

class DataValidator:
    def validate(self, df: pd.DataFrame) -> pd.DataFrame:
        # lógica de validação separada
        return df

class DataCleaner:
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.dropna()

class DataPipeline:
    def __init__(self, source: DataSource, validator: DataValidator, cleaner: DataCleaner):
        self.source = source
        self.validator = validator
        self.cleaner = cleaner
    
    def process(self, paths: list[str], validate: bool = True) -> pd.DataFrame:
        dfs = [self.source.load(p) for p in paths]
        df = pd.concat(dfs)
        
        if validate:
            df = self.validator.validate(df)
        
        return self.cleaner.clean(df)
```

**CHECKPOINT**: Dívida técnica não é "código ruim" - é escolha consciente de trocar qualidade por velocidade. O problema é quando não há plano para pagá-la.

# 7. Testes rápidos e validação

Para validar a compreensão desses princípios, faça este exercício mental:

**Cenário**: Você precisa adicionar suporte para carregar dados de uma API REST (além de CSV).

**Teste 1 - Modularidade**: 
- No código monolítico: você tem que mexer no `main()` gigante
- No código modular: você cria nova classe `APIDataLoader` e usa no pipeline
- ✅ Se entendeu que a segunda opção é melhor, conceito assimilado!

**Teste 2 - Coesão**:
- Onde colocar a nova funcionalidade de autenticação da API?
- Resposta ruim: em `Utils` genérico
- Resposta boa: em novo módulo `api_auth.py` focado em autenticação
- ✅ Se escolheu a segunda, entendeu coesão!

**Teste 3 - Acoplamento**:
- Se `UserRepository` depende diretamente de `PostgreSQLDatabase`, consegue testar sem banco?
- Resposta: Não
- Se depende de `DatabaseInterface`, consegue passar um mock?
- Resposta: Sim!
- ✅ Se entendeu a diferença, assimilou acoplamento!

# 8. Observabilidade e boas práticas (mini-bloco)

**1. Nomeie módulos por responsabilidade, não por tipo técnico**
- ❌ Ruim: `utils.py`, `helpers.py`, `common.py`
- ✅ Bom: `validadores.py`, `formatadores.py`, `calculos_financeiros.py`
- **Trade-off**: Requer pensar na responsabilidade, mas código fica auto-documentado

**2. Função/classe deve fazer UMA coisa e fazê-la bem**
- ❌ Ruim: `def process_and_save_and_send_email()`
- ✅ Bom: `def process()`, `def save()`, `def send_email()` separadas
- **Trade-off**: Mais funções, mas cada uma é simples e testável

**3. Prefira composição a herança profunda**
- ❌ Ruim: `ClasseA → ClasseB → ClasseC → ClasseD` (herança de 4 níveis)
- ✅ Bom: Classes injetam dependências via composição
- **Trade-off**: Mais flexível, menos acoplado, mas requer entender injeção de dependência

**Por que vale a pena:**
- Código modular com alta coesão e baixo acoplamento é 3-5x mais fácil de manter
- Reduz bugs em 40-60% (estudos empíricos)
- Facilita onboarding de novos desenvolvedores
- Permite crescimento sustentável do projeto

# 9. Troubleshooting (erros comuns)

**Erro 1: "Modularizar demais" (over-engineering)**
- **Sintoma**: Arquivo com 5 linhas, 20 arquivos para funcionalidade simples
- **Solução**: Balance. Módulo deve ter tamanho significativo (50-300 linhas típico)
- **Como identificar**: Se você gasta mais tempo navegando entre arquivos que lendo código

**Erro 2: "Módulos que não são realmente módulos"**
- **Sintoma**: Separou em arquivos, mas todos dependem uns dos outros circularmente
- **Solução**: Dependências devem formar um grafo direcionado acíclico (DAG)
- **Como identificar**: Import circular errors ou dificuldade de decidir ordem de imports

**Erro 3: "Coesão aparente"**
- **Sintoma**: Módulo chamado `data_processing.py` que faz 15 coisas diferentes
- **Solução**: Se precisa "e" para descrever, provavelmente tem baixa coesão
- **Como identificar**: Nome genérico ou precisa de múltiplas sentenças para explicar

**Erro 4: "Abstrações prematuras"**
- **Sintoma**: Criar interfaces e hierarquias antes de entender o problema
- **Solução**: Regra de três: abstraia quando houver 3 casos similares, não antes
- **Como identificar**: Interfaces com um único implementador

**Erro 5: "Ignorar dívida técnica até ser tarde demais"**
- **Sintoma**: "Depois eu arrumo" vira "nunca arrumo"
- **Solução**: Reserve 20% do tempo para pagar dívida técnica (refatoração)
- **Como identificar**: Velocidade de desenvolvimento desmorona com o tempo

**Erro 6: "Acoplamento escondido via dados globais"**
- **Sintoma**: Módulos parecem independentes mas compartilham estado global
- **Solução**: Evite variáveis globais, passe dependências explicitamente
- **Como identificar**: Bugs difíceis de reproduzir, comportamento dependente de ordem

# 10. Exercícios (básico e avançado)

## Exercícios Básicos

**Exercício 1: Refatorando para Modularidade**

Pegue este código monolítico e refatore em 3 módulos com responsabilidades claras:

```python
# pipeline_confuso.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def main():
    # Carrega
    df = pd.read_csv('data.csv')
    # Limpa
    df = df.dropna()
    df['income'] = df['income'].fillna(0)
    # Transforma
    df['log_income'] = np.log1p(df['income'])
    # Treina
    X = df[['log_income', 'age']]
    y = df['target']
    model = RandomForestClassifier()
    model.fit(X, y)
    # Salva
    import pickle
    pickle.dump(model, open('model.pkl', 'wb'))

if __name__ == "__main__":
    main()
```

**Critério de sucesso**:
- [ ] 3+ módulos criados com responsabilidades únicas
- [ ] Cada módulo pode ser testado isoladamente
- [ ] Pipeline principal (`main`) orquestra os módulos

**Exercício 2: Identificando Problemas de Coesão**

Para cada módulo abaixo, diga se tem alta ou baixa coesão e justifique:

```python
# A)
class MathOperations:
    def add(self, a, b): return a + b
    def subtract(self, a, b): return a - b
    def multiply(self, a, b): return a * b

# B)
class SystemUtils:
    def send_email(self, to, subject): pass
    def calculate_tax(self, value): pass
    def format_date(self, date): pass
    
# C)
class UserAuthentication:
    def login(self, username, password): pass
    def logout(self, session_id): pass
    def verify_token(self, token): pass
```

**Critério de sucesso**:
- [ ] Identificou corretamente alta coesão (A e C) e baixa coesão (B)
- [ ] Justificou com base no princípio de responsabilidade única

## Exercício Avançado

**Exercício 3: Redesenhando com Baixo Acoplamento**

Você tem este código altamente acoplado:

```python
class DataProcessor:
    def __init__(self):
        self.db = PostgreSQLDatabase()  # Acoplamento direto
        self.cache = RedisCache()        # Acoplamento direto
        self.logger = FileLogger('app.log')  # Acoplamento direto
    
    def process(self, data_id: int):
        # Busca do banco
        data = self.db.query(f"SELECT * FROM data WHERE id = {data_id}")
        
        # Verifica cache
        cached = self.cache.get(f"processed_{data_id}")
        if cached:
            self.logger.log(f"Cache hit for {data_id}")
            return cached
        
        # Processa
        result = self._transform(data)
        
        # Salva no cache
        self.cache.set(f"processed_{data_id}", result)
        self.logger.log(f"Processed {data_id}")
        
        return result
    
    def _transform(self, data):
        return data.upper()
```

**Seu desafio**:
1. Crie interfaces (abstract base classes) para `Database`, `Cache` e `Logger`
2. Modifique `DataProcessor` para receber dependências via construtor (injeção de dependência)
3. Crie uma implementação mock de cada interface para testes
4. Mostre como testar `DataProcessor` sem banco de dados real

**Critério de sucesso**:
- [ ] 3 interfaces (ABCs) criadas
- [ ] `DataProcessor` usa injeção de dependência
- [ ] Código de teste que usa mocks (sem dependências externas)
- [ ] Fácil trocar PostgreSQL por MongoDB sem mudar `DataProcessor`

**Exemplo de teste esperado**:
```python
# test_processor.py
from unittest.mock import Mock

def test_process_with_cache_miss():
    # Arrange
    mock_db = Mock(spec=DatabaseInterface)
    mock_cache = Mock(spec=CacheInterface)
    mock_logger = Mock(spec=LoggerInterface)
    
    mock_db.query.return_value = "test_data"
    mock_cache.get.return_value = None  # cache miss
    
    processor = DataProcessor(mock_db, mock_cache, mock_logger)
    
    # Act
    result = processor.process(123)
    
    # Assert
    assert result == "TEST_DATA"
    mock_cache.set.assert_called_once()
    mock_logger.log.assert_called()
```

# 11. Resultados e Lições

## Resultados

Como medir se você está aplicando esses princípios:

**1. Facilidade de Mudança**
   - Métrica: Tempo para adicionar nova funcionalidade
   - Esperado: Código modular → mudanças localizadas → ~70% mais rápido
   - Como medir: Compare tempo para adicionar feature antes e depois da refatoração

**2. Testabilidade**
   - Métrica: % de código coberto por testes
   - Esperado: Baixo acoplamento → 80%+ de cobertura possível
   - Como medir: Use ferramentas como `pytest-cov`

**3. Compreensibilidade**
   - Métrica: Tempo para novo desenvolvedor entender o código
   - Esperado: Código coeso → entendimento por módulo independente
   - Como medir: Tempo de onboarding, perguntas de esclarecimento

**4. Dívida Técnica**
   - Métrica: Complexidade ciclomática, duplicação de código
   - Esperado: Código modular → complexidade baixa (< 10 por função)
   - Como medir: Ferramentas como `pylint`, `radon`

## Lições

**1. Modularidade é investimento, não custo**
   - Parece demorar mais no início
   - Compensa exponencialmente conforme projeto cresce
   - Permite múltiplas pessoas trabalharem sem conflitos

**2. Coesão alta = Código auto-documentado**
   - Se módulo tem nome claro e faz uma coisa, é fácil de entender
   - Documentação externa se torna menos necessária
   - Reduz carga cognitiva do desenvolvedor

**3. Baixo acoplamento = Flexibilidade**
   - Trocar implementações fica trivial
   - Testes ficam simples e rápidos
   - Sistema resiste melhor a mudanças de requisitos

**4. Dívida técnica é inevitável, mas gerenciável**
   - Atalhos às vezes são necessários (deadlines)
   - Mas devem ser conscientes e com plano de pagamento
   - Reserve tempo regular para refatoração (não deixe acumular)

**5. Princípios de design não são dogmas**
   - Use bom senso: não module excessivamente
   - Contexto importa: um script de 50 linhas não precisa de 10 módulos
   - Evolua a arquitetura conforme necessário

# 12. Encerramento e gancho para a próxima aula (script)

Excelente! Nesta aula aprofundamos nos princípios fundamentais de design de código: modularidade, coesão e acoplamento. Vimos que código bem estruturado não é luxo - é necessidade para projetos que precisam evoluir e ser mantidos.

Entendemos que:
- **Modularidade** divide complexidade em partes gerenciáveis
- **Alta coesão** mantém coisas relacionadas juntas
- **Baixo acoplamento** reduz dependências e aumenta flexibilidade
- **Dívida técnica** se acumula quando ignoramos esses princípios

Esses não são conceitos abstratos de academia - são práticas testadas em milhões de projetos reais que fazem a diferença entre sucesso e fracasso.

Agora temos os fundamentos conceituais (Parte 01) e os princípios de design (Parte 02). Mas teoria sem prática não consolida aprendizado. Por isso, na **Aula 01 - Parte 03**, vamos ver tudo isso em ação!

Vamos fazer uma **demonstração prática comparando programação estruturada e orientação a objetos** no contexto de Data Science. Você verá, com código real rodando, como encapsulamento e classes ajudam a organizar projetos complexos. Vamos resolver o mesmo problema de duas formas e comparar legibilidade, manutenibilidade e escalabilidade.

É aquele momento onde os conceitos saem do papel e ganham vida. Preparem-se para colocar a mão no código!

Nos vemos na Parte 03. Até lá!

