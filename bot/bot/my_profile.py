from bot.bot import *
from bot.resources.strings import lang_dict
from bot.resources.conversationList import MY_PROFILE

from app.models import Contracts, PayHistory
from app.services.one_c_sync import OneCAPI
from bot.models import Bot_user


async def to_my_profile(update: Update, context: CustomContext):
    user = await Bot_user.objects.aget(user_id=update.message.chat.id)
    if not user.one_c_id:
        return

    text = await get_word('my_profile_ans', user=user)
    my_contract_bt = await get_word('my_contract_bt', user=user)
    installment_bt = await get_word('installment_bt', user=user)
    markup = await build_keyboard(update, [my_contract_bt, installment_bt], 2, back_button=False)
    await bot_send_message(update, context, text, reply_markup=markup)
    return MY_PROFILE


async def my_profile(update: Update, context: CustomContext):
    user = await Bot_user.objects.aget(user_id=update.message.chat.id)
    if not user.one_c_id:
        return

    if update.message.text in lang_dict["my_contract_bt"]:
        text = ""
        contracts = Contracts.objects.filter(user_id=user.id).order_by('-created')[:10]

        async for contract in contracts:
            text_format = await get_word("my_contract_info", user=user)
            text += text_format.format(
                car=contract.car, quantity=contract.quantity, price=f"{contract.price:,}".replace(",", " "),
                created=contract.created.strftime("%Y.%m.%d"), pay_date=contract.pay_date.strftime("%Y.%m.%d")
            ) + "\n\n"
        if not contracts:
            text = "Not have"
        await bot_send_message(update, context, text=text)

    elif update.message.text in lang_dict["installment_bt"]:
        text = await get_word('my_profile_ans', user=user)
        history_bt = await get_word('history_bt', user=user)
        pay_schedule_bt = await get_word('pay_schedule_bt', user=user)
        markup = await build_keyboard(
            update, [history_bt, pay_schedule_bt], 2, back_button=True
        )
        await bot_send_message(update, context, text=text, reply_markup=markup)
        return INSTALLMENT

    else:
        text = await get_word('my_profile_ans', user=user)
        await bot_send_message(update, context, text=text)


async def my_installment(update: Update, context: CustomContext):
    user = await Bot_user.objects.aget(user_id=update.message.chat.id)
    if not user.one_c_id:
        return

    if update.message.text in lang_dict["history_bt"]:
        text = ""
        contracts = Contracts.objects.filter(user_id=user.id)
        contracts_ids = []

        async for contract in contracts:
            contracts_ids.append(contract.id)

        pay_histories = PayHistory.objects.filter(contract_id__in=contracts_ids)
        async for pay in pay_histories:
            text_format = await get_word("history_info", user=user)
            text += text_format.format(
                date=pay.date.strftime("%Y.%m.%d"), amount=f"{pay.amount:,}".replace(",", " "), currency=pay.currency
            ) + "\n\n"

        if not pay_histories:
            text = "Not have"
        await bot_send_message(update, context, text=text)

    elif update.message.text in lang_dict["pay_schedule_bt"]:
        text = "Скоро"
        await bot_send_message(update, context, text=text)

    elif update.message.text in lang_dict["back"]:
        await to_my_profile(update, context)
        return MY_PROFILE

    else:
        text = await get_word('my_profile_ans', user=user)
        await bot_send_message(update, context, text=text)
