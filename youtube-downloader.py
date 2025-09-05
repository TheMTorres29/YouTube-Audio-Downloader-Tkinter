import re
import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from pytubefix import YouTube
from pytubefix.cli import on_progress
import threading


class YouTubeAudioDownloader:
    def __init__(self, root):
        self.root = root
        self.current_theme = "light"
        self.setup_ui()
        self.set_theme(self.current_theme)

    def is_valid_youtube_url(self, url):
        pattern = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]{11}(&.*)?$'
        return re.match(pattern, url) is not None

    def sanitize_filename(self, title):
        return re.sub(r'[\\/:"*?<>|]+', '_', title)

    def download_audio(self):
        url = self.url_entry.get()
        if not self.is_valid_youtube_url(url):
            messagebox.showerror("Invalid URL", "Please enter a valid YouTube URL.")
            return
        self.download_btn.config(state=tk.DISABLED)
        self.progress["value"] = 0  # Reset progress bar
        # Start the download in a new thread
        threading.Thread(target=self.download_audio_thread, args=(url,), daemon=True).start()

    def download_audio_thread(self, url):
        try:
            yt = YouTube(url, on_progress_callback=self.on_progress)
            ys = yt.streams.get_audio_only()
            ext = ".m4a"
            default_filename = self.sanitize_filename(yt.title) + ext
            save_path = filedialog.asksaveasfilename(
                defaultextension=ext,
                filetypes=[("M4A Audio", "*.m4a"), ("All Files", "*.*")],
                initialfile=default_filename,
                title="Save audio as..."
            )
            if not save_path:
                self.download_btn.config(state=tk.NORMAL)
                return
            output_dir = os.path.dirname(save_path)
            filename = os.path.basename(save_path)
            ys.download(output_path=output_dir, filename=filename)
            messagebox.showinfo("Success", f"Downloaded audio for {yt.title}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download: {e}")
        finally:
            self.download_btn.config(state=tk.NORMAL)

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percent = int(bytes_downloaded / total_size * 100)
        self.progress["value"] = percent
        self.root.update_idletasks()

    def set_theme(self, mode):
        style = ttk.Style()
        if mode == "dark":
            self.root.configure(bg="#222222")
            self.main_frame.configure(style="Dark.TFrame")
            style.configure("Dark.TFrame", background="#222222")
            style.configure("TLabel", background="#222222", foreground="#f0f0f0")
            style.configure("TEntry", fieldbackground="#333333", foreground="#000000")
            style.configure("TButton", background="#333333", foreground="#000000")
            self.footer.configure(background="#222222", foreground="#888888")
        else:
            self.root.configure(bg="#f0f0f0")
            self.main_frame.configure(style="Light.TFrame")
            style.configure("Light.TFrame", background="#f0f0f0")
            style.configure("TLabel", background="#f0f0f0", foreground="#222222")
            style.configure("TEntry", fieldbackground="#ffffff", foreground="#222222")
            style.configure("TButton", background="#e0e0e0", foreground="#222222")
            self.footer.configure(background="#f0f0f0", foreground="gray")

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.set_theme(self.current_theme)

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.main_frame, text="YouTube to M4A Downloader", font=("Segoe UI", 16, "bold")).pack(pady=(0, 10))
        ttk.Label(self.main_frame, text="Enter YouTube URL:", font=("Segoe UI", 10)).pack(anchor="w")
        self.url_entry = ttk.Entry(self.main_frame, width=50, font=("Segoe UI", 10))
        self.url_entry.pack(pady=5, fill=tk.X)

        self.download_btn = ttk.Button(self.main_frame, text="Download Audio", command=self.download_audio)
        self.download_btn.pack(pady=10)

        self.progress = ttk.Progressbar(self.main_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=5)

        self.theme_btn = ttk.Button(self.main_frame, text="Toggle Light/Dark Mode", command=self.toggle_theme)
        self.theme_btn.pack(pady=10)

        self.footer = ttk.Label(self.main_frame, text="© 2025 MT29", font=("Segoe UI", 8), foreground="gray")
        self.footer.pack(side="bottom", pady=(10, 0))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("MT29 YouTube to M4A Downloader")
    root.geometry("420x260")
    root.resizable(False, False)
    app = YouTubeAudioDownloader(root)
    root.mainloop()