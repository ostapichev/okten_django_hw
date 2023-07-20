from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.users.models import UserModel as User

from ..models import AutoParkModel

UserMode: User = get_user_model()


class AutoParkTestCase(APITestCase):
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

    def test_all_auto_parks_view(self):
        response = self.client.get(reverse('auto_parks_list_create'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_all_cars_view_auto_park(self):
        self._authenticate()
        auto_park_test = {'name': 'Uklon'}
        self.client.post(reverse('auto_parks_list_create'), auto_park_test, format='json')
        auto_park = AutoParkModel.objects.get(name=auto_park_test['name'])
        car_test1 = {
            "brand": "Audi",
            "body": "Sedan",
            "price": 12000,
            "year": 2010,
        }
        car_test2 = {
            "brand": "Suzuki",
            "body": "Jeep",
            "price": 15000,
            "year": 2006,
        }
        self.client.post(reverse('auto_park_car_list_create_view', kwargs={'pk': auto_park.id}),
                         car_test1, format='json')
        response = self.client.get(reverse('auto_park_car_list_create_view', kwargs={'pk': auto_park.id}))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_create_auto_park_without_auth(self):
        count = AutoParkModel.objects.count()
        sample_auto_park = {
            "name": "Uber"
        }
        response = self.client.post(reverse('auto_parks_list_create'), sample_auto_park)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(AutoParkModel.objects.count(), count)

    def test_create_auto_park(self):
        self._authenticate()
        count = AutoParkModel.objects.count()
        sample_auto_park = {
            "name": "Uber"
        }
        response = self.client.post(reverse('auto_parks_list_create'), sample_auto_park)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(AutoParkModel.objects.count(), count + 1)
        self.assertEquals(response.data['name'], 'Uber')
        self.assertIsInstance(response.data['cars'], list)

    def test_get_auto_park_id(self):
        self._authenticate()
        auto_park_test = {'name': 'Uklon'}
        self.client.post(reverse('auto_parks_list_create'), auto_park_test, format='json')
        auto_park = AutoParkModel.objects.get(name=auto_park_test['name'])
        response = self.client.get(reverse('auto_park_retrieve_update_destroy', kwargs={'pk': auto_park.id}))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_put_auto_park_id(self):
        self._authenticate()
        auto_park_test = {'name': 'Uklon'}
        self.client.post(reverse('auto_parks_list_create'), auto_park_test, format='json')
        auto_park = AutoParkModel.objects.get(name=auto_park_test['name'])
        response = self.client.put(reverse('auto_park_retrieve_update_destroy', kwargs={'pk': auto_park.id}),
                                   {'name': 'OneTaxi'})
        print(f'test put content: {response.data}')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_patch_auto_park_id(self):
        self._authenticate()
        auto_park_test = {'name': 'Uklon'}
        self.client.post(reverse('auto_parks_list_create'), auto_park_test, format='json')
        auto_park = AutoParkModel.objects.get(name=auto_park_test['name'])
        response = self.client.patch(reverse('auto_park_retrieve_update_destroy', kwargs={'pk': auto_park.id}),
                                     {'name': 'Taxi 838'})
        print(f'test patch content: {response.data}')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_delete_auto_park_id(self):
        self._authenticate()
        auto_park_test = {'name': 'Uklon'}
        self.client.post(reverse('auto_parks_list_create'), auto_park_test, format='json')
        auto_park = AutoParkModel.objects.get(name=auto_park_test['name'])
        response = self.client.delete(reverse('auto_park_retrieve_update_destroy', kwargs={'pk': auto_park.id}))
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
