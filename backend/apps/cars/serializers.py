from rest_framework import serializers

from .models import CarModel


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('id', 'brand', 'model', 'price', 'year', 'created_at', 'updated_at')


class CarPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('photo_car',)
        extra_kwargs = {
            'photo_car': {
                'required': True
            }
        }
