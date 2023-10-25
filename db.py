import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()


def add_user(userid, username, name):
    c.execute("INSERT INTO userinfo (userid, username, name) VALUES (?,?,?)", (userid, username, name))
    conn.commit()


def add_user_if_not_exists(userid, username, name):
    c.execute("SELECT COUNT(*) FROM userinfo WHERE userid = ?", (userid,))
    user_exists = c.fetchone()[0] > 0

    if not user_exists:
        c.execute("INSERT INTO userinfo (userid, name, username) VALUES (?, ?, ?)", (userid, name, username))
        conn.commit()


def get_user(userid):
    c.execute('SELECT * FROM userinfo WHERE userid = ?', (userid,))
    user = c.fetchone()
    return user


def get_user_from_name(name):
    c.execute('SELECT userid FROM userinfo WHERE name = ?', (name,))
    user = c.fetchone()
    return user

def get_user_from_username(username):
    c.execute('SELECT userid FROM userinfo WHERE username = ?', (username,))
    user = c.fetchone()
    return user

def get_user_hui(userid):
    c.execute('SELECT * FROM hui WHERE userid = ?', (userid,))
    hui = c.fetchone()
    return hui


def add_hui(userid, username, razm_hui, day, month, year):
    c.execute('INSERT INTO hui (userid, username, razm_hui, day, month, year) VALUES (?,?,?,?,?, ?)',
              (userid, username, razm_hui, day, month, year))
    conn.commit()


def update_hui(razm_hui, day, month, year, userid):
    c.execute('UPDATE hui SET razm_hui =?, day =?, month=?, year =? WHERE userid =?',
              (razm_hui, day, month, year, userid))
    conn.commit()

def full_update(userid, username, name):
    c.execute("UPDATE userinfo SET username=?, name=? WHERE userid=?", (username, name, userid))
    c.execute('UPDATE hui SET username=? WHERE userid =?',
              (name, userid))
    c.execute('UPDATE varns SET username=? WHERE userid = ?', (name, userid))
    c.execute('UPDATE nedrochabr SET username=? WHERE userid =?', (name, userid))
    conn.commit()


def update_user(userid, username, name):
    c.execute("UPDATE userinfo SET username=?, name=? WHERE userid=?", (username, name, userid))
    conn.commit()


def delete_user(userid):
    c.execute("DELETE FROM userinfo WHERE userid=?", (userid,))
    conn.commit()


def get_top_users():
    c.execute('SELECT userid, username, razm_hui FROM hui ORDER BY razm_hui DESC LIMIT 10')
    top_users = c.fetchall()
    return top_users


def new_varn_user(userid, username, value_varns, reason):
    c.execute('INSERT INTO varns (userid, username, value_varns, reason) VALUES (?, ?, ?, ?)',
              (userid, username, value_varns, reason))
    conn.commit()


def get_varn_users(userid):
    c.execute('SELECT value_varns FROM varns WHERE userid = ?', (userid,))
    user = c.fetchone()
    return user


def update_varn_user(userid, value_varns, reason):
    c.execute('UPDATE varns SET value_varns = ?, reason = ? WHERE userid = ?', (value_varns, reason, userid))
    conn.commit()


def delete_varn_user(userid):
    c.execute("DELETE FROM varns WHERE userid=?", (userid,))
    conn.commit()


def get_top_varn_users():
    c.execute('SELECT userid, username, value_varns, reason FROM varns ORDER BY value_varns')
    top_users = c.fetchall()
    return top_users


def get_users():
    c.execute('SELECT userid FROM userinfo')
    user = c.fetchall()
    return user

def add_user_nedr(userid, username, status):
    c.execute('INSERT INTO nedrochabr (userid, username, status) VALUES (?,?,?)', (userid, username, status))
    conn.commit()

def update_user_nedr(userid, username, status):
    c.execute('UPDATE nedrochabr SET username=?, status=?, perehod=1 WHERE userid =?', (username, status, userid))
    conn.commit()

def get_status_nedr(userid):
    c.execute('SELECT status FROM nedrochabr WHERE userid =?', (userid,))
    user = c.fetchone()
    return user

def get_users_nedr():
    c.execute('SELECT userid, username, status FROM nedrochabr')
    user = c.fetchall()
    return user

def get_user_nedr(userid):
    c.execute('SELECT username, status, perehod FROM nedrochabr WHERE userid =?', (userid,))
    user = c.fetchone()
    return user
