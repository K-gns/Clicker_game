from rest_framework import serializers
from .models import MainCycle, User, Boost


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
        fields = ['id', 'user', 'coinsCount', 'clickPower', 'boosts', 'auto_click_power', 'level', 'toNextLevel']

class BoostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boost
        fields = ['level', 'power', 'price', 'boost_type']
