from django.urls import path
from rest_framework.authtoken import views as auth_views

from api import views


urlpatterns = [
    path('register/', views.UserView.as_view()),
    path('api-token-auth/', auth_views.obtain_auth_token),
    path('hello/', views.hello_world),
]
