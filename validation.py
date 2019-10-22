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
