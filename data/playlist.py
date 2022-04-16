import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Track(SqlAlchemyBase):
    __tablename__ = "playlist"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    img_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    track_duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # в секундах
    all_track = None
