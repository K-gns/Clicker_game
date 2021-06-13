from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('click/', views.callClick, name="click"),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('cycles/', views.CycleList.as_view()),
    path('cycles/<int:pk>/', views.CycleDetail.as_view()),
    path('buyBoost/', views.buyBoost, name="buyBoost"),
    path('boosts/<int:mainCycle>/', views.BoostList.as_view()),
    path('set_main_cycle/', views.set_main_cycle),
]

urlpatterns = format_suffix_patterns(urlpatterns)
