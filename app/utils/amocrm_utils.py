class LeadCustomFields:
    async def get_7492114(self):
        return [
            {
                "field_id": 1614073,
                "values": [
                    {
                        "value": "Безналичный",
                        "enum_id": 3832001,
                        "enum_code": None
                    }
                ]
            },
            {
                "field_id": 1616659,
                "values": [
                    {
                        "value": "Реклама в интернете",
                        "enum_id": 4028735,
                        "enum_code": None
                    }
                ]
            },
            {
                "field_id": 1598657,
                "values": [
                    {
                        "value": "Электромобиль",
                        "enum_id": 1026879,
                        "enum_code": None
                    }
                ]
            },
            {
            "field_id": 1617025,
            "values": [
                    {
                        "value": True
                    }
                ]
            }
        ]

    async def get_8282930(self, brand, model, region):
        return [
            {
                "field_id": 1618711, # Марка
                "values": [
                    {
                        "value": brand
                    }
                ]
            },
            {
                "field_id": 1618713, # Модель
                "values": [
                    {
                        "value": model
                    }
                ]
            },
            {
                "field_id": 1618715, # Филиал
                "values": [
                    {
                        "value": region
                    }
                ]
            },


        ]