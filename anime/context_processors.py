from django.contrib.auth.models import Group

def user_groups_context(request):
    if request.user.is_authenticated:
        return {
            'is_moderator': request.user.groups.filter(name='moderator').exists() if request.user.is_authenticated else False,
            'is_animeshnik': request.user.groups.filter(name='animeshnik').exists() if request.user.is_authenticated else False,
        }
    return {}