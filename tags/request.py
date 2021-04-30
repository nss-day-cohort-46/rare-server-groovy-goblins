import sqlite3
import json


def create_tag(new_tag):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Tags
            ( label )
        VALUES
            ( ? )
        """, (new_tag['label'], ))

        id = db_cursor.lastrowid
        new_tag['id'] = id
    
    return json.dumps(new_tag)

def update_tag(id, new_tag):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Tags
            SET
                label = ?
        WHERE id = ?
        """, ( new_tag['label'], id ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True

def add_tag_to_post(obj):
    post_id = obj['post_id']
    tag_id = obj['tag_id']

    with sqlite3.connect("./rare.db") as conn:

        db_cursor = conn.cursor()

        db_cursor.execute("""
            INSERT INTO PostTags (post_id, tag_id)
            VALUES(?, ?);
        """, (post_id, tag_id))

        id = db_cursor.lastrowid

        obj['id'] = id
    return json.dumps(obj)
