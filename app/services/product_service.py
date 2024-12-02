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
    return Product.objects.exclude(element_id=None).order_by('id')

async def get_product_by_id(id):
    obj = await Product.objects.aget(pk=id)
    return obj

@sync_to_async
def list_of_brands_of_products():
    query = Product.objects.filter(view_to=True).values_list('brand', flat=True).distinct().order_by('brand')
    return list(query)

@sync_to_async
def list_of_models_of_products_by_brand(brand):
    query = Product.objects.filter(brand=brand, view_to=True).values_list('model', flat=True).distinct()
    return list(query)
