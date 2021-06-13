from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerDetail, CycleSerializer, CycleSerializerDetail, BoostSerializer
from .models import MainCycle, Boost
from .forms import UserForm
import json
import services
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def callClick(request):
    data = services.clicker_services.callClick(request)
    return Response(data)

@api_view(['POST'])
def buyBoost(request):
    main_cycle, level, price, power = services.clicker_services.buy_boost(request)
    return Response({'clickPower': main_cycle.clickPower,
                    'coinsCount':main_cycle.coinsCount,
                    'auto_click_power': main_cycle.auto_click_power,
                    'level':level,
                    'price':price,
                    'power': power})

@api_view(['POST'])
def set_main_cycle(request):
    main_cycle, boosts = services.clicker_services.set_main_cycle(request)
    return Response({"coins_count": main_cycle.coinsCount,
                    "level": main_cycle.level,
                     "boosts": boosts,
                     "toNextLevel": main_cycle.toNextLevel})

from rest_framework import generics
from . import serializers
from django.contrib.auth.models import User


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class CycleList(generics.ListAPIView):
    queryset = MainCycle.objects.all()
    serializer_class = serializers.CycleSerializer

class CycleDetail(generics.RetrieveAPIView):
    queryset = MainCycle.objects.all()
    serializer_class = serializers.CycleSerializerDetail

class BoostList(generics.ListCreateAPIView):
    queryset = Boost
    serializer_class = BoostSerializer
    def get_queryset(self):
        return Boost.objects.filter(mainCycle=self.kwargs['mainCycle'])
