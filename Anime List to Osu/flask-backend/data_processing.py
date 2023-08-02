from ossapi import Ossapi
import re
from mal import Anime, AnimeSearch
import bs4
import requests
from dotenv import load_dotenv
import os
import unicodedata
from urllib.parse import urlparse, parse_qs
import sqlite3

#load_dotenv()
#KEY = os.getenv("KEY")
#PASSWORD = os.getenv("PASSWORD")
ERROR_IMG_URL = 'https://developers.google.com/static/maps/documentation/maps-static/images/error-image-generic.png'

# user = 'MayilArna'
# user = "raj_23"


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


# print(anime_list)


def extract_titles(text):
    pattern = r'"([^"]+)"'
    return re.findall(pattern, text)


def get_google_results(search_term):
    res = requests.get(f"https://www.google.com/search?q={search_term}")
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    linkElements = soup.select(".kCrYT > a")
    # print(linkElements)
    linkToOpen = min(3, len(linkElements))
    to_return = []
    for i in range(linkToOpen):
        to_return.append("https://www.google.com" + linkElements[i].get("href"))
    return extract_anime_id(to_return[0])


def extract_anime_id(url):
    pattern = r"/(\d+)/"
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


def get_anime_type(anime):
    # search = AnimeSearch(anime)
    # Getting ID from google search results instead of using the API is much
    # faster and has to make half as many calls
    try:
        MAL_id = get_google_results(f"{anime} MyAnimeList")
        anime_info = Anime(MAL_id)
    except ValueError:
        search = AnimeSearch(anime)
        anime_info = Anime(search.results[0].mal_id)
    # ops = anime_info.opening_themes
    img = anime_info.image_url
    anime_type = anime_info.type
    # titles = [extract_titles(item) for item in ops], img,
    return img, anime_type


def get_links(input_string):

    pattern = r"url='(https://osu\.ppy\.sh/beatmaps/\d+)'"

    urls_with_link_https = re.findall(pattern, input_string)
    links = []
    # Print the extracted URLs
    for url in urls_with_link_https:
        links.append(url)
    return links


def get_links_by_anime_osuapi(
    api, name: str, n: int = 1, sort_method=None, game_mode=0
):
    return get_links(
        str(api.search_beatmapsets(query=name, sort=sort_method, mode=game_mode))
    )[:2]


def get_first_non_empty(data):
    for item in data:
        if item:
            return item
    return [None]


def get_links_by_anime_google(search_term):
    res = requests.get(f"https://www.google.com/search?q={search_term}")
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    linkElements = soup.select(".kCrYT > a")
    # print(linkElements)
    linkToOpen = min(2, len(linkElements))
    to_return = []
    for i in range(linkToOpen):
        to_return.append("https://www.google.com" + linkElements[i].get("href"))
    # try:
    return (to_return[0])
    # except IndexError:
    #     return None


def remove_japanese(text):
    return list(filter(lambda ele: re.search("[a-zA-Z\s]+", ele) is not None, text))


def remove_blank_entries(lst):
    return [entry.strip() for entry in lst if entry.strip()]


def decode_unicode(lst):
    decoded_list = []
    for entry in lst:
        decoded_entry = entry.encode("ascii", "ignore").decode("utf-8")
        decoded_list.append(decoded_entry)
    return decoded_list


def save_list_to_textfile(lst, filename):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for item in lst:
                file.write(str(item) + "\n")
        print(f"The list has been successfully saved to '{filename}'.")
    except Exception as e:
        print(f"Error occurred while saving the list: {e}")


def extract_osu_link_and_id(link):
    parsed_url = urlparse(link)
    query_params = parse_qs(parsed_url.query)
    return query_params.get("q", [""])[0]


def get_song_from_osu(api, osu_id):
    #title_pattern = r"title='(.*?)'"
    attributes = api.beatmap(beatmap_id=int(osu_id))
    #print(attributes)
    #print(type(attributes))
    #return re.search(title_pattern, attributes).group(1)

# api = Ossapi(KEY, PASSWORD)
# print(api.user("tybug").username)
# print(api.beatmap(1114515).id)
# #print(get_song_from_osu(api, 297204))

def scrape_osu(link):
    result = requests.get(link)
    soup = bs4.BeautifulSoup(result.text, "html.parser")
    title_tag = soup.find("title")
    if title_tag:
        artist_and_title = title_tag.text.strip()
        return artist_and_title.split("·")[0]
    else:
        return "Title Not Found"

def get_id_from_link(link):
    return (link.split("/")[-1])

def convertor(user, s, e):
    conn = sqlite3.connect("anime_list.sqlite")
    c = conn.cursor()
    #api = Ossapi(KEY, PASSWORD)
    anime_list = decode_unicode(remove_blank_entries(mal(user)[s:e]))
    list_info = []
    for anime in anime_list:
        c.execute("SELECT 1 FROM anime WHERE anime_name = ? LIMIT 1", (anime,))
        result = c.fetchone()
        #print(anime)
        if not result:
            #print("Not in database")
            img, anime_type = get_anime_type(anime)
            song = [None]
            if anime_type == "TV":
                # osu_api_search_term = f"{anime} {song[0]}"
                # print(search_term)
                # link = get_links_by_anime(api, search_term, 1)
                google_search_term = f"{anime} Osu Beatmap Anime"
                link = get_links_by_anime_google(google_search_term)
                #print(link)
                #osu_id = get_id_from_link(link)
                #print(osu_id)
                song = scrape_osu(link)


            if anime_type != "TV":
                link = [f"Some {anime_type}'s are not supported yet"]

            if song[0] is None or song[0] == "None":
                link = "Does not exist"
                song = "No song found"
            list_info.append([anime, song, img, link])
        else:
            select_query = """
            SELECT * FROM anime
            WHERE anime_name = ?;
        """
            try:
                # Execute the select query
                c.execute(select_query, (anime,))
                row = c.fetchone()

                if row:
                    # If a row is found, you can access the columns like this
                    db_anime_name, db_anime_song, db_anime_img, db_osu_link = row
                    list_info.append([db_anime_name, db_anime_song, db_anime_img, db_osu_link])
                else:
                    list_info.append([anime, "No song", ERROR_IMG_URL, "Does not exist"])
            except Exception as e:
                list_info.append([anime, "No song", ERROR_IMG_URL, "Does not exist"])
    conn.close()
    # first = list_info[0]
    # return {first[0]: [first[1], first[2], first[3]]}
    return list_info





#_, t = get_anime_type("Gintama")
#print([t])

# anime = "Food Wars"
# google_search_term = f"{anime} Osu Beatmap"
# print((get_links_by_anime_google(google_search_term)))


print(convertor("raj_23", 0, 2)[0][1])


#print((a))


# api = Ossapi(KEY, PASSWORD)
#print(get_song_from_osu(api, 667216))



# if __name__ == "__main__":
#     main()
