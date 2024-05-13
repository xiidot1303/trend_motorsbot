from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from app.scheduled_job import amocrm_job
from asgiref.sync import async_to_sync

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
    # scheduler.add_job(job.alert_clients, 'cron', hour=8, minute=0, second=0)

    
