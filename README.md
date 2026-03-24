# 🎸 VibeCoding: Audio Separation Engine

[![Python Version](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![OS](https://img.shields.io/badge/OS-Ubuntu%20Studio%2024.04-orange.svg)](https://ubuntustudio.org/)
[![Engine](https://img.shields.io/badge/Engine-Spleeter-green.svg)](https://github.com/deezer/spleeter)

Um motor de separação de áudio de alta performance capaz de isolar **Vocais** e **Acompanhamento Instrumental**, otimizado especificamente para rodar em hardware local legado com recursos limitados.

---

## 🚀 O Desafio de Engenharia

Este projeto foi desenvolvido e testado em um **Dell Latitude E6430** (Hardware de 2012), provando que é possível executar modelos modernos de IA e Processamento de Sinais sem depender de infraestrutura em nuvem dispendiosa.

### 🛠️ Especificações do Host
- **Processador:** Intel® Core™ i5-3320M @ 2.60GHz
- **Memória:** 16GB DDR3 RAM
- **S.O:** Ubuntu Studio 24.04 (Kernel Low-Latency)
- **Ambiente:** KDE Plasma / VS Code com Extensão Cline

---

## 🧠 Otimizações Implementadas

Para viabilizar o projeto no hardware disponível, foram aplicadas as seguintes estratégias:

1. **Python 3.10 Runtime Downgrade**: Migração estratégica do Python 3.12 (padrão do sistema) para o 3.10. Isso resolveu a incompatibilidade crítica do `pkgutil.ImpImporter` (removido no 3.12), permitindo a execução estável do TensorFlow e Spleeter.
2. **AI-Assisted Development (Zero-Footprint)**: Utilização do modelo **TinyLlama** via Ollama. Essa escolha manteve o consumo de RAM da IA abaixo de **1GB**, liberando os outros **15GB** para o carregamento dos modelos de rede neural do Spleeter.
3. **Memory Management**: Configuração de timeouts de API para **600s**, permitindo que a CPU processe o "Cold Start" dos modelos sem interrupções de conexão no ambiente de desenvolvimento.

---

## 📊 Fluxo de Processamento

O sistema segue uma pipeline de três etapas:

1. **Injestão**: Recebe arquivos MP3 na pasta `backend/input`.
2. **Separação**: O `processor.py` utiliza o modelo `2stems` para gerar arquivos `.wav` isolados.
3. **Validação**: O `visualizer.py` gera espectrogramas de frequência para comprovar a pureza da separação.

### Exemplo de Saída (Espectrograma)
[Aqui você pode inserir o link para a imagem do espectrograma que geramos]

---

## ⚙️ Como Executar

1. **Preparar o Ambiente**:
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   pip install spleeter pydub matplotlib librosa
