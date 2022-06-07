from ninja import NinjaAPI

from user_profile.api.views import router as user_profile_router

api = NinjaAPI(version='1.0.0', title='Auction Core API')

api.add_router('/user-profiles', user_profile_router)
