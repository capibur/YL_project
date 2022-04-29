from flask import *
from data import db_session
from data.user import User
from data.track import Track
from data.playlist import Playlist
import os
import rec_api
import requests
from data.playlist_track import PlaylistTrack
from flask_restful import reqparse, abort, Api, Resource
import random
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user

from forms import LoginForm, RegForm, AddTrack, AddPlaylist, SearchMusic, ShowMusic

db_session.global_init("db/min.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('user_id', required=True, type=int)






def check_path(path):
    if os.path.exists(path):
        path


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/reg", methods=["POST", "GET"])
def sing_up():
    form = RegForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user.name = form.name.data
        user.town = form.town.data
        print(form.email.data)
        user.email = form.email.data

        user.hashed_password = user.set_password(form.password.data)
        db_sess.add(user)

        db_sess.commit()
        l_playlist = Playlist()
        l_playlist.name = "liked"
        l_playlist.description = "лайкнутные треки"
        l_playlist.img_path = "liked.png"
        l_playlist.user_id = user.id
        db_sess.add(l_playlist)
        db_sess.commit()

        login_user(user, remember=True)
        return redirect("/homepage")
    return render_template("singup_page.html", form=form)


@app.route("/log", methods=["POST", "GET"])
def sing_in():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)

    return render_template("singin_page.html", form=form)


@app.route("/add/song", methods=["POST", "GET"])
@login_required
def add_song():
    form = AddTrack()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        new_track = Track()
        new_track.track_name = form.track_name.data
        new_track.temp_preference = round(form.temp_preference.data / 5, 3)
        new_track.mood_preference = round(form.mood_preference.data / 5, 3)
        new_track.user_id = session.get("_user_id")
        data_track = form.track_file.data

        path = f"tracks/{new_track.track_name}.wav"
        cover = form.cover_file.data
        cover.save(f"static/track_cover/{form.track_name.data}.png")
        new_track.img_path = f"track_cover/{form.track_name.data}.png"
        new_track.tack_path = path
        if data_track:
            data_track.save("static/" + path)
            db_sess.add(new_track)
            db_sess.commit()
    return render_template("add_track.html", form=form)


# _user_id


@app.route("/add/playlist", methods=["POST", "GET"])
@login_required
def add_playlist():
    form = AddPlaylist()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        new_playlist = Playlist()
        new_playlist.name = form.playlists_name.data
        new_playlist.description = form.playlists_description.data
        cover = form.playlists_cover.data
        cover.save(f"static/playlist_cover/{new_playlist.id}.png")
        new_playlist.user_id = session.get("_user_id")
        new_playlist.img_path = f"playlist_cover/{new_playlist.id}.png"
        db_sess.add(new_playlist)
        db_sess.commit()
    return render_template("add_playlist.html", form=form)


@app.route("/radio", methods=["POST", "GET"])
@login_required
def radio():
    db_sess = db_session.create_session()
    a = requests.get(f'https://ylp3.herokuapp.com/rec_api/Moscow/1/{session.get("_user_id")}')
    first_track_path = a.json()["track"]["tack_path"]
    session["_track_now"] = first_track_path
    playlists = [i for i in db_sess.query(Playlist).filter(Playlist.user_id == session.get("_user_id"))]

    return render_template("radio_player.html", first_track=url_for('static', filename=first_track_path), pl=playlists,
                           img_path=a.json()["track"]["img_path"],
                           name=a.json()["track"]["track_name"])


@app.route("/homepage", methods=["POST", "GET"])
@login_required
def home_page():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == session.get("_user_id")).first()
    tracks = db_sess.query(Track).all()
    pl = [i for i in db_sess.query(Playlist).filter(Playlist.user_id == session.get("_user_id"))]
    if pl:
        track_list = [random.choice(tracks) for i in range(10)]
    else:
        tracks_list = []
    return render_template("home_page.html", user_name=user.name, tracks=track_list, pl=pl)


@app.route("/myplaylists", methods=["POST", "GET"])
@login_required
def my_playlists():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == session.get("_user_id")).first()
    pl = [i for i in db_sess.query(Playlist).filter(Playlist.user_id == session.get("_user_id"))]

    return render_template("my_playlists.html", pl=pl)

@app.route("/show_music", methods=["GET", "POST"])
def show_music(name):
    form = ShowMusic()
    db_sess = db_session.create_session()
    music = db_sess.query(Track).filter(Track.track_name.like(f"%{name}%"))
    music_list = [i.get_name() for i in music]

    return render_template("show_music.html", form=form, music_name=name, music_list=music_list)


@app.route("/search_music", methods=["GET", "POST"])
def search_music():
    form = SearchMusic()
    if form.validate_on_submit():
        name = form.search_line.data
        return show_music(name)
    return render_template("search_music.html", form=form)


@app.route("/playlist/<int:playlist_id>")
def playlist(playlist_id):
    db_sess = db_session.create_session()
    pl = db_sess.query(Playlist).filter(Playlist.id==playlist_id).first()
    tracks_id = db_sess.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist_id).all()
    tracks = [db_sess.query(Track).filter(Track.id == i.track_id).first() for i in tracks_id]
    a = requests.get(f'https://ylp3.herokuapp.com/track_pl/{playlist_id}')
    try:
        first_track_path = a.json()["track"]["tack_path"]
    except TypeError:
        first_track_path = "/none"
    print(pl.user_id, session.get("_user_id"))
    is_pl_my = True if str(pl.user_id) == session.get("_user_id") else False
    return render_template("playlist.html", tracks=tracks, playlist_id=playlist_id,
                           first_track=first_track_path,
                           img_path=pl.img_path,
                           pl_description=pl.description,
                           pl_name=pl.name,
                           is_pl_my=is_pl_my)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == session.get("_user_id")).first()
    tracks = db_sess.query(Track).filter(Track.user_id == session.get("_user_id")).all()
    if request.method == "POST":
        user.email = request.form.get("email")
    db_sess.commit()
    return render_template("profile.html", tracks=tracks,
                           name=user.name,
                           email=user.email,
                           temp=user.temp_preference,
                           mood=user.mood_preference
                           )


@app.route("/yong")
def ter():
    return "oppps"


api.add_resource(rec_api.TrackResource, "/rec_api/<string:town>/<int:one_track>",
                 "/rec_api/<string:town>/<int:one_track>/<int:user_id>")
api.add_resource(rec_api.ToPlaylist, "/pl_api/<string:choose_playlist>",
                 "/pl_api/<string:choose_playlist>/<string:track_id>")
api.add_resource(rec_api.TrackInPlayList, "/track_pl/<int:playlist_id>", "/track_pl/<int:playlist_id>/<int:track_id>")
api.add_resource(rec_api.TrackApi, "/track_del/<int:track_id>")
api.add_resource(rec_api.ChangePref, "change_pref/<string:action>")
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)