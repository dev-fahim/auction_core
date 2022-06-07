from ninja.security import APIKeyHeader, HttpBearer


class ApiKeyAuthCheck:
    @staticmethod
    def authenticate(request, key):
        print(key)
        return key


class HttpBearerAuthCheck:
    @staticmethod
    def authenticate(request, token):
        print(token)
        return token


class ApiKeyAuth(ApiKeyAuthCheck, APIKeyHeader):
    param_name = 'X-API-KEY'


class JWTAuth(HttpBearerAuthCheck, HttpBearer):
    pass
