import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Track(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "track"

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    track_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    tack_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    img_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    track_duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # в секундах
    temp_preference = sqlalchemy.Column(sqlalchemy.Float, nullable=True)

    mood_preference = sqlalchemy.Column(sqlalchemy.Float, nullable=True)

    def __repr__(self):
        return str(self.id)

    def __int__(self):
        return int(self.id)
    def get_id(self):
        return str(self.id)

    def get_name(self):
        return str(self.track_name)