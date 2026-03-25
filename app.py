import os
import re
import subprocess
import threading
import customtkinter as ctk
from tkinter import filedialog
import pygame

# =================================================================
# 🎸 RIFFFORGE - ULTRA-FIDELITY AUDIO DECONSTRUCTION ENGINE
# Desenvolvido por: Pereira
# Versão: 2.0 (6-Channel Mixer Edition)
# Finalidade: Estúdio de isolamento local para músicos e produtores.
# =================================================================

class RiffForgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # --- CONFIGURAÇÃO DA JANELA PRINCIPAL ---
        # Definimos dimensões que comportem confortavelmente os 6 faders de volume.
        self.title("RiffForge: 6-Channel Studio Mixer")
        self.geometry("700x950")
        self.configure(fg_color="#0f0f13") # Estética Dark Mode Industrial

        # --- MOTOR DE ÁUDIO SINCRONIZADO (PYGAME) ---
        # Inicializamos o mixer com buffer reduzido (512) para garantir que o 
        # disparo de múltiplas trilhas ocorra sem atrasos perceptíveis (latência).
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # Reservamos 10 canais para permitir expansões futuras sem conflitos de áudio.
        pygame.mixer.set_num_channels(10) 
        
        # DICIONÁRIO DE CONFIGURAÇÃO DOS STEMS (CANAIS):
        # Aqui definimos a identidade visual de cada instrumento no Mixer.
        # O diferencial do RiffForge é o isolamento de GUITARRA e PIANO individualmente.
        self.stem_configs = {
            "vocals": {"name": "🎤 VOZ", "color": "#ff00ff"},
            "drums":  {"name": "🥁 BATERIA", "color": "#00d4ff"},
            "bass":   {"name": "🎸 BAIXO", "color": "#00ffcc"},
            "guitar": {"name": "🎸 GUITARRA", "color": "#ffff00"},
            "piano":  {"name": "🎹 TECLADO", "color": "#00ffff"},
            "other":  {"name": "🎼 OUTROS", "color": "#7000ff"}
        }
        
        # Mapeamento de Canais: Cada instrumento recebe um canal exclusivo do Pygame.
        self.channels = {stem: pygame.mixer.Channel(i) for i, stem in enumerate(self.stem_configs.keys())}
        self.sounds = {} # Repositório para os arquivos carregados na memória RAM.

        # --- INTERFACE VISUAL (BRANDING RIFFFORGE) ---
        self.label = ctk.CTkLabel(self, text="RIFFFORGE", 
                                 font=("Impact", 45, "italic"), text_color="#00f2ff")
        self.label.pack(pady=(30, 5))
        
        self.sub_label = ctk.CTkLabel(self, text="Audio Deconstruction Engine", 
                                     font=("Arial", 14, "bold"), text_color="#7000ff")
        self.sub_label.pack(pady=(0, 20))

        # Barra de Progresso Neon: Essencial para monitorar a "Forja" das trilhas pela IA.
        self.progress_bar = ctk.CTkProgressBar(self, width=500, height=15, 
                                              progress_color="#7000ff", fg_color="#1a1a2e")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Status: Pronto para forjar trilhas", text_color="#00ffcc")
        self.status_label.pack(pady=5)

        self.select_button = ctk.CTkButton(self, text="IMPORTAR ÁUDIO PARA FORJA", 
                                          command=self.select_file, fg_color="#7000ff", 
                                          hover_color="#5a00cc", font=("Arial", 14, "bold"))
        self.select_button.pack(pady=15)

        # --- PAINEL DO MIXER INTERATIVO ---
        # Este painel contém os controles de volume e só é revelado após o processamento.
        self.mixer_frame = ctk.CTkFrame(self, fg_color="#16161e", corner_radius=15)
        
        # Controles Master (Play/Stop da Sessão)
        self.master_frame = ctk.CTkFrame(self.mixer_frame, fg_color="transparent")
        self.master_frame.pack(pady=15, fill="x", padx=20)
        
        ctk.CTkButton(self.master_frame, text="▶ PLAY SESSION", width=140, fg_color="#00ffcc", 
                      text_color="black", font=("Arial", 12, "bold"), command=self.play_all).pack(side="left", padx=10)
        ctk.CTkButton(self.master_frame, text="🛑 STOP", width=140, fg_color="#ff4b2b", 
                      font=("Arial", 12, "bold"), command=self.stop_all).pack(side="left", padx=10)

        # Área de Rolagem para os Faders (Sliders)
        self.scroll_frame = ctk.CTkScrollableFrame(self.mixer_frame, width=600, height=450, fg_color="transparent")
        self.scroll_frame.pack(pady=10, padx=10)

        # Geração dinâmica dos controles de volume baseada no dicionário de Stems.
        self.volume_sliders = {}
        for stem, config in self.stem_configs.items():
            self.create_mixer_strip(stem, config)

        self.selected_path = ""
        self.song_name = ""

    def create_mixer_strip(self, stem, config):
        """Cria uma faixa de canal individual com label e slider de volume."""
        strip = ctk.CTkFrame(self.scroll_frame, fg_color="#1a1a2e", pady=12)
        strip.pack(fill="x", pady=5, padx=5)
        
        lbl = ctk.CTkLabel(strip, text=config["name"], text_color=config["color"], font=("Arial", 13, "bold"), width=120)
        lbl.pack(side="left", padx=10)
        
        # O Slider controla o ganho do canal em tempo real (0.0 a 1.0).
        slider = ctk.CTkSlider(strip, from_=0, to=1, progress_color=config["color"],
                              command=lambda v, s=stem: self.update_volume(s, v))
        slider.set(1.0) # Inicia em volume total (Unity Gain)
        slider.pack(side="left", fill="x", expand=True, padx=15)
        self.volume_sliders[stem] = slider

    def select_file(self):
        """Abre o seletor de arquivos para escolher a música a ser processada."""
        path = filedialog.askopenfilename(filetypes=[("Áudio", "*.mp3 *.wav *.flac")])
        if path:
            self.selected_path = path
            self.song_name = os.path.splitext(os.path.basename(path))[0]
            self.start_processing_thread()

    def start_processing_thread(self):
        """Gerencia o processamento em uma Thread separada para não travar a interface."""
        self.select_button.configure(state="disabled")
        self.mixer_frame.pack_forget() # Oculta mixagens anteriores
        self.status_label.configure(text="🔥 Forjando Stems (Modelo Neural 6s)...", text_color="yellow")
        self.progress_bar.set(0)
        
        # Iniciamos a "Forja" Neural.
        threading.Thread(target=self.run_demucs_6s, daemon=True).start()

    def run_demucs_6s(self):
        """
        EXECUÇÃO DO MOTOR NEURAL: Invoca o Demucs com o modelo de 6 stems.
        Este modelo isola: vocals, drums, bass, guitar, piano, other.
        """
        output_dir = os.path.abspath("backend/output")
        # Caminho para o ambiente virtual dedicado ao Demucs (evita conflito de bibliotecas).
        python_env = os.path.expanduser("~/Documents/vibeCoding/venv_demucs/bin/python3")
        
        # Comando para extração de alta fidelidade em MP3.
        cmd = [python_env, "-m", "demucs", "--mp3", "-n", "htdemucs_6s", "-o", output_dir, self.selected_path]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            # Captura o progresso (0-100%) da saída do terminal para atualizar a barra neon.
            match = re.search(r"(\d+)%", line)
            if match:
                self.after(0, lambda v=int(match.group(1))/100: self.progress_bar.set(v))
            print(line, end="") # Debug no terminal
        process.wait()
        self.after(0, self.finish_ui)

    def finish_ui(self):
        """Finaliza a fase de processamento e libera o Mixer para o usuário."""
        self.status_label.configure(text="✨ Forja Concluída!", text_color="#00ffcc")
        self.progress_bar.set(1)
        self.select_button.configure(state="normal")
        self.mixer_frame.pack(pady=15, fill="both", expand=True, padx=20)
        self.load_sounds() # Carrega os resultados na memória RAM
        
        # Notificação do sistema (Ubuntu Studio / Linux)
        os.system('notify-send "RiffForge" "Sua mixagem interativa está pronta!"')

    def load_sounds(self):
        """Carrega os arquivos de áudio processados como objetos de som do Pygame."""
        for stem in self.stem_configs.keys():
            file_path = os.path.join("backend/output/htdemucs_6s", self.song_name, f"{stem}.mp3")
            if os.path.exists(file_path):
                self.sounds[stem] = pygame.mixer.Sound(file_path)

    def play_all(self):
        """
        REPRODUÇÃO SINCRONIZADA: O coração do RiffForge.
        Dispara todos os canais simultaneamente, aplicando o volume dos Sliders.
        """
        pygame.mixer.stop() # Limpa reproduções anteriores
        for stem, sound in self.sounds.items():
            # Toca o som no canal correspondente ao instrumento.
            self.channels[stem].play(sound)
            # Define o volume inicial baseado na posição atual do Slider.
            self.channels[stem].set_volume(self.volume_sliders[stem].get())
        self.status_label.configure(text="🎧 RiffForge Session: ACTIVE", text_color="#00f2ff")

    def update_volume(self, stem, value):
        """Ajusta o volume do canal em tempo real enquanto a música toca."""
        if stem in self.channels:
            self.channels[stem].set_volume(float(value))

    def stop_all(self):
        """Interrompe toda a reprodução de áudio imediatamente."""
        pygame.mixer.stop()
        self.status_label.configure(text="Sessão Parada", text_color="#00ffcc")

if __name__ == "__main__":
    # Inicialização da aplicação RiffForge
    app = RiffForgeApp()
    app.mainloop()