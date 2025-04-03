import re
import sqlite3

import bs4
import requests
from mal import Anime, AnimeSearch

from config import DB_PATH, TEST_MODE

ERROR_IMG_URL = "https://developers.google.com/static/maps/documentation/streetview/images/error-image-generic.png"


def mal(user: str, status="completed") -> list:
    # Find anime titles from MAL by user name sorted from highest to lowest score
    link = f"https://myanimelist.net/animelist/{user}?status=2&order=4&order2=0"
    if status == "airing":
        link = f"https://myanimelist.net/animelist/{user}?status=1&order=4&order2=0"
    with requests.Session() as session:
        return _extracted_from_mal_(session, link)


def _extracted_from_mal_(session, link):
    response = session.get(link)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    html_list = soup.find("table", attrs={"class": "list-table"})
    source = str(html_list)
    start_sep = ",&quot;anime_title&quot;:&quot;"
    end_sep = "&quot;,&quot;anime_title_eng&quot;:&quot;"
    tmp = source.split(start_sep)
    return [par.split(end_sep)[0] for par in tmp if end_sep in par]


def get_google_results(search_term: str) -> str or None:
    # Returns the first google search results for the search term
    res = requests.get(f"https://www.google.com/search?q={search_term}")
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    linkElements = soup.select(".kCrYT > a")
    linkToOpen = min(2, len(linkElements))
    to_return = [
        "https://www.google.com" + linkElements[i].get("href")
        for i in range(linkToOpen)
    ]
    try:
        return to_return[0]
    except IndexError:
        return None


def extract_anime_id(url: str) -> str or None: # type: ignore
    # Extracts the anime ID from a google link
    try:
        if match := re.search(r"/(\d+)/", url):
            return match[1]
    except Exception:
        return None
    return None


def get_anime_type(anime: str) -> tuple:
    # Getting ID from google search results instead of using the API is faster
    # and has to make half as many calls, but there is a potential for error
    google_result = get_google_results(f"{anime} MyAnimeList")
    try:
        MAL_id = extract_anime_id(google_result)
        anime_info = Anime(MAL_id)
    except ValueError:
        MAL_id = AnimeSearch(anime).results[0].mal_id
        anime_info = Anime(MAL_id)
    finally:
        img = anime_info.image_url
        anime_type = anime_info.type
        return img, anime_type


def scrape_osu(link: str):
    # Returns the artist and title of the song from the osu beatmap link
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        title_tag = soup.find("title")

        if title_tag:
            artist_and_title = title_tag.text.strip()
            return artist_and_title.split("·")[0]
        else:
            return [None]
    except (requests.RequestException, IndexError):
        return [None]


def remove_blank_entries(lst):
    return [entry.strip() for entry in lst if entry.strip()]

def decode_unicode(lst):
    return [
    entry.encode("ascii", "ignore").decode("utf-8") for entry in lst
]

def convert_to_string(input_string):
    return input_string.encode().decode("unicode_escape")


def convertor(user: str, start: int, end: int, status: str = "completed") -> list:
    # Converts the anime list from MAL to a list of lists containing the anime name, song, image, and osu link
    # Initialise Database connection
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    searched = 0
    # Get the user anime list
    try:
        anime_list = decode_unicode(remove_blank_entries(mal(user, status)[start:end]))
    except Exception as e:
        print(e)
        anime_list = []
    list_info = []
    for anime in anime_list:
        # print(anime)
        # Check if anime is already in the database
        c.execute("SELECT 1 FROM anime WHERE anime_name = ? LIMIT 1", (anime,))
        result = c.fetchone()
        if not result and (TEST_MODE is True or searched < 0):
            # If not in database get the anime type and image
            searched += 1
            img, anime_type = get_anime_type(anime)
            song = [None]
            # Filter any anime that aren't TV
            if anime_type == "TV":
                # If they are TV, search on google for osu maps related to them
                google_search_term = f"{anime} Osu Beatmap Anime"
                link = str(get_google_results(google_search_term))
                # Make sure they are osu maps and not discussions or other links
                if link is None:
                    song = "No song found"
                    link = "Does not exist"
                elif (
                    link.startswith(
                        "https://www.google.com/url?q=https://osu.ppy.sh/beatmapsets/"
                    )
                    and "discussion" not in link
                ):
                    song = scrape_osu(link)
                else:
                    link = "No song found"
                    song = "No song found"
            else:
                link = "Does not exist"
                song = "No song found"

            if song[0] is None or song[0] == "None":
                link = "Does not exist"
                song = "No song found"
            anime = convert_to_string(anime)
            list_info.append([anime, song, img, link])
        else:
            # If anime is in database, get all its information and append to the list
            select_query = """
            SELECT * FROM anime
            WHERE anime_name = ?;
        """
            try:
                # Execute the select query
                c.execute(select_query, (anime,))
                if row := c.fetchone():
                    # If a row is found, you can access the columns like this
                    db_anime_name, db_anime_song, db_anime_img, db_osu_link = row
                    db_anime_name = convert_to_string(db_anime_name)
                    list_info.append(
                        [db_anime_name, db_anime_song, db_anime_img, db_osu_link]
                    )
            except Exception:
                print("error")
                # list_info.append([anime, "No song", ERROR_IMG_URL, "Does not exist"])
    conn.close()
    return list_info
