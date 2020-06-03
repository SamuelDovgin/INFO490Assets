#
# for some of the lines that are commented out
# you can experiment
# but the tests assume they are NOT used
#
import re


def read_data(filename):
    with open(filename, 'r') as fd:
        return fd.read()


def split_chapters(data):
    pattern = r'^CHAPTER\s[A-Z\s]+\.?$'
    # pattern = r'CHAPTER\s[A-Z\s]+'
    regex = re.compile(pattern, re.M)
    return regex.split(data)


def tokenize(data):
    # how to treat: you-did—I-didn't
    pattern = r"[A-Za-z0-9']+-?[A-Za-z0-9']+"
    # pattern = r"[A-Za-z0-9']+"
    regex = re.compile(pattern)
    tokens = regex.findall(data)

    # remove leading and trailing single quotes
    t = [t.strip("'") for t in tokens]
    return " ".join(t)


def clean_chapter(chapter):
    c = chapter.replace("\n", " ")
    return c.strip()


def clean_chapters(chapters):
    out = []
    for i, c in enumerate(chapters):
        c = clean_chapter(c)
        if len(c) > 0:
            out.append(tokenize(c))
    return out


def split_into_tokens(data, normalize=True):
    tokens = data.split()
    if normalize:
        tokens = [t.lower() for t in tokens]
        #tokens = [t.lower() for t in tokens if len(t) > 2]
    return tokens
