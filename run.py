import random
import music
import time
import tweet
import validation
import issue
import config

# check is song is already posted before
def duplicated(track_id):

    used_track_ids = [
        t.strip()
        for t in issue.get_issue(config.GITHUB_REPO_URL, config.GITHUB_ISSUE_ID).split()
    ]

    if track_id in used_track_ids:
        return True

    return False


# update the used song list
def update_used_song_list(track_id):
    issue.update_issue(config.GITHUB_REPO_URL, config.GITHUB_ISSUE_ID, str(track_id))


# separate verses from lyric
# if min_len is given, only verses longer than min_len is returned
def separate_verses(lyric, min_len=0, max_len=99999):
    splited = lyric.split("\n\n")

    splited = [s for s in splited if min_len <= len(s) <= max_len]

    return splited


# select a verse from a song
def select_verse(lyric, title, artist, min_len, max_len):

    # separate lyric to verses
    verses = separate_verses(
        lyric,
        min_len=min_len,
        max_len=max_len - len(title) - len(artist) - 10,
    )

    # if no verse that pass filter
    if not verses:
        raise ValueError

    verse = random.choice(verses)

    # check english/korean ratio of the lyric
    if not validation.is_lyric_native(lyric, ratio=0.2):
        raise ValueError

    # check english/korean ratio of the verse
    if not validation.is_lyric_native(verse, ratio=0.1):
        raise ValueError

    # check special chracters in verse
    if not validation.is_lyric_pure(verse):
        raise ValueError

    return verse


# get random verse from naver music
def get_random_verse(min_len=0, max_len=99999):
    track_infos = music.get_song_list()

    while True:
        track = random.choice(track_infos)

        # if this song had been already used
        if duplicated(track["track_id"]):
            continue

        lyric = music.get_lyric(track["track_id"])
        try:
            verse = select_verse(lyric, track["title"], track["artist"], min_len, max_len)
        except Exception as e:
            # print(e)
            continue

        # verse found
        update_used_song_list(track["track_id"])
        break

    return track["title"], track["artist"], verse


# format song data for tweet
def format_tweet(title, artist, verse):
    tweet = ""
    tweet += verse
    tweet += "\n\n"
    tweet += artist + " - " + title

    return tweet


def main():
    title, artist, verse = get_random_verse(
        min_len=30, max_len=config.TWEET_LENGTH_LIMIT
    )
    body = format_tweet(title, artist, verse)

    if config.DEBUG:
        print(body)
    else:
        tweet.post(body)


if __name__ == "__main__":
    main()
