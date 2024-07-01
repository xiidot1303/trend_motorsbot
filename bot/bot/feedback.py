from bot.bot import *
import asyncio
from app.services import amocrm_service as amocrm

async def start(update: Update, context: CustomContext):
    await main_menu(update, context)
    return ConversationHandler.END

async def to_the_getting_name(update: Update, context: CustomContext):
    text = await get_word('type name', update)
    markup = await build_keyboard(update, [], 2, back_button=False)
    await bot_send_message(update, context, text, reply_markup=markup)
    return GET_NAME

async def _to_the_getting_contact(update: Update):
    text = await get_word('send number', update)
    i_contact = KeyboardButton(
        text=await get_word("leave number", update),
        request_contact=True
    )
    markup = await build_keyboard(update, [i_contact], 2)
    await update_message_reply_text(update, text, reply_markup=markup)
    return GET_CONTACT

async def _to_the_getting_message(update: Update):
    text = await get_word('write your feedback', update)
    markup = await build_keyboard(update, [], 2)
    await update_message_reply_text(update, text, reply_markup=markup)
    return GET_FEEDBACK_MESSAGE

###############################################################################################

async def get_name(update: Update, context: CustomContext):
    # get name of user from message text
    name = update.message.text
    # save it to user data
    context.user_data['name'] = name
    return await _to_the_getting_contact(update)

async def get_contact(update: Update, context: CustomContext):
    if await is_message_back(update):
        return await to_the_getting_name(update, context)
    
    # get contact of user from message text or message contact
    if c := update.message.contact:
        contact = c.phone_number
    else:
        contact = update.message.text
    context.user_data['contact'] = contact
    # collect all data of the statement from user data

    return await _to_the_getting_message(update)

async def get_message(update: Update, context: CustomContext):
    if await is_message_back(update):
        return await _to_the_getting_contact(update)
    
    # get feedback message of user from message text
    message = update.message.text
    feedback = f"{lang_dict['message of user'][1]}:\n{message}"
    context.user_data['feedback'] = feedback

    # get bot user
    bot_user: Bot_user = await get_object_by_user_id(update.message.chat.id)
    ## send statement to amo crm that create lead
    asyncio.create_task(
        create_lead_in_amocrm(bot_user, context)
    )

    # send last message
    await update_message_reply_text(
        update, 
        await get_word('thanks wait call', update)
        )
    await main_menu(update, context)
    return ConversationHandler.END

async def create_lead_in_amocrm(bot_user: Bot_user, context: CustomContext):
    # create contact in amocrm if not created in the past
    data = context.user_data
    name, contact, feedback = data['name'], data['contact'], data['feedback']
    contact_id = await amocrm.create_simple_contact(
        name, contact
    )

    # create lead
    lead_obj: amocrm.Lead = amocrm.Lead(pipeline_id=7492114)
    lead_id = await lead_obj.create_lead()

    # link contact to lead
    await amocrm.link_contact_to_lead(lead_id=lead_id, contact_id=contact_id)
    
    # add note to lead
    await amocrm.create_note(lead_id, feedback)