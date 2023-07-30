from ossapi import Ossapi
import re
from mal import *
import bs4
import requests
from dotenv import load_dotenv
import os

load_dotenv()
KEY = os.getenv("KEY")
PASSWORD = os.getenv("PASSWORD")

# user = 'MayilArna'
user = "raj_23"


def mal(user):
    link = f"https://myanimelist.net/animelist/{user}?status=2&order=4&order2=0"
    url = requests.get(link)
    url.raise_for_status
    soup = bs4.BeautifulSoup(url.text, "html.parser")
    html_list = soup.find("table", attrs={"class": "list-table"})
    source = str(html_list)
    start_sep = "&quot;,&quot;anime_title_eng&quot;:&quot;"
    end_sep = "&quot;,&quot;anime_num_episodes&quot"
    results = []
    tmp = source.split(start_sep)
    for par in tmp:
        if end_sep in par:
            results.append(par.split(end_sep)[0])

    return results


anime_list = mal(user)[10:15]
# print(anime_list)


def extract_titles(text):
    pattern = r'"([^"]+)"'
    return re.findall(pattern, text)

def get_opening(anime):
    search = AnimeSearch(anime)
    ops = Anime(search.results[0].mal_id).opening_themes
    return [extract_titles(item) for item in ops]


def get_openings(anime_list):
    openings = []
    for anime in anime_list:
        openings.append(get_opening(anime))
    return openings


def get_links(input_string):

    pattern = r"url='(https://osu\.ppy\.sh/beatmaps/\d+)'"

    urls_with_link_https = re.findall(pattern, input_string)
    links = []
    # Print the extracted URLs
    for url in urls_with_link_https:
        links.append(url)
    return links


def get_links_by_anime(api, name: str, n: int = 1, sort_method=None, game_mode=0):
    return (get_links(str(api.search_beatmapsets(query=name, sort=sort_method, mode=game_mode)))[:2])

def get_first_non_empty(data):
    for item in data:
        if item:
            return item
    return [None]

def remove_japanese_in_brackets(text):
    non_ascii_in_brackets_pattern = r'\(([^)]*[\u0080-\uFFFF]+[^)]*)\)'
    cleaned_text = re.sub(non_ascii_in_brackets_pattern, '', text)
    return cleaned_text

api = Ossapi(KEY, PASSWORD)
for anime in anime_list:
    song = remove_japanese_in_brackets(get_first_non_empty(get_opening(anime))[0])
    link = get_links_by_anime(api, song, 1)
    print('Anime:', anime, 'Song:', song, "Link:", link)

