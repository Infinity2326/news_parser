import sqlite3


connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()


def getUser(user_id):
    try:
        cursor.execute(f'SELECT login FROM users WHERE login="{user_id}"')
        newId = cursor.fetchone()
        if not newId:
            return False

        try:
            newId = newId[0]
        except:
            pass
        
        return newId

    except sqlite3.Error as e:
        print(e)



class UserLogin():
    def from_database(self, user_id):
        self.__user = getUser(user_id)
        return self

    def create_user(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        user = self.__user
        return str(user)