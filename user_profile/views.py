from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import MainCycle, Boost
from .forms import UserForm
import json




def callClick(request):
    user = User.objects.filter(id=request.user.id)
    mainCycle = MainCycle.objects.filter(user=request.user)[0]
    mainCycle.Click()
    mainCycle.save()
    return HttpResponse(mainCycle.coinsCount)

def buyBoost(request):
    mainCycle = MainCycle.objects.filter(user=request.user)[0]
    if not mainCycle.boosts.filter():
        boost = Boost()
        boost.mainCycle = mainCycle
        boost.save()
    else:
        boost = mainCycle.boosts.filter()[0]
        boost.mainCycle = mainCycle
    boost.Upgrade()
    mainCycle.save()
    json1 = { "clickPower": mainCycle.clickPower, "boostPrice": mainCycle.boostPrice, "coinsCount": mainCycle.coinsCount }
    responseJson = json.dumps(json1)
    return HttpResponse(responseJson)


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
