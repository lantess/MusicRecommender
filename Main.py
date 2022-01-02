from SoundTransformer import SoundTransformer
from WindowManager import WindowManager as wm
from WindowManager import WindowHandler as wh
from MusicPlayer import MusicPlayer
import PySimpleGUI as sg

st = SoundTransformer()
player = MusicPlayer()


def _update_soundbase(window: sg.Window, values: dict):
    window.close()
    new_window = wm.getProgressWindow()
    st.update_soundbase(new_window)


def _close_window(window: sg.Window, values: dict):
    window.close()


def _play_song(window: sg.Window, values: dict):
    url = window['-INPUT-'].get()
    window.close()
    if len(url) == 0:  # TODO: Komunikat o błędzie
        player.play('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')  # TODO: w sumie wszystko xD
    else:
        player.play(url)


def _random_song(window: sg.Window, values: dict):
    print('DEBUG: song recommendated.', values)


def create_initial_window():
    if st.has_new_files():
        new_song_window_handler = wh(wm.getNewSongsWindow())
        new_song_window_handler.addAction('Yes', _update_soundbase)
        new_song_window_handler.addAction('No', _close_window)
        new_song_window_handler.handle()

    main_windows_handler = wh(wm.getMainWindow())
    main_windows_handler.addAction('Random', _random_song)
    main_windows_handler.addAction('Recommend', _play_song)
    while main_windows_handler.handle():
        pass


def main():
    create_initial_window()


if __name__ == "__main__":
    main()
