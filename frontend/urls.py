from django.urls import path
from frontend import views
#from user_profile import views1 as user_profile_views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.user_login, name="login" ),
    path('logout/', views.user_logout),
    path('registration/', views.user_registration, name="registration"),

]
