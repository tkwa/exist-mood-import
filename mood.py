from collections import namedtuple

# TODO: extend to include custom attributes

"""
An object representing mood and tags for a given day.
date: a `datetime` object
level: mood level on a 1-5 integer scale
comment: daily mood note. Note Exist has a 250 char limit as of 6/2020
tags: a set of strings representing tags for that day
"""
Mood = namedtuple('Mood', ['date', 'level', 'comment', 'tags'])

MoodData = namedtuple('MoodData', ['mood_tags', 'moods'])

def combine(date, moods):
    moods = list(moods)
    new_level = sum(m.level for m in moods) // len(moods)
    tags = set(tag for m in moods for tag in m.tags)
    comment = ' '.join(m.comment for m in moods).strip()
    return Mood(date, new_level, comment, tags)

