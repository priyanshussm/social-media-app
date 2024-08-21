import sqlite3

connection = sqlite3.connect('project\database.db')


with open('project\schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content, email) VALUES (?, ?, ?)",
            ('First Post', 'Content for the first post', 'admin')
            )

cur.execute("INSERT INTO posts (title, content, email) VALUES (?, ?, ?)",
            ('Second Post', 'Content for the second post', 'admin')
            )

connection.commit()
connection.close()