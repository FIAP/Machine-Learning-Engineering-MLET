FROM python:3.12-slim

WORKDIR /app

# Instalar uv
RUN pip install --no-cache-dir uv

# Copiar todos os arquivos necessários para a construção
COPY pyproject.toml ./
COPY requirements.txt ./
COPY uv.lock ./
COPY src/ ./src/

# Instalar dependências sem o modo editável
RUN sed '/^-e \./d' requirements.txt > requirements-no-editable.txt && \
    uv pip install --system --no-cache -r requirements-no-editable.txt && \
    rm requirements-no-editable.txt

# Expor porta
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]