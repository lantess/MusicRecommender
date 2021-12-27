import vlc
import pafy
import threading
CODE_BAD_LINK = -1


def _duration_to_seconds(duration: str) -> int:
    h = int(duration[:duration.find(':')])
    m = int(duration[duration.find(':') + 1:duration.rfind(':')])
    s = int(duration[duration.rfind(':') + 1:])
    return h * 60 * 60 + m * 60 + s


def _download(url: str):
    youtube_video = pafy.new(url)
    audio_stream = youtube_video.getbestaudio()
    audio_stream.download(filepath='../data/wav.old/'
                                   + audio_stream.title
                                   + '.' + audio_stream.extension)


def _play(_vlc, _player, url: str):
    youtube_video = pafy.new(url)
    audio_stream = youtube_video.getbestaudio()
    media = _vlc.media_new(audio_stream.url)
    media.get_mrl()
    _player.set_media(media)
    _player.play()


class MusicPlayer:
    def __init__(self):
        self._vlc = vlc.Instance()
        self._player = self._vlc.media_player_new()
        self._download_thread = None
        self._playing_thread = None

    def play(self, url: str) -> int:
        if url.find('youtube.com') == -1:
            return CODE_BAD_LINK
        _download_thread = threading.Thread(target=_download,
                                            args=(url,))
        _playing_thread = threading.Thread(target=_play,
                                           args=(self._vlc, self._player, url))
        _download_thread.start()
        _playing_thread.start()
