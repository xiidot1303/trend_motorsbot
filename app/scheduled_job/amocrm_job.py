from app.services.amocrm_service import  get_catalog, get_vin_codes
from app.services.product_service import update_or_create_product
from app.services.vin_code_service import update_or_create_vin_code, delete_vin_codes_by_element_ids
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

async def update_vin_code_by_amocrm():
    elements = await get_vin_codes()
    element_ids = []
    for element in elements:
        # get data from request
        element_id = element["id"]
        element_ids.append(element_id)
        full_title = element["name"]
        try:
            vin_code, product_title, branch_title = full_title.split("|")
            # create vin code object
            await update_or_create_vin_code(
                element_id, full_title, vin_code.strip(), product_title.strip(), branch_title.strip()
            )
        except:
            None
            
    await delete_vin_codes_by_element_ids(element_ids)