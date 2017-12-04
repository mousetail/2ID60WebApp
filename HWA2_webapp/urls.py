"""HWA2_webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from blog.views import register
from blog.index import index, postEntry, viewEntry

urlpatterns = [
    url(r'^$', index),
    url(r'^home/$', index),
    url(r'^home/(?P<message>[_a-zA-Z]+)/$', index),
    url(r'^view/(?P<num>[0-9]+)/$', viewEntry),
    url(r'^post$', postEntry),
    url(r'^post/(?P<pk>[0-9]+)/$', postEntry),
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/', register),
    url(r'^accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
