from app.services import *
from app.models import Vin_code, Product
from asgiref.sync import sync_to_async

async def update_or_create_vin_code(
        element_id, full_title, code, product_title, branch_title
    ):
    # get or create vin code
    obj, is_created = await Vin_code.objects.aget_or_create(
        element_id=element_id, defaults={
            "full_title": full_title,
            "code": code,
            "branch_title": branch_title
        }
    )
    obj_product = await get_object_product(obj)
    # set product if vin code is created
    if is_created or obj_product is None:
        # get product by title
        try:
            product: Product = await Product.objects.aget(title=product_title)
            obj.product = product
            await obj.asave()
        except:
            None
    return obj

@sync_to_async
def get_object_product(obj: Vin_code):
    return obj.product