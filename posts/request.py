import sqlite3
import json
from models import Post, User, Category


def get_all_posts():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.content,
            p.approved,
            u.first_name,
            u.last_name,
            c.label,
            c.deleted
        FROM posts p
        JOIN users u ON u.id = p.user_id
        JOIN Categories c ON c.id = p.category_id
        WHERE p.approved = 1
        AND p.publication_date < date('now')
        ORDER BY p.publication_date
        """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['publication_date'], row['content'],
                        row['approved'])

            author = User(first_name=row['first_name'],
                          last_name=row['last_name'])
            category = Category(row['category_id'],
                                row['label'], row['deleted'])

            post.author = author.__dict__
            post.category = category.__dict__

            posts.append(post.__dict__)

    return json.dumps(posts)


def get_posts_by_user(user_id):
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id, 
            p.user_id, 
            p.category_id,
            p.title,
            p.publication_date,
            p.content,
            p.approved,
            u.first_name, 
            u.last_name,
            c.label,
            c.deleted
        FROM posts p
        JOIN users u ON u.id = p.user_id
        JOIN Categories c ON c.id = p.category_id
        WHERE p.user_id = ?
        ORDER BY p.publication_date

        """, (user_id))

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['publication_date'], row['content'],
                        row['approved'])

            author = User(first_name=row['first_name'],
                          last_name=row['last_name'])
            category = Category(row['category_id'],
                                row['label'], row['deleted'])

            post.author = author.__dict__
            post.category = category.__dict__

            posts.append(post.__dict__)

    return json.dumps(posts)


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


def delete_post(id):
    print("I never get here")
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            DELETE FROM Posts
            WHERE id = ?
        """, (id, ))
