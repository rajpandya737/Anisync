from ossapi import Ossapi
import config

# create a new client at https://osu.ppy.sh/home/account/edit#oauth
api = Ossapi(config.client_id, config.client_secret)

# see docs for full list of endpoints

print((api.search_beatmapsets("tokyo ghoul unravel"))[0])