from bot.bot import *
import json
from app.services.product_service import *
from app.services.passport_data_service import *
from app.services.order_service import *
from app.services.vin_code_service import *
from app.services import amocrm_service as amocrm
import asyncio

async def web_app_data(update: Update, context: CustomContext) -> None:
    data = json.loads(update.effective_message.web_app_data.data)
    try:
        # get bot user
        bot_user: Bot_user = await get_object_by_user_id(update.message.chat_id)
        # get values from data
        product_id = int(data['id'])
        passport_serial = data['passport_serial']
        passport_number = data['passport_number']
        branch_id = data['branch_id']
        # get product by id
        product: Product = await get_product_by_id(product_id)
        # get passport data
        passport_data: Passport_data = await get_passport_data_by_serial_number(
            passport_serial, passport_number
        )
        # create order
        order: Order = await create_order(
            bot_user, passport_data, product.pk
        )
        # find vin code by product and branch id
        vin_code: Vin_code = await get_vin_code_by_product_and_branch(
            product, branch_id
        )
        if not vin_code:
            text = await get_word('this car is already taken', update)
            await update_message_reply_text(update, text)
            return

        # create lead and send contract in background
        loop = asyncio.get_event_loop()
        loop.create_task(send_contract(
            bot_user, order, passport_data, vin_code
        ))

    except:
        text = await get_word('error getting web app data', update)
        await update_message_reply_text(update, text)
        return

async def send_contract(
            bot_user: Bot_user, order: Order, passport_data: Passport_data,
            vin_code: Vin_code
        ):
    # create contact in amocrm if not created in the past
    if not bot_user.amocrm_contact_id:
        birth_datetime = datetime.combine(passport_data.birth_date, datetime.min.time())
        datetime_begin_document = datetime.combine(passport_data.date_begin_document, datetime.min.time())
        contact_id = await amocrm.create_contact(
            passport_data.name, passport_data.surname, bot_user.phone,
            passport_data.serial, passport_data.number, int(birth_datetime.timestamp()),
            passport_data.doc_give_place, int(datetime_begin_document.timestamp()),
            passport_data.pnfl, passport_data.birth_place
        )
        bot_user.amocrm_contact_id = contact_id
        await bot_user.asave()
    
    # get contact id in amocrm from bot user
    contact_id = bot_user.amocrm_contact_id

    # create lead
    lead_id = await amocrm.create_lead()

    # set lead id to order
    set_amocrm_lead_id_to_order(order, lead_id)

    # link contact and add vin code to lead
    await amocrm.link_vin_code_and_contact_to_lead(
        lead_id, vin_code.element_id, contact_id
    )
    # delete vin code
    await vin_code.adelete()
    status = await amocrm.change_lead_status(lead_id)
    # check status of changing lead status
    if status == 200:
        # successed, can send contract after 3 seconds
        text = await get_word('successfully ordered', chat_id=bot_user.user_id)
        await bot.send_message(bot_user.user_id, text)
        pass
    else:
        text = await get_word('error getting web app data', chat_id=bot_user.user_id)
        await bot.send_message(bot_user.user_id, text)
        return





