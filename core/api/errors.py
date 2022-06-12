import sys

from api.api import api
from core.api.schemas import ErrorCodes, ErrorSchema


class ApiError(Exception):
    msg: str = 'got'

    def __init__(self, msg):
        self.msg = msg


class GetError(ApiError):
    pass


class CreateError(ApiError):
    pass


class UpdateError(ApiError):
    pass


class DeleteError(ApiError):
    pass


class OperationalError(ApiError):
    pass


class TransactionalError(ApiError):
    pass


class UniqueError(ApiError):
    pass


class IntegrityError(ApiError):
    pass


class CredentialError(ApiError):
    pass


class NotPermittedError(ApiError):
    pass


@api.exception_handler(GetError)
def api_get_error(request, exe):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    return api.create_response(
        request,
        ErrorSchema(error=f"{exe.msg}_get_error_{exc_tb.tb_lineno}", code=ErrorCodes.GLOBAL_GET_ERROR),
        status=422
    )


@api.exception_handler(CreateError)
def api_create_error(request, exe):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    return api.create_response(
        request,
        ErrorSchema(error=f"{exe.msg}_create_error_{exc_tb.tb_lineno}", code=ErrorCodes.GLOBAL_CREATE_ERROR),
        status=422
    )


@api.exception_handler(UpdateError)
def api_update_error(request, exe):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    return api.create_response(
        request,
        ErrorSchema(error=f"{exe.msg}_update_error_{exc_tb.tb_lineno}", code=ErrorCodes.GLOBAL_UPDATE_ERROR),
        status=422
    )


@api.exception_handler(DeleteError)
def api_delete_error(request, exe):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    return api.create_response(
        request,
        ErrorSchema(error=f"{exe.msg}_delete_error_{exc_tb.tb_lineno}", code=ErrorCodes.GLOBAL_DELETE_ERROR),
        status=422
    )


@api.exception_handler(TransactionalError)
def api_transactional_error(request, exe):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    return api.create_response(
        request,
        ErrorSchema(error=f"{exe.msg}_transactional_error_{exc_tb.tb_lineno}", code=ErrorCodes.GLOBAL_OPERATION_ERROR),
        status=422
    )


@api.exception_handler(UniqueError)
def api_unique_error(request, exe):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    return api.create_response(
        request,
        ErrorSchema(error=f"{exe.msg}_unique_error_{exc_tb.tb_lineno}", code=ErrorCodes.GLOBAL_UNIQUE_ERROR),
        status=422
    )


@api.exception_handler(IntegrityError)
def api_integrity_error(request, exe):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    return api.create_response(
        request,
        ErrorSchema(error=f"{exe.msg}_integrity_error_{exc_tb.tb_lineno}", code=ErrorCodes.GLOBAL_INTEGRITY_ERROR),
        status=422
    )


@api.exception_handler(CredentialError)
def api_credential_error(request, exe):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    return api.create_response(
        request,
        ErrorSchema(error=f"{exe.msg}_credential_error_{exc_tb.tb_lineno}", code=ErrorCodes.GLOBAL_CREDENTIAL_ERROR),
        status=422
    )


@api.exception_handler(NotPermittedError)
def api_not_permitted_error(request, exe):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    return api.create_response(
        request,
        ErrorSchema(error=f"{exe.msg}_not_permitted_error_{exc_tb.tb_lineno}",
                    code=ErrorCodes.GLOBAL_NOT_PERMITTED_ERROR),
        status=422
    )


@api.exception_handler(OperationalError)
def api_operational_error(request, exe):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    return api.create_response(
        request,
        ErrorSchema(error=f"{exe.msg}_operational_error_{exc_tb.tb_lineno}", code=ErrorCodes.GLOBAL_OPERATION_ERROR),
        status=422
    )
