import pafy
import vlc
import time

#snd = urlopen('http://www.youtube.com/watch?v=BaW_jenozKc').read()

url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

video = pafy.new(url)

print(video.duration)
print(video.title, video.author)
for s in video.audiostreams:
    print(s)

stream = video.getbestaudio()
print(stream.url)

filename = stream.download(filepath='../data/wav.new/'+'.'+video.title+stream.extension)


vlcIns = vlc.Instance()
player = vlcIns.media_player_new()

media = vlcIns.media_new(stream.url)
media.get_mrl()
player.set_media(media)
player.play()

time.sleep(10)