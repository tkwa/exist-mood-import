import json
import re
import sys
from mood import Mood
from datetime import datetime


def date_of_title(title):
    title = re.sub(r"st,|nd,|rd,|th,", r",", title)
    # parse in format "March 1, 2020"
    date = datetime.strptime(title, "%B %d, %Y")
    return date


def make_tag_name(s):
    # Keep only alphanumerics and underscores; convert space to underscore
    s = re.sub(r'\s+', '_', s, 0)
    return re.sub(r'[\W]+', '', s, 0)


def mood_from_page(page, date):
    """
    Constructs a mood object from a Roam page.
    TODO Required format described in `roam.md`.

    :param page: A Roam date page, as JSON object
    :param date: The date represented
    :return: A Mood object for that day. Fields not specified are None.
    """
    print("Importing page", page["title"], ": ", end='')

    level = comment = None
    tags = set()

    if "children" not in page:
        return None

    # Look for all "tags::" blocks at top-level
    for block in page["children"]:
        string = block["string"]
        if string.startswith("tags::"):
            # Add all space-separated words in the string, but not "tags::" itself
            tags |= set([m.group(1) for m in re.finditer(r"#?(\w+)", string)][1:])

            # Add all "attr::" children of the block as tags
            try:
                for child in block["children"]:
                    match = re.fullmatch(r"(\w+)::\s*(.*)", child["string"])  # match at start of string
                    if not match: continue

                    tag, rest = match.group(1, 2)
                    if tag == "mood":
                        try:
                            level = int(re.search("\d+", rest).group(0))
                        except:
                            print(f"Failed to parse mood {rest}")
                    elif tag == "note" or tag == "comment":
                        comment = rest.strip()
                        # TODO support note as child of "note" block
                    else:
                        tags.add(tag)
            except KeyError: pass

    ret = Mood(date, level, comment, tags)
    print(ret)
    return ret


def import_json(json_file_name, start_date=datetime(2020, 5, 29)):
    """
    Imports from a JSON-format Roam export.
    Roam JSON schema here:
    https://roamresearch.com/#/app/help/page/RxZF78p60

    :param json_file_name: File name to import
    :return: list of Mood objects
    """
    with open(json_file_name, encoding="utf8") as jsonfile:
        pages = json.load(jsonfile)

    all_moods = []
    for page in pages:
        try:
            date = date_of_title(page["title"])
            if date >= start_date:
                mood = mood_from_page(page, date)
                if mood is not None:
                    all_moods.append(mood)
        except ValueError:
            pass
    return all_moods