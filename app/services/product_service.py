from app.services import *
from app.models import Product
 
async def update_or_create_product(
        element_id, title, model, brand, color, price,
        category, battery_range, battery_capacity, remainder
    ):  
    # get or create product
    product, is_created = await Product.objects.aget_or_create(
        element_id = element_id, defaults={
            "title": title,
            "model": model,
            "brand": brand,
            "color": color,
            "price": price,
            "category": category,
            "battery_range": battery_range,
            "battery_capacity": battery_capacity,
            "remainder": remainder
        }
    )
    
    # update price and remainder if product is not created
    if not is_created:
        product.price = price
        product.remainder = remainder
        await product.asave()

def product_list_all():
    return Product.objects.all()