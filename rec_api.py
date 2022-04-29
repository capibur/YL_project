from flask import *
import requests
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.user import User
from data.track import Track
from data.playlist import Playlist
from data.playlist_track import PlaylistTrack
import json
import pprint
import random
app = Flask("rec_api")
api = Api(app)
db_session.global_init("db/min.db")


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
        print(self)
        try:

            track_id = random.choice(
                [i.track_id for i in db_sess.query(PlaylistTrack).filter(PlaylistTrack.playlist_id == playlist_id)])
        except IndexError:
            return 8

        track = db_sess.query(Track).filter(Track.id == track_id).first()
        response = {"track": track.to_dict()}
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
        if choose_playlist == "liked":
            choose_playlist = db_sess.query(Playlist).filter(Playlist.name == "liked",
                                                             Playlist.user_id == session.get("_user_id")
                                                             ).first().id
        if track_id:
            track = db_sess.query(Track).filter(Track.id == track_id).first()
        else:
            track = db_sess.query(Track).filter(Track.tack_path == session.get("_track_now")).first()
        track_playlist = PlaylistTrack()
        track_playlist.track_id = track.id
        print(choose_playlist)
        playlist = db_sess.query(Playlist).filter(Playlist.id == choose_playlist).first()
        if playlist:
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
class TrackApi(Resource):
    def delete(self, track_id=0):
        db_sess = db_session.create_session()
        db_sess.query(Track).filter(Track.id == track_id).delete()
        db_sess.query(PlaylistTrack).filter(PlaylistTrack.track_id == track_id
                                            ).delete()
        db_sess.commit()
