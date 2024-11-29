import asyncio

from bot.bot import *
from bot.resources.conversationList import AUTH_PASSPORT, AUTH_CODE

from app.services.one_c_sync import one_api
from bot.models import Bot_user
from bot.bot.main import main_menu

sync_tasks = []


async def to_auth(update: Update, context: CustomContext):
    user = await Bot_user.objects.aget(user_id=update.message.chat.id)
    if user.one_c_id:
        await main_menu(update, context)
        return

    text = await get_word('auth_passport', user=user)
    markup = await build_keyboard(update, [], 2, back_button=False)
    await bot_send_message(update, context, text, reply_markup=markup)
    return AUTH_PASSPORT


async def check_code(update: Update, context: CustomContext):
    user = await Bot_user.objects.aget(user_id=update.message.chat.id)
    if update.message.text and len(update.message.text) == 9 and update.message.text[2:].isdigit():
        context.user_data['passport'] = update.message.text
        text = await get_word("auth_code", user=user)
        await bot_send_message(update, context, text)
        return AUTH_CODE

    else:
        text = await get_word('wrong_format', user=user)
        await bot_send_message(update, context, text)


async def check_passport(update: Update, context: CustomContext):
    user: Bot_user = await Bot_user.objects.aget(user_id=update.message.chat.id)
    if update.message.text.isdigit():
        passport = context.user_data['passport']
        try:
            info = await one_api.get_contragent(update.message.text)
            if info.get("passport_sn") == passport:
                text = await get_word("auth_success", user=user)
                user.one_c_id = update.message.text
                await user.asave()
                await bot_send_message(update, context, text)
                sync_tasks.append(asyncio.create_task(one_api.sync_contracts(context.bot, users=[user])))

            else:
                text = await get_word('incorrect_auth', user=user)
                await bot_send_message(update, context, text)

        except Exception as e:
            text = await get_word('auth_error', user=user)
            await bot_send_message(update, context, text)

        await main_menu(update, context)
        return ConversationHandler.END

    else:
        text = await get_word('wrong_format', user=user)
        await bot_send_message(update, context, text)
