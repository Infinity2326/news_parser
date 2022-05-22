import sqlite3


connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS posts(
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              title TEXT NOT NULL, 
              story TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS rating(
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              score INTEGER NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS comments(
              postid INTEGER NOT NULL, 
              author TEXT NOT NULL,
              text TEXT NOT NULL,
              post_time TEXT NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS users(
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              login TEXT NOT NULL,
              password TEXT NOT NULL)''')
connection.commit()

cursor.execute('''CREATE TABLE IF NOT EXISTS ratingusers(
              vote TEXT NOT NULL,
              user TEXT NOT NULL)''')
connection.commit()
