import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
import flask_login

class User(SqlAlchemyBase, flask_login.UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    town = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    temp_preference = sqlalchemy.Column(sqlalchemy.Float, nullable=True, default=10)

    mood_preference = sqlalchemy.Column(sqlalchemy.Float, nullable=True, default=10)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
        return self.hashed_password

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


    def set_preference(self, liked_tp, liked_mp, action):
        if action == "like":
            self.temp_preference = (self.temp_preference + liked_tp) / 2
            self.mood_preference = (self.mood_preference + liked_mp) / 2
        elif action =="dislike":
            self.temp_preference = self.temp_preference + (self.temp_preference - liked_tp) / 2
            self.temp_preference = self.mood_preference + (self.mood_preference - liked_mp) / 2

    def __repr__(self):
        return str(self.id)
