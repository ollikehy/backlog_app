from application import db
from application.auth.models import User

from sqlalchemy.sql import text

class VideoGame(db.Model):

    __tablename__ = "videogame"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(144), nullable=False)
    releaseYear = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    
    games = db.relationship("GameInstance", backref="videogame", lazy=True)

    def __init__(self, name, year, genre):
        self.name = name
        self.releaseYear = year
        self.genre = genre

class GameInstance(db.Model):

    __tablename__ = "gameinstance"

    id = db.Column(db.Integer, primary_key=True)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                            nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('videogame.id'),
                        nullable=False)

    completed = db.Column(db.Boolean, nullable=False)

    def __init__(self, account_id, game_id):
        self.account_id = account_id
        self.game_id = game_id
        self.completed = False

    def find_games_by_user(account_id):
        stmt = text("SELECT videogame.name, videogame.genre, videogame.releaseYear "
                    "FROM videogame, gameinstance, account "
                    "WHERE account.id = :account_id "
                    "AND gameinstance.game_id = videogame.id").params(account_id=account_id)
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"name":row[0],"genre":row[1],"releaseYear":row[2]})
        
        return response