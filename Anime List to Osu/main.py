from ossapi import Ossapi
import local_config
import re
from mal import *
import bs4
import requests
from dotenv import load_dotenv
import os

load_dotenv()
KEY = os.getenv("client_id")
PASSWORD = os.getenv("client_secret")

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

