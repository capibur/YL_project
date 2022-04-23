import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Playlist(SqlAlchemyBase):
    __tablename__ = "playlist"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    img_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    all_track = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
