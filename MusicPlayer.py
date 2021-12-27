import vlc
import pafy
import threading
from WindowManager import WindowManager as wm, WindowHandler
import time
from PySimpleGUI import Window

CODE_BAD_LINK = -1


def _duration_to_seconds(duration: str) -> int:
    h = int(duration[:duration.find(':')])
    m = int(duration[duration.find(':') + 1:duration.rfind(':')])
    s = int(duration[duration.rfind(':') + 1:])
    return h * 60 * 60 + m * 60 + s


def _download(url: str):
    time.sleep(1) #cause sleep is the best concurrency friend, it helps making everything right
    youtube_video = pafy.new(url)
    audio_stream = youtube_video.getbestaudio()
    audio_stream.download(filepath='data/wav.new/'
                                   + audio_stream.title
                                   + '.' + audio_stream.extension,
                          quiet=True)
    print('DOWNLOAD COMPLETE.')


def _play(_vlc, _player, url: str):
    youtube_video = pafy.new(url)
    audio_stream = youtube_video.getbestaudio()
    media = _vlc.media_new(audio_stream.url)
    media.get_mrl()
    _player.set_media(media)
    _player.play()
    print('PLAYED.')


class MusicPlayer:
    def __init__(self):
        self._vlc = vlc.Instance()
        self._player = self._vlc.media_player_new()
        self._download_thread = None
        self._playing_thread = None

    def _play(self, url: str):
        if 'youtube.com' not in url:
            return
        self._download_thread = threading.Thread(target=_download,
                                            args=(url,))
        self._playing_thread = threading.Thread(target=_play,
                                           args=(self._vlc, self._player, url))
        self._playing_thread.start()
        self._download_thread.start()

    def _return_to_main_window(self, window: Window):
        window.close()
        self._player.stop()
        import Main
        Main.create_initial_window()

    def _open_player_window(self) -> WindowHandler:
        self._playing_thread.join()
        window = wm.getPlayerWindow()
        window.finalize()
        wh = WindowHandler(window)
        wh.addCloseAction(self._return_to_main_window)
        return wh

    def play(self, url: str):
        self._play(url)
        wh = self._open_player_window()
        while wh.handle():
            pass