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
        self.geometry("600x450")

        # Rótulo principal
        self.label = ctk.CTkLabel(self, text="VibeCoding: Separador de 5 Instrumentos", font=("Arial", 18, "bold"))
        self.label.pack(pady=20)

        # Botão de seleção
        self.select_button = ctk.CTkButton(self, text="Selecionar MP3 e Iniciar", command=self.select_file, height=45, fg_color="#1f538d")
        self.select_button.pack(pady=10)

        # BARRA DE PROGRESSO
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=20)

        # Status
        self.status_label = ctk.CTkLabel(self, text="Status: Pronto para processar", text_color="gray")
        self.status_label.pack(pady=5)

        # BOTÕES DE AÇÃO (Escondidos inicialmente)
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.view_button = ctk.CTkButton(self.button_frame, text="Ver Gráficos", command=self.open_visualizer, fg_color="green", hover_color="#050")
        self.folder_button = ctk.CTkButton(self.button_frame, text="Abrir Pasta de MP3", command=self.open_output_folder, fg_color="#d35400", hover_color="#a04000")
        
        self.selected_path = ""
        self.song_name = ""

    def select_file(self):
        self.selected_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
        if self.selected_path:
            self.song_name = os.path.splitext(os.path.basename(self.selected_path))[0]
            self.label.configure(text=f"Música: {self.song_name}")
            self.start_processing()

    def start_processing(self):
        self.status_label.configure(text="Status: IA trabalhando no i5...", text_color="yellow")
        self.select_button.configure(state="disabled")
        self.view_button.pack_forget()
        self.folder_button.pack_forget()
        
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        
        thread = threading.Thread(target=self.run_engine)
        thread.start()

    def run_engine(self):
        try:
            # Executa o processador atualizado
            result = subprocess.run(["python3", "backend/processor.py"], capture_output=True, text=True)
            
            self.after(0, self.stop_progress)

            if result.returncode == 0:
                self.status_label.configure(text="✅ Concluído! Arquivos prontos.", text_color="green")
                self.view_button.pack(side="left", padx=10) 
                self.folder_button.pack(side="left", padx=10)
            else:
                self.status_label.configure(text="❌ Erro no Spleeter.", text_color="red")
        except Exception as e:
            self.status_label.configure(text=f"Erro: {str(e)}", text_color="red")
        finally:
            self.select_button.configure(state="normal")

    def stop_progress(self):
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(1)

    def open_visualizer(self):
        subprocess.Popen(["python3", "backend/visualizer.py"])

    def open_output_folder(self):
        """Abre a pasta de saída no Dolphin (KDE/Ubuntu Studio)"""
        output_path = os.path.abspath(f"backend/output/{self.song_name}")
        if os.path.exists(output_path):
            # xdg-open é o comando padrão Linux para abrir pastas/arquivos
            subprocess.run(["xdg-open", output_path])
        else:
            self.status_label.configure(text="Pasta não encontrada!", text_color="orange")

if __name__ == "__main__":
    app = VibeCodingApp()
    app.mainloop()