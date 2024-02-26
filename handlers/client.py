from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

import config
from database.client import User
from database.admin import Chanel
from bot import bot, dp
from keyboard import keyboard

User_db = User()
Chanel_db = Chanel()

@dp.message_handler(commands='start', state='*')
async def start(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    username = message.from_user.username
    await User_db.add_user(user_id, str(username))
    await message.answer('Выбери категорию', reply_markup=keyboard.category_menu())


@dp.callback_query_handler(lambda call: (call.data in config.CATEGORY.values()) or (call.data.startswith('back_')), state='*')
async def get_chanel(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer()
    if call.data.startswith('back_'):
        category = call.data.split('_')[1]
    else:
        category = call.data
    chanels = await Chanel_db.get_all_chanels_category(category)
    if not chanels:
        await call.message.edit_text('В этой категории еще нет каналов\n'
                                     'Для добавления канал писать @khann_tg', reply_markup=keyboard.back_btn())
        return
    text_list = []
    for chanel_id, link, name, price, subs, views in chanels:
        text_list.append(f'<b>Канал:</b> {name} - {link}\n'
                         f'<b>Пдп/охват:</b> {subs}👥 {views}👀\n'
                         f'<b>Цена/спм:</b> {price}руб  {int(round(price/views, 2)*1000)}cpm\n' 
                        f'<b>Стата:</b> /stat_{chanel_id}\n\n')
    n = 5  # Кол-во  в 1 странице
    result = [text_list[i:i + n] for i in range(0, len(text_list), n)]
    for text in result:
        msg_text = ''.join(text) + 'Для покупки писать @khann_tg'
        if result[-1] == text:
            await call.message.answer(msg_text, reply_markup=keyboard.back_btn(), parse_mode='HTML', disable_web_page_preview=True)
        else:
            await call.message.answer(msg_text, parse_mode='HTML', disable_web_page_preview=True)
    #await call.message.edit_text(''.join(text), reply_markup=keyboard.back_btn())

@dp.message_handler(lambda message: message.text.startswith('/stat'))
async def get_stat(message: Message):
    chanel_id = message.text.split('_')[1]
    category = await Chanel_db.get_category(chanel_id)
    link = await Chanel_db.get_link(chanel_id)
    print(chanel_id, category)
    try:
        file = open(f'img/stat_{chanel_id}.jpg', 'rb')
        await message.answer_photo(file, reply_markup=keyboard.telemetr_link(link))
    except:
        pass
    try:
        stat = await Chanel_db.get_stat(chanel_id)
        await message.answer(stat, reply_markup=keyboard.back_temat_btn(category))
    except Exception as e:
        print(e)


@dp.callback_query_handler(lambda call: call.data=='main_menu', state='*')
async def main_menu(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    await call.message.edit_text('Выбери категорию', reply_markup=keyboard.category_menu())