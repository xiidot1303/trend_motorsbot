from app.services import *
from app.models import Vin_code, Product, Branch
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

def filter_branches_by_product(product: Product):
    # filter vin codes of this product
    vin_codes = Vin_code.objects.filter(product=product)
    # get list of branch titles from vin codes
    branch_titles = vin_codes.values_list('branch_title', flat=True)
    # filter branches by this titles
    branches = Branch.objects.filter(title__in = branch_titles)
    return branches

@sync_to_async
def delete_vin_codes_by_element_ids(ids):
    query = Vin_code.objects.exclude(element_id__in = ids)
    query.delete()

@sync_to_async
def get_vin_code_by_product_and_branch(product: Product, branch_id: int):
    branch: Branch = Branch.objects.get(pk=branch_id)
    vin_codes = Vin_code.objects.filter(product = product, branch_title = branch.title)
    return vin_codes[0] if vin_codes else None

@sync_to_async
def list_regions_of_branches():
    query = Branch.objects.all().values_list('region', flat=True).distinct()
    return list(query)