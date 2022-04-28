from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalRangeField, FileField
from wtforms.validators import DataRequired

class RegForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired()])
    town = StringField("Город", validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class AddTrack(FlaskForm):
    track_name = StringField("Название песни", validators=[DataRequired()])
    temp_preference = DecimalRangeField(label="Темп песни", places=2)
    mood_preference = DecimalRangeField(label="Настроение песни", places=2)
    track_file = FileField()
    cover_file = FileField()
    submit = SubmitField('Загрузить')


class AddPlaylist(FlaskForm):
    playlists_name = StringField("Название Плейлиста", validators=[DataRequired()])
    playlists_description = StringField("Описание")
    playlists_cover = FileField()
    submit = SubmitField('Создать')

#new
class SearchMusic(FlaskForm):
    search_line = StringField("Название песни", validators=[DataRequired()])
    submit = SubmitField('Поиск')

class ShowMusic(FlaskForm):
    music = SubmitField('Поиск')
