import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np # Corrigido de 'prosperity'

def visualize_demucs_stems(song_name, output_folder="backend/output"):
    """
    Gera espectrogramas para as trilhas separadas pelo Demucs.
    """
    # O Demucs cria uma pasta com o nome do modelo (htdemucs) antes da pasta da música
    song_path = os.path.join(output_folder, "htdemucs", song_name)
    stems = ['vocals', 'drums', 'bass', 'other']
    
    plt.figure(figsize=(15, 10))
    plt.suptitle(f"VibeCoding - Análise de Frequência (Demucs): {song_name}", fontsize=16, color='#00f2ff')

    for i, stem in enumerate(stems):
        file_path = os.path.join(song_path, f"{stem}.mp3")
        
        if os.path.exists(file_path):
            y, sr = librosa.load(file_path, sr=None)
            S = librosa.feature.melspectrogram(y=y, sr=sr)
            S_dB = librosa.power_to_db(S, ref=np.max) # Corrigido aqui

            plt.subplot(2, 2, i+1)
            librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr)
            plt.colorbar(format='%+2.0f dB')
            plt.title(f"Trilha: {stem.capitalize()}", color='white')
        else:
            print(f"⚠️ Aviso: Arquivo {stem}.mp3 não encontrado em {song_path}")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.gcf().set_facecolor('#0f0f13')
    
    viz_output = os.path.join(song_path, "spectrogram_comparison.png")
    plt.savefig(viz_output)
    print(f"📊 Visualização gerada com sucesso em: {viz_output}")
    plt.show()

if __name__ == "__main__":
    # Coloque aqui o nome do ficheiro que processou (sem o .mp3)
    visualize_demucs_stems("Indesculpavel(Ao-Vivo)fhop")