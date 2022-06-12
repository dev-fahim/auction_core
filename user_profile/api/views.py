from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.db.utils import DatabaseError
from django.utils import timezone
from ninja import Router

from api.auth import JWTAuth, ApiKeyAuth
from core.api.errors import OperationalError, UpdateError, CredentialError, GetError
from core.api.schemas import ErrorSchema, MsgSchema
from core.utils.auth import generate_token
from core.utils.builders import page_builder
from core.utils.validators import is_valid_email
from user_profile.api.schemas import ProfileSchema, CheckEmailSchema, SignUpSchema, SignInSchema, \
    UserTokenSchema, ProfileUpdateSchema, CreditSchema, CreditTransactionListSchema
from user_profile.enums import UserTypeEnum
from user_profile.models import Profile, Credit, CreditTransaction

router = Router(auth=[JWTAuth()])


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

    raise UpdateError("user")


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
    raise CredentialError("user")


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

            profile = Profile.objects.create(
                user_id=user.id, user_type=UserTypeEnum.BUYER if data.is_buyer else UserTypeEnum.SELLER)

            Credit.objects.create(
                user_id=user.id,
                balance=0,
                expiry=timezone.now()
            )

        return profile

    except DatabaseError:
        raise OperationalError("user_and_profile")


@router.get('/credit', response={200: CreditSchema, 422: ErrorSchema}, tags=['Credits'])
def get_credit(request):
    try:
        return Credit.objects.get(user_id=request.user.id, is_active=True)
    except Credit.DoesNotExist:
        raise GetError('credit')


@router.get('/credit/transactions', response=CreditTransactionListSchema, tags=['Credits'])
def get_credit_transactions(request, page_number: int = 1):
    transactions = CreditTransaction.objects.select_related(
        'credit').filter(credit__user_id=request.user.id)
    return page_builder(transactions, 10, page_number)
