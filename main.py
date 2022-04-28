from flask import *
from data import db_session
from data.user import User
from data.track import Track
from data.playlist import Playlist
import os
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
        new_track.img_path = f"static/track_cover/{form.track_name.data}.png"
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
    a = requests.get(f'http://127.0.0.1:5000/rec_api/Moscow/1/{session.get("_user_id")}')
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
    track_list = [random.choice(tracks) for i in range(10)]
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



@app.route("/yong")
def ter():
    return "oppps"


api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('user_id', required=True, type=int)


def get_weather_coefficient(town):
    weather_request = requests.get("http://api.openweathermap.org/data/2.5/find",
                                   params={'q': town, 'type': 'like', 'units': 'metric',
                                           'APPID': "fc20e1ec34892c63aaba900d9516615a"})
    weather_request = weather_request.json()
    if not weather_request["list"]:
        return 1
    res_cof = 4

    if abs(weather_request["list"][0]["main"]["temp"]) <= 20:
        res_cof += weather_request["list"][0]["main"]["temp"] / 10
    else:
        if weather_request["list"][0]["main"]["temp"] > 0:
            res_cof += 1
        else:
            res_cof -= 2
    if 200 < int(weather_request["list"][0]["weather"][0]["id"]) < 800:
        res_cof -= 1.5
    else:
        res_cof += 1
    return round(res_cof, 2)


class TrackResource(Resource):
    def get(self, town="Moscow", one_track=0, user_id=0):
        db_sess = db_session.create_session()
        if not user_id:
            user = db_sess.query(User).filter(User.id == session.get("_user_id")).first()
        else:
            user = db_sess.query(User).filter(User.id == user_id).first()
        if not user:
            return json.dump({"res": "Not founded"})
        print(user.id)
        tp = user.temp_preference

        mp = user.mood_preference
        weat_coef = get_weather_coefficient(town)
        similar_users = [i.id for i in
                         db_sess.query(User).filter(tp - weat_coef < User.temp_preference,
                                                    tp + weat_coef > User.temp_preference,
                                                    mp - weat_coef < User.mood_preference,
                                                    mp + weat_coef > User.mood_preference)]
        others_liked = set()
        for i in similar_users:
            pl = db_sess.query(Playlist).filter(Playlist.user_id == i).first()
            if i == 5:
                id_pl = pl.id
                for j in db_sess.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == id_pl):
                    others_liked.add(j.track_id)

        similar_tracks = set([i.id for i in
                              db_sess.query(Track).filter(tp - weat_coef < Track.temp_preference,
                                                          tp + weat_coef > Track.temp_preference,
                                                          mp - weat_coef < Track.mood_preference,
                                                          mp + weat_coef > Track.mood_preference)])
        rec_first_lvl = list(similar_tracks & others_liked)
        rec_second_lvl = list(similar_tracks)
        res = rec_second_lvl + rec_first_lvl
        if one_track == 1:
            print(weat_coef)
            response = {
                "track": db_sess.query(Track).get(random.choice(res)).to_dict()}
            session["_track_now"] = response["track"]
        elif one_track == 1 and not rec_first_lvl and not rec_first_lvl:
            response = {"track": random.choice([i.id for i in db_sess.query(Track).all()])}
            session["_track_now"] = response["track"]
        else:
            response = {
                "rec_first_lvl": [db_sess.query(Track).get(i).to_dict() for i in rec_first_lvl],
                "rec_second_lvl": [db_sess.query(Track).get(i).to_dict() for i in rec_second_lvl]
            }

        response_res = jsonify(response)
        response_res.headers.add('Access-Control-Allow-Origin', '*')
        return response_res


class TrackInPlayList(Resource):
    def get(self, playlist_id, track_id=0):
        db_sess = db_session.create_session()
        response = {"track": random.choice(
            [i.id for i in db_sess.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist_id)])}
        response_res = jsonify(response)
        response_res.headers.add('Access-Control-Allow-Origin', '*')
        return response_res

    def delete(self, playlist_id, track_id=0):
        db_sess = db_session.create_session()
        pl_id = playlist_id
        db_sess.query(PlaylistTrack).filter(PlaylistTrack.track_id == track_id,
                                            PlaylistTrack.playlist_id == pl_id
                                            ).delete()
        db_sess.commit()


class ToPlaylist(Resource):
    def post(self, choose_playlist, track_id=0):
        db_sess = db_session.create_session()
        if track_id:
            track = db_sess.query(Track).filter(Track.id == track_id).first()
        else:
            track = db_sess.query(Track).filter(Track.tack_path == session.get("_track_now")).first()
        track_playlist = PlaylistTrack()
        track_playlist.track_id = track.id
        playlist = db_sess.query(Playlist).filter(Playlist.id == choose_playlist).first()
        if playlist.id:
            track_playlist.playlist_id = playlist.id
            response_res = jsonify({"response": "succes"})
            response_res.headers.add('Access-Control-Allow-Origin', '*')

        else:
            response_res = jsonify({"response": "not_succes"})
        if not db_sess.query(PlaylistTrack).filter(PlaylistTrack.track_id == track_playlist.track_id,
                                                   PlaylistTrack.playlist_id == track_playlist.playlist_id).first():
            db_sess.add(track_playlist)
        db_sess.commit()
        return response_res

    def delete(self, choose_playlist, track_id=0):
        db_sess = db_session.create_session()
        print(choose_playlist, 23232)
        pl_id = choose_playlist
        db_sess.query(PlaylistTrack).filter(
            PlaylistTrack.playlist_id == pl_id
        ).delete()
        db_sess.query(Playlist).filter(
            Playlist.id == pl_id
        ).delete()
        db_sess.commit()


api.add_resource(TrackResource, "/rec_api/<string:town>/<int:one_track>",
                 "/rec_api/<string:town>/<int:one_track>/<int:user_id>")
api.add_resource(ToPlaylist, "/pl_api/<string:choose_playlist>",
                 "/pl_api/<string:choose_playlist>/<string:track_id>")
api.add_resource(TrackInPlayList, "/track_pl/<int:playlist_id>", "/track_pl/<int:playlist_id>/<int:track_id>")
app.run(debug=True)
