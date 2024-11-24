import httpx
import base64
from datetime import datetime

from bot.models import Bot_user
from app.models import Contracts

from config import ONE_C_URL, ONE_C_LOGIN, ONE_C_PASSWORD


class OneCAPI:
    def __init__(self, url: str, login: str, password: str) -> None:
        auth_string = f"{login}:{password}"
        self.auth_header = {
            "Authorization": f"Basic {base64.b64encode(auth_string.encode()).decode()}",
            "Content-Type": "application/json"
        }
        self.base_url = url

    async def _request(self, method: str, params=None, data=None):
        url = f"{self.base_url}"
        async with httpx.AsyncClient(headers=self.auth_header) as client:
            response = await client.request(method, url, params=params, json=data)
            response.raise_for_status()
            return response.json()

    async def get_order(self, order_id: str):
        params = {
            "id": order_id,
            "type": "order"
        }
        return await self._request("GET", data=params)

    async def get_contragent(self, contragent_id: str) -> dict:
        params = {
            "id": contragent_id,
            "type": "contragent"
        }
        return await self._request("GET", data=params)

    async def sync_contracts(self, user: Bot_user = None):
        users: list[Bot_user] = []
        if user:
            users.append(user)
        else:
            users_q = Bot_user.objects.exclude(one_c_id__isnull=True).exclude(one_c_id__exact="")
            async for user in users_q:
                users.append(user)

        for user_obj in users:
            data = {
                "id": user_obj.one_c_id,
                "type": "contract"
            }
            contracts = await self._request("GET", data=data)
            print(contracts)
            for contract in contracts.get("contracts", []):
                obj, created = await Contracts.objects.aupdate_or_create(
                    one_c_uidd=contract["id"],
                    defaults={
                        "user_id": user_obj.id,
                        "car": contract["car"],
                        "quantity": contract["quantity"],
                        "price": contract["price"],
                        "created": datetime.strptime(contract["created"], "%Y-%m-%d").date(),
                        "pay_date": datetime.strptime(contract["pay_date"], "%Y-%m-%d").date()
                    }
                )
                print(obj, created)


one_api = OneCAPI(ONE_C_URL, ONE_C_LOGIN, ONE_C_PASSWORD)
