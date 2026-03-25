# 🎸 RiffForge: The Ultra-Fidelity Audio Deconstruction Engine

[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![OS](https://img.shields.io/badge/OS-Ubuntu%20Studio%2024.04-orange.svg)](https://ubuntustudio.org/)
[![Engine](https://img.shields.io/badge/Engine-Demucs_6s-yellow.svg)](https://github.com/facebookresearch/demucs)

O **RiffForge** é um estúdio de isolamento de áudio de 6 canais projetado para músicos e produtores que exigem precisão absoluta. Utilizando o modelo neural `htdemucs_6s`, o sistema desconstrói arquivos estéreo em trilhas individuais de alta fidelidade, permitindo o controle independente de **Guitarra** e **Piano**.

---

## 🚀 O Desafio de Engenharia: IA em Hardware Legado

O grande diferencial do **RiffForge** é a sua otimização para hardware legado. Ele foi desenvolvido e validado em um **Dell Latitude E6430** (2012), provando que o processamento de sinais moderno é viável localmente e sem dependência de nuvem.

### 🛠️ Especificações da Forja
- **Processador:** Intel® Core™ i5-3320M @ 2.60GHz
- **Memória:** 16GB DDR3 RAM
- **S.O:** Ubuntu Studio 24.04 (Kernel Low-Latency)
- **Ambiente:** KDE Plasma / VS Code com Integração Dolphin

---

## 🧠 Otimizações e Arquitetura

Para viabilizar a execução do motor **Demucs** de 6 stems em um hardware i5 de 3ª geração, implementamos as seguintes estratégias:

1. **Dual-Venv Architecture**: Separação de ambientes virtuais (`venv` e `venv_demucs`) para evitar conflitos de dependências entre a interface gráfica e o motor PyTorch.
2. **CPU-Bound Optimization**: Configuração otimizada para os 4 threads do processador, garantindo estabilidade térmica.
3. **Synchronized Mixer Engine**: Motor baseado em `pygame.mixer` que dispara as 6 trilhas simultaneamente com precisão de milissegundos.
4. **Real-time Fader Control**: Interface interativa que permite ajustar volumes individuais para criação de backing tracks personalizadas.

---

## 📈 Performance e Resultados

O sistema demonstra estabilidade total em ciclos longos de processamento neural.

* **Capacidade**: Isolação de 6 trilhas principais: **Vocais**, **Bateria**, **Baixo**, **Guitarra**, **Piano** e **Outros**.
* **Tempo de Processamento**: Aproximadamente 45-50 minutos para uma faixa completa em modo de ultra-fidelidade (6 stems).
* **Eficiência de RAM**: Consumo estabilizado em **8.8GB de RAM**, mantendo o sistema Ubuntu Studio fluido para multitarefa.

---

## 📊 Fluxo de Trabalho

1. **Injestão**: Seleção de arquivos via interface CustomTkinter.
2. **Forja Neural**: Execução do modelo `htdemucs_6s` via ambiente virtual dedicado.
3. **Mixagem Interativa**: Controle de volume em tempo real através dos faders neon do RiffForge.
4. **Análise**: Geração de espectrogramas de frequência para conferência de pureza sonora.

---

## ⚙️ Como Executar

### 1. Preparar os Ambientes
```bash
# Ambiente da Interface e Mixer
python3 -m venv venv
source venv/bin/activate
pip install customtkinter pygame

# Ambiente do Motor (Demucs)
python3 -m venv venv_demucs
source venv_demucs/bin/activate
pip install demucs librosa matplotlib numpy
```
### 2. Iniciar a Aplicação
```bash
source venv/bin/activate
python3 app.py

---

## ⚖️ Licença e Créditos

Desenvolvido por **Pereira** como um projeto de acessibilidade tecnológica para músicos.
>>>>>>> 7683c3e (feat: official rebrand to RiffForge & implement 6-channel synchronized mixer)

Motor de IA baseado no projeto Demucs da **Meta AI Research**.