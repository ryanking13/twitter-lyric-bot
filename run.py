import random
import music
import time
import tweet
import validation

USED_LIST = "used_song_list.txt"
TWEET_LENGTH_LIMIT = 140


# check is song is already posted before
def is_song_duplicated(track_id):

    with open(USED_LIST, "r") as f:
        used_songs = [l.strip() for l in f.readlines()]

        if track_id in used_songs:
            return True

    return False


# update the used song list file
def update_used_song_list(track_id, max_list_size=50):

    with open(USED_LIST, "r") as f:
        lines = f.readlines()

    if len(lines) > max_list_size:
        lines = lines[-max_list_size:]

    with open(USED_LIST, "w") as f:
        f.writelines(lines)
        f.write(track_id + "\n")


# return song that contains lyric data
def select_song(track_list):

    while True:
        track = random.choice(track_list)

        # if that song is already used
        if is_song_duplicated(track):
            continue

        song = music.get_song(track)

        # if it contains lyric data
        if song:
            return song, track


# get random verse from naver music
def get_random_verse(min_len=0, max_len=99999):
    track_list = music.get_song_list()

    while True:
        song, track_id = select_song(track_list)
        lyric = song["lyric"]
        title = song["title"]
        artist = song["artist"]

        # check english/korean ratio of the lyric
        if not validation.is_lyric_native(lyric, ratio=0.2):
            continue

        # separate lyric to verses
        verses = music.separate_verse(
            lyric, min_len=min_len, max_len=max_len - len(title) - len(artist) - 10
        )

        # if no verse that pass filter
        if not verses:
            continue

        verse = random.choice(verses)

        # check english/korean ratio of the verse
        if not validation.is_lyric_native(verse, ratio=0.1):
            continue

        # check special chracters in verse
        if not validation.is_lyric_pure(verse):
            continue

        # verse found
        update_used_song_list(track_id)
        break

    return song["title"], song["artist"], verse


# format song data to tweet
def format_tweet(title, artist, verse):
    tweet = ""
    tweet += verse
    tweet += "\n\n"
    tweet += artist + " - " + title

    return tweet


def run_bot():
    title, artist, verse = get_random_verse(min_len=30, max_len=TWEET_LENGTH_LIMIT)
    body = format_tweet(title, artist, verse)
    tweet.post(body)


def main():
    run_bot()


if __name__ == "__main__":
    main()
