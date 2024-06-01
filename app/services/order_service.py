from app.services import *
from app.models import *
from bot.models import Bot_user
from app.services.product_service import get_product_by_id as _get_product_by_id
from app.utils.order_utils import create_contract

async def create_order_item(product_id) -> Order_item:
    product: Product = await _get_product_by_id(product_id)
    obj: Order_item = await Order_item.objects.acreate(
        product = product, price = product.price
    )
    return obj

async def create_order(
        bot_user: Bot_user, passport_data: Passport_data, product_id, 
    ) -> Order:
    # create order item
    order_item: Order_item = await create_order_item(product_id)

    # create order
    obj: Order = await Order.objects.acreate(
        bot_user = bot_user, passport_data = passport_data,
        order_item = order_item
    )
    return obj

async def generate_contract_and_set_to_order(order: Order):
    passport_data: Passport_data = order.passport_data
    now = await datetime_now()
    # set replacements of texts in file
    replacements = {
        "[[name]]": passport_data.name,
        "[[surname]]": passport_data.surname,
        "[[patronym]]": passport_data.patronym,
        "[[pnfl]]": passport_data.pnfl,
        "[[passport_serial]]": passport_data.serial,
        "[[passport_number]]": passport_data.number,
        "[[birth_date]]": passport_data.birth_date.strftime("%d.%m.%Y"),
        "[[doc_give_place]]": passport_data.doc_give_place,
        "[[date_begin_document]]": passport_data.date_begin_document.strftime("%d.%m.%Y"),

        "[[product_title]]": order.order_item.product.title,
        "[[price]]": order.order_item.price,

        "[[date]]": now.strftime("%d.%m.%Y"),
        "[[time]]": now.strftime("%H:%M"),
    }

    contract_file_path = await create_contract(
        f"contract_{order.pk}", replacements
    )

    order.contract = contract_file_path
    await order.asave()
    return contract_file_path

async def set_amocrm_lead_id_to_order(order: Order, lead_id):
    order.amocrm_lead_id = lead_id
    await order.asave()
    return