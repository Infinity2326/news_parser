import sqlite3


connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS posts(
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              title TEXT, 
              story TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS rating(
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              score INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS comments(
              postid INTEGER, 
              author TEXT,
              text TEXT,
              post_time TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS users(
              login TEXT,
              password TEXT)''')
connection.commit()
