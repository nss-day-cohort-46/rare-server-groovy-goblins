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
            c.label
        FROM posts p
        JOIN users u ON u.id = p.user_id
        JOIN Categories c ON c.id = p.category_id
        """)

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['publication_date'], row['content'],
                        row['approved'])

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
            c.label
        FROM posts p
        JOIN users u ON u.id = p.user_id
        JOIN Categories c ON c.id = p.category_id
        WHERE p.user_id = ?
        """, (user_id))

        posts = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post = Post(row['id'], row['user_id'], row['category_id'],
                        row['title'], row['publication_date'], row['content'],
                        row['approved'])

            author = User(first_name = row['first_name'], last_name = row['last_name'])
            category = Category(row['category_id'], row['label'])

            post.author = author.__dict__
            post.category = category.__dict__

            posts.append(post.__dict__)

    return json.dumps(posts)