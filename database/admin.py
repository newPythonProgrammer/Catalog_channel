import asyncio
import aiomysql
import config


class Chanel:
    async def add_chanel(self, name, link, price, views, category, subs, stat):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''INSERT INTO chanel(Link, Name, Category, Price, Subs, Views, Stat) VALUES (%s, %s, %s, %s, %s, %s, %s)''', (link, name, category, price, subs, views, stat))
        await connect.commit()
        connect.close()

    async def edit_price(self, chanel_id, price):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE chanel SET Price = %s WHERE Id = %s''', (price, chanel_id))
        await connect.commit()
        connect.close()

    async def edit_subs(self, chanel_id, subs):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE chanel SET Subs = %s WHERE Id = %s''', (subs, chanel_id))
        await connect.commit()
        connect.close()

    async def edit_views(self, chanel_id, views):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE chanel SET Views = %s WHERE Id = %s''', (views, chanel_id))
        await connect.commit()
        connect.close()

    async def edit_stat(self, chanel_id, stat):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''UPDATE chanel SET Stat = %s WHERE Id = %s''', (stat, chanel_id))
        await connect.commit()
        connect.close()

    async def get_stat(self, chanel_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Stat FROM chanel WHERE Id = %s''', (chanel_id,))
        data = await cursor.fetchone()
        return str(data[0])

    async def del_chanel(self, chanel_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''DELETE FROM chanel WHERE Id = %s''', (chanel_id,))
        await connect.commit()
        connect.close()

    async def get_all_chanels_category(self, category):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT * FROM chanel WHERE Category = %s''', (category,))
        data = await cursor.fetchall()
        connect.close()
        result = []
        for i in data:
            result.append([int(i[0]), str(i[1]), str(i[2]), int(i[4]), int(i[5]), int(i[6])])
        return result

    async def get_all_chanels(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT * FROM chanel''')
        data = await cursor.fetchall()
        connect.close()
        result = []
        for i in data:
            result.append([int(i[0]), str(i[1])])
        return result

    async def get_last_id(self):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Id FROM chanel''', )
        data = await cursor.fetchall()
        print(data)
        try:
            connect.close()
            return int(data[-1][0])
        except:
            await cursor.execute('''ALTER TABLE telemetr_bot.chanel AUTO_INCREMENT = 1''', )
            await connect.commit()
            connect.close()
            return 0

    async def get_name(self, chanel_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Name FROM chanel WHERE Id = %s''', (chanel_id,))
        data = await cursor.fetchone()
        return str(data[0])

    async def get_category(self, chanel_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Category FROM chanel WHERE Id = %s''', (chanel_id,))
        data = await cursor.fetchone()
        return int(data[0])

    async def get_link(self, chanel_id):
        connect: aiomysql.connection.Connection = await aiomysql.connect(host='127.0.0.1', user=config.MYSQL_USER,
                                                                         password=config.MYSQL_PASSWORD,
                                                                         db=config.MYSQL_DATABASE)
        cursor: aiomysql.cursors.Cursor = await connect.cursor()
        await cursor.execute('''SELECT Link FROM chanel WHERE Id = %s''', (chanel_id,))
        data = await cursor.fetchone()
        return data[0]

# loop = asyncio.get_event_loop()
# chanel = Chanel()
# # loop.run_until_complete(chanel.add_chanel('name', 'link', 1,2,3,4,'stat'))
# print(loop.run_until_complete(chanel.get_stat(11)))
