import sqlite3
import time
from mal import AnimeSearch
from data_processing import convertor

 
def main():
    #add_user_to_db("Stark700", 0)
    update_anime_names_unicode(0, 1490)
    pass

def add_user_to_db(user: str, start: int):
    for i in range(6):
        end = start + 20
        print(start, end, "start")
        anime_list = convertor(user, start, end)
        add_anime_by_list(anime_list)
        time.sleep(30)
        print(start, end, "end")
        start = end

def convert_unicode_to_string(unicode_str: str) -> str:
    converted_chars = []
    for char in unicode_str:
        if ord(char) > 127:  # Characters outside ASCII range
            converted_chars.append("\\u{:04X}".format(ord(char)).lower())
        else:
            converted_chars.append(char)
    return "".join(converted_chars)



def update_anime_names_unicode(start: int, end: int):
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
                (new_name, anime_song, anime_img, osu_link,)
            )
            conn.commit()

def set_song_to_none():
    update_query = """
        UPDATE anime
        SET anime_song = 'No song found'
        WHERE osu_link = 'Does not exist';
    """
    c.execute(update_query)


conn = sqlite3.connect("database/translated_anime_list.sqlite")
c = conn.cursor()


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
    c.execute("DELETE FROM anime WHERE anime_name = ?", (anime_name_to_remove,))
    conn.commit()


def insert_anime(anime_name: str, anime_song: str, anime_img: str, osu_link: str):
    c.execute(
        "INSERT INTO anime VALUES (?, ?, ?, ?)",
        (anime_name, anime_song, anime_img, osu_link),
    )
    conn.commit()


def add_anime_by_list(anime_list: list):
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
    query = "SELECT rowid, anime_name FROM anime"
    c.execute(query)
    anime_data = c.fetchall()

    return [(row[0], row[1]) for row in anime_data]


def update_anime_name(row_id: int, name: str):
    query = "UPDATE anime SET anime_name = ? WHERE rowid = ?"
    c.execute(query, (name, row_id))


get_japanese_name = lambda s: AnimeSearch(s).results[0].title


def get_japanese_names(english_names: str):
    japanese_names = []
    for name in english_names:
        japanese_name = get_japanese_name(name)
        japanese_names.append(japanese_name)
        print(japanese_name)
    return japanese_names


main()
conn.commit()
conn.close()
