from app.services import *
from config import MYCAR_LOGIN, MYCAR_PASSWORD

class Personal_data:
    def __init__(self, pnfl=None, surname=None, name=None, patronym=None, birth_place=None, nationality=None, blank=False):
        if not blank:
            self.pnfl = pnfl
            self.surname = surname
            self.name = name
            self.patronym = patronym
            self.birth_place = birth_place
            self.nationality = nationality
        

async def auth_mycar_and_get_token():
    url = "https://my-car.uz:2312/auth/v1/auth/authenticate"
    data = {
        "username": MYCAR_LOGIN,
        "password": MYCAR_PASSWORD, 
        "to_remember": False
        }
    content, headers = await send_request(url, data, type='post')
    return content['data']['access_token']

async def get_personal_data_with_passport_data(
        passport_serial, passport_number, birth_date
    ) -> Personal_data:
    url = "https://my-car.uz:2312/integration/v1/gcp/person-info-by-passport"
    url += f"?serial={passport_serial}&number={passport_number}&birth_date={birth_date}"

    token = await auth_mycar_and_get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    content, h = await send_request(url, headers=headers)
    data = content["data"]
    if data:
        data = data[0]
        personal_data = Personal_data(
            data['pnfl'], data['surname_latin'], data['name_latin'], data['patronym_latin'],
            data['birth_place'], data['nationality']
        )
    else:
        personal_data = Personal_data(blank=True)
    return personal_data

