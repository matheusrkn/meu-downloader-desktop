> ℹ️ **Este projeto é apenas para fins educacionais.** Leia o [Disclaimer](#disclaimer) ao final para mais informações.

# 🎵 Mathew Downloader APP (MP3/MP4)

Aplicativo simples e funcional para baixar vídeos do YouTube em diferentes qualidades, com suporte a conversão direta para áudio (MP3), utilizando interface gráfica via Tkinter.

---

## 🧠 Objetivo

Este projeto foi criado com fins **acadêmicos e de aprendizado pessoal** em desenvolvimento Python. A aplicação permite baixar vídeos do YouTube com segurança e convertê-los para MP3 ou MP4, sem exposição a riscos comuns como malwares em sites de download.

---

## 💡 Funcionalidades

- 🎞️ Download de vídeos em diversas qualidades:
  - 144p SD
  - 360p SD
  - 720p HD
  - 1080p UHD
  - Melhor Qualidade disponível
- 🎧 Extração de áudio em MP3
- 📂 Escolha de diretório para salvar os arquivos
- 🔄 Feedback visual em tempo real durante o download
- 🧩 Suporte a playlists (com limitações)
- ✅ Integração com FFMPEG embutido
- 🔒 Log de eventos (debug.log)

---

## 🖼️ Interface

A interface gráfica é feita com `Tkinter`, simples e funcional, ideal para quem não está familiarizado com terminal.

---

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- Tkinter (GUI)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (YouTube Downloader)
- FFmpeg (para conversão de áudio e vídeo)
- threading, logging, subprocess

---

## 🚫 Avisos Importantes

- Certos vídeos podem não ser baixáveis devido a restrições de privacidade ou **direitos autorais**.
- O aplicativo pode interpretar **URLs de playlists** como múltiplos downloads.  
  Para interromper, utilize o **Gerenciador de Tarefas** (`Win + R > taskmgr`).

---

## 📜 Código de Conduta e Licenciamento

- Este projeto é de uso **estritamente pessoal e educacional**.
- **Não é permitido** o uso comercial, redistribuição ou cópia sem autorização do autor.
- A aplicação **não está disponível online** e não deve ser hospedada por terceiros.
- O código é disponibilizado como base de estudo e experimentação.

---

## ⚙️ Requisitos para Execução

- Python 3.8+
- Biblioteca `yt-dlp` instalada:
  ```bash
  pip install yt-dlp

---

## Disclaimer

> Este projeto **não possui vínculo com o YouTube** nem com qualquer entidade de streaming.  
> O autor **não se responsabiliza pelo uso indevido** do aplicativo.  
> Utilizar este software para baixar conteúdos protegidos por direitos autorais **pode violar os Termos de Serviço do YouTube**.

