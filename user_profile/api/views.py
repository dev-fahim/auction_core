from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import transaction
from django.db.utils import DatabaseError
from ninja import Router

from api.auth import JWTAuth, ApiKeyAuth
from core.api.errors import OperationalError, UpdateError, CredentialError
from core.api.schemas import ErrorSchema, MsgSchema
from core.utils.auth import generate_token
from core.utils.builders import page_builder
from core.utils.validators import is_valid_email
from user_profile.enums import UserTypeEnum
from user_profile.models import Profile
from user_profile.api.schemas import ProfileListSchema, ProfileSchema, CheckEmailSchema, SignUpSchema, SignInSchema, \
    UserTokenSchema, ProfileUpdateSchema

router = Router(auth=[JWTAuth()])


# @router.get('/all', tags=['User Profiles'], response=ProfileListSchema)
# def get_profiles(request, page_number: int = 1):
#     profiles = Profile.objects.select_related('user', 'verified_by').order_by('-id')
#
#     return page_builder(profiles, 10, page_number)


@router.get('/get', tags=['User Profiles'], response=ProfileSchema)
def get_profile_object(request):
    return request.user.profile


@router.put('/update', tags=['User Profiles'], response={200: ProfileSchema, 422: ErrorSchema})
def update_profile_object(request, data: ProfileUpdateSchema):
    if is_valid_email(data.email):
        try:
            user = request.user
            user.username = data.email
            user.email = data.email
            user.first_name = data.first_name
            user.last_name = data.last_name
            user.save()

            return user.profile
        except DatabaseError:
            pass

    raise UpdateError()


@router.post('/auth/check-email', auth=[ApiKeyAuth(), JWTAuth()], tags=['Authentication'], response=MsgSchema)
def check_email(request, data: CheckEmailSchema):
    if is_valid_email(data.email) is False:
        return MsgSchema(msg='email_is_not_valid')

    user = User.objects.filter(email__iexact=data.email)

    if user.exists():
        return MsgSchema(msg='email_is_already_taken')
    return MsgSchema(msg='email_is_unique')


@router.post('/auth/sign-in', auth=[ApiKeyAuth()], tags=['Authentication'], response={
    200: UserTokenSchema,
    422: ErrorSchema
})
def sign_in(request, data: SignInSchema):
    user = authenticate(username=data.email, password=data.password)

    if user:
        try:
            profile: ProfileSchema = Profile.objects.select_related('user', 'verified_by').get(user_id=user.id)
            return UserTokenSchema(
                accessToken=generate_token(sub=profile.guid),
                profile=profile
            )
        except Profile.DoesNotExist:
            pass
    raise CredentialError()


@router.post('/auth/sign-up', auth=[ApiKeyAuth()], tags=['Authentication'],
             response={200: ProfileSchema, 422: ErrorSchema})
def sign_up(request, data: SignUpSchema):
    try:
        with transaction.atomic():
            user = User.objects.create_user(
                username=data.email,
                email=data.email,
                password=data.password,
                first_name=data.first_name,
                last_name=data.last_name)

            profile = Profile.objects.create(user_id=user.id,
                                             user_type=UserTypeEnum.BUYER if data.is_buyer else UserTypeEnum.SELLER)

        return profile

    except DatabaseError:
        raise OperationalError()
