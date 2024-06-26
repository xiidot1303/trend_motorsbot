from bot.services.language_service import get_word
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)


async def _inline_footer_buttons(update, buttons, back=True, main_menu=True):
    new_buttons = []
    if back:
        new_buttons.append(
            InlineKeyboardButton(text=get_word('back', update), callback_data='back'),
        )
    if main_menu:
        new_buttons.append(
            InlineKeyboardButton(text=get_word('main menu', update), callback_data='main_menu'),
        )

    buttons.append(new_buttons)
    return buttons

async def select_lang_keyboard():
    buttons = [["UZ 🇺🇿", "RU 🇷🇺"]]
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
    return markup

async def settings_keyboard(update):

    buttons = [
        [get_word("change lang", update)],
        [get_word("change name", update)],
        [get_word("change phone number", update)],
        [get_word("main menu", update)],
    ]

    return buttons

async def regions_of_contacts_keyboard(update, regions_list):
    # create buttons list
    buttons_list = [
        InlineKeyboardButton(
            text=await get_word(region, update),
            callback_data=f'contacts_of-{region}'
        )
        for region in regions_list
    ]
    # split list by two cols
    buttons = [
        buttons_list[i:i + 2] 
        for i in range(0, len(buttons_list), 2)]

    reply_markup = InlineKeyboardMarkup(buttons)
    return reply_markup