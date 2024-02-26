from aiogram.types import Message, CallbackQuery, ContentType, MediaGroup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

import config
from database.client import User
from database.admin import Chanel
from database.spam import Spam
from bot import  dp
from keyboard import keyboard
from states import states
from telemetr import parse_telemetr
import asyncio
from typing import List, Union
import ast
import time
import threading
Chanel_db = Chanel()
User_db = User()
Spam_db = Spam()

class AlbumMiddleware(BaseMiddleware):
    """This middleware is for capturing media groups."""

    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        """
        You can provide custom latency to make sure
        albums are handled properly in highload.
        """
        self.latency = latency
        super().__init__()

    async def on_process_message(self, message: Message, data: dict):
        if not message.media_group_id:
            return

        try:
            self.album_data[message.media_group_id].append(message)
            raise CancelHandler()  # Tell aiogram to cancel handler for this group element
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            message.conf["is_last"] = True
            data["album"] = self.album_data[message.media_group_id]

    async def on_post_process_message(self, message: Message, result: dict, data: dict):
        """Clean up after handling our album."""
        if message.media_group_id and message.conf.get("is_last"):
            del self.album_data[message.media_group_id]


@dp.message_handler(lambda message: message.from_user.id in config.ADMINS, commands='panel', state='*')
async def show_panel(message: Message, state:FSMContext):
    await state.finish()
    await message.answer('Вот твоя админка', reply_markup=keyboard.admin_panel())


@dp.callback_query_handler(lambda call: (call.from_user.id in config.ADMINS) and (call.data=='stat'), state='*')
async def statistic(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    users = await User_db.get_all_user()
    await call.message.answer(f'Кол-во юзеров: {len(users)}')


@dp.callback_query_handler(lambda call: (call.from_user.id in config.ADMINS) and (call.data=='add_chanel'), state='*')
async def add_chanel(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    await call.message.answer('Пришли мне ссылку на канал')
    await states.ADD_CHANEL.link.set()



@dp.message_handler(state=states.ADD_CHANEL.link)
async def add_chanel2(message: Message, state: FSMContext):
    name = await parse_telemetr.get_name_chanel(message.text)
    if name != '***':
        async with state.proxy() as data:
            data['link'] = message.text
        await states.ADD_CHANEL.next()
        await message.answer('Пришли мне цену рекламы')
    else:
        await message.answer('Что то пошло не так, возможно не коректная ссылка')
        await state.finish()

@dp.message_handler(state=states.ADD_CHANEL.price)
async def add_chanel3(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Теперь пришли мне категорию', reply_markup=keyboard.admin_category_menu())
    await states.ADD_CHANEL.next()

@dp.message_handler(state=states.ADD_CHANEL.category)
async def add_chanel4(message: Message, state: FSMContext):
    category = config.CATEGORY[message.text]
    async with state.proxy() as data:
        link = data['link']
        price = data['price']
        await message.answer('Получаю основные данные канала из api')
        name = await parse_telemetr.get_name_chanel(link)
        subs = await parse_telemetr.get_sub(link)
        views = await parse_telemetr.get_views(link)
        chanel_id = await Chanel_db.get_last_id()
        await message.answer('Получаю статистику канала из телеметра...')
        stat = await parse_telemetr.get_photo_stat_and_sub(chanel_id+1, link)
        await Chanel_db.add_chanel(name, link, price, views, category, subs, stat)
        await message.answer('Канал добавлен')
        await state.finish()

@dp.callback_query_handler(lambda call: (call.from_user.id in config.ADMINS) and (call.data=='del_chanel'), state='*')
async def del_chanel(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    await call.message.answer('Пришли мне id канала.\т\n'
                              'ID канала - это то что стоит на месте "x" в команде /stat_x')
    await states.DEL_CHANEL.chanel_id.set()

@dp.message_handler(state=states.DEL_CHANEL.chanel_id)
async def del_chanel2(message: Message, state: FSMContext):
    await state.finish()
    chanel_id = int(message.text)
    try:
        name = await Chanel_db.get_name(chanel_id)
        await Chanel_db.del_chanel(chanel_id)
        await message.answer(f'Канал {name} удален')
    except Exception as e:
        await message.answer(f'Фатальная ошибка, скорее всего потому что такого канала нету {e}')

@dp.callback_query_handler(lambda call: (call.from_user.id in config.ADMINS) and (call.data=='edit_price'), state='*')
async def edit_price(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer()
    await call.message.answer('Пришли мне id канала.\т\n'
                              'ID канала - это то что стоит на месте "x" в команде /stat_x')
    await states.EDIT_PRICE.chanel_id.set()

@dp.message_handler(state=states.EDIT_PRICE.chanel_id)
async def edit_price2(message: Message, state: FSMContext):
    try:
        chanel_id = int(message.text)
        await message.answer('Пришли мне новый прайс')
        async with state.proxy() as data:
            data['chanel_id'] = chanel_id
        await states.EDIT_PRICE.next()
    except Exception as e:
        await message.answer(f'Фатальная ошибка {e}')


@dp.message_handler(state=states.EDIT_PRICE.price)
async def edit_price3(message: Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            chanel_id = data['chanel_id']
            await Chanel_db.edit_price(chanel_id, int(message.text))
            await message.answer('Прайс изменен')
            await state.finish()
    except Exception as e:
        await message.answer(f'Фатальная ошибка {e}')


@dp.callback_query_handler(lambda call: (call.data=='spam') and (call.from_user.id  in config.ADMINS), state='*')
async def spam1(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    user_id = call.from_user.id
    if user_id in config.ADMINS:
        await call.message.answer('Пришли пост')
        await states.FSM_ADMIN_SPAM.text.set()

@dp.message_handler(state=states.FSM_ADMIN_SPAM.text, is_media_group=True, content_types=ContentType.ANY,)
async def spam2_media_group(message: Message, album: List[Message], state: FSMContext):
    """This handler will receive a complete album of any type."""
    media_group = MediaGroup()
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        try:
            # We can also add a caption to each file by specifying `"caption": "text"`
            media_group.attach({"media": file_id, "type": obj.content_type, "caption": obj.caption,
                                "caption_entities": obj.caption_entities})
        except ValueError:
            return await message.answer("This type of album is not supported by aiogram.")
    media_group = ast.literal_eval(str(media_group))
    async with state.proxy() as data:
        try:
            data['text'] = media_group[0]['caption']
        except:
            data['text'] = 'None'
        data['media'] = media_group
        await Spam_db.add_spam(data['text'], 'None', str(media_group))
    last_id = await Spam_db.select_last_id()
    await message.answer_media_group(media_group)
    await message.answer(f'Пришли команду /sendspam_{last_id} чтоб начать рассылку')
    await state.finish()

@dp.message_handler(state=states.FSM_ADMIN_SPAM.text, content_types=['photo', 'video', 'animation', 'text'])
async def spam2(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        if message.content_type in ('photo', 'video', 'animation'):
            async with state.proxy() as data:
                try:
                    data['text'] = message.html_text
                except:
                    data['text'] = None
                if message.content_type == 'photo':
                    data['media'] = ('photo', message.photo[-1].file_id)
                else:
                    data['media'] = (message.content_type, message[message.content_type].file_id)
        else:
            async with state.proxy() as data:
                data['text'] = message.html_text
                data['media'] = 'None'
        await message.answer('Теперь пришли кнопки например\n'
                             'text - url1\n'
                             'text2 - url2 && text3 - url3\n\n'
                             'text - надпись кнопки url - ссылка'
                             '"-" - разделитель\n'
                             '"&&" - склеить в строку\n'
                             'ЕСЛИ НЕ НУЖНЫ КНОПКИ ОТПРАВЬ 0')
        await states.FSM_ADMIN_SPAM.next()

@dp.message_handler(state=states.FSM_ADMIN_SPAM.btns)
async def spam3(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        if message.text != '0':
            # конструктор кнопок
            try:
                buttons = []
                for char in message.text.split('\n'):
                    if '&&' in char:
                        tmpl = []
                        for i in char.split('&&'):
                            tmpl.append(dict([i.split('-', maxsplit=1)]))
                        buttons.append(tmpl)
                    else:
                        buttons.append(dict([char.split('-', maxsplit=1)]))
                menu = InlineKeyboardMarkup()
                btns_list = []
                items = []
                for row in buttons:
                    if type(row) == dict:
                        url1 = str(list(row.items())[0][1]).strip()
                        text1 = list(row.items())[0][0]
                        menu.add(InlineKeyboardButton(text=text1, url=url1))
                    else:
                        items.clear()
                        btns_list.clear()
                        for d in row:
                            items.append(list(d.items())[0])
                        for text, url in items:
                            url = url.strip()
                            btns_list.append(InlineKeyboardButton(text=text, url=url))
                        menu.add(*btns_list)
                ###########$##############
                async with state.proxy() as data:
                    data['btns'] = str(menu)
                    media = data['media']
                    text = data['text']
                    await Spam_db.add_spam(text, str(menu), str(media))

                    if media != 'None':
                        content_type = media[0]
                        if content_type == 'photo':
                            await message.bot.send_photo(user_id, media[1], caption=text, parse_mode='HTML',
                                                         reply_markup=menu)
                        elif content_type == 'video':
                            await message.bot.send_video(user_id, media[1], caption=text, parse_mode='HTML',
                                                         reply_markup=menu)
                        elif content_type == 'animation':
                            await message.bot.send_animation(user_id, media[1], caption=text, parse_mode='HTML',
                                                             reply_markup=menu)
                    else:
                        await message.answer(text, reply_markup=menu, parse_mode='HTML', disable_web_page_preview=True)

            except Exception as e:
                await message.reply(f'Похоже что непрвильно введена клавиатура')
        else:
            async with state.proxy() as data:
                data['btns'] = 'None'
                media = data['media']
                text = data['text']
                await Spam_db.add_spam(text, 'None', str(media))


                if media != 'None':
                    content_type = media[0]
                    if content_type == 'photo':
                        await message.bot.send_photo(user_id, media[1], caption=text, parse_mode='HTML')
                    elif content_type == 'video':
                        await message.bot.send_video(user_id, media[1], caption=text, parse_mode='HTML')
                    elif content_type == 'animation':
                        await message.bot.send_animation(user_id, media[1], caption=text, parse_mode='HTML')
                else:
                    await message.answer(text, parse_mode='HTML', disable_web_page_preview=True)
        last_id = await Spam_db.select_last_id()
        await message.answer(f'Пришли команду /sendspam_{last_id} чтоб начать рассылку')
        await state.finish()

@dp.message_handler(lambda message: (message.from_user.id in config.ADMINS) and (message.text.startswith('/sendspam')))
async def start_spam(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        spam_id = int(message.text.replace('/sendspam_', ''))
        text = await Spam_db.select_text(spam_id)
        keyboard = await Spam_db.select_keyboard(spam_id)
        media = await Spam_db.select_media(spam_id)
        if text == 'None':
            text = None
        if keyboard == 'None':
            keyboard = None
        all_user = await User_db.get_all_user()
        await message.answer(f'Считанно {len(all_user)} пользователей запускаю рассылку')
        no_send = 0
        send = 0
        for user in all_user:
            user = int(user)
            try:
                if media != 'None' and media != None:  # Есть медиа
                    if type(media) is list:
                        await message.bot.send_media_group(user, media)
                    else:
                        content_type = media[0]

                        if content_type == 'photo':
                            await message.bot.send_photo(user, media[1], caption=text, parse_mode='HTML',
                                                         reply_markup=keyboard)
                        elif content_type == 'video':
                            await message.bot.send_video(user, media[1], caption=text, parse_mode='HTML',
                                                         reply_markup=keyboard)
                        elif content_type == 'animation':
                            await message.bot.send_animation(user, media[1], caption=text, parse_mode='HTML',
                                                             reply_markup=keyboard)

                else:  # Нету медиа
                    if keyboard != 'None' and keyboard != None:  # Есть кнопки
                        await message.bot.send_message(chat_id=user, text=text, reply_markup=keyboard,
                                                       parse_mode='HTML', disable_web_page_preview=True)
                    else:
                        await message.bot.send_message(chat_id=user, text=text, parse_mode='HTML',
                                                       disable_web_page_preview=True)
                send += 1

            except:
                no_send += 1
        await message.answer(f'Рассылка окончена.\n'
                             f'Отправленно: {send} пользователям\n'
                             f'Не отправленно: {no_send} пользователям')


dp.middleware.setup(AlbumMiddleware())