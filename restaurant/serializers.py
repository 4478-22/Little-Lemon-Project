from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Booking, Menu

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['first_name', 'reservation_date', 'reservation_slot']

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'description', 'price']  # Adjust fields as necessary

    def create(self, validated_data):
        menu_item = Menu(**validated_data)
        menu_item.save()
        return menu_item

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()