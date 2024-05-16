from app.views import *
from rest_framework.views import APIView
from app.serializers import PassportDataSerializer
from app.services.passport_data_service import *
from asgiref.sync import async_to_sync

class PersonalDataByPassport(APIView):
    def post(self, request):
        serializer = PassportDataSerializer(data=request.data)
        if serializer.is_valid():
            # set attributes
            serial = serializer.validated_data['serial']
            number = serializer.validated_data['number']
            birth_date = serializer.validated_data['birth_date']
            # get personal info from special services using passport data and birth date
            data: Personal_data = async_to_sync(get_personal_data_with_passport_data)(
                serial, number, birth_date
            )
            return Response(data.__dict__, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)