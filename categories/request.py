import sqlite3
import json

from models import Category


def get_all_categories():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                c.id, 
                c.label,
                c.deleted
            FROM Categories c
        """)

        categories = []

        data = db_cursor.fetchall()

        for row in data:
            category = Category(
                row['id'],
                row['label'],
                row['deleted']
            )
            categories.append(category.__dict__)

    return json.dumps(categories)


def create_category(new_category):

    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Categories( 
            label, deleted
        )
        VALUES ( ?, 0 );
        """, (new_category['label'], ))

        id = db_cursor.lastrowid
        new_category['id'] = id

    return json.dumps(new_category)


def delete_category(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Categories
        SET deleted = 1
        WHERE id = ?
        """, (id, ))
