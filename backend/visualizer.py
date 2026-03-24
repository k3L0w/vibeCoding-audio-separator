import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_spectrogram(file_path, title, save_path):
    if not os.path.exists(file_path):
        print(f"Erro: Arquivo {file_path} não encontrado.")
        return
    
    # Carrega o áudio
    y, sr = librosa.load(file_path)
    # Converte para decibéis (escala logarítmica)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    
    plt.figure(figsize=(12, 6))
    librosa.display.specshow(D, y_axis='log', x_axis='time', sr=sr, cmap='magma')
    plt.colorbar(format='%+2.0f dB')
    plt.title(title)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"Gráfico salvo em: {save_path}")

# Caminhos baseados no seu sucesso anterior
output_dir = 'backend/output/fhop'
graphs_dir = 'backend/output'

generate_spectrogram(f'{output_dir}/vocals.wav', 'Espectrograma: Vocais (Fhop)', f'{graphs_dir}/vocals_spectrogram.png')
generate_spectrogram(f'{output_dir}/accompaniment.wav', 'Espectrograma: Instrumental (Fhop)', f'{graphs_dir}/accompaniment_spectrogram.png')