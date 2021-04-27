import sqlite3
import json


def create_post(new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            ( user_id, category_id, title, publication_date, image_url, content, approved )
        VALUES
            ( ?, ?, ?, DATETIME(), ?, ?, 1);
        """, (
            new_post['user_id'], 
            new_post['category_id'], 
            new_post['title'],
            new_post['image_url'],
            new_post['content'], )
        )

        id = db_cursor.lastrowid
        new_post['id'] = id

    return json.dumps(new_post)


#     CREATE TABLE "Posts" (
#   "id" INTEGER PRIMARY KEY AUTOINCREMENT,
#   "user_id" INTEGER,
#   "category_id" INTEGER,
#   "title" varchar,
#   "publication_date" date,
#   "image_url" varchar,
#   "content" varchar,
#   "approved" bit
# );
