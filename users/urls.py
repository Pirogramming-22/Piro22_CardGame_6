from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.card_main, name="card_main"),
]