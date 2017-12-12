from . import models


def viewbase(request):
    if request.user.is_authenticated:
        userinfo = models.BlogUser.objects.get(user=request.user)
        return {"base_username": request.user.username,
                "base_user_id": request.user.id,
                "base_user_image": userinfo.profilePicture}
    else:
        return {"base_username": ""}
