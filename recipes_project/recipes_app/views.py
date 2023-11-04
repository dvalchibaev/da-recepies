from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from fuzzywuzzy import fuzz, process

from .models import Recipe, Category, Profile
from .forms import RecipeForm, CategoryForm, ProfileForm
from . import utils


def home(request):
    # Retrieve 5 random recipes from the database
    recipes = Recipe.objects.order_by('?')[:5]
    print(recipes)

    context = {
        'recipies': recipes,
    }

    return render(request, 'recipes_app/home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
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
            return redirect('home')
    return render(request, 'recipes_app/login.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'recipes_app/edit_profile.html', {'form': form})


def recipies(request):
    return render(request, 'recipes_app/home.html')


def get_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    context = {
        'recipe': recipe,
        'steps': utils.make_cooking_steps_article(recipe.cooking_steps),
    }

    return render(request, 'recipes_app/recipe_detail.html', context)


@login_required
def add_recipe(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe.save()

            return redirect('home')
    else:
        form = RecipeForm()

    return render(request, 'recipes_app/add_recipe.html', {'form': form, 'categories': categories})


def find_best_matching_recipe(request, recipe_name):
    all_recipe_names = Recipe.objects.values_list('name', flat=True)

    best_match = process.extractOne(recipe_name, all_recipe_names)

    if best_match[1] >= 50:
        return best_match[0]

    return None


def get_recipe_by_name(request, recipe_name):
    best_matching_recipe = find_best_matching_recipe(request, recipe_name)
    if best_matching_recipe:
        recipe = Recipe.objects.filter(name=best_matching_recipe).first()
        return redirect('recipe', recipe_id=recipe.id)

    return render(request, 'recipes_app/no_recipe_found.html')


@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    categories = Category.objects.all()

    if request.user == recipe.author:
        if request.method == 'POST':
            form = RecipeForm(request.POST, instance=recipe)
            if form.is_valid():
                form.save()
                return redirect('recipe_detail', recipe.id)  # Redirect to the recipe detail page
        else:
            form = RecipeForm(instance=recipe)
        return render(request,
                      'recipes_app/edit_recipe.html',
                      {'form': form, 'recipe': recipe, 'categories': categories}
                      )
    else:
        return redirect('home')


def get_recipes(request, user=None):
    if user:
        user_obj = User.objects.filter(username=user).first()
        if user_obj:
            recipes = Recipe.objects.filter(author=user_obj)
        else:
            recipes = []
    else:
        recipes = Recipe.objects.all()

    context = {
        'recipes': recipes
    }

    return render(request, 'recipes_app/recipe_list.html', context)


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save()
            return redirect('home')
    else:
        form = CategoryForm()

    return render(request, 'recipes_app/add_category.html', {'form': form})


def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'recipes_app/all_categories.html', {'categories': categories})


def search(request):
    if request.method == 'GET':
        # Retrieve the recipe name from the query parameter
        recipe_name = request.GET.get('recipe_name')

        if recipe_name:
            # If a recipe name is provided, redirect to the 'get_recipe_by_name' view
            return redirect('recipe_by_name', recipe_name=recipe_name)

    # Handle other cases, such as invalid searches or empty queries
    return render(request, '/recipes_app/no_recipe_found.html')
