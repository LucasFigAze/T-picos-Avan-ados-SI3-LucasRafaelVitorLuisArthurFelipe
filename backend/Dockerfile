FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Define o diretório de trabalho dentro do container
WORKDIR /app

# 4. Instala as dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# 5. Copia o resto do código do projeto
COPY . .

# 6. Expõe a porta que o Django usará
EXPOSE 8000
