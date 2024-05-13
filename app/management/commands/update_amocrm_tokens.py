from django.core.management.base import BaseCommand
from app.services.amocrm_service import update_tokens
import asyncio

class Command(BaseCommand):
    help = 'Command for updating access and refresh tokens of AmoCrm'

    def handle(self, *args, **options):
        asyncio.run(
            update_tokens()
        )
        print("Tokens updated successfully")