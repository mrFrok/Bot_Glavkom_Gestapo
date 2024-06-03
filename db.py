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
    else:
        c.execute("UPDATE users SET username=?, name=? WHERE userid=?",
                  (username, name, userid))
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


def get_user2_from_username(username):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user


def delete_user(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE userid=?", (userid,))
    conn.commit()
    conn.close()


def get_user_dick(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM dicks WHERE userid = ?', (userid,))
    dick = c.fetchone()
    conn.close()
    return dick


def update_user(userid, username, name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE users SET username=?, name=? WHERE userid=?", (username, name, userid))
    conn.commit()
    conn.close()


def add_dick(userid, name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM dicks WHERE userid = ?", (userid,))
    user_exists = c.fetchone()[0] > 0
    if not user_exists:
        c.execute('INSERT INTO dicks (userid, name) VALUES (?,?)',
                  (userid, name))
        c.execute('INSERT INTO dicks_inventory (userid) VALUES (?)', (userid,))
        conn.commit()
    conn.close()


def update_dick1(size, last_used, userid, object_1):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks SET size =?, last_used =? WHERE userid =?',
              (size, last_used, userid))
    c.execute('UPDATE dicks_inventory SET object_1 =? WHERE userid =?', (object_1, userid))
    conn.commit()
    conn.close()


def update_dick2(size, last_used, userid, object_2):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks SET size =?, last_used =? WHERE userid =?',
              (size, last_used, userid))
    c.execute('UPDATE dicks_inventory SET object_2 =? WHERE userid =?', (object_2, userid))
    conn.commit()
    conn.close()


def update_dick3(size, last_used, userid, object_3):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks SET size =?, last_used =? WHERE userid =?',
              (size, last_used, userid))
    c.execute('UPDATE dicks_inventory SET object_3 =? WHERE userid =?', (object_3, userid))
    conn.commit()
    conn.close()


def update_last_worked(userid, worked):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks SET last_worked =? WHERE userid =?',
              (worked, userid))
    conn.commit()
    conn.close()


def get_work_level(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT work_level FROM dicks WHERE userid = ?', (userid,))
    work = c.fetchone()
    conn.close()
    return work


def get_work_use(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT work_used FROM dicks WHERE userid = ?', (userid,))
    work = c.fetchone()
    conn.close()
    return work


def update_work_use(userid, work):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks SET work_used =? WHERE userid =?',
              (work, userid))
    conn.commit()
    conn.close()


def get_last_worked(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT last_worked FROM dicks WHERE userid = ?', (userid,))
    work = c.fetchone()
    conn.close()
    return work


def update_work_level(userid, work):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks SET work_level =? WHERE userid =?',
              (work, userid))
    conn.commit()
    conn.close()


def update_money(userid, money):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks_inventory SET money =? WHERE userid =?',
              (money, userid))
    conn.commit()
    conn.close()


def get_money(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT money FROM dicks_inventory WHERE userid = ?', (userid,))
    money = c.fetchone()
    conn.close()
    return money


def get_objects(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT object_1, object_2, object_3 FROM dicks_inventory WHERE userid = ?', (userid,))
    objects = c.fetchone()
    conn.close()
    return objects


def get_medicine(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT medicine FROM dicks_inventory WHERE userid = ?', (userid,))
    medicine = c.fetchone()
    conn.close()
    return medicine


def get_inventory(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT object_1, object_2, object_3, medicine FROM dicks_inventory WHERE userid = ?', (userid,))
    inventory = c.fetchone()
    conn.close()
    return inventory


def update_object1(userid, object_1, money):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks_inventory SET money =? WHERE userid =?', (money, userid))
    c.execute('UPDATE dicks_inventory SET object_1 =? WHERE userid =?',
              (object_1, userid))
    conn.commit()
    conn.close()


def update_object2(userid, object_2, money):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks_inventory SET money =? WHERE userid =?', (money, userid))
    c.execute('UPDATE dicks_inventory SET object_2 =? WHERE userid =?',
              (object_2, userid))
    conn.commit()
    conn.close()


def update_object3(userid, object_3, money):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks_inventory SET money =? WHERE userid =?', (money, userid))
    c.execute('UPDATE dicks_inventory SET object_3 =? WHERE userid =?',
              (object_3, userid))
    conn.commit()
    conn.close()


def update_medicine(userid, medicine, money):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks_inventory SET money =? WHERE userid =?', (money, userid))
    c.execute('UPDATE dicks_inventory SET medicine =? WHERE userid =?',
              (medicine, userid))
    conn.commit()
    conn.close()


def get_sick(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT is_sick FROM dicks WHERE userid = ?', (userid,))
    sick = c.fetchone()
    conn.close()
    return sick


def update_sick(userid, sick):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks SET is_sick =? WHERE userid =?',
              (sick, userid))
    conn.commit()
    conn.close()


def heal_sick(userid, sick, medicine):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks SET is_sick =? WHERE userid =?',
              (sick, userid))
    c.execute('UPDATE dicks_inventory SET medicine =? WHERE userid =?', (medicine, userid))
    conn.commit()
    conn.close()


def get_top_dicks():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT userid, name, size FROM dicks ORDER BY size DESC LIMIT 10')
    top_users = c.fetchall()
    conn.close()
    return top_users


def decrease_dick(userid, size):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks SET size =? WHERE userid =?',
              (size, userid))
    conn.commit()
    conn.close()


def add_loan(userid, is_loan, loan_balance, date_loan):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks SET is_loan =?, loan_balance =?, date_loan = ? WHERE userid =?',
              (is_loan, loan_balance, date_loan, userid))
    conn.commit()
    conn.close()


def get_loan(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT is_loan, loan_balance, date_loan, last_check_loan, last_update_loan FROM dicks WHERE userid = ?',
              (userid,))
    loan = c.fetchone()
    conn.close()
    return loan


def update_loan_balance(userid, loan_balance, last_check_loan, last_update_loan):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE dicks SET loan_balance = ?, last_check_loan = ?, last_update_loan = ? WHERE userid = ?',
              (loan_balance, last_check_loan, last_update_loan, userid))
    conn.commit()
    conn.close()


def repay_the_loan(userid, is_loan):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(
        'UPDATE dicks SET loan_balance = 0, is_loan = ?, date_loan = NULL, last_check_loan = NULL, last_update_loan = NULL WHERE userid =?',
        (is_loan, userid))
    conn.commit()
    conn.close()


def full_update(userid, username, name):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE users SET username=?, name=? WHERE userid=?", (username, name, userid))
    c.execute('UPDATE dicks SET name=? WHERE userid =?',
              (name, userid))
    c.execute('UPDATE varns SET name=?, username=? WHERE userid = ?', (name, username, userid))
    c.execute('UPDATE restricts SET name=?, username=? WHERE userid = ?', (name, username, userid))
    c.execute('UPDATE reputations SET name=?, username=? WHERE userid = ?', (name, username, userid))
    c.execute('UPDATE reminder SET name=? WHERE userid = ?', (name, userid))
    try:
        c.execute('UPDATE marriages SET name1=? WHERE userid1 = ?', (name, userid))
    except:
        c.execute('UPDATE marriages SET name2=? WHERE userid2 = ?', (name, userid))
    conn.commit()


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


def new_reminder(userid, name, time):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO reminder (userid, name, is_send, time) VALUES (?, ?, 0, ?)', (userid, name, time))
    conn.commit()
    conn.close()


def check_reminder(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT name FROM reminder WHERE userid=?',
              (userid,))  # Небольшой костыль, мне просто нужно знать, есть ли пользователь в бд :)
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
    c.execute('UPDATE reminder SET time = ?, is_send = 0 WHERE userid =?', (time, userid))
    conn.commit()


def update_send_remind(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE reminder SET is_send = 1 WHERE userid =?', (userid,))
    conn.commit()


def get_reminders():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT userid, time, is_send FROM reminder')
    users = c.fetchall()
    return users


def add_restricts(userid, username, name, reason_restrict, type_restrict, date_restrict):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(
        'INSERT INTO restricts (userid, username, name, reason_restrict, type_restrict, date_restrict) VALUES (?, ?, ?, ?, ?, ?)',
        (userid, username, name, reason_restrict, type_restrict, date_restrict))
    conn.commit()
    conn.close()


def get_user_restricts(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM restricts WHERE userid=?', (userid,))
    user = c.fetchall()
    conn.close()
    return user


def get_user_restricts_for_two_weeks(userid):
    from datetime import datetime, timedelta
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    two_weeks_ago = datetime.now() - timedelta(weeks=2)
    c.execute(
        'SELECT type_restrict, reason_restrict, date_restrict FROM restricts WHERE userid=? AND date_restrict >= ?',
        (userid, two_weeks_ago))
    user = c.fetchall()
    conn.close()
    return user


def add_reputation_if_not_exists(userid, username, name, reputation):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM reputations WHERE userid = ?", (userid,))
    user_exists = c.fetchone()[0] > 0
    if not user_exists:
        c.execute(
            'INSERT INTO reputations (userid, username, name, reputation) VALUES (?, ?, ?, ?)',
            (userid, username, name, reputation))
        conn.commit()

    conn.close()


def get_user_reputation(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT reputation FROM reputations WHERE userid=?', (userid,))
    user = c.fetchone()
    conn.close()
    return user


def get_top_reputation():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT userid, name, reputation FROM reputations ORDER BY reputation DESC LIMIT 10')
    user = c.fetchall()
    conn.close()
    return user


def update_reputation(userid, reputaion):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE reputations SET reputation = ? WHERE userid =?', (reputaion, userid))
    conn.commit()
    conn.close()


def get_last_use_reputation(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT last_use FROM reputations WHERE userid=?', (userid,))
    user = c.fetchone()
    conn.close()
    return user


def update_last_use_reputation(userid, last_use):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE reputations SET last_use = ? WHERE userid =?', (last_use, userid))
    conn.commit()
    conn.close()


def delete_restricts_user(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM restricts WHERE userid=?', (userid,))
    conn.commit()
    conn.close()


def update_about(userid, about):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('UPDATE users SET about = ? WHERE userid =?', (about, userid))
    conn.commit()
    conn.close()


def get_about(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT about FROM users WHERE userid=?', (userid,))
    user = c.fetchone()
    conn.close()
    return user


def add_marriage(userid1, userid2, username1, username2, name1, name2, date):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(
        'INSERT INTO marriages (userid1, userid2, username1, username2, name1, name2, date) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (userid1, userid2, username1, username2, name1, name2, date))
    conn.commit()
    conn.close()


def get_marriages():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM marriages ORDER BY date')
    users = c.fetchall()
    conn.close()
    return users


def delete_marriage(userid1, userid2):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM marriages WHERE userid1=? AND userid2=?', (userid1, userid2))
    conn.commit()
    conn.close()


def check_marriage(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM marriages WHERE userid1=? OR userid2=?', (userid, userid))
    user = c.fetchall()
    conn.close()
    return user


def add_temp(userid1, userid2, username1, username2, name1, name2):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO temp (userid1, userid2, username1, username2, name1, name2) VALUES (?, ?, ?, ?, ?, ?)',
              (userid1, userid2, username1, username2, name1, name2))
    conn.commit()
    conn.close()


def get_temp(userid):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM temp WHERE userid1=? OR userid2=?', (userid, userid))
    user = c.fetchall()
    conn.close()
    return user


def delete_temp(userid1, userid2):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM temp WHERE userid1=? AND userid2=?', (userid1, userid2))
    conn.commit()
    conn.close()
