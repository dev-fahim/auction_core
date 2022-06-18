from core.api.api import api
from user_profile.api.views import router as user_profile_router
from product.api.views import router as product_router
from auction.api.views import router as auction_router

api.add_router('/user-profiles', user_profile_router)
api.add_router('/products', product_router, tags=['Products'])
api.add_router('/auctions', auction_router, tags=['Auctions'])
