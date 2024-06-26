from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    InlineQueryHandler,
    TypeHandler,
    ConversationHandler
)

from bot.resources.strings import lang_dict
from bot.resources.conversationList import *

from bot.bot import (
    main, login, web_app, TO
)

exceptions_for_filter_text = (~filters.COMMAND) & (~filters.Text(lang_dict['main menu']))

login_handler = ConversationHandler(
    entry_points=[CommandHandler("start", main.start)],
    states={
        GET_LANG: [
            MessageHandler(filters.Text(lang_dict["uz_ru"]), login.get_lang),
            MessageHandler(filters.TEXT & (~filters.COMMAND), login.get_lang)
        ],
        GET_NAME: [
            MessageHandler(filters.TEXT & (~filters.COMMAND), login.get_name)
        ],
        GET_CONTACT: [
            MessageHandler(filters.CONTACT, login.get_contact),
            MessageHandler(filters.Text(lang_dict['back']), login.get_contact),
            MessageHandler(filters.TEXT & (~filters.COMMAND), login.get_contact)
        ]
    },
    fallbacks=[
        CommandHandler("start", login.start)
    ],
    name="login",
)

web_app_data_handler = MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app.web_app_data)

contact_handler = MessageHandler(filters.Text(lang_dict['contacts']), main.contact)

contacts_of_region_handler = CallbackQueryHandler(main.contacts_of_region, pattern=r"^contacts_of")

social_networks_handler = MessageHandler(filters.Text(lang_dict['social_networks']), main.social_networks)

TO_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Text(lang_dict['TO']), main.TO)
    ],
    states={
        GET_BRAND_NAME: [
            MessageHandler(filters.TEXT & exceptions_for_filter_text, TO.get_brand_name)
        ],
        GET_MODEL_NAME: [
            MessageHandler(filters.TEXT & exceptions_for_filter_text, TO.get_model_name)
        ],
        GET_REGION: [
            MessageHandler(filters.TEXT & exceptions_for_filter_text, TO.get_region)
        ],
        GET_NAME: [
            MessageHandler(filters.TEXT & exceptions_for_filter_text, TO.get_name)
        ],
        GET_CONTACT: [
            MessageHandler(filters.TEXT & exceptions_for_filter_text, TO.get_contact)
        ],

    },
    fallbacks=[
        CommandHandler('start', TO.start),
        MessageHandler(filters.Text(lang_dict['main menu']), TO.start)
    ],
    name="TO",
)

handlers = [
    login_handler,
    web_app_data_handler,
    contact_handler,
    contacts_of_region_handler,
    social_networks_handler,
    TO_handler,

]