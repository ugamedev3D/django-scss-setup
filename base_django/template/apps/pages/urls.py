
from django.urls import path

from apps.pages.views import Home


urlpatterns = [
    path("", Home, name="home"),
]
