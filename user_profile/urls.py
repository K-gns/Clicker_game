from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.user_login, name="login" ),
    path('logout/', views.user_logout, name="logout"),
    path('registration/', views.user_registration, name="registration"),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
