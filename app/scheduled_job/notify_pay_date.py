from datetime import datetime, timedelta

from telegram import Bot

from bot.models import Bot_user
from app.models import PaySchedule, Contracts
from bot.services.language_service import get_word
from app.services.one_c_sync import one_api


async def notify_pay_date(bot: Bot, days_to_notify: int = 3):
    now = datetime.now()
    target_date = now + timedelta(days=days_to_notify)

    not_updated = PaySchedule.objects.filter(pay_date__lt=now, payed=False)
    async for pay in not_updated:
        await one_api.update_notify_date(pay, now=now)

    pays = PaySchedule.objects.filter(pay_date__gt=now, pay_date__lt=target_date, payed=False)
    async for pay in pays:
        try:
            contract: Contracts = await Contracts.objects.aget(id=pay.contract_id)
            user: Bot_user = await Bot_user.objects.aget(id=contract.user_id)

            days = pay.pay_date - now
            text_format = await get_word("pay_notify", user=user)
            text = text_format.format(car=contract.car, days=days.days)
            await bot.send_message(user.user_id, text)
            await one_api.update_notify_date(pay, target_date)

        except Exception as e:
            print(e)
