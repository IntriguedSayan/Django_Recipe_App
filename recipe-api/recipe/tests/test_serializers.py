import pytest;
from django.urls import reverse;
from rest_framework import status;
from rest_framework.test import APIClient;
from recipe.models import Recipe, RecipeCategory, RecipeLike;
from django.contrib.auth.models import User;

@pytest.fixture
def api_client():
    return APIClient();

@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpassword");

@pytest.fixture
def recipe(user, recipe_category):
    return Recipe.objects.create(
        title = "Test Recipe",
        desc = "Test Description",
        cook_time = "30 minutes",
        ingredients = "Test Ingredients",
        procedure = "Test Procedure",
        author = user,
        category = recipe_category
    );

@pytest.fixture
class TestRecipeListAPIView:
    def test_list_recipes(self, api_client, recipe):
        url = reverse("recipe-list");
        response = api_client.get(url);
        assert response.status_code == status.HTTP_200_OK;
        assert len(response.data) == 1;

@pytest.mark.django_db
class TestRecipeCreateAPIView:
    def test_create_recipe(self, api_client, user, recipe_category):
        api_client.force_authenticate(user=user)
        url = reverse('recipe-create')
        data = {
            'title': 'New Recipe',
            'desc': 'New Description',
            'cook_time': '45 minutes',
            'ingredients': 'New Ingredients',
            'procedure': 'New Procedure',
            'category': {'id': recipe_category.id, 'name': recipe_category.name}
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
class TestRecipeAPIView:
    def test_retrieve_recipe(self, api_client, recipe):
        url = reverse('recipe-detail', kwargs={'pk': recipe.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == recipe.title

    def test_update_recipe(self, api_client, user, recipe):
        api_client.force_authenticate(user=user)
        url = reverse('recipe-detail', kwargs={'pk': recipe.id})
        data = {'title': 'Updated Recipe'}
        response = api_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Recipe'

    def test_delete_recipe(self, api_client, user, recipe):
        api_client.force_authenticate(user=user)
        url = reverse('recipe-detail', kwargs={'pk': recipe.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
class TestRecipeLikeAPIView:
    def test_like_recipe(self, api_client, user, recipe):
        api_client.force_authenticate(user=user)
        url = reverse('recipe-like', kwargs={'pk': recipe.id})
        response = api_client.post(url)
        assert response.status_code == status.HTTP_201_CREATED

    def test_unlike_recipe(self, api_client, user, recipe):
        RecipeLike.objects.create(user=user, recipe=recipe)
        api_client.force_authenticate(user=user)
        url = reverse('recipe-like', kwargs={'pk': recipe.id})
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_200_OK