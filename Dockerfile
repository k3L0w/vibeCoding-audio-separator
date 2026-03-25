# --- RiffForge: Backend Engine Dockerization ---
# Usamos a imagem oficial do Python 3.10 para estabilidade no Ubuntu
FROM python:3.10-slim

# Evita que o Python gere ficheiros .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências de sistema (FFmpeg é o coração do processamento de áudio)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas os requisitos primeiro para aproveitar o cache de camadas do Docker
COPY requirements.txt .

# Instala as dependências de IA e Mixer
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir demucs pydub librosa

# Cria a estrutura de pastas do backend
RUN mkdir -p backend/input backend/output

# Copia o restante do código fonte
COPY . .

# Comando para iniciar o motor (pode ser ajustado conforme a evolução da v1.4)
CMD ["python", "app.py"]