# Anisync - Convert your Anime List to osu maps!

## Check out the Youtube video of the design process [here](https://www.youtube.com/watch?v=s8QjH_Dcb8g)

## Description

Have you ever had an issue of finding maps to play? well we are here to fix that by bridging the gap between anime and osu! Anisync is a web application that takes a MyAnimeList (MAL) username as input and returns a list of songs from the popular game osu! that appear on the user's anime list. As an osu! player myself, I always found it difficult to find maps to play when it was so tedious to search an anime one by one. For those who don't know, osu! is a popular rhythm game that has a large community of players. The game has a large library of songs to choose from and is constantly growing. The game is free to play and can be downloaded [here](https://osu.ppy.sh/home/download).


![View Maps](Anisync/static/images/view-maps.png)
## How to run the program

Currently, a website for this program is deployed with the latest version being available at: https://anisync.live

To run it locally using docker, follow these steps:

1. Clone this repository to your local machine and navigate into it:

```bash
git clone https://github.com/RajPandya737/Anisync.git
cd Anisync
```

2. Build the Docker container:

```bash
sudo docker build -t anisync .
```

3. Run the Docker container and access the website at http://localhost:8000:

```bash
sudo docker run -p 8000:8000 anisync
```


## Usage

On the website, simply type in your MAL username into the search bar and click submit. The program will then take a few seconds to process the data and return a list of beatmaps that appear on your anime list. The beatmaps are sorted by the rating you gave on your list, and is limited to 300 beatmaps. If you have typed in your username correctly and no maps appear, it is likely due to the theme you have enabled on your anime profile, please disable it and try again.

If you are running it locally, make your way to http://localhost:8000 and follow the same steps as above.

## Project Structure
The project consists of the following files inside of the Anisync Folder folder:

1. `app.py`: The main Python script.
2. `config.py`: Contains all constants used in the program.
3. `data_processing.py`: Stores all data retrieval functions.
4. `db.py`: Runs any database related functions, used to add data to the database.
5. `static/css`: Contains CSS for each of the respective HTML files. The CSS is minified.
6. `static/images`: Contains all images used in the project.
7. `static/js/about.js`: Gives FAQ button functionality on about route.
8. `static/js/index.js`: Corrects anime name mistakes due to the data_processing.py script on view-maps route.
9. `static/js/scroll.js`: Sticky header functionality on view-maps route.
10. `templates`: Contains all HTML files used in the project.
11. `translated_anime_list.sqlite`: SQLite3 database that stores all anime data.
12. `wsgi.py`: Used for deployment on Digital Ocean.


## Future Development

I will try to maintain this site and add new features when possible, however, with school and other commitments, I cannot guarantee that I will be able to. If you have any suggestions, feel free to let me know. As of right now, a few features I would like to add are:
 - Anilist Support
 - Top Anime ranked by MAL and their maps
 - Sorting by categories other than user rating
 - Multiple maps per anime


## Credits

- **MyAnimeList API**: Currently used to get the anime image. [Github and Documentation](https://github.com/darenliang/mal-api)
- **Osu! API**: While I do not use this in the current state of the project, I initially did to aid in prototyping. [Github and Documentation](https://github.com/circleguard/ossapi)
- **MAL Accounts Used for Testing and Data Gathering**:
    - [04Ace](https://myanimelist.net/profile/04Ace)
    - [MayilArna](https://myanimelist.net/profile/MayilArna)
    - [Kyoko_52](https://myanimelist.net/profile/Kyoko_52)
    - [cantstudy](https://myanimelist.net/profile/cantstudy)
    - [NuxTaku](https://myanimelist.net/profile/NuxTaku)
    - [KingAbsalon21](https://myanimelist.net/profile/KingAbsalon21)
    - [ashuulinksu](https://myanimelist.net/profile/ashuulinksu)
    - [Joshhhp](https://myanimelist.net/profile/Joshhhp)
    - [sayu-simp](https://myanimelist.net/profile/sayu-simp)
    - [Lakdinu](https://myanimelist.net/profile/Lakdinu)
    - [Kineta](https://myanimelist.net/profile/Kineta)
    - [SenApai07](https://myanimelist.net/profile/SenApai07)
    - [SingleH](https://myanimelist.net/profile/SingleH)
    - [ThatAnimeSnobRE](https://myanimelist.net/profile/ThatAnimeSnobRE)
    - [Gsarthotegga](https://myanimelist.net/profile/Gsarthotegga)
- **Netflix**: Much of the UI is inspired by Netflix's login page. [Netflix Website](https://www.netflix.com/)


## License
This project is licensed under the [GNU Affero General Public License v3.0](LICENSE).
