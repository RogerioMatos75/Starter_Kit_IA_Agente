# Usar uma imagem oficial do Python como base
FROM python:3.11-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Definir variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copiar o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código da aplicação para o diretório de trabalho
COPY . .

# Expor a porta que o Gunicorn vai usar
EXPOSE 5001

# Comando para rodar a aplicação quando o contêiner iniciar
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]