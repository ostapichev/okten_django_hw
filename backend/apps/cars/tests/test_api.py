from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.auto_parks.models import AutoParkModel
from apps.cars.models import CarModel
from apps.users.models import UserModel as User

UserModel: User = get_user_model()


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
        user = UserModel.objects.get(email=user['email'])
        user.is_active = True
        user.is_staff = True
        user.save()
        response = self.client.post(reverse('auth_login'), {'email': email, 'password': password})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

    def test_all_get_cars(self):
        """Test method GET all cars of class CarListView"""
        self._authenticate()
        sample_auto_park = {
            'name': 'Uklon'
        }
        self.client.post(reverse('auto_parks_list_create'), sample_auto_park, format='json')
        auto_park = AutoParkModel.objects.get(name=sample_auto_park['name'])
        sample_car = {
            "brand": "Audi",
            "body": "Sedan",
            "price": 12000,
            "year": 2010,
        }
        self.client.post(reverse('auto_park_car_list_create_view', kwargs={'pk': auto_park.id}),
                         sample_car, format='json')
        response = self.client.get(reverse('car_list_view'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_car_id(self):
        """Test method GET car by id of class CarRetrieveUpdateDestroyView"""
        self._authenticate()
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
        self.client.post(reverse('auto_park_car_list_create_view', kwargs={'pk': auto_park.id}),
                         sample_car, format='json')
        car = CarModel.objects.get(brand=sample_car['brand'])
        response = self.client.get(reverse('car_retrieve_update_destroy', kwargs={'pk': car.id}))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_put_car_id(self):
        """Test method PUT car by id of class CarRetrieveUpdateDestroyView"""
        self._authenticate()
        sample_auto_park = {
            'name': 'Uklon'
        }
        sample_car = {
            "brand": "Audi",
            "body": "Sedan",
            "price": 12000,
            "year": 2010,
        }
        car_update = {
            'brand': 'Suzuki',
            'body': 'Jeep',
            'price': 20000,
            'year': 2007
        }
        self.client.post(reverse('auto_parks_list_create'), sample_auto_park, format='json')
        auto_park = AutoParkModel.objects.get(name=sample_auto_park['name'])
        self.client.post(reverse('auto_park_car_list_create_view', kwargs={'pk': auto_park.id}),
                         sample_car, format='json')
        car = CarModel.objects.get(brand=sample_car['brand'])
        response = self.client.put(reverse('car_retrieve_update_destroy', kwargs={'pk': car.id}), car_update)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['brand'], car_update['brand'])
        self.assertEquals(response.data['body'], car_update['body'])
        self.assertEquals(response.data['price'], car_update['price'])
        self.assertEquals(response.data['year'], car_update['year'])

    def test_patch_car_id(self):
        """Test method PATCH car by id of class CarRetrieveUpdateDestroyView"""
        self._authenticate()
        sample_auto_park = {
            'name': 'Uklon'
        }
        sample_car = {
            "brand": "Audi",
            "body": "Sedan",
            "price": 12000,
            "year": 2010,
        }
        car_update = {
            'price': 20000
        }
        self.client.post(reverse('auto_parks_list_create'), sample_auto_park, format='json')
        auto_park = AutoParkModel.objects.get(name=sample_auto_park['name'])
        self.client.post(reverse('auto_park_car_list_create_view', kwargs={'pk': auto_park.id}),
                         sample_car, format='json')
        car = CarModel.objects.get(brand=sample_car['brand'])
        response = self.client.patch(reverse('car_retrieve_update_destroy', kwargs={'pk': car.id}), car_update)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['price'], car_update['price'])

    def test_delete_car_id(self):
        """Test method DELETE car by id of class CarRetrieveUpdateDestroyView"""
        self._authenticate()
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
        self.client.post(reverse('auto_park_car_list_create_view', kwargs={'pk': auto_park.id}),
                         sample_car, format='json')
        car = CarModel.objects.get(brand=sample_car['brand'])
        response = self.client.delete(reverse('car_retrieve_update_destroy', kwargs={'pk': car.id}))
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
