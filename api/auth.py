from ninja.security import APIKeyHeader, HttpBearer

from core.models import ApiKey
from core.utils.auth import decode_token
from user_profile.models import Profile


class ApiKeyAuthCheck:
    @staticmethod
    def authenticate(request, key):
        try:
            key = ApiKey.objects.get(secret__exact=key)
            return key.secret
        except ApiKey.DoesNotExist:
            pass


class HttpBearerAuthCheck:
    @staticmethod
    def authenticate(request, token):
        decoded = decode_token(token)
        if decoded:
            profile = Profile.objects.select_related('user').get(guid__exact=decoded.sub)
            user = profile.user
            request.user = user
            return token


class ApiKeyAuth(ApiKeyAuthCheck, APIKeyHeader):
    param_name = 'X-API-KEY'


class JWTAuth(HttpBearerAuthCheck, HttpBearer):
    pass
