from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from .models import Recipe, Category


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'cooking_steps', 'time_to_cook', 'picture', 'categories']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')