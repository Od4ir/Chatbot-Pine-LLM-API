# Usar a imagem base oficial do Python
FROM python:3.9-slim

# Setar o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos requirements.txt para o container
COPY app/requirements.txt .

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o conteúdo da pasta app para dentro do container
COPY app/ .

# Expôr a porta que o Flask vai rodar (5000 por padrão)
EXPOSE 5000

# Definir o comando que vai rodar quando o container iniciar
CMD ["python", "main.py"]
