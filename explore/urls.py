from django.urls import path
from . import views

urlpatterns = [
    path("", views.explore_home, name="explore"),
    path("flowers/", views.explore_flowers, name="explore_flowers"),
    path("fruits/", views.explore_fruits, name="explore_fruits"),
    path("leaves/", views.explore_leaves, name="explore_leaves"),
    path("roots/", views.explore_roots, name="explore_roots"),
    path("gums/", views.explore_gums, name="explore_gums"),
    path("specific_plant/<slug:slug>/", views.specific_plant, name="specific_plant"),
    path("search/", views.search_plants, name="search_plants"),
]