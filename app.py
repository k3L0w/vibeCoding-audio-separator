import os
import re
import subprocess
import threading
import customtkinter as ctk
from tkinter import filedialog
import pygame
# Importamos a função de visualização que você já tem no backend
from backend.visualizer import visualize_demucs_stems 

class VibeCodingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("VibeCoding - Estúdio de Alta Fidelidade")
        self.geometry("600x820") # Aumentado para o novo botão
        self.configure(fg_color="#0f0f13")

        pygame.mixer.init()

        # UI - Título Neon
        self.label = ctk.CTkLabel(self, text="VibeCoding: Estúdio de Isolamento", 
                                 font=("Arial", 24, "bold"), text_color="#00f2ff")
        self.label.pack(pady=20)

        self.progress_bar = ctk.CTkProgressBar(self, width=450, height=15, 
                                              progress_color="#7000ff", fg_color="#1a1a2e")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="Status: Pronto", text_color="#00ffcc")
        self.status_label.pack(pady=5)

        self.select_button = ctk.CTkButton(self, text="Selecionar Música e Isolar Trilhas", 
                                          command=self.select_file, fg_color="#7000ff")
        self.select_button.pack(pady=20)

        # Painel do Player e Visualização (Inicia oculto)
        self.player_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        ctk.CTkLabel(self.player_frame, text="🎸 Controles de Estudo & Análise", 
                     font=("Arial", 16, "bold"), text_color="#7000ff").pack(pady=10)

        # Botões de Instrumentos
        self.create_player_button("🎤 Voz", "vocals", "#ff00ff")
        self.create_player_button("🥁 Bateria", "drums", "#00d4ff")
        self.create_player_button("🎸 Baixo", "bass", "#00ffcc")
        self.create_player_button("🎹 Outros", "other", "#7000ff")

        # Botão para abrir o Gráfico Neon (Espectrograma)
        self.viz_button = ctk.CTkButton(self.player_frame, text="📊 Ver Análise de Frequência", 
                                       command=self.open_visualizer, fg_color="#1a1a2e", 
                                       border_width=2, border_color="#00f2ff")
        self.viz_button.pack(pady=15, fill="x", padx=100)

        ctk.CTkButton(self.player_frame, text="🛑 Parar Áudio", 
                      command=self.stop_all, fg_color="#ff4b2b").pack(pady=10)

        self.selected_path = ""
        self.song_name = ""

    def create_player_button(self, text, stem, color):
        btn = ctk.CTkButton(self.player_frame, text=text, fg_color=color,
                            command=lambda: self.play_stem(stem))
        btn.pack(pady=5, fill="x", padx=100)

    def select_file(self):
        path = filedialog.askopenfilename(filetypes=[("Áudio", "*.mp3 *.wav *.flac")])
        if path:
            self.selected_path = path
            self.song_name = os.path.splitext(os.path.basename(path))[0]
            self.start_processing_thread()

    def start_processing_thread(self):
        self.select_button.configure(state="disabled")
        self.player_frame.pack_forget()
        self.status_label.configure(text="🧠 IA Separando Instrumentos...", text_color="yellow")
        self.progress_bar.set(0)
        threading.Thread(target=self.run_demucs, daemon=True).start()

    def run_demucs(self):
        output_dir = os.path.abspath("backend/output")
        python_env = os.path.expanduser("~/Documents/vibeCoding/venv_demucs/bin/python3")
        cmd = [python_env, "-m", "demucs", "--mp3", "-n", "htdemucs", "-o", output_dir, self.selected_path]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            match = re.search(r"(\d+)%", line)
            if match:
                self.after(0, lambda v=int(match.group(1))/100: self.progress_bar.set(v))
            print(line, end="")
        process.wait()
        self.after(0, self.finish_ui)

    def finish_ui(self):
        self.status_label.configure(text="✅ Trilhas Prontas!", text_color="#00ffcc")
        self.progress_bar.set(1)
        self.select_button.configure(state="normal")
        self.player_frame.pack(pady=10, fill="x")
        os.system('notify-send "VibeCoding" "Processamento concluído!"')

    def play_stem(self, stem_name):
        file_path = os.path.join("backend/output/htdemucs", self.song_name, f"{stem_name}.mp3")
        if os.path.exists(file_path):
            pygame.mixer.stop()
            pygame.mixer.Sound(file_path).play()
            self.status_label.configure(text=f"Ouvindo Solo: {stem_name.upper()}", text_color="#00f2ff")

    def open_visualizer(self):
        """Chama a função do backend para gerar os gráficos"""
        if self.song_name:
            self.status_label.configure(text="📊 Gerando Espectrogramas...", text_color="#00f2ff")
            # Executa em uma thread separada para não travar a UI
            threading.Thread(target=lambda: visualize_demucs_stems(self.song_name), daemon=True).start()

    def stop_all(self):
        pygame.mixer.stop()
        self.status_label.configure(text="Áudio Parado", text_color="#00ffcc")

if __name__ == "__main__":
    app = VibeCodingApp()
    app.mainloop()