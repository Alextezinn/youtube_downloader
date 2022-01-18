from pathlib import Path

from youtube_downloader.youtube import YouTubeVideoDownloaderHighestResolution


def main():
    current_dir = Path.cwd()

    if not (current_dir / Path('download')).exists():
        Path.mkdir(current_dir / Path('download'))

    youtube = YouTubeVideoDownloaderHighestResolution(
        url="url на видео с ютуба"
    )

    youtube.download_video(output_path=str(current_dir / Path('download')))

    files = list(Path.iterdir(current_dir / Path('download')))

    if len(files) != 2:
        print("Ошибка! В папке должно быть два файла: аудио и видео")
    else:
        if not (current_dir / Path('output')).exists():
            Path.mkdir(current_dir / Path('output'))

        if str(files[0]).endswith(".mp4"):

            YouTubeVideoDownloaderHighestResolution.merge_audio_with_video(
                videofile=str(files[0]),
                audiofile=str(files[1]),
                outputfile=str(current_dir / Path('output') / files[0].parts[-1])
            )

        else:
            YouTubeVideoDownloaderHighestResolution.merge_audio_with_video(
                videofile=str(files[1]),
                audiofile=str(files[0]),
                outputfile=str(current_dir / Path('output') / files[1].parts[-1])
            )

    for file in Path.iterdir(current_dir / Path('download')):
        Path.unlink(current_dir / Path('download') / file)


if __name__ == "__main__":
    main()



