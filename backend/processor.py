import os
from pydub import AudioSegment
from spleeter.separator import Separator

def convert_to_mp3(source_file):
    """Converte um arquivo wav para mp3 e remove o original."""
    target_file = source_file.replace(".wav", ".mp3")
    audio = AudioSegment.from_wav(source_file)
    audio.export(target_file, format="mp3", bitrate="192k")
    os.remove(source_file) # Remove o wav para economizar espaço
    return target_file

def separate_stems_5_mp3(mp3_filepath, output_folder="backend/output"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Inicializa o separador para 5 trilhas
    separator = Separator("spleeter:5stems")
    
    print(f"🎸 Iniciando separação (5 stems) de: {os.path.basename(mp3_filepath)}")
    
    # O Spleeter separa e salva como .wav inicialmente
    separator.separate_to_file(mp3_filepath, output_folder)
    
    # Localiza a pasta criada pelo Spleeter (geralmente o nome do arquivo)
    song_name = os.path.splitext(os.path.basename(mp3_filepath))[0]
    song_folder = os.path.join(output_folder, song_name)
    
    print(f"📦 Convertendo trilhas para MP3...")
    for file in os.listdir(song_folder):
        if file.endswith(".wav"):
            full_path = os.path.join(song_folder, file)
            convert_to_mp3(full_path)
            
    print(f"✅ Processo concluído! Arquivos MP3 salvos em: {song_folder}")

if __name__ == "__main__":
    input_folder = "backend/input"
    output_folder = "backend/output"
    
    mp3_files = [f for f in os.listdir(input_folder) if f.endswith(".mp3")]

    if mp3_files:
        mp3_filepath = os.path.join(input_folder, mp3_files[0])
        separate_stems_5_mp3(mp3_filepath, output_folder)
    else:
        print(f"❌ Nenhum arquivo MP3 encontrado em {input_folder}")