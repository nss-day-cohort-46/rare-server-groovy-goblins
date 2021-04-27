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
                c.content
            FROM Comments c
        """)

        categories = []

        data = db_cursor.fetchall()

        for row in data:
            category = Comment(
                row['id'], row['post_id'], row['author_id'], row['content']
            )
            categories.append(category.__dict__)

        return json.dumps(categories)


def create_category(new_category):
    """
    CREATE TABLE "Categories" (
        "id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "label" varchar
    );
    INSERT INTO Categories ('label')
    VALUES ('News');
    """

    print("creating new category")
    print(new_category)
    print(type(new_category))
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Categories( 
            label
        )
        VALUES ( ? );
        """, (new_category['label'], ))

        id = db_cursor.lastrowid
        new_category['id'] = id

    return json.dumps(new_category)