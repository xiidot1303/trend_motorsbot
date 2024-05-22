from config import AMOCRM_CLIENT_ID, AMOCRM_CLIENT_SECRET
from app.services import *
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
    
async def create_contact(
        name, surname, phone_number, passport_serial, passport_number,
        date_birth, doc_give_place, date_begin_document, pnfl, birth_place
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