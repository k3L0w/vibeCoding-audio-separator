# 🎸 RiffForge: The Ultra-Fidelity Audio Deconstruction Engine

[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![OS](https://img.shields.io/badge/OS-Ubuntu%20Studio%2024.04-orange.svg)](https://ubuntustudio.org/)
[![Engine](https://img.shields.io/badge/Engine-Demucs_6s-yellow.svg)](https://github.com/facebookresearch/demucs)

O **RiffForge** é um motor de separação de áudio de alta fidelidade de 6 canais, projetado para isolar instrumentos com precisão profissional. Utilizando o modelo `htdemucs_6s`, o sistema transforma arquivos estéreo em trilhas individuais, permitindo o isolamento dedicado de **Guitarra** e **Teclado**.

---

## 🚀 O Desafio de Engenharia: IA em Hardware Legado

Desenvolvido e validado num **Dell Latitude E6430** (2012), provando que o processamento de sinais moderno é viável localmente.

### 🛠️ Especificações do Host
- **Processador:** Intel® Core™ i5-3320M @ 2.60GHz
- **Memória:** 16GB DDR3 RAM
- **S.O:** Ubuntu Studio 24.04 (Kernel Low-Latency)

---

## 📈 Performance e Stems

* **Capacidade**: Isolação de 6 trilhas: **Voz**, **Bateria**, **Baixo**, **Guitarra**, **Teclado** e **Outros**.
* **Mixer Interativo**: Inclui faders individuais e um **Master Gain** global para controlo em tempo real.
* **Eficiência**: Consumo estabilizado em **8.8GB de RAM**.

---

## 🎸 Exemplos de Uso Prático

O **RiffForge** foi desenhado para cenários reais de estudo e produção musical:

* **Criação de Backing Tracks**: Mute a trilha de **Guitarra** ou **Baixo** para praticar o seu instrumento sobre a gravação original, mantendo a fidelidade total dos outros músicos.
* **Estudo de Transcrição**: Isole apenas o **Teclado** ou a **Voz** para captar nuances de arranjo que seriam impossíveis de ouvir na mixagem estéreo comum.
* **Controle de Ensaio com Master Gain**: Use o **Master Fader** para ajustar rapidamente o volume do projeto ao nível do seu amplificador externo, sem precisar reequilibrar cada instrumento individualmente.
* **Análise de Mixagem**: Compare a pureza das frequências isoladas utilizando o visualizador integrado para entender a engenharia por trás das suas músicas favoritas.

---

## ⚙️ Como Executar

### 1. Preparar os Ambientes
```bash
### 1. Preparar o Ambiente
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 2. Iniciar a Aplicação
```bash
source venv/bin/activate
python3 app.py

## ⚖️ Licença e Créditos
Desenvolvido por **Pereira** como um projeto de acessibilidade tecnológica para músicos.

Motor de IA baseado no projeto [Demucs](https://github.com/facebookresearch/demucs) da **Meta AI Research**.