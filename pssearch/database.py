import sqlite3, os
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash


def create_account(username, password):
    connection = sqlite3.connect(os.path.join(app.root_path, 'static/accounts.db'))
    cursor = connection.cursor()
    cursor.execute(
            """INSERT INTO accounts ("username", "password") VALUES (?, ?)""",
            (username, generate_password_hash(password))
            )
    connection.commit()
    connection.close()

def check_account(username, password):
    connection = sqlite3.connect(os.path.join(app.root_path, 'static/accounts.db'))
    cursor = connection.cursor()
    cursor.execute(
            """SELECT * FROM accounts WHERE "username"=?""",
            (username, )
            )

    account = cursor.fetchone()
    connection.close()
    if account and check_password_hash(account[2], password):
        return True
    else:
        return False


