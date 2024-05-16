import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bot.control.updater import application
from telegram import Update
import asyncio
from asgiref.sync import sync_to_async, async_to_sync
from time import sleep


@csrf_exempt
@async_to_sync
async def bot_webhook(request):
    data = json.loads(request.body.decode("utf-8"))
    update = Update.de_json(data = data, bot=application.bot)
    async with application:
        await application.process_update(update)
    return HttpResponse('')

async def update_bot(update):
    # await asyncio.sleep(5)
    async with application:
        await application.process_update(update)