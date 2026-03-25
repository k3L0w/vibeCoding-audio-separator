# 🎸 RiffForge: The Ultra-Fidelity Audio Deconstruction Engine

[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![OS](https://img.shields.io/badge/OS-Ubuntu%20Studio%2024.04-orange.svg)](https://ubuntustudio.org/)
[![Engine](https://img.shields.io/badge/Engine-Demucs_6s-yellow.svg)](https://github.com/facebookresearch/demucs)

O **RiffForge** é um estúdio de isolamento de áudio de 6 canais projetado para músicos que exigem precisão absoluta. Diferente de separadores comuns, o RiffForge utiliza o modelo `htdemucs_6s` para forjar trilhas independentes de **Guitarra** e **Piano**, além de Voz, Baixo e Bateria.

---

## 🚀 Engenharia de Precisão em Hardware Real

O **RiffForge** foi forjado e validado em um **Dell Latitude E6430**, otimizando o processamento de IA para ambientes locais sem latência de nuvem.

### 🛠️ Especificações da Forja
- **Host:** Dell Latitude E6430 (Intel® Core™ i5-3320M)
- **RAM:** 16GB DDR3 (Otimizada para 8.8GB de uso estável)
- **S.O:** Ubuntu Studio 24.04 (Kernel Low-Latency)

---

## 🧠 Arquitetura do Sistema

1. **6-Stem Neural Isolation**: Separação dedicada de Guitarra e Teclado.
2. **Synchronized Mixer Engine**: Motor Pygame que dispara todas as trilhas com precisão de milissegundos.
3. **Real-time Fader Control**: Mixagem interativa para criação de Backing Tracks personalizadas.
4. **Spectral Analysis**: Visualização de frequências para conferência de pureza sonora.

---

## ⚙️ Como Operar o RiffForge

### 1. Preparar a Forja (Ambientes)
```bash
# Ambiente de Interface e Mixer
python3 -m venv venv
source venv/bin/activate
pip install customtkinter pygame

# Ambiente Neural (Demucs)
python3 -m venv venv_demucs
source venv_demucs/bin/activate
pip install demucs librosa matplotlib numpy
```

### 2. Iniciar a Sessão
```bash
source venv/bin/activate
python3 app.py
```

## ⚖️ Licença e Créditos

Desenvolvido por Pereira.

O RiffForge utiliza o motor de IA Demucs da Meta AI Research.
---
