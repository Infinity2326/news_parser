import sqlite3


connection = sqlite3.connect('posts.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS posts(
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              title TEXT, 
              story TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS rating(
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              score INTEGER)''')
connection.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS comments(
              postid INTEGER, 
              author TEXT,
              text TEXT,
              post_time TEXT)''')
connection.commit()
