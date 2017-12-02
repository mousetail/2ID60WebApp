import re

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import models as authmodels, password_validation, login

def register(request):
    usererror=emailerror=passworderror=password2error=""
    username = request.POST.get("username", "")
    email = request.POST.get("email", "")
    password = request.POST.get("password", "")
    password_2 = request.POST.get("password_2", "")
    
    try:
        otheruser = authmodels.User.objects.get(username=username)
        usererror = "Name \""+username+"\" allready taken"
    except authmodels.User.DoesNotExist:
        
        usererror = ""
        
    if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is None:
        emailerror = "Invalid email adress"
        
    try:
        password_validation.validate_password(password, username)
    except password_validation.ValidationError as ex:
        passworderror = ", ".join(ex.messages)
        
    if password!=password_2:
        password2error="passwords do not match"
    
    if (usererror == emailerror == passworderror == password2error == "" and
        "" not in (username, email, password, password_2)):
        user = authmodels.User.objects.create_user(username, email, password)
        user.save()
        login(request, user)
        return HttpResponseRedirect("/")
        
    return render(request, 'registration/register.html',
        {"username":username,
         "usererror":usererror,
         "emailerror":emailerror,
         "passworderror":passworderror,
         "password2error":password2error,
         "email":email,
         "password":password,
         "password2":password_2})

# Create your views here.
