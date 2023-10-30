from django.shortcuts import render, get_object_or_404
from .models import Recipe, Category
from django.contrib.auth.decorators import login_required


def home(request):
    # Basic page
    return render(request, 'recipes_app/Base.html')


def recipies(request):
    # Retrieve 5 random recipes to display on the home page
    # random_recipes = Recipe.objects.order_by('?')[:5]
    return render(request, 'recipes_app/home.html')


def get_recipe(request, recipe_id):
    # Retrieve the recipe based on the provided recipe_id or return a 404 page if not found
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    # Define any additional data you want to pass to the template
    # For example, you might want to include related data like comments, ratings, or author information.

    context = {
        'recipe': recipe,
        # Add other context data here if needed
    }

    # Render the recipe detail page using the 'recipe_detail.html' template
    return render(request, 'recipes_app/recipe_detail.html', context)


def get_five_random_recipes(request):
    # Retrieve 5 random recipes from the database
    recipes = Recipe.objects.order_by('?')[:5]
    print(recipes)

    # Define any additional data you want to pass to the template
    # For example, you might want to include other information or featured recipes.

    context = {
        'recipies': recipes,
        # Add other context data here if needed
    }

    # Render the home page using the 'home.html' template
    return render(request, 'recipes_app/home.html', context)