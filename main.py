from flask import *
from data import db_session
from data.user import User
from data.track import Track
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

db_session.global_init("db/main.db")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

class RegForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


@app.route("/reg", methods=["POST", "GET"])
def red():
    form = RegForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.hashed_password = user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()
    elif request.method == "POST":
        if request.form["test"] == "top":

            print(request.form)
            return redirect("/yong")

    return render_template("singup_page.html", form=form)

@app.route("/log", methods=["POST", "GET"])
def blur():
    form = LoginForm()
    print(0)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        print(1)
        if user and user.check_password(form.password.data):
            return redirect("/yong")
    return render_template("singin_page.html", form=form)

@app.route("/wav")
def streamwav():
    def generate():
        with open("static/song.wav", "rb") as fwav:
            data = fwav.read(1024)
            print(data)
            while data:
                yield data
                data = fwav.read(1024)

    return Response(generate(), mimetype="audio/x-wav")





@app.route("/yong")
def ter():
    return "oppps"
app.run(debug = True)