# 🎸 VibeCoding: Audio Separation Engine (Demucs Edition)

[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![OS](https://img.shields.io/badge/OS-Ubuntu%20Studio%2024.04-orange.svg)](https://ubuntustudio.org/)
[![Engine](https://img.shields.io/badge/Engine-Demucs-blueviolet.svg)](https://github.com/facebookresearch/demucs)

O **vibeCoding-audio-separator** é um motor de separação de áudio de alta fidelidade projetado para isolar instrumentos com precisão profissional. Utilizando inteligência artificial de ponta, o sistema transforma arquivos estéreo em trilhas individuais (stems), sendo uma alternativa robusta e local para músicos e produtores.

---

## 🚀 O Desafio de Engenharia: IA em Hardware Legado

O grande diferencial deste projeto é a sua otimização para hardware legado. Ele foi desenvolvido e validado em um **Dell Latitude E6430** (2012), provando que o processamento de sinais moderno é viável sem dependência de nuvem.

### 🛠️ Especificações do Host
- **Processador:** Intel® Core™ i5-3320M @ 2.60GHz
- **Memória:** 16GB DDR3 RAM
- **S.O:** Ubuntu Studio 24.04 (Kernel Low-Latency)
- **Ambiente:** KDE Plasma / VS Code com Integração Dolphin

---

## 🧠 Otimizações e Arquitetura

Para viabilizar a execução do **Demucs** (motor de alta complexidade matemática) em um i5 de 3ª geração, implementamos as seguintes estratégias:

1. **Dual-Venv Architecture**: Separação de ambientes virtuais (`venv` e `venv_demucs`) para evitar conflitos de dependências entre a interface gráfica e o motor PyTorch.
2. **CPU-Bound Optimization**: Configuração forçada para modo CPU (`CUDA_VISIBLE_DEVICES=-1`), otimizando o uso dos 4 threads do processador.
3. **UI Assíncrona com QProcess**: A interface neon monitora o progresso em tempo real sem bloquear o sistema operacional, utilizando expressões regulares para capturar o status da IA.

---

## 📈 Performance e Resultados

O sistema demonstra estabilidade total em ciclos longos de processamento.

* **Capacidade**: Isolação de 4 trilhas principais: **Vocais**, **Bateria**, **Baixo** e **Outros** (Guitarras/Teclados).
* **Tempo de Processamento**: Aproximadamente 31 minutos para uma faixa completa em modo de alta fidelidade.
* **Eficiência Térmica e de RAM**: Consumo estabilizado em **8.8GB de RAM**, mantendo o sistema Ubuntu Studio fluido para multitarefa.

---

## 📊 Fluxo de Trabalho

1. **Injestão**: Seleção de arquivos via interface CustomTkinter.
2. **Processamento**: Execução do modelo `htdemucs` via ambiente virtual dedicado.
3. **Análise**: Geração de espectrogramas de frequência via `visualizer.py` para conferência de pureza sonora.

---

## ⚙️ Como Executar

### 1. Preparar os Ambientes
```bash
# Ambiente da Interface
python3 -m venv venv
source venv/bin/activate
pip install customtkinter

# Ambiente do Motor (Demucs)
python3 -m venv venv_demucs
source venv_demucs/bin/activate
pip install demucs librosa matplotlib numpy
