from bot.bot import *

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await is_group(update):
        return
    
    if await is_registered(update.message.chat.id):
        # main menu
        return
    else:
        # await get_or_create(user_id=update.message.chat.id)
        # obj = await get_object_by_user_id(user_id=update.message.chat.id)
        # obj.lang = "uz"
        # await obj.asave()
        # return 
        hello_text = lang_dict['hello']
        await update_message_reply_text(
            update,
            hello_text,
            reply_markup= await select_lang_keyboard()
        )
        return GET_LANG