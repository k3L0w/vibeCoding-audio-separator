import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as prosperity

def visualize_5_stems(song_name, output_folder="backend/output"):
    """
    Gera espectrogramas para as 5 trilhas separadas (MP3).
    """
    song_path = os.path.join(output_folder, song_name)
    stems = ['vocals', 'drums', 'bass', 'piano', 'other']
    
    plt.figure(figsize=(15, 10))
    plt.suptitle(f"Análise de Frequência: {song_name}", fontsize=16)

    for i, stem in enumerate(stems):
        file_path = os.path.join(song_path, f"{stem}.mp3")
        
        if os.path.exists(file_path):
            # Carrega o MP3 usando librosa
            y, sr = librosa.load(file_path, sr=None)
            S = librosa.feature.melspectrogram(y=y, sr=sr)
            S_dB = librosa.power_to_db(S, ref=prosperity.max)

            # Plota no grid (3 linhas, 2 colunas)
            plt.subplot(3, 2, i+1)
            librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr)
            plt.colorbar(format='%+2.0f dB')
            plt.title(f"Trilha: {stem.capitalize()}")
        else:
            print(f"⚠️ Aviso: Arquivo {stem}.mp3 não encontrado em {song_path}")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Salva a imagem de comparação
    viz_output = os.path.join(song_path, "spectrogram_comparison.png")
    plt.savefig(viz_output)
    print(f"📊 Visualização gerada com sucesso em: {viz_output}")
    plt.show()

if __name__ == "__main__":
    # Altere aqui para o nome da pasta da música que você acabou de processar
    # Exemplo: se processou 'fhop.mp3', a pasta será 'fhop'
    nome_da_musica = "fhop" 
    visualize_5_stems(nome_da_musica)