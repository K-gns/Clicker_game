from django.contrib.auth.models import User
from user_profile.models import MainCycle, Boost
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_profile.serializers import BoostSerializer

def main_page(request):
    user = User.objects.filter(id=request.user.id)
    if len(user) > 0:
        mainCycle = MainCycle.objects.filter(user=request.user)[0]
        return (False, 'index.html', {'user':user[0], 'mainCycle':mainCycle})
    else:
        return (True, 'login', {})

def callClick(request):
    mainCycle = MainCycle.objects.get(user=request.user)
    is_level_up = mainCycle.Click()
    boosts_query = Boost.objects.filter(mainCycle=mainCycle)
    boosts = BoostSerializer(boosts_query, many=True).data
    #print(boosts)
    mainCycle.save()
    if is_level_up:
        return ({"coinsCount":mainCycle.coinsCount,
                "boosts": boosts})
    return ({"coinsCount":mainCycle.coinsCount,
            "boosts": None})

def buy_boost(request):
    boost_level = request.data['boost_level']
    cycle = MainCycle.objects.filter(user=request.user)[0]
    boost = Boost.objects.get_or_create(mainCycle=cycle, level=boost_level)[0]
    main_cycle, level, price, power = boost.upgrade()
    boost.save()
    print(main_cycle, level, price, power)
    return (main_cycle, level, price, power)

def set_main_cycle(request):
    main_cycle = MainCycle.objects.get(user=request.user)
    is_level_up = main_cycle.set_main_cycle(int(request.data['coins_count']))
    boosts_query = Boost.objects.filter(mainCycle=main_cycle)
    boosts = BoostSerializer(boosts_query, many=True).data
    main_cycle.save()
    if is_level_up:
        return (main_cycle, boosts)
    return (main_cycle, None)
