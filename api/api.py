from ninja import NinjaAPI

from user_profile.api.views import router as user_profile_router
from api.auth import ApiKeyAuth, JWTAuth

api = NinjaAPI(version='1.0.0', auth=[JWTAuth(), ApiKeyAuth()])

api.add_router('/user-profile', user_profile_router)
