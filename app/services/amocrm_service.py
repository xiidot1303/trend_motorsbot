from config import AMOCRM_CLIENT_ID, AMOCRM_CLIENT_SECRET
from app.services import *
import aiofiles

URL = "https://trendmotor.amocrm.ru"

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
    # get access token
    async with aiofiles.open('amocrm_tokens/access.txt', mode='r') as f:
        access_token = await f.read()

    url = URL + '/api/v4/catalogs/12730/elements'
    headers = {"Authorization": f"Bearer {access_token}"}
    content, headers = await send_request(url, headers=headers)
    
    # get elements from request
    elements = content["_embedded"]["elements"]

    return elements