# 🎸 RiffForge v1.3 - Professional Audio Deconstruction Engine

<p align="center">
  <strong>O Engine de Decomposição de Áudio de Ultra-Fidelidade</strong><br>
  Separação avançada em 6 canais (Stems) otimizada para estudo musical, transcrição e performance.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-blue">
  <img alt="Platform" src="https://img.shields.io/badge/Platform-Linux%20%28Ubuntu%20Studio%2024.04%29-informational">
  <img alt="Audio Engine" src="https://img.shields.io/badge/Engine-Demucs-success">
  <img alt="Model" src="https://img.shields.io/badge/Model-htdemucs__6s-orange">
  <img alt="UI Framework" src="https://img.shields.io/badge/UI-CustomTkinter-blueviolet">
  <img alt="Status" src="https://img.shields.io/badge/Status-Stable--v1.3-green">
</p>

---

## 📖 Sobre o Projeto

O **RiffForge** é uma estação de trabalho especializada na extração de *stems* (trilhas isoladas) com alta precisão. Utilizando o estado da arte em IA (modelo `htdemucs_6s`), o software decompõe arquivos de áudio complexos em 6 componentes individuais, permitindo que músicos foquem no que realmente importa: o aprendizado e a prática técnica.

---

## ✨ Funcionalidades Principais

### 1. Separação Granular (6-Stems)
Ao contrário de separadores comuns de 4 canais, o RiffForge isola **Guitarras** e **Teclados** em canais independentes, essencial para guitarristas e pianistas.
*   **Vocais, Bateria, Baixo, Guitarra, Teclado e "Outros".**

### 2. Smart-Cache System (Forja Instantânea)
O sistema detecta automaticamente se uma música já foi processada anteriormente no disco. Se os arquivos existirem, o mixer é carregado em milissegundos, ignorando a etapa de processamento pesado da IA.

### 3. Mixer Profissional com Feedback Visual
*   **VU Meters Reais:** Visualização dinâmica dos níveis de saída de cada canal.
*   **Controles Solo/Mute:** Isolamento de faixas com latência zero via Pygame Mixer.
*   **Master Gain:** Controle global de volume para ajuste fino durante a prática.

### 4. Arquitetura Multi-threaded
O processamento da IA ocorre em background, garantindo que a interface gráfica (GUI) permaneça fluida e responsiva durante a extração.

---

## 🛠️ Desafio de Engenharia: Performance em Hardware Legado

Um dos pilares do RiffForge v1.3 é a eficiência. O software foi otimizado para rodar em estações de áudio com hardware de entrada ou anterior à geração atual de processadores de IA.

### Ambiente de Referência (Stress Test)

| Componente | Especificação |
|------------|---------------|
| Host | Dell Latitude E6430 |
| CPU | Intel Core i5-3320M |
| RAM | 16 GB DDR3 |
| Sistema Operacional | Ubuntu Studio 24.04 |
| Kernel | Low-Latency |

### Estratégias de Otimização
*   **Priorização de Processo (`nice`):** O motor Demucs é executado com prioridade ajustada (`nice -n 10`) para garantir que o kernel Linux dê prioridade às tarefas de interface e áudio em tempo real, evitando congelamentos do sistema.
*   **Gerenciamento de Memória:** Buffer de áudio do Pygame configurado para `512` para equilibrar latência e consumo de CPU.
*   **Venv Dedicado:** Isolamento completo de dependências para evitar conflitos com drivers de áudio do sistema.

---

## ⚙️ Como Executar

### Pré-requisitos
*   Python 3.10 ou superior.
*   FFmpeg instalado no sistema (`sudo apt install ffmpeg`).

### Instalação

1.  **Configurar o ambiente:**
    ```bash
    # Dê permissão e execute o script de setup
    chmod +x setup_env.sh
    ./setup_env.sh
    ```

2.  **Ativar o Ambiente Virtual:**
    ```bash
    source venv/bin/activate
    ```

3.  **Instalar dependências (Manual):**
    ```bash
    pip install -r requirements.txt
    ```

### Inicialização
  ```bash
  python3 app.py
  ```
---

## ⚖️ Licença e Créditos

### **Desenvolvedor Principal**
* **Antonio Pereira** (@pereira-Latitude-E6430): Concepção, arquitetura de interface em CustomTkinter e integração de áudio multi-canal no Ubuntu Studio.

### **Motores de Inteligência Artificial**
* **Demucs (Meta AI Research):** O RiffForge utiliza o modelo de separação de fontes `htdemucs_6s`.
* **Licença do Motor:** Licenciado sob a **MIT License**. Copyright (c) Facebook, Inc. e seus afiliados.

### **Bibliotecas e Tecnologias**
* **CustomTkinter:** Framework para a interface visual moderna.
* **Pygame Mixer:** Motor para reprodução sincronizada e gerenciamento de buffers.
* **Spleeter (Deezer):** Utilizado como dependência de backend para processamento de stems.

---
