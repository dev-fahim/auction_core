from api.api import api
from user_profile.api.views import router as user_profile_router
from product.api.views import router as product_router

api.add_router('/user-profiles', user_profile_router)
api.add_router('/products', product_router, tags=['Products'])
