import youtube_dl
import os
import pygame.mixer as mixer
import time
from urllib.request import urlopen

SAVE_PATH = '../data/wav.new'

def download_from_youtube(url: str) -> []:
    ydl_opts = {
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'outtmpl': SAVE_PATH + '/%(title)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

download_from_youtube('http://www.youtube.com/watch?v=BaW_jenozKc')

for wav in os.listdir('../data/wav.new'):
    mixer.init()
    mixer.music.load(os.path.join('../data/wav.new', wav))
    mixer.music.play(-1, 0, 0)
    time.sleep(10)
    mixer.music.stop()

