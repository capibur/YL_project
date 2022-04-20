import sqlite3


def create_playlist(db, name, user):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {name}{str(user)}(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       track int
       );
    """)
    conn.commit()


def del_playlist(db, name, user):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f"""DROP TABLE {name}{str(user)} """)
    conn.commit()


def edit_playlist(db, name, user, track, edit_type=True):
    # при edit_type==True, трек добавляется
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    if edit_type:
        print(3333)
        cur.execute(f"""
        INSERT INTO {name}{str(user)}(track)
        VALUES ({track})
    """)
        conn.commit()
    elif not edit_type:
        cur.execute(f"DELETE FROM {name}{str(user)} WHERE track={track};")
        conn.commit()
edit_playlist("db/min.db", "liked", 2, 243534)
