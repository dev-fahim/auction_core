from ninja import Router

from api.auth import JWTAuth

router = Router(auth=[JWTAuth()])


@router.get('/all')
def get_all_products(request):
    pass
