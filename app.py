import customtkinter as ctk
from tkinter import filedialog
import subprocess
import threading
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VibeCodingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VibeCoding - Multi-Engine Audio Separator")
        self.geometry("600x500")

        self.label = ctk.CTkLabel(self, text="Escolha o Motor de Separação", font=("Arial", 18, "bold"))
        self.label.pack(pady=15)

        # SELETOR DE MOTOR
        self.engine_mode = ctk.CTkSegmentedButton(self, values=["Spleeter (Rápido)", "Demucs (Qualidade)"], command=self.update_mode_text)
        self.engine_mode.set("Spleeter (Rápido)")
        self.engine_mode.pack(pady=10)

        self.info_label = ctk.CTkLabel(self, text="Ideal para rascunhos rápidos (2-3 min)", text_color="gray")
        self.info_label.pack(pady=5)

        self.select_button = ctk.CTkButton(self, text="Selecionar MP3 e Iniciar", command=self.select_file, height=45)
        self.select_button.pack(pady=20)

        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Status: Pronto", text_color="gray")
        self.status_label.pack(pady=10)

        self.folder_button = ctk.CTkButton(self, text="Abrir Pasta de Saída", command=self.open_output_folder, fg_color="#d35400")
        
        self.selected_path = ""
        self.song_name = ""

    def update_mode_text(self, value):
        if "Spleeter" in value:
            self.info_label.configure(text="Ideal para rascunhos rápidos (2-3 min)")
        else:
            self.info_label.configure(text="Alta fidelidade para Guitarras (8-12 min)")

    def select_file(self):
        self.selected_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        if self.selected_path:
            self.song_name = os.path.splitext(os.path.basename(self.selected_path))[0]
            self.start_processing()

    def start_processing(self):
        self.status_label.configure(text="Processando... Prepare o café! ☕", text_color="yellow")
        self.select_button.configure(state="disabled")
        self.folder_button.pack_forget()
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        
        thread = threading.Thread(target=self.run_engine)
        thread.start()

    def run_engine(self):
        try:
            mode = self.engine_mode.get()
            output_dir = os.path.abspath("backend/output")

            if "Demucs" in mode:
                # Chama o Python do ambiente isolado venv_demucs
                python_env = os.path.abspath("venv_demucs/bin/python3")
                command = [python_env, "-m", "demucs", "--mp3", "-o", output_dir, self.selected_path]

                # O modelo htdemucs_6s separa: vocals, drums, bass, other, guitar, piano
                command = [
                    python_env, "-m", "demucs", 
                    "--mp3", 
                    "-n", "htdemucs_6s", 
                    "-o", output_dir, 
                    self.selected_path
                ]
            else:
                # Chama o backend original no ambiente padrão
                command = ["python3", "backend/processor.py"]

            result = subprocess.run(command, capture_output=True, text=True)
            self.after(0, self.finish_ui, result.returncode)
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Erro: {str(e)}", text_color="red"))

    def finish_ui(self, returncode):
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(1)
        self.select_button.configure(state="normal")
        if returncode == 0:
            self.status_label.configure(text="✅ Concluído! Arquivos salvos.", text_color="green")
            self.folder_button.pack(pady=10)
        else:
            self.status_label.configure(text="❌ Erve um erro no processamento.", text_color="red")

    def open_output_folder(self):
        # Para o Demucs, a pasta costuma ser htdemucs/nome_da_musica
        path = os.path.abspath(f"backend/output")
        subprocess.run(["xdg-open", path])

if __name__ == "__main__":
    app = VibeCodingApp()
    app.mainloop()