# Use a imagem oficial do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instale as dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copie o arquivo requirements.txt e instale as dependências do Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da aplicação
COPY . /app/

# Exponha a porta que o Django vai rodar
EXPOSE 8000

# Execute o comando para iniciar o servidor
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "brain_agriculture.wsgi:application"]
