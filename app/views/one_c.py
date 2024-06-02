from app.views import *
from rest_framework.views import APIView
from rest_framework import generics
from app.serializers import GetContractSerializer
from app.services.order_service import generate_contract_and_set_to_order, Order
from asgiref.sync import async_to_sync
from bot.services.newsletter_service import send_contract_to_bot_user
import asyncio

class GetOrderContract(APIView):
    def post(self, request):
        serializer = GetContractSerializer(data=request.data)
        if serializer.is_valid():
            # set attributes
            lead_id = serializer.validated_data['lead_id']
            contract = serializer.validated_data['contract']

            # get order by lead_id
            order = Order.objects.get(amocrm_lead_id=lead_id)
            # generate contract from base64 and set to order
            order = async_to_sync(generate_contract_and_set_to_order)(order, contract)
            # send contract to user
            send_contract_to_bot_user(order)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        