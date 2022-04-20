import flask
import requests
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.user import User
from data.track import Track
import json
import pprint
import sqlite3

app = Flask("rec_api")
api = Api(app)
db_session.global_init("db/min.db")


def get_weather_coefficient(town):
    weather_request = requests.get("http://api.openweathermap.org/data/2.5/find",
                                   params={'q': town, 'type': 'like', 'units': 'metric',
                                           'APPID': "fc20e1ec34892c63aaba900d9516615a"})
    weather_request = weather_request.json()
    pprint.pprint(weather_request["list"][0]["weather"])
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
    def get(self, user_id, town="Moscow"):

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()
        if not user:
            return json.dump({"res": "Not founded"})
        tp = user.temp_preference

        mp = user.mood_preference
        weat_coef = get_weather_coefficient(town)
        similar_users = [i.id for i in
                         db_sess.query(User).filter(tp - weat_coef < User.temp_preference,
                                                    tp + weat_coef > User.temp_preference,
                                                    mp - weat_coef < User.mood_preference,
                                                    mp + weat_coef > User.mood_preference)]
        conn = sqlite3.connect("db/min.db")
        cur = conn.cursor()
        others_liked = set()
        for i in similar_users:
            try:
                res = cur.execute(f"""SELECT track FROM liked{i}""").fetchall()
                for i in res:
                    others_liked.add(int(i[0]))
            except:
                print("Error")
        similar_tracks = set([i.id for i in
                              db_sess.query(Track).filter(tp - weat_coef < Track.temp_preference,
                                                          tp + weat_coef > Track.temp_preference,
                                                          mp - weat_coef < Track.mood_preference,
                                                          mp + weat_coef > Track.mood_preference)])
        rec_first_lvl = similar_tracks & others_liked
        rec_second_lvl = similar_tracks
        response = {
            "rec_first_lvl": [db_sess.query(Track).get(i).to_dict() for i in rec_first_lvl],
            "rec_second_lvl": [db_sess.query(Track).get(i).to_dict() for i in rec_second_lvl]
        }
        return flask.jsonify(response)


api.add_resource(TrackResource, "/rec_api/<int:user_id>/<string:town>")
app.run()
