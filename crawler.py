import requests
from bs4 import BeautifulSoup
import json

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
)

sess = requests.session()
sess.headers.update({"User-Agent": USER_AGENT})


# parse lyric and other data from naver music lyric page
def parse_data(page):
    soup = BeautifulSoup(page, "html.parser")
    data = {}

    # parse lyric
    lyric_section = soup.find("div", id="lyricText")
    lyric = []

    if not lyric_section:
        return None

    for l in lyric_section:

        if str(l) == "<br/>":
            lyric.append("\n")
        else:
            lyric.append(l)

    data["lyric"] = "".join(lyric)

    # parse title, artist
    for header in soup.find_all("span"):
        header_class = header.get("class")[0]

        # title info
        if header_class == "ico_play":
            data["title"] = header.find("a").get("title")
        # artist info
        if header_class == "artist":
            data["artist"] = header.find("a").get("title")

    return data


# get song using naver music trackID
def get_song(track_id):
    url = "http://music.naver.com/lyric/index.nhn"

    r = sess.get(url=url, params={"trackId": track_id})
    data = parse_data(r.text)
    return data


# separate verses from lyric
# if min_len is given, only verses longer than min_len is returned
def separate_verse(lyric, min_len=0, max_len=99999):
    splited = lyric.split("\n\n")

    splited = [s for s in splited if min_len <= len(s) <= max_len]

    return splited


# check lyric's english ratio
# if english's ratio is over `percentage`, return false
def is_lyric_native(lyric, ratio=0.2):

    # can't use isalpha() because it returns True for korean words
    # alphabets = [a for a in lyric if a.isalpha()]
    alphabets = [
        a
        for a in lyric
        if ord("a") <= ord(a) <= ord("z") or ord("A") <= ord(a) <= ord("Z")
    ]

    lyric_ratio = len(alphabets) / len(lyric)

    if lyric_ratio > ratio:
        return False

    return True


# check words in lyric
def is_lyric_pure(lyric):

    filter_list = ["(", ")"]

    for f in filter_list:
        if f in lyric:
            return False

    return True


# get song trackIDs
def get_song_list(page_range=5):
    url = "http://music.naver.com/listen/newTrack.nhn"

    track_ids = []
    for i in range(1, page_range + 1):
        r = sess.get(url=url, params={"page": str(i)})
        soup = BeautifulSoup(r.text, "html.parser")

        for header in soup.find_all("div"):
            if header.get("class") and header.get("class")[0] == "_tracklist_mytrack":

                data = header.get("artistdata")
                data = data.replace("'", '"')  # change to valid json format

                try:
                    data = json.loads(data)
                # if not valid json, ignore it
                except json.decoder.JSONDecodeError:
                    break

                for d in data:
                    track_id = list(d.keys())[0]
                    track_ids.append(track_id)

                break

    return track_ids
