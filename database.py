import sqlite3


connection = sqlite3.connect('../pythonProject/posts.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS posts(
              id INTEGER PRIMARY KEY AUTOINCREMENT, 
              title TEXT, 
              story TEXT)''')
connection.commit()
