from config import AMOCRM_CLIENT_ID, AMOCRM_CLIENT_SECRET
from app.services import *
from app.utils.amocrm_utils import *
import aiofiles

URL = "https://trendmotor.amocrm.ru"

async def generate_headers():
    async with aiofiles.open('amocrm_tokens/access.txt', mode='r') as f:
        access_token = await f.read()
    headers = {"Authorization": f"Bearer {access_token}"}
    return headers

async def update_tokens():
    async with aiofiles.open('amocrm_tokens/refresh.txt', mode='r') as f:
        refresh_token = await f.read()
    
    url = URL + '/oauth2/access_token'

    data = {
        "client_id": AMOCRM_CLIENT_ID,
        "client_secret": AMOCRM_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "redirect_uri": "https://google.com"
    }

    content, headers = await send_request(url, data, type='post')
    new_refresh_token = content['refresh_token']
    new_access_token = content['access_token']

    async with aiofiles.open('amocrm_tokens/refresh.txt', mode='w') as f:
        await f.write(new_refresh_token)

    async with aiofiles.open('amocrm_tokens/access.txt', mode='w') as f:
        await f.write(new_access_token)

async def get_catalog():
    url = URL + '/api/v4/catalogs/12730/elements?limit=250&page=1'
    headers = await generate_headers()
    result = []
    while True:
        content, h = await send_request(url, headers=headers)
        # get elements from request
        elements = content["_embedded"]["elements"]
        result += elements
        if "next" in content["_links"]:
            url = content["_links"]["next"]['href']
        else:
            break

    return result

async def get_vin_codes():
    url = URL + '/api/v4/catalogs/13091/elements?limit=250&page=1'
    headers = await generate_headers()
    result = []
    while True:
        content, h = await send_request(url, headers=headers)
        # get elements from request
        elements = content["_embedded"]["elements"]
        result += elements
        if "next" in content["_links"]:
            url = content["_links"]["next"]['href']
        else:
            break

    return result

async def create_simple_contact(
        name, phone_number
    ):

    url = URL + '/api/v4/contacts'
    headers = await generate_headers()
    method = "post"

    data = [
        {
            "name": name,
            "first_name": name,
            "custom_fields_values": [
                {
                    "field_id": 1438451,
                    "values": [
                        {
                            "value": phone_number,
                            "enum_id": 858577,
                            "enum_code": "WORK"
                        }
                    ]
                },
            ]
        }
    ]

    content, h = await send_request(url, data, headers=headers, type=method)
    contact_id = content['_embedded']['contacts'][0]['id']
    return contact_id


async def create_contact(
        name, surname, phone_number, passport_serial, passport_number,
        date_birth: int, doc_give_place, date_begin_document: int, pnfl, birth_place
    ):    
    url = URL + '/api/v4/contacts'
    headers = await generate_headers()
    method = "post"
    data = [
        {
            "name": f"{name} {surname}",
            "first_name": name,
            "last_name": surname,
            "responsible_user_id": 10287314,
            "custom_fields_values": [
                {
                    "field_id": 1438451,
                    "values": [
                        {
                            "value": phone_number,
                            "enum_id": 858577,
                            "enum_code": "WORK"
                        }
                    ]
                },
                {
                    "field_id": 1561288,
                    "values": [
                        {
                            "value": f"{passport_serial}{passport_number}"
                        }
                    ]
                },
                {
                    "field_id": 1575435,
                    "values": [
                        {
                            "value": date_birth
                        }
                    ]
                },
                {
                    "field_id": 1597603,
                    "values": [
                        {
                            "value": doc_give_place
                        }
                    ]
                },
                {
                    "field_id": 1597609,
                    "values": [
                        {
                            "value": date_begin_document
                        }
                    ]
                },
                {
                    "field_id": 1598027,
                    "values": [
                        {
                            "value": True
                        }
                    ]
                },
                {
                    "field_id": 1451161,
                    "values": [
                        {
                            "value": pnfl
                        }
                    ]
                },
                {
                    "field_id": 1579197,
                    "values": [
                        {
                            "value": birth_place
                        }
                    ]
                }
            ]
        }
    ]

    content, h = await send_request(url, data, headers=headers, type=method)
    contact_id = content['_embedded']['contacts'][0]['id']
    return contact_id

class Lead(LeadCustomFields):
    def __init__(self, pipeline_id):
        """
        pipeline_id = 7492114 Заказ авто\n
        pipeline_id = 8282930 Cервис авто
        """
        self.pipeline_id = pipeline_id
        self.custom_fields_values = None

    async def set_data_for_8282930(self, brand, model, region):
        self.custom_fields_values = await self.get_8282930(
            brand=brand, model=model, region=region
        )

    async def create_lead(self):
        url = URL + "/api/v4/leads"
        headers = await generate_headers()
        custom_fields_values = self.custom_fields_values
        match self.pipeline_id:
            case 7492114:
                custom_fields_values = await self.get_7492114()

        data = [
            {
                "created_by": 0,
                "pipeline_id": self.pipeline_id,
                "custom_fields_values": custom_fields_values
            }
        ]
        content, h = await send_request(url, data, headers=headers, type='post')
        lead_id = content['_embedded']['leads'][0]['id']
        return lead_id

async def link_vin_code_and_contact_to_lead(
        lead_id, vin_code_id, contact_id
    ):
    headers = await generate_headers()
    url = URL + f"/api/v4/leads/{lead_id}/link"

    data = [
        {
            "to_entity_id": vin_code_id,
            "to_entity_type": "catalog_elements",
            "metadata": {
                "quantity": 1,
                "catalog_id": 13091
            }
        },
        {
            "to_entity_id": contact_id,
            "to_entity_type": "contacts",
            "metadata": {
                "is_main": True
            }
        }
    ]

    content, h = await send_request(url, data, headers=headers, type='post')
    return


async def link_contact_to_lead(
        lead_id, contact_id
    ):
    headers = await generate_headers()
    url = URL + f"/api/v4/leads/{lead_id}/link"

    data = [
        {
            "to_entity_id": contact_id,
            "to_entity_type": "contacts",
            "metadata": {
                "is_main": True
            }
        }
    ]

    content, h = await send_request(url, data, headers=headers, type='post')
    return



async def change_lead_status(lead_id):
    url = URL + "/api/v4/leads"
    headers = await generate_headers()

    data = [
        {
            "id": lead_id,
            "pipeline_id": 7492114,
            "status_id": 62145310
        }
    ]

    response = requests.patch(url, json=data, headers=headers)
    status = response.status_code
    return status