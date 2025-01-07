from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls"), name="main"),
    path("services/", include("services.urls"), name="service"),
    path("explore/", include("explore.urls"), name="explore"),
    path("users/", include("users.urls"), name="users"),
    path("search/", include("search.urls"), name="search"),
]
