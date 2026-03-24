import os
import re
import subprocess
import threading
import customtkinter as ctk
from tkinter import filedialog

class VibeCodingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VibeCoding - Demucs Edition")
        self.geometry("600x500")
        self.configure(fg_color="#0f0f13")

        # UI - Estética Neon para Músicos
        self.label = ctk.CTkLabel(self, text="VibeCoding: Alta Fidelidade (Demucs)", 
                                 font=("Arial", 22, "bold"), text_color="#00f2ff")
        self.label.pack(pady=30)

        self.status_label = ctk.CTkLabel(self, text="Status: Pronto para Processar", text_color="#00ffcc")
        self.status_label.pack(pady=5)

        self.progress_bar = ctk.CTkProgressBar(self, width=450, height=15, 
                                              progress_color="#7000ff", fg_color="#1a1a2e")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=20)

        self.select_button = ctk.CTkButton(self, text="Escolher Música e Isolar Trilhas", 
                                          command=self.select_file, fg_color="#7000ff", hover_color="#5a00cc")
        self.select_button.pack(pady=20)

        self.folder_button = ctk.CTkButton(self, text="📁 Ver Arquivos Separados", 
                                          command=self.open_output_folder, fg_color="#2c3e50")
        self.folder_button.pack_forget()

        self.selected_path = ""
        self.song_name = ""

    def select_file(self):
        path = filedialog.askopenfilename(filetypes=[("Áudio", "*.mp3 *.wav *.flac")])
        if path:
            self.selected_path = path
            self.song_name = os.path.splitext(os.path.basename(path))[0]
            self.start_processing_thread()

    def start_processing_thread(self):
        self.select_button.configure(state="disabled")
        self.status_label.configure(text="🧠 IA Separando Instrumentos...", text_color="yellow")
        self.progress_bar.set(0)
        
        thread = threading.Thread(target=self.run_demucs, daemon=True)
        thread.start()

    def run_demucs(self):
        output_dir = os.path.abspath("backend/output")
        # Caminho absoluto para o seu venv_demucs no Dell Latitude
        python_env = os.path.expanduser("~/Documents/vibeCoding/venv_demucs/bin/python3")
        
        # Modelo htdemucs: O melhor equilíbrio entre CPU e Qualidade
        cmd = [python_env, "-m", "demucs", "--mp3", "-n", "htdemucs", "-o", output_dir, self.selected_path]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        for line in process.stdout:
            # Captura o progresso [  0%] do Demucs
            match = re.search(r"(\d+)%", line)
            if match:
                val = int(match.group(1)) / 100
                self.after(0, lambda v=val: self.progress_bar.set(v))
            print(line, end="")

        process.wait()
        self.after(0, self.finish_ui)

    def finish_ui(self):
        self.status_label.configure(text="✅ Concluído! Trilhas Prontas.", text_color="#00ffcc")
        self.progress_bar.set(1)
        self.select_button.configure(state="normal")
        self.folder_button.pack(pady=10)
        os.system('notify-send "VibeCoding" "O isolamento de trilhas terminou!"')

    def open_output_folder(self):
        # O Demucs cria uma subpasta com o nome do modelo (htdemucs)
        path = os.path.abspath(f"backend/output/htdemucs/{self.song_name}")
        if not os.path.exists(path):
            path = os.path.abspath("backend/output")
        subprocess.run(["xdg-open", path])

if __name__ == "__main__":
    app = VibeCodingApp()
    app.mainloop()