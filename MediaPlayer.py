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

#TODO: jak utwór się skończy odtwarzaj następny od razu
#TODO: hej coś się nie przetwarza do chuja pana
#TODO: trzeba przyśpieszyć rejestrowanie w bazie nowego utworu

def _convert_to_wav_and_move():
    for file in os.listdir(var.NEW_WAV_DIR):
        in_path = os.path.join(var.NEW_WAV_DIR, file)
        out_path = os.path.join(var.WAV_DIR, file[:file.rfind('.')] + '.wav')
        stream = ffmpeg.input(in_path)
        stream = ffmpeg.output(stream, out_path)
        ffmpeg.run(stream, quiet=True)
        os.remove(in_path)


def _download(url: str):
    time.sleep(1)
    youtube_video = pafy.new(url)
    audio_stream = youtube_video.getbestaudio()
    audio_stream.download(filepath='data/wav.new/'
                                   + audio_stream.title
                                   + '.' + audio_stream.extension,
                          quiet=True)
    _convert_to_wav_and_move()
    from Main import st as st
    st.update_soundbase()

class MediaPlayer:
    def __init__(self):
        self._vlc_instance = vlc.Instance()
        self._player = self._vlc_instance.media_player_new()
        self._player.audio_set_volume(var.START_VOLUME)
        self._window = None
        self._wh = None
        self._isLiked = 0
        self._startTime = 0
        self._download_thread = None #TODO: Jutro Adam weź tu wykmiń fajną konstrukcję taką, żeby się te pobierania kolejkowały czy coś, o mam pomysł, możesz sprawdzać listę a potem pobierać xD Fajnie będzie, zobaczysz
        self._playing_thread = None

    def _add_to_log(self, filename: str, time_started, is_skipped: bool, rate):
        id = db.execute_query(query.GET_SONG_ID_BY_NAME, params=(filename+'.wav',))[0][0]
        print(id)
        timestamp = time.time()
        listening_time = timestamp - time_started
        skipped = 1 if is_skipped else 0
        language_code = locale.getdefaultlocale()[0]
        db.execute_query(query.ADD_LISTEN_LOG, params=(id, timestamp, rate, listening_time, skipped, language_code))
        self._isLiked = 0

    def _return_to_main_window(self, window: Window, values: dict):
        window.close()
        self._player.stop()
        self._startTime = -1
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

    def _next_song(self, window: Window, values: dict): #TODO:====================================================
        #TODO: POPRAWIĆ
        label = self._window['-TITLE-'].get().replace('Now playing: ', '')
        self._add_to_log(label, self._startTime, True, self._isLiked)
        #DEBUG TODO: tymczasowe rozwiązanie
        path = db.execute_query(query.GET_RANDOM_SONG)[0][1]
        self._play_local(path)
        pass #TODO: rekomendacja

    def _open_player_window(self):
        self._window = wm.getPlayerWindow()
        self._window.finalize()
        wh = WindowHandler(self._window)
        wh.addCloseAction(self._return_to_main_window)
        wh.addAction('-LIKE-', self._on_like_action)
        wh.addAction('-DISLIKE-', self._on_dislike_action)
        wh.addAction('-PLAY-PAUSE-', self._on_pause_play_action)
        wh.addAction('-VOL-', self._volume_change_action)
        wh.addAction('-NEXT-', self._next_song)
        self._wh = wh

    def _play_local(self, path: str):
        media = self._vlc_instance.media_new(os.path.join(var.WAV_DIR, path))
        self._player.pause()
        self._player.set_media(media)
        self._player.play()
        self._window['-TITLE-'].update(value='Now playing: ' + path.replace('.wav', ''))

    def _play_youtube(self, url: str):
        youtube_video = pafy.new(url)
        audio_stream = youtube_video.getbestaudio()
        media = self._vlc_instance.media_new(audio_stream.url)
        media.get_mrl()
        self._player.set_media(media)
        self._window['-TITLE-'].update(value='Now playing: ' + youtube_video.title)
        self._player.play()

    def _play_next_if_song_ends(self):
        #TODO: Tu narazie jest ścierniko, ale będzie rekomendacja
        if 1000000 > (time.time() - self._startTime) > 5:
            if not self._player.is_playing():
                label = self._window['-TITLE-'].get().replace('Now playing: ', '')
                self._add_to_log(label, self._startTime, False, self._isLiked)
                path = db.execute_query(query.GET_RANDOM_SONG)[0][1]
                self._playing_thread = threading.Thread(target=self._play_local,
                                                        args=(path,))
                self._playing_thread.start()

    def _play(self, song_source: str):
        if song_source.find('http://') != -1 or song_source.find('https://') != -1:
            if 'youtube.com' in song_source:
                self._download_thread = threading.Thread(target=_download,
                                                         args=(song_source,))
                self._playing_thread = threading.Thread(target=self._play_youtube,
                                                        args=(song_source,))
            else:
                pass
            self._download_thread.start()
        else:
            self._playing_thread = threading.Thread(target=self._play_local,
                                                    args=(song_source,))
        self._startTime = time.time()
        self._open_player_window()
        self._playing_thread.start()
        while self._wh.handle():
            self._play_next_if_song_ends()

    def play(self, song_source: str):
        self._play(song_source)

