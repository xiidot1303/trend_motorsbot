from swagger import *

personal_data_by_passport_schema_dict = {
    "200": openapi.Response(
        description='',
        schema=openapi.Schema(
            type="object",
            properties={
                "pnfl": openapi.Schema(type="string"), 
                "surname": openapi.Schema(type="string"), 
                "name": openapi.Schema(type="string"), 
                "patronym": openapi.Schema(type="string"), 
                "birth_place": openapi.Schema(type="string"), 
                "nationality": openapi.Schema(type="string"), 
                "doc_give_place": openapi.Schema(type="string"), 
                "date_begin_document": openapi.Schema(type="string"), 
                
            },
            required=[],  # Specify required properties
        ),
        # examples={
        #     "application/json": {
        #         "key1": "value1",
        #         "key2": 123,
        #     },
        # },
    ),
}
