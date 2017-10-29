import random
import crawler
from twitter_manager import post

USED_LIST = 'used_song_list.txt'


# check is song is already posted before
def is_song_duplicated(track_id):

    with open(USED_LIST, 'r') as f:
        used_songs = [l.strip() for l in f.readlines()]

        if track_id in used_songs:
            return True

    return False


# update the used song list file
def update_used_song_list(track_id):

    with open(USED_LIST, 'a') as f:
        f.write(track_id + '\n')


# return song that contains lyric data
def select_song(track_list):

    while True:
        track = random.choice(track_list)

        # if that song is already used
        if is_song_duplicated(track):
            continue

        song = crawler.get_song(track)

        # if it contains lyric data
        if song:
            update_used_song_list(track)
            return song


# get random verse from naver music
def get_random_verse(min_len=0, max_len=99999):
    track_list = crawler.get_song_list()

    while True:

        song = select_song(track_list)
        lyric = song['lyric']
        title = song['title']
        artist = song['artist']

        # check english/korean ratio of the lyric
        if not crawler.is_lyric_native(lyric, ratio=0.2):
            continue

        # separate lyric to verses
        verses = crawler.separate_verse(lyric, min_len=min_len,
                                        max_len=max_len - len(title) - len(artist) - 10)

        # if no verse that pass filter
        if len(verses) == 0:
            continue

        verse = random.choice(verses)

        # check english/korean ratio of the verse
        if not crawler.is_lyric_native(verse, ratio=0.1):
            continue

        # verse found
        break

    return song['title'], song['artist'], verse


# format song data to tweet
def format_tweet(title, artist, verse):
    tweet = ''
    tweet += verse
    tweet += '\n\n'
    tweet += artist + ' - ' + title

    return tweet


def main():

    tweet_length_limit = 140

    title, artist, verse = get_random_verse(min_len=30, max_len=tweet_length_limit)
    tweet = format_tweet(title, artist, verse)

    post(tweet)

if __name__ == '__main__':
    main()
