from rest_framework import serializers

from apps.cars.models import CarModel


class CarSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        price = attrs.get('price')
        year = attrs.get('year')
        if price == year:
            raise serializers.ValidationError({'details': 'price == year'})
        return super().validate(attrs)

    def validate_brand(self, brand):
        if brand == 'Sas':
            raise serializers.ValidationError({'detail': 'brand == Sas'})
        return brand

    class Meta:
        model = CarModel
        fields = ('id', 'brand', 'body', 'price', 'year', 'created_at', 'updated_at')
