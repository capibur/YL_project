import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Track(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "track"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    id_playlist = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    tack_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    track_duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # в секундах
    temp_preference = sqlalchemy.Column(sqlalchemy.Float, nullable=True)

    mood_preference = sqlalchemy.Column(sqlalchemy.Float, nullable=True)
    def __repr__(self):
        return str(self.id)
    def __int__(self):
        return int(self.id)