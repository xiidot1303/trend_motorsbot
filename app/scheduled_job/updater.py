from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from app.scheduled_job import amocrm_job
from asgiref.sync import async_to_sync
from app.services.amocrm_service import update_tokens as _update_tokens
from app.services.one_c_sync import one_api
from bot.control.updater import application


class jobs:
    scheduler = BackgroundScheduler(timezone='Asia/Tashkent')
    # scheduler = AsyncIOScheduler
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    scheduler.add_job(
        async_to_sync(amocrm_job.update_products_by_amocrm), 
        'interval', 
        minutes=10
        )
    scheduler.add_job(
        async_to_sync(amocrm_job.update_vin_code_by_amocrm), 
        'interval', 
        minutes=5
        )
    scheduler.add_job(
        async_to_sync(_update_tokens), 
        'cron', hour=1, minute=0, second=0)

    scheduler.add_job(
        async_to_sync(one_api.sync_all),
        'cron', minute=15, second=0,
        args=[application.bot]
    )
