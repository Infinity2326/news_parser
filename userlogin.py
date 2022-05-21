import sqlite3


connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()

def getUser(self, user_id):
    try:
        self.cursor.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
        newId = self.cursor.fetchone()
        if not newId:
            return False

        return newId

    except sqlite3.Error as e:
        print(e)

class UserLogin():
    def from_database(self, user_id):
        self.__user = getUser(user_id)
        
        return self

    def create_user(self, user):
        self.__user = user
        print(type(self.__user), self.__user)
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user['id'])