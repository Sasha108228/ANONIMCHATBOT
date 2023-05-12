import sqlite3


class Database:

    def __init__(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
        self.name = ' '



#----------------------------------------------------------------------------------------------------------------

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

#----------------------------------------------------------------------------------------------------------------

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))

#----------------------------------------------------------------------------------------------------------------


    def set_name(self, user_id, name):
        with self.connection:
            return self.cursor.execute("UPDATE users SET name = ? WHERE user_id = ?", (name, user_id,))

#----------------------------------------------------------------------------------------------------------------


    def get_name(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT name FROM users WHERE user_id = ?", (user_id,)).fetchall()
            for row in result:
                name = str(row[0])
            return name

#----------------------------------------------------------------------------------------------------------------

    def set_age(self, user_id, age):
        with self.connection:
            return self.cursor.execute("UPDATE users SET age = ? WHERE user_id = ?", (age, user_id,))


    def get_age(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT age FROM users WHERE user_id = ?", (user_id,)).fetchall()

            for row in result:
                age = str(row[0])
            return age


#----------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------

    def set_text(self, user_id, text):
        with self.connection:
            return self.cursor.execute("UPDATE users SET text = ? WHERE user_id = ?", (text, user_id,))

    def get_text(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT text FROM users WHERE user_id = ?", (user_id,)).fetchall()

            for row in result:
                text = str(row[0])
            return text

#----------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------

    def set_gender(self, user_id, gender):
        with self.connection:
            return self.cursor.execute("UPDATE users SET gender = ? WHERE user_id = ?", (gender, user_id,))

    def get_gender(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT gender FROM users WHERE user_id = ?", (user_id,)).fetchall()

            for row in result:
                gender = str(row[0])
            return gender



#----------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------

    def null_block(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET block=0 WHERE user_id=?", (user_id,))

    def set_block(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET block=1 WHERE user_id =?", (user_id,))

    def get_block(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT block FROM users WHERE user_id = ?", (user_id,)).fetchone()

            return result[0]
            # return int(result[0])

            # return bool(result)

            # for row in result:
            #     global blocking
            #     blocking = int(row[0])
            # return blocking


#----------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------

    def null_num_chats(self, user_id):
        with self.connection:
            #cursor.execute("INSERT INTO likes_dislikes likes = ?, dislikes = ? WHERE user_id = ? ", (0, 0, user_id,))
            return self.cursor.execute("UPDATE users SET num_chats=? WHERE user_id=?", (0, user_id,))

    def set_num_chats(self, user_id, num_chats):
        with self.connection:
            return self.cursor.execute("UPDATE users SET num_chats=? WHERE user_id = ?", (num_chats, user_id,))

    def get_num_chats(self, user_id):
        with self.connection:
            num_chat = self.cursor.execute("SELECT num_chats FROM users WHERE user_id = ?", (user_id,))
            chats = num_chat.fetchone()[0]
            num_chats = int(chats)
            return num_chats

    def get_top_num_chats(self):
        with self.connection:
            result = self.cursor.execute("SELECT name, num_chats FROM users ORDER BY num_chats DESC").fetchmany(10)
            #dict_result = dict(result)
            #return dict_result
            # output_str = ""
            # for row in result:
            #     output_str += "{0}: {1}\n".format(row[0], row[1])
            #     print(output_str)
            #     return ("{0}: {1}".format(row[0], row[1]))
            # i=1
            # output_list = ["{0}) {1}: {2}".format(i+1, row[0], row[1]) for row in result]
            # output_str = "\n".join(output_list)
            output_str = "\n".join(["{0}) {1}: {2} Диалога/ов".format(i+1, row[0], row[1]) for i, row in enumerate(result)])
            return output_str

            # # Создание пустых списков
            # keys = []
            # values = []
            # # Извлечение ключей и значений из картежа
            # for item in result:
            #     key, value = item
            #     keys.append(key)
            #     values.append(value)
            # return keys, values


#----------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------

    def null_like_dislike(self, user_id):
        with self.connection:
            #cursor.execute("INSERT INTO likes_dislikes likes = ?, dislikes = ? WHERE user_id = ? ", (0, 0, user_id,))
            return self.cursor.execute("UPDATE users SET likes=?, dislikes=? WHERE user_id=?", (0, 0, user_id,))


    def set_likes(self, user_id, likes):
        with self.connection:
            return self.cursor.execute("UPDATE users SET likes=? WHERE user_id = ?", (likes, user_id,))

    def set_dislikes(self, user_id, dislikes):
        with self.connection:
            return self.cursor.execute("UPDATE users SET dislikes=? WHERE user_id = ?", (dislikes, user_id,))

    def get_like(self, partner):
        with self.connection:
            ratel = self.cursor.execute("SELECT likes FROM users WHERE user_id = ?", (partner,))
            like = ratel.fetchone()[0]
            likes = int(like)
            return likes

    def get_dislike(self, partner):
        with self.connection:
            rated = self.cursor.execute("SELECT likes, dislikes FROM users WHERE user_id = ?", (partner,))
            dislike = rated.fetchone()[1]
            dislikes = int(dislike)
            return dislikes

#----------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------

    def get_users(self):
        with self.connection:
            result = self.cursor.execute("SELECT user_id FROM users").fetchall()
            return result

#----------------------------------------------------------------------------------------------------------------

    def add_queue(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO queue (user_id) VALUES (?)", (user_id,))

#----------------------------------------------------------------------------------------------------------------


    def delete_queue(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM queue WHERE user_id = ?", (user_id,))

#----------------------------------------------------------------------------------------------------------------


    def get_queue(self):
        with self.connection:
            queue = self.cursor.execute("SELECT * FROM queue").fetchmany(1)

            if bool(len(queue)):
                for row in queue:
                    return row[1]
            else:
                return False

#----------------------------------------------------------------------------------------------------------------


    def create_chat(self, user_id, partner_id):
        if partner_id != 0:
            with self.connection:
                self.cursor.execute("INSERT INTO chats (user, partner) VALUES (?, ?)", (user_id, partner_id))
                return True

        return False

#----------------------------------------------------------------------------------------------------------------


    def get_chat(self, user_id):
        with self.connection:
            chat = self.cursor.execute("SELECT * FROM chats WHERE user = ? OR partner = ?", (user_id, user_id))

            for i in chat:
                return [i[0], i[1] if i[1] != user_id else i[2]]

            return False

#----------------------------------------------------------------------------------------------------------------


    def delete_chat(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM chats WHERE user = ? OR partner = ?", (user_id, user_id))