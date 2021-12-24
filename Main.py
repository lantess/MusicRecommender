from SoundTransformer import SoundTransformer
from WindowManager import WindowManager as wm
from WindowManager import WindowHandler as wh
import MusicPlayer as player

st = SoundTransformer()

def _update_soundbase(window):
    window.close()
    new_window = wm.getProgressWindow()
    st.update_soundbase(new_window)

def _close_window(window):
    window.close()


def _play_song(window):
    if window['-INPUT-'].get() == '':
        window['-INPUT-'].update(value='Metallica- Mama Said.wav') #Hardkodowane do testów TODO: poprawić
        player.play('Metallica- Mama Said.wav')
    if window['-PLAY-'].get_text() == 'Play':
        window['-PLAY-'].update(text='Pause')
        player.stop()
    else:
        window['-PLAY-'].update(text='Play')


def _recommend_song(window):
    print('DEBUG: song recommendated.')


def create_initial_window():
    if st.has_new_files():
        new_song_window_handler = wh(wm.getNewSongsWindow())
        new_song_window_handler.addAction('Yes', _update_soundbase)
        new_song_window_handler.addAction('No', _close_window)
        new_song_window_handler.handle()

    main_windows_handler = wh(wm.getMainWindow())
    main_windows_handler.addAction('-PLAY-', _play_song)
    main_windows_handler.addAction('Recommend', _recommend_song)
    while main_windows_handler.handle():
        pass

def main():
    create_initial_window()


if __name__ == "__main__":
    main()