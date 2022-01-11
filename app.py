from youtube_downloader.youtube import YouTubeVideoDownloaderHighestResolution


if __name__ == "__main__":
    youtube = YouTubeVideoDownloaderHighestResolution("url на видео с ютуба")
    youtube.merge_audio_with_video(videofile="name.mp4",
                                   audiofile = "name.webm",
                                   outputfile="output.mp4")
