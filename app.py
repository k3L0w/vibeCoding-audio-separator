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

        self.title("VibeCoding - Audio Separator Pro")
        self.geometry("600x400")

        # Rótulo principal
        self.label = ctk.CTkLabel(self, text="Selecione um MP3 para separar os 5 instrumentos", font=("Arial", 16, "bold"))
        self.label.pack(pady=20)

        # Botão de seleção
        self.select_button = ctk.CTkButton(self, text="Selecionar e Processar", command=self.select_file, height=40)
        self.select_button.pack(pady=10)

        # BARRA DE PROGRESSO (Nova!)
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0) # Começa em 0%
        self.progress_bar.pack(pady=20)

        # Status
        self.status_label = ctk.CTkLabel(self, text="Status: Pronto", text_color="gray")
        self.status_label.pack(pady=5)

        # BOTÃO DE VISUALIZAÇÃO (Novo - começa escondido)
        self.view_button = ctk.CTkButton(self, text="Ver Gráficos de Frequência", command=self.open_visualizer, fg_color="green", hover_color="#050")
        
        self.selected_path = ""
        self.song_name = ""

    def select_file(self):
        self.selected_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        if self.selected_path:
            self.song_name = os.path.splitext(os.path.basename(self.selected_path))[0]
            self.label.configure(text=f"Música: {self.song_name}")
            self.start_processing()

    def start_processing(self):
        self.status_label.configure(text="Status: IA trabalhando... (CPU i5 em ação)", text_color="yellow")
        self.select_button.configure(state="disabled")
        self.view_button.pack_forget() # Esconde o botão se rodar de novo
        
        # Inicia a animação da barra (modo indeterminado para IA)
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        
        thread = threading.Thread(target=self.run_engine)
        thread.start()

    def run_engine(self):
        try:
            # Executa o processador que já testamos
            result = subprocess.run(["python3", "backend/processor.py"], capture_output=True, text=True)
            
            self.after(0, self.stop_progress) # Para a barra na thread principal

            if result.returncode == 0:
                self.status_label.configure(text="✅ Sucesso! 5 Stems gerados em MP3.", text_color="green")
                self.view_button.pack(pady=10) # Mostra o botão de ver gráficos
            else:
                self.status_label.configure(text="❌ Erro no processamento da IA.", text_color="red")
        except Exception as e:
            self.status_label.configure(text=f"Erro crítico: {str(e)}", text_color="red")
        finally:
            self.select_button.configure(state="normal")

    def stop_progress(self):
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(1) # Enche a barra

    def open_visualizer(self):
        """Chama o nosso visualizador para a música atual"""
        self.status_label.configure(text="📊 Abrindo visualizador...")
        subprocess.Popen(["python3", "backend/visualizer.py"])

if __name__ == "__main__":
    app = VibeCodingApp()
    app.mainloop()