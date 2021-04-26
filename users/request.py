import sqlite3
import json


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
