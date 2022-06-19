from django.utils import timezone
from ninja import Router

from core.api.auth import JWTAuth
from core.api.errors import UpdateError, CreateError, GetError, NotPermittedError
from core.api.schemas import ErrorSchema
from core.helpers import func_debugger
from core.utils.builders import page_builder
from product.api.permissions import check_seller_limited
from product.api.schemas import ProductListSchema, ProductSchema, CreateProductSchema, UpdateProductSchema, \
    CategoryListSchema
from product.models import Product, Category

router = Router(auth=[JWTAuth()])


@router.get('/all', response=ProductListSchema)
@func_debugger
def get_all_products(request, page_number: int = 1):
    user = request.user

    products = Product.objects.filter(user_id=user.id, is_active=True).order_by('-id')

    return page_builder(products, 10, page_number)


@router.get('/get/{guid}', response={200: ProductSchema, 422: ErrorSchema})
@func_debugger
def get_product_object(request, guid):
    user = request.user

    try:
        product = Product.objects.get(user_id=user.id, guid__exact=guid, is_active=True)
    except Product.DoesNotExist:
        raise GetError("product")

    return product


@router.get('/categories', response=CategoryListSchema)
@func_debugger
def get_all_categories(request):
    return CategoryListSchema(data=list(Category.objects.filter(is_active=True)))


@router.post('/create', response={200: ProductSchema, 422: ErrorSchema})
@func_debugger
def create_product(request, data: CreateProductSchema):
    check_seller_limited(request.user)

    now = timezone.now()

    if now < data.bid_starts < data.bid_expires and data.min_bid_price >= 0:
        user = request.user
        try:
            category = Category.objects.get(guid__exact=data.category) if data.category else None
            product = Product.objects.create(
                user_id=user.id,
                category=category,
                name=data.name,
                description=data.description,
                min_bid_price=data.min_bid_price,
                bid_starts=data.bid_starts,
                bid_expires=data.bid_expires,
                is_active=True
            )
            return product
        except Category.DoesNotExist:
            raise GetError("category")

    raise CreateError("fields")


@router.put('/update/{guid}', response={200: ProductSchema, 422: ErrorSchema})
@func_debugger
def update_product(request, guid: str, data: UpdateProductSchema):
    check_seller_limited(request.user)

    user = request.user

    try:
        product = Product.objects.get(guid__exact=guid, user_id=user.id)
    except Product.DoesNotExist:
        raise GetError("product")

    if product.is_updatable is False:
        raise NotPermittedError("product")

    now = timezone.now()

    if now < data.bid_starts < data.bid_expires and data.min_bid_price >= 0:
        try:
            category = Category.objects.get(guid__exact=data.category) if data.category else product.category
            data_dict = dict(data)
            data_dict.pop('category')
            for key, value in data_dict.items():
                setattr(product, key, value)
            product.category = category
            product.updated = timezone.now()
            product.save()
            return product
        except Category.DoesNotExist:
            raise GetError("category")

    raise UpdateError("fields")


@router.delete('/delete/{guid}', response={200: ProductSchema, 422: ErrorSchema})
def delete_product(request, guid: str):
    check_seller_limited(request.user)

    user = request.user

    try:
        product = Product.objects.get(guid__exact=guid, user_id=user.id)
    except Product.DoesNotExist:
        raise GetError("product")

    product.delete()

    return product
