import aiomysql
import config


class User:
    async def add_user(self, user_id, username):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT * FROM user WHERE Id = %s''', (user_id,))
        check = await cursor.fetchone()
        if not bool(check):
            await cursor.execute('''INSERT INTO user VALUES(%s, %s, CURRENT_DATE())''', (user_id, username))
            await connect.commit()
        connect.close()

    async def get_all_user(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT ID FROM user''')
        result = await cursor.fetchall()

        user_ids = [int(row[0]) for row in result]
        connect.close()
        return user_ids




