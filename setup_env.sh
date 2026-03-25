#!/bin/bash

# --- RiffForge Setup Script para Ubuntu Studio ---

echo "🎸 Iniciando a forja do ambiente RiffForge..."

# 1. Atualizar pacotes do sistema (essencial para o Pygame e FFmpeg)
echo "📦 Verificando dependências de sistema (FFmpeg e Python Dev)..."
sudo apt update && sudo apt install -y ffmpeg python3-dev python3-venv

# 2. Criar e configurar o ambiente principal (Interface e Mixer)
echo "🐍 Criando venv principal para a Interface..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# 3. Criar e configurar o ambiente de IA (Demucs)
echo "🤖 Criando venv_demucs para o motor de separação..."
python3 -m venv venv_demucs
source venv_demucs/bin/activate
pip install --upgrade pip
pip install demucs
deactivate

# 4. Criar estrutura de pastas (caso não existam)
echo "📂 Organizando estrutura de diretórios..."
mkdir -p backend/input
mkdir -p backend/output
touch backend/input/.gitkeep
touch backend/output/.gitkeep

echo "✨ Configuração concluída com sucesso, Pereira!"
echo "🚀 Para iniciar o app: source venv/bin/activate && python app.py"
