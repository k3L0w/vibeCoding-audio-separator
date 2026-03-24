🎸 VibeCoding: Audio Separation Engine
Um motor de separação de áudio de alta performance baseado em Spleeter, otimizado para rodar localmente em hardware legado.

🚀 O Desafio Técnico
O projeto foi desenvolvido em um Dell Latitude E6430 (Intel i5, 16GB RAM) rodando Ubuntu Studio 24.04.

Principais Otimizações:

Python 3.10 Runtime: Migração estratégica do Python 3.12 para 3.10 para garantir compatibilidade com TensorFlow e Spleeter (resolvendo erros de pkgutil).

Ollama Integration: Uso do modelo TinyLlama para assistência de codificação via Cline, mantendo o consumo de RAM abaixo de 1GB para liberar recursos para o processamento de áudio.

Gestão de Memória: Configuração de timeouts estendidos para permitir que a CPU processe modelos de IA sem interrupções de conexão.

📊 Resultados
O sistema separa arquivos MP3 em trilhas de Voz e Acompanhamento com sucesso, gerando espectrogramas para validação da limpeza de frequências.

✅ Checklist de Conclusão
Instale as bibliotecas: No terminal, rode pip install matplotlib librosa.

Execute o visualizador: python3 backend/visualizer.py.

Confira as imagens: Elas aparecerão na pasta backend/output.
