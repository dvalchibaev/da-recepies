from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'cooking_steps', 'time_to_cook', 'picture', 'categories']
