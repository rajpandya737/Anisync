import sqlite3
from data_processing import convertor
import time

def main():
    pass

def set_song_to_none():
    update_query = """
        UPDATE anime
        SET anime_song = 'No song found'
        WHERE osu_link = 'Does not exist';
    """
    c.execute(update_query)


def add_songs_by_user(user, start, stop):
    for i in range(8):
        user = "NuxTaku"
        start = 170 + 20*i
        end = 200 + 20*i
        print(start, end, "start")
        anime_list = convertor(user, start, end)
        add_anime_by_list(anime_list)
        time.sleep(30)
        print(start, end, "end")

conn = sqlite3.connect("anime_list.sqlite")
c = conn.cursor()


def no_map(anime_name, anime_song, anime_img):
    remove_anime(anime_name)
    insert_anime(anime_name, anime_song, anime_img, "Does not exist")


def insert_and_delete(anime_name, anime_song, anime_img, osu_link):
    remove_anime(anime_name)
    insert_anime(anime_name, anime_song, anime_img, osu_link)


# c.execute(
#     """CREATE TABLE anime (
#     anime_name DATATYPE,
#     anime_song DATATYPE,
#     anime_img DATATYPE,
#     osu_link DATATYPE
# )
# """
# )


def delete_rows_by_id(start_row, end_row):
    c.execute("DELETE FROM anime WHERE rowid BETWEEN ? AND ?", (start_row, end_row))
    conn.commit()


def remove_anime(anime_name_to_remove):
    c.execute("DELETE FROM anime WHERE anime_name = ?", (anime_name_to_remove,))
    conn.commit()


def insert_anime(anime_name, anime_song, anime_img, osu_link):
    c.execute(
        "INSERT INTO anime VALUES (?, ?, ?, ?)",
        (anime_name, anime_song, anime_img, osu_link),
    )
    conn.commit()


def add_anime_by_list(anime_list):
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


main()
conn.commit()
conn.close()
