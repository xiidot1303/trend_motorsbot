from bot.bot import *
import json

async def start(update: Update, context: CustomContext):
    if await is_group(update):
        return
    
    if await is_registered(update.message.chat.id):
        # main menu
        await main_menu(update, context)
        return
    else:
        hello_text = lang_dict['hello']
        await update_message_reply_text(
            update,
            hello_text,
            reply_markup= await select_lang_keyboard()
        )
        return GET_LANG

async def web_app_data(update: Update, context: CustomContext) -> None:
    data = json.loads(update.effective_message.web_app_data.data)
    print(data)
    await update_message_reply_text(update, "received data")