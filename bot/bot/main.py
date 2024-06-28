from bot.bot import *
from bot.services.contact_service import list_of_regions_of_contacts, get_contact_by_region
from bot.bot.TO import to_the_getting_brand_name as _to_the_getting_brand_name
from bot.bot.feedback import to_the_getting_name as _to_the_getting_name
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

async def contact(update: Update, context: CustomContext):
    # get list of regions of contacts
    regions_list = await list_of_regions_of_contacts()
    markup = await regions_of_contacts_keyboard(update, regions_list)
    text = await get_word('select region of contact', update)
    await update_message_reply_text(
        update,
        text,
        reply_markup=markup
    )

async def contacts_of_region(update: Update, context: CustomContext):
    query = update.callback_query
    data = query.data
    *args, region_title = data.split("-")
    contact: Contact = await get_contact_by_region(region_title)
    await bot_edit_message_text(query, context, contact.value)

async def social_networks(update: Update, context: CustomContext):
    text = await get_social_networks_text()
    await update_message_reply_text(update, text)

async def TO(update: Update, context: CustomContext):
    return await _to_the_getting_brand_name(update)

async def feedback(update: Update, context: CustomContext):
    return await _to_the_getting_name(update, context)