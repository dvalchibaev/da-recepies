from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import Recipe, Category
from .forms import RecipeForm


def home(request):
    # Basic page
    return redirect('recipes')


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


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)
            return redirect('home')  # Redirect to the homepage or any other desired page
    else:
        form = UserCreationForm()
    return render(request, 'recipes_app/registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the homepage or any other desired page
    return render(request, 'recipes_app/login.html')


@login_required
def add_recipe(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        # If the request is a POST request, it means the form has been submitted
        form = RecipeForm(request.POST, request.FILES)  # Create a form instance with the POST data
        if form.is_valid():
            # If the form is valid, save the recipe
            new_recipe = form.save(commit=False)  # Create a new recipe instance, but don't save it to the database yet
            new_recipe.author = request.user  # Set the author to the currently logged-in user
            new_recipe.save()  # Save the recipe to the database

            # Add categories (if you have a multiple select field for categories)
            categories = request.POST.getlist('categories')
            new_recipe.categories.set(Category.objects.filter(pk__in=categories))

            return redirect('home')  # Redirect to the homepage or a different page after successful submission
    else:
        # If the request is a GET request, display the form
        form = RecipeForm()  # Create a new empty form instance

    return render(request, 'recipes_app/add_recipe.html', {'form': form, 'categories': categories})
