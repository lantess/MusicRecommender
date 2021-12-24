from pygame import mixer
import os
import SoundTransformer as st

_music = mixer.init()

def play(filename):
    _music.music.load(os.path.join(st.WAV_DIR, filename))
    _music.music.play()

def stop():
    _music.music.stop()