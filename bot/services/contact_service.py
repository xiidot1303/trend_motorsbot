from bot.models import Contact
from app.services import *

@sync_to_async
def list_of_regions_of_contacts():
    query = Contact.objects.all().values_list('region', flat=True).distinct()
    return list(query)

async def get_contact_by_region(region) -> Contact:
    obj = await Contact.objects.aget(region=region)
    return obj