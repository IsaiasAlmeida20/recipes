from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase, Recipe
class RecipeViewsTest(RecipeTestBase):
   
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(views.home, view.func)

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes in here 😢</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(200, response.status_code)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        response_context = response.context['recipes']
        response_content = response.content.decode('utf-8')
        self.assertIsInstance(response_context.first(), Recipe)
        self.assertEqual(len(response_context), 1)
        self.assertIn('Recipe Title', response_content)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes in here 😢</h1>',
            response.content.decode('utf-8')
        )


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

    def test_recipe_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(views.recipe, view.func)

    def test_recipe_view_returns_404_if_not_recipe(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(404, response.status_code)

    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=test')
        self.assertTemplateUsed(response, 'recipes/pages/search-view.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        response = self.client.get(reverse('recipes:search') + '?q=<test>')
        self.assertIn(
            '&lt;test&gt;',
            response.content.decode('utf-8')
        )
