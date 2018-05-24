from bs4 import BeautifulSoup, NavigableString
import collections
import json
import urllib
import time

def get_song_titles(artist):
  formatted_artist = artist.replace(" ", "").lower()
  url = "https://www.azlyrics.com/m/%s.html" % formatted_artist
  try:
    response = urllib.request.urlopen(url)
    page_text = BeautifulSoup(response.read(), "lxml")
    all_links = page_text.find_all("a")
    song_titles = []
    for link in all_links:
      link_target = link.get("href")
      if link_target is not None and formatted_artist in link_target:
        song_titles.append(link_target.split("/")[-1].split(".")[0])
    return song_titles
  except urllib.error.HTTPError as e:
    print("Couldn't find songs for artist: %s" % artist)
    print(e)

def get_song_lyrics(artist, song_titles=None):
  formatted_artist = artist.replace(" ", "").lower()
  song_lyrics = {}
  if not song_titles:
    song_titles = get_song_titles(artist)
  for song in song_titles:
    url = "https://www.azlyrics.com/lyrics/%s/%s.html" % (formatted_artist, song)
    print("Trying url: %s" % url)
    try:
      response = urllib.request.urlopen(url)
      page_text = BeautifulSoup(response.read(), "lxml")
      song_lyrics[song] = page_text.find("div", attrs={"class": None, "id": None}).getText()
    except urllib.error.HTTPError as e:
      print("Couldn't find song %s by %s." % (song, artist))
      print(e)
    time.sleep(10)
  with open("%s.json" % formatted_artist, "w") as wh:
    json.dump(song_lyrics, wh)

def get_songs_by_album(artist):
  formatted_artist = artist.replace(" ", "").lower()
  url = "https://www.azlyrics.com/m/%s.html" % formatted_artist
  songs_by_album = collections.defaultdict(list)
  try:
    response = urllib.request.urlopen(url)
    page_text = BeautifulSoup(response.read(), "lxml")
    album = page_text.find("div", attrs={"class": "album"})
    formatted_album = "".join(album.getText().split(":")[1:]).replace("\"","")[1:]
    for sibling in album.next_siblings:
      if isinstance(sibling, NavigableString):
        continue
      sibling_class = sibling.get("class")
      if sibling_class is not None and sibling_class[0] == "album":
        formatted_album = "".join(sibling.getText().split(":")[1:]).replace("\"","")[1:]
      link_target = sibling.get("href")
      if link_target is not None and formatted_artist in link_target:
        songs_by_album[formatted_album].append(link_target.split("/")[-1].split(".")[0])
  except urllib.error.HTTPError as e:
    print("Couldn't find artist: %s" % artist)
    print(e)
  with open("%s_songs_by_album.json" % formatted_artist, "w") as wh:
    json.dump(songs_by_album, wh, indent=4, sort_keys=True)

get_songs_by_album("Modest Mouse")
# get_song_lyrics("Modest Mouse")
