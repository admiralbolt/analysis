import collections
import json
import pprint
from operator import itemgetter
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import re

with open("modestmouse.json", "r") as rh:
  song_lyrics = json.load(rh)
with open("modestmouse_songs_by_album.json", "r") as rh:
  songs_by_album = json.load(rh)

well_count = collections.defaultdict(int)

# Pure word counts
for song, lyrics in song_lyrics.items():
  wells = lyrics.lower().count("well")
  well_count[song] = wells

def graph_songs():
  songs = []
  num_wells = []
  for song, well in sorted(well_count.items(), key=itemgetter(1), reverse=True):
    if well == 0:
      continue
    print(song, well)
    songs.append(song)
    num_wells.append(well)


  y_pos = np.arange(len(songs)) * 4
  plt.bar(y_pos, num_wells, align='center', alpha=0.5)
  plt.rc('xtick', labelsize=6)
  plt.xticks(y_pos, songs, rotation='vertical')
  plt.ylabel('Number of "Wells"')
  plt.title('Well...')
  plt.show()

def graph_albums():
  num_wells = []
  albums = [album for album in songs_by_album.keys() if album]
  albums.sort(key=lambda x: int(re.findall(r"\d+", x)[0]))
  for album in albums:
    well = 0
    for song in songs_by_album[album]:
      well += well_count[song]
    num_wells.append(well)

  fig, ax = plt.subplots(figsize=(6.4, 9))
  fig.subplots_adjust(bottom = 0.45)
  fig.subplots_adjust(top = 0.95)
  y_pos = np.arange(len(albums))
  plt.bar(y_pos, num_wells, align='center', alpha=0.5)
  plt.rc('xtick', labelsize=6)
  plt.xticks(y_pos, albums, rotation='vertical', size=8)
  yticks = range(0, 110, 10)
  plt.yticks(yticks, yticks)
  for i, v in enumerate(num_wells):
    ax.text(i - 0.25, v + 3, str(v), color='blue', fontweight='bold')
  plt.ylabel('Number of "Wells"')
  plt.title('Well...')
  plt.show()
