import httpx
import base64
import asyncio
from datetime import datetime

from telegram import Bot

from bot.models import Bot_user, LogGroup
from app.models import Contracts, PaySchedule, PayHistory
from config import ONE_C_URL, ONE_C_LOGIN, ONE_C_PASSWORD


class OneCAPI:
    def __init__(self, url: str, login: str, password: str) -> None:
        auth_string = f"{login}:{password}"
        self.auth_header = {
            "Authorization": f"Basic {base64.b64encode(auth_string.encode()).decode()}",
            "Content-Type": "application/json"
        }
        self.base_url = url

    async def _request(self, method: str, params=None, data=None) -> dict:
        url = f"{self.base_url}"
        async with httpx.AsyncClient(headers=self.auth_header) as client:
            response = await client.request(method, url, params=params, json=data)
            response.raise_for_status()
            return response.json()

    async def sync_all(self, bot: Bot) -> None:
        tasks = (
            self.sync_contracts(bot),
            self.sync_pay_schedule(bot),
            self.sync_order(),
        )
        for task in tasks:
            try:
                await task
            except Exception as e:
                print(f"{e}")

    async def get_contragent(self, contragent_id: str) -> dict:
        params = {
            "id": contragent_id,
            "type": "contragent"
        }
        return await self._request("GET", data=params)

    async def sync_contracts(self, bot: Bot, users: list[Bot_user] = None):
        if not users:
            users: list[Bot_user] = []
            users_q = Bot_user.objects.exclude(one_c_id__isnull=True).exclude(one_c_id__exact="")
            async for user in users_q:
                users.append(user)

        created = []
        for user_obj in users:
            try:
                data = {"id": user_obj.one_c_id,"type": "contract"}
                contracts = await self._request("GET", data=data)
                for contract in contracts.get("contracts", []):
                    try:
                        obj, create_status = await Contracts.objects.aupdate_or_create(
                            one_c_uidd=contract["id"],
                            one_c_id=contract["id2"],
                            defaults={
                                "user_id": user_obj.id,
                                "car": contract["car"],
                                "quantity": contract["quantity"],
                                "price": contract["price"],
                                "created": datetime.strptime(contract["created"], "%Y-%m-%d").date(),
                                "pay_date": datetime.strptime(contract["pay_date"], "%Y-%m-%d").date(),
                                "installment": contract["installment"],
                            }
                        )
                        if create_status and obj.installment:
                            created.append(obj)

                    except Exception as e:
                        print(f"sync_contracts -> contract {e}")
            except Exception as e:
                print(f"sync_contracts: {e}")

        if created:
            try:
                await self.sync_pay_schedule(bot, created)
                await self.sync_order(created)
            except Exception as e:
                print(f"sync_contracts: {e}")

    async def sync_pay_schedule(self, bot: Bot, contracts: list[Contracts] = None):
        if not contracts:
            contracts: list[Contracts] = []
            contracts_q = Contracts.objects.filter(installment=True)
            async for contract in contracts_q:
                contracts.append(contract)

        for contract_obj in contracts:
            data = {"id": contract_obj.one_c_id, "type": "monthly"}
            contract_up = await self._request("GET", data=data)

            pay_schedule = await PaySchedule.objects.filter(contract_id=contract_obj.id).afirst()
            if not pay_schedule or pay_schedule.json != contract_up.get("monthly", {}):
                await self.update_pay_schedule(
                    contract_obj, contract_up["monthly"], bot, file_base64=contract_up.get("monthly_pdf", "")
                )  # TODO It is necessary to separate the methods of obtaining json and images
                await asyncio.sleep(6)

            await asyncio.sleep(1)

    async def update_pay_schedule(self, contract: Contracts, json_date: dict, bot: Bot, file_base64: str = None):
        log_group: LogGroup = await LogGroup.objects.aget(id=1)
        file_id = ""

        if not log_group:  # Cache file to telegram
            return

        if not file_base64:  # TODO It is necessary to separate the methods of obtaining json and images
            data = {"id": contract.one_c_uidd, "type": "monthly"}
            pay_histories = await self._request("GET", data=data)
            file_base64 = pay_histories.get("monthly_pdf", "")

        if file_base64:
            file_data = base64.b64decode(file_base64)
            file = await bot.send_document(
                log_group.tg_id, document=file_data, filename=f"{contract.car}.pdf"
            )
            await bot.delete_message(log_group.tg_id, file.id)
            file_id = file.document.file_id

        pay_schedule = await PaySchedule.objects.filter(contract_id=contract.id).afirst()
        if pay_schedule:
            pay_schedule.json = json_date
            pay_schedule.file_id = file_id
            await pay_schedule.asave()

        else:
            pay_schedule = PaySchedule(
                contract_id=contract.id,
                file_id=file_id,
                json=json_date
            )
            await pay_schedule.asave()
        await self.update_notify_date(pay_schedule)

    @staticmethod
    async def update_notify_date(pay_schedule: PaySchedule, now: datetime = None):
        if not now:
            now = datetime.now()

        for info in pay_schedule.json:
            date = datetime.strptime(info.get("date"), "%Y-%m-%d")
            date = date.replace(hour=9, minute=0, second=0, microsecond=0)

            if now < date:
                pay_schedule.pay_date = date
                await pay_schedule.asave()
                break
        else:
            pay_schedule.payed = True
            await pay_schedule.asave()

    async def sync_order(self, contracts: list[Contracts] = None):
        if not contracts:
            contracts: list[Contracts] = []
            contracts_q = Contracts.objects.filter(installment=True)
            async for contract in contracts_q:
                contracts.append(contract)

        for contract_obj in contracts:
            params = {"id": contract_obj.one_c_uidd, "type": "order"}
            histories = await self._request("GET", data=params)

            for history in histories.get("orders", []):
                try:
                    await PayHistory.objects.aupdate_or_create(
                        contract_id=contract_obj.id,
                        one_c_id=history["id"],
                        defaults={
                            "date": history["date"],
                            "amount": history["amount"],
                            "currency": history["currency"],
                        }
                    )
                except Exception as e:
                    print(f"sync_order: {e}")


one_api = OneCAPI(ONE_C_URL, ONE_C_LOGIN, ONE_C_PASSWORD)
