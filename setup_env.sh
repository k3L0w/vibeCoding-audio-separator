#!/bin/bash

echo "🚀 Iniciando a configuração do VibeCoding Audio Engine..."

# 1. Verificar se o Python 3.10 está instalado
if ! command -v python3.10 &> /dev/null
then
    echo "❌ Python 3.10 não encontrado. Por favor, instale-o com: sudo apt install python3.10 python3.10-venv"
    exit
fi

# 2. Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual (venv) com Python 3.10..."
    python3.10 -m venv venv
else
    echo "✅ Ambiente virtual já existe."
fi

# 3. Ativar venv e instalar dependências
echo "🛠️ Instalando dependências (Spleeter, Librosa, Pydub, Matplotlib)..."
source venv/bin/activate
pip install --upgrade pip
pip install spleeter pydub librosa matplotlib setuptools

# 4. Criar estrutura de pastas
echo "📂 Organizando estrutura de diretórios..."
mkdir -p backend/input
mkdir -p backend/output

# 5. Criar arquivos .gitkeep para manter as pastas no Git (vazias)
touch backend/input/.gitkeep
touch backend/output/.gitkeep

echo "✨ Tudo pronto! Para começar, use: source venv/bin/activate"
echo "🎵 Depois, coloque seu MP3 em backend/input/ e rode: python3 backend/processor.py"