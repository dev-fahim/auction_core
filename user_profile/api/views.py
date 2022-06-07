from ninja import Router

from core.utils.builders import page_builder
from user_profile.models import Profile
from user_profile.api.schemas import ProfileListSchema


router = Router()


@router.get('/all', tags=['User Profile'], response=ProfileListSchema)
def get_profiles(request, page_number: int = 1):
    profiles = Profile.objects.select_related('user', 'verified_by').order_by('-id')

    return page_builder(profiles, 10, page_number)
