from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Recipe, Category, User


class RecipeViewsTest(TestCase):
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
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='username@email.com',
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            cover = SimpleUploadedFile("fake_image.jpg", b"file_content", content_type="image/jpeg"),
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True,
        )
        response = self.client.get(reverse('recipes:home'))
        response_context = response.context['recipes']
        response_content = response.content.decode('utf-8')
        self.assertIsInstance(response_context.first(), Recipe)
        self.assertEqual(len(response_context), 1)
        self.assertIn('Recipe Title', response_content)


    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(views.category, view.func)

    def test_recipe_category_view_returns_404_if_not_recipes(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(404, response.status_code)

    def test_recipe_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(views.recipe, view.func)

    def test_recipe_view_returns_404_if_not_recipe(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(404, response.status_code)
