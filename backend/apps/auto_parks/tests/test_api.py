from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.users.models import UserModel as User

from ...cars.models import CarModel
from ..models import AutoParkModel

UserMode: User = get_user_model()


class AutoParkTestCase(APITestCase):
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
        user = UserMode.objects.get(email=user['email'])
        user.is_active = True
        user.is_staff = True
        user.save()
        response = self.client.post(reverse('auth_login'), {'email': email, 'password': password})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_all_auto_parks_view(self):
        """Test method GET of class AutoParkListCreateView"""
        sample_auto_park1 = {
            "name": "Uber"
        }
        sample_auto_park2 = {
            "name": "Taxi 30-40"
        }
        sample_auto_park3 = {
            "name": "Taxi 838"
        }
        self.client.post(reverse('auto_parks_list_create'), sample_auto_park1)
        self.client.post(reverse('auto_parks_list_create'), sample_auto_park2)
        self.client.post(reverse('auto_parks_list_create'), sample_auto_park3)
        response = self.client.get(reverse('auto_parks_list_create'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_create_auto_park_without_auth(self):
        """Test method POST of class AutoParkListCreateView without auth"""
        count = AutoParkModel.objects.count()
        sample_auto_park = {
            "name": "Uber"
        }
        response = self.client.post(reverse('auto_parks_list_create'), sample_auto_park)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEquals(AutoParkModel.objects.count(), count)

    def test_create_auto_park(self):
        """Test method POST of class AutoParkListCreateView with auth"""
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
        """Test method GET of class AutoParkRetrieveUpdateDestroyView"""
        self._authenticate()
        sample_auto_park = {
            'name': 'Uklon'
        }
        self.client.post(reverse('auto_parks_list_create'), sample_auto_park, format='json')
        auto_park = AutoParkModel.objects.get(name=sample_auto_park['name'])
        response = self.client.get(reverse('auto_park_retrieve_update_destroy', kwargs={'pk': auto_park.id}))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_put_auto_park_id(self):
        """Test method PUT of class AutoParkRetrieveUpdateDestroyView"""
        self._authenticate()
        sample_auto_park = {
            'name': 'Uklon'
        }
        update_auto_park = {
            'name': 'One Taxi'
        }
        self.client.post(reverse('auto_parks_list_create'), sample_auto_park, format='json')
        auto_park = AutoParkModel.objects.get(name=sample_auto_park['name'])
        response = self.client.put(reverse(
            'auto_park_retrieve_update_destroy',
            kwargs={'pk': auto_park.id}),
            update_auto_park)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['name'], update_auto_park['name'])

    def test_patch_auto_park_id(self):
        """Test method PATCH of class AutoParkRetrieveUpdateDestroyView"""
        self._authenticate()
        sample_auto_park = {
            'name': 'Uklon'
        }
        update_auto_park = {
            'name': 'One Taxi'
        }
        self.client.post(reverse('auto_parks_list_create'), sample_auto_park, format='json')
        auto_park = AutoParkModel.objects.get(name=sample_auto_park['name'])
        response = self.client.patch(reverse(
            'auto_park_retrieve_update_destroy',
            kwargs={'pk': auto_park.id}),
            update_auto_park)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['name'], update_auto_park['name'])

    def test_delete_auto_park_id(self):
        """Test method DELETE auto park by id of class AutoParkRetrieveUpdateDestroyView"""
        self._authenticate()
        sample_auto_park = {
            'name': 'Uklon'
        }
        self.client.post(reverse('auto_parks_list_create'), sample_auto_park, format='json')
        auto_park = AutoParkModel.objects.get(name=sample_auto_park['name'])
        response = self.client.delete(reverse('auto_park_retrieve_update_destroy', kwargs={'pk': auto_park.id}))
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_all_get_cars_auto_park(self):
        """Test method GET all cars in auto park by id of class AutoParkCarListCreateView"""
        self._authenticate()
        sample_auto_park = {
            'name': 'Uklon'
        }
        sample_car1 = {
            "brand": "Audi",
            "body": "Sedan",
            "price": 12000,
            "year": 2010,
        }
        sample_car2 = {
            "brand": "Mazda",
            "body": "Sedan",
            "price": 15000,
            "year": 2020,
        }
        self.client.post(reverse('auto_parks_list_create'), sample_auto_park, format='json')
        auto_park = AutoParkModel.objects.get(name=sample_auto_park['name'])
        self.client.post(reverse(
            'auto_park_car_list_create_view',
            kwargs={'pk': auto_park.id}),
            sample_car1, format='json')
        self.client.post(reverse(
            'auto_park_car_list_create_view',
            kwargs={'pk': auto_park.id}),
            sample_car2, format='json')
        response = self.client.get(reverse('auto_park_car_list_create_view', kwargs={'pk': auto_park.id}))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data[0]['brand'], sample_car1['brand'])
        self.assertEquals(response.data[1]['brand'], sample_car2['brand'])

    def test_all_create_cars_auto_park(self):
        """Test method POST create car in auto park by id of class AutoParkCarListCreateView"""
        self._authenticate()
        count = CarModel.objects.count()
        sample_auto_park = {
            'name': 'Uklon'
        }
        sample_car = {
            "brand": "Audi",
            "body": "Sedan",
            "price": 12000,
            "year": 2010,
        }
        self.client.post(reverse('auto_parks_list_create'), sample_auto_park, format='json')
        auto_park = AutoParkModel.objects.get(name=sample_auto_park['name'])
        response = self.client.post(reverse(
            'auto_park_car_list_create_view',
            kwargs={'pk': auto_park.id}),
            sample_car, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(CarModel.objects.count(), count + 1)
        self.assertEquals(response.data['brand'], 'Audi')
