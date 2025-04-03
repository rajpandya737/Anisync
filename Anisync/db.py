# This file contains all the functions that interact with the database,
# is not used in the actual program, but mainly used to add additional anime to the database

import sqlite3
import time

from mal import Anime, AnimeSearch

from config import DB_PATH, TEST_MODE
from data_processing import convertor

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()


def main():
    # Run the commands here while testing
    if not TEST_MODE:
        print("Not running in test mode")
        return
    add_user_to_db("test_account_737", 0, "airing")


def add_user_to_db(user: str, start: int, status: str = "airing"):
    # Gets the users list and adds anime to the database if its not already in it
    for _ in range(6):
        end = start + 5
        print(start, end, "start")
        anime_list = convertor(user, start, end, status)
        print(anime_list)
        add_anime_by_list(anime_list)
        print(start, end, "end")
        time.sleep(20)
        start = end


def convert_unicode_to_string(unicode_str: str) -> str:
    # Helper functions to determine if a string is in unicode
    converted_chars = []
    for char in unicode_str:
        if ord(char) > 127:  # Characters outside ASCII range
            converted_chars.append("\\u{:04X}".format(ord(char)).lower())
        else:
            converted_chars.append(char)
    return "".join(converted_chars)


def update_anime_names_unicode(start: int, end: int):
    # This was to fix a bug where some anime names were in unicode and some were not
    # The fix is to have 2 versions of the same anime, one in unicode and one not
    c.execute("SELECT * FROM anime")
    rows = c.fetchall()
    for row in rows[start:end]:
        old_name, anime_song, anime_img, osu_link = row[0], row[1], row[2], row[3]
        new_name = convert_unicode_to_string(old_name)
        c.execute("SELECT COUNT(*) FROM anime WHERE anime_name = ?", (new_name,))
        count = c.fetchone()[0]
        if new_name != old_name and count == 0:
            print(new_name)
            c.execute(
                "INSERT INTO anime (anime_name, anime_song, anime_img, osu_link) VALUES (?, ?, ?, ?)",
                (
                    new_name,
                    anime_song,
                    anime_img,
                    osu_link,
                ),
            )
            conn.commit()


def osu_link_dne():
    # While adding entries to the database,
    # I changed the osu link depending on if
    # the song was found or not and if it was not a TV anime
    # This just converted everything to a uniform format
    update_query = """
        UPDATE anime
        SET osu_link = 'Does not exist'
        WHERE osu_link = 'Not Supported Yet' 
        OR osu_link = 'No song found';
    """
    c.execute(update_query)


def song_link_not_found():
    # While adding entries to the database, sometimes no link
    # would be found but a song would still have a title, this is to fix that issue
    update_query = """
        UPDATE anime
        SET anime_song = 'No song found'
        WHERE osu_link = 'Does not exist';
    """
    c.execute(update_query)


def no_map(anime_name: str, anime_song: str, anime_img: str):
    remove_anime(anime_name)
    insert_anime(anime_name, anime_song, anime_img, "Does not exist")


def insert_and_delete(anime_name: str, anime_song: str, anime_img: str, osu_link: str):
    remove_anime(anime_name)
    insert_anime(anime_name, anime_song, anime_img, osu_link)


def update_anime_links_and_songs(old_word: str, new_link: str, new_song: str):
    # Fetch anime records containing the old_word in the osu_link
    c.execute("SELECT * FROM anime")
    anime_records = c.fetchall()

    # Update the link and song for each matching record
    for record in anime_records:
        anime_name, anime_song, anime_img, osu_link = record

        if old_word in osu_link:
            updated_osu_link = new_link
            updated_anime_song = new_song

            # Execute the UPDATE query
            c.execute(
                "UPDATE anime SET osu_link = ?, anime_song = ? WHERE anime_name = ?",
                (updated_osu_link, updated_anime_song, anime_name),
            )

    conn.commit()


def create_table():
    c.execute(
        """CREATE TABLE anime (
        anime_name DATATYPE,
        anime_song DATATYPE,
        anime_img DATATYPE,
        osu_link DATATYPE
    )
    """
    )


def delete_rows_by_id(start_row: int, end_row: int):
    c.execute("DELETE FROM anime WHERE rowid BETWEEN ? AND ?", (start_row, end_row))
    conn.commit()


def remove_anime(anime_name_to_remove: str):
    # Removes anime from the database based on name
    c.execute("DELETE FROM anime WHERE anime_name = ?", (anime_name_to_remove,))
    conn.commit()


def insert_anime(anime_name: str, anime_song: str, anime_img: str, osu_link: str):
    # Inserts anime into the database
    c.execute(
        "INSERT INTO anime VALUES (?, ?, ?, ?)",
        (anime_name, anime_song, anime_img, osu_link),
    )
    conn.commit()


def add_anime_by_list(anime_list: list):
    # Adds anime to the database by a list of tuples
    for anime in anime_list:
        anime_name = anime[0]  # Extract the anime_name from the tuple
        c.execute("SELECT COUNT(*) FROM anime WHERE anime_name = ?", (anime_name,))
        if c.fetchone()[0] == 0:  # Check if the anime_name does not exist
            c.execute(
                "INSERT INTO anime (anime_name, anime_song, anime_img, osu_link) VALUES (?, ?, ?, ?)",
                anime,
            )
            print(anime)
    conn.commit()


def get_anime_names():
    # gets all the anime names from the database
    query = "SELECT rowid, anime_name FROM anime"
    c.execute(query)
    anime_data = c.fetchall()

    return [(row[0], row[1]) for row in anime_data]


def update_anime_name(row_id: int, name: str):
    # changes the anime name depending on the row id
    query = """
            UPDATE anime 
            SET anime_name = ? 
            WHERE rowid = ?
            """
    c.execute(query, (name, row_id))


def get_japanese_name(s):
    return AnimeSearch(s).results[0].title


def get_japanese_names(english_names: str):
    # Old helper function to get the japanese names of the anime
    japanese_names = []
    for name in english_names:
        japanese_name = get_japanese_name(name)
        japanese_names.append(japanese_name)
        print(japanese_name)
    return japanese_names


def change_image():
    # This was to solve a bug that was present in the database,
    # many enteries had the same image instead of the actual
    # image they should have, this was to fix it
    query = """SELECT anime_name 
    FROM anime 
    WHERE anime_img = 'https://cdn.myanimelist.net/images/anime/1792/91081.jpg'
    """
    c.execute(query)
    anime_data = c.fetchall()
    query = """UPDATE anime 
                   SET anime_img = ? 
                   WHERE anime_img = 'https://cdn.myanimelist.net/images/anime/1792/91081.jpg' 
                   AND anime_name = ?"""
    for i, anime in enumerate(anime_data):
        if i % 10 == 0 and i != 0:
            time.sleep(10)
        time.sleep(1)
        anime = anime[0]
        MAL_id = AnimeSearch(anime).results[0].mal_id
        anime_info = Anime(MAL_id)
        img = anime_info.image_url
        print(anime, img)
        c.execute(
            query,
            (
                img,
                anime,
            ),
        )
        conn.commit()


main()
conn.commit()
conn.close()
