from telegram import Update
from telegram.ext import ContextTypes, CallbackContext, ExtBot
from dataclasses import dataclass
from asgiref.sync import sync_to_async
from bot.utils import *
from bot.utils.bot_functions import *
from bot.utils.keyboards import *
from bot.resources.strings import lang_dict
from bot.services import *
from bot.services.language_service import *
from bot.resources.conversationList import *
from config import WEBAPP_URL

@dataclass
class WebhookUpdate:
    """Simple dataclass to wrap a custom update type"""
    user_id: int
    payload: str

class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    @classmethod
    def from_update(
        cls,
        update: object,
        application: "Application",
    ) -> "CustomContext":
        if isinstance(update, WebhookUpdate):
            return cls(application=application, user_id=update.user_id)
        return super().from_update(update, application)


async def is_message_back(update: Update):
    if update.message.text == await get_word("back", update):
        return True
    else:
        return False

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update = update.callback_query if update.callback_query else update

    bot = context.bot
    buy_car_button = KeyboardButton(
        text=await get_word('order car', update),
        web_app=WebAppInfo(url=WEBAPP_URL)
    )
    trade_in_button = KeyboardButton(
        text=await get_word('trade in', update),
        web_app=WebAppInfo(url='https://trendmotors.uz/trade-in')
    )
    contacts_button = await get_word('contacts', update)
    social_networks_button = await get_word('social_networks', update)
    TO_button = await get_word('TO', update)
    feedback_button = await get_word('feedback', update)
    auth_button = await get_word('auth', update)
    profile_button = await get_word('my_profile', update)

    user = await Bot_user.objects.aget(user_id=update.message.from_user.id)

    keyboards = [
        [buy_car_button, trade_in_button],
        [TO_button, social_networks_button],
        [contacts_button, feedback_button],
        [profile_button if user.one_c_id else auth_button]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard=keyboards, resize_keyboard=True)
    await bot.send_message(
        update.message.chat_id,
        await get_word('main menu', update),
        reply_markup=reply_markup
    )

    await check_username(update)