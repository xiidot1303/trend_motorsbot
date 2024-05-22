from django.core.management.base import BaseCommand
from app.scheduled_job.amocrm_job import update_vin_code_by_amocrm
import asyncio

class Command(BaseCommand):
    help = 'Command for updating vin codes by getting data from AmoCrm'

    def handle(self, *args, **options):
        asyncio.run(
            update_vin_code_by_amocrm()
        )
        print("Vin codes are updated succesfully")