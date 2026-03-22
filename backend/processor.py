
import os
from pydub import AudioSegment
from spleeter.separator import Separator

def separate_stems(mp3_filepath, output_folder="output"):
    """
    Separates vocals and accompaniment from an MP3 file using Spleeter.

    Args:
        mp3_filepath (str): The path to the input MP3 file.
        output_folder (str): The folder where the separated stems will be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Initialize Spleeter separator with 2 stems (vocals and accompaniment)
    separator = Separator("spleeter:2stems")

    # Separate the audio and save the results
    separator.separate_to_file(mp3_filepath, output_folder)

    print(f"Stems separated and saved to {output_folder}")

if __name__ == "__main__":
    # Example usage (replace with your actual MP3 file path)
    input_folder = "backend/input"
    output_folder = "backend/output"
    # Assuming there's only one MP3 file in the input folder for this example
    mp3_files = [f for f in os.listdir(input_folder) if f.endswith(".mp3")]

    if mp3_files:
        mp3_filepath = os.path.join(input_folder, mp3_files[0])
        separate_stems(mp3_filepath, output_folder)
        print(f"Stems separated and saved to {output_folder}")
    else:
        print(f"No MP3 files found in {input_folder}")
