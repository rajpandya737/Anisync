# Anisync - Convert your MAL to Osu maps!

## Description

Anisync is a web application that takes a MyAnimeList (MAL) username as input and returns a list of songs from the popular game Osu! that appear on the user's anime list. The app has previously utilized the Osu! API, unofficial MyAnimeList API, and Beautiful Soup for data gathering. This website uses regular HTML, CSS, and Javascript, and Jinja to display the content. The back end uses Flask with an SQLite3 database for faster processing and the full website is hosted on a Digital Ocean server (droplet).

## How to run the program

Currently, a website for this program is in developing with the latest version being avaliable at: https://anisync.live

The program can also be run locally by following these steps. Please ensure you have pip installed on your machine. If you do not, please follow the instructions [here](https://pip.pypa.io/en/stable/installing/).

1. Clone this repository to your local machine:

```bash
git clone https://github.com/RajPandya737/Anisync.git
```

2. Change to the project directory:

```bash
cd Anisync
```

3. The project utilizes many libraries. Ensure you have all of them downloaded by running

```bash
pip install -r requirements.txt
```

4. Run the program, please read the usage part of this file before continuing:

```bash
python Anisync/app.py
```

## Usage

On the website, simply type in your MAL username into the search bar and click submit. The program will then take a few seconds to process the data and return a list of beatmaps that appear on your anime list. The beatmaps are sorted by the rating you gave on your list, and the list is limited to 300 beatmaps. If you have typed in your username correctly and no maps appear, it is likely due to the theme you have enabled on your anime profile, please disable it and try again.

If you are running it locally, make your way to http://localhost:8000 and follow the same steps as above.

## Project Structure
The project consists of the following files inside of the Anisync Folder folder:

1. `app.py`: The main Python script.
2. `config.py`: Contains all constants used in the program.
3. `data_processing.py`: Stores all data retrival functions.
4. `db.py`: Runs any database related functions, used to add data to the database.
5. `static/css`: Contains CSS for each of the respective HTML files. The CSS is minified.
6. `static/images`: Contains all images used in the project.
7. `static/js/about.js`: Gives FAQ button functionality on about route.
8. `static/js/index.js`: Corrects anime name mistakes due to the data_processing.py script on view-maps route.
9. `static/js/scroll.js`: Sticky header functionality on view-maps route.
10. `templates`: Contains all HTML files used in the project.
11. `translated_anime_list.sqlite`: SQLite3 database that stores all anime data.
12. `wsgi.py`: Used for deployment on Digital Ocean.

## Credits

- **MyAnimeList API**: Currently used to get the anime image. [Github and Documentation](https://github.com/darenliang/mal-api)
- **Osu! API**: While I do not use this in the current state of the project, I initially did to aid in prototyping. [Github and Documentation](https://github.com/circleguard/ossapi)
- **MAL Accounts Used for Testing and Data Gathering**:
  - Personal Account:
    - [raj_23](https://myanimelist.net/profile/raj_23)
  - Friend Accounts:
    - [04Ace](https://myanimelist.net/profile/04Ace)
    - [MayilArna](https://myanimelist.net/profile/MayilArna)
    - [Kyoko_52](https://myanimelist.net/profile/Kyoko_52)
    - [cantstudy](https://myanimelist.net/profile/cantstudy)
  - Additional Accounts:
    - [NuxTaku](https://myanimelist.net/profile/NuxTaku)
    - [KingAbsalon21](https://myanimelist.net/profile/KingAbsalon21)
    - [ashuulinksu](https://myanimelist.net/profile/ashuulinksu)
    - [Joshhhp](https://myanimelist.net/profile/Joshhhp)
- **Netflix**: Much of the UI is inspired by Netflix's login page. [Netflix Website](https://www.netflix.com/)


## License
This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).
