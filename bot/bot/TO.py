from bot.bot import *
from app.services.product_service import *
from bot.services.contact_service import list_of_regions_of_contacts
from app.services import amocrm_service as amocrm
import asyncio

async def start(update: Update, context: CustomContext):
    await main_menu(update, context)
    return ConversationHandler.END

async def to_the_getting_brand_name(update: Update):
    brands_list = await list_of_brands_of_products()
    markup = await build_keyboard(update, brands_list, 2, back_button=False)
    text = await get_word('about TO and select brand', update)
    await update_message_reply_text(update, text, reply_markup=markup)
    return GET_BRAND_NAME

async def _to_the_getting_model_name(update: Update, context: CustomContext):
    # get brand from user_data 
    brand = context.user_data['brand']
    # get list of models of this brand
    models_list = await list_of_models_of_products_by_brand(brand)
    # create keyboard markup using this list of models
    markup = await build_keyboard(update, models_list, 2)
    text = await get_word('select model', update)
    await update_message_reply_text(update, text, reply_markup=markup)
    return GET_MODEL_NAME

async def _to_the_getting_region(update: Update):
    # get list of regions of branches and translate they to lang of user
    regions_list = [
        await get_word(region, update)
        for region in await list_of_regions_of_contacts()
        ]
    # create keyboard markup using this list of regions
    markup = await build_keyboard(update, regions_list, 2)
    text = await get_word('select region', update)
    await update_message_reply_text(update, text, reply_markup=markup)
    return GET_REGION

async def _to_the_getting_name(update: Update, context: CustomContext):
    text2 = await get_word('type name', update)
    markup = await build_keyboard(update, [], 2)
    await bot_send_message(update, context, text2, reply_markup=markup)
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

############################################################################################################################

async def get_brand_name(update: Update, context: CustomContext):
    # get brand name form message text
    brand = update.message.text
    # save brand name to user data
    context.user_data['brand'] = brand
    return await _to_the_getting_model_name(update, context)

async def get_model_name(update: Update, context: CustomContext):
    if await is_message_back(update):
        return await to_the_getting_brand_name(update)
    model = update.message.text
    context.user_data['model'] = model
    return await _to_the_getting_region(update)

async def get_region(update: Update, context: CustomContext):
    if await is_message_back(update):
        return await _to_the_getting_model_name(update, context)

    # get region from message text
    region = update.message.text
    # save it to user data
    context.user_data['region'] = region

    # send message that leave your contacts and we will connect you for support
    text1 = await get_word('leave your contacts and we will connect you', update)
    await update_message_reply_text(update, text1)

    return await _to_the_getting_name(update, context)

async def get_name(update: Update, context: CustomContext):
    if await is_message_back(update):
        return await _to_the_getting_region(update)

    # get name of user from message text
    name = update.message.text
    # save it to user data
    context.user_data['name'] = name

    return await _to_the_getting_contact(update)

async def get_contact(update: Update, context: CustomContext):
    if await is_message_back(update):
        return await _to_the_getting_name(update, context)
    
    # get contact of user from message text or message contact
    if c := update.message.contact:
        contact = c.phone_number
    else:
        contact = update.message.text
    context.user_data['contact'] = contact
    # collect all data of the statement from user data

    # get bot user
    bot_user: Bot_user = await get_object_by_user_id(update.message.chat.id)
    # send statement to amo crm that create lead
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
    brand, model, region, name, contact = data['brand'], data['model'], data['region'], data['name'], data['contact'], 
    contact_id = await amocrm.create_simple_contact(
        name, contact
    )

    # create lead
    lead_obj: amocrm.Lead = amocrm.Lead(pipeline_id=8282930)
    await lead_obj.set_data_for_8282930(
        brand, model, region
    )
    lead_id = await lead_obj.create_lead()

    # link contact to lead
    await amocrm.link_contact_to_lead(lead_id=lead_id, contact_id=contact_id)
