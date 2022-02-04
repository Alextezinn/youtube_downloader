from pathlib import Path
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mb

from youtube_downloader.youtube import YouTubeVideoDownloaderHighestResolution


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.gui()

    def gui(self):
        self.current_dir = Path.cwd()

        url_label = Label(text="URL")
        self.url_entry = Entry(width=40)

        url_label.place(x=60, y=20)
        self.url_entry.place(x=100, y=20)

        btn_download = Button(text="Скачать", command=self.click_download)
        btn_download.place(x=50, y=220)

        label_progress_download_video = Label(text="Скачивание видеофайла")
        label_progress_download_video.place(x=20, y=130)

        self.pb_video = ttk.Progressbar(length=150, mode="determinate")
        self.pb_video.place(x=200, y=130)

        label_progress_download_audio = Label(text="Скачивание аудиофайла")
        label_progress_download_audio.place(x=20, y=160)

        self.pb_audio = ttk.Progressbar(length=150, mode="determinate")
        self.pb_audio.place(x=200, y=160)

    def click_download(self):
        if not (self.current_dir / Path('download')).exists():
            Path.mkdir(self.current_dir / Path('download'))

        youtube = YouTubeVideoDownloaderHighestResolution(url=self.url_entry.get())

        output_path = str(self.current_dir / Path('download'))

        self.pb_video['value'] = 0
        for download_percent in youtube.download_video(output_path=output_path):
            self.pb_video['value'] += download_percent

        self.pb_audio['value'] = 0
        for download_percent in youtube.download_audio(output_path=output_path):
            self.pb_audio['value'] += download_percent

        files = list(Path.iterdir(self.current_dir / Path('download')))

        if len(files) != 2:
            mb.showerror("Ошибка", "В папке должно быть два файла: аудио и видео")
        else:
            if not (self.current_dir / Path('output')).exists():
                Path.mkdir(self.current_dir / Path('output'))

            if str(files[0]).endswith(".mp4"):

                YouTubeVideoDownloaderHighestResolution.merge_audio_with_video(
                    videofile=str(files[0]),
                    audiofile=str(files[1]),
                    outputfile=str(self.current_dir / Path('output') / files[0].parts[-1])
                )

            else:
                YouTubeVideoDownloaderHighestResolution.merge_audio_with_video(
                    videofile=str(files[1]),
                    audiofile=str(files[0]),
                    outputfile=str(self.current_dir / Path('output') / files[1].parts[-1])
                )

        for file in Path.iterdir(self.current_dir / Path('download')):
            Path.unlink(self.current_dir / Path('download') / file)

        self.pb_audio['value'] = 0
        for download_percent in youtube.download_audio(output_path=output_path):
            self.pb_audio['value'] += download_percent

        files = list(Path.iterdir(self.current_dir / Path('download')))

        if len(files) != 2:
            mb.showerror("Ошибка", "В папке должно быть два файла: аудио и видео")
        else:
            if not (self.current_dir / Path('output')).exists():
                Path.mkdir(self.current_dir / Path('output'))

            if str(files[0]).endswith(".mp4"):

                YouTubeVideoDownloaderHighestResolution.merge_audio_with_video(
                    videofile=str(files[0]),
                    audiofile=str(files[1]),
                    outputfile=str(self.current_dir / Path('output') / files[0].parts[-1])
                )

            else:
                YouTubeVideoDownloaderHighestResolution.merge_audio_with_video(
                    videofile=str(files[1]),
                    audiofile=str(files[0]),
                    outputfile=str(self.current_dir / Path('output') / files[1].parts[-1])
                )

        for file in Path.iterdir(self.current_dir / Path('download')):
            Path.unlink(self.current_dir / Path('download') / file)


if __name__ == "__main__":
    app = App()

    app.title("Скачивание видео с Youtube")
    app.resizable(0, 0)
    w = app.winfo_screenwidth()
    h = app.winfo_screenheight()
    w = w // 2
    h = h // 2
    w = w - 200
    h = h - 155
    app.geometry(f'400x300+{w}+{h}')
    app.mainloop()
