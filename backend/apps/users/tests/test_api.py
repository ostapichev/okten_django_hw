from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.users.models import UserModel as User

UserModel: User = get_user_model()


class UserTestCase(APITestCase):
    def _authenticate(self):
        """Authenticate user"""
        email = 'admin@gmail.com'
        password = 'P@$$word1'
        user = {
            'email': email,
            'password': password,
            'profile': {
                'name': 'Иван',
                'surname': 'Иванов',
                'age': 20
            }
        }
        self.client.post(reverse('users_list_create'), user, format='json')
        user = UserModel.objects.get(email=user['email'])
        user.is_active = True
        user.is_staff = True
        user.save()
        response = self.client.post(reverse('auth_login'), {'email': email, 'password': password})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_all_get_users_with_auth(self):
        """Test method GET all users with auth for class UserListCreateView"""
        self._authenticate()
        sample_user = {
            'email': 'user@gmail.com',
            'password': 'P@$$word1',
            'profile': {
                'name': 'Петя',
                'surname': 'Петров',
                'age': 20
            }
        }
        self.client.post(reverse('users_list_create'), sample_user, format='json')
        response = self.client.get(reverse('users_list_create'), sample_user, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_all_get_users_without_auth(self):
        """Test method GET all users without auth for class UserListCreateView"""
        sample_user = {
            'email': 'user@gmail.com',
            'password': 'P@$$word1',
            'profile': {
                'name': 'Петя',
                'surname': 'Петров',
                'age': 20
            }
        }
        self.client.post(reverse('users_list_create'), sample_user, format='json')
        response = self.client.get(reverse('users_list_create'), sample_user, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_all_post_user(self):
        """Test method POST create new user for class UserListCreateView"""
        count = UserModel.objects.count()
        sample_user = {
            'email': 'user@gmail.com',
            'password': 'P@$$word1',
            'profile': {
                'name': 'Петя',
                'surname': 'Петров',
                'age': 20
            }
        }
        response = self.client.post(reverse('users_list_create'), sample_user, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(UserModel.objects.count(), count + 1)
        self.assertEquals(response.data['email'], sample_user['email'])