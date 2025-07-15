import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os
import threading
import yt_dlp
import logging
import subprocess

# ========= Função para localizar o FFMPEG dentro da pasta "bin" =========

if getattr(sys, 'frozen', False):
    caminho_ffmpeg = os.path.join(sys._MEIPASS, 'bin')
    caminho_icon = os.path.join(sys._MEIPASS, 'icon.ico')
else:
    caminho_ffmpeg = os.path.join(os.path.dirname(__file__), 'bin')
    caminho_icon = os.path.join(os.path.dirname(__file__), 'icon.ico')

    # Para caso o ffmpeg esteja instalado localmente, no PATH, substituir o script acima por:
    # caminho_ffmpeg = "ffmpeg"


# ============================ LOG DE DEPURAÇÃO ============================

class LoggerCustom:
    def debug(self, msg):
        logging.debug(msg)

    def info(self, msg):
        logging.info(msg)

    def warning(self, msg):
        logging.warning(msg)

    def error(self, msg):
        logging.error(msg)

    def critical(self, msg):
        logging.critical(msg)

    def exception(self, msg):
        logging.exception(msg)

log_path = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "debug.log")

logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ============================ FUNÇÕES PRINCIPAIS ============================

def escolher_diretorio():
    caminho = filedialog.askdirectory(title="Escolha onde salvar o arquivo")
    if caminho:
        destino_var.set(caminho)

def animar_botao_retorno(botao, original_color="#4CAF50", destaque_color="#ffcc00", vezes=4, intervalo=250):
    def piscar(contagem=0):
        nova_cor = destaque_color if contagem % 2 == 0 else original_color
        botao.config(bg=nova_cor)
        if contagem < vezes * 2:
            janela.after(intervalo, lambda: piscar(contagem + 1))
    piscar()

def processo_download():
    url = url_entry.get()
    destino = destino_var.get()
    opcao = tipo_var.get()
    qualidade = qualidade_var.get()

    if not url or not destino or not opcao or not qualidade:
        messagebox.showwarning("Campos incompletos", "Por favor, preencha todos os campos.")
        return

    status_var.set("Iniciando download...")
    logging.info(f"Iniciando download: {url} | Tipo: {opcao} | Qualidade: {qualidade}")

    botao_download.pack_forget()

    formatos = {
        "144p SD": "bestvideo[height<=144]+bestaudio/best[height<=144]",
        "360p SD": "bestvideo[height<=360]+bestaudio/best[height<=360]",
        "720p HD": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "1080p UHD": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "Melhor Qualidade": "bestvideo+bestaudio/best"
    }

    ydl_opts = {
        'format': formatos.get(qualidade, 'bestvideo+bestaudio/best'),
        'outtmpl': os.path.join(destino, '%(title)s.%(ext)s'),
        'ffmpeg_location': caminho_ffmpeg,
        'quiet': True,
        'postprocessors': [],
        'logger': LoggerCustom(),
    }

    def run():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                titulo = info.get('title', 'Arquivo')
                logging.info(f"Título detectado: {titulo}")

                if opcao == "audio":
                    abr = info.get('abr', 128)
                    prefer_quality = 256
                    real_quality = min(prefer_quality, abr)
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': str(real_quality),
                    }]
                    status_var.set(f"Convertendo para MP3 ({real_quality} kbps)...")
                    logging.info(f"Processando áudio para MP3 ({real_quality} kbps)")
           
                else:
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }]
                    status_var.set("Fazendo download do vídeo com áudio...")
                    logging.info("Processando vídeo com áudio...")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl_download:
                ydl_download.download([url])
                logging.info("Download concluído.")

            janela.after(0, lambda: status_var.set(f"'{titulo}' baixado com sucesso!"))

        except Exception as e:
            logging.error("Erro durante o download", exc_info=True)
            janela.after(0, lambda: status_var.set("Erro durante o download."))
            messagebox.showerror("Erro", str(e))

        finally:
            janela.after(0, lambda: [
                botao_download.pack(pady=(15, 10)),
                animar_botao_retorno(botao_download)
            ])

    threading.Thread(target=run).start()

# ============================ GUI ============================

import time
import sys

janela = tk.Tk()
janela.title("Mathew Downloader APP (MP3/MP4)")
janela.geometry("550x500")
janela.resizable(False, False)
janela.iconbitmap(caminho_icon)

destino_var = tk.StringVar()
status_var = tk.StringVar()

tk.Label(janela, text="Cole Aqui a URL do YouTube:").pack(pady=(10, 5))
url_entry = tk.Entry(janela, width=65, font=("Arial", 10))
url_entry.pack(pady=5)

frame_opcoes = tk.Frame(janela)
frame_opcoes.pack(pady=10)

tipo_var = tk.StringVar()
tk.Label(frame_opcoes, text="Tipo de Download:", font=("Arial", 10)).grid(row=0, column=0, padx=10, sticky='w')
tk.OptionMenu(frame_opcoes, tipo_var, "video", "audio").grid(row=0, column=1)

qualidade_var = tk.StringVar()
tk.Label(frame_opcoes, text="Qualidade:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky='w')
qualidade_opcoes = ["144p SD", "360p SD", "720p HD", "1080p UHD", "Melhor Qualidade"]
tk.OptionMenu(frame_opcoes, qualidade_var, *qualidade_opcoes).grid(row=1, column=1)

tk.Label(janela, text="Salvar em:", font=("Arial", 10)).pack(pady=(10, 5))
tk.Entry(janela, textvariable=destino_var, width=50, font=("Arial", 9), state="readonly").pack()
tk.Button(janela, text="Escolher pasta", command=escolher_diretorio).pack(pady=5)

botao_download = tk.Button(janela, text="Iniciar Download", command=processo_download, bg="#4CAF50", fg="white", width=25, font=("Arial", 11, "bold"))
botao_download.pack(pady=(15, 10))

tk.Label(janela, textvariable=status_var, fg="blue", font=("Arial", 10)).pack()

janela.mainloop()
