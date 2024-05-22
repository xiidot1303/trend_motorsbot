from app.services import *
from app.models import Vin_code, Product

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

    # set product if vin code is created
    if is_created or obj.product == None:
        # get product by title
        product: Product = await Product.objects.aget(title=product_title)
        obj.product = product
        await obj.asave()
        
    return obj