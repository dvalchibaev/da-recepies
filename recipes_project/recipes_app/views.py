from django.shortcuts import render, get_object_or_404
# from .models import Recipe, Category
from django.contrib.auth.decorators import login_required


def home(request):
    # Retrieve 5 random recipes to display on the home page
    # random_recipes = Recipe.objects.order_by('?')[:5]
    return render(request, 'recipes_app/home.html', {'recipes': 'None'})

