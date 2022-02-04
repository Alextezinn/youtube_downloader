import os
from urllib.error import HTTPError
from typing import Optional, List

import pytube
from pytube import YouTube, extract, exceptions, request
from pytube.streams import Stream


class YouTubeStream(Stream):

    def download(
        self,
        output_path: Optional[str] = None,
        filename: Optional[str] = None,
        filename_prefix: Optional[str] = None,
        skip_existing: bool = True,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = 0
    ) -> str:

        file_path = self.get_file_path(
            filename=filename,
            output_path=output_path,
            filename_prefix=filename_prefix,
        )

        if skip_existing and self.exists_at_path(file_path):
            raise Exception(f'Файл {file_path} уже существует')

        bytes_remaining = self.filesize
        print(f'Скачивается ({self.filesize} всего байт) файл в {file_path}')

        for download_percent in self.download_byte(file_path, bytes_remaining):
            yield download_percent

        self.on_complete(file_path)

    def download_byte(self,
        file_path: Optional[str],
        bytes_remaining: Optional[int],
        timeout: Optional[int] = None,
        max_retries: Optional[int] = 0
    ):

        with open(file_path, "wb") as fh:
            try:
                for chunk in request.stream(
                    self.url,
                    timeout=timeout,
                    max_retries=max_retries
                ):

                    bytes_remaining -= len(chunk)
                    percent_completed = 100 - ((bytes_remaining / self.filesize) * 100)

                    yield percent_completed

                    self.on_progress(chunk, fh, bytes_remaining)

            except HTTPError as e:
                if e.code != 404:
                    raise

                for chunk in request.seq_stream(
                    self.url,
                    timeout=timeout,
                    max_retries=max_retries
                ):

                    bytes_remaining -= len(chunk)
                    percent_completed = 100 - ((bytes_remaining / self.filesize) * 100)

                    yield percent_completed

                    self.on_progress(chunk, fh, bytes_remaining)


    def __repr__(self) -> str:
        parts = ['itag="{s.itag}"', 'mime_type="{s.mime_type}"']
        if self.includes_video_track:
            parts.extend(['res="{s.resolution}"', 'fps="{s.fps}fps"'])
            if not self.is_adaptive:
                parts.extend(
                    ['vcodec="{s.video_codec}"', 'acodec="{s.audio_codec}"',]
                )
            else:
                parts.extend(['vcodec="{s.video_codec}"'])
        else:
            parts.extend(['abr="{s.abr}"', 'acodec="{s.audio_codec}"'])
        parts.extend(['progressive="{s.is_progressive}"', 'type="{s.type}"'])
        return f"<YouTubeStream: {' '.join(parts).format(s=self)}>"


class YouTubeVideoDownloaderHighestResolution(YouTube):
    def __init__(self, url: str):
        super().__init__(url)
        self._fmt_streams: Optional[List[YouTubeStream]] = None

    def download_video(self, filename=None, output_path=None):
        video_stream = self.streams.filter(adaptive=True, file_extension='mp4').first()

        for download_percent in video_stream.download(output_path=output_path, filename=filename):
            yield int(download_percent)

    def download_audio(self, filename=None, output_path=None):
        audio_stream = self.streams.filter(only_audio=True).desc().first()

        for download_percent in audio_stream.download(output_path=output_path, filename=filename):
            yield  download_percent

    @staticmethod
    def merge_audio_with_video(videofile="Inna name.mp4", audiofile="name.webm", outputfile="output.mp4"):
        command_cmd = f"ffmpeg -y -i \"{videofile}\" -i \"{audiofile}\" -map 0:v -map 1:a -c copy -strict -2 \"{outputfile}\""
        os.system(command_cmd)

    @property
    def fmt_streams(self):

        self.check_availability()
        if self._fmt_streams:
            return self._fmt_streams

        self._fmt_streams = []

        stream_manifest = extract.apply_descrambler(self.streaming_data)

        try:
            extract.apply_signature(stream_manifest, self.vid_info, self.js)
        except exceptions.ExtractError:
            # To force an update to the js file, we clear the cache and retry
            self._js = None
            self._js_url = None
            pytube.__js__ = None
            pytube.__js_url__ = None
            extract.apply_signature(stream_manifest, self.vid_info, self.js)

        for stream in stream_manifest:
            video = YouTubeStream(
                stream=stream,
                monostate=self.stream_monostate,
            )
            self._fmt_streams.append(video)

        self.stream_monostate.title = self.title
        self.stream_monostate.duration = self.length

        return self._fmt_streams