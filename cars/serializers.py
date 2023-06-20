from rest_framework import serializers

from cars.models import CarModel


class CarBaseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    brand = serializers.CharField(max_length=25)
    year = serializers.IntegerField()


class CarAllSerializer(CarBaseSerializer):
    pass


class CarSerializer(CarBaseSerializer):
    """
        Створити модель Car з такими полями:
            - марка машини
            - рік випуску
            - кількість місць
            - тип кузову
            - об'єм двигуна (float)
            реалізувати всі CRUD операції
            при виведені всіх машин показувати тільки (id, марку машини та рік)
    """
    num_seats = serializers.IntegerField()
    body_type = serializers.CharField(max_length=15)
    engine_volume = serializers.FloatField()

    def create(self, validated_data):
        return CarModel.objects.create(**validated_data)

    def update(self, instance, validated_data: dict):
        for k, v in validated_data.items():
            setattr(instance, k, v)

        instance.save()
        return instance
