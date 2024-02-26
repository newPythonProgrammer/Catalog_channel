import asyncio
import aiomysql
import config
import ast

class Spam:
    async def add_spam(self, text, keyboard, media):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''INSERT INTO spam(Text, Keyboard, Media) VALUES(%s, %s, %s)''', (text, keyboard, media))
        await connect.commit()
        connect.close()

    async def select_text(self, spam_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Text FROM spam WHERE Id = %s''', (spam_id,))
        result = await cursor.fetchone()
        connect.close()
        return result[0]

    async def select_keyboard(self, spam_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Keyboard FROM spam WHERE Id = %s''', (spam_id,))
        result = await cursor.fetchone()
        connect.close()
        try:
            return ast.literal_eval(result[0])
        except:
            return None

    async def select_media(self, spam_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Media FROM spam WHERE Id = %s''', (spam_id,))
        result = await cursor.fetchone()
        connect.close()
        try:
            return ast.literal_eval(result[0])
        except:
            return None


    async def select_last_id(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Id FROM spam''', )
        data = await cursor.fetchall()
        return int(data[-1][0])