from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Booking

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

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()