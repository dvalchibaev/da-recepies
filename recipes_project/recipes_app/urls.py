from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipies/', views.get_five_random_recipes, name='recipies'),
]