import customtkinter as ctk
from tkinter import filedialog
import subprocess
import threading
import os
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VibeCodingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela
        self.title("VibeCoding - Audio Separator Pro")
        self.geometry("600x550")

        # Rótulo principal
        self.label = ctk.CTkLabel(self, text="VibeCoding: Inteligência Artificial Musical", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)

        # SELETOR DE MOTOR (Spleeter vs Demucs)
        self.engine_mode = ctk.CTkSegmentedButton(self, 
                                                 values=["Spleeter (Rápido)", "Demucs (Qualidade 6-Stems)"], 
                                                 command=self.update_mode_text)
        self.engine_mode.set("Spleeter (Rápido)")
        self.engine_mode.pack(pady=10)

        self.info_label = ctk.CTkLabel(self, text="Ideal para rascunhos rápidos (2-3 min)", text_color="gray")
        self.info_label.pack(pady=5)

        # Botão de seleção
        self.select_button = ctk.CTkButton(self, text="Selecionar MP3 e Iniciar", command=self.select_file, height=45, font=("Arial", 14, "bold"))
        self.select_button.pack(pady=20)

        # BARRA DE PROGRESSO
        self.progress_bar = ctk.CTkProgressBar(self, width=450)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        # Status e Tempo
        self.status_label = ctk.CTkLabel(self, text="Status: Pronto para processar", text_color="gray")
        self.status_label.pack(pady=5)
        
        self.time_label = ctk.CTkLabel(self, text="", text_color="#3498db")
        self.time_label.pack(pady=5)

        # BOTÕES DE AÇÃO (Escondidos inicialmente)
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=20)

        self.folder_button = ctk.CTkButton(self.button_frame, text="Abrir Pasta de MP3", command=self.open_output_folder, fg_color="#d35400", hover_color="#a04000")
        
        self.selected_path = ""
        self.song_name = ""
        self.start_time = 0

    def update_mode_text(self, value):
        if "Spleeter" in value:
            self.info_label.configure(text="Ideal para rascunhos rápidos (2-3 min)")
        else:
            self.info_label.configure(text="Alta fidelidade: Isola Guitarra e Piano (12-18 min)")

    def select_file(self):
        self.selected_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        if self.selected_path:
            self.song_name = os.path.splitext(os.path.basename(self.selected_path))[0]
            self.label.configure(text=f"Música: {self.song_name}")
            self.start_processing()

    def notify_user(self, title, message):
        """Envia uma notificação visual e sonora no Ubuntu Studio (KDE)"""
        os.system(f'notify-send "{title}" "{message}" --icon=multimedia-audio-player')
        # Toca o som de conclusão padrão do sistema
        os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga &')

    def start_processing(self):
        self.start_time = time.time()
        self.status_label.configure(text="Status: IA trabalhando... Prepare o café! ☕", text_color="yellow")
        self.time_label.configure(text="Processando...")
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
                # Chama o Python do ambiente isolado venv_demucs usando o modelo de 6 stems
                python_env = os.path.abspath("venv_demucs/bin/python3")
                command = [
                    python_env, "-m", "demucs", 
                    "--mp3", 
                    "-n", "htdemucs_6s", 
                    "-o", output_dir, 
                    self.selected_path
                ]
            else:
                # Chama o backend original no ambiente padrão (Spleeter)
                command = ["python3", "backend/processor.py"]

            result = subprocess.run(command, capture_output=True, text=True)
            
            # Calcula o tempo total
            end_time = time.time()
            duration = round((end_time - self.start_time) / 60, 2)
            
            self.after(0, self.finish_ui, result.returncode, duration)
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Erro crítico: {str(e)}", text_color="red"))

    def finish_ui(self, returncode, duration):
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(1)
        self.select_button.configure(state="normal")
        
        if returncode == 0:
            self.status_label.configure(text="✅ Sucesso! Arquivos gerados.", text_color="green")
            self.time_label.configure(text=f"Tempo total: {duration} minutos")
            self.folder_button.pack(side="left", padx=10)
            
            # Notificação final
            self.notify_user("VibeCoding Pro", f"Concluído: {self.song_name}\nTempo: {duration} min")
        else:
            self.status_label.configure(text="❌ Erro no processamento.", text_color="red")
            self.notify_user("VibeCoding Erro", "Ocorreu um erro inesperado no motor de IA.")

    def open_output_folder(self):
        """Abre a pasta raiz de saída para facilitar a localização das tracks"""
        output_path = os.path.abspath("backend/output")
        if os.path.exists(output_path):
            subprocess.run(["xdg-open", output_path])

if __name__ == "__main__":
    app = VibeCodingApp()
    app.mainloop()