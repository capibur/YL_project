import sqlalchemy
from .db_session import SqlAlchemyBase


class PlaylistTrack(SqlAlchemyBase):
    __tablename__ = "playlist_track"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    playlist_id = sqlalchemy.Column(sqlalchemy.Integer)
    track_id = sqlalchemy.Column(sqlalchemy.Integer)
