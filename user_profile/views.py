from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from user_profile.models import Profile


def all_profiles(request):
    profiles_queryset = Profile.objects.select_related('user')
    my_context = {
        'profiles': profiles_queryset,
    }
    return render(request, 'user_profile/all_profiles.html', context=my_context)
