from ossapi import Ossapi
import config

# create a new client at https://osu.ppy.sh/home/account/edit#oauth
api = Ossapi(config.id, config.password)

# see docs for full list of endpoints
print(api.user("tybug").username)
print(api.user(12092800, mode="osu").username)
print(api.beatmap(221777).id)