import vlc
import pafy
import threading
from WindowManager import WindowManager as wm, WindowHandler
import time
from PySimpleGUI import Window
import os
import Variables as var
from Variables import SQLQuery as query
import ffmpeg
import Database as db
import locale

out_extension = 'wav'


def _duration_to_seconds(duration: str) -> int:
    h = int(duration[:duration.find(':')])
    m = int(duration[duration.find(':') + 1:duration.rfind(':')])
    s = int(duration[duration.rfind(':') + 1:])
    return h * 60 * 60 + m * 60 + s


def _convert_to_wav_and_move():
    for file in os.listdir(var.NEW_WAV_DIR):
        in_path = os.path.join(var.NEW_WAV_DIR, file)
        out_path = os.path.join(var.WAV_DIR, file[:file.rfind('.')] + '.wav')
        stream = ffmpeg.input(in_path)
        stream = ffmpeg.output(stream, out_path)
        ffmpeg.run(stream, quiet=True)
        os.remove(in_path)


def _download(url: str):
    time.sleep(1)  # cause sleep is the best concurrency friend, it helps making everything right
    youtube_video = pafy.new(url)
    audio_stream = youtube_video.getbestaudio()
    audio_stream.download(filepath='data/wav.new/'
                                   + audio_stream.title
                                   + '.' + audio_stream.extension,
                          quiet=True)
    _convert_to_wav_and_move()
    from Main import st as st
    st.update_soundbase()
    print('Soundbase updated after download.')


class MusicPlayer:
    def __init__(self):
        self._vlc = vlc.Instance()
        self._player = self._vlc.media_player_new()
        self._download_thread = None
        self._playing_thread = None
        self._progress_thread = None
        self._duration = -1
        self._window = None
        self._isLiked = 0

    def _add_to_log(self, filename: str, time_started, is_skipped: bool, rate):
        #TODO: kurwa no możesz się ogarnąć
        #w bazie nie ma przecież jeszcze tej piosenki, trzeba kurwa ją dodać no ja jebę
        #kurwa kolejny duży task z dupy no ile można kurwa, chuj mi w dupę normalnie
        id = db.execute_query(query.GET_SONG_ID_BY_NAME, params=(filename,))
        print(id)
        timestamp = time.time()
        listening_time = time.time()-time_started
        skipped = 1 if is_skipped else 0
        language_code = locale.getdefaultlocale()
        db.execute_query(query.ADD_LISTEN_LOG, params=(id, timestamp, rate, listening_time, skipped, language_code))

    def _youtube_play(self, url: str):
        youtube_video = pafy.new(url)
        self._duration = _duration_to_seconds(youtube_video.duration)
        audio_stream = youtube_video.getbestaudio()
        media = self._vlc.media_new(audio_stream.url)
        media.get_mrl()
        self._player.set_media(media)
        self._window['-TITLE-'].update(value='Now playing: '+youtube_video.title)
        self._player.audio_set_volume(50)
        self._player.play()

    def _play(self, url: str):
        if 'youtube.com' in url:
            self._download_thread = threading.Thread(target=_download,
                                                     args=(url,))
            self._playing_thread = threading.Thread(target=self._youtube_play,
                                                    args=(url,))
        else:
            pass #TODO: nowe odsłuchy
        self._playing_thread.start()
        self._download_thread.start()

    def _return_to_main_window(self, window: Window, values: dict):
        window.close()
        self._player.stop()
        import Main
        Main.create_initial_window()

    def _on_like_action(self, window: Window, values: dict):
        self._isLiked = 1

    def _on_dislike_action(self, window: Window, values: dict):
        self._isLiked = -1

    def _on_pause_play_action(self, window: Window, values: dict):
        key = window['-PLAY-PAUSE-'].get_text()
        if key == 'Pause':
            self._player.pause()
            window['-PLAY-PAUSE-'].update(text='Play')
        else:
            self._player.play()
            window['-PLAY-PAUSE-'].update(text='Pause')

    def _volume_change_action(self, window: Window, values: dict):
        self._player.audio_set_volume(int(values['-VOL-']))

    def _next_song(self, window: Window, values: dict):
        label = self._window['-TITLE-'].get().replace('Now playing: ', '')
        self._add_to_log(label, time.time(), True, self._isLiked)
        pass #TODO: rekomendacja

    def _open_player_window(self) -> WindowHandler:
        self._window = wm.getPlayerWindow()
        self._window.finalize()
        wh = WindowHandler(self._window)
        wh.addCloseAction(self._return_to_main_window)
        wh.addAction('-LIKE-', self._on_like_action)
        wh.addAction('-DISLIKE-', self._on_dislike_action)
        wh.addAction('-PLAY-PAUSE-', self._on_pause_play_action)
        wh.addAction('-VOL-', self._volume_change_action)
        wh.addAction('-NEXT-', self._next_song)
        return wh

    def play(self, url: str):
        self._play(url)
        wh = self._open_player_window()
        while wh.handle():
            pass
