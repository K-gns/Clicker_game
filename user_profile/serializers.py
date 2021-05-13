from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MainCycle


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'cycle', 'email', 'last_login', 'is_staff']

class UserSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'cycle', 'email', 'last_login', 'is_staff']

class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCycle
        fields = ['id']

class CycleSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = MainCycle
        fields = ['id', 'user', 'coinsCount', 'clickPower', 'boostPrice', 'boosts']
