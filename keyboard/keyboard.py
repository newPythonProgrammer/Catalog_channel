from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import config

def category_menu():
    menu = InlineKeyboardMarkup(row_width=1)
    for categoty in config.CATEGORY.keys():
        menu.add(InlineKeyboardButton(text=categoty, callback_data=config.CATEGORY[categoty]))
    return menu

def admin_category_menu():
    menu = ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
    for categoty in config.CATEGORY.keys():
        menu.add(KeyboardButton(text=categoty))
    return menu

def back_btn():
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text='Назад', callback_data='main_menu')
    menu.add(btn1)
    return menu

def back_temat_btn(temat):
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text='Назад', callback_data=f'back_{temat}')
    menu.add(btn1)
    return menu

def admin_panel():
    menu = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text='Статистика', callback_data='stat')
    btn2 = InlineKeyboardButton(text='Рассылка', callback_data='spam')
    btn3 = InlineKeyboardButton(text='Добавить канал', callback_data='add_chanel')
    btn4 = InlineKeyboardButton(text='Удалить канал', callback_data='del_chanel')
    btn5 = InlineKeyboardButton(text='Изменить прайс', callback_data='edit_price')
    menu.add(btn1, btn2, btn3, btn4, btn5)
    return menu

def telemetr_link(link):
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text='Подробная статистика', url=f'https://telemetr.me/analytics/?name={link}')
    menu.add(btn1)
    return menu