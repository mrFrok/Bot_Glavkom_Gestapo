import sqlite3


def add_user(userid, username, name, date_add):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (userid, username, name, date_add) VALUES (?,?,?,?)",
              (userid, username, name, date_add))
    conn.commit()
    conn.close()


def add_user_if_not_exists(userid, username, name, date_add):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users WHERE userid = ?", (userid,))
    user_exists = c.fetchone()[0] > 0

    if not user_exists:
        c.execute("INSERT INTO users (userid, username, name, date_add) VALUES (?,?,?,?)",
                  (userid, username, name, date_add))
        conn.commit()

    conn.close()


def get_user(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE userid = ?', (userid,))
    user = c.fetchone()
    conn.close()
    return user


def get_user_from_name(name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT userid FROM users WHERE name = ?', (name,))
    user = c.fetchone()
    conn.close()
    return user


def get_user_from_username(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT userid FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user


def get_user_dick(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM dicks WHERE userid = ?', (userid,))
    dick = c.fetchone()
    conn.close()
    return dick


def add_dick(userid, name, size, last_used):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO dicks (userid, name, size, last_used) VALUES (?,?,?,?)',
              (userid, name, size, last_used))
    conn.commit()
    conn.close()


def update_dick(size, last_used, userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks SET size =?, last_used =? WHERE userid =?',
              (size, last_used, userid))
    conn.commit()
    conn.close()


def full_update(userid, username, name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE users SET username=?, name=? WHERE userid=?", (username, name, userid))
    c.execute('UPDATE dicks SET name=? WHERE userid =?',
              (name, userid))
    c.execute('UPDATE varns SET name=?, username=? WHERE userid = ?', (name, username, userid))
    # c.execute('UPDATE nedrochabr SET username=? WHERE userid =?', (name, userid))
    # c.execute('UPDATE reminder SET name=? WHERE userid =?', (name, userid))
    conn.commit()


def update_user(userid, username, name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE users SET username=?, name=? WHERE userid=?", (username, name, userid))
    conn.commit()
    conn.close()


def delete_user(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE userid=?", (userid,))
    conn.commit()
    conn.close()


def get_top_dicks():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT userid, name, size FROM dicks ORDER BY size DESC LIMIT 10')
    top_users = c.fetchall()
    conn.close()
    return top_users


def new_varn_user(userid, username, varns, reason, date_last_varn):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO varns (userid, username, varns, reason, date_last_varn) VALUES (?, ?, ?, ?, ?)',
              (userid, username, varns, reason, date_last_varn))
    conn.commit()
    conn.close()


def get_varn_users(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT varns FROM varns WHERE userid = ?', (userid,))
    user = c.fetchone()
    conn.close()
    return user


def update_varn_user(userid, varns, date_last_varn, reason):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE varns SET varns = ?, reason = ?, date_last_varn=? WHERE userid = ?',
              (varns, reason, date_last_varn, userid))
    conn.commit()
    conn.close()


def delete_varn_user(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM varns WHERE userid=?", (userid,))
    conn.commit()
    conn.close()


def get_top_varn_users():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT userid, username, varns, reason, date_last_varn FROM varns ORDER BY varns')
    top_users = c.fetchall()
    conn.close()
    return top_users


def get_users():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT userid FROM users')
    user = c.fetchall()
    conn.close()
    return user


def add_user_nedr(userid, username, status):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO nedrochabr (userid, username, status) VALUES (?,?,?)', (userid, username, status))
    conn.commit()
    conn.close()


def update_user_nedr(userid, username, status):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE nedrochabr SET username=?, status=?, perehod=1 WHERE userid =?', (username, status, userid))
    conn.commit()
    conn.close()


def get_status_nedr(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT status FROM nedrochabr WHERE userid =?', (userid,))
    user = c.fetchone()
    conn.close()
    return user


def get_users_nedr():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT userid, username, status FROM nedrochabr')
    user = c.fetchall()
    conn.close()
    return user


def get_user_nedr(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT username, status, perehod FROM nedrochabr WHERE userid =?', (userid,))
    user = c.fetchone()
    conn.close()
    return user


def new_reminder(userid, name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO reminder (userid, name, active) VALUES (?, ?, 1)', (userid, name))
    conn.commit()
    conn.close()


def check_reminder(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT active FROM reminder WHERE userid=?', (userid,))
    user = c.fetchone()
    return user


def delete_reminder(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM reminder WHERE userid=?', (userid,))
    conn.commit()


def update_reminder(userid, time):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE reminder SET time = ? WHERE userid =?', (time, userid))
    conn.commit()


def get_reminders():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT userid FROM reminder')
    users = c.fetchall()
    return users
