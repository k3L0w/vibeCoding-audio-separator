import os
import re
import subprocess
import threading
import customtkinter as ctk
from tkinter import filedialog
import pygame

# =================================================================
# 🎸 RIFFFORGE - ULTRA-FIDELITY AUDIO DECONSTRUCTION ENGINE
# "Forjando o som perfeito, nota por nota."
# =================================================================

class RiffForgeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("RiffForge: Professional 6-Channel Mixer")
        self.geometry("700x980")
        self.configure(fg_color="#0f0f13")

        # Motor de áudio otimizado para Dell Latitude E6430
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.set_num_channels(12) 
        
        self.master_gain = 1.0 
        
        self.stem_configs = {
            "vocals": {"name": "🎤 VOZ", "color": "#ff00ff"},
            "drums":  {"name": "🥁 BATERIA", "color": "#00d4ff"},
            "bass":   {"name": "🎸 BAIXO", "color": "#00ffcc"},
            "guitar": {"name": "🎸 GUITARRA", "color": "#ffff00"},
            "piano":  {"name": "🎹 TECLADO", "color": "#00ffff"},
            "other":  {"name": "🎼 OUTROS", "color": "#7000ff"}
        }
        
        self.channels = {stem: pygame.mixer.Channel(i) for i, stem in enumerate(self.stem_configs.keys())}
        self.sounds = {}

        # UI RIFFFORGE
        self.label = ctk.CTkLabel(self, text="RIFFFORGE", 
                                 font=("Impact", 45, "italic"), text_color="#00f2ff")
        self.label.pack(pady=(20, 5))
        
        # MASTER GAIN CONTROL
        self.master_strip = ctk.CTkFrame(self, fg_color="#1a1a2e", border_width=2, border_color="#00f2ff")
        self.master_strip.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(self.master_strip, text="🎚️ MASTER GAIN", text_color="#00f2ff", 
                     font=("Arial", 14, "bold")).pack(side="left", padx=15)

        self.master_slider = ctk.CTkSlider(self.master_strip, from_=0, to=1, progress_color="#00f2ff",
                                          command=self.update_master_volume)
        self.master_slider.set(1.0)
        self.master_slider.pack(side="left", fill="x", expand=True, padx=20)

        self.progress_bar = ctk.CTkProgressBar(self, width=500, height=12, 
                                              progress_color="#7000ff", fg_color="#1a1a2e")
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Status: Pronto para forjar", text_color="#00ffcc")
        self.status_label.pack(pady=5)

        self.select_button = ctk.CTkButton(self, text="IMPORTAR PARA FORJA (6-STEMS)", 
                                          command=self.select_file, fg_color="#7000ff", 
                                          font=("Arial", 14, "bold"))
        self.select_button.pack(pady=10)

        self.mixer_frame = ctk.CTkFrame(self, fg_color="#16161e", corner_radius=15)
        
        self.master_btns = ctk.CTkFrame(self.mixer_frame, fg_color="transparent")
        self.master_btns.pack(pady=15, fill="x", padx=20)
        
        ctk.CTkButton(self.master_btns, text="▶ PLAY ALL", width=140, fg_color="#00ffcc", 
                      text_color="black", font=("Arial", 12, "bold"), command=self.play_all).pack(side="left", padx=10)
        ctk.CTkButton(self.master_btns, text="🛑 STOP", width=140, fg_color="#ff4b2b", 
                      font=("Arial", 12, "bold"), command=self.stop_all).pack(side="left", padx=10)

        self.scroll_frame = ctk.CTkScrollableFrame(self.mixer_frame, width=600, height=450, fg_color="transparent")
        self.scroll_frame.pack(pady=5, padx=10)

        self.volume_sliders = {}
        for stem, config in self.stem_configs.items():
            self.create_mixer_strip(stem, config)

        self.selected_path = ""
        self.song_name = ""

    def create_mixer_strip(self, stem, config):
        # CORREÇÃO: Removido pady do construtor do Frame
        strip = ctk.CTkFrame(self.scroll_frame, fg_color="#1a1a2e")
        strip.pack(fill="x", pady=12, padx=5) 
        
        lbl = ctk.CTkLabel(strip, text=config["name"], text_color=config["color"], font=("Arial", 12, "bold"), width=110)
        lbl.pack(side="left", padx=10)
        
        slider = ctk.CTkSlider(strip, from_=0, to=1, progress_color=config["color"],
                              command=lambda v, s=stem: self.update_volume(s, v))
        slider.set(1.0)
        slider.pack(side="left", fill="x", expand=True, padx=15)
        self.volume_sliders[stem] = slider

    def select_file(self):
        path = filedialog.askopenfilename(filetypes=[("Áudio", "*.mp3 *.wav *.flac")])
        if path:
            self.selected_path = path
            self.song_name = os.path.splitext(os.path.basename(path))[0]
            self.start_processing_thread()

    def start_processing_thread(self):
        self.select_button.configure(state="disabled")
        self.mixer_frame.pack_forget()
        self.status_label.configure(text="🔥 Forjando Stems (Modelo 6s)...", text_color="yellow")
        threading.Thread(target=self.run_demucs_6s, daemon=True).start()

    def run_demucs_6s(self):
        output_dir = os.path.abspath("backend/output")
        python_env = os.path.expanduser("~/Documents/vibeCoding/venv_demucs/bin/python3")
        cmd = [python_env, "-m", "demucs", "--mp3", "-n", "htdemucs_6s", "-o", output_dir, self.selected_path]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            match = re.search(r"(\d+)%", line)
            if match:
                self.after(0, lambda v=int(match.group(1))/100: self.progress_bar.set(v))
        process.wait()
        self.after(0, self.finish_ui)

    def finish_ui(self):
        self.status_label.configure(text="✨ Forja Concluída!", text_color="#00ffcc")
        self.progress_bar.set(1)
        self.select_button.configure(state="normal")
        self.mixer_frame.pack(pady=10, fill="both", expand=True, padx=20)
        self.load_sounds()

    def load_sounds(self):
        for stem in self.stem_configs.keys():
            file_path = os.path.join("backend/output/htdemucs_6s", self.song_name, f"{stem}.mp3")
            if os.path.exists(file_path):
                self.sounds[stem] = pygame.mixer.Sound(file_path)

    def update_master_volume(self, value):
        self.master_gain = float(value)
        for stem in self.stem_configs.keys():
            self.update_volume(stem, self.volume_sliders[stem].get())

    def update_volume(self, stem, value):
        if stem in self.channels:
            final_vol = float(value) * self.master_gain
            self.channels[stem].set_volume(final_vol)

    def play_all(self):
        pygame.mixer.stop()
        for stem, sound in self.sounds.items():
            self.channels[stem].play(sound)
            self.update_volume(stem, self.volume_sliders[stem].get())
        self.status_label.configure(text="🎧 RiffForge Session: ACTIVE", text_color="#00f2ff")

    def stop_all(self):
        pygame.mixer.stop()
        self.status_label.configure(text="Sessão Parada", text_color="#00ffcc")

if __name__ == "__main__":
    app = RiffForgeApp()
    app.mainloop()