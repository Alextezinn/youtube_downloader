from youtube_downloader.youtube import YouTubeVideoDownloaderHighestResolution


if __name__ == "__main__":
    youtube = YouTubeVideoDownloaderHighestResolution("https://www.youtube.com/watch?v=8Fl6d_fSRNs")
    youtube.download_video()
