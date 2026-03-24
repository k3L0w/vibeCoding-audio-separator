import customtkinter as ctk
from tkinter import filedialog
import subprocess
import threading
import os

# Configuração visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class VibeCodingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("VibeCoding - Audio Separator")
        self.geometry("500x300")

        # Rótulo de instrução
        self.label = ctk.CTkLabel(self, text="Selecione um arquivo MP3 para separar os stems", font=("Arial", 14))
        self.label.pack(pady=20)

        # Botão de seleção
        self.select_button = ctk.CTkButton(self, text="Selecionar MP3", command=self.select_file)
        self.select_button.pack(pady=10)

        # Status do processamento
        self.status_label = ctk.CTkLabel(self, text="Status: Aguardando...", text_color="gray")
        self.status_label.pack(pady=20)

        # Caminho do arquivo selecionado
        self.selected_path = ""

    def select_file(self):
        self.selected_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        if self.selected_path:
            filename = os.path.basename(self.selected_path)
            self.label.configure(text=f"Selecionado: {filename}")
            self.start_processing()

    def start_processing(self):
        self.status_label.configure(text="Status: Processando... (Isso pode levar alguns minutos)", text_color="yellow")
        self.select_button.configure(state="disabled")
        
        # Rodar em uma thread separada para não travar a janela
        thread = threading.Thread(target=self.run_engine)
        thread.start()

    def run_engine(self):
        try:
            # Chama o seu processador Python que acabamos de testar
            # Usamos o venv atual para garantir que o Spleeter seja encontrado
            result = subprocess.run(["python3", "backend/processor.py"], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.status_label.configure(text="Status: Concluído com Sucesso! \o/", text_color="green")
            else:
                self.status_label.configure(text="Status: Erro no processamento.", text_color="red")
        except Exception as e:
            self.status_label.configure(text=f"Erro: {str(e)}", text_color="red")
        finally:
            self.select_button.configure(state="normal")

if __name__ == "__main__":
    app = VibeCodingApp()
    app.mainloop()