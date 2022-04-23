from flask import *
from data import db_session
from data.user import User
from data.track import Track
from data.playlist import Playlist
import os
import playlists
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required

from forms import LoginForm, RegForm, AddTrack, AddPlaylist

db_session.global_init("db/min.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
def check_path(path):
    if os.path.exists(path):
        path

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/reg", methods=["POST", "GET"])
def sing_up():
    form = RegForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user.name = form.name.data
        user.town = form.town.data
        user.email = form.email.data
        user.hashed_password = user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=True)
        playlists.create_playlist("db/min.db", "liked", user.id)


    return render_template("singup_page.html", form=form)


@app.route("/log", methods=["POST", "GET"])
def sing_in():
    form = LoginForm()
    print(0)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(1)
        if user and user.check_password(form.password.data):
            return redirect("/yong")
    return render_template("singin_page.html", form=form)





@app.route("/add/song", methods=["POST", "GET"])
def add_song():
    form = AddTrack()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        new_track = Track()
        new_track.track_name = form.track_name.data
        new_track.temp_preference = form.temp_preference.data / 5
        new_track.mood_preference = form.mood_preference.data / 5
        new_track.user_id = session.get("_user_id")
        data_track = form.track_file.data

        path = f"static/tracks/{new_track.id}.wav"
        new_track.tack_path = path
        if data_track:
            data_track.save(path)
            db_sess.add(new_track)
            db_sess.commit()
    return render_template("add_track.html", form=form)

#_user_id


@app.route("/add/playlist", methods=["POST", "GET"])
def add_playlist():
    form = AddPlaylist()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        new_playlist = Playlist()
        new_playlist.name = form.playlists_name.data
        new_playlist.description = form.playlists_description.data

        new_playlist.all_track = f"{form.playlists_name.data}{session.get('_user_id')}"
        playlists.create_playlist("db/min.db",form.playlists_name.data, session.get("_user_id"))

        cover = form.playlists_cover.data
        cover.save(f"static/playlist_cover/{new_playlist.id}.png")
        db_sess.add(new_playlist)
        db_sess.commit()

    return render_template("add_playlist.html", form=form)


@app.route("/yong")
def ter():
    return "oppps"


app.run(debug=True)
