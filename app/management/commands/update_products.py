from django.core.management.base import BaseCommand
from app.scheduled_job.amocrm_job import update_products_by_amocrm
import asyncio

class Command(BaseCommand):
    help = 'Command for updating products by getting data from AmoCrm'

    def handle(self, *args, **options):
        asyncio.run(
            update_products_by_amocrm()
        )
        print("Products are updated succesfully")