import os

import pytube
from pytube import YouTube


class YouTubeVideoDownloaderHighestResolution(YouTube):

    def download_video(self, filename=None, output_path=None) -> None:
        video_stream = self.streams.filter(adaptive=True, file_extension='mp4').first()
        audio_stream = self.streams.filter(only_audio=True).desc().first()

        video_stream.download(output_path=output_path, filename=filename)
        audio_stream.download(output_path=output_path, filename=filename)

    def merge_audio_with_video(self, videofile="name.mp4",
                               audiofile = "name.webm",
                               outputfile="output.mp4"):

        command_cmd = f"ffmpeg -y -i '{videofile}' -i '{audiofile}' -map 0:v -map 1:a -c copy -strict -2 {outputfile}"
        os.system(command_cmd)
