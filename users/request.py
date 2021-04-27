import sqlite3
import json

from models import User


def get_all_users():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active
        FROM users u
        """)

        users = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            user = User(
                row['first_name'],
                row['last_name'],
                row['email'],
                row['bio'],
                row['username'],
                row['password'],
                row['profile_image_url'],
                row['created_on'],
                row['active']
            )
            users.append(user.__dict__)
    return json.dumps(users)


def get_user_by_email(obj):
    email = obj["username"]
    _pw = obj["password"]

    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            u.email,
            u.password
        FROM users u
        WHERE u.email = ?
        """, (email, ))

        data = db_cursor.fetchone()

        if (data):
            # if you do not check for data you will need to
            # do a try/catch when creating a User instance.
            user = User(
                username=data['email'],
                password=data['password'])

            if(user.password != _pw):
                user = False
        else:
            user = False

        # client-side response needs object
        # if ("valid" in res && res.valid)
        # "token" - for localStorage.setItem
        if(user):
            res = {"valid": True, "token": user.username}
        else:
            res = {"valid": False}

    return json.dumps(res)


def create_user(new_user):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Users
            ( first_name, last_name, username, email, password, created_on )
        VALUES
            ( ?, ?, ?, ?, ?, DATETIME());
        """, (
            new_user['first_name'],
            new_user['last_name'],
            new_user['username'],
            new_user['email'],
            new_user['password'], )
        )

        id = db_cursor.lastrowid
        new_user['id'] = id

    return json.dumps(new_user)
