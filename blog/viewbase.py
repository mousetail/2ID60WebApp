def viewbase(request):
    if request.user:
        return {"base_username": request.user.username}
    else:
        return {"base_username", ""}