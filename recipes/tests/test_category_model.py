from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized


class CategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Test category'
        )
        return super().setUp()

    def test_category_string_representation(self):
        self.assertEqual(
            str(self.category), 
            self.category.name
        )