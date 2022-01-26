from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk

from youtube_downloader.youtube import YouTubeVideoDownloaderHighestResolution


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        url_label = Label(text="URL")
        self.url_entry = Entry(width=40)

        url_label.place(x=60, y=20)
        self.url_entry.place(x=100, y=20)

        videoname_label = Label(text="Имя видеофайла")
        self.videoname_entry = Entry()

        videoname_label.place(x=60, y=50)
        self.videoname_entry.place(x=170, y=50)

        audioname_label = Label(text="Имя аудиофайла")
        self.audioname_entry = Entry()

        audioname_label.place(x=60, y=80)
        self.audioname_entry.place(x=170, y=80)

        btn_download = Button(text="Скачать", command=self.click_download)
        btn_download.place(x=50, y=220)

        btn_merge_audio_with_video = Button(text="Наложить аудио на видео",
                                            command=self.click_merge_audio_with_video)
        btn_merge_audio_with_video.place(x=200, y=220)

        label_progress_download_video = Label(text="Скачивание видеофайла")
        label_progress_download_video.place(x=20, y=130)

        self.pb_video = ttk.Progressbar(length=150, mode="determinate")
        self.pb_video.place(x=200, y=130)

        label_progress_download_audio = Label(text="Скачивание аудиофайла")
        label_progress_download_audio.place(x=20, y=160)

        self.pb_audio = ttk.Progressbar(length=150, mode="determinate")
        self.pb_audio.place(x=200, y=160)

    def click_download(self):
        youtube = YouTubeVideoDownloaderHighestResolution(self.url_entry.get())

        self.pb_video['value'] = 0
        for download_percent in youtube.download_video():
            self.pb_video['value'] += download_percent

        self.pb_audio['value'] = 0
        for download_percent in youtube.download_audio():
            self.pb_audio['value'] += download_percent

    def click_merge_audio_with_video(self):
        YouTubeVideoDownloaderHighestResolution.merge_audio_with_video(videofile=self.videoname_entry.get(),
                                                                       audiofile=self.audioname_entry.get())

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
