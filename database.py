import sqlite3


connection = sqlite3.connect('posts.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS posts(
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              title TEXT, 
              story TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS rating(
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              score INTEGER)''')
connection.commit()
