from models.comment import Comment
import sqlite3
import json



def get_all_comments():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                c.id, 
                c.post_id, 
                c.author_id, 
                c.content,
                c.created_on
            FROM Comments c
        """)

        comments = []

        data = db_cursor.fetchall()

        for row in data:
            comment = Comment(
                row['id'], row['post_id'], row['author_id'], row['content'], row['created_on']
            )
            comments.append(comment.__dict__)

        return json.dumps(comments)


def create_comment(new_comment):

    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Comments( 
            post_id, author_id, content, created_on
        )
        VALUES ( ?, ?, ?, DATETIME() );
        """, (new_comment['post_id'], new_comment['author_id'], new_comment['content'], ))

        id = db_cursor.lastrowid
        new_comment['id'] = id

    return json.dumps(new_comment)