from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('recipes/', views.get_five_random_recipes, name='recipes'),
    path('recipe/<int:recipe_id>', views.get_recipe, name='recipe'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
]