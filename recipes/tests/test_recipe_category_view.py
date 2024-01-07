from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase, Recipe
class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(views.category, view.func)

    def test_recipe_category_view_returns_404_if_not_recipes(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(404, response.status_code)

    def test_recipe_category_template_loads_recipes(self):
        title = 'this is a category test'
        self.make_recipe(title=title)
        response = self.client.get(reverse('recipes:category', args=(1,)))
        response_context = response.context['recipes']
        response_content = response.content.decode('utf-8')
        self.assertIn(title, response_content)

    def test_recipe_category_template_dont_load_recipe_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': recipe.category.id}))
        self.assertEqual(404, response.status_code)
