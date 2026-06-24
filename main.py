import customtkinter as ctk
from tkinter import filedialog, messagebox
from pytubefix import YouTube
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class YoutubeDownloader:

    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader - por José Gabriel")
        self.root.geometry("650x350")

        # Título
        self.titulo = ctk.CTkLabel(
            root,
            text="YouTube Downloader",
            font=("Segoe UI", 24, "bold")
        )
        self.titulo.pack(pady=20)

        # Campo URL
        self.url_entry = ctk.CTkEntry(
            root,
            width=550,
            height=40,
            placeholder_text="Cole a URL do vídeo aqui..."
        )
        self.url_entry.pack(pady=10)

        # Frame para pasta
        self.frame_pasta = ctk.CTkFrame(root, fg_color="transparent")
        self.frame_pasta.pack(pady=10)

        self.path_entry = ctk.CTkEntry(
            self.frame_pasta,
            width=420,
            height=40,
            placeholder_text="Escolha o local para salvar o vídeo..."
        )
        self.path_entry.pack(side="left", padx=5)

        self.botao_pasta = ctk.CTkButton(
            self.frame_pasta,
            text="Selecionar",
            command=self.escolher_pasta,
            width=120
        )
        self.botao_pasta.pack(side="left", padx=5)

        # Informações do vídeo
        self.info_label = ctk.CTkLabel(
            root,
            text="Cole uma URL do YouTube",
            wraplength=550
        )
        self.info_label.pack(pady=10)

        # Barra de progresso
        self.progress = ctk.CTkProgressBar(
            root,
            width=550
        )
        self.progress.pack(pady=10)
        self.progress.set(0)

        # Botão  de download
        self.botao_download = ctk.CTkButton(
            root,
            text="Baixar Vídeo",
            command=self.iniciar_download,
            width=200,
            height=40
        )
        self.botao_download.pack(pady=20)

    def escolher_pasta(self):
        pasta = filedialog.askdirectory()

        if pasta:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, pasta)

    def progresso(self, stream, chunk, bytes_restantes):
        tamanho_total = stream.filesize

        baixado = tamanho_total - bytes_restantes
        percentual = baixado / tamanho_total

        self.progress.set(percentual)

    def download(self):
        try:
            url = self.url_entry.get().strip()

            if not url:
                messagebox.showwarning(
                    "Aviso",
                    "Informe uma URL."
                )
                return

            yt = YouTube(
                url,
                on_progress_callback=self.progresso
            )

            self.info_label.configure(
                text=f"Título: {yt.title}"
            )

            stream = yt.streams.get_highest_resolution()

            destino = self.path_entry.get().strip()

            if not destino:
                destino = "."

            stream.download(output_path=destino)

            self.progress.set(1)

            messagebox.showinfo(
                "Sucesso",
                "Download concluído!"
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                str(erro)
            )

    def iniciar_download(self):
        self.progress.set(0)

        threading.Thread(
            target=self.download,
            daemon=True
        ).start()


app = ctk.CTk()
YoutubeDownloader(app)
app.mainloop()