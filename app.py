import os  # Biblioteca para manipular caminhos de arquivos e pastas
import re  # Biblioteca de expressões regulares para capturar o progresso da IA
import subprocess  # Permite executar o Demucs como um processo externo no Ubuntu
import threading  # Permite que a IA rode em segundo plano sem travar a interface
import random  # Usado para simular a variação visual nos VU Meters
import customtkinter as ctk  # Framework moderno para a interface visual neon
from tkinter import filedialog  # Janela padrão para selecionar arquivos de áudio
import pygame  # Motor de áudio de baixa latência para tocar os 6 canais

# =================================================================
# 🎸 RIFFFORGE - v1.3 (CÓDIGO DOCUMENTADO)
# =================================================================

class RiffForgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()  # Inicializa a janela principal do CustomTkinter

        self.title("RiffForge: Professional 6-Channel Mixer")  # Define o título da aplicação
        self.geometry("750x1000")  # Define o tamanho da janela
        self.configure(fg_color="#0f0f13")  # Define a cor de fundo (Dark Theme)

        # Inicializa o mixer do Pygame otimizado para hardware Latitude
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.set_num_channels(12)  # Reserva canais extras para evitar cortes de áudio

        self.master_gain = 1.0  # Multiplicador global de volume
        self.solo_track = None  # Armazena qual trilha está isolada pelo botão Solo
        self.muted_tracks = set()  # Conjunto que armazena trilhas silenciadas

        # Configuração visual e técnica dos 6 instrumentos (stems)
        self.stem_configs = {
            "vocals": {"name": "🎤 VOZ", "color": "#ff00ff"},
            "drums":  {"name": "🥁 BATERIA", "color": "#00d4ff"},
            "bass":   {"name": "🎸 BAIXO", "color": "#00ffcc"},
            "guitar": {"name": "🎸 GUITARRA", "color": "#ffff00"},
            "piano":  {"name": "🎹 TECLADO", "color": "#00ffff"},
            "other":  {"name": "🎼 OUTROS", "color": "#7000ff"}
        }

        # Cria dicionários para gerenciar os objetos de áudio e elementos da UI
        self.channels = {stem: pygame.mixer.Channel(i) for i, stem in enumerate(self.stem_configs.keys())}
        self.sounds = {}  # Armazena os objetos Sound carregados
        self.vu_meters = {}  # Armazena as barras de progresso (VU)
        self.volume_sliders = {}  # Armazena os sliders de volume
        self.mute_buttons = {}  # Armazena os botões de Mute
        self.solo_buttons = {}  # Armazena os botões de Solo

        # --- CONSTRUÇÃO DA INTERFACE (UI) ---
        self.label = ctk.CTkLabel(self, text="RIFFFORGE", font=("Impact", 45, "italic"), text_color="#00f2ff")
        self.label.pack(pady=(20, 5)) # Título principal com estilo neon

        # Seção do Master Gain (Controle Geral)
        self.master_strip = ctk.CTkFrame(self, fg_color="#1a1a2e", border_width=2, border_color="#00f2ff")
        self.master_strip.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(self.master_strip, text="🎚️ MASTER GAIN", text_color="#00f2ff", font=("Arial", 14, "bold")).pack(side="left", padx=15)

        # Slider Master (Usa lambda para evitar o erro de inicialização)
        self.master_slider = ctk.CTkSlider(self.master_strip, from_=0, to=1, progress_color="#00f2ff",
                                          command=lambda v: self.update_master_volume(v))
        self.master_slider.set(1.0)
        self.master_slider.pack(side="left", fill="x", expand=True, padx=20)

        # Barra de progresso da IA (Forja)
        self.progress_bar = ctk.CTkProgressBar(self, width=500, height=12, progress_color="#7000ff", fg_color="#1a1a2e")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        # Rótulo de status dinâmico
        self.status_label = ctk.CTkLabel(self, text="Status: Pronto para forjar", text_color="#00ffcc")
        self.status_label.pack(pady=5)

        # Botão para importar arquivos e iniciar a separação
        self.select_button = ctk.CTkButton(self, text="IMPORTAR PARA FORJA (6-STEMS)", command=self.select_file,
                                          fg_color="#7000ff", font=("Arial", 14, "bold"))
        self.select_button.pack(pady=10)

        # Frame principal do Mixer (Fica oculto até a música ser carregada)
        self.mixer_frame = ctk.CTkFrame(self, fg_color="#16161e", corner_radius=15)

        # Controles principais de transporte (Play/Stop)
        self.master_btns = ctk.CTkFrame(self.mixer_frame, fg_color="transparent")
        self.master_btns.pack(pady=15, fill="x", padx=20)
        ctk.CTkButton(self.master_btns, text="▶ PLAY ALL", width=140, fg_color="#00ffcc", text_color="black",
                   command=self.play_all).pack(side="left", padx=10)
        ctk.CTkButton(self.master_btns, text="🛑 STOP", width=140, fg_color="#ff4b2b",
                   command=self.stop_all).pack(side="left", padx=10)

        # Área de rolagem para os canais individuais
        self.scroll_frame = ctk.CTkScrollableFrame(self.mixer_frame, width=650, height=500, fg_color="transparent")
        self.scroll_frame.pack(pady=5, padx=10)

        # Loop para criar as trilhas do mixer baseadas na configuração
        for stem, config in self.stem_configs.items():
            self.create_mixer_strip(stem, config)

        self.selected_path = "" # Caminho do arquivo original
        self.song_name = "" # Nome da música para gestão de cache
        self.update_vu_loop() # Inicia a animação dos medidores VU

    def create_mixer_strip(self, stem, config):
        """Cria uma faixa de canal individual (Slider, VU, Solo, Mute)"""
        strip = ctk.CTkFrame(self.scroll_frame, fg_color="#1a1a2e")
        strip.pack(fill="x", pady=8, padx=5)

        # VU Meter Vertical (Barra que reage ao som)
        vu = ctk.CTkProgressBar(strip, width=12, height=70, orientation="vertical", progress_color=config["color"], fg_color="#0f0f13")
        vu.set(0)
        vu.pack(side="left", padx=(10, 5), pady=5)
        self.vu_meters[stem] = vu

        # Nome do Instrumento
        lbl = ctk.CTkLabel(strip, text=config["name"], text_color=config["color"], font=("Arial", 11, "bold"), width=90)
        lbl.pack(side="left")

        # Slider de Volume Individual
        slider = ctk.CTkSlider(strip, from_=0, to=1, progress_color=config["color"], command=lambda v, s=stem: self.update_volume(s, v))
        slider.set(1.0)
        slider.pack(side="left", fill="x", expand=True, padx=10)
        self.volume_sliders[stem] = slider

        # Container para botões Solo/Mute
        btn_frame = ctk.CTkFrame(strip, fg_color="transparent")
        btn_frame.pack(side="right", padx=10)

        # Botão Mute (Silenciar)
        m_btn = ctk.CTkButton(btn_frame, text="M", width=35, height=35, fg_color="#333", command=lambda s=stem: self.toggle_mute(s))
        m_btn.pack(side="left", padx=2)
        self.mute_buttons[stem] = m_btn

        # Botão Solo (Isolar)
        s_btn = ctk.CTkButton(btn_frame, text="S", width=35, height=35, fg_color="#333", command=lambda s=stem: self.toggle_solo(s))
        s_btn.pack(side="left", padx=2)
        self.solo_buttons[stem] = s_btn

    def select_file(self):
        """Gerencia a seleção de arquivos e a lógica de Cache"""
        path = filedialog.askopenfilename(filetypes=[("Áudio", "*.mp3 *.wav *.flac")])
        if path:
            self.selected_path = path
            self.song_name = os.path.splitext(os.path.basename(path))[0] # Remove a extensão

            # Verifica se os arquivos processados já existem no HD
            cache_path = os.path.abspath(os.path.join("backend/output/htdemucs_6s", self.song_name))

            if os.path.exists(cache_path) and any(f.endswith('.mp3') for f in os.listdir(cache_path)):
                # Carregamento instantâneo (Smart-Skip)
                self.status_label.configure(text="⚡ Cache Detetado! Carregando Sessão...", text_color="#00f2ff")
                self.after(500, self.finish_ui)
            else:
                # Inicia a IA se for uma música nova
                self.start_processing_thread()

    def start_processing_thread(self):
        """Prepara a interface e inicia o thread da IA"""
        self.select_button.configure(state="disabled") # Bloqueia o botão durante o processo
        self.mixer_frame.pack_forget() # Esconde o mixer anterior se houver
        self.status_label.configure(text="🔥 Forjando Stems (Modelo 6s)...", text_color="yellow")
        threading.Thread(target=self.run_demucs_6s, daemon=True).start()

    def run_demucs_6s(self):
        """Executa o Demucs via terminal com prioridade 'nice' no Linux"""
        output_dir = os.path.abspath("backend/output")
        python_env = os.path.expanduser("~/Documents/vibeCoding/venv_demucs/bin/python3") # Caminho do venv

        # Executa com prioridade 10 para não travar o Ubuntu Studio
        cmd = ["nice", "-n", "10", python_env, "-m", "demucs", "--mp3", "-n", "htdemucs_6s", "-o", output_dir, self.selected_path]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            match = re.search(r"(\d+)%", line) # Captura a porcentagem de progresso
            if match:
                self.after(0, lambda v=int(match.group(1))/100: self.progress_bar.set(v)) # Atualiza barra de progresso
        process.wait()
        self.after(0, self.finish_ui) # Finaliza a interface após a conclusão

    def finish_ui(self):
        """Exibe o mixer e carrega os sons após o processamento"""
        self.status_label.configure(text="✨ Sessão Pronta!", text_color="#00ffcc")
        self.progress_bar.set(1)
        self.select_button.configure(state="normal")
        self.mixer_frame.pack(pady=10, fill="both", expand=True, padx=20) # Mostra o mixer na tela
        self.load_sounds()

    def load_sounds(self):
        """Carrega os arquivos MP3 separados no motor Pygame"""
        base_dir = os.path.join("backend/output/htdemucs_6s", self.song_name)
        for stem in self.stem_configs.keys():
            file_path = os.path.join(base_dir, f"{stem}.mp3")
            if os.path.exists(file_path):
                self.sounds[stem] = pygame.mixer.Sound(file_path) # Cria o objeto de som

    def update_master_volume(self, value):
        """Atualiza o multiplicador global de volume"""
        self.master_gain = float(value)
        for stem in self.stem_configs.keys():
            self.update_volume(stem, self.volume_sliders[stem].get())

    def toggle_mute(self, stem):
        """Liga/Desliga o silenciamento de uma trilha"""
        if stem in self.muted_tracks:
            self.muted_tracks.remove(stem)
            self.mute_buttons[stem].configure(fg_color="#333")
        else:
            self.muted_tracks.add(stem)
            self.mute_buttons[stem].configure(fg_color="#ff4b2b") # Botão fica vermelho quando em mute
        self.update_volume(stem, self.volume_sliders[stem].get())

    def toggle_solo(self, stem):
        """Isola uma trilha e silencia todas as outras"""
        if self.solo_track == stem:
            self.solo_track = None # Desativa o solo
            self.solo_buttons[stem].configure(fg_color="#333", text_color="white")
        else:
            if self.solo_track:
                self.solo_buttons[self.solo_track].configure(fg_color="#333", text_color="white")
            self.solo_track = stem
            self.solo_buttons[stem].configure(fg_color="#ffff00", text_color="black") # Botão fica amarelo em Solo

        # Atualiza o volume de todos os canais para refletir a nova regra de Solo
        for s in self.stem_configs.keys():
            self.update_volume(s, self.volume_sliders[s].get())

    def update_volume(self, stem, value):
        """Calcula o volume final baseado em Slider, Master Gain, Solo e Mute"""
        if stem in self.channels:
            if self.solo_track:
                # Regra: Se houver Solo, apenas a trilha Solo toca. O resto é 0.
                final_vol = float(value) * self.master_gain if stem == self.solo_track else 0
            else:
                # Regra: Se a trilha está em Mute, volume é 0. Caso contrário, aplica ganhos.
                final_vol = 0 if stem in self.muted_tracks else float(value) * self.master_gain
            self.channels[stem].set_volume(final_vol)

    def update_vu_loop(self):
        """Animação dos VUs a 20 FPS (Sincronizado com o Playback)"""
        if pygame.mixer.get_busy(): # Só anima se houver áudio tocando
            for stem, channel in self.channels.items():
                if channel.get_busy() and channel.get_volume() > 0:
                    # Gera uma leve variação (jitter) para dar vida ao medidor
                    level = channel.get_volume() * random.uniform(0.7, 1.0)
                    self.vu_meters[stem].set(level)
                else:
                    self.vu_meters[stem].set(0) # Zera se o canal estiver em silêncio
        else:
            for vu in self.vu_meters.values(): vu.set(0) # Zera todos se o Play parar
        self.after(50, self.update_vu_loop) # Reagenda a execução para 50ms depois

    def play_all(self):
        """Inicia a reprodução sincronizada de todos os stems"""
        pygame.mixer.stop() # Garante que nada esteja tocando antes de começar
        for stem, sound in self.sounds.items():
            self.channels[stem].play(sound) # Toca o som no canal reservado
            self.update_volume(stem, self.volume_sliders[stem].get()) # Aplica o volume atual
        self.status_label.configure(text="🎧 RiffForge Session: ACTIVE", text_color="#00f2ff")

    def stop_all(self):
        """Para todos os canais de áudio instantaneamente"""
        pygame.mixer.stop()
        self.status_label.configure(text="Sessão Parada", text_color="#00ffcc")

# --- EXECUÇÃO DO APP ---
if __name__ == "__main__":
    app = RiffForgeApp() # Instancia a aplicação
    app.mainloop() # Inicia o loop principal de eventos
