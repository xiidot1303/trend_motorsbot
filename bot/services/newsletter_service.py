from app.services import *
from app.models import Order
from bot.models import Bot_user
from asgiref.sync import sync_to_async, async_to_sync
from bot.bot import send_newsletter
from bot.control.updater import application

def send_contract_to_bot_user(order: Order):
    bot_user: Bot_user = order.bot_user
    contract = order.contract
    # send message to user
    text = f"{order.passport_data.surname} {order.passport_data.name} {order.passport_data.patronym}"
    async_to_sync(send_newsletter)(
        application.bot, bot_user.user_id, text, document=contract.open()
        )
    