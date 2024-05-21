from app.services.amocrm_service import  get_catalog
from app.services.product_service import update_or_create_product
import re

async def update_products_by_amocrm():
    elements = await get_catalog()

    for element in elements:
        # get data from request
        element_id = element["id"]
        full_title = element["name"]
        custom_fields = element["custom_fields_values"]
        price = 0
        category = None
        remainder = 0
        # get data from custom fields
        for custom_field in custom_fields:
            match custom_field["field_id"]:
                case 1565354:
                    category = custom_field["values"][0]["value"]
                case 1565352:
                    price = int(custom_field["values"][0]["value"])
                case 1565368:
                    remainder = int(custom_field["values"][0]["value"])

        ### GET ADDTIONAL DATA FROM FULL_TITLE
        text = full_title
        words = text.split()

        # get variables from full title and make model name by removing remaining words
        brand = words[0]
        text = text.replace(f"{brand} ", "")

        color = text[text.find("(")+1:text.find(")")] if "(" in text else None
        text = text.replace(f"({color})", "")

        try:
            battery_range = re.search(r'\b(\d+)km\b', text).group(1) + " km"
            text = text.replace(f"{battery_range}km", "")
        except:
            battery_range = None

        try:
            battery_capacity = re.search(r'\b(\d+)kW\b', text).group(1) + " kW"
            text = text.replace(f"{battery_capacity}kW", "")
        except:
            battery_capacity = None

        model = text.strip()

        # save product data
        await update_or_create_product(
            element_id, full_title, model, brand,
            color, price, category, battery_range, 
            battery_capacity, remainder
        )
