from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.users.models import UserModel as User

UserMode: User = get_user_model()


class CarTestCase(APITestCase):
    def _authenticate(self):
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
        user = UserMode.objects.get(email=user['email'])
        user.is_active = True
        user.is_staff = True
        user.save()
        response = self.client.post(reverse('auth_login'), {'email': email, 'password': password})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_get_cars(self):
        response = self.client.get(reverse('car_list_view'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)


