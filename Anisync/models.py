from flask_sqlalchemy import SQLAlchemy
from app import db

class Anime(db.Model):
    anime_name = db.Column(db.String(100), primary_key=True)
    anime_song = db.Column(db.String(200), primary_key=True)
    anime_img = db.Column(db.String(1000), primary_key=True)
    osu_link = db.Column(db.String(1000), primary_key=True)