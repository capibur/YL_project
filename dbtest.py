from data import db_session
from data.user import User
db_session.global_init("db/jin.db")

user = User()
shdbch = User()
user.name = "Пользователь "
user.about = "биография пользователя 1"
user.email = "email@email.ru"
shdbch.name = "Пользователь 1"
shdbch.about = "биография пользователя 1"
shdbch.email = "email@email.ru"
db_sess = db_session.create_session()
db_sess.add(user)
db_sess.add(shdbch)
db_sess.commit()