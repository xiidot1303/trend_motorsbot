from bot.bot import *
import json
from app.services.product_service import *
from app.services.passport_data_service import *
from app.services.order_service import *

async def web_app_data(update: Update, context: CustomContext) -> None:
    data = json.loads(update.effective_message.web_app_data.data)
    try:
        # get bot user
        bot_user: Bot_user = await get_object_by_user_id(update.message.chat_id)
        # get values from data
        product_id = int(data['id'])
        passport_serial = data['passport_serial']
        passport_number = data['passport_number']

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

        # generate contract for order
        contract_file = await generate_contract_and_set_to_order(order)

        # send contract to bot user
        await bot_send_document(update, context, open(contract_file, 'rb'))
    except:
        text = await get_word('error getting web app data', update)
        return