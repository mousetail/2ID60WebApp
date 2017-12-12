import re

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import models as authmodels, password_validation, login

from . import viewbase, models


def register(request):
    usererror = emailError = passworderror = password2error = ""
    registerToken = request.POST.get("registerToken", "")
    username = request.POST.get("username", "")
    email = request.POST.get("email", "")
    password = request.POST.get("password", "")
    password_2 = request.POST.get("password_2", "")

    try:
        otheruser = authmodels.User.objects.get(username=username)
        usererror = "Name \"" + username + "\" allready taken"
    except authmodels.User.DoesNotExist:

        usererror = ""

    if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is None:
        emailError = "Invalid email adress"

    try:
        password_validation.validate_password(password, username)
    except password_validation.ValidationError as ex:
        passworderror = ", ".join(ex.messages)

    if password != password_2:
        password2error = "passwords do not match"

    if (usererror == emailError == passworderror == password2error == "" and
                "" not in (username, email, password, password_2, registerToken)):
        user = authmodels.User.objects.create_user(username, email, password)
        user.clean() #fix email
        user.save()
        login(request, user)

        blogUser = models.BlogUser()
        blogUser.user = user
        blogUser.save()
        return HttpResponseRedirect("/home/registration_completed")

    if registerToken == "":
        emailError = ""
        password2error = ""

    return render(request, 'registration/register.html',
                  {"username": username,
                   "usererror": usererror,
                   "emailerror": emailError,
                   "passworderror": passworderror,
                   "password2error": password2error,
                   "email": email,
                   "password": password,
                   "password2": password_2,
                   **viewbase.viewbase(request)})

# Create your views here.
